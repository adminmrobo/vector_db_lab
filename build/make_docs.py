# -*- coding: utf-8 -*-
"""표지 지시문(16비트 RPG 픽셀아트), 이미지 제작 명세서, cover_manifest.json 만들기"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)

CH = {
    'doc': 'chibi scientist, thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie',
    'asst': 'girl researcher, long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans',
    'fly': 'anthropomorphic fruit fly researcher, black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables, white lab coat over a black vest, black gloves, transparent wings',
    'robo': 'boxy beige retro CRT-monitor robot, dark green screen face with mint pixel eyes and mouth, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads, holding a wooden abacus',
    'sia': 'young intern girl in a classic black-and-white maid-style uniform, straight black hair',
    'moa': 'young intern girl in a classic black-and-white maid-style uniform, wavy beige hair',
}
COVERS = [
    ('cover_00', 'index.html', '목차 — 벡터 DB 연구실', '낮의 연구실 강의실, 큰 창과 흰 칠판', 'ko',
     ['doc', 'asst', 'sia', 'moa', 'fly', 'robo'],
     '하루가 칠판 앞에서 처음 강의하는 순간(살짝 긴장), 인턴 둘이 앞줄에서 노트를 펼침, 칠판에는 글자 없이 표(격자)와 흩어진 색 점 무리',
     'a nervous but brave girl researcher giving her first lecture at a white board; on the board, a plain grid table on the left and colorful clusters of dots on the right, connected by a hand-drawn arrow (no letters)',
     '조수(하루)가 칠판 앞에서 첫 강의를 하고 인턴 둘과 식구들이 지켜보는 장면'),
    ('cover_01', '01_why_not_table.html', '1장 · 표에 담기지 않는 말', '낮의 자료실, 흰 서랍장과 큰 탁자', 'ko',
     ['doc', 'asst', 'fly', 'robo'],
     '격자 서랍장에 깔끔히 들어간 별점 카드(노란 별)와, 서랍에 들어가지 못하고 탁자 위로 넘쳐 흐르는 말풍선 모양 종이들',
     'a neat white grid cabinet whose drawers hold small cards with yellow stars, while many speech-bubble shaped paper slips overflow from the top and spill onto the table because they do not fit any drawer',
     '별점 카드는 서랍장에 잘 들어가고, 말풍선 종이는 넘쳐 흐르는 자료실'),
    ('cover_02', '02_embedding.html', '2장 · 말을 좌표로', '낮의 연구실 바닥에 깐 큰 모눈 매트', 'ko',
     ['doc', 'asst', 'fly', 'robo'],
     '말풍선 종이들이 모눈 매트 위 좌표 점으로 내려앉고, 뜻이 비슷한 말풍선끼리 같은 색 무리로 모임. 두 화살표 사이의 각도를 재는 큰 각도기',
     'speech-bubble paper slips floating down and landing as colored pixel dots on a big grid floor mat, similar bubbles gathering into same-color clusters; a giant protractor measuring the angle between two arrows',
     '말풍선이 모눈 위 좌표 점으로 내려앉고 각도기로 화살표 각도를 재는 장면'),
    ('cover_03', '03_vector_store.html', '3장 · 벡터 창고', '낮의 높은 선반 창고, 천장 채광창', 'ko',
     ['doc', 'asst', 'fly', 'robo'],
     '색 점 상자들이 군집별 서랍에 정리된 높은 선반, 바닥에는 점과 점을 잇는 빛나는 길(그래프)과 위층 고속도로 표지(글자 없는 화살표)',
     'tall daylight warehouse shelves with drawers grouped by colored dot clusters; on the floor, glowing paths connect dots like a small-world graph, with a raised highway level above (plain arrow signs, no letters)',
     '군집 서랍이 있는 선반 창고와 바닥의 빛나는 길 그래프'),
    ('cover_04', '04_llm_rag.html', '4장 · 찾아서 답하는 AI', '낮의 고객센터, 헤드셋과 모니터 데스크', 'ko',
     ['doc', 'asst', 'fly', 'robo'],
     '주판봇 옆 큰 말하는 책(LLM)이 입을 열고, 하루가 창고 선반에서 꺼낸 문서 조각 세 장을 책에 끼워 주는 순간. 오래된 누런 문서 한 장은 초파리가 집어 따로 빼냄',
     'a big friendly talking book character (representing a language model) at a help-desk; the girl researcher slides three small document pieces from a shelf into its pages; the fruit fly pulls out one old yellowed page and sets it aside',
     '하루가 문서 조각을 말하는 책에 끼워 주고 초파리가 옛 문서를 빼내는 고객센터'),
    ('cover_05', '05_cases.html', '5장 · 현장 사례', '낮의 상황실, 여러 개의 큰 화면(글자 없음)', 'ko',
     ['doc', 'asst', 'fly', 'robo'],
     '화면 네 개: 영화 필름 띠와 하트, 말풍선 무리 중 빨간 새 무리, 대화 기억 수첩, 저울(표 vs 점 무리). 식구들이 각 화면을 가리킴',
     'a bright daytime control room with four large screens without text: film strips with hearts, clusters of speech bubbles with one new red cluster growing, a memory notebook with sticky notes, and a balance scale weighing a grid table against a dot cluster',
     '네 화면이 있는 상황실에서 식구들이 각 사례를 가리키는 장면'),
    ('cover_07', '06_attention_3d.html', '6장 · LLM은 찾은 자료를 어떻게 읽나', '낮의 연구실, 공중에 뜬 3층 투명 판(홀로그램 느낌의 픽셀 판)', 'ko',
     ['doc', 'asst', 'fly', 'robo'],
     '창고 선반에서 꺼낸 문서 조각 두 장이 빛나는 띠(프롬프트)로 이어지고, 그 위로 투명한 판 세 층에 작은 점(토큰)들이 늘어서 있으며 위층 점에서 아래층 점들로 굵기가 다른 빨간 실선이 뻗음',
     'two document pieces pulled from a shelf feed into a glowing ribbon; above it, three stacked translucent pixel panels hold rows of small dots (tokens), and red strings of different thickness connect a dot on the top panel to many dots below, like a 3D attention tower',
     '문서 조각이 빛나는 띠로 이어지고 3층 판의 점들이 빨간 실로 이어진 어텐션 탑을 식구들이 올려다보는 장면'),
    ('cover_08', '07_graph_ontology.html', '7장 · 좌표와 관계', '낮의 연구실, 천장에 매단 구슬 그물 모형', 'ko',
     ['doc', 'asst', 'fly', 'robo'],
     '천장에 매단 색 구슬(개체)과 이름표 없는 끈(관계)으로 된 입체 그물을 초록 실 하나가 세 구슬을 지나며 따라가고, 바닥에는 가지가 뻗은 개념 나무 모양 선반',
     'a hanging 3D web of colored beads connected by strings (a knowledge graph) where one green thread traces a path through three beads; on the floor a shelf shaped like a branching concept tree with small boxes on each branch',
     '구슬 그물 모형에서 초록 실이 길을 따라가고 바닥에 개념 나무 선반이 있는 연구실'),
    ('cover_06', 'practice/index.html', '실전 연습장 — 랩플릭스 운영실', '낮의 운영실, 초록·파랑 손잡이 조작판', 'ko',
     ['asst', 'sia', 'moa', 'robo'],
     '인턴 둘이 초록·파랑 손잡이 조작판 앞에 앉아 직접 운영하고, 하루가 뒤에서 미소, 주판봇이 옆에서 응원. 조작판 위 신호등 네 개',
     'two interns sitting at a long control panel with green and blue knobs and four small traffic lights, operating it themselves; the girl researcher smiles proudly behind them; the robot cheers beside them',
     '인턴 둘이 조작판을 운영하고 하루가 뒤에서 미소 짓는 운영실'),
]
POSE = {'doc': 'center back, calm guiding gesture', 'asst': 'front center', 'fly': 'on the left facing right, pointing with curiosity',
        'robo': 'on the right facing left, holding a wooden abacus', 'sia': 'seated on the left', 'moa': 'seated next to her on the right'}


def prompt(c):
    key, page, title, place, _, chars, meta_ko, meta_en, alt = c
    who = ';\n  '.join('%s, %s' % (CH[w], POSE[w]) for w in chars)
    return ('웹페이지 맨 위에 거는 표지 그림 1장을 만들어 줘.\n- 비율 16:9, 가로 1920px 이상\n- 그림체는 반드시 16비트 RPG풍 픽셀아트 (네모 픽셀이 보이게, 매끈한 일러스트·벡터·수채화·3D 금지)\n'
            '- 첨부한 참고 이미지의 캐릭터를 같은 외형으로, 모두 픽셀아트로 등장\n- 그림 안에 글자·숫자·로고를 넣지 말 것\n- 얼굴과 손은 가장자리에서 떨어진 가운데 영역에, 왼쪽 아래 구석은 밝고 단순하게\n아래 영어 프롬프트를 그대로 써 줘.\n\n'
            'Website top cover illustration, wide 16:9.\nArt style (required, always): 16-bit RPG style pixel art with clearly visible square pixels, limited palette, bold dark outline, 2-3 tone shading, small highlights; no smooth gradients, no painterly, vector, watercolor or 3D look.\n'
            'Match the characters\' proportions and colors of the attached reference images exactly, drawn in this same pixel-art style. Height ratio: doctor 1.00, girl 0.90, interns 0.85, robot 0.72, fruit fly 0.41.\n'
            'Scene: bright daytime lab setting, white walls, big windows with natural light, small lavender, mint and pink accents. No night, no neon.\n'
            'Characters:\n  %s.\nVisual metaphor of the topic: %s.\n'
            'Composition: keep every face and hand inside the central safe area (12%% margin left and right, 10%% top, 18%% bottom); keep the bottom-left corner plain, bright and simple.\n'
            'Mood: curious, warm, a little nervous first lesson turning into confidence.\nNo text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands.') % (who, meta_en)


def main():
    md = ['# 표지 지시문 — 벡터 DB 연구실 (vector_db_lab)', '',
          '목차·장·실전 연습장 맨 위에 거는 표지 9장의 생성 지시문입니다. Genspark 등 이미지 생성 도구에 **위에서부터 순서대로** 붙여 넣으세요.', '',
          '- 그림체: **16비트 RPG풍 픽셀아트 (필수, 고정)** — 매끈한 일러스트·벡터·수채화·3D로 나오면 다시 받습니다.',
          '- 배경: **낮의 연구실** (흰 벽, 큰 창으로 드는 자연광). 밤·네온은 쓰지 않습니다.',
          '- 참고 이미지: GitHub `adminmrobo/fruitfly-lab-expressions`의 기본 그림 — 박사·조수·초파리·주판봇 `images/{doctor,haru,fruitfly,jupanbot}/E13_neutral.png`, 인턴 `images/{sia,moa}/E13_neutral.png`. **목차 표지(cover_00)를 먼저 받아** 그림체를 확인한 뒤, 나머지에 cover_00도 참고 그림으로 함께 올립니다.',
          '- 받은 그림은 `img/cover_00.webp` ~ `img/cover_08.webp`(1600×900, 220 KB 이하)로 넣고 `python3 build/build_all.py`를 다시 돌리면 대체 표지 대신 보입니다. 같은 그림을 잘라 `thumb_NN.webp`(1200×800)와 `og_NN.webp`(1200×630)도 만듭니다.',
          '- 이 시리즈의 이야기: 조수 하루의 첫 인턴 교육. 표지가 뒤로 갈수록 하루가 덜 긴장한 모습이 되게 합니다(cover_00 살짝 긴장 → cover_06 뿌듯한 미소).', '',
          '| 키 | 페이지 | 장소 | 주제 은유 (글자 없이) |', '|---|---|---|---|']
    for c in COVERS:
        md.append('| %s | %s | %s | %s |' % (c[0], c[1], c[3], c[6]))
    md += ['', '**공통 영어 묘사**', ''] + ['- %s: *%s*' % (k, v) for k, v in CH.items()] + ['', '---', '']
    for c in COVERS:
        md += ['## %s · %s' % (c[0], c[2]), '', '| 항목 | 내용 |', '|---|---|', '| 키 · 판 | %s · L (16:9, 1920 이상) |' % c[0], '| 장소 | %s |' % c[3],
               '| 등장 | %s |' % ', '.join({'doc': '박사', 'asst': '조수(하루)', 'fly': '초파리 연구원', 'robo': '주판봇', 'sia': '인턴 시아', 'moa': '인턴 모아'}[w] for w in c[5]),
               '| 대체 글 (alt) | %s |' % c[8], '', '**Genspark에 붙여 넣기 ↓**', '```', prompt(c), '```', '']
    os.makedirs(os.path.join(ROOT, 'docs'), exist_ok=True)
    open(os.path.join(ROOT, 'docs', 'COVER_PROMPTS_vector_db_lab.md'), 'w', encoding='utf-8').write('\n'.join(md))

    img = ['# 벡터 DB 연구실 — 이미지 제작 명세서', '', '## 1. 그림체와 고정 외형', '',
           '- 그림체: 16비트 RPG풍 픽셀아트 (굵은 어두운 외곽선, 2~3단계 명암, 작은 반사광). 캐릭터 팩 `CHAR_lab4`를 따릅니다.',
           '- 장면 조명: 낮의 연구실. 흰 벽, 큰 창의 자연광, 연보라·민트·분홍 소품. 밤·어둠·네온은 쓰지 않습니다.',
           '- 고정 외형: 박사·조수(하루)·초파리 연구원·주판봇 v2·인턴 시아·인턴 모아. 미공개 X1~X3는 본문 방청석에만 나오고 표지에는 넣지 않습니다.',
           '- 그림 안 글자·숫자·로고 금지.', '', '## 2. 필요한 그림 전체', '',
           '| 키 | 판 | 상태 | 쓰는 곳 | 만드는 법 |', '|---|---|---|---|---|',
           '| cover_00 ~ cover_08 | L (16:9, 1600×900) | 새로 그림 (지금은 대체 표지) | 각 페이지 맨 위 표지 | `COVER_PROMPTS_vector_db_lab.md` |',
           '| thumb_00 ~ thumb_08 | 3:2 (1200×800) | 표지에서 자름 | 목차 카드·현황판 | 표지 가운데 기준 자르기 |',
           '| og_00 ~ og_08 | 1200×630 | 표지에서 자름 | 공유 미리보기(og:image) | 표지 가운데 기준 자르기 |',
           '| sc_NN_outro | E (3:2) | 선택 | 아웃트로 장면 자리 | 지금은 캐릭터 팩 표정 그림을 한 줄로 세워 대신합니다 |',
           '| 캐릭터 표정 | A (96px) | 캐릭터 팩 재사용 | 말풍선·대화·대결·방청석 | `build_character_pack.py --pick` (페이지마다 쓰는 키만) |', '',
           '하루의 긴장 표정은 `asst_e15`(당황)·`asst_e20`(땀방울), 풀린 표정은 `asst_e16`(뿌듯)·`asst_e01`(기쁨)을 씁니다. 방청석 X1~X3는 `e15·e02·e04`(걱정)와 `e01·e16`(응원)을 씁니다.', '',
           '## 3. 일관성 지침', '', '- cover_00을 먼저 받아 그림체를 확인하고, 나머지는 cover_00을 참고 그림으로 함께 올립니다.',
           '- 표지는 대결 전 장면입니다. 누가 이길지 드러나는 표정을 쓰지 않습니다.', '- 초파리는 왼쪽에서 오른쪽을, 주판봇은 오른쪽에서 왼쪽을 봅니다.', '']
    open(os.path.join(ROOT, 'docs', 'IMG_vector_db_lab.md'), 'w', encoding='utf-8').write('\n'.join(img))

    items = []
    for c in COVERS:
        n = c[0][-2:]
        chars = ['jupanbot' if w == 'robo' else w for w in c[5]]
        exists = os.path.exists(os.path.join(ROOT, 'img', c[0] + '.webp'))
        items.append({'id': c[0], 'role': 'cover', 'page': c[1], 'path': 'img/%s.webp' % c[0], 'size': [1600, 900], 'characters': chars, 'robot': 'jupanbot-v2',
                      'prompt_en': 'see docs/COVER_PROMPTS_vector_db_lab.md#%s' % c[0], 'source_of': None, 'status': 'ok' if exists else 'missing', 'alt_ko': c[8]})
        for role, size in (('thumb', [1200, 800]), ('og', [1200, 630])):
            items.append({'id': '%s_%s' % (role, n), 'role': role, 'path': 'img/%s_%s.webp' % (role, n), 'size': size, 'characters': chars, 'robot': 'jupanbot-v2',
                          'prompt_en': None, 'source_of': c[0], 'status': 'ok' if os.path.exists(os.path.join(ROOT, 'img', '%s_%s.webp' % (role, n))) else 'missing'})
    pages = [c[1] for c in COVERS]
    man = {'series_ko': 'AI 응용 · 벡터 DB', 'title_ko': '벡터 DB 연구실 (vector_db_lab) — 표에 담기지 않는 말을 저장하는 법', 'site_title': '벡터 DB 연구실 — 표에 담기지 않는 말을 저장하는 법 (목차)',
           'site_url': 'https://adminmrobo.github.io/vector_db_lab/',
           'ontology': {'pages': [{'path': p, 'kg': True, 'export': True} for p in pages], 'files': ['kg/%s/kg.json' % (p.replace('.html', '').replace('/index', '') if p != 'index.html' else 'index') for p in pages]},
           'i18n': {'langs': ['ko'], 'pages': {'ko': len(pages)}, 'readme_langs': ['ko']}, 'languages': ['ko'], 'items': items, 'updated': '2026-11-22'}
    json.dump(man, open(os.path.join(ROOT, 'cover_manifest.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('docs ok', len(items))


if __name__ == '__main__':
    main()
