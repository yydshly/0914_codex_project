"""Render only standalone diagram assets, not the gallery UI, to PNG at native viewBox size × 2."""
from pathlib import Path
import json
import re
import shutil
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]

def main():
    records=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        for file in sorted((ROOT/'cases').glob('*.svg')):
            source=file.read_text(encoding='utf-8');w,h=map(int,re.search(r'viewBox="0 0 (\d+) (\d+)"',source).groups())
            page=browser.new_page(viewport={'width':w,'height':h},device_scale_factor=2)
            page.goto(file.as_uri(),wait_until='load')
            page.evaluate('document.fonts.ready')
            page.locator('svg').screenshot(path=str(file.with_suffix('.png')),omit_background=True)
            measured=Image.open(file.with_suffix('.png')).size
            assert measured==(w*2,h*2),(file,measured)
            font=page.locator('svg text').last.evaluate('(el)=>getComputedStyle(el).fontFamily')
            records.append({'file':file.name,'png':file.with_suffix('.png').name,'width':measured[0],'height':measured[1],'font_stack':font,'microsoft_yahei_available':page.evaluate('document.fonts.check("20px Microsoft YaHei")')})
            page.close()
        browser.close()
    (ROOT/'evidence/png-export.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
    shutil.copy2(ROOT/'cases/research-blue.png',ROOT/'assets/research-workflow.png')
    thumbs=[]
    for record in records:
        im=Image.open(ROOT/'cases'/record['png']).convert('RGB');im.thumbnail((800,450));tile=Image.new('RGB',(820,480),'#e2e7ee');tile.paste(im,((820-im.width)//2,10));ImageDraw.Draw(tile).text((20,460),record['file'],fill='#16253d');thumbs.append(tile)
    sheet=Image.new('RGB',(1640,480*((len(thumbs)+1)//2)),'white')
    for i,im in enumerate(thumbs):sheet.paste(im,((i%2)*820,(i//2)*480))
    sheet.save(ROOT/'assets/case-contact-sheet.jpg',quality=92)
    print(f'Exported {len(records)} PNGs; pixel dimensions verified')

if __name__=='__main__':main()
