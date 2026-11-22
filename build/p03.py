# -*- coding: utf-8 -*-
"""3장 · 벡터 창고 — 벡터 DB의 저장·색인·검색"""
from lib import *

P = '03_vector_store.html'
IVF = {x['nprobe']: x for x in R['ivf']}; GR = {x['ef']: x for x in R['graph']}; ST = R['storage']


def body():
    b = three([
        ('무엇을', '2장에서 만든 좌표를 창고(벡터 DB)에 넣고, 수백만 개 중 가까운 것을 "모두와 재지 않고" 빨리 찾는 두 가지 색인(서랍 색인 IVF, 길 찾기 그래프 HNSW)을 움직여 봅니다.'),
        ('왜 중요한가', '질문 하나에 리뷰 100만 개와 모두 코사인을 재면 느리고 비쌉니다. 벡터 DB는 "조금 덜 정확해도 훨씬 빠르게"를 고를 수 있게 해 줍니다.'),
        ('업무에서는', '벡터 DB를 고를 때 비교하는 것들 — 저장 용량, 검색 속도, 재현율, 메타데이터 필터, 관계형 DB와 함께 쓰기 — 을 숫자로 판단할 수 있게 됩니다.')],
        '코드·수식을 몰라도 됩니다. 점이 흩어진 지도 위를 누르면 그 자리가 질문이 되고, 색인이 어떤 길로 찾아가는지 보입니다.',
        [('ANN', 'Approximate Nearest Neighbor, 근사 최근접 이웃 검색'), ('IVF', 'Inverted File index, 서랍(군집)으로 나눈 색인'),
         ('HNSW', 'Hierarchical Navigable Small World, 여러 층 길 찾기 그래프'), ('PQ', 'Product Quantization, 좌표를 잘게 나눠 압축'), ('k', '돌려줄 가까운 결과 수')])

    b += section('map', '큰 그림 — 이 장은 어디쯤인가',
                 '<div class="mapbar"><span>1장 · 표의 한계</span><i>→</i><span>2장 · 임베딩</span><i>→</i><span class="on">3장 · 벡터 창고</span><i>→</i><span>4장 · LLM과 RAG</span><i>→</i><span>5장 · 현장 사례</span><i>→</i><span>6장 · 어텐션 3D</span><i>→</i><span>7장 · 그래프·온톨로지</span></div>'
                 '<p>2장 마지막에 "모든 리뷰와 일일이 재기 버겁다"는 숙제가 남았습니다. 이 장은 넣기(3-1) → 서랍으로 찾기(3-2) → 길 따라 찾기(3-3) → 표 조건 함께 걸기(3-4) → 관계형 DB와 나눠 맡기(3-5) 순서로 갑니다.</p>'
                 + '<div class="steps" aria-label="이 장의 맞바꿈"><div><span class="n">⇄</span><h4>이 장의 손잡이는 모두 시소입니다</h4><p>한쪽 끝은 <b>빠르기</b>(비교 횟수가 적다), 다른 끝은 <b>빠짐없음</b>(재현율이 높다). nprobe·ef·먼저 찾을 수를 올리면 빠짐없음 쪽으로, 내리면 빠르기 쪽으로 기웁니다.</p></div>'
                   '<div><span class="n">?</span><h4>먼저 정할 것</h4><p>"재현율 95%%는 지킨다"처럼 빠짐없음의 바닥을 먼저 정하고, 그 안에서 가장 빠른 설정을 고릅니다.</p></div>'
                   '<div><span class="n">✓</span><h4>늘 숫자로</h4><p>설정을 바꾸면 재현율과 비교 횟수를 함께 다시 잽니다. 이 장의 실험이 모두 그 두 숫자를 보여 줍니다.</p></div></div>'
                 + say('doc', 'front', '이 장의 핵심 낱말은 "근사"입니다. 정답 10개 중 9.5개만 찾아도 100배 빠르다면, 대부분의 서비스는 그쪽을 고릅니다. 얼마나 덜 정확한지는 꼭 숫자로 확인합니다.'))

    # ── 3-1 넣기
    s = say('doc', 'think', '상황 하나. 리뷰가 하루 1만 건씩 쌓여 1년이면 수백만 건입니다. 좌표와 원문, 별점을 어디에 어떻게 함께 넣어 둘까요?')
    s += duo(why([('문제 상황', '좌표(실수 수백 개)와 원문, 별점·장르 같은 정보를 함께 저장하고, "가까운 좌표"를 빨리 찾아야 합니다.'),
                  ('앞 방법의 한계', '관계형 DB의 보통 색인(B-트리)은 "같은 값·범위"를 찾는 정렬 목록이라 "가까운 좌표"를 찾지 못합니다.'),
                  ('해법', '벡터 DB는 한 레코드에 번호·좌표·메타데이터를 함께 넣고, 가까운 좌표를 찾는 전용 색인(ANN 색인)을 만들어 둡니다.')],
                 '책 정보 카드(제목·저자·분류)와 함께 "이 책과 분위기가 비슷한 책 지도"를 따로 붙여 두는 도서관입니다.'),
             mathbox('좌표 100만 개를 넣으면 몇 GB가 돼요? 계산기 없이는 무서워요.', '곱셈과 단위 바꾸기 — 바이트(B) → 기가바이트(GB)',
                     '저장 용량 = 건수 × 차원 수 × 4바이트',
                     [('건수', '', '저장할 문장 수'), ('차원 수', 'd', '좌표 숫자의 개수 (384, 768, 1,536 …)'), ('4바이트', '', '실수 하나를 적는 데 드는 크기(32비트 실수)'),
                      ('GB', '기가바이트', '10억 바이트')],
                     '리뷰 100만 개 × 768차원 × 4바이트 = 3,072,000,000바이트 ≈ <b>%s GB</b>. 색인(그래프 연결선 등)은 이와 별도로 더 듭니다.' % num(ST['gb'], 2),
                     '원문보다 좌표가 훨씬 무겁네요! 그래서 압축 방법(양자화)이 따로 있군요.'))
    s += dbnote('리뷰 표: 번호, 영화 번호, 별점, 날짜, 문장. 색인은 B-트리라서 "별점 = 4", "날짜 ≥ 9월"을 빨리 찾습니다.',
                '레코드: 번호 + 좌표(실수 d개) + 메타데이터(장르·별점·날짜) + 원문. 색인은 "이 좌표와 가까운 것"을 빨리 찾는 ANN 색인입니다.')
    s += talk([('asst', 'e15', '시아, 리뷰 100만 개를 768차원으로 저장하면 몇 GB쯤일까?'),
               ('sia', 'think', '100만 곱하기 768 곱하기 4… 30억쯤이니까 3GB?'),
               ('robo', 'calc', '3GB면 껌이지! 1억 개도 그냥 다 넣자!'),
               ('fly', 'point', '1억 개면 몇 GB야? 아래 계산기에서 건수를 1억으로, 차원을 1,536으로 올려 봐.'),
               ('asst', 'report', '%s GB예요… 메모리에 다 올리기 어려운 크기예요.' % num(1e8 * 1536 * 4 / 1e9, 0))])
    s += crowd('"하루가 계산을 인턴한테 맡겼어!" "그게 교육이지." "근데 1억은 너무했다…"', moods=('e04', 'e13', 'e24'))
    s += panel('p31', '실험 · 레코드 미리보기와 저장 용량 계산기', '가상 데이터 · 설명용 계산',
               '<div class="ctrl"><div class="group"><button class="bt" id="nx31">다른 리뷰 넣어 보기</button></div></div>'
               '<div class="prompt" id="rec31" aria-live="polite"></div>'
               '<div class="ctrl"><div class="group"><span class="glabel">건수</span><input type="range" id="n31" min="4" max="9" step="0.5" value="6" aria-label="건수(10의 거듭제곱)"><span class="val" id="nv31"></span></div>'
               '<div class="group"><span class="glabel">차원 수</span><select class="sel" id="d31"><option>24</option><option>384</option><option selected>768</option><option>1536</option><option>3072</option></select></div>'
               '<div class="group"><span class="glabel">저장 방식</span><button class="bt" data-q="4" aria-pressed="true">실수 4바이트</button><button class="bt" data-q="1" aria-pressed="false">압축 1바이트 (양자화)</button></div></div>'
               '<section class="kpis" id="k31" aria-label="용량"></section><div class="insight" id="in31" aria-live="polite"></div>', real=True)
    s += explain(['한 레코드 = 번호 + 좌표 + 메타데이터 + (원문 또는 원문 위치). 좌표는 검색에, 메타데이터는 거르기에, 원문은 사람·LLM에게 보여 주는 데 씁니다.',
                  '용량은 건수와 차원 수에 비례합니다. 차원을 두 배로 늘리면 저장 용량도, 거리 계산 시간도 두 배입니다.',
                  '좌표 숫자를 1바이트로 줄이는 압축(양자화, PQ)을 쓰면 용량이 크게 줄지만 거리 계산이 조금 부정확해집니다.'],
                 '용량 계산은 좌표만 센 값입니다. 실제로는 색인 구조, 메타데이터, 복제본이 더해집니다. 도입 전에는 쓰려는 제품의 설명서로 다시 어림해야 합니다.')
    s += codefold([("collection.add(ids=[...], embeddings=[...], metadatas=[{'genre': '코미디', 'stars': 5}], documents=[...])", '벡터 DB에 레코드를 넣는 전형적인 모양 (Chroma 등)'),
                   ('ALTER TABLE review ADD COLUMN embedding vector(768);', 'PostgreSQL + pgvector: 리뷰 표에 768차원 좌표 열을 추가')])
    s += wrapup('벡터 DB의 한 레코드는 좌표·메타데이터·원문의 묶음입니다. 좌표는 생각보다 무겁습니다. 이제 이 좌표들 사이에서 빨리 찾는 법을 봅니다.')
    s += quiz('q31')
    b += step('s1', '3-1', '창고에 넣기 — 레코드 모양과 저장 용량', ['방법: 레코드 · 메타데이터 · 양자화', '일상: 도서 카드 + 분위기 지도'], s)

    # ── 3-2 IVF
    i4 = IVF[4]
    s = recap('재현율', '<p>진짜 가장 가까운 10개 중 색인이 찾아온 비율입니다. 10개 중 9개를 찾으면 90%%입니다. 1장의 재현율(정답 중 찾은 비율)과 같은 생각을 "가까운 10개"에 쓴 것입니다.</p>')
    s += say('doc', 'think', '질문 하나가 들어올 때마다 리뷰 100만 개와 모두 코사인을 재면 어떻게 될까요? 1초에 질문 수천 개가 들어오는 서비스라면요.')
    s += duo(why([('문제 상황', '가장 가까운 k개를 찾으려면, 원래는 모든 점과 거리를 재야 합니다(전수 비교). 점이 많으면 느립니다.'),
                  ('앞 방법의 한계', '전수 비교는 정확하지만 비교 횟수 = 전체 건수입니다. 건수가 10배면 시간도 10배입니다.'),
                  ('해법', '미리 점들을 서랍(군집) 몇십~몇천 개에 나눠 담습니다(IVF). 질문이 오면 가까운 서랍 몇 개만 열어 그 안에서만 잽니다. 열 서랍 수(nprobe)가 속도와 정확도를 바꿉니다.')],
                 '옷장 서랍에 "겨울옷", "운동복"을 나눠 넣어 두면, 털장갑을 찾을 때 모든 서랍을 열지 않습니다. 가끔 엉뚱한 서랍에 들어간 장갑은 놓칠 수 있습니다.'),
             mathbox('서랍을 쓰면 비교가 몇 번으로 줄어요?', '나눗셈과 어림 — 평균적으로 한 서랍에 몇 개가 들었나',
                     '비교 횟수 ≈ 서랍 수 L + (전체 N ÷ L) × 연 서랍 수',
                     [('N', '엔', '전체 점 수'), ('L', '엘', '서랍(군집) 수. 서랍 중심과 먼저 거리를 잼'), ('nprobe', '엔프로브', '열어 볼 서랍 수')],
                     'N = 5,000, L = 64, nprobe = 4: 64 + (5,000 ÷ 64) × 4 ≈ 64 + 78 × 4 ≈ <b>376번</b>. 이 페이지에서 질문 60개로 잰 평균은 <b>%s번</b>, 전수 비교는 5,000번입니다.' % num(i4['cmp']),
                     '5,000번이 400번 정도로! 그런데 정답을 몇 개나 놓치는지도 봐야겠죠?'))
    s += talk([('asst', 'e15', '모아, 서랍을 하나만 열면 가장 가까운 10개를 다 찾을까?'),
               ('moa', 'think', '질문이 서랍 가장자리에 있으면… 옆 서랍에 있는 점을 놓칠 것 같아요.'),
               ('robo', 'happy', '서랍 하나면 제일 빠르잖아. 그걸로 가자!'),
               ('fly', 'point', '지도에서 서랍 경계 근처를 눌러 봐. 그리고 nprobe를 1에서 4로 올리면서 재현율을 봐.'),
               ('asst', 'report', '서랍 1개면 재현율 %s, 4개면 %s예요. 비교는 %s번 → %s번이고요.' % (pct(IVF[1]['recall']), pct(i4['recall']), num(IVF[1]['cmp']), num(i4['cmp'])))])
    s += panel('p32', '실험 · 서랍 색인(IVF) — 몇 개를 열까', '설명용 점 5,000개 · 페이지가 직접 계산',
               '<div class="ctrl"><div class="group"><span class="glabel">연 서랍 수 nprobe</span><input type="range" id="np32" min="1" max="16" value="1" aria-label="nprobe"><span class="val" id="npv32"></span></div>'
               '<div class="group"><button class="bt" id="rq32">다른 질문 자리</button></div></div>'
               + canvas('cv32', 380, '점 5,000개와 서랍 64개. 질문 자리와 연 서랍, 찾은 점이 표시된 지도') +
               '<p class="small muted">지도를 누르면 그 자리가 질문이 됩니다. 진하게 칠한 점 = 연 서랍에 든 점, 초록 고리 = 진짜 가장 가까운 10개, 파란 점 = 서랍 색인이 찾은 10개.</p>'
               '<section class="kpis" id="k32" aria-label="숫자 요약"></section><div class="insight" id="in32" aria-live="polite"></div>', real=True)
    s += explain(['서랍 중심 64개와 먼저 거리를 재고, 가까운 서랍 nprobe개만 열어 그 안의 점과 잽니다.',
                  '질문 60개 평균: ' + ', '.join('nprobe %d → 재현율 %s, 비교 %s번' % (x['nprobe'], pct(x['recall']), num(x['cmp'])) for x in R['ivf']) + '. 전수 비교는 재현율 100%%, 비교 5,000번입니다.',
                  '서랍을 더 열수록 정확해지고 느려집니다. 서비스는 "재현율 95%에서 가장 빠른 설정"처럼 목표를 정하고 고릅니다.',
                  '<b>고차원에서도 그럴까?</b> 2차원 그림만 믿지 않으려고, 교육용 24차원 리뷰 좌표 %d개를 서랍 16개로 나눠 같은 실험을 했습니다(질문 %d개, 같은 거리는 정답으로 침): ' % (R['ivf24']['n'], R['ivf24']['q']) + ', '.join('nprobe %d → 재현율 %s, 비교 %d번' % (x['nprobe'], pct(x['recall']), x['cmp']) for x in R['ivf24']['rows']) + '. 차원이 높으면 질문 근처에 서랍 경계가 더 많아, 같은 재현율에 더 많은 서랍을 열어야 합니다.'],
                 '서랍은 데이터를 넣을 때 한 번 나눠 둡니다. 나중에 들어온 데이터의 분포가 크게 바뀌면 서랍을 다시 나눠야(재학습) 합니다.')
    s += codefold([('index = faiss.IndexIVFFlat(quantizer, d, nlist=64)', 'Meta의 FAISS 라이브러리로 서랍 64개짜리 IVF 색인 만들기'),
                   ('index.nprobe = 4', '질문할 때 열어 볼 서랍 수')])
    s += wrapup('근사 검색은 "얼마나 덜 정확한가"를 재현율로 재고, 속도와 맞바꿉니다. 서랍 수와 연 서랍 수가 그 손잡이입니다.')
    s += quiz('q32')
    b += step('s2', '3-2', '모두와 재지 않기 — 서랍 색인 (IVF)', ['방법: 근사 최근접 이웃 · IVF', '일상: 옷장 서랍'], s)

    # ── 3-3 HNSW
    s = say('doc', 'think', '서랍 말고 다른 방법도 있습니다. 처음 가는 동네에서 사람들에게 "여기서 더 가까운 곳은요?"라고 물으며 찾아가는 방법이죠.')
    s += duo(why([('문제 상황', '서랍 경계 근처의 질문은 서랍을 여러 개 열어야 해서 느려집니다.'),
                  ('앞 방법의 한계', 'IVF는 서랍을 미리 나눠야 하고, 경계에서 정답을 놓치기 쉽습니다.'),
                  ('해법', '점마다 가까운 이웃 몇 개와 길(연결선)을 이어 둡니다. 위층에는 띄엄띄엄한 고속도로, 아래층에는 촘촘한 골목길을 둡니다(HNSW). 질문이 오면 위층에서 크게 다가간 뒤, 아래층에서 더 가까운 이웃으로 옮겨 가며 찾습니다.')],
                 '서울에서 부산의 한 가게를 찾을 때, 고속도로(위층)로 부산까지 간 다음 골목길(아래층)에서 길을 물어 찾아가는 것과 같습니다.'),
             pair('일상으로 치면', '"여섯 다리만 건너면 모두 아는 사이"라는 작은 세상 이야기처럼, 길 몇 번만 건너면 먼 곳에도 닿습니다.',
                  '색인에서는', '이 페이지의 그래프는 점마다 가까운 이웃 7개 + 먼 지름길 1개를 잇고, 점 4%%를 위층으로 올립니다. ef는 아래층에서 "후보를 몇 개까지 들고 다닐지"입니다.'))
    s += talk([('asst', 'e20', '시아, 위층 고속도로에서 출발하면… 음, 왜 더 빨라지는 걸까?'),
               ('sia', 'explain', '위층에서 몇 번만 건너도 질문 근처까지 가니까요. 아래층에선 근처만 둘러보면 돼요.'),
               ('robo', 'wow', '그럼 서랍보다 무조건 그래프지!'),
               ('fly', 'point', '"무조건"은 없어. 길을 저장하는 메모리도 들어. 아래에서 ef를 10과 80으로 바꿔 비교 횟수와 재현율을 봐.'),
               ('asst', 'report', 'ef 10이면 비교 %s번에 재현율 %s, ef 40이면 %s번에 %s예요.' % (num(GR[10]['cmp']), pct(GR[10]['recall']), num(GR[40]['cmp']), pct(GR[40]['recall'])))])
    s += panel('p33', '실험 · 길 찾기 그래프(HNSW) — 어떤 길로 다가가나', '설명용 점 5,000개 · 페이지가 직접 계산',
               '<div class="ctrl"><div class="group"><span class="glabel">후보 수 ef</span><input type="range" id="ef33" min="10" max="80" step="10" value="20" aria-label="ef"><span class="val" id="efv33"></span></div>'
               '<div class="group"><button class="bt" id="pl33">길 따라가기 다시 보기</button><button class="bt" id="rq33">다른 질문 자리</button></div></div>'
               + canvas('cv33', 380, '점 5,000개 위에서 위층 길(주황)과 아래층 길(파랑)로 질문에 다가가는 경로') +
               '<p class="small muted">지도를 누르면 그 자리가 질문입니다. 주황 굵은 선 = 위층 고속도로로 건넌 길, 파란 점 = 아래층에서 거리를 잰 점, 초록 고리 = 진짜 가장 가까운 10개.</p>'
               '<section class="kpis" id="k33" aria-label="숫자 요약"></section><div class="insight" id="in33" aria-live="polite"></div>', real=True)
    s += explain(['위층(점 %d개)에서 질문에 더 가까운 이웃이 없을 때까지 건너가고, 그 자리에서 아래층으로 내려가 ef개의 후보를 들고 이웃을 넓혀 갑니다.' % R['graph_top'],
                  '질문 60개 평균: ' + ', '.join('ef %d → 재현율 %s, 비교 %s번' % (x['ef'], pct(x['recall']), num(x['cmp'])) for x in R['graph']) + '.',
                  '이 점 구름에서는 그래프가 서랍보다 적은 비교로 높은 재현율에 닿습니다. HNSW가 여러 벡터 DB와 pgvector에서 널리 쓰이는 이유입니다.'],
                 '그래프는 연결선을 저장하느라 메모리를 많이 쓰고, 점을 지우거나 대량으로 넣을 때 다시 잇는 비용이 듭니다. 실제 HNSW는 층이 더 많고 이웃 고르는 규칙도 더 정교합니다(여기서는 두 층으로 줄였습니다).')
    s += codefold([('CREATE INDEX ON review USING hnsw (embedding vector_cosine_ops) WITH (m = 16, ef_construction = 64);', 'pgvector에서 HNSW 색인 만들기 (m = 점마다 이을 이웃 수)'),
                   ('SET hnsw.ef_search = 40;', '질문할 때 들고 다닐 후보 수(ef)')])
    s += wrapup('그래프 색인은 "길을 물어 가며 다가가기"입니다. ef를 키우면 정확해지고 느려집니다. 서랍이든 그래프든, 손잡이는 늘 속도와 재현율의 맞바꿈입니다.')
    s += quiz('q33')
    b += step('s3', '3-3', '길 따라 찾기 — 그래프 색인 (HNSW)', ['방법: HNSW · 작은 세상 그래프', '일상: 고속도로 → 골목길'], s)

    # ── 3-4 메타데이터 필터
    s = say('doc', 'think', '마케팅팀이 다시 왔습니다. "재밌다는 리뷰인데요, 별점 4점 이상이고 코미디 영화 것만 주세요." 좌표만으로 될까요?')
    s += duo(why([('문제 상황', '뜻(좌표)과 표 조건(장르·별점·날짜)을 함께 만족하는 결과가 필요합니다.'),
                  ('앞 방법의 한계', '좌표는 장르·별점을 모르고, 2장의 비꼬는 리뷰처럼 별점과 뜻이 엇갈리는 경우도 거르지 못합니다.'),
                  ('해법', '레코드에 함께 넣은 메타데이터로 거릅니다. ① 먼저 거르기(조건에 맞는 것 중에서 가까운 k개) ② 찾은 뒤 거르기(가까운 k개를 찾고 조건으로 걸러냄).')],
                 '맛집 앱에서 "분위기 좋은 곳"(뜻)과 "지금 영업 중·5천 원 이하"(조건)를 함께 거는 것과 같습니다.'),
             pair('일상으로 치면', '"비슷한 옷 추천" 뒤에 "내 치수·재고 있음"을 거는 쇼핑몰 필터입니다.',
                  '벡터 DB에서는', '"찾은 뒤 거르기"는 간단하지만 조건이 까다로우면 k개를 못 채웁니다. "먼저 거르기"는 k개를 채우지만 색인을 조건과 함께 쓰는 기술이 필요합니다.'))
    s += talk([('asst', 'e15', '모아, 재밌다는 리뷰 5개를 먼저 찾고 나서 "코미디·4점 이상"으로 거르면 몇 개가 남을까?'),
               ('moa', 'ok', '5개 중 코미디가 있으면 남겠죠… 없으면 0개?'),
               ('robo', 'coin', '그럼 처음부터 50개 찾고 거르면 되지!'),
               ('fly', 'point', '50개도 모자랄 수 있어. 아래에서 "찾은 뒤 거르기"와 "먼저 거르기"를 바꿔 가며 돌려준 개수를 세어 봐.'),
               ('asst', 'report', '찾은 뒤 거르기는 5개를 다 못 채울 때가 있어요. 먼저 거르기는 늘 5개를 채워요.')])
    s += panel('p34', '실험 · 좌표 검색 + 메타데이터 필터', '가상 데이터 · 페이지가 직접 계산',
               '<div class="ctrl"><div class="group"><span class="glabel">질문</span><select class="sel" id="q34"></select></div>'
               '<div class="group"><span class="glabel">장르</span><select class="sel" id="g34"><option value="">전체</option></select></div>'
               '<div class="group"><span class="glabel">별점</span><input type="range" id="s34" min="1" max="5" value="4" aria-label="최소 별점"><span class="val" id="sv34"></span></div></div>'
               '<div class="ctrl"><div class="group"><span class="glabel">거르는 순서</span><button class="bt" data-m="post" aria-pressed="true">찾은 뒤 거르기</button><button class="bt" data-m="pre" aria-pressed="false">먼저 거르기</button></div>'
               '<div class="group"><span class="glabel">먼저 찾을 수</span><input type="range" id="c34" min="5" max="50" step="5" value="5" aria-label="먼저 찾을 수"><span class="val" id="cv34"></span></div></div>'
               '<div class="sqlbox" id="sql34"></div><section class="kpis" id="k34" aria-label="숫자 요약"></section><ul class="res" id="rs34"></ul><div class="insight" id="in34" aria-live="polite"></div>', real=True)
    s += explain(['메타데이터는 좌표가 모르는 사실(장르, 별점, 날짜, 권한)을 담습니다. 검색 결과를 믿을 만하게 만드는 일등 공신입니다.',
                  '찾은 뒤 거르기는 조건이 까다로울수록(희귀한 장르 + 높은 별점) k개를 못 채웁니다. 먼저 찾을 수를 늘리면 채우지만 그만큼 느려집니다.',
                  '먼저 거르기는 조건에 맞는 점들 사이에서만 찾습니다. 조건이 아주 까다로우면 오히려 전수 비교가 빠를 수도 있어, 벡터 DB마다 내부 전략이 다릅니다.'],
                 '별점이 높아도 뜻이 엇갈린 리뷰(비꼼)는 여전히 남을 수 있습니다. 필터는 "조건"을 걸 뿐, 뜻을 이해하지는 않습니다.')
    s += aicheck('"결과가 2개뿐인데요?"',
                 '<p>주판봇이 "재밌는 영화 리뷰 + 공포 + 5점"으로 찾은 뒤 거르기를 돌렸더니 결과가 0~2개뿐입니다. 주판봇의 결론: "공포 영화 중 재밌다는 5점 리뷰는 거의 없다!"</p>'
                 '<p><b>확인 질문</b> 이 결론을 믿어도 될까요? 무엇을 바꿔 확인하면 될까요?</p>'
                 '<details><summary>생각해 본 뒤 열어 보기</summary><p>믿기 이릅니다. 찾은 뒤 거르기는 "먼저 찾은 5개" 안에서만 거릅니다. 공포 리뷰가 그 5개에 없었을 뿐일 수 있습니다. '
                 '"먼저 거르기"로 바꾸거나 "먼저 찾을 수"를 늘려 다시 세어 보면 됩니다. 결과가 적다는 것과 데이터가 적다는 것은 다릅니다.</p></details>')
    s += codefold([("collection.query(query_embeddings=[q], n_results=5, where={'$and': [{'genre': '코미디'}, {'stars': {'$gte': 4}}]})", '벡터 DB에서 메타데이터 조건을 함께 거는 모양'),
                   ("SELECT text FROM review WHERE genre = '코미디' AND stars >= 4 ORDER BY embedding <=> :q LIMIT 5;", 'pgvector: SQL 조건 + 좌표 거리 정렬을 한 문장에')])
    s += wrapup('좌표는 뜻을, 메타데이터는 사실을 맡습니다. 둘을 함께 걸 때는 "거르는 순서" 때문에 결과 수가 달라질 수 있다는 점을 기억하세요.')
    s += quiz('q34')
    b += step('s4', '3-4', '좌표 + 표 조건 — 메타데이터 필터', ['방법: 메타데이터 필터 · 먼저/나중 거르기', '일상: 쇼핑몰 필터'], s)

    # ── 3-5 관계형 DB와 함께
    s = say('doc', 'think', '그럼 관계형 DB는 이제 버리나요? 벡터 DB를 한 장에 정리한 인포그래픽들도 대개 같은 답을 냅니다(목차의 "그림 아홉 개" 대응표 8번). "둘을 함께 쓴다."')
    s += duo(why([('문제 상황', '서비스에는 주문·결제(한 건도 틀리면 안 됨)와 의미 검색(대략 가까우면 됨)이 함께 있습니다.'),
                  ('앞 방법의 한계', '한쪽만 쓰면 다른 쪽 일을 억지로 합니다. 벡터 DB로 결제를 관리하거나, 관계형 DB에서 모든 행과 거리를 재는 식입니다.'),
                  ('해법', '정형 데이터와 트랜잭션은 관계형 DB가, 의미 검색은 벡터 색인이 맡습니다. 하나의 PostgreSQL에 pgvector 확장을 붙이거나, 전용 벡터 DB를 옆에 두고 번호로 잇습니다.')],
                 '돈이 오가는 기록은 금고(관계형 DB)에, 분위기로 찾는 사진첩은 앨범(벡터 DB)에. 둘은 같은 번호표로 연결됩니다.'),
             pair('관계형 DB', '정확한 일치·범위·집계, 트랜잭션(ACID). 예: PostgreSQL, MySQL, SQLite, SQL Server. 데이터베이스 설계 강좌 전부가 여기에 해당합니다.',
                  '벡터 DB', '가까운 좌표 찾기(ANN), 메타데이터 필터. 예: Pinecone, Milvus, Weaviate, Qdrant, Chroma. 관계형 DB에 벡터 검색을 더하는 확장(pgvector)도 널리 쓰입니다.'))
    s += talk([('asst', 'e15', '시아, 결제 기록은 어디에 저장해야 할까? 벡터 DB? 관계형 DB?'),
               ('sia', 'firm', '관계형 DB요! 한 건도 틀리면 안 되니까 트랜잭션이 필요해요.'),
               ('robo', 'coin', '요즘은 다 벡터 DB 아니야? 하나로 통일하자!'),
               ('fly', 'point', '아래 여덟 가지 장면을 하나씩 골라 봐. 어디에 둘지, 둘 다인지.'),
               ('asst', 'report', '대부분 "둘 다"예요. 뜻으로 찾고, 사실은 표에서 확인해요.')])
    s += panel('p35', '실험 · 어디에 저장할까 — 장면 여덟 개', '설명용 판별 연습',
               '<div id="sc35"></div><section class="kpis" id="k35" aria-label="맞힌 수"></section>', real=True)
    s += explain(['관계형 DB와 벡터 DB는 경쟁자라기보다 역할 분담입니다. 질문이 "정확히 이것"이면 표, "이것과 비슷한 것"이면 벡터입니다.',
                  '작게 시작할 때는 이미 쓰는 PostgreSQL에 pgvector를 붙이는 방법이 단순합니다. 수억 건·초당 많은 질문이 필요하면 전용 벡터 DB를 검토합니다.',
                  '어느 쪽이든 원문과 메타데이터의 "진짜 원본"은 한 곳에 두고, 다른 쪽은 번호로 가리키게 해야 기록이 엇갈리지 않습니다.'],
                 '제품별 기능(필터 방식, 트랜잭션 지원, 가격)은 빠르게 바뀝니다. 도입할 때는 그 시점의 공식 문서로 확인해야 합니다.')
    s += codefold([('CREATE EXTENSION vector;', 'PostgreSQL에 pgvector 확장을 켭니다'),
                   ('SELECT r.text, m.title FROM review r JOIN movie m ON r.movie_id = m.id ORDER BY r.embedding <=> :q LIMIT 5;', '조인(관계형)과 좌표 거리 정렬(벡터)을 한 문장에서')])
    s += wrapup('관계형 DB는 사실을, 벡터 DB는 뜻을 맡습니다. 많은 실제 시스템은 둘을 함께 씁니다. 다음 장에서는 이 창고를 LLM에게 연결합니다.')
    s += quiz('q35')
    b += step('s5', '3-5', '표와 함께 쓰기 — 관계형 DB와 벡터 DB의 역할 나누기', ['방법: 역할 분담 · pgvector', '일상: 금고와 앨범'], s)

    b += duel('d3', '점 5,000개에서 가까운 10개 찾기 — 전수 비교 vs 서랍 색인(nprobe 4)', '전수 비교 (모두와 잰다, 늘 정확)', '서랍 색인 IVF (서랍 64개 중 4개만 연다)',
              '"정확한 게 최고야. 근사는 언젠가 사고를 쳐."', '"빠른 게 최고지! 조금 놓쳐도 대세엔 지장 없어."',
              '질문 하나당 비교 횟수 (적을수록 좋음, 단 재현율 95% 이상일 때만 인정)')

    b += section('sum', '정리 — 벡터 창고의 손잡이',
                 '<div class="tw"><table class="tb"><tr><th>손잡이</th><th>올리면</th><th>내리면</th></tr>'
                 '<tr><td>차원 수</td><td>뜻을 더 세밀히 담음, 용량·시간 증가</td><td>가볍고 빠름, 뜻이 뭉개질 수 있음</td></tr>'
                 '<tr><td>압축(양자화)</td><td>용량 크게 감소</td><td>거리 계산이 정확</td></tr>'
                 '<tr><td>IVF의 nprobe</td><td>재현율 증가, 느려짐</td><td>빠름, 경계에서 놓침</td></tr>'
                 '<tr><td>HNSW의 ef</td><td>재현율 증가, 느려짐</td><td>빠름, 가끔 엉뚱한 동네에서 멈춤</td></tr>'
                 '<tr><td>먼저 찾을 수 (찾은 뒤 거르기)</td><td>k개를 채우기 쉬움, 느려짐</td><td>빠름, 결과가 모자랄 수 있음</td></tr></table></div>'
                 + bridge('field', '현장에 옮기면', '벡터 DB를 고를 때는 "우리 데이터·우리 질문"으로 재현율과 응답 시간을 직접 재 봅니다. 제품 소개 자료의 숫자는 다른 데이터로 잰 값입니다.',
                          '이 장의 점 5,000개는 2차원 설명용입니다. 실제 좌표는 수백 차원이라 서랍·그래프의 성질이 2차원 그림과 다를 수 있습니다.'))

    b += outro([('doc', 'front', '오늘 세 줄 정리. ① 벡터 DB의 레코드는 좌표·메타데이터·원문의 묶음이다. ② 근사 색인(IVF, HNSW)은 재현율을 조금 내주고 속도를 크게 얻는다. ③ 사실은 표가, 뜻은 벡터가 맡고 둘을 함께 쓴다.'),
                ('robo', 'happy', '드디어 이겼다! 빠른 게 최고라니까. …재현율도 확인했으니까 하는 말이야.'),
                ('fly', 'coffee', '이번엔 인정. 대신 재현율 재는 습관은 계속 가져가.'),
                ('sia', 'proud', '서랍은 nprobe, 그래프는 ef. 손잡이 표 정리했어요.'),
                ('moa', 'report', 'DB 설계 노트에 "pgvector로 함께 쓰기" 그림을 그렸어요.'),
                ('asst', 'e01', '다음은 제일 기대되는 4장, LLM과 RAG예요!')],
               '창고 선반 사이에서 하루와 인턴들이 서랍과 길 지도를 들고 서 있는 장면',
               crowd('"주판봇 첫 승이다!" "하루 오늘 완전 선생님 같았어."', moods=('e04', 'e16', 'e01')))
    return b


