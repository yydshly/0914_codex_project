"""Package public pages and their media, without credentials or synthesis requests."""
from pathlib import Path
import argparse
import re
import shutil
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

ROOT=Path(__file__).resolve().parents[1]
REPO='https://github.com/yydshly/0914_codex_project/blob/main/projects/001-audio-locked-paper-theatre/'

class Links(HTMLParser):
    def __init__(self):super().__init__();self.urls=[]
    def handle_starttag(self,tag,attrs):
        self.urls.extend(v for k,v in attrs if k in ('src','href','poster') and v)

def build(output):
    output=output.resolve()
    if output.exists():raise ValueError('Choose a new output directory to avoid stale files')
    output.mkdir(parents=True)
    files=[*ROOT.glob('web/*.html')]
    files += [ROOT/'assets'/name for name in ['audio-animation-architecture.png','audio-animation-architecture.svg']]
    files += [ROOT/p for p in ['assets/cover.jpg','assets/narration.mp3','assets/library-overview.png','assets/library-overview.svg','output/paper-theatre-demo.mp4','output/captions.srt','output/contact-sheet.jpg']]
    for slug in ['dns','task-training','english']:
        files += [ROOT/'demos'/slug/p for p in ['assets/cover.jpg','assets/narration.mp3','output/demo.mp4','output/captions.srt','output/contact-sheet.jpg']]
    for source in files:
        dest=output/source.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True)
        if source.suffix=='.html':
            document=source.read_text(encoding='utf-8')
            def rewrite(match):
                link=match[1]
                if urlsplit(link).scheme or not urlsplit(link).path.endswith('.md'):return match[0]
                path=(source.parent/urlsplit(link).path).resolve().relative_to(ROOT)
                return 'href="'+REPO+path.as_posix()+'"'
            document=re.sub(r'href="([^"]+)"',rewrite,document)
            dest.write_text(document,encoding='utf-8',newline='\n')
        else:shutil.copy2(source,dest)
    (output/'index.html').write_text('<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0;url=web/guide.html"><title>纸艺剧场 · 培训视频与教学微课</title><meta name="description" content="画板是舞台，物品是演员，代码是动作脚本，音频时间轴是演出节拍。用于培训视频制作、教学微课、科普与产品说明。"></head><body><p><a href="web/guide.html">进入纸艺剧场：能力、原理与四个演示</a></p></body></html>',encoding='utf-8')
    pages=list(output.rglob('*.html'))
    for page in pages:
        parser=Links();parser.feed(page.read_text(encoding='utf-8'))
        for url in parser.urls:
            parts=urlsplit(url)
            if parts.scheme or parts.netloc or not parts.path:continue
            target=(page.parent/unquote(parts.path)).resolve()
            if not target.is_relative_to(output) or not target.is_file():raise ValueError(f'Broken local link in {page.name}: {url}')
    print(f'Packaged {len(pages)} pages, {len(files)+1} files; all local page/media links resolve.')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'web/dist');args=parser.parse_args();build(args.output)
