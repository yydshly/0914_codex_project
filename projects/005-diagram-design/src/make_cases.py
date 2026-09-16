"""Author reproducible Chinese cases following Diagram Design's geometry rules.

This is study code written by the agent, not an upstream general-purpose renderer.
"""
from pathlib import Path
import html
import json
import re
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
NAMES=['原始资料','提取关系','核实事实','整理图规格','生成图形','检查与导出']
SUBS=['源码、文档与需求','节点、方向与分组','确认来源与关系','受众、尺寸与重点','按规范编写 SVG','检查、渲染、交付']
FONTS="'Microsoft YaHei','PingFang SC','Noto Sans SC',sans-serif"

def save(path,text):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text,encoding='utf-8',newline='\n')

def inputs():
    folder=ROOT/'inputs'
    folder.mkdir(exist_ok=True)
    mermaid='flowchart LR\n'+'\n'.join(f'  n{i}["{name}"]' for i,name in enumerate(NAMES))+'\n'+'\n'.join(f'  n{i} --> n{i+1}' for i in range(5))+'\n'
    save(folder/'research.mmd',mermaid)
    mx=ET.Element('mxfile',host='app.diagrams.net'); dia=ET.SubElement(mx,'diagram',id='research',name='研究流程'); model=ET.SubElement(dia,'mxGraphModel'); root=ET.SubElement(model,'root')
    ET.SubElement(root,'mxCell',id='0'); ET.SubElement(root,'mxCell',id='1',parent='0')
    elements=[]
    for i,name in enumerate(NAMES):
        x=60+i*260;y=100+(i%2)*36
        cell=ET.SubElement(root,'mxCell',id=f'n{i}',value=name,style='rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;',vertex='1',parent='1')
        ET.SubElement(cell,'mxGeometry',x=str(x),y=str(y),width='180',height='80',attrib={'as':'geometry'})
        base=dict(x=x,y=y,width=180,height=80,angle=0,strokeColor='#1e1e1e',backgroundColor='#a5d8ff',fillStyle='solid',strokeWidth=1,strokeStyle='solid',roughness=1,opacity=100,groupIds=[],frameId=None,roundness={'type':3},seed=i+1,version=1,versionNonce=i+100,isDeleted=False,updated=1,link=None,locked=False)
        elements.append(dict(base,id=f'n{i}',type='rectangle',boundElements=[{'id':f't{i}','type':'text'}]))
        elements.append(dict(base,id=f't{i}',type='text',x=x+20,y=y+26,width=140,height=28,text=name,originalText=name,fontSize=20,fontFamily=2,textAlign='center',verticalAlign='middle',containerId=f'n{i}',autoResize=True,lineHeight=1.25,baseline=22,boundElements=None))
    for i in range(5):
        cell=ET.SubElement(root,'mxCell',id=f'e{i}',source=f'n{i}',target=f'n{i+1}',edge='1',parent='1',style='edgeStyle=orthogonalEdgeStyle;endArrow=classic;')
        ET.SubElement(cell,'mxGeometry',relative='1',attrib={'as':'geometry'})
        elements.append(dict(id=f'e{i}',type='arrow',x=240+i*260,y=140+(i%2)*36,width=80,height=36,points=[[0,0],[80,36 if i%2==0 else -36]],startBinding={'elementId':f'n{i}','focus':0,'gap':0},endBinding={'elementId':f'n{i+1}','focus':0,'gap':0},startArrowhead=None,endArrowhead='arrow',strokeColor='#1e1e1e',strokeStyle='solid',strokeWidth=1,backgroundColor='transparent',fillStyle='solid',roughness=1,opacity=100,angle=0,groupIds=[],boundElements=None,seed=100+i,version=1,versionNonce=200+i,isDeleted=False,updated=1,link=None,locked=False))
    save(folder/'research.drawio',ET.tostring(mx,encoding='unicode'))
    save(folder/'research.excalidraw',json.dumps(dict(type='excalidraw',version=2,source='diagram-design-study',elements=elements,appState={'viewBackgroundColor':'#ffffff'},files={}),ensure_ascii=False,indent=2))
    save(folder/'research-content.json',json.dumps({'subject':'GitHub 项目研究流程（本研究建议流程，非运行轨迹）','nodes':[{'id':f'n{i}','name':name,'description':SUBS[i]} for i,name in enumerate(NAMES)],'edges':[{'from':f'n{i}','to':f'n{i+1}'} for i in range(5)]},ensure_ascii=False,indent=2))

