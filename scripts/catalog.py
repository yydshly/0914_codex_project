"""Maintain the research catalog using only the Python standard library."""

import argparse
from datetime import date
import html
import json
from pathlib import Path
import re
import shutil
import sys
from urllib.parse import quote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
STATUSES = {"待研究", "研究中", "已完成", "已归档"}
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def https_url(value):
    parts = urlsplit(value)
    return (parts.scheme == "https" and bool(parts.hostname)
            and not parts.username and not parts.password
            and not any(char.isspace() for char in value))


def folder(project):
    return f"projects/{project['id']}-{project['slug']}"


def md(value):
    value = html.escape(value, quote=False)
    return re.sub(r"([\\`*_{}\[\]()#+.!|>~-])", r"\\\1", value)


def link(label, target):
    return f"[{md(label)}]({quote(target, safe='/:#?=&%+@~')})"


def load_projects():
    data = json.loads((ROOT / "projects.json").read_text(encoding="utf-8"))
    require(isinstance(data, dict) and isinstance(data.get("projects"), list),
            "projects.json 必须包含 projects 数组")
    projects = data["projects"]
    ids, slugs, registered = set(), set(), set()
    for project in projects:
        require(isinstance(project, dict), "每个项目必须是一个对象")
        for key in ("id", "slug", "name", "repo", "summary", "status",
                    "cover", "cover_alt", "demo"):
            value = project.get(key)
            require(isinstance(value, str) and not any(c in value for c in "\r\n"),
                    f"{key} 必须是单行字符串")
        pid = project["id"]
        require(bool(re.fullmatch(r"[0-9]{3,}", pid)) and int(pid) > 0
                and pid == f"{int(pid):03d}", f"编号无效：{pid}")
        require(pid not in ids, f"编号重复：{pid}")
        require(bool(SLUG.fullmatch(project["slug"])), f"slug 无效：{pid}")
        require(project["slug"] not in slugs, f"slug 重复：{pid}")
        require(type(project.get("order")) is int and project["order"] > 0,
                f"order 必须是正整数：{pid}")
        require(project["name"].strip() and project["summary"].strip(),
                f"名称和摘要不能为空：{pid}")
        require(project["status"] in STATUSES, f"状态无效：{pid}")
        require(https_url(project["repo"]), f"上游地址必须是 HTTPS：{pid}")
        require(not project["demo"] or https_url(project["demo"]),
                f"演示地址必须是 HTTPS 或空字符串：{pid}")
        require(isinstance(project.get("tags"), list) and all(
            isinstance(tag, str) and tag.strip() and not any(c in tag for c in "\r\n")
            for tag in project["tags"]), f"tags 必须是单行非空字符串数组：{pid}")
        directory = ROOT / folder(project)
        require((directory / "README.md").is_file(), f"缺少研究 README：{pid}")
        cover = project["cover"]
        if cover:
            image = (ROOT / cover).resolve()
            require(image.is_relative_to((directory / "assets").resolve()),
                    f"封面必须位于本项目 assets 目录：{pid}")
            require(cover.startswith(folder(project) + "/assets/")
                    and "\\" not in cover and ".." not in Path(cover).parts,
                    f"封面必须使用相对仓库根目录的正斜杠路径：{pid}")
            require(image.is_file(), f"封面文件不存在：{cover}")
            require(image.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"},
                    f"不支持的封面格式：{cover}")
            require(project["cover_alt"].strip(), f"请填写封面说明：{pid}")
        ids.add(pid)
        slugs.add(project["slug"])
        registered.add(directory.name)
    actual = {p.name for p in (ROOT / "projects").iterdir() if p.is_dir()}
    require(actual == registered,
            f"存在未登记项目目录：{', '.join(sorted(actual - registered))}")
    return projects


