# -*- coding: utf-8 -*-
"""2장 · 말을 좌표로 — 임베딩과 유사도"""
from lib import *

P = '02_embedding.html'
SM = R['search_mean']; WC = {(x['a'], x['b']): x['cos'] for x in R['word_cos']}; SC = {(x['a'], x['b']): x['cos'] for x in R['sent_cos']}


def body():
    b = three([
        ('무엇을', '문장을 숫자 좌표(벡터)로 바꾸는 임베딩을 만들고, 두 좌표가 얼마나 가까운지 재는 세 가지 자(코사인·유클리드·내적)를 직접 움직여 봅니다.'),
        ('왜 중요한가', '1장에서 글자로는 뜻을 찾지 못했습니다. 뜻을 좌표로 바꾸면 "꿀잼"과 "시간 가는 줄 몰랐다"가 가까운 자리에 놓이고, 가까운 것을 찾는 일이 곧 검색이 됩니다.'),
        ('업무에서는', '고객 문의·리뷰·사내 문서를 "뜻이 비슷한 것끼리" 찾고 묶는 모든 기능(의미 검색, 추천, RAG)의 출발점입니다.')],
        '코드·수식을 몰라도 됩니다. 이 장의 임베딩은 차원마다 이름이 붙은 24차원짜리 교육용 임베딩이라, 숫자가 무슨 뜻인지 눈으로 볼 수 있습니다.',
        [('BoW', 'Bag of Words, 낱말 세기'), ('cos', '코사인, 두 화살표 사이 각도로 잰 닮음'), ('dot', '내적, 자리끼리 곱해 더한 값'), ('d', '차원 수, 좌표 숫자의 개수')])

    b += section('map', '큰 그림 — 이 장은 어디쯤인가',
                 '<div class="mapbar"><span>1장 · 표의 한계</span><i>→</i><span class="on">2장 · 임베딩</span><i>→</i><span>3장 · 벡터 창고</span><i>→</i><span>4장 · LLM과 RAG</span><i>→</i><span>5장 · 현장 사례</span><i>→</i><span>6장 · 어텐션 3D</span><i>→</i><span>7장 · 그래프·온톨로지</span></div>'
                 '<p>1장의 결론은 "글자 ≠ 뜻"이었습니다. 2장은 뜻을 숫자로 바꾸는 법을 배웁니다. 여기서 만든 좌표를 3장에서 창고(벡터 DB)에 저장하고, 4장에서 LLM에게 넘깁니다.</p>'
                 + say('doc', 'front', '이 장은 네 걸음입니다. 낱말 세기(2-1) → 뜻의 좌표(2-2) → 가까움을 재는 자(2-3) → 문장으로 찾기(2-4). 앞 걸음의 한계가 다음 걸음의 이유가 됩니다.'))

    # ── 2-1 낱말 세기
    s = say('doc', 'think', '상황 하나. 컴퓨터는 숫자만 계산합니다. 리뷰 문장을 숫자로 바꾸는 가장 쉬운 방법은 무엇일까요?')
    s += duo(why([('문제 상황', '문장끼리 "얼마나 비슷한가"를 계산하려면 문장이 숫자여야 합니다.'),
                  ('앞 방법의 한계', 'LIKE는 낱말 하나가 들어 있는지만 봅니다. 문장 전체를 비교하지 못합니다.'),
                  ('해법', '사전에 있는 낱말마다 자리를 하나씩 주고, 문장에 그 낱말이 몇 번 나왔는지 적습니다(낱말 세기, BoW). 두 문장은 겹친 낱말이 많을수록 비슷합니다.')],
                 '장바구니 영수증처럼 "사과 2, 우유 1"로 적으면, 두 영수증이 얼마나 비슷한 장보기였는지 셀 수 있습니다.'),
             mathbox('낱말 세기로 바꾼 두 문장의 닮음은 어떻게 계산해요?', '피타고라스 정리와 비율 — 겹친 개수 ÷ (각 문장 길이의 곱)',
                     '닮음 = 겹친 낱말 수 ÷ ( √A의 낱말 수 × √B의 낱말 수 )',
                     [('겹친 낱말 수', '', '두 문장에 함께 나온 낱말 개수'), ('√', '루트', '문장 길이를 화살표 길이로 바꿈'), ('닮음', '', '0이면 하나도 안 겹침, 1이면 같은 낱말 구성')],
                     '"꿀잼 강추" vs "재밌어요 강추": 겹친 낱말은 "강추" 하나. 닮음 = 1 ÷ (√2 × √2) = <b>0.5</b>. "꿀잼" vs "재밌어요"는 겹친 낱말이 없어 <b>0</b>입니다.',
                     '"강추"가 같아서 절반은 닮았다고 나오는데, 정작 뜻이 같은 "꿀잼"과 "재밌어요"는 남남이네요!'))
    s += talk([('asst', 'e15', '시아, 낱말마다 자리를 하나씩 주면 "꿀잼"과 "재밌어요"는 얼마나 비슷하다고 나올까?'),
               ('sia', 'think', '자리가 서로 다르니까… 0이요?'),
               ('robo', 'coin', '낱말을 더 많이 세면 해결이야. 사전을 10만 개로 늘리자!'),
               ('fly', 'point', '10만 개로 늘려도 "꿀잼" 자리와 "재밌" 자리는 따로야. 아래에서 두 문장을 바꿔 가며 겹친 자리를 세어 봐.'),
               ('asst', 'report', '낱말 세기 닮음은 0, 아래 줄의 뜻 점수는 %s예요. 낱말 세기는 뜻을 모르네요.' % num(WC[('꿀잼', '재밌')], 2))])
    s += panel('p21', '실험 · 낱말 세기 vs 뜻 좌표 — 두 문장 비교기', '가상 문장 · 페이지가 직접 계산',
               '<div class="ctrl"><div class="group"><span class="glabel">문장 A</span><input type="text" id="a21" value="꿀잼 강추" aria-label="문장 A"></div>'
               '<div class="group"><span class="glabel">문장 B</span><input type="text" id="b21" value="재밌어요 강추" aria-label="문장 B"></div></div>'
               '<div class="chips" id="pr21"></div><div class="tw"><table class="tb mini-table" id="t21"></table></div>'
               '<section class="kpis" id="k21" aria-label="숫자 요약"></section><div class="insight" id="in21" aria-live="polite"></div>', real=True)
    s += explain(['낱말 세기는 낱말마다 자리 하나를 줍니다. 겹친 낱말이 있어야만 닮음이 0보다 커집니다.',
                  '"꿀잼"과 "재밌어요"처럼 뜻이 같아도 낱말이 다르면 닮음 0. "강추"처럼 뜻과 상관없는 낱말이 겹치면 닮음이 올라갑니다.',
                  '실제 사전은 수만~수십만 낱말이라 자리 수가 그만큼 많고, 문장 하나에서는 거의 모든 자리가 0입니다(희소 벡터).'],
                 '낱말끼리는 서로 남남입니다. "꿀잼과 재밌은 같은 편"이라는 관계를 담을 자리가 없습니다. 다음 단계에서 그 관계를 좌표에 담습니다.')
    s += codefold([('CountVectorizer().fit_transform(reviews)', '리뷰마다 낱말을 세어 희소 벡터를 만듭니다 (scikit-learn)'),
                   ('TfidfVectorizer()', '흔한 낱말의 무게를 낮춘 낱말 세기. 자연어 데이터 분석 강좌 4-2쪽')])
    s += wrapup('낱말 세기는 쉽고 빠르지만, 낱말끼리의 뜻 관계를 모릅니다. 그래서 낱말이 아니라 "뜻의 성분"마다 자리를 주는 방법이 나왔습니다.')
    s += quiz('q21')
    b += step('s1', '2-1', '낱말 세기 — 가장 쉬운 숫자 바꾸기와 그 한계', ['방법: 낱말 세기(BoW) · 희소 벡터', '일상: 장바구니 영수증'], s)

    # ── 2-2 임베딩
    s = say('doc', 'think', '그럼 낱말마다 자리를 주지 말고, "재미", "감동", "공포" 같은 뜻의 성분마다 자리를 주면 어떨까요? 꿀잼과 재밌어요는 같은 성분이 커질 겁니다.')
    s += duo(why([('문제 상황', '같은 뜻을 다른 낱말로 말해도 가까운 숫자가 되어야 합니다.'),
                  ('앞 방법의 한계', '낱말 세기는 낱말끼리 남남이라 "꿀잼"과 "재밌어요"의 닮음이 0입니다.'),
                  ('해법', '뜻의 성분 수십~수천 개로 좌표를 만듭니다(임베딩). 뜻이 비슷한 낱말·문장은 가까운 좌표에 놓입니다. 실제 모델은 이 성분과 값을 수많은 문장에서 스스로 배웁니다.')],
                 '색을 빨강·초록·파랑 세 숫자로 적으면, 주황(255,165,0)과 귤색(255,140,0)은 이름이 달라도 숫자가 가깝습니다.'),
             mathbox('문장이 어떻게 숫자 스물네 개가 돼요?', '벡터의 덧셈과 크기 (고등학교 기하) — 화살표를 이어 붙이고 길이를 1로 맞추기',
                     '문장 좌표 = (낱말 좌표들의 합) ÷ (그 합의 길이)',
                     [('낱말 좌표', '', '사전에 적힌 뜻의 성분. 꿀잼 = 재미 1.0, 좋고 나쁨 +0.9'), ('합', '', '문장에 나온 낱말 좌표를 성분끼리 더함'),
                      ('길이', '', '√(성분² 의 합). 이 값으로 나누면 길이가 1이 됩니다')],
                     '"꿀잼 강추" = 꿀잼(재미 1.0, 좋음 0.9) + 강추(좋음 0.9) = (재미 1.0, 좋음 1.8). 길이 = √(1.0² + 1.8²) ≈ 2.06. 나누면 <b>(재미 0.49, 좋음 0.87)</b>.',
                     '더하고 길이로 나누면 끝이네요. 그래서 "안"이 붙으면 좋음 부호만 뒤집히는 거고요!'))
    s += dbnote('리뷰 표의 text 열에는 문장이 글자 그대로 들어 있습니다(VARCHAR). 검색은 글자 일치뿐입니다.',
                'text 옆에 embedding 열을 하나 더 둡니다. 이 연구실에서는 실수 24개, 실제 서비스에서는 384·768·1,536개 같은 실수 배열입니다.')
    s += talk([('asst', 'e20', '모아, "꿀잼"을 숫자 스물네 개로 쓰면 어느 성분이 가장 클까?'),
               ('moa', 'ok', '음… "재미" 성분이요! 그리고 "좋고 나쁨"이 플러스일 것 같아요.'),
               ('robo', 'wow', '숫자 스물네 개면 부족해. 실제 모델처럼 1,536개로 가자!'),
               ('fly', 'point', '개수보다 "무엇이 가까이 모이나"가 먼저야. 아래 지도에서 "노잼"을 눌러 봐. 꿀잼과 같은 쪽에 있을까?'),
               ('asst', 'report', '노잼은 꿀잼과 같은 "재미" 쪽에 있고 색만 빨개요. 주제는 같고 좋고 나쁨이 반대라서요.')])
    s += crowd('"하루, 이번엔 숫자를 막힘없이 읽네." "인턴들이 질문을 잘 받아 주니까 덜 떠는 것 같아."', moods=('e01', 'e13', 'e16'))
    s += panel('p22', '실험 · 임베딩 해부실 + 낱말 지도', '교육용 24차원 임베딩 · 페이지가 직접 계산',
               '<div class="ctrl"><div class="group"><span class="glabel">문장</span><input type="text" class="wide" id="t22" value="돈이 하나도 안 아깝다 강추" aria-label="임베딩할 문장"></div></div>'
               '<div class="chips" id="pr22"></div><div class="grid2"><div><h4>낱말 찾기 결과</h4><p id="hl22"></p><h4>가장 큰 성분 8개</h4><div class="vbars" id="vb22"></div></div>'
               '<div>' + canvas('cv22', 360, '뜻의 성분 23개를 원 둘레에 놓고 낱말을 그 사이에 그린 지도') + '<p class="small muted">원 둘레의 이름 = 뜻의 성분. 점은 성분의 무게 중심에 놓입니다(RadViz 방식). 파랑 = 좋은 쪽, 빨강 = 나쁜 쪽. ★ = 입력한 문장. 점을 누르면 가장 가까운 낱말 다섯이 나옵니다.</p></div></div>'
               '<div class="insight" id="in22" aria-live="polite"></div>', real=True)
    s += explain(['문장 안에서 사전에 있는 가장 긴 낱말부터 찾고, 그 좌표를 모두 더한 뒤 길이 1로 맞춥니다. "안", "~지 않"은 바로 옆 낱말의 "좋고 나쁨" 부호를 뒤집습니다(빨간 물결).',
                  '뜻이 같은 낱말(꿀잼·재밌·존잼)은 같은 자리에 겹칩니다. 주제가 같고 평가가 반대인 낱말(꿀잼·노잼)은 같은 쪽에 있지만 색이 다릅니다. 낱말 코사인으로는 꿀잼–재밌 %s, 꿀잼–노잼 %s입니다.' % (num(WC[('꿀잼', '재밌')], 2), num(WC[('꿀잼', '노잼')], 2)),
                  '사전에 없는 말("주가", "메뉴")만 있는 문장은 모든 성분이 0인 영벡터가 됩니다. 어디와도 가깝지 않습니다.'],
                 '이 임베딩은 사람이 %d개 낱말에 뜻을 직접 적은 교육용입니다. 실제 임베딩 모델은 성분에 이름이 없고, 수백~수천 개 성분의 값을 문장 수십억 개에서 스스로 배웁니다. 그래서 더 많은 말투를 알지만, 왜 그 숫자인지 설명하기는 어렵습니다.' % R['n']['lex'])
    s += codefold([('model = SentenceTransformer("문장 임베딩 모델 이름")', '미리 학습된 문장 임베딩 모델을 불러옵니다 (sentence-transformers)'),
                   ('vec = model.encode("돈이 하나도 안 아깝다")', '문장 하나 → 실수 384개 같은 배열. 모델마다 개수가 다릅니다'),
                   ('client.embeddings.create(model=..., input=texts)', 'API로 임베딩을 받는 방식. 회사 데이터가 밖으로 나가는지 확인해야 합니다')])
    s += wrapup('임베딩은 "뜻의 성분"으로 만든 좌표입니다. 뜻이 비슷하면 가까이 놓입니다. 이제 "가깝다"를 어떤 자로 잴지 정해야 합니다.')
    s += quiz('q22')
    b += step('s2', '2-2', '뜻의 좌표 — 임베딩', ['방법: 문장 임베딩 · 밀집 벡터', '일상: 색을 세 숫자로'], s)

    # ── 2-3 세 가지 자
    s = say('doc', 'think', '좌표가 생겼으니 "가깝다"를 재야 합니다. 그런데 자가 하나가 아닙니다. 방향을 볼까요, 거리를 볼까요, 둘을 섞을까요?')
    s += duo(why([('문제 상황', '질문 좌표와 리뷰 좌표가 "얼마나 가까운지" 숫자 하나로 말해야 순위를 매길 수 있습니다.'),
                  ('앞 방법의 한계', '눈으로 지도를 보는 것은 24차원, 1,536차원에서는 불가능합니다.'),
                  ('해법', '세 가지 자를 씁니다. ① 코사인: 두 화살표 사이 각도(방향이 같으면 1). ② 유클리드 거리: 끝점 사이 직선 거리(가까우면 0). ③ 내적: 자리끼리 곱해 더한 값(방향과 길이를 함께 봄).')],
                 '두 사람이 같은 쪽을 가리키는가(코사인), 두 사람이 서 있는 곳이 가까운가(거리), 같은 쪽을 얼마나 힘껏 가리키는가(내적)의 차이입니다.'),
             mathbox('cos θ = q·x ÷ (‖q‖ ‖x‖)… 기호가 많아요. 하나씩 읽어 주세요.', '벡터의 내적과 각도 (고등학교 기하) — 코사인 법칙',
                     'cos θ = (q · x) ÷ ( ‖q‖ × ‖x‖ )',
                     [('q, x', '큐, 엑스', '질문 좌표와 리뷰 좌표'), ('q · x', '큐 내적 엑스', '자리끼리 곱해서 모두 더한 값'), ('‖q‖', '노름 큐', '화살표 q의 길이 = √(성분² 의 합)'),
                      ('θ', '세타', '두 화살표 사이의 각도'), ('cos θ', '코사인 세타', '같은 방향 1, 직각 0, 반대 방향 −1')],
                     'q = (0.8, 0.6), x = (0.6, 0.8). 내적 = 0.8×0.6 + 0.6×0.8 = <b>0.96</b>. 길이는 둘 다 √(0.64+0.36) = 1이라 cos θ = 0.96 ÷ 1 = <b>0.96</b>. '
                     '유클리드 거리 = √((0.8−0.6)² + (0.6−0.8)²) = √0.08 ≈ <b>0.28</b>.',
                     '길이가 1이면 코사인과 내적이 같은 값이 되는군요! 그래서 미리 길이를 1로 맞춰 두는 거예요?'))
    s += talk([('asst', 'e15', '시아, 화살표 두 개가 같은 방향인데 하나만 두 배로 길면, 코사인은 어떻게 될까?'),
               ('sia', 'explain', '방향이 같으니까 코사인은 그대로 1이요. 거리는 멀어지고요.'),
               ('robo', 'chart', '그럼 내적이 최고지. 길이까지 쳐주니까 정보가 더 많잖아!'),
               ('fly', 'point', '"길이"가 뭘 뜻하는지가 문제야. 아래에서 B의 길이만 늘려 보고, 세 숫자가 어떻게 바뀌는지 봐.'),
               ('asst', 'report', 'B를 길게 하면 내적만 계속 커져요. 문장에서 길이는 "낱말이 많다"일 때가 많은데… 그게 뜻이 가깝다는 걸까요?')])
    s += panel('p23', '실험 · 화살표 두 개로 세 가지 자 재기', '설명용 2차원 · 페이지가 직접 계산',
               '<div class="ctrl"><div class="group"><span class="glabel">B의 각도</span><input type="range" id="an23" min="0" max="180" value="35" aria-label="B 각도"><span class="val" id="anv23"></span></div>'
               '<div class="group"><span class="glabel">B의 길이</span><input type="range" id="ln23" min="20" max="250" value="100" aria-label="B 길이"><span class="val" id="lnv23"></span></div>'
               '<div class="group"><button class="bt" id="nz23" aria-pressed="false">길이를 1로 맞추기 (정규화)</button></div></div>'
               + canvas('cv23', 300, 'A와 B 두 화살표와 사이 각도') + '<section class="kpis" id="k23" aria-label="세 가지 자"></section><div class="insight" id="in23" aria-live="polite"></div>', real=True)
    s += explain(['코사인은 방향만 봅니다(−1~1, 클수록 닮음). 유클리드 거리는 끝점 사이 거리입니다(0 이상, 작을수록 닮음). 내적은 방향과 길이를 함께 봅니다(범위 제한 없음, 클수록 닮음).',
                  '모든 좌표의 길이를 1로 맞춰 두면(정규화) 세 자가 같은 순위를 냅니다. 그래서 많은 벡터 DB가 정규화한 뒤 내적으로 빠르게 계산합니다.',
                  '정규화하지 않고 내적을 쓰면 "길이가 긴" 좌표, 문장에서는 낱말이 많은 긴 글이 유리해집니다. 이 장의 대결 주제입니다.'],
                 '어떤 자가 맞는지는 임베딩 모델이 어떻게 학습되었는지에 달렸습니다. 모델 설명서가 권하는 자를 따르는 것이 기본입니다.')
    s += codefold([('np.dot(q, x) / (np.linalg.norm(q) * np.linalg.norm(x))', '코사인 유사도'),
                   ("CREATE INDEX ... USING hnsw (embedding vector_cosine_ops);", 'PostgreSQL의 pgvector에서 "코사인으로 재겠다"고 정하는 줄 (3장)')])
    s += wrapup('자는 세 가지, 핵심은 하나입니다. 길이를 1로 맞추면 방향만 남고, 방향이 곧 뜻입니다.')
    s += quiz('q23')
    b += step('s3', '2-3', '가까움을 재는 세 가지 자 — 코사인·유클리드·내적', ['방법: 코사인 유사도 · 정규화', '일상: 같은 쪽을 가리키나'], s)

    # ── 2-4 의미 검색
    s = say('doc', 'think', '이제 1장의 마케팅팀 요청을 다시 받아 봅시다. "재밌다는 리뷰만 모아 주세요." 질문도 좌표로 바꾸면 어떻게 될까요?')
    s += duo(why([('문제 상황', '질문과 뜻이 가까운 리뷰를 순서대로 가져와야 합니다.'),
                  ('앞 방법의 한계', 'LIKE는 글자가 같아야 하고, 동의어 사전은 질문마다 사람이 목록을 만들어야 합니다.'),
                  ('해법', '질문 문장도 같은 임베딩으로 좌표를 만들고, 모든 리뷰와 코사인을 재서 가장 큰 k개를 돌려줍니다. 이것이 의미 검색(벡터 검색)의 전부입니다.')],
                 '도서관 사서에게 "웃기면서 찡한 책"이라고 말하면, 제목에 그 낱말이 없어도 그런 책을 골라 줍니다.'),
             pair('1장에서는', 'LIKE \'%%재밌%%\'은 %d개만 찾고 재현율 %s. 사전을 만들면 좋아지지만 질문마다 목록이 필요했습니다.' % (R['search'][0]['like']['n'], pct(R['search'][0]['like']['r'])),
                  '2장에서는', '질문 "재밌는 영화 리뷰"를 좌표로 바꿔 가장 가까운 리뷰부터 줄 세웁니다. 질문마다 따로 만들 목록이 없습니다.'))
    s += talk([('asst', 'e15', '모아, 1장에서 LIKE로 실패했던 "재밌는 영화 리뷰"를 이번엔 좌표로 찾아볼까?'),
               ('moa', 'cheer', '네! 이번엔 꿀잼도 시간 가는 줄 몰랐다도 나오겠죠?'),
               ('robo', 'happy', '좌표면 무조건 100점이지!'),
               ('fly', 'point', '100점인지는 채점해 봐야 알아. 위의 "찾을 뜻" 목록을 바꿔 가며 세 방법의 F1을 비교해. "감동"을 고르면 수상한 리뷰도 하나 있을 거야.'),
               ('asst', 'report', '여덟 가지 뜻의 F1 평균이 LIKE %s, 동의어 사전 %s, 좌표 검색 %s예요.' % (num(SM['like'], 3), num(SM['dict'], 3), num(SM['vec'], 3)))])
    s += panel('p24', '실험 · 의미 검색기 — LIKE vs 사전 vs 좌표', '가상 데이터 · 이름표로 채점',
               '<div class="ctrl"><div class="group"><span class="glabel">찾을 뜻</span><select class="sel" id="q24"></select></div>'
               '<div class="group"><span class="glabel">직접 입력 (좌표 검색만)</span><input type="text" id="t24" placeholder="예: 웃기면서 찡한 영화" aria-label="직접 입력할 질문"></div>'
               '<div class="group"><span class="glabel">보여 줄 개수 k</span><input type="range" id="k24" min="3" max="10" value="5" aria-label="k"><span class="val" id="kv24"></span></div></div>'
               '<section class="kpis" id="kk24" aria-label="채점"></section><div class="cols3"><div><h4>LIKE 낱말 하나</h4><ul class="res" id="r24a"></ul></div>'
               '<div><h4>동의어 사전</h4><ul class="res" id="r24b"></ul></div><div><h4>좌표 검색 (코사인)</h4><ul class="res" id="r24c"></ul></div></div>'
               '<div class="insight" id="in24" aria-live="polite"></div>', real=True)
    s += explain(['좌표 검색은 질문마다 목록을 만들지 않아도 "꿀잼", "몰입감 최고", "시간 가는 줄 몰랐다"를 함께 찾습니다. 부정어로 뒤집힌 "안 재밌어요"는 뒤로 밀립니다.',
                  '이 작은 데이터에서는 잘 만든 동의어 사전(F1 %s)과 좌표 검색(F1 %s)이 비슷합니다. 차이는 비용입니다. 사전은 질문마다 사람이 만들고, 좌표 검색은 새 질문에도 바로 씁니다.' % (num(SM['dict'], 3), num(SM['vec'], 3)),
                  '"음악이 좋은 영화"에서는 사전이 이기고, "지루하고 재미없는 영화"에서는 좌표 검색이 크게 이깁니다. 어느 쪽도 늘 이기지 않습니다.',
                  '<b>공정성 주의</b> 교육용 임베딩 사전은 이 연구실 리뷰의 말투를 알고 만든 것이라, 좌표 검색 점수가 실제 모델로 처음 보는 데이터를 찾을 때보다 후하게 나왔을 수 있습니다. 동의어 사전도 같은 사정입니다. 이 숫자는 "어떤 차이가 생기는가"를 보는 설명용이고, 실제 성능 비교가 아닙니다.'],
                 '사전에 없는 말만으로 된 질문은 영벡터가 되어 아무것도 찾지 못합니다. 비꼬는 말("와 진짜 감동이다 ^^ 극장에서 잤음")은 겉말대로 감동 쪽에 놓입니다.')
    s += aicheck('"감동" 검색 결과 1위의 정체',
                 '<p>"눈물 나는 감동적인 영화"로 좌표 검색을 하면 위쪽에 이런 리뷰가 섞일 수 있습니다: <b>"와 진짜 감동이다 ^^ 극장에서 잤음"</b> (별점 1점).</p>'
                 '<p><b>확인 질문</b> ① 이 리뷰는 정말 감동받았다는 뜻일까요? ② 검색 결과를 그대로 광고 문구로 쓰기 전에 무엇을 확인해야 할까요?</p>'
                 '<details><summary>생각해 본 뒤 열어 보기</summary><p>① 아닙니다. 비꼬는 말입니다. "감동"이라는 낱말과 "잤음"이 섞여 좌표가 감동 쪽에 놓였습니다. '
                 '② 별점(표에 있는 정형 정보)을 함께 걸러 보면 됩니다. 별점 1점짜리 "감동" 리뷰는 수상합니다. 3장의 "메타데이터 필터"가 바로 이 일을 합니다.</p></details>')
    s += codefold([('scores = reviews_vec @ q_vec', '모든 리뷰 좌표와 질문 좌표의 내적(정규화했으면 코사인)을 한 번에 계산'),
                   ('top = scores.argsort()[::-1][:k]', '점수가 큰 순서로 k개')])
    s += wrapup('질문도 같은 좌표로 바꾸고, 가장 가까운 k개를 가져오면 의미 검색입니다. 다만 리뷰가 수백만 개면 모든 리뷰와 일일이 재기 버겁습니다. 3장의 창고가 그 문제를 풉니다.')
    s += quiz('q24')
    b += step('s4', '2-4', '문장으로 찾기 — 의미 검색 맛보기', ['방법: 벡터 검색 · 상위 k개', '일상: 사서에게 뜻으로 묻기'], s)

    b += duel('d2', '리뷰 찾기의 자 — 코사인(길이 1로) vs 내적(길이 그대로)', '코사인 (길이를 1로 맞춘 뒤 방향만)', '내적 (낱말이 많을수록 길어진 좌표 그대로)',
              '"긴 글이 늘 더 관련 있는 건 아니야. 방향만 보자."', '"낱말 많은 리뷰가 정보도 많지! 길이까지 쳐주는 내적이 최고야."',
              '여덟 가지 뜻의 F1 평균 (정답 수만큼 위에서 자름)')

    b += section('sum', '정리 — 숫자로 바꾸는 법과 재는 법',
                 '<div class="tw"><table class="tb"><tr><th></th><th>낱말 세기 (BoW)</th><th>임베딩</th></tr>'
                 '<tr><td>자리 하나의 뜻</td><td>낱말 하나</td><td>뜻의 성분 하나 (실제 모델은 이름 없음)</td></tr>'
                 '<tr><td>자리 수</td><td>사전 크기 (수만~수십만), 대부분 0</td><td>수백~수천 (예: 384, 768, 1,536), 대부분 0이 아님</td></tr>'
                 '<tr><td>꿀잼 vs 재밌어요</td><td>0 (겹친 낱말 없음)</td><td>%s</td></tr>'
                 '<tr><td>강점</td><td>빠르고 설명이 쉬움, 고유한 낱말·코드에 강함</td><td>같은 뜻 다른 표현을 찾음</td></tr></table></div>'
                 '<div class="tw"><table class="tb"><tr><th>자</th><th>범위</th><th>닮을수록</th><th>쓰는 곳</th></tr>'
                 '<tr><td>코사인</td><td>−1 ~ 1</td><td>커짐</td><td>문장 임베딩 검색의 기본</td></tr>'
                 '<tr><td>유클리드 거리</td><td>0 ~ ∞</td><td>작아짐</td><td>점 사이 실제 거리가 뜻이 있을 때</td></tr>'
                 '<tr><td>내적</td><td>−∞ ~ ∞</td><td>커짐</td><td>길이를 1로 맞춘 뒤 빠른 계산, 또는 길이에 뜻을 담은 모델</td></tr></table></div>' % num(WC[('꿀잼', '재밌')], 2)
                 + bridge('gen', '생성 AI로 치면', 'LLM 안에서도 토큰 하나하나가 먼저 임베딩(수천 차원 좌표)으로 바뀝니다. 다만 LLM 안의 좌표와 검색용 문장 임베딩은 목적이 달라, 검색에는 보통 검색용으로 학습한 임베딩 모델을 따로 씁니다.',
                          'LLM 안의 좌표는 "다음 말 맞히기"에 맞춰져 있어, 그대로 꺼내 쓴다고 좋은 검색 좌표가 되지는 않습니다.'))

    b += outro([('doc', 'front', '오늘 세 줄 정리. ① 낱말 세기는 낱말끼리 남남이다. ② 임베딩은 뜻이 가까우면 좌표가 가깝다. ③ 길이를 1로 맞추고 방향(코사인)으로 잰다.'),
                ('fly', 'arms', '좌표도 비꼬는 말엔 속아. 별점 같은 표 정보가 옆에 있어야 해.'),
                ('robo', 'sigh', '길이가 길수록 좋은 줄 알았는데… 또 손절이네.'),
                ('sia', 'proud', '코사인·거리·내적 범위 표, 외웠어요.'),
                ('moa', 'sparkle', '노트의 "벡터로 할 때" 항목에 embedding 열을 그려 넣었어요!'),
                ('asst', 'e16', '오늘은 덜 떨었어요! 다음 장은 이 좌표 수백만 개를 넣을 창고를 지어요.')],
               '연구실 칠판에 그려진 화살표 두 개 앞에서 하루와 인턴들이 각도를 재는 장면',
               crowd('"하루 오늘 목소리 안 떨렸어!" "인턴들도 잘 따라오네."', moods=('e16', 'e01', 'e01')))
    return b