def diagram(slug,theme='blue',simple=False,slide=False):
    palettes={'blue':('#f5f6f8','#16253d','#506078','#335deb','#e9eeff','#ffffff','#bdc9d9'),
              'orange':('#f5f5f5','#2d3142','#4f5d75','#eb6c36','#fff0e8','#ffffff','#c4cbd4'),
              'dark':('#172032','#eef3ff','#bac7dc','#8daaff','#273958','#1f2b42','#64748d')}
    paper,ink,muted,accent,tint,white,rule=palettes[theme]
    W,H=(1600,900) if slide else (1280,720)
    title='从理解资料，到制作交付' if simple else 'GitHub 项目研究流程'
    desc='资料经提取、核实、整理图规格、绘图与检查导出，形成研究配图；这是建议流程，不代表实际自动化系统。'
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="{slug}-title {slug}-desc"><title id="{slug}-title">{title}</title><desc id="{slug}-desc">{desc}</desc><defs>']
    for name,color in [('arrow',muted),('arrow-accent',accent),('arrow-link','#2e5aa8')]:
        out.append(f'<marker id="{name}" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="{color}"/></marker>')
    out.append(f'</defs><rect width="{W}" height="{H}" fill="{paper}"/>')
    def text(x,y,value,size=20,color=ink,anchor='start',weight=400,serif=False):
        font="Georgia,'Noto Serif SC',SimSun,serif" if serif else FONTS
        return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-weight="{weight}">{html.escape(value)}</text>'
    out.extend([text(64,52,'研究流程 / 中文重绘实验',18,muted),text(64,104,title,36,serif=True)])
    if simple:
        names=['理解资料','确认表达','制作交付'];subs=['原始资料 · 提取关系','核实事实 · 整理图规格','生成图形 · 检查与导出']
        positions=[(64,248),(496,248),(928,248)];nw,nh=288,152
        lines=[(352,324,496,324),(784,324,928,324)]
    elif slide:
        names=NAMES;subs=SUBS;nw,nh=208,156
        positions=[(64+i*252,300) for i in range(6)];lines=[(x+nw,y+78,positions[i+1][0],y+78) for i,(x,y) in enumerate(positions[:-1])]
    else:
        names=NAMES;subs=SUBS;nw,nh=288,116
        positions=[(64,180),(496,180),(928,180),(928,436),(496,436),(64,436)]
        lines=[(352,238,496,238),(784,238,928,238),(1072,296,1072,436),(928,494,784,494),(496,494,352,494)]
    for x1,y1,x2,y2 in lines:
        out.append(f'<path d="M {x1} {y1} L {x2} {y2}" fill="none" stroke="{muted}" stroke-width="2" marker-end="url(#arrow)"/>')
    for i,((x,y),name,sub) in enumerate(zip(positions,names,subs)):
        focal=i==(1 if simple else 2)
        out.append(f'<rect x="{x}" y="{y}" width="{nw}" height="{nh}" rx="6" fill="{tint if focal else white}" stroke="{accent if focal else rule}" stroke-width="{2 if focal else 1}"/>')
        out.extend([text(x+20,y+29,f'{i+1:02d}',16,muted),text(x+20,y+65,name,26 if not slide else 24,ink,weight=600)])
        if slide:
            # Multi-line strings preserve meaning and readable size in the narrower slide nodes.
            chunks=[sub[:5],sub[5:]] if len(sub)>8 else [sub]
            for n,chunk in enumerate(chunks):out.append(text(x+20,y+103+n*28,chunk,20,muted))
        else:out.append(text(x+20,y+95,sub,20,muted))
    fy=H-116
    out.append(f'<path d="M64 {fy} H{W-64}" stroke="{rule}" stroke-width="1"/>')
    out.extend([text(64,fy+40,'关系由人与 AI 确认；图形负责清晰表达。',22,ink),text(64,fy+76,'本研究的建议流程 · 实线表示先后关系 · 焦点表示需要核实的阶段',18,muted)])
    out.append('</svg>')
    return ''.join(out),palettes[theme]