GLOSS = {
    '벡터 DB': ['벡터 데이터베이스 (vector database)', '좌표(벡터)와 메타데이터를 저장하고, 가까운 좌표를 빨리 찾는 색인을 갖춘 데이터베이스.'],
    '메타데이터': ['메타데이터 (metadata)', '데이터에 대한 정보. 장르·별점·날짜·작성자·권한처럼 표로 다루는 사실.'],
    '색인': ['색인 (index)', '찾기를 빠르게 하려고 미리 만들어 둔 구조. 관계형 DB는 B-트리, 벡터 DB는 IVF·HNSW 등.'],
    '전수 비교': ['전수 비교 (brute force, flat)', '모든 점과 거리를 재는 방법. 늘 정확하지만 느립니다.'],
    '근사': ['근사 최근접 이웃 (ANN)', '가장 가까운 점을 "거의" 정확하게, 훨씬 빠르게 찾는 방법들.'],
    '재현율': ['재현율 (recall@k)', '진짜 가장 가까운 k개 중 색인이 찾아온 비율.'],
    '양자화': ['양자화 (quantization)', '좌표 숫자를 더 적은 바이트로 줄여 저장하는 압축. PQ가 대표적.'],
    'IVF': ['IVF (서랍 색인)', '점들을 군집(서랍)으로 나눠 두고, 가까운 서랍 몇 개만 열어 찾는 색인.'],
    'HNSW': ['HNSW (길 찾기 그래프)', '점마다 이웃과 길을 이어 두고, 위층(듬성)에서 아래층(촘촘)으로 내려가며 찾는 색인.'],
    'pgvector': ['pgvector', 'PostgreSQL에 벡터 열과 벡터 색인(IVF, HNSW)을 더하는 확장.'],
    'FAISS': ['FAISS', 'Meta가 공개한 대규모 벡터 검색 라이브러리.'],
    '트랜잭션': ['트랜잭션 (ACID)', '여러 작업을 모두 되거나 모두 안 되거나로 묶어 기록이 깨지지 않게 하는 성질.'],
}