GLOSS = {
    '임베딩': ['임베딩 (embedding)', '문장·낱말·그림의 뜻을 숫자 좌표(실수 배열)로 바꾼 것. 뜻이 비슷하면 좌표가 가깝습니다.'],
    '벡터': ['벡터 (vector)', '숫자 여러 개를 순서대로 묶은 것. 방향과 길이를 가진 화살표로 볼 수 있습니다.'],
    '차원': ['차원 (dimension)', '좌표 숫자의 개수. 이 연구실은 24차원, 실제 모델은 384·768·1,536차원 등.'],
    '낱말 세기': ['낱말 세기 (Bag of Words)', '낱말마다 자리를 주고 몇 번 나왔는지 적는 방법. 낱말 순서와 뜻은 버립니다.'],
    '희소 벡터': ['희소 벡터 (sparse vector)', '대부분의 자리가 0인 벡터. 낱말 세기 결과가 그렇습니다.'],
    '밀집 벡터': ['밀집 벡터 (dense vector)', '대부분의 자리가 0이 아닌 벡터. 임베딩이 그렇습니다.'],
    '코사인': ['코사인 유사도 (cosine similarity)', '두 화살표 사이 각도로 잰 닮음. 같은 방향 1, 직각 0, 반대 −1.'],
    '유클리드 거리': ['유클리드 거리', '두 끝점 사이 직선 거리. 0에 가까울수록 닮음.'],
    '내적': ['내적 (dot product)', '두 벡터의 같은 자리끼리 곱해 모두 더한 값. 방향과 길이를 함께 반영.'],
    '정규화': ['정규화 (normalization)', '벡터를 길이로 나눠 길이를 1로 맞추는 일. 그러면 코사인과 내적이 같아집니다.'],
    '영벡터': ['영벡터 (zero vector)', '모든 성분이 0인 벡터. 방향이 없어 어떤 것과도 코사인이 0입니다.'],
    '의미 검색': ['의미 검색 (semantic search)', '글자가 아니라 뜻이 가까운 것을 찾는 검색. 벡터 검색이라고도 합니다.'],
    'Word2Vec': ['Word2Vec', '2013년 구글 연구진이 낸 낱말 임베딩 학습법. 주변 낱말로 낱말 좌표를 배웁니다.'],
}

