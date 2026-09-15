"""Package local research demos as a static site under web/dist (no publishing)."""
import hashlib
import json
import shutil
import subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'web/dist'
OUT.mkdir(parents=True,exist_ok=True)
for p in ['index.html','style.css','app.js','credits.html']:
    shutil.copy2(ROOT/'web'/p,OUT/p)
media=OUT/'media'; media.mkdir(exist_ok=True)
for name in ['demo-2d.mp4','demo-3d.mp4','cover.png','technology-map.png','technology-map.svg']:
    shutil.copy2(ROOT/'assets'/name,media/name)
subprocess.run(['ffmpeg','-v','error','-y','-ss','1.5','-i',str(media/'demo-2d.mp4'),'-frames:v','1','-q:v','2',str(media/'poster-2d.jpg')],check=True)
three=OUT/'demos/three'; (three/'src').mkdir(parents=True,exist_ok=True); (three/'vendor').mkdir(exist_ok=True)
for name in ['index.js','src/sceneControls.js']:
    shutil.copy2(ROOT/'src/demo-3d'/name,three/name)
vendor=ROOT/'src/demo-3d/node_modules/three'
for source,target in [('build/three.module.js','three.module.js'),('examples/jsm/controls/OrbitControls.js','controls/OrbitControls.js'),('LICENSE','THREE-LICENSE.txt')]:
    dst=three/'vendor'/target; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(vendor/source,dst)
html=(ROOT/'src/demo-3d/index.html').read_text(encoding='utf-8')
html=html.replace('./node_modules/three/build/three.module.js','./vendor/three.module.js').replace('./node_modules/three/examples/jsm/','./vendor/')
html=html.replace('</head>','<style>.camera-controls,.render-panel,.camera-frame{display:none!important}.preview-shell{width:min(100vw,calc(100vh * 16 / 9));}</style></head>')
(three/'index.html').write_text(html,encoding='utf-8')
spotlight=OUT/'demos/spotlight/index.html'
subprocess.run(['python','-X','utf8',str(ROOT/'upstream/skills/light-spotlight-render/scripts/render_light_spotlight.py'),'--label-text','VIBE MOTION','--swing-cycle-seconds','3','--mask-color','#ffffff','--text-color','#526078','--background-color','#101723','--video-width','1080','--video-height','810','--output',str(spotlight)],check=True)
html=spotlight.read_text(encoding='utf-8').replace('https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js','../../vendor/gsap-3.12.2.min.js')
spotlight.write_text(html,encoding='utf-8')
subprocess.run(['python','-X','utf8',str(ROOT/'upstream/skills/printed-curtain-render/scripts/create_printed_curtain.py'),'--text','VIBE','--text','MOTION','--cloth-color','#b7e35e','--ink-color','#11220a','--background-color','#101723','--output-dir',str(OUT/'demos/curtain'),'--overwrite'],check=True)
(OUT/'data').mkdir(exist_ok=True)
texts=['先把分散的信息汇总起来。','再按重要程度排出优先级。','最后，把任务安排到时间轴上。']
srt='\n\n'.join(f'{i+1}\n00:00:{i*4:02d},000 --> 00:00:{(i+1)*4:02d},000\n{text}' for i,text in enumerate(texts))+'\n'
(OUT/'data/example.srt').write_text(srt,encoding='utf-8')
story={'type':'preauthored_explanatory_demo','model_called':False,'fps':30,'duration_seconds':12,'scenes':[{'start':i*4,'end':(i+1)*4,'text':text,'meaning':['汇总','优先级','安排'][i],'visual':['散卡片归位','列表重排','任务落到时间轴'][i]} for i,text in enumerate(texts)]}
(OUT/'data/storyboard.json').write_text(json.dumps(story,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
probes={}
for filename in ['demo-2d.mp4','demo-3d.mp4']:
    probes[filename]=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(media/filename)],text=True))
(ROOT/'notes/gallery-media.json').write_text(json.dumps(probes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
files=[{'path':p.relative_to(OUT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(OUT.rglob('*')) if p.is_file()]
(ROOT/'notes/gallery-files.json').write_text(json.dumps(files,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Built static gallery: {len(files)} files')