QUIZ = {
    'q31': [{'q': '리뷰 100만 개 × 768차원 × 4바이트는 대략?', 'o': ['약 0.3GB', '약 3GB', '약 30GB'], 'a': 1,
             'why': '1,000,000 × 768 × 4 = 3,072,000,000바이트 ≈ 3.07GB.', 'hint': '768 × 4 = 3,072바이트가 한 건입니다.'},
            {'q': '벡터 DB 레코드에서 메타데이터의 역할은?', 'o': ['뜻을 계산한다', '장르·별점 같은 사실로 결과를 거른다', '좌표를 압축한다'], 'a': 1,
             'why': '메타데이터는 좌표가 모르는 사실을 담아 거르기에 씁니다.', 'hint': '"코미디만, 4점 이상만"을 떠올려 보세요.'}],
    'q32': [{'q': '서랍 색인(IVF)에서 nprobe를 늘리면?', 'o': ['빨라지고 정확해진다', '느려지고 정확해진다', '용량이 줄어든다'], 'a': 1,
             'why': '서랍을 더 열수록 비교가 늘어 느려지고, 놓치는 정답이 줄어듭니다.', 'hint': '서랍을 많이 열면 무엇이 늘까요?'},
            {'q': 'N=5,000, 서랍 64개, nprobe 4일 때 비교 횟수 어림값은?', 'o': ['약 64번', '약 376번', '약 5,000번'], 'a': 1,
             'why': '64 + (5,000 ÷ 64) × 4 ≈ 64 + 312 = 376.', 'hint': '서랍 중심과 먼저 재고, 연 서랍 안의 점과 잽니다.'}],
    'q33': [{'q': 'HNSW 위층(고속도로)의 역할은?', 'o': ['정답을 확정한다', '먼 거리를 몇 번 만에 건너 질문 근처로 데려간다', '메타데이터를 거른다'], 'a': 1,
             'why': '위층은 듬성듬성한 지름길이라 몇 번만 건너도 질문 근처에 닿습니다.', 'hint': '서울→부산 고속도로를 떠올려 보세요.'},
            {'q': 'HNSW의 약점으로 맞는 것은?', 'o': ['연결선 저장에 메모리가 많이 든다', '근사가 아니라 늘 전수 비교한다', '코사인을 못 쓴다'], 'a': 0,
             'why': '점마다 이웃 연결을 저장하므로 메모리가 들고, 지우기·대량 추가 때 다시 잇는 비용이 있습니다.', 'hint': '길을 저장하는 데도 공간이 듭니다.'}],
    'q34': [{'q': '"찾은 뒤 거르기"에서 결과가 k개보다 적게 나오는 이유는?', 'o': ['데이터에 조건 맞는 것이 없어서만', '먼저 찾은 k개 중에 조건에 맞는 것이 적어서', '코사인이 틀려서'], 'a': 1,
             'why': '먼저 찾은 몇 개 안에서만 거르기 때문에, 조건이 까다로우면 모자랍니다.', 'hint': '거르는 대상이 전체인가요, 먼저 찾은 몇 개인가요?'},
            {'q': '비꼬는 리뷰(별점 1점, "감동이다 ^^")를 걸러 내는 데 도움이 되는 것은?', 'o': ['별점 메타데이터 조건', '차원 늘리기', 'nprobe 늘리기'], 'a': 0,
             'why': '별점 같은 사실 정보로 함께 거르면 뜻과 별점이 엇갈린 리뷰를 걸러 낼 수 있습니다.', 'hint': '표에 남아 있는 숫자를 쓰세요.'}],
    'q35': [{'q': '결제 기록 저장에 알맞은 곳은?', 'o': ['벡터 DB', '관계형 DB', '어디든 같다'], 'a': 1,
             'why': '결제는 한 건도 틀리면 안 되어 트랜잭션(ACID)이 필요합니다. 관계형 DB의 강점입니다.', 'hint': '트랜잭션이 필요한가요?'},
            {'q': 'pgvector는 무엇인가?', 'o': ['전용 벡터 DB 제품 이름', 'PostgreSQL에 벡터 열과 벡터 색인을 더하는 확장', '임베딩 모델'], 'a': 1,
             'why': '이미 쓰는 PostgreSQL에서 벡터 검색을 함께 할 수 있게 해 주는 확장입니다.', 'hint': 'pg = PostgreSQL'}],
}