QUIZ = {
    'q21': [{'q': '낱말 세기로 "꿀잼"과 "재밌어요"의 닮음이 0인 이유는?', 'o': ['두 낱말이 서로 다른 자리를 써서', '문장이 짧아서', '코사인이 틀려서'], 'a': 0,
             'why': '낱말마다 자리가 따로라, 겹친 자리가 없으면 닮음이 0입니다. 뜻이 같다는 관계를 담을 곳이 없습니다.', 'hint': '겹친 낱말이 몇 개인가요?'},
            {'q': '"꿀잼 강추"와 "재밌어요 강추"의 낱말 세기 닮음은?', 'o': ['0', '0.5', '1'], 'a': 1,
             'why': '겹친 낱말 "강추" 1개 ÷ (√2 × √2) = 0.5. 뜻이 아니라 "강추"가 같아서 생긴 닮음입니다.', 'hint': '겹친 낱말 수 ÷ (√2 × √2)'}],
    'q22': [{'q': '임베딩에서 "꿀잼"과 "노잼"은 어떻게 놓이나?', 'o': ['완전히 반대편', '같은 주제(재미) 쪽, 좋고 나쁨만 반대', '아무 관계 없음'], 'a': 1,
             'why': '둘 다 "재미" 성분이 크고 "좋고 나쁨"만 부호가 다릅니다. 주제가 같아서 생각보다 가깝다는 점이 실제 임베딩의 흔한 함정입니다.', 'hint': '지도에서 두 점의 위치와 색을 비교해 보세요.'},
            {'q': '실제 임베딩 모델과 이 연구실 교육용 임베딩의 가장 큰 차이는?', 'o': ['실제 모델은 성분에 이름이 없고 데이터에서 스스로 배운다', '실제 모델은 숫자가 아니다', '차이가 없다'], 'a': 0,
             'why': '교육용은 사람이 성분 이름과 값을 정했습니다. 실제 모델은 수백~수천 개 성분을 수많은 문장에서 학습합니다.', 'hint': '"재미", "감동" 같은 이름을 누가 붙였나요?'}],
    'q23': [{'q': 'q = (0.8, 0.6), x = (0.6, 0.8)의 코사인은?', 'o': ['0.28', '0.96', '1.4'], 'a': 1,
             'why': '내적 0.48 + 0.48 = 0.96, 두 길이가 1이므로 코사인 0.96.', 'hint': '자리끼리 곱해서 더하고, 길이의 곱으로 나눕니다.'},
            {'q': '모든 벡터를 길이 1로 맞추면?', 'o': ['코사인과 내적이 같은 순위를 낸다', '거리가 모두 0이 된다', '검색이 불가능해진다'], 'a': 0,
             'why': '길이가 1이면 내적 = 코사인이고, 유클리드 거리도 코사인과 같은 순서가 됩니다.', 'hint': 'cos θ = q·x ÷ (1 × 1)'}],
    'q24': [{'q': '의미 검색에서 질문 문장은 어떻게 다루나?', 'o': ['LIKE 조건으로 바꾼다', '리뷰와 같은 임베딩으로 좌표를 만든다', '사람이 동의어 목록을 만든다'], 'a': 1,
             'why': '질문도 같은 방식으로 좌표로 바꿔야 리뷰 좌표와 거리를 잴 수 있습니다.', 'hint': '같은 지도 위에 올려야 거리를 잴 수 있습니다.'},
            {'q': '별점 1점인데 "감동" 검색 상위에 나온 리뷰를 걸러 내려면?', 'o': ['차원을 늘린다', '별점 같은 표 정보로 함께 거른다', '코사인을 내적으로 바꾼다'], 'a': 1,
             'why': '비꼬는 말은 좌표만으로 잘 안 잡힙니다. 별점 같은 정형 정보(메타데이터)로 함께 거르면 됩니다.', 'hint': '표에 남아 있는 숫자 정보를 떠올려 보세요.'}],
}