def render(projects):
    if not projects:
        return ("暂无研究项目。添加首个项目后，这里会自动生成有序索引。",
                "待添加项目摘要和截图。")
    rows = ["| 顺序 | 编号 | 项目 | 源库 | 能力摘要 | 状态 | 演示 |",
            "| --- | --- | --- | --- | --- | --- | --- |"]
    previews = []
    for position, project in enumerate(sorted(projects, key=lambda p: (p["order"], int(p["id"]))), 1):
        detail = folder(project) + "/README.md"
        demo = link("在线演示", project["demo"]) if project["demo"] else "—"
        source_name = urlsplit(project["repo"]).path.rstrip("/").split("/")[-1]
        rows.append(f"| {position} | {project['id']} | {link(project['name'], detail)} | "
                    f"{link(source_name, project['repo'])} | "
                    f"{md(project['summary'])} | {project['status']} | {demo} |")
        block = [f"### {project['id']} · {md(project['name'])}", "", md(project["summary"]), ""]
        if project["cover"]:
            block += ["!" + link(project["cover_alt"], project["cover"]), ""]
        entries = [link("研究记录", detail), link("上游仓库", project["repo"])]
        if project["demo"]:
            entries.append(demo)
        block.append(" · ".join(entries))
        if project["tags"]:
            block += ["", "标签：" + " / ".join(md(tag) for tag in project["tags"])]
        previews.append("\n".join(block))
    return "\n".join(rows), "\n\n".join(previews)


def updated_readme(projects):
    content = (ROOT / "README.md").read_text(encoding="utf-8")
    for section, body in zip(("PROJECT_INDEX", "PROJECT_PREVIEWS"), render(projects)):
        start, end = f"<!-- {section}:START -->", f"<!-- {section}:END -->"
        require(content.count(start) == 1 and content.count(end) == 1
                and content.index(start) < content.index(end),
                f"README 中的 {section} 标记缺失、重复或顺序错误")
        before, rest = content.split(start)
        _, after = rest.split(end)
        content = before + start + "\n" + body + "\n" + end + after
    return content


def write(path, content):
    path.write_text(content, encoding="utf-8", newline="\n")


def add(args, projects):
    require(bool(SLUG.fullmatch(args.slug)), "slug 请使用小写英文、数字和单个连字符")
    require(not any(p["slug"] == args.slug for p in projects), "slug 已存在")
    require(https_url(args.repo), "上游仓库请使用 HTTPS 地址")
    for value in (args.name, args.summary):
        require(value.strip() and not any(c in value for c in "\r\n"), "名称和摘要必须是单行非空文本")
    pid = f"{max((int(p['id']) for p in projects), default=0) + 1:03d}"
    project = dict(id=pid, order=max((p["order"] for p in projects), default=0) + 10,
                   slug=args.slug, name=args.name, repo=args.repo, summary=args.summary,
                   status="待研究", tags=[], cover="", cover_alt="", demo="")
    updated_readme(projects)  # Check markers before creating any files.
    destination = ROOT / folder(project)
    require(not destination.exists(), f"目录已存在：{destination.name}")
    template = (ROOT / "templates/project/README.md").read_text(encoding="utf-8")
    values = {"ID": pid, "NAME": md(args.name), "SUMMARY": md(args.summary),
              "REPO": link("上游仓库", args.repo), "DATE": date.today().isoformat()}
    template = re.sub(r"\{\{(ID|NAME|SUMMARY|REPO|DATE)\}\}",
                      lambda match: values[match[1]], template)
    shutil.copytree(ROOT / "templates/project", destination)
    write(destination / "README.md", template)
    projects.append(project)
    write(ROOT / "projects.json", json.dumps({"projects": projects}, ensure_ascii=False, indent=2) + "\n")
    write(ROOT / "README.md", updated_readme(load_projects()))
    print(f"Created {folder(project)} and updated README.md")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    new = commands.add_parser("add", help="Create the next numbered research project")
    new.add_argument("slug")
    new.add_argument("--name", required=True)
    new.add_argument("--repo", required=True)
    new.add_argument("--summary", required=True)
    commands.add_parser("sync", help="Update the root README from projects.json")
    commands.add_parser("check", help="Validate metadata and detect an outdated README")
    args = parser.parse_args()
    try:
        projects = load_projects()
        if args.command == "add":
            add(args, projects)
        else:
            expected = updated_readme(projects)
            if args.command == "sync":
                write(ROOT / "README.md", expected)
                print("README.md updated")
            else:
                require((ROOT / "README.md").read_text(encoding="utf-8") == expected,
                        "首页索引已过期，请运行 python scripts/catalog.py sync")
                print(f"Catalog OK: {len(projects)} projects")
    except (ValueError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
