"""Browser QA for the research explainer only; never requests Douyin."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '.cache'
OUT.mkdir(exist_ok=True)
results = {'url': 'http://127.0.0.1:8088/', 'errors': [], 'checks': []}
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 1000}, device_scale_factor=1)
    page.on('pageerror', lambda error: results['errors'].append(str(error)))
    page.on('response', lambda response: results['errors'].append(f'{response.status}: {response.url}') if response.status >= 400 else None)
    page.goto(results['url'], wait_until='networkidle')
    assert page.title() == '抖音采集如何发生 · Douyin Downloader 研究'
    for mode, text in [('fallback', '真实页面请求更多主页作品'), ('desktop', '网页 SDK 提供动态环境信息'), ('direct', '携带参数、请求头和签名')]:
        button = page.locator(f'[data-mode="{mode}"]')
        button.click()
        assert button.get_attribute('aria-pressed') == 'true'
        assert text in page.locator('#route-panel').inner_text()
        assert page.locator('[data-mode][aria-pressed="true"]').count() == 1
        assert page.locator('#route li').count() == 4
    results['checks'].append('Three request paths update all steps and selection state')
    for detail in page.locator('details').all():
        if detail.get_attribute('open') is None:
            detail.locator('summary').click()
        assert detail.get_attribute('open') is not None
    results['checks'].append('All three capability details expand')
    page.locator('[data-mode="fallback"]').focus()
    page.keyboard.press('Enter')
    assert page.locator('[data-mode="fallback"]').get_attribute('aria-pressed') == 'true'
    results['checks'].append('Keyboard Enter activates a request path')
    page.locator('[data-mode="direct"]').click()
    for width in [1440, 768, 390, 320]:
        page.set_viewport_size({'width': width, 'height': 1000})
        page.evaluate('window.scrollTo(0, 0)')
        assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), f'Overflow at {width}'
        page.screenshot(path=str(OUT / f'web-{width}.png'), full_page=True)
    results['checks'].append('No horizontal overflow at 1440, 768, 390 and 320 CSS px')
    page.set_viewport_size({'width': 780, 'height': 1000})
    page.add_style_tag(content='html{font-size:200% !important}body{font-size:2rem !important}')
    assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), 'Overflow at enlarged text'
    results['checks'].append('No page overflow under enlarged root and body text')
    assert page.locator('.poster img').evaluate('(img) => img.complete && img.naturalWidth === 2400')
    for target in ['assets/douyin-overview.png', 'assets/douyin-overview.svg', 'notes/understanding.md', 'notes/capabilities.md', 'notes/sources.md', 'notes/verification.md', 'notes/image-production.md', 'notes/UPSTREAM-LICENSE.txt']:
        assert page.request.get(results['url'] + target).status == 200, target
    results['checks'].append('Poster and all public document downloads return HTTP 200')
    browser.close()
assert not results['errors'], results['errors']
(OUT / 'web-verification.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(results, ensure_ascii=False, indent=2))