JS = r'''
var D=VL.load(),RV=D.reviews,DIMS=VL.DIMS;
/* 2-1 */
(function(){var P=[['꿀잼 강추','재밌어요 강추'],['꿀잼','시간 가는 줄 몰랐다'],['재밌어요','안 재밌어요'],['돈 아깝다','배우가 아깝다'],['OST가 너무 좋다','음악이 귀에 맴돈다']];
  $('#pr21').innerHTML=P.map(function(p,i){return '<button class="bt" data-i="'+i+'">'+p[0]+' / '+p[1]+'</button>'}).join('');
  $$('#pr21 .bt').forEach(function(b){b.addEventListener('click',function(){var p=P[+b.dataset.i];$('#a21').value=p[0];$('#b21').value=p[1];run();})});
  function words(t){return t.replace(/[.,!?]/g,' ').split(/\s+/).filter(Boolean);}
  function run(){var A=words($('#a21').value),B=words($('#b21').value),V=[];A.concat(B).forEach(function(w){if(V.indexOf(w)<0)V.push(w)});
    var ca=V.map(function(w){return A.filter(function(x){return x===w}).length}),cb=V.map(function(w){return B.filter(function(x){return x===w}).length});
    var bow=VL.cos(ca,cb),emb=VL.cos(VL.embed($('#a21').value).v,VL.embed($('#b21').value).v),ov=V.filter(function(w,i){return ca[i]&&cb[i]}).length;
    $('#t21').innerHTML='<tr><th>낱말 (자리)</th>'+V.map(function(w){return '<th class="n">'+VL.esc(w)+'</th>'}).join('')+'</tr><tr><td>문장 A</td>'+ca.map(function(c){return '<td class="n">'+c+'</td>'}).join('')+'</tr><tr><td>문장 B</td>'+cb.map(function(c){return '<td class="n">'+c+'</td>'}).join('')+'</tr>';
    VL.kpis($('#k21'),[[V.length+'자리','이 두 문장만의 사전 크기','i'],[ov+'개','겹친 낱말','a'],[bow.toFixed(2),'낱말 세기 닮음 (코사인)','r'],[emb.toFixed(2),'뜻 점수 (교육용 임베딩 코사인)','g']]);
    $('#in21').innerHTML='<p class="'+(Math.abs(bow-emb)>.4?'r':'g')+'">'+(Math.abs(bow-emb)>.4?'낱말 세기와 뜻 점수가 크게 엇갈립니다. 낱말 세기는 글자가 같은 낱말만 같다고 봅니다.':'이 쌍은 두 점수가 비슷합니다. 다른 버튼도 눌러 보세요.')+'</p><p class="m">낱말은 띄어쓰기로만 나눴습니다. 실제로는 형태소 분석(자연어 강좌 3장)으로 "재밌어요"를 "재밌 + 어요"처럼 더 잘게 나눕니다.</p>';}
  $('#a21').addEventListener('input',run);$('#b21').addEventListener('input',run);run();
})();
/* 2-2 */
(function(){var cv=$('#cv22'),PRE=['돈이 하나도 안 아깝다 강추','꿀잼','노잼','하나도 안 무섭다','노래 듣고 소름','LP-204 오류가 떠요','오늘 저녁 메뉴 추천','랩플릭스 주가'];
  $('#pr22').innerHTML=PRE.map(function(p){return '<button class="bt" data-t="'+p+'">'+p+'</button>'}).join('');
  var W=['재밌','꿀잼','노잼','지루','몰입','감동','눈물','여운','신파','무섭','소름','쫄깃','긴장감','웃김','터졌','썰렁','스토리','반전','개연성','결말','연기','배우','발연기','영상미','액션','CG','OST','음악','노래','돈값','아깝','날렸','러닝타임','질질','마라탕','맛집','날씨','첫눈','미세먼지','출근','야근','회의','무료','이벤트','쿠폰','요금제','결제','할인','환불','해지','계정','화질','자막','오류','점검','다운','고객센터'];
  var N=DIMS.length,anc=[];for(var i=1;i<N;i++){var a=-Math.PI/2+(i-1)/(N-1)*Math.PI*2;anc.push([Math.cos(a),Math.sin(a)]);}
  function rad(v){var sx=0,sy=0,sw=0;for(var i=1;i<N;i++){var w=Math.abs(v[i]);sx+=w*anc[i-1][0];sy+=w*anc[i-1][1];sw+=w;}return sw?[sx/sw,sy/sw]:[0,0];}
  var pts=W.map(function(w){var v=VL.wordVec(w);return {w:w,v:v,p:rad(v)}}),sel=null,cur=null;
  function draw(){var f=fit(cv),g=f.c,cx=f.W/2,cy=f.H/2,Rr=Math.min(f.W,f.H)/2-40;g.fillStyle='#fff';g.fillRect(0,0,f.W,f.H);g.strokeStyle='#e6ebf1';g.beginPath();g.arc(cx,cy,Rr,0,6.2832);g.stroke();
    g.font='11px "IBM Plex Sans KR",sans-serif';g.fillStyle='#5b6874';anc.forEach(function(a,i){var x=cx+a[0]*(Rr+14),y=cy+a[1]*(Rr+14);g.textAlign=a[0]>.3?'left':a[0]<-.3?'right':'center';g.fillText(DIMS[i+1],x,y+4);});g.textAlign='left';
    pts.forEach(function(p){var x=cx+p.p[0]*Rr,y=cy+p.p[1]*Rr;p.x=x;p.y=y;VL.dot2(g,x,y,sel===p?7:5,p.v[0]<-.05?'#c9302c':p.v[0]>.05?'#1e55c8':'#8a96a3',.85);});
    g.font='12px "IBM Plex Sans KR",sans-serif';g.fillStyle='#16212b';pts.forEach(function(p){if(sel===p||(sel&&sel.nb.indexOf(p.w)>=0))g.fillText(p.w,p.x+7,p.y-6);});
    if(cur){var q=rad(cur.v),x=cx+q[0]*Rr,y=cy+q[1]*Rr;g.fillStyle='#a35c00';g.font='700 22px sans-serif';g.fillText('★',x-8,y+8);}
    stamp(g,f.W,'교육용 24차원 · RadViz 지도');}
  cv.addEventListener('click',function(e){var r=cv.getBoundingClientRect(),mx=e.clientX-r.left,my=e.clientY-r.top,b=null,bd=1e9;pts.forEach(function(p){var d=(p.x-mx)*(p.x-mx)+(p.y-my)*(p.y-my);if(d<bd){bd=d;b=p;}});
    if(b&&bd<400){sel=b;b.nb=pts.filter(function(p){return p!==b}).map(function(p){return [VL.cos(b.v,p.v),p.w]}).sort(function(x,y){return y[0]-x[0]}).slice(0,5).map(function(x){return x[1]});
      $('#in22').innerHTML='<p class="m"><b>'+b.w+'</b>와 가장 가까운 낱말: '+pts.filter(function(p){return b.nb.indexOf(p.w)>=0}).map(function(p){return p.w+' ('+VL.cos(b.v,p.v).toFixed(2)+')'}).join(', ')+'</p>';draw();}});
  function run(){var t=$('#t22').value,e=VL.embed(t);cur=e;$('#hl22').innerHTML=e.hits.length?VL.mark(t,e.hits):'<span class="muted">'+VL.esc(t)+' — 사전에 있는 낱말이 없습니다.</span>';VL.dimBars($('#vb22'),e.v);
    if(!sel)$('#in22').innerHTML='<p class="'+(e.len?'g':'r')+'">'+(e.len?'찾은 낱말 '+e.hits.length+'개의 좌표를 더해 길이 1로 맞췄습니다. 노란 형광은 사전 낱말, 빨간 물결은 부정어 때문에 "좋고 나쁨"이 뒤집힌 낱말입니다.':'영벡터입니다. 이 문장은 어떤 리뷰와도 가깝지 않다고 나옵니다. 사전에 없는 말의 한계입니다.')+'</p>';draw();}
  $$('#pr22 .bt').forEach(function(b){b.addEventListener('click',function(){$('#t22').value=b.dataset.t;sel=null;run();})});$('#t22').addEventListener('input',function(){sel=null;run();});
  run();Loop.add(cv,function(dt){if(dt===0)draw();});
})();
/* 2-3 */
(function(){var cv=$('#cv23'),nz=false;
  function draw(){var an=+$('#an23').value,ln=+$('#ln23').value/100;if(nz)ln=1;$('#anv23').textContent=an+'°';$('#lnv23').textContent=ln.toFixed(2);
    var a0=30*Math.PI/180,A=[Math.cos(a0),Math.sin(a0)],b0=(30+an)*Math.PI/180,B=[ln*Math.cos(b0),ln*Math.sin(b0)];
    var f=fit(cv),g=f.c,cx=f.W/2,cy=f.H*.62,sc=Math.min(f.W/6.5,f.H*.56/2.6);g.fillStyle='#fff';g.fillRect(0,0,f.W,f.H);g.strokeStyle='#e6ebf1';g.beginPath();g.moveTo(0,cy);g.lineTo(f.W,cy);g.moveTo(cx,0);g.lineTo(cx,f.H);g.stroke();
    function arrow(v,c,lab){var x=cx+v[0]*sc,y=cy-v[1]*sc;g.strokeStyle=c;g.lineWidth=3;g.beginPath();g.moveTo(cx,cy);g.lineTo(x,y);g.stroke();var ang=Math.atan2(cy-y,x-cx);g.fillStyle=c;g.beginPath();g.moveTo(x,y);g.lineTo(x-10*Math.cos(ang-.4),y+10*Math.sin(ang-.4));g.lineTo(x-10*Math.cos(ang+.4),y+10*Math.sin(ang+.4));g.fill();g.font='700 14px sans-serif';g.fillText(lab,x+6,y-6);g.lineWidth=1;}
    g.strokeStyle='#a35c00';g.beginPath();g.arc(cx,cy,34,-a0,-b0,true);g.stroke();g.fillStyle='#a35c00';g.font='13px sans-serif';g.fillText('θ='+an+'°',cx+38*Math.cos((a0+b0)/2),cy-38*Math.sin((a0+b0)/2));
    g.setLineDash([4,4]);g.strokeStyle='#9b3fb5';g.beginPath();g.moveTo(cx+A[0]*sc,cy-A[1]*sc);g.lineTo(cx+B[0]*sc,cy-B[1]*sc);g.stroke();g.setLineDash([]);
    arrow(A,'#1e55c8','A');arrow(B,'#c42a6e','B');stamp(g,f.W,'설명용 2차원');
    var cs=VL.cos(A,B),eu=VL.euclid(A,B),dt=VL.dot(A,B);VL.kpis($('#k23'),[[cs.toFixed(2),'코사인 (−1~1, 클수록 닮음)','g'],[eu.toFixed(2),'유클리드 거리 (작을수록 닮음, 보라 점선)','m'],[dt.toFixed(2),'내적 (클수록 닮음)','a'],[ln.toFixed(2),'B의 길이 (A는 1)','i']]);
    $('#in23').innerHTML='<p class="'+(ln>1.3&&an<45?'r':'g')+'">'+(nz?'길이를 1로 맞췄습니다. 이제 내적 = 코사인입니다. 각도만 바꿔 보세요.':ln>1.3&&an<45?'B가 길어지자 내적이 '+dt.toFixed(2)+'로 커졌습니다. 방향(코사인)은 그대로인데 말이죠. 길이가 "뜻이 더 가깝다"는 뜻일까요?':'각도를 0°에 가깝게 하면 코사인이 1, 90°면 0, 180°면 −1이 됩니다.')+'</p>';}
  $('#an23').addEventListener('input',draw);$('#ln23').addEventListener('input',draw);$('#nz23').addEventListener('click',function(){nz=!nz;this.setAttribute('aria-pressed',nz?'true':'false');draw();});
  Loop.add(cv,function(dt){if(dt===0)draw();});
})();
/* 2-4 */
(function(){var Q=D.searchq,sel=$('#q24');sel.innerHTML=Q.map(function(q,i){return '<option value="'+i+'">'+q.q+'</option>'}).join('');
  function li(r,s,q){var ok=q?VL.rel(r,q.asp):null;return '<li class="'+(ok===null?'nt':ok?'ok':'no')+'">'+(s!=null?'<span class="sc">'+s.toFixed(2)+'</span>':'')+'<small>'+r.title+' · '+VL.stars(r.stars)+(ok===null?'':ok?' · 정답':' · 정답 아님')+'</small>'+VL.esc(r.text)+'</li>';}
  function run(){var k=+$('#k24').value;$('#kv24').textContent=k+'개';var t=$('#t24').value.trim(),q=t?null:Q[+sel.value],qt=t||q.q,qv=VL.embed(qt).v;
    var vec=VL.topk(RV,function(r){return VL.cos(qv,r.vec)},k);$('#r24c').innerHTML=vec.map(function(x){return li(x.it,x.s,q)}).join('');
    if(q){var L=VL.like(RV,q.like),Di=VL.likeAny(RV,q.dict);$('#r24a').innerHTML='<li class="nt"><small>LIKE \'%'+q.like+'%\' · '+L.length+'개 중 앞 '+Math.min(k,L.length)+'개</small></li>'+L.slice(0,k).map(function(r){return li(r,null,q)}).join('');
      $('#r24b').innerHTML='<li class="nt"><small>'+q.dict.join(', ')+' · '+Di.length+'개 중 앞 '+Math.min(k,Di.length)+'개</small></li>'+Di.slice(0,k).map(function(r){return li(r,null,q)}).join('');
      var n=RV.filter(function(r){return VL.rel(r,q.asp)}).length,V=VL.topk(RV,function(r){return VL.cos(qv,r.vec)},n).map(function(x){return x.it});
      var a=VL.prf(L,RV,q.asp),b=VL.prf(Di,RV,q.asp),c=VL.prf(V,RV,q.asp);
      VL.kpis($('#kk24'),[[n+'개','이 뜻의 정답 리뷰','i'],[a.f1.toFixed(3),'LIKE F1','r'],[b.f1.toFixed(3),'동의어 사전 F1','a'],[c.f1.toFixed(3),'좌표 검색 F1 (위에서 '+n+'개)','g']]);
      $('#in24').innerHTML='<p class="'+(c.f1>=b.f1?'g':'a')+'">'+(c.f1>=b.f1?'좌표 검색이 사전과 같거나 더 좋습니다. 질문마다 목록을 만들지 않았는데도요.':'이 뜻에서는 잘 만든 사전이 좌표 검색보다 낫습니다. 사전의 낱말이 정답 리뷰의 말투를 거의 다 덮었기 때문입니다.')+'</p>';}
    else{$('#r24a').innerHTML='<li class="nt">직접 입력한 질문에는 정답 이름표가 없어 LIKE·사전 비교를 하지 않습니다.</li>';$('#r24b').innerHTML='';
      VL.kpis($('#kk24'),[[VL.embed(qt).hits.length+'개','질문에서 찾은 사전 낱말','i'],[vec.length?vec[0].s.toFixed(2):'—','1위 점수','g']]);
      $('#in24').innerHTML='<p class="m">점수는 코사인입니다. 질문에서 사전 낱말을 하나도 못 찾으면 모든 점수가 0입니다.</p>';}}
  sel.addEventListener('change',function(){$('#t24').value='';run();});$('#t24').addEventListener('input',run);$('#k24').addEventListener('input',run);run();
})();
/* 대결 2 */
Duel({el:'#d2',run:function(){var f=0,r=0;D.searchq.forEach(function(q){var qv=VL.embed(q.q).v,n=RV.filter(function(x){return VL.rel(x,q.asp)}).length;
    f+=VL.prf(VL.topk(RV,function(x){return VL.cos(qv,x.vec)},n).map(function(x){return x.it}),RV,q.asp).f1;
    r+=VL.prf(VL.topk(RV,function(x){return VL.dot(qv,VL.embed(x.text).raw)},n).map(function(x){return x.it}),RV,q.asp).f1;});return {fly:f/D.searchq.length,robo:r/D.searchq.length}},scale:1,fmt:function(v){return v.toFixed(3)},
  report:function(r){return '여덟 가지 뜻의 F1 평균: 코사인 '+r.fly.toFixed(3)+', 길이 그대로 내적 '+r.robo.toFixed(3)+'. 내적은 "재미도 있고 감동도 있고 연기도 좋고…"처럼 낱말 많은 리뷰를 위로 올렸어요.'},
  verdict:{fly:'초파리 승. 길이를 맞추지 않으면 "낱말이 많다"가 "뜻이 가깝다"를 이깁니다. 1장 특징 ④(길이·단위가 없다)가 여기서 다시 나왔습니다. 길이를 1로 맞추면 내적도 코사인과 같아지니, 자 자체보다 "정규화했나"가 핵심입니다.',robo:'주판봇 승.',draw:'무승부.'}});
'''


