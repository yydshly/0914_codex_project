"""Smoke-check the research navigation and published inventory with Chromium."""
from pathlib import Path
import json
import argparse
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]

def main(url):
    errors=[];checks=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        page=browser.new_page(viewport={'width':1440,'height':1000})
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto(url,wait_until='networkidle')
        assert page.locator('#overview').is_visible()
        assert page.locator('#overview img').first.evaluate('(e)=>e.complete&&e.naturalWidth===3600')
        checks.append('overview is default; high-resolution image loads')
        for panel in ('gallery','taxonomy','cases','principles','compare','evidence','overview'):
            page.locator(f'.navigation a[href="#{panel}"]').click()
            page.locator('#'+panel).wait_for(state='visible')
            assert page.locator('#'+panel).is_visible()
        checks.append('all seven navigation panels')
        page.locator('.navigation a[href="#gallery"]').click()
        page.locator('#gallery').wait_for(state='visible')
        assert page.locator('#type-list button').count()==57
        page.select_option('#kind','动画演示')
        assert page.locator('#type-list button').count()==3
        page.select_option('#kind','基础图型')
        page.select_option('#category','数值与统计')
        assert page.locator('#type-list button').count()==8
        page.locator('#type-list button').last.click()
        assert page.locator('#type-name').inner_text()=='瀑布图'
        page.locator('#variants button').last.click()
        assert page.locator('#preview').get_attribute('src').endswith('-full.html')
        checks.append('57-example list, kind/category filters and variant switching')
        page.locator('.navigation a[href="#cases"]').click()
        page.locator('#cases').wait_for(state='visible')
        assert page.locator('#case-selector button').count()==8
        page.locator('#case-selector button').last.click()
        assert page.locator('#case-preview').get_attribute('src').endswith('research-annotation.html')
        checks.append('eight authored cases and download links')
        page.locator('.navigation a[href="drawings.html"]').click()
        assert page.locator('a[href^="vendor/example-"]').count()==155
        assert page.locator('a[href^="cases/"]').count()==24
        checks.append('standalone inventory: 155 originals and 24 authored case files')
        page.set_viewport_size({'width':390,'height':844})
        page.goto(url,wait_until='networkidle')
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
        assert page.locator('#overview').is_visible()
        checks.append('390px mobile viewport: no page-level horizontal overflow')
        screenshots=ROOT.parents[1]/'.cache/diagram-publish-check'
        screenshots.mkdir(parents=True,exist_ok=True)
        page.screenshot(path=str(screenshots/'overview-mobile.png'),full_page=True)
        page.set_viewport_size({'width':1440,'height':1000})
        page.screenshot(path=str(screenshots/'overview-desktop.png'),full_page=True)
        browser.close()
    assert not errors,errors
    result={'url':url,'checks':checks,'javascript_errors':errors,'scope':'Chromium smoke checks; not exhaustive multi-browser or 155-diagram visual review'}
    (ROOT/'evidence/browser-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--url',default='http://127.0.0.1:8785/');args=parser.parse_args();main(args.url)
