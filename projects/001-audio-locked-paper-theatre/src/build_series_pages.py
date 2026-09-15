"""Build local video-player pages from the project's original player layout."""
import json
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
base=(ROOT/"web/index.html").read_text(encoding="utf-8")
configs={
 "english":{
   "title":"Where is the ball?",
   "subtitle":"英语微课堂：看位置、听例句、跟读，再自己说出来。",
   "chapters":[(0,"课前导入",False),(12.132,"in · 在里面",False),(25.884,"on · 在表面",False),(38.7,"under · 在下面",False),(52.092,"拼出完整句子",False),(64.5,"暂停看图作答",True),(66.708,"听参考答案",False)],
   "look":"适合初学者的中英双语微课：同一颗球进入盒子、落在桌面、移到桌下，位置变化与 in / on / under 对应。跟读后保留停顿，最后用完整句子回答 Where is the ball?",
   "about":'本课聚焦物体的位置用法。MiniMax 合成中英双语配音，句级字幕控制画面节奏；下方三道题按固定答案即时反馈。可用于课堂导入、暂停提问或课后复习。语法参考 <a href="https://learnenglishkids.britishcouncil.org/grammar-vocabulary/grammar-practice/prepositions-place" target="_blank" rel="noreferrer">British Council</a>。本页不采集录音，也不进行发音评分。'
 },
 "dns":{
   "title":"输入网址后，电脑怎样找到网站？",
   "subtitle":"科普演示：跟着一条查询，看懂 DNS 的分工。",
   "chapters":[(0,"名字与地址",False),(18.396,"逐级查询",False),(34.38,"地址返回",False),(39.672,"连接网站与缓存",False)],
   "look":"观察查询如何从设备发给递归解析器，再分别询问根、顶级域和权威服务器。每条指引返回解析器；地址返回设备后，浏览器再连接网站。",
   "about":'这是简化的 DNS 解析示意，未实时查询 example.com，也未展示别名、多地址和连接握手等细节。依据 <a href="https://www.cloudflare.com/learning/dns/dns-server-types/" target="_blank" rel="noreferrer">Cloudflare DNS 文档</a>；域名使用 <a href="https://www.iana.org/help/example-domains" target="_blank" rel="noreferrer">IANA 文档示例域名</a>。'
 },
 "task-training":{
   "title":"把一句模糊需求，变成可执行任务",
   "subtitle":"教学培训演示：看示范、补要素，再做一道练习。",
   "chapters":[(0,"发现模糊点",False),(15.948,"补齐四个要素",False),(57.4,"暂停做练习",True),(60.588,"揭晓练习答案",False)],
   "look":"从“尽快整理客户反馈”出发，逐步补齐负责人、交付物、期限和验收标准。随后演示交接复述，并用“尽快优化首页”检验理解。",
   "about":"这是一段自编的新人培训示例。点击“暂停做练习”，视频会停在题目处；想好后再点“揭晓练习答案”。模板用于辅助任务沟通，可按团队实际要求调整。"
 }
}
for slug,c in configs.items():
    tl=json.loads((ROOT/"demos"/slug/"assets/timeline.json").read_text(encoding="utf-8"))
    duration=round(tl["duration"])
    html=base.replace("三条记录，一张行动摘要",c["title"]).replace("先确定声音，再让画面把意思演出来。",c["subtitle"])
    html=html.replace("MiniMax 真实配音 · 47 秒",f"MiniMax 真实配音 · {duration} 秒")
    html=html.replace("../output/paper-theatre-demo.mp4",f"../demos/{slug}/output/demo.mp4")
    for path in ["assets/cover.jpg","assets/narration.mp3","output/captions.srt","output/contact-sheet.jpg"]:
        html=html.replace("../"+path,f"../demos/{slug}/{path}")
    nav='<nav aria-label="按场景跳转">'+''.join(f'<button data-time="{t}" data-pause="{str(pause).lower()}"><small>{int(t)//60:02}:{int(t)%60:02} / 场景 {i+1}</small>{name}</button>' for i,(t,name,pause) in enumerate(c["chapters"]))+'</nav>'
    html=re.sub(r'<nav aria-label="按场景跳转">.*?</nav>',nav,html,flags=re.S)
    html=html.replace("固定的纸艺舞台上，记录卡独立移动。机器提取时间、负责人和前置条件，摘要从对应出口出现。原始记录仍然保留，字幕跟着语音切换。",c["look"])
    html=html.replace("MiniMax 生成配音和句级时间戳；AI 生成机器素材；程序负责文字、图层、运动与视频合成。示例中的记录和摘要为预先编写，机器用于表现整理过程。",c["about"])
    html=html.replace("这个样例如何完成","内容与使用说明").replace("video.duration||47",f"video.duration||{duration}")
    html=html.replace("video.currentTime=Number(button.dataset.time);video.play()", "video.currentTime=Number(button.dataset.time);if(button.dataset.pause==='true'){video.pause();status.textContent='已暂停，请先思考，再点击揭晓答案';return;}video.play()")
    if slug=="english":
        html=html.replace('</main>',(ROOT/'src/english_quiz.html').read_text(encoding='utf-8')+'</main>')
    (ROOT/"web"/f"{slug}.html").write_text(html,encoding="utf-8")
    print(f"Saved web/{slug}.html")
