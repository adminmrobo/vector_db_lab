# 실전 연습장 미션 점검: 정답 조작을 흉내 내어 장면마다 미션 3개가 모두 "통과"로 바뀌는지 본다
import os, asyncio, json
from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET = '''(a)=>{const [sel,val]=a;const e=document.querySelector(sel);e.value=val;e.dispatchEvent(new Event('input',{bubbles:true}));e.dispatchEvent(new Event('change',{bubbles:true}));}'''
CLICK = '''(sel)=>document.querySelector(sel).click()'''

PLAN = {
    'search': [('set', '#q_s', '6'), ('click', '#search [data-me=like]'), ('set', '#q_s', '0'), ('click', '#search [data-me=vec]'), ('click', '#f_s'),
               ('set', '#k_s', '115'), ('set', '#q_s', '1'), ('set', '#k_s', '25'), ('set', '#q_s', '2'), ('set', '#k_s', '65')],
    'rag': [('click', '#n_r'), ('set', '#sz_r', '120'), ('set', '#k_r', '2'), ('set', '#a_r', '5'), ('set', '#t_r', '55'),
            ('click', '#old_r'), ('click', '#old_r'), ('click', '#n_r'), ('set', '#t_r', '35'), ('click', '#n_r')],
    'sns': [('set', '#d_n', '14'), ('set', '#p_n', '79'), ('set', '#g_n', '98'), ('set', '#g_n', '44'), ('set', '#a_n', '2')],
    'store': [('click', '#store [data-ix=ivf]'), ('set', '#np_t', '1'), ('click', '#store [data-ix=hnsw]'), ('set', '#ef_t', '10'), ('click', '#store [data-n="2000"]')],
}


async def main():
    out = {}
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        page = await b.new_page(viewport={'width': 1280, 'height': 900})
        errs = []
        page.on('pageerror', lambda e: errs.append(str(e)))
        await page.route('**/fonts.g*/**', lambda r: r.abort())
        await page.goto('file://' + os.path.join(ROOT, 'practice', 'index.html'))
        await page.wait_for_timeout(800)
        for tab, steps in PLAN.items():
            await page.evaluate(CLICK, '[data-tab=%s]' % tab)
            await page.wait_for_timeout(200)
            before = await page.evaluate('(t)=>document.querySelectorAll("#ms_"+t+" .mission.ok").length', tab)
            for s in steps:
                if s[0] == 'set':
                    await page.evaluate(SET, [s[1], s[2]])
                else:
                    await page.evaluate(CLICK, s[1])
                await page.wait_for_timeout(120)
            after = await page.evaluate('(t)=>document.querySelectorAll("#ms_"+t+" .mission.ok").length', tab)
            out[tab] = {'before': before, 'after': after}
        out['errors'] = errs
        await b.close()
    print(json.dumps(out, ensure_ascii=False))


asyncio.run(main())