JS = r'''
var D=VL.load(),RV=D.reviews;
/* 3-1 */
(function(){var idx=0;
  function rec(){var r=RV[idx%RV.length];$('#rec31').textContent='{\n  "id": '+r.id+',\n  "vector": ['+r.vec.map(function(x){return x.toFixed(2)}).join(', ')+'],   ← 24차원 좌표\n  "metadata": {"movie": "'+r.title+'", "genre": "'+r.genre+'", "stars": '+r.stars+', "date": "'+r.date+'"},\n  "document": "'+r.text+'"\n}';}
  function calc(){var n=Math.pow(10,+$('#n31').value),d=+$('#d31').value,qb=+($('#p31 [data-q][aria-pressed=true]').dataset.q),gb=n*d*qb/1e9;
    $('#nv31').textContent=n>=1e8?VL.fmt(n/1e8,n%1e8?1:0)+'억 건':n>=1e4?VL.fmt(n/1e4,0)+'만 건':VL.fmt(n)+'건';
    VL.kpis($('#k31'),[[gb<1?VL.fmt(gb*1000,0)+' MB':VL.fmt(gb,gb<10?2:0)+' GB','좌표만 저장할 때 용량','g'],[VL.fmt(d*qb)+' 바이트','한 건의 좌표 크기','i'],[VL.fmt(n*d)+'번','질문 하나를 전수 비교할 때 곱셈 수','r'],[qb===1?'약 1/4':'기준','압축 효과','a']]);
    $('#in31').innerHTML='<p class="'+(gb>64?'r':'g')+'">'+(gb>64?'좌표만 '+VL.fmt(gb,0)+' GB입니다. 보통 서버 한 대의 메모리에 다 올리기 어렵습니다. 압축하거나 여러 대에 나눠 담아야 합니다.':'이 정도면 서버 한 대 메모리에 올릴 만합니다. 건수나 차원을 올려 보세요.')+'</p>'+(qb===1?'<p class="a">1바이트 압축은 용량을 약 1/4로 줄입니다. 대신 거리가 조금 부정확해져, 다시 정밀하게 재는 단계(재정렬)를 덧붙이곤 합니다.</p>':'');}
  $('#nx31').addEventListener('click',function(){idx+=37;rec();});$('#n31').addEventListener('input',calc);$('#d31').addEventListener('change',calc);
  $$('#p31 [data-q]').forEach(function(b){b.addEventListener('click',function(){$$('#p31 [data-q]').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});calc();})});rec();calc();
})();
/* 3-2, 3-3 공용 점 구름 */
var PTS=VL.cloud(5000,11,9),IVFX=VL.kmeans(PTS,64,3,12),GRX=VL.graph(PTS,8,5),COLS=['#1e55c8','#13733a','#c42a6e','#a35c00','#9b3fb5','#0b7a86','#5b6874','#8f5a2e'];
function mapAxes(g,f){var L=10,T=10,S=Math.min(f.W-20,f.H-20),ox=(f.W-S)/2;g.fillStyle='#fff';g.fillRect(0,0,f.W,f.H);g.strokeStyle='#e6ebf1';g.strokeRect(ox,T,S,S);return {sx:function(v){return ox+v*S},sy:function(v){return T+(1-v)*S},inv:function(x,y){return [(x-ox)/S,1-(y-T)/S]}};}
(function(){var cv=$('#cv32'),q=[.52,.47],r=VL.rng(4),A;
  /* 처음 질문 자리: 서랍 1개로는 놓치는 경계 자리를 고른다 */
  for(var tr=0;tr<80;tr++){var p0=PTS[Math.floor(r()*PTS.length)],c0=[p0[0]+.004,p0[1]+.004];if(VL.recall(VL.ivfSearch(PTS,IVFX,c0,10,1).ids,VL.exact(PTS,c0,10))<=.6){q=c0;break;}}
  function draw(){var np=+$('#np32').value;$('#npv32').textContent=np+'개 / 64개';var f=fit(cv),g=f.c;A=mapAxes(g,f);var s=VL.ivfSearch(PTS,IVFX,q,10,np),t=VL.exact(PTS,q,10),pr={};s.probed.forEach(function(c){pr[c]=1});
    for(var i=0;i<PTS.length;i++){var c=IVFX.lab[i];VL.dot2(g,A.sx(PTS[i][0]),A.sy(PTS[i][1]),pr[c]?2.2:1.6,COLS[c%COLS.length],pr[c]?.7:.12);}
    IVFX.C.forEach(function(c,i){g.fillStyle=pr[i]?'#16212b':'#9aa6b2';g.fillRect(A.sx(c[0])-3,A.sy(c[1])-3,6,6);});
    t.forEach(function(i){g.strokeStyle='#13733a';g.lineWidth=2;g.beginPath();g.arc(A.sx(PTS[i][0]),A.sy(PTS[i][1]),7,0,6.2832);g.stroke();});g.lineWidth=1;
    s.ids.forEach(function(i){VL.dot2(g,A.sx(PTS[i][0]),A.sy(PTS[i][1]),3.6,'#1e55c8',1);});
    g.fillStyle='#c9302c';g.font='700 22px sans-serif';g.fillText('★',A.sx(q[0])-8,A.sy(q[1])+8);stamp(g,f.W,'설명용 2차원 점 5,000개');
    var rc=VL.recall(s.ids,t);VL.kpis($('#k32'),[[VL.fmt(s.cmp)+'번','이번 질문의 비교 횟수 (전수 5,000번)','i'],[VL.pct(rc,0),'재현율 (진짜 10개 중 찾은 비율)',rc>=.95?'g':'r'],[(5000/s.cmp).toFixed(1)+'배','전수 비교보다 빠른 정도','a'],[np+'개','연 서랍','m']]);
    $('#in32').innerHTML='<p class="'+(rc>=.95?'g':'r')+'">'+(rc>=.95?'진짜 가장 가까운 10개를 '+VL.pct(rc,0)+' 찾았습니다. 비교는 '+VL.fmt(s.cmp)+'번.':'초록 고리 중 파란 점이 없는 것이 놓친 정답입니다. 옆 서랍에 들어 있었습니다. nprobe를 올려 보세요.')+'</p>';}
  cv.addEventListener('click',function(e){var b=cv.getBoundingClientRect();q=A.inv(e.clientX-b.left,e.clientY-b.top);q=[Math.min(.99,Math.max(.01,q[0])),Math.min(.99,Math.max(.01,q[1]))];draw();});
  $('#np32').addEventListener('input',draw);$('#rq32').addEventListener('click',function(){var p=PTS[Math.floor(r()*PTS.length)];q=[p[0]+.01,p[1]-.01];draw();});
  Loop.add(cv,function(dt){if(dt===0)draw();});
})();
(function(){var cv=$('#cv33'),q=[.3,.7],r=VL.rng(8),A,anim=0,res=null;
  function search(){var ef=+$('#ef33').value;$('#efv33').textContent=ef;res=VL.graphSearch(PTS,GRX,q,10,ef);res.t=VL.exact(PTS,q,10);anim=window.REDUCED?1e9:0;}
  function draw(){var f=fit(cv),g=f.c;A=mapAxes(g,f);for(var i=0;i<PTS.length;i+=1)VL.dot2(g,A.sx(PTS[i][0]),A.sy(PTS[i][1]),1.4,'#8a96a3',.25);
    g.strokeStyle='rgba(163,92,0,.18)';GRX.topIds.forEach(function(i){(GRX.top[i]||[]).forEach(function(j){g.beginPath();g.moveTo(A.sx(PTS[i][0]),A.sy(PTS[i][1]));g.lineTo(A.sx(PTS[j][0]),A.sy(PTS[j][1]));g.stroke();})});
    if(!res)return;var n=Math.floor(anim),top=res.top,low=res.path.slice(top.length);
    g.strokeStyle='#a35c00';g.lineWidth=3;g.beginPath();top.slice(0,Math.min(top.length,n+1)).forEach(function(i,k){var x=A.sx(PTS[i][0]),y=A.sy(PTS[i][1]);k?g.lineTo(x,y):g.moveTo(x,y);});g.stroke();g.lineWidth=1;
    low.slice(0,Math.max(0,n-top.length)*3).forEach(function(i){VL.dot2(g,A.sx(PTS[i][0]),A.sy(PTS[i][1]),2.6,'#1e55c8',.8);});
    res.t.forEach(function(i){g.strokeStyle='#13733a';g.lineWidth=2;g.beginPath();g.arc(A.sx(PTS[i][0]),A.sy(PTS[i][1]),7,0,6.2832);g.stroke();});g.lineWidth=1;
    g.fillStyle='#c9302c';g.font='700 22px sans-serif';g.fillText('★',A.sx(q[0])-8,A.sy(q[1])+8);var e=PTS[GRX.entry];g.fillStyle='#a35c00';g.fillText('◆',A.sx(e[0])-7,A.sy(e[1])+7);stamp(g,f.W,'설명용 2차원 · 두 층 그래프');
    var rc=VL.recall(res.ids,res.t);VL.kpis($('#k33'),[[VL.fmt(res.cmp)+'번','비교 횟수 (전수 5,000번)','i'],[VL.pct(rc,0),'재현율',rc>=.95?'g':'r'],[(top.length-1)+'번','위층에서 건넌 횟수','a'],[(5000/res.cmp).toFixed(1)+'배','전수보다 빠른 정도','m']]);
    $('#in33').innerHTML='<p class="'+(rc>=.95?'g':'r')+'">◆에서 출발해 위층 길(주황)로 '+(top.length-1)+'번 건넌 뒤, 아래층에서 '+VL.fmt(res.cmp)+'번 재서 '+VL.pct(rc,0)+'를 찾았습니다.'+(rc<.95?' ef를 올려 보세요.':'')+'</p>';}
  cv.addEventListener('click',function(e){var b=cv.getBoundingClientRect();q=A.inv(e.clientX-b.left,e.clientY-b.top);search();});
  $('#ef33').addEventListener('input',function(){search();});$('#pl33').addEventListener('click',function(){anim=0;});$('#rq33').addEventListener('click',function(){var p=PTS[Math.floor(r()*PTS.length)];q=[p[0],p[1]+.01];search();});
  search();Loop.add(cv,function(dt,force){if(res&&anim<res.top.length+40){anim+=dt*6;draw();}else if(dt===0||force)draw();});
})();
/* 3-4 */
(function(){var Q=D.searchq,mode='post';$('#q34').innerHTML=Q.map(function(q,i){return '<option value="'+i+'">'+q.q+'</option>'}).join('');
  var G=[];D.movies.forEach(function(m){if(G.indexOf(m.genre)<0)G.push(m.genre)});$('#g34').innerHTML+=G.map(function(g){return '<option>'+g+'</option>'}).join('');
  function ok(r){var g=$('#g34').value,s=+$('#s34').value;return (!g||r.genre===g)&&r.stars>=s;}
  function run(){var q=Q[+$('#q34').value],qv=VL.embed(q.q).v,k=5,c=+$('#c34').value,g=$('#g34').value,st=+$('#s34').value;$('#sv34').textContent=st+'점 이상';$('#cv34').textContent=mode==='post'?c+'개':'(쓰지 않음)';
    var out,cmp;if(mode==='post'){out=VL.topk(RV,function(r){return VL.cos(qv,r.vec)},c).filter(function(x){return ok(x.it)}).slice(0,k);cmp=RV.length;}
    else{var pool=RV.filter(ok);out=VL.topk(pool,function(r){return VL.cos(qv,r.vec)},k);cmp=pool.length;}
    $('#sql34').innerHTML=mode==='post'?'<span class="k">찾기</span> 가까운 '+c+'개  →  <span class="k">거르기</span> '+(g?'장르 = '+g+' AND ':'')+'별점 ≥ '+st+'  →  앞 5개':'<span class="k">거르기</span> '+(g?'장르 = '+g+' AND ':'')+'별점 ≥ '+st+'  →  <span class="k">찾기</span> 그 안에서 가까운 5개';
    var good=out.filter(function(x){return VL.rel(x.it,q.asp)}).length;
    VL.kpis($('#k34'),[[out.length+' / 5','돌려준 결과',out.length<5?'r':'g'],[good+'개','그중 뜻도 맞는 것','i'],[RV.filter(ok).length+'개','조건에 맞는 리뷰 전체','a'],[VL.fmt(cmp)+'번','거리 잰 횟수','m']]);
    $('#rs34').innerHTML=out.map(function(x){var r=x.it;return '<li class="'+(VL.rel(r,q.asp)?'ok':'no')+'"><span class="sc">'+x.s.toFixed(2)+'</span><small>'+r.title+' · '+r.genre+' · '+VL.stars(r.stars)+'</small>'+VL.esc(r.text)+'</li>'}).join('')||'<li class="nt">결과가 없습니다.</li>';
    $('#in34').innerHTML='<p class="'+(out.length<5?'r':'g')+'">'+(out.length<5?'5개를 다 못 채웠습니다. 조건에 맞는 리뷰는 '+RV.filter(ok).length+'개나 있는데도요. "먼저 찾을 수"를 늘리거나 "먼저 거르기"로 바꿔 보세요.':'5개를 채웠습니다. 조건을 더 까다롭게(희귀한 장르 + 5점) 바꿔 보세요.')+'</p>';}
  ['#q34','#g34','#s34','#c34'].forEach(function(s){$(s).addEventListener('input',run);$(s).addEventListener('change',run);});
  $$('#p34 [data-m]').forEach(function(b){b.addEventListener('click',function(){mode=b.dataset.m;$$('#p34 [data-m]').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});run();})});run();
})();
/* 3-5 */
(function(){var S=[['고객이 낸 결제 금액과 결제 시각','rdb','한 건도 틀리면 안 되는 기록입니다. 트랜잭션이 필요합니다.'],
  ['"이 영화와 분위기가 비슷한 영화" 추천','vec','뜻이 가까운 것을 찾는 일이라 좌표 검색이 맡습니다.'],
  ['리뷰 원문 + 별점 + "재밌다는 리뷰" 검색','both','별점·날짜는 표가, 뜻 검색은 벡터가 맡고 번호로 잇습니다.'],
  ['직원 출퇴근 기록과 월별 집계','rdb','정확한 집계(SUM, GROUP BY)가 핵심입니다.'],
  ['사내 문서 3만 쪽에서 질문에 맞는 단락 찾기 (4장 RAG)','both','단락의 뜻은 벡터로 찾고, 문서 권한·작성일은 표 조건으로 거릅니다.'],
  ['상품 사진으로 비슷한 상품 찾기','vec','사진도 임베딩으로 좌표가 됩니다. 가격·재고는 표에서 확인합니다.'],
  ['회원 가입 정보(이메일·비밀번호 해시)','rdb','정확한 일치 조회와 개인정보 보호가 우선입니다.'],
  ['고객센터 문의 중 "환불"과 뜻이 같은 글 모으기','both','뜻은 벡터, 문의 날짜·처리 상태는 표에서.']],L={rdb:'관계형 DB',vec:'벡터 DB',both:'둘 다'},ans={};
  $('#sc35').innerHTML=S.map(function(s,i){return '<div class="mission" data-i="'+i+'"><span class="st">장면 '+(i+1)+'</span><div><p><b>'+s[0]+'</b></p><div class="chips">'+['rdb','vec','both'].map(function(k){return '<button class="bt" data-k="'+k+'" aria-pressed="false">'+L[k]+'</button>'}).join('')+'</div><p class="small fb" aria-live="polite"></p></div></div>'}).join('');
  function score(){var n=Object.keys(ans).length,ok=Object.keys(ans).filter(function(i){return ans[i]}).length;VL.kpis($('#k35'),[[ok+' / '+S.length,'맞힌 장면','g'],[n+'개','고른 장면','i']]);}
  $$('#sc35 .mission').forEach(function(m){var i=+m.dataset.i;$$('.bt',m).forEach(function(b){b.addEventListener('click',function(){$$('.bt',m).forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});var good=b.dataset.k===S[i][1];ans[i]=good;m.classList.toggle('ok',good);
    $('.fb',m).textContent=(good?'맞아요. ':'정답은 "'+L[S[i][1]]+'". ')+S[i][2];score();});});});score();
})();
/* 대결 3 */
Duel({el:'#d3',higherIsBetter:false,run:function(){var Q=VL.cloud(60,77,9),cf=0,cr=0,rr=0;Q.forEach(function(q){var t=VL.exact(PTS,q,10),s=VL.ivfSearch(PTS,IVFX,q,10,4);cf+=PTS.length;cr+=s.cmp;rr+=VL.recall(s.ids,t);});
    window._d3={rr:rr/Q.length};return {fly:cf/Q.length,robo:cr/Q.length}},scale:5000,fmt:function(v){return VL.fmt(v)+'번'},bigGap:1000,
  report:function(r){return '질문 60개 평균. 전수 비교 '+VL.fmt(r.fly)+'번(재현율 100%), 서랍 색인 '+VL.fmt(r.robo)+'번(재현율 '+VL.pct(window._d3.rr)+'). 둘 다 95% 기준을 넘었어요.'},
  verdict:{robo:'주판봇 승. 재현율 95% 이상을 지키면서 비교를 열 배 넘게 줄였습니다. 다만 이 승리는 "재현율을 재 봤기 때문에" 인정됩니다. 재지 않은 근사는 이긴 것이 아니라 운이 좋았던 것입니다.',fly:'초파리 승.',draw:'무승부.'}});
'''