def main():
    inputs()
    for slug,theme,simple,slide in [('research-blue','blue',False,False),('research-orange','orange',False,False),('research-dark','dark',False,False),('research-full','blue',False,False),('research-executive','blue',True,False),('research-slide','blue',False,True),('research-sketchy','blue',False,False),('research-annotation','blue',False,False)]:
        svg,palette=diagram(slug,theme,simple,slide)
        if slug.endswith('sketchy'):
            svg=svg.replace('</defs>','<filter id="sketchy" x="-2%" y="-2%" width="104%" height="104%"><feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="2" seed="4"/><feDisplacementMap in="SourceGraphic" scale="2"/></filter></defs>')
            # Filter only node boxes and connectors; leave text and canvas crisp.
            svg=re.sub(r'(<rect x="[^"]+" y="[^"]+"[^>]+/>|<path d="[^"]+"[^>]+/>)',r'<g filter="url(#sketchy)">\1</g>',svg)
        if slug.endswith('annotation'):
            note=f'<text x="1200" y="142" text-anchor="end" font-family="Georgia,SimSun,serif" font-size="20" font-style="italic" fill="#16253d">先核实，再决定怎样画</text><path d="M 1072 151 Q 1064 160 1072 175" fill="none" stroke="#506078" stroke-width="1" stroke-dasharray="4,3"/><circle cx="1072" cy="175" r="2" fill="#506078"/>'
            svg=svg.replace('</svg>',note+'</svg>')
        paper,ink,muted,*_=palette
        extra=''
        if slug.endswith('full'):
            extra='<div class="cards"><section><h2>先确认事实</h2><p>核实来源、组件和关系，避免把推断画成已确认的系统。</p></section><section><h2>再决定表达</h2><p>根据读者、尺寸和重点选图，复杂内容拆成总览与细节。</p></section><section><h2>最后检查交付</h2><p>结构检查与实际渲染各自验证不同问题，业务结论仍需人判断。</p></section></div>'
        page=f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>中文研究案例 · {slug}</title><style>*{{box-sizing:border-box}}body{{margin:0;background:{paper};color:{ink};font:16px/1.8 {FONTS}}}.frame{{max-width:1440px;margin:auto;padding:20px;overflow:auto}}svg{{width:100%;min-width:760px;display:block}}.cards{{display:grid;grid-template-columns:1.2fr 1fr 1fr;gap:24px;padding:10px 44px 40px}}.cards section{{border-top:2px solid #335deb;padding-top:16px}}h2{{font-size:20px;margin:0 0 8px}}p{{margin:0;color:{muted}}}@media(max-width:800px){{.cards{{grid-template-columns:1fr;padding:20px}}.frame{{padding:0}}}}</style></head><body><div class="frame">{svg}{extra}</div></body></html>'
        save(ROOT/'cases'/f'{slug}.html',page);save(ROOT/'cases'/f'{slug}.svg',svg)
    ledger={'source':'research-content.json','source_nodes':6,'source_edges':5,'faithful':{'drawn_nodes':6,'drawn_edges':5,'merged':[],'dropped':[]},'simplified':{'drawn_nodes':3,'drawn_edges':2,'merged':{'理解资料':['n0','n1'],'确认表达':['n2','n3'],'制作交付':['n4','n5']},'dropped':[]},'note':'节点描述由本研究提供；重绘由 AI 按规范编写，不是上游提取器自动生成。'}
    save(ROOT/'evidence/fidelity-ledger.json',json.dumps(ledger,ensure_ascii=False,indent=2))
    save(ROOT/'notes/style-guide.md',f'''# 本次中文研究配图规范

适用范围：本次 AI 编写的中文案例。上游示例保持原样，不修改安装目录或全局配置。

| 角色 | 蓝色研究版 | 橙色对照版 | 深色对照版 |
|---|---|---|---|
| paper | #f5f6f8 | #f5f5f5 | #172032 |
| ink | #16253d | #2d3142 | #eef3ff |
| muted | #506078 | #4f5d75 | #bac7dc |
| accent | #335deb | #eb6c36 | #8daaff |
| accent-tint | #e9eeff | #fff0e8 | #273958 |

正文：{FONTS}。中文标题使用宋体后备；SVG 最小文字 16px，常用说明 18–22px。
本机 PNG 导出使用已安装的 Microsoft YaHei；不声称其他平台字体一致。
无阴影，结构坐标与尺寸按 4px 网格，一处焦点，直线连接对齐端口。
同结构三版仅变颜色；完整页面增加摘要；概览显式记录合并；幻灯片重新布局。
这次手动指定配色，没有运行网站品牌抓取或命名 Profile 安装流程。
''')
    print('Authored 8 Chinese HTML/SVG pairs and 3 source formats')

if __name__=='__main__':main()