def build_page():
    nav = [('#s1', '2-1 낱말 세기'), ('#s2', '2-2 임베딩'), ('#s3', '2-3 세 가지 자'), ('#s4', '2-4 의미 검색'), ('#duel', '대결'), ('#sum', '정리')]
    cov = cover('cover_02', '벡터 DB 연구실 · 2장', '말을 좌표로', chars=(('doc', 'board'), ('asst', 'e16'), ('fly', 'point'), ('robo', 'coin')))
    hr = hero('벡터 DB 연구실 · 2장 · 임베딩과 유사도', '말을 좌표로',
              '"꿀잼"과 "시간 가는 줄 몰랐다"를 같은 뜻이라고 컴퓨터가 알게 하려면, 문장을 어떤 숫자로 바꿔야 할까?',
              '두 번째 수업. 하루는 인턴들에게 문장을 숫자 좌표로 바꾸는 법을 묻습니다. 낱말을 세어 보고, 뜻의 성분으로 좌표를 만들고, 화살표 두 개의 각도를 잽니다.',
              [('24차원', '교육용 임베딩 (성분마다 이름 있음)', 'i'), (num(WC[('꿀잼', '재밌')], 2), '꿀잼 ↔ 재밌 뜻 점수', 'g'),
               (num(SC[('재밌어요', '안 재밌어요')], 2), '재밌어요 ↔ 안 재밌어요', 'a'), (num(SM['vec'], 3), '좌표 검색 F1 평균 (LIKE %s)' % num(SM['like'], 3), 'm')],
              [('doc', 'board', '1장에서 "글자 ≠ 뜻"을 확인했죠. 오늘은 뜻을 숫자로 바꿉니다.'),
               ('asst', 'e15', '좋아요… 시아, 모아, 오늘도 질문 많이 할게요. 틀려도 괜찮아요. 저도 떨리니까요!'),
               ('sia', 'smile', '저는 오늘 수식도 따라가 볼게요.'), ('moa', 'cheer', '노트 새 쪽 펼쳤어요!')],
              crowd('"오늘은 하루가 먼저 웃었어." "어제보다 낫다!"', moods=('e13', 'e01', 'e16')))
    return build(P, title='2장 · 말을 좌표로 — 임베딩과 유사도 | 벡터 DB 연구실',
                 desc='낱말 세기의 한계, 뜻의 좌표(임베딩), 코사인·유클리드·내적, 의미 검색을 24차원 교육용 임베딩으로 직접 움직여 봅니다.',
                 nav=nav, cover_html=cov, hero=hr,
                 body=body() + footer([('리뷰 데이터', '이 연구실이 만든 가상 데이터'), ('교육용 임베딩', 'code/lexicon.py — 사람이 뜻을 정한 %d개 낱말, 24차원' % R['n']['lex']),
                                       ('낱말 임베딩', 'Mikolov 외 (2013) Efficient Estimation of Word Representations in Vector Space, arXiv:1301.3781'),
                                       ('문장 임베딩', 'Reimers & Gurevych (2019) Sentence-BERT, EMNLP-IJCNLP 2019'),
                                       ('낱말 세기·TF-IDF', '<a href="%s">인공지능과 자연어 데이터 분석 강좌</a> 4장' % NLP)],
                                      ['24차원 교육용 임베딩과 RadViz 지도는 설명용입니다. 실제 모델의 좌표는 성분 이름이 없습니다.', '2-3의 화살표는 설명용 2차원입니다.'],
                                      prev=('01_why_not_table.html', '1장 · 표에 담기지 않는 말'), nxt=('03_vector_store.html', '3장 · 벡터 창고')),
                 gloss=GLOSS, quizzes=QUIZ, page_js=JS, og='og_02')


if __name__ == '__main__':
    print(build_page())
