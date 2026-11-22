# 브라우저 점검: 콘솔 오류, 390·1280px 가로 넘침, 빈 캐릭터 그림, 스크린샷
import sys, os, json, asyncio
from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


async def run(pages, shots):
    out = {}
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        for pg in pages:
            res = {}
            for w in (1280, 390):
                ctx = await b.new_context(viewport={'width': w, 'height': 900}, device_scale_factor=1)
                page = await ctx.new_page()
                errs = []
                page.on('console', lambda m: errs.append(m.text) if m.type == 'error' and 'ERR_FAILED' not in m.text else None)
                page.on('pageerror', lambda e: errs.append('PAGEERROR ' + str(e)))
                await page.route('**/fonts.googleapis.com/**', lambda r: r.abort())
                await page.route('**/fonts.gstatic.com/**', lambda r: r.abort())
                await page.goto('file://' + os.path.join(ROOT, pg))
                await page.wait_for_timeout(1500)
                # 모든 캔버스가 보이도록 스크롤
                h = await page.evaluate('document.documentElement.scrollHeight')
                for y in range(0, h, 700):
                    await page.evaluate('window.scrollTo(0,%d)' % y); await page.wait_for_timeout(60)
                await page.wait_for_timeout(400)
                info = await page.evaluate('''()=>({sw:document.documentElement.scrollWidth,
                    emptyImg:[...document.querySelectorAll('img[data-who]')].filter(i=>!i.getAttribute('src')).map(i=>i.dataset.who+'_'+i.dataset.mood).slice(0,10),
                    quiz:document.querySelectorAll('.quiz .qq').length, jt:document.querySelectorAll('.jt').length,
                    wide:[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.right>document.documentElement.clientWidth+1 && !e.closest('.cwrap,.tw,nav.top,.code,pre,.eq,.eqbig,details')}).slice(0,6).map(e=>e.tagName+'.'+e.className+'#'+e.id)})''')
                info['errors'] = errs[:10]
                res[w] = info
                if pg in shots:
                    await page.evaluate('window.scrollTo(0,0)')
                    name = pg.replace('/', '_').replace('.html', '')
                    await page.screenshot(path='/home/claude/work/shot_%s_%d.png' % (name, w), full_page=True)
                await ctx.close()
            out[pg] = res
        await b.close()
    return out


if __name__ == '__main__':
    pages = sys.argv[1].split(',')
    shots = sys.argv[2].split(',') if len(sys.argv) > 2 else []
    print(json.dumps(asyncio.run(run(pages, shots)), ensure_ascii=False, indent=1))