def build_page():
    nav = [('#s1', '3-1 넣기'), ('#s2', '3-2 서랍'), ('#s3', '3-3 그래프'), ('#s4', '3-4 필터'), ('#s5', '3-5 함께 쓰기'), ('#duel', '대결'), ('#sum', '정리')]
    cov = cover('cover_03', '벡터 DB 연구실 · 3장', '벡터 창고', chars=(('doc', 'front'), ('asst', 'e16'), ('fly', 'magnify'), ('robo', 'happy')))
    hr = hero('벡터 DB 연구실 · 3장 · 벡터 DB의 저장·색인·검색', '벡터 창고',
              '좌표 수백만 개 중에서 가장 가까운 것을, 모두와 재지 않고 어떻게 빨리 찾을까?',
              '세 번째 수업은 창고 짓기. 하루는 인턴들에게 좌표를 어떻게 넣고, 서랍과 길 지도로 어떻게 빨리 찾는지 묻습니다. 주판봇이 처음으로 웃을지도 모릅니다.',
              [('%s GB' % num(ST['gb'], 2), '리뷰 100만 × 768차원 좌표 용량', 'i'), (pct(IVF[4]['recall']), '서랍 색인 재현율 (nprobe 4)', 'g'),
               ('%s번' % num(IVF[4]['cmp']), '질문당 비교 (전수 5,000번)', 'a'), (pct(GR[20]['recall']), '그래프 색인 재현율 (ef 20)', 'm')],
              [('doc', 'front', '오늘은 2장의 숙제를 풉니다. 좌표가 수백만 개일 때 어떻게 빨리 찾느냐.'),
               ('asst', 'e16', '오늘 실험이 제일 재밌어요. 지도를 누르면 길이 보여요! 시아, 모아, 준비됐죠?'),
               ('sia', 'smile', '계산기 챙겼어요.'), ('moa', 'report', '서랍 그림 미리 그려 왔어요.')],
              crowd('"오늘 하루 표정 좋다." "익숙해졌나 봐."', moods=('e01', 'e13', 'e16')))
    return build(P, title='3장 · 벡터 창고 — 벡터 DB의 저장·색인·검색 | 벡터 DB 연구실',
                 desc='벡터 DB 레코드와 저장 용량, 서랍 색인(IVF)과 그래프 색인(HNSW)의 속도·재현율 맞바꿈, 메타데이터 필터, 관계형 DB와 함께 쓰기를 실험으로 봅니다.',
                 nav=nav, cover_html=cov, hero=hr,
                 body=body() + footer([('리뷰 데이터', '이 연구실이 만든 가상 데이터'), ('IVF·PQ', 'Jégou, Douze, Schmid (2011) Product Quantization for Nearest Neighbor Search, IEEE TPAMI 33(1)'),
                                       ('HNSW', 'Malkov & Yashunin (2020) Efficient and robust approximate nearest neighbor search using HNSW graphs, IEEE TPAMI 42(4)'),
                                       ('FAISS', 'Johnson, Douze, Jégou (2021) Billion-scale similarity search with GPUs, IEEE Transactions on Big Data 7(3)'),
                                       ('pgvector', 'github.com/pgvector/pgvector (PostgreSQL 확장)'), ('관계형 DB', '<a href="%s">데이터베이스 설계 강좌</a> 9·10·13주차' % DBD)],
                                      ['점 5,000개는 설명용 2차원 점 구름입니다. 실제 좌표는 수백 차원입니다.', '그래프 색인은 HNSW를 두 층으로 줄인 설명용 구현입니다.', '"어디에 저장할까" 장면은 설명용 연습입니다.'],
                                      prev=('02_embedding.html', '2장 · 말을 좌표로'), nxt=('04_llm_rag.html', '4장 · LLM과 RAG')),
                 gloss=GLOSS, quizzes=QUIZ, page_js=JS, og='og_03')


if __name__ == '__main__':
    print(build_page())
