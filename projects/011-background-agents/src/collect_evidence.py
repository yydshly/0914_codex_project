"""Index a pinned upstream checkout. This is static evidence collection, not a runtime test."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

COMMIT = "4c470da615eaecbf8f64b0ae5a04666c99b4c536"
BASE = "https://github.com/ColeMurray/background-agents"
PROJECT = Path(__file__).resolve().parents[1]
SOURCES = [
    ("S01", "项目名称、功能与单租户边界", "README.md", ["# Background Agents: Open-Inspect", "No per-user repository access validation", "Ad-hoc sets"]),
    ("S02", "运行流程、会话与环境恢复", "docs/HOW_IT_WORKS.md", ["## How Prompts Flow", "## The Agent", "## The Sandbox Lifecycle"]),
    ("S03", "任务排队、分发与并发认领", "packages/control-plane/src/session/message-queue.ts", ["async processMessageQueue", "getProcessingMessage()", "startMessageProcessing(", "spawnSandbox()", "queueDepth >= MAX_UNFINISHED_PROMPTS"]),
    ("S04", "断线存活与代理调用", "packages/sandbox-runtime/src/sandbox_runtime/bridge.py", ["prompt tasks must survive WS disconnects", "await self.harness.run_prompt", "harness must not emit execution_complete"]),
    ("S05", "代理统一接口", "packages/sandbox-runtime/src/sandbox_runtime/harness/base.py", ["class HarnessId", "class AgentHarness", "class TurnOutcome"]),
    ("S06", "运行层与模型兼容性", "packages/shared/src/harnesses.ts", ["HARNESS_IDS", 'modelFamilies: ["anthropic"]', "checkHarnessCompatibility"]),
    ("S07", "子会话的深度、仓库与基准分支", "packages/control-plane/src/routes/session-child-spawn.ts", ["MAX_SPAWN_DEPTH = 2", "child sessions are single-repo by design", "Child sessions must use the same repository", "spawnContext.baseBranch"]),
    ("S08", "PR 创建时的身份选择", "packages/control-plane/src/session/pull-request-service.ts", ["input.promptingAuth ?? appAuth", "sourceControlProvider.createPullRequest"]),
    ("S09", "自动化种类、间隔与失败暂停", "docs/AUTOMATIONS.md", ["Linear Event", "15 minutes", "3 consecutive", "scheduled automations only"]),
    ("S10", "Node 容器部署与单实例假设", "docs/CONTROL_PLANE_CONTAINER.md", ["one Node process", "The web app is not part of the stack", "Two processes at once"]),
    ("S11", "沙箱供应商工厂", "packages/control-plane/src/sandbox/provider-factory.ts", ['case "daytona"', 'case "e2b"', 'case "modal"', 'case "vercel"', 'case "opencomputer"']),
    ("S12", "Modal 状态恢复能力声明", "packages/control-plane/src/sandbox/providers/modal-provider.ts", ["supportsSnapshots: true", "supportsPersistentResume: false"]),
    ("S13", "Daytona 状态恢复能力声明", "packages/control-plane/src/sandbox/providers/daytona-provider.ts", ["supportsSnapshots: false", "supportsPersistentResume: true"]),
    ("S14", "E2B 状态恢复能力声明", "packages/control-plane/src/sandbox/providers/e2b-provider.ts", ["supportsSnapshots: false", "supportsPersistentResume: true"]),
    ("S15", "Vercel 状态恢复能力声明", "packages/control-plane/src/sandbox/providers/vercel/provider.ts", ["supportsSnapshots: true", "supportsPersistentResume: false"]),
    ("S16", "OpenComputer 状态恢复能力声明", "packages/control-plane/src/sandbox/providers/opencomputer-provider.ts", ["supportsSnapshots: true", "supportsPersistentResume: true"]),
    ("S17", "复用指令与技能版本", "docs/MANAGED_SKILLS.md", ["Managed skills give agents", "permission boundary"]),
    ("S18", "上游许可证", "LICENSE", ["MIT License", "Copyright"]),
    ("S19", "Node 最低版本", "package.json", ['"node": ">=22.13.0"']),
    ("S20", "单会话待完成任务上限", "packages/shared/src/types/prompts.ts", ["MAX_UNFINISHED_PROMPTS = 50"]),
    ("S21", "部署指南", "docs/SETUP_GUIDE.md", ["Full Self-Hosted Deployment"]),
    ("S22", "模型与供应商目录", "docs/AVAILABLE_MODELS.md", ["## Harnesses", "## OpenAI", "## OpenCode Go", "## DeepSeek"]),
    ("S23", "Claude 程序、SDK 与认证配置", "docs/CLAUDE_AGENT.md", ["Settings > Provider Accounts", "claude", "ANTHROPIC_API_KEY"]),
    ("S24", "OpenAI 账号与 API Key 接入", "docs/OPENAI_MODELS.md", ["Use API key", "access-token"]),
    ("S25", "OpenCode 服务运行方式", "packages/sandbox-runtime/src/sandbox_runtime/harness/opencode.py", ["opencode serve", "HTTP/SSE"]),
]


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkout", type=Path)
    args = parser.parse_args()
    actual = git(args.checkout, "rev-parse", "HEAD").decode().strip()
    if actual != COMMIT:
        raise SystemExit(f"Expected {COMMIT}; found {actual}. Use the pinned revision.")
    records = []
    missing = []
    for sid, title, path, needles in SOURCES:
        raw = git(args.checkout, "show", f"{COMMIT}:{path}")
        lines = raw.decode("utf-8").splitlines()
        matches = []
        for needle in needles:
            numbers = [i for i, line in enumerate(lines, 1) if needle in line]
            if not numbers:
                missing.append(f"{sid}: {needle}")
            matches.append({"query": needle, "lines": numbers})
        records.append({"id": sid, "title": title, "path": path,
                        "sha256": hashlib.sha256(raw).hexdigest(),
                        "line_count": len(lines), "url": f"{BASE}/blob/{COMMIT}/{path}",
                        "matches": matches})
    if missing:
        raise SystemExit("Evidence anchors missing:\n" + "\n".join(missing))
    output = {"upstream": BASE, "commit": COMMIT, "method": "static source/document inspection",
              "runtime_validated": False, "files": records}
    (PROJECT / "notes/evidence.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = ["# 固定版本与来源索引", "", f"研究基准：[{COMMIT}]({BASE}/tree/{COMMIT})。",
          "", "以下为静态阅读定位：行号及 SHA-256 直接从该提交的 Git 对象生成，不代表运行测试通过。",
          "上游许可证为 MIT，版权属于 Open-Inspect Contributors。本项目笔记为中文研究整理；未将完整上游代码复制进正式研究目录。", ""]
    for record in records:
        md += [f"## {record['id']}", "", f"**{record['title']}** · [原始文件]({record['url']})", ""]
        for match in record["matches"]:
            links = ", ".join(f"[L{n}]({record['url']}#L{n})" for n in match["lines"])
            md.append(f"- `{match['query']}`：{links}")
        md.append("")
    (PROJECT / "notes/sources.md").write_text("\n".join(md), encoding="utf-8")
    print(f"Indexed {len(records)} pinned source files; no upstream runtime was executed.")


if __name__ == "__main__":
    main()
