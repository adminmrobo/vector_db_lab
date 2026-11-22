# -*- coding: utf-8 -*-
"""7장 · 좌표와 관계 — 코사인 유사도 실전, 지식 그래프, 온톨로지"""
from lib import *

P = '07_graph_ontology.html'
G7 = R['graph7']; CD = R['cosdist']
TENSE = sum(m['n'] for m in R['movies'] if m['genre'] in ('공포', '스릴러', '미스터리', '액션'))


def body():
    b = three([
        ('무엇을', '벡터 DB를 실제로 쓸 때 꼭 만나는 세 가지를 다룹니다. ① 코사인 점수를 어떻게 읽고 문턱을 정하나 ② 점수만으로는 못 잇는 "관계"를 담는 지식 그래프 ③ 개념의 이름·계층·규칙을 정해 두는 온톨로지.'),
        ('왜 중요한가', '좌표는 "얼마나 닮았나"만 압니다. "프리미엄은 4K를 지원한다", "공포는 긴장감 장르의 하나다" 같은 관계와 약속은 모릅니다. 실제 서비스는 좌표·관계·약속을 함께 써서 검색을 단단하게 만듭니다.'),
        ('업무에서는', '"유사도 0.8이면 같은 건가요?", "여러 단계를 거쳐야 답이 나오는 질문은?", "부서마다 같은 걸 다르게 부르는데?"에 답할 수 있게 됩니다.')],
        '코드·수식을 몰라도 됩니다. 지식 그래프는 3D로 돌려 볼 수 있고, 온톨로지는 개념 나무를 눌러 검색 범위를 바꿔 봅니다.',
        [('KG', 'Knowledge Graph, 지식 그래프'), ('GraphRAG', '그래프를 함께 쓰는 RAG'), ('RDF', '사실을 주어·관계·목적어 세 부분으로 적는 표준'), ('OWL', '온톨로지를 적는 표준 언어'), ('SKOS', '개념의 이름·다른 이름·상하 관계를 적는 표준')])

    b += section('map', '큰 그림 — 이 장은 어디쯤인가',
                 '<div class="mapbar"><span>2장 · 임베딩</span><i>→</i><span>3장 · 벡터 창고</span><i>→</i><span>4장 · LLM과 RAG</span><i>→</i><span>6장 · 어텐션 3D</span><i>→</i><span class="on">7장 · 그래프·온톨로지</span><i>→</i><span>실전 연습장</span></div>'
                 '<div class="tw"><table class="tb"><tr><th></th><th>좌표 (벡터 DB)</th><th>관계 (지식 그래프)</th><th>약속 (온톨로지)</th></tr>'
                 '<tr><td>담는 것</td><td>뜻의 닮음</td><td>개체와 개체 사이의 이름 붙은 관계</td><td>개념의 이름·다른 이름·상하 계층·규칙</td></tr>'
                 '<tr><td>잘 답하는 질문</td><td>"이것과 비슷한 것"</td><td>"A의 B의 C는?" (여러 걸음)</td><td>"이 범주에 드는 것 전부", "이 데이터가 규칙에 맞나"</td></tr>'
                 '<tr><td>이 장의 실험</td><td>7-1 점수 분포와 문턱</td><td>7-2 그래프 3D, 7-3 GraphRAG</td><td>7-4 개념 나무로 거르기</td></tr></table></div>'
                 + say('doc', 'front', '좌표는 "닮음", 그래프는 "관계", 온톨로지는 "약속"입니다. 셋 중 하나만 고르는 게 아니라, 무엇을 묻느냐에 따라 함께 씁니다. 이 페이지 맨 아래 "지식 색인"도 바로 이 셋으로 만든 것입니다.'))

    # ── 7-1 코사인 실전
    s = say('doc', 'think', '상황 하나. 개발자가 묻습니다. "코사인 0.7 넘으면 같은 뜻으로 보면 되죠? 다른 팀이 그렇게 쓰던데요." 그대로 가져다 써도 될까요?')
    s += duo(why([('문제 상황', '검색 결과를 "보여 줄지 말지", 중복을 "합칠지 말지" 정하려면 점수 문턱이 필요합니다.'),
                  ('앞 방법의 한계', '2장은 순위(위에서 k개)만 썼습니다. 점수가 0.6이면 좋은 건지 나쁜 건지는 말하지 않았습니다.'),
                  ('해법', '우리 데이터에서 정답과 오답의 점수 분포를 그려 보고, 두 분포가 갈리는 곳에 문턱을 둡니다. 임베딩 모델이 바뀌면 점수의 눈금 자체가 바뀌므로 문턱도 다시 정합니다.')],
                 '시험 점수 70점의 뜻은 시험마다 다릅니다. 쉬운 시험의 70점과 어려운 시험의 70점은 다르니, 이번 시험의 점수 분포를 보고 합격선을 정합니다.'),
             mathbox('분포 두 개가 갈리는 곳은 어떻게 찾아요?', '자료의 정리 (중학교) — 중앙값과 그 가운데',
                     '대략의 문턱 ≈ (정답 점수의 중앙값 + 오답 점수의 중앙값) ÷ 2',
                     [('중앙값', '', '점수를 줄 세웠을 때 한가운데 값'), ('정답', '', '사람 이름표로 "재밌다는 리뷰"인 것'), ('오답', '', '나머지 리뷰')],
                     '"재밌는 영화 리뷰"에서 정답 %d개의 중앙값은 %s, 오답 %d개의 중앙값은 %s. 가운데는 (%s + %s) ÷ 2 ≈ <b>%s</b>. 여기서 시작해 정밀도·재현율을 보며 조정합니다.' % (
                         CD['rel_n'], num(CD['rel_med'], 2), CD['irr_n'], num(CD['irr_med'], 2), num(CD['rel_med'], 2), num(CD['irr_med'], 2), num((CD['rel_med'] + CD['irr_med']) / 2, 3)),
                     '0.7이 아니라 0.46 근처네요! 다른 팀 숫자를 그대로 쓰면 안 되겠어요.'))
    s += talk([('asst', 'e16', '시아, 다른 팀이 쓰는 "코사인 0.7 이상"을 우리 리뷰에 그대로 쓰면 어떻게 될까?'),
               ('sia', 'think', '0.7이면 꽤 높은 기준이니까… 정확하긴 한데 많이 놓칠 것 같아요.'),
               ('robo', 'coin', '0.7은 업계 표준이야! 그냥 쓰면 돼.'),
               ('fly', 'point', '"표준"인지 우리 데이터로 확인해 봐. 아래에서 문턱을 0.7에 두고 재현율을 보고, "다른 모델 눈금" 버튼도 눌러 봐.'),
               ('asst', 'report', '0.7이면 재현율이 크게 떨어져요. 다른 모델 눈금으로 바꾸면 같은 0.7이 전혀 다른 결과를 내요.')])
    s += panel('p71', '실험 · 코사인 점수 분포와 문턱', '가상 데이터 · "다른 모델 눈금"은 설명용 가정',
               '<div class="ctrl"><div class="group"><span class="glabel">찾을 뜻</span><select class="sel" id="q71"></select></div>'
               '<div class="group"><span class="glabel">문턱</span><input type="range" id="t71" min="0" max="100" value="70" aria-label="문턱"><span class="val" id="tv71"></span></div>'
               '<div class="group"><button class="bt" id="m71" aria-pressed="false">다른 모델 눈금 (점수가 0.6~0.95에 몰리는 모델)</button></div></div>'
               + canvas('cv71', 280, '정답 리뷰와 오답 리뷰의 코사인 점수 분포 막대그래프와 문턱 선') +
               '<div class="legend" id="lg71"></div><section class="kpis" id="k71" aria-label="채점"></section><div class="insight" id="in71" aria-live="polite"></div>', real=True)
    s += explain(['초록(정답)과 회색(오답) 분포가 겹치는 구간이 있습니다. 문턱을 어디에 두든 그 구간에서는 놓침이나 헛걸음이 생깁니다.',
                  '실제 임베딩 모델 중에는 서로 관계없는 문장끼리도 코사인이 0.6~0.8로 나오는 모델이 있습니다. 점수의 눈금이 모델마다 달라서, 문턱은 모델과 데이터마다 다시 정합니다.',
                  '문턱 대신 "위에서 k개"를 쓰면 눈금 문제를 피하지만, 관련 있는 것이 하나도 없을 때도 k개를 내밉니다(4장 주가 질문). 그래서 둘을 함께 씁니다.'],
                 '정답 이름표가 있어야 분포를 그릴 수 있습니다. 현장에서는 질문 수십~수백 개에 사람이 이름표를 붙인 평가 묶음을 먼저 만듭니다.')
    s += aicheck('"유사도 0.92, 같은 고객입니다"',
                 '<p>주판봇이 고객 문의 두 개의 코사인이 0.92라며 "같은 사람이 두 번 쓴 글이니 하나로 합치자"고 합니다.</p>'
                 '<p><b>확인 질문</b> ① 코사인 0.92가 "같은 사람"을 뜻할까요? ② 무엇을 함께 봐야 할까요?</p>'
                 '<details><summary>생각해 본 뒤 열어 보기</summary><p>① 아닙니다. 코사인은 "뜻이 닮았다"만 말합니다. 다른 고객 둘이 같은 불만을 쓰면 점수가 높게 나옵니다. '
                 '② 고객 번호·작성 시각 같은 표 정보(메타데이터)를 함께 봐야 합니다. 그리고 0.92가 이 모델에서 얼마나 높은 점수인지도 분포로 확인합니다.</p></details>')
    s += wrapup('코사인 점수는 절대 눈금이 아닙니다. 우리 데이터·우리 모델의 분포를 그려 문턱을 정하고, 모델이 바뀌면 다시 그립니다.')
    s += quiz('q71')
    b += step('s1', '7-1', '코사인 유사도 실전 — 점수를 읽고 문턱을 정하기', ['방법: 점수 분포 · 문턱 정하기', '일상: 시험마다 다른 합격선'], s)

    # ── 7-2 지식 그래프
    s = say('doc', 'think', '이번엔 고객이 이렇게 물었습니다. "프리미엄 화질로 보려면 인터넷이 얼마나 빨라야 해요?" 답은 두 문서에 나뉘어 있습니다. 요금제 안내에 "프리미엄 = 4K", 화질 안내에 "4K = 초당 25메가비트".')
    s += duo(why([('문제 상황', '답이 "프리미엄 → 4K → 25메가비트"처럼 사실 두 개를 이어야 나옵니다.'),
                  ('앞 방법의 한계', '좌표는 "프리미엄"과 "25메가비트"가 닮았는지만 봅니다. 두 낱말은 닮지 않았습니다. 그 사이를 잇는 것은 닮음이 아니라 "지원 화질", "필요 속도"라는 관계입니다.'),
                  ('해법', '사실을 (주어, 관계, 목적어) 세 부분으로 적어 점과 선으로 잇습니다(지식 그래프). 질문의 낱말에서 출발해 선을 따라가면 여러 걸음 떨어진 답에 닿습니다.')],
                 '지하철 노선도처럼, 역(개체)과 노선(관계)이 그려져 있으면 환승 두 번 거리의 역도 찾아갑니다. 역 이름이 비슷한지는 상관없습니다.'),
             mathbox('사실을 세 부분으로 적는다는 게 뭐예요?', '순서쌍과 관계 (고등학교 집합·함수의 생각) — (a, b)처럼 순서가 있는 짝에 이름을 붙인 것',
                     '사실 = (주어, 관계, 목적어),&nbsp;&nbsp; 두 걸음 = (A, 관계1, B) 다음 (B, 관계2, C)',
                     [('주어', '', '이야기의 대상. 예: 프리미엄'), ('관계', '', '이름 붙은 선. 예: 지원 화질'), ('목적어', '', '닿는 곳. 예: 4K')],
                     '(프리미엄, 지원 화질, 4K)와 (4K, 필요 속도, 초당 25메가비트)를 이으면 → 프리미엄은 <b>초당 25메가비트</b>가 필요합니다. 이 연구실 그래프는 점 %d개, 사실 %d개입니다.' % (G7['nodes'], G7['edges']),
                     '선 두 개만 따라가면 되네요! 좌표에는 선의 이름이 없었는데.'))
    s += dbnote('사실을 "주어 | 관계 | 목적어 | 출처" 열을 가진 표 하나에 담을 수 있습니다. 여러 걸음은 같은 표를 자기 자신과 여러 번 잇는(JOIN) SQL이 됩니다. 걸음이 늘수록 SQL이 길어집니다.',
                '그래프 DB(Neo4j 등)는 이 "선 따라가기"를 기본 동작으로 합니다. 벡터 DB와 함께 쓸 때는 점마다 좌표를 붙여 두고, 좌표로 출발점을 찾은 뒤 선을 따라갑니다(7-3).')
    s += talk([('asst', 'e16', '모아, "프리미엄"에서 "25메가비트"까지 몇 걸음일까?'),
               ('moa', 'report', '프리미엄 → 4K → 25메가비트. 두 걸음이요!'),
               ('robo', 'wow', '좌표로 "프리미엄"과 가장 닮은 걸 찾으면 바로 나오지 않아?'),
               ('fly', 'point', '아래 3D 그래프에서 "프리미엄"을 눌러 봐. 이어진 선의 이름을 읽고, "4K"를 이어서 눌러 봐.'),
               ('asst', 'report', '프리미엄에서 "지원 화질" 선으로 4K, 4K에서 "필요 속도" 선으로 25메가비트에 닿아요.')])
    s += panel('p72', '실험 · 랩플릭스 지식 그래프 3D', '안내 문서에서 뽑은 사실 %d개 · 3D 배치는 설명용' % G7['edges'],
               '<div class="ctrl"><div class="group"><button class="bt" id="lb72" aria-pressed="false">모든 점 이름 보이기</button><button class="bt" id="rot72" aria-pressed="true">자동 회전</button></div></div>'
               + canvas('cv72', 420, '랩플릭스 안내 문서에서 뽑은 개체 점과 관계 선으로 된 3차원 지식 그래프') +
               '<div class="legend" id="lg72"></div><div class="grid2"><div><h4 id="nm72">고른 점</h4><ul class="res" id="fx72"></ul></div><div><h4>점 고르기</h4><div class="chips" id="ch72"></div></div></div>', real=True)
    s += explain(['점의 색은 온톨로지 클래스(요금제·화질·오류 코드 등, 7-4)입니다. 선에는 "가격", "지원 화질", "원인" 같은 관계 이름이 붙어 있습니다.',
                  '모든 사실에는 출처 문서가 붙어 있습니다. 답을 낼 때 "어느 문서의 어느 사실을 이었나"를 그대로 보여 줄 수 있어, 근거 확인(4-5)이 쉬워집니다.',
                  '이 그래프는 사람이 안내 문서에서 사실을 뽑아 만들었습니다. 현장에서는 LLM으로 문서에서 개체와 관계를 뽑아 그래프를 만들고, 사람이 검수하기도 합니다.'],
                 '그래프를 만들고 고치는 비용이 큽니다. 문서가 바뀌면 사실도 바꿔야 하고, 뽑을 때 빠지거나 틀린 사실은 그대로 답의 구멍이 됩니다.')
    s += codefold([('MATCH (p:요금제 {name:"프리미엄"})-[:지원_화질]->(q)-[:필요_속도]->(s) RETURN s', '그래프 DB(Cypher)에서 두 걸음 따라가기'),
                   ('SELECT s3.o FROM fact s1 JOIN fact s3 ON s1.o = s3.s WHERE s1.s = \'프리미엄\' AND s1.p = \'지원 화질\' AND s3.p = \'필요 속도\';', '같은 일을 관계형 DB의 사실 표로')])
    s += wrapup('지식 그래프는 "닮음"이 아니라 "관계"를 저장합니다. 여러 걸음을 이어야 하는 질문에 강하고, 답의 근거 길을 그대로 보여 줄 수 있습니다.')
    s += quiz('q72')
    b += step('s2', '7-2', '지식 그래프 — 점과 이름 붙은 선', ['방법: 지식 그래프 · 삼항', '일상: 지하철 노선도'], s)

    # ── 7-3 GraphRAG
    s = say('doc', 'think', '그럼 벡터 DB는 필요 없을까요? 아닙니다. 고객은 "4K로 보면서 다운로드도 되는 요금제는 얼마야?"처럼 말하지, 그래프의 점 이름을 정확히 대지 않습니다. 출발점을 찾는 데 좌표가 필요합니다.')
    s += duo(why([('문제 상황', '여러 걸음 질문에 답하려면 ① 질문이 그래프의 어느 점에서 출발하는지 찾고 ② 선을 따라 필요한 사실을 모아야 합니다.'),
                  ('앞 방법의 한계', '벡터 검색만 쓰면 조각 k개 안에 필요한 문서가 모두 들어온다는 보장이 없습니다. 그래프만 쓰면 질문 말투와 점 이름이 다를 때 출발점을 못 찾습니다.'),
                  ('해법 (GraphRAG)', '① 질문의 낱말과 점 이름이 글자로 맞거나, 좌표가 가까운 점을 입구로 고릅니다. ② 입구에서 선을 1~2걸음 따라가 사실을 모읍니다. ③ 모은 사실을 글로 바꿔 LLM에게 붙입니다.')],
                 '처음 가는 동네에서 지도 앱 검색(좌표)으로 가까운 역을 찾고, 거기서부터 노선도(그래프)를 따라 목적지까지 갑니다.'),
             pair('벡터만 (조각 2개)', '질문 %d개 중 필요한 문서를 모두 모은 질문 %d개, 넘긴 글 평균 %d자. 조각 5개로 늘리면 %d개, %d자.' % (G7['mq'], G7['vec2']['ok'], G7['vec2']['chars'], G7['vec5']['ok'], G7['vec5']['chars']),
                  '벡터 + 그래프 (2걸음)', '답에 이르는 길의 점을 모두 모은 질문 %d개, 넘긴 사실 평균 %s개(%d자). 사실마다 출처 문서가 붙어 있습니다.' % (G7['graph']['ok'], num(G7['graph']['facts'], 1), G7['graph']['chars'])))
    s += talk([('asst', 'e13', '시아, 질문에 "4K"와 "다운로드"가 있으면 그래프의 어디서 출발하면 될까?'),
               ('sia', 'explain', '"4K" 점과 "다운로드" 점이요. 거기서 선을 따라가면 둘 다 이어진 요금제가 나와요!'),
               ('robo', 'happy', '그래프 + 벡터! 최신 GraphRAG가 최고야!'),
               ('fly', 'point', '최고인지는 질문마다 달라. 아래에서 걸음 수를 0, 1, 2로 바꿔 보고, 벡터만 쓴 쪽과 넘긴 글 양도 비교해 봐.'),
               ('asst', 'report', '0걸음이면 입구 점만, 1걸음이면 반쯤, 2걸음이면 답의 길이 다 모여요. 대신 2걸음에선 관계없는 사실도 조금 딸려 와요.')])
    s += panel('p73', '실험 · GraphRAG — 좌표로 입구를 찾고, 선을 따라 모으기', '가상 안내 문서 · 페이지가 직접 계산',
               '<div class="ctrl"><div class="group"><span class="glabel">여러 걸음 질문</span><select class="sel" id="q73"></select></div>'
               '<div class="group"><span class="glabel">따라갈 걸음</span><input type="range" id="h73" min="0" max="2" value="2" aria-label="걸음 수"><span class="val" id="hv73"></span></div>'
               '<div class="group"><button class="bt" id="rot73" aria-pressed="true">자동 회전</button></div></div>'
               + canvas('cv73', 400, '지식 그래프에서 입구 점과 따라간 점, 답의 길이 강조된 3D 그림') +
               '<p class="small muted">빨간 고리 = 입구(글자로 맞음), 주황 고리 = 입구(좌표가 가까움), 진한 점 = 따라가서 모은 점, 초록 굵은 선 = 답에 이르는 길.</p>'
               '<div class="grid2"><div><h4>그래프에서 모은 사실</h4><ul class="res" id="gf73"></ul></div><div><h4>벡터 검색만 (조각 2개)</h4><ul class="res" id="vc73"></ul></div></div>'
               '<section class="kpis" id="k73" aria-label="비교"></section><div class="insight" id="in73" aria-live="polite"></div>', real=True)
    s += explain(['입구는 두 가지로 찾습니다. 질문에 점 이름이 글자 그대로 있으면(글자), 아니면 점 이름의 좌표가 질문 좌표와 가까우면(뜻). 4장의 하이브리드 검색과 같은 생각입니다.',
                  '걸음을 늘리면 필요한 사실이 모이지만 관계없는 사실도 늘어납니다. 3장의 "근사의 손잡이"처럼, 빠짐없음과 군더더기의 맞바꿈입니다.',
                  '이 질문 %d개는 일부러 문서 두 개를 이어야 답이 나오게 골랐습니다. 한 문서로 답하는 질문(4장 대부분)에서는 벡터 검색만으로 충분하고 더 쌉니다.' % G7['mq']],
                 '좌표로 고른 입구가 엉뚱할 수 있습니다(입구 표시에서 엉뚱한 주황 고리를 찾아보세요). 실제 GraphRAG는 LLM으로 질문 속 개체를 뽑아 입구를 정하기도 하고, 그래프 전체를 묶음별로 요약해 두기도 합니다.')
    s += codefold([('entries = vector_db.query(embed(question), k=2, filter={"type": "entity"})', '좌표로 입구 점 찾기'),
                   ('facts = graph.expand(entries, hops=2)', '입구에서 2걸음 따라가 사실 모으기'),
                   ('prompt = SYSTEM + "\\n".join(f"{s} —{p}→ {o} ({doc})" for s, p, o, doc in facts) + question', '사실을 글로 바꿔 LLM에게')])
    s += wrapup('GraphRAG = 좌표로 입구를 찾고, 그래프로 길을 따라가고, 모은 사실을 근거로 붙이는 것. 여러 걸음 질문과 근거 설명이 필요할 때 씁니다.')
    s += quiz('q73')
    b += step('s3', '7-3', 'GraphRAG — 좌표로 입구를, 그래프로 길을', ['방법: GraphRAG · 여러 걸음 질문', '일상: 지도 앱 + 노선도'], s)

    # ── 7-4 온톨로지
    s = say('doc', 'think', '마케팅팀의 새 요청. "긴장감 있는 장르 영화 중에서 연기 좋다는 리뷰만 주세요." 그런데 영화 표에는 "공포", "스릴러"만 있고 "긴장감 장르"라는 값은 없습니다.')
    s += duo(why([('문제 상황', '사람은 "긴장감 장르"가 공포·스릴러·미스터리·액션을 묶는 말이라는 걸 압니다. 데이터는 모릅니다.'),
                  ('앞 방법의 한계', '장르 = "긴장감 장르"로 거르면 0건입니다. 좌표로 "긴장감"과 닮은 리뷰를 찾으면 장르와 상관없이 "심장 쫄깃", "소름" 같은 리뷰만 모이고, 정작 "연기가 좋다"는 조건은 흐려집니다.'),
                  ('해법 (온톨로지)', '개념의 계층(공포 ⊂ 긴장감 장르 ⊂ 장르), 다른 이름(꿀잼·존잼 → 재미), 규칙(현행 규정은 하나)을 미리 적어 둡니다. 검색할 때 이 약속으로 범위를 넓히거나 좁히고, 데이터가 약속에 맞는지 검사합니다.')],
                 '도서관 분류표에서 "문학 > 소설 > 추리소설"을 정해 두면, "소설 코너"를 찾는 사람에게 추리소설도 함께 보여 줄 수 있습니다.'),
             mathbox('"하위 개념 포함"은 어떻게 계산해요?', '집합 (고등학교) — 부분집합은 이어진다 (A ⊂ B, B ⊂ C이면 A ⊂ C)',
                     '공포 ⊂ 긴장감 장르 ⊂ 장르 ⇒ 공포 ⊂ 장르,&nbsp;&nbsp; 긴장감 장르의 영화 = 공포 ∪ 스릴러 ∪ 미스터리 ∪ 액션',
                     [('⊂', '부분집합', '왼쪽이 오른쪽에 포함됨'), ('∪', '합집합', '둘 중 하나라도 속하면'), ('⇒', '그러므로', '규칙에서 저절로 나오는 결론(추론)')],
                     '영화 표에 "긴장감 장르"는 0편. 온톨로지로 하위 개념을 펼치면 공포·스릴러·미스터리·액션 네 편, 리뷰 <b>%d개</b>가 검색 범위가 됩니다.' % TENSE,
                     '표에 없는 말도 약속(온톨로지)만 있으면 찾아지네요. 1장의 동의어 사전을 제대로 정리한 버전 같아요!'))
    s += talk([('asst', 'e16', '모아, "긴장감 장르"로 영화 표를 거르면 몇 편이 나올까?'),
               ('moa', 'think', '장르 열에 그런 값이 없으니까… 0편이요?'),
               ('robo', 'coin', '그럼 좌표로 "긴장감" 리뷰를 찾으면 되지!'),
               ('fly', 'point', '그러면 다른 장르 리뷰도 섞일걸. 아래 개념 나무에서 "긴장감 장르"를 고르고 "하위 개념 포함"을 껐다 켜 봐.'),
               ('asst', 'report', '끄면 0건, 켜면 네 장르가 범위에 들어와요. 그 안에서만 좌표 검색을 하니 다른 장르가 안 섞여요.')])
    s += crowd('"하루, 이제 질문을 거꾸로 받아도 막힘이 없다." "인턴들도 척척이야."', moods=('e16', 'e01', 'e01'))
    s += panel('p74', '실험 · 온톨로지로 검색 범위 정하기', '설명용 온톨로지 · 페이지가 직접 계산',
               '<div class="grid2"><div><h4>개념 나무 (장르)</h4><div id="tr74" class="tree"></div>'
               '<div class="ctrl"><div class="group"><button class="bt" id="inf74" aria-pressed="true">하위 개념 포함 (추론)</button></div></div></div>'
               '<div><div class="ctrl"><div class="group"><span class="glabel">찾을 뜻</span><select class="sel" id="q74"></select></div></div>'
               '<div class="ctrl"><div class="group"><span class="glabel">다른 이름으로 넓히기</span><button class="bt" id="alt74" aria-pressed="false">온톨로지의 다른 이름 목록 보기</button></div></div><p class="small" id="al74"></p></div></div>'
               '<section class="kpis" id="k74" aria-label="숫자 요약"></section><ul class="res" id="rs74"></ul>'
               '<h4>온톨로지 규칙 검사 — 데이터가 약속을 지키나</h4><div class="ctrl"><div class="group"><button class="bt" id="bad74" aria-pressed="false">잘못된 데이터 넣어 보기 (구버전 규정도 "현행"으로 표시)</button></div></div><div id="ru74"></div>'
               '<div class="insight" id="in74" aria-live="polite"></div>', real=True)
    s += explain(['개념 나무의 한 클래스를 고르면, 하위 개념을 모두 펼쳐 그 영화의 리뷰만 검색 범위로 삼습니다(메타데이터 필터, 3-4). 그 안에서 좌표 검색을 합니다.',
                  '"다른 이름" 목록(SKOS의 altLabel)은 1장의 동의어 사전을 개념마다 정리해 둔 것입니다. 글자 검색을 넓히거나, 그래프의 입구를 찾을 때 씁니다.',
                  '규칙 검사는 온톨로지의 약속으로 데이터의 모순을 찾습니다. "현행 규정이 둘"이면 4-5의 함정이 생기기 전에 미리 알 수 있습니다.',
                  '이 연구실 페이지마다 맨 아래 붙은 지식 색인도 같은 방식입니다. 개념(Concept)·방법(Method)·주장(Claim) 같은 클래스와 "broader", "hasLimitation" 같은 관계로 시리즈 전체를 하나의 그래프로 잇습니다.'],
                 '이 온톨로지는 설명용으로 작게 만들었습니다. 실제 온톨로지는 분야 전문가가 오래 다듬고, OWL·SKOS 같은 표준으로 적어 여러 시스템이 함께 씁니다.')
    s += codefold([('ex:공포 rdfs:subClassOf ex:긴장감장르 .', 'RDF/OWL로 "공포는 긴장감 장르의 하위 개념"을 적기'),
                   ('ex:재미 skos:altLabel "꿀잼"@ko, "존잼"@ko .', 'SKOS로 다른 이름 적기'),
                   ("collection.query(q, where={'genre': {'$in': expand('긴장감 장르')}})", '온톨로지로 펼친 장르 목록을 벡터 검색 필터로')])
    s += wrapup('온톨로지는 "무엇을 같은 것으로, 무엇을 무엇의 한 종류로 볼지"의 약속입니다. 벡터 검색의 범위를 정하고, 그래프의 점에 종류를 주고, 데이터의 모순을 미리 잡습니다.')
    s += quiz('q74')
    b += step('s4', '7-4', '온톨로지 — 개념의 이름·계층·규칙', ['방법: 온톨로지 · 하위 개념 추론', '일상: 도서관 분류표'], s)

    # ── 7-5 셋을 함께
    s = say('doc', 'think', '마지막으로 정리해 봅시다. 랩플릭스에 들어오는 질문 여덟 개를 받았습니다. 각각 무엇으로 답하면 가장 좋을까요? 표, 좌표, 그래프, 온톨로지.')
    s += duo(why([('문제 상황', '한 서비스에 성격이 다른 질문이 섞여 들어옵니다.'),
                  ('앞 방법의 한계', '한 가지 도구로 모두 답하려 하면, 다른 도구가 잘하는 질문에서 실수합니다(1·4·7장의 대결들).'),
                  ('해법', '질문의 모양으로 나눕니다. 정확한 값·집계 → 표(SQL). 비슷한 것 → 좌표(벡터 DB). 여러 걸음 관계 → 그래프. 범주·다른 이름·규칙 → 온톨로지. 대부분은 둘 이상을 함께 씁니다.')],
                 '연장통에서 못에는 망치, 나사에는 드라이버를 꺼내듯, 질문 모양을 먼저 봅니다.'),
             pair('한 줄 기준', '"정확히?" → 표 · "비슷한?" → 좌표 · "A의 B의 C?" → 그래프 · "이 종류 전부? 같은 말?" → 온톨로지',
                  '함께 쓰는 흔한 모양', '온톨로지로 범위를 정하고(필터) → 좌표로 찾고 → 그래프로 근거 길을 잇고 → 표에서 최신 값·권한을 확인한다.'))
    s += talk([('asst', 'e01', '시아, 모아, 마지막 문제! 질문 여덟 개를 도구별로 나눠 볼까요?'),
               ('sia', 'firm', '저는 표하고 그래프 문제 맡을게요.'), ('moa', 'cheer', '그럼 저는 좌표하고 온톨로지요!'),
               ('robo', 'happy', '전부 GraphRAG로 하면 안 돼?'),
               ('fly', 'point', '"이번 달 결제 건수"를 GraphRAG로 셀 거야? 하나씩 골라 보면 알게 돼.')])
    s += panel('p75', '실험 · 이 질문엔 무엇으로? — 질문 여덟 개 나누기', '설명용 판별 연습', '<div id="sc75"></div><section class="kpis" id="k75" aria-label="맞힌 수"></section>', real=True)
    s += explain(['정답은 하나가 아닌 경우가 많습니다. 여기서는 "가장 먼저 꺼낼 도구"를 정답으로 두고, 함께 쓰면 좋은 도구를 풀이에 적었습니다.',
                  '이 시리즈 전체가 이 표의 한 줄씩이었습니다. 1장은 표, 2~4장은 좌표, 6장은 좌표를 읽는 모델, 7장은 그래프와 온톨로지.'],
                 '도구를 늘릴수록 만들고 고치는 비용도 늘어납니다. 질문 묶음으로 효과를 재고, 효과가 비용보다 클 때 더합니다.')
    s += wrapup('좌표는 닮음, 그래프는 관계, 온톨로지는 약속, 표는 사실. 질문의 모양을 먼저 보고 도구를 고르면, 벡터 DB가 가장 빛나는 자리가 보입니다.')
    s += quiz('q75')
    b += step('s5', '7-5', '셋을 함께 — 좌표·관계·약속, 그리고 표', ['판단: 질문 모양별 도구', '일상: 연장통'], s)

    b += duel('d7', '여러 걸음 질문 %d개 — 벡터 검색만 (조각 2개) vs 벡터 + 지식 그래프 (2걸음)' % G7['mq'], '벡터 검색만, 조각 2개 (단순하고 싸게)', 'GraphRAG — 좌표로 입구, 그래프로 2걸음',
              '"그래프 만드는 비용이 커. 조각 두 개면 웬만한 건 다 들어 있을걸?"', '"최신은 GraphRAG지! 관계를 따라가야 여러 걸음 질문이 풀린다고!"',
              '필요한 사실(문서)을 모두 모은 질문 수 (질문 %d개)' % G7['mq'])

    b += section('sum', '정리 — 벡터 DB를 "제대로" 쓰는 네 가지 습관',
                 '<div class="steps"><div><span class="n">1</span><h4>점수는 분포로 읽는다</h4><p>코사인 0.7의 뜻은 모델과 데이터마다 다릅니다. 정답·오답 분포를 그려 문턱을 정합니다.</p></div>'
                 '<div><span class="n">2</span><h4>관계는 그래프에</h4><p>"A의 B의 C" 질문은 좌표가 아니라 이름 붙은 선이 답합니다. 좌표는 입구를 찾습니다.</p></div>'
                 '<div><span class="n">3</span><h4>약속은 온톨로지에</h4><p>범주·다른 이름·규칙을 적어 두면 검색 범위가 정확해지고, 데이터의 모순이 미리 보입니다.</p></div>'
                 '<div><span class="n">4</span><h4>사실은 표에서 확인</h4><p>가격·날짜·권한의 최신 값은 표(관계형 DB)가 맡습니다. 1장에서 시작한 이야기가 여기서 다시 만납니다.</p></div></div>'
                 + bridge('field', '현장에 옮기면', '사내 문서 챗봇에 "부서·문서 종류·보안 등급" 온톨로지를 붙이면, 권한 있는 문서만 좌표로 찾고(필터), 규정 사이의 "대체함" 관계로 최신 판을 고르고, 답에 근거 길을 달 수 있습니다.',
                          '그래프와 온톨로지는 만드는 비용이 큽니다. 작게 시작해 자주 묻는 관계부터 넣습니다.'))

    b += outro([('doc', 'front', '오늘 세 줄 정리. ① 코사인 점수는 우리 데이터의 분포로 읽는다. ② 여러 걸음 관계는 지식 그래프가, 입구 찾기는 좌표가 맡는다. ③ 온톨로지는 범위·다른 이름·규칙의 약속이다.'),
                ('robo', 'happy', '마지막 대결 승리! 이로써 전적 3승 4패. 실전 연습장에서 마저 따라잡는다!'),
                ('fly', 'coffee', '이번엔 인정. 다만 한 문서 질문엔 여전히 벡터만으로 충분하다는 것도 잊지 마.'),
                ('sia', 'proud', '질문 모양 보고 도구 고르기, 회사 가서 바로 써먹을래요.'),
                ('moa', 'sparkle', 'DB 설계 노트 마지막에 "좌표·관계·약속·사실" 네 항목 표를 그렸어요!'),
                ('asst', 'e01', '특강까지 모두 끝! 이제 진짜 실전 연습장이에요. 처음엔 떨렸는데, 여러분 덕분에 끝까지 왔어요.')],
               '하루와 인턴들이 3D 지식 그래프 앞에서 선을 따라가며 웃는 장면',
               crowd('"하루, 특강까지 완주!" "처음 그 떨던 하루 맞아?" "박수!"', moods=('e01', 'e16', 'e01')))
    return b


GLOSS = {
    '지식 그래프': ['지식 그래프 (knowledge graph)', '개체를 점으로, 관계를 이름 붙은 선으로 이은 사실의 그물. (주어, 관계, 목적어)로 적습니다.'],
    '온톨로지': ['온톨로지 (ontology)', '한 분야의 개념과 그 이름·계층·성질·규칙을 정해 둔 약속. OWL·SKOS 같은 표준으로 적습니다.'],
    'GraphRAG': ['GraphRAG', '좌표 검색으로 그래프의 입구를 찾고, 관계를 따라 모은 사실을 근거로 LLM에게 붙이는 RAG.'],
    '삼항': ['삼항 (triple)', '사실 하나를 (주어, 관계, 목적어) 세 부분으로 적은 것. RDF의 기본 단위.'],
    '문턱': ['문턱 (threshold)', '이 점수 이상이면 보여 주거나 같다고 보는 기준값.'],
    '하위 개념': ['하위 개념 (subclass)', '더 넓은 개념에 포함되는 개념. 공포는 긴장감 장르의 하위 개념.'],
    '다른 이름': ['다른 이름 (altLabel)', '같은 개념의 동의어·줄임말. SKOS의 altLabel.'],
    '추론': ['추론 (reasoning)', '적어 둔 약속에서 저절로 나오는 결론을 계산하는 것. 공포 ⊂ 긴장감 장르 ⊂ 장르 ⇒ 공포 ⊂ 장르.'],
    '그래프 DB': ['그래프 DB', '점과 선을 저장하고 선 따라가기를 기본 동작으로 하는 데이터베이스. Neo4j 등.'],
    '코사인': ['코사인 유사도', '두 좌표 사이 각도로 잰 닮음. 2장.'],
}

QUIZ = {
    'q71': [{'q': '다른 팀이 쓰는 "코사인 0.7 이상" 문턱을 그대로 가져오면 안 되는 이유는?', 'o': ['코사인은 계산이 틀리기 쉬워서', '점수의 눈금이 모델과 데이터마다 달라서', '0.7은 너무 작아서'], 'a': 1,
             'why': '같은 0.7이라도 모델과 데이터에 따라 뜻이 다릅니다. 우리 데이터의 정답·오답 분포로 다시 정합니다.', 'hint': '"다른 모델 눈금" 버튼을 떠올려 보세요.'},
            {'q': '정답 중앙값 0.63, 오답 중앙값 0.30일 때 출발점 문턱 어림값은?', 'o': ['0.30', '약 0.47', '0.90'], 'a': 1,
             'why': '(0.63 + 0.30) ÷ 2 ≈ 0.465. 여기서 시작해 정밀도·재현율을 보며 조정합니다.', 'hint': '두 중앙값의 가운데.'}],
    'q72': [{'q': '"프리미엄 → 4K → 25메가비트"를 잇는 것은?', 'o': ['좌표의 닮음', '이름 붙은 관계(지원 화질, 필요 속도)', '별점'], 'a': 1,
             'why': '프리미엄과 25메가비트는 뜻이 닮지 않았습니다. 둘을 잇는 것은 관계입니다.', 'hint': '선에 적힌 이름.'},
            {'q': '지식 그래프의 사실 하나를 적는 기본 모양은?', 'o': ['(주어, 관계, 목적어)', '(좌표, 점수)', '(행, 열)'], 'a': 0,
             'why': '삼항(triple)이라고 부르며, RDF의 기본 단위입니다.', 'hint': '세 부분.'}],
    'q73': [{'q': 'GraphRAG에서 좌표(벡터 검색)의 역할은?', 'o': ['선을 따라간다', '질문과 맞는 그래프의 입구 점을 찾는다', '온톨로지를 만든다'], 'a': 1,
             'why': '질문의 말투와 점 이름이 달라도 좌표로 가까운 점을 입구로 찾습니다. 그다음 선을 따라갑니다.', 'hint': '지도 앱 검색 + 노선도.'},
            {'q': '따라갈 걸음 수를 늘리면?', 'o': ['필요한 사실도, 관계없는 사실도 늘어난다', '사실이 줄어든다', '아무 변화가 없다'], 'a': 0,
             'why': '빠짐없음과 군더더기의 맞바꿈입니다.', 'hint': '0·1·2걸음 비교.'}],
    'q74': [{'q': '영화 표에 "긴장감 장르" 값이 없는데도 찾을 수 있게 해 주는 것은?', 'o': ['코사인 문턱', '온톨로지의 하위 개념 추론', 'k를 늘리기'], 'a': 1,
             'why': '공포·스릴러·미스터리·액션이 긴장감 장르의 하위 개념이라는 약속으로 범위를 펼칩니다.', 'hint': '"하위 개념 포함" 버튼.'},
            {'q': '"현행 환불 규정이 둘"이라는 모순을 미리 잡는 것은?', 'o': ['온톨로지 규칙 검사', '어텐션', 'BM25'], 'a': 0,
             'why': '"현행 판은 하나뿐"이라는 약속에 데이터를 비춰 봅니다.', 'hint': '잘못된 데이터 넣어 보기.'}],
    'q75': [{'q': '"이번 달 결제 건수는?"에 가장 먼저 꺼낼 도구는?', 'o': ['벡터 DB', '표(SQL 집계)', '지식 그래프'], 'a': 1,
             'why': '정확한 집계는 표가 가장 잘합니다.', 'hint': '"정확히?"인가요?'},
            {'q': '"LP-204가 주말에 뜨면 어디에 물어야 빨라?"에 알맞은 조합은?', 'o': ['표만', '좌표로 입구 + 그래프로 여러 걸음', '온톨로지만'], 'a': 1,
             'why': 'LP-204 → 결제 문제 → 채팅 상담 → 주말 운영, 여러 걸음 관계입니다.', 'hint': '7-3의 질문.'}],
}

JS = r'''
var D=VL.load(),RV=D.reviews,G=VL.graphPrep(D.graph),CH=VL.chunk(D.kb,150,0,true);
var CLS=['요금제','가격','화질','동시 시청 수','기능','조건','할인','오류 코드','원인','일정','앱 메뉴','상담 창구','문의 유형','규정','절차','정책','요금 항목','자막 언어'],CC={},PAL=['#1e55c8','#a35c00','#13733a','#9b3fb5','#0b7a86','#8a96a3','#c42a6e','#c9302c','#b23a48','#6d4c41','#3949ab','#2f7d32','#e08a00','#5b6874','#00838f','#7b1fa2','#795548','#558b2f'];CLS.forEach(function(c,i){CC[c]=PAL[i%%PAL.length]});
var LAY=VL.layout3d(G.nodes.length,G.edges.map(function(e){return [G.idx[e.s],G.idx[e.o]]}),7);
function rotBtn(id,v){$(id).addEventListener('click',function(){var on=v.toggleAuto();this.setAttribute('aria-pressed',on?'true':'false');});if(window.REDUCED)$(id).setAttribute('aria-pressed','false');}
function factText(e){return G.nodes[G.idx[e.s]].label+' —'+e.p+'→ '+G.nodes[G.idx[e.o]].label;}
/* 7-1 */
(function(){var cv=$('#cv71'),alt=false,Q=D.searchq;$('#q71').innerHTML=Q.map(function(q,i){return '<option value="'+i+'">'+q.q+'</option>'}).join('');
  function sc(x){return alt?.62+.33*x:x;}
  function draw(){var q=Q[+$('#q71').value],qv=VL.embed(q.q).v,t=+$('#t71').value/100;$('#tv71').textContent=t.toFixed(2);var S=RV.map(function(r){return {s:sc(VL.cos(qv,r.vec)),y:VL.rel(r,q.asp)}});
    var bins=40,lo=-0.4,hi=1,hr=new Array(bins).fill(0),hn=new Array(bins).fill(0);S.forEach(function(x){var b=Math.max(0,Math.min(bins-1,Math.floor((x.s-lo)/(hi-lo)*bins)));(x.y?hr:hn)[b]++;});
    var f=fit(cv),g=f.c,mx=Math.max.apply(null,hr.concat(hn)),A=VL.axes(g,f.W,f.H,{xmin:lo,xmax:hi,ymin:0,ymax:mx+2,xlab:'코사인 점수',ylab:'리뷰 수',xfmt:function(v){return v.toFixed(1)}}),bw=(A.sx(hi)-A.sx(lo))/bins;
    for(var i=0;i<bins;i++){var x=A.sx(lo+i*(hi-lo)/bins);g.fillStyle='rgba(138,150,163,.55)';g.fillRect(x,A.sy(hn[i]),bw-1,A.sy(0)-A.sy(hn[i]));g.fillStyle='rgba(19,115,58,.75)';g.fillRect(x+bw*.25,A.sy(hr[i]),bw*.5,A.sy(0)-A.sy(hr[i]));}
    g.strokeStyle='#c9302c';g.lineWidth=2;g.beginPath();g.moveTo(A.sx(t),A.T);g.lineTo(A.sx(t),A.sy(0));g.stroke();g.lineWidth=1;stamp(g,f.W,alt?'다른 모델 눈금 (가정)':'교육용 임베딩');
    VL.legend($('#lg71'),[['정답 (이름표가 맞음)','#13733a'],['오답','#8a96a3'],['문턱','#c9302c']]);
    var tp=S.filter(function(x){return x.y&&x.s>=t}).length,fp=S.filter(function(x){return !x.y&&x.s>=t}).length,fn=S.filter(function(x){return x.y&&x.s<t}).length,p=tp/(tp+fp||1),r=tp/(tp+fn||1);
    VL.kpis($('#k71'),[[(tp+fp)+'개','문턱을 넘은 리뷰','i'],[VL.pct(p),'정밀도','g'],[VL.pct(r),'재현율','m'],[(p+r?2*p*r/(p+r):0).toFixed(3),'F1','a']]);
    $('#in71').innerHTML='<p class="'+(r<.5?'r':'g')+'">'+(r<.5?'문턱 '+t.toFixed(2)+'에서는 정답의 절반 넘게 놓칩니다.':'문턱 '+t.toFixed(2)+'에서 정답의 '+VL.pct(r,0)+'를 건집니다.')+(alt?' 다른 모델 눈금에서는 거의 모든 점수가 0.6 위로 몰려, 같은 문턱의 뜻이 완전히 달라집니다.':'')+'</p>';}
  $('#q71').addEventListener('change',draw);$('#t71').addEventListener('input',draw);$('#m71').addEventListener('click',function(){alt=!alt;this.setAttribute('aria-pressed',alt?'true':'false');draw();});
  Loop.add(cv,function(dt){if(dt===0)draw();});
})();
/* 7-2 */
(function(){var lab=false,sel=G.idx['premium'],v=VL.view3d($('#cv72'),{stamp:'점 '+G.nodes.length+' · 사실 '+G.edges.length,onPick:function(id){sel=id;run();}});rotBtn('#rot72',v);
  VL.legend($('#lg72'),CLS.slice(0,12).map(function(c){return [c,CC[c]]}));
  $('#ch72').innerHTML=['premium','uhd','lp204','refund2','student','dl'].map(function(id){return '<button class="bt" data-n="'+G.idx[id]+'">'+G.nodes[G.idx[id]].label+'</button>'}).join('');
  $$('#ch72 .bt').forEach(function(b){b.addEventListener('click',function(){sel=+b.dataset.n;run();})});
  function run(){var nb={};G.adj[sel].forEach(function(a){nb[a[0]]=a[1]});var it=[];
    G.edges.forEach(function(e,k){var i=G.idx[e.s],j=G.idx[e.o],on=i===sel||j===sel;it.push({t:'ln',a:LAY[i],b:LAY[j],c:on?'#c9302c':'#b8c2cc',w:on?2.5:1,al:on?.9:.5});});
    G.nodes.forEach(function(nd,i){var on=i===sel||(i in nb);it.push({p:LAY[i],r:i===sel?9:on?6:4,c:CC[nd.cls]||'#5b6874',al:on?1:.55,label:(lab||on)?nd.label:null,bold:i===sel,id:i,ring:i===sel?'#c9302c':null});});v.set(it);
    $('#nm72').textContent='고른 점: '+G.nodes[sel].label+' ('+G.nodes[sel].cls+')';
    $('#fx72').innerHTML=G.adj[sel].map(function(a){var e=G.edges[a[1]];return '<li class="nt"><small>출처: '+D.kb.filter(function(k){return k.id===e.doc})[0].title+'</small>'+VL.esc(factText(e))+'</li>'}).join('');}
  $('#lb72').addEventListener('click',function(){lab=!lab;this.setAttribute('aria-pressed',lab?'true':'false');run();});run();
})();
/* 7-3 */
(function(){$('#q73').innerHTML=G.mq.map(function(q,i){return '<option value="'+i+'">'+q.q+'</option>'}).join('');var v=VL.view3d($('#cv73'),{stamp:'GraphRAG'});rotBtn('#rot73',v);
  function run(){var q=G.mq[+$('#q73').value],h=+$('#h73').value;$('#hv73').textContent=h+'걸음';var r=VL.graphRAG(G,q.q,{hops:h}),path=q.path.map(function(p){return G.idx[p]}),on={};r.nodes.forEach(function(i){on[i]=1});
    var it=[];G.edges.forEach(function(e){var i=G.idx[e.s],j=G.idx[e.o],pi=path.indexOf(i),pj=path.indexOf(j),onp=pi>=0&&pj>=0&&Math.abs(pi-pj)===1&&on[i]&&on[j];it.push({t:'ln',a:LAY[i],b:LAY[j],c:onp?'#13733a':(on[i]&&on[j]?'#a35c00':'#d5dbe2'),w:onp?4:(on[i]&&on[j]?1.8:1),al:onp?1:.6});});
    G.nodes.forEach(function(nd,i){var e=r.entries[i];it.push({p:LAY[i],r:e?9:on[i]?6:3.5,c:CC[nd.cls]||'#5b6874',al:on[i]?1:.3,label:on[i]?nd.label:null,bold:!!e||path.indexOf(i)>=0,ring:e==='글자'?'#c9302c':e==='뜻'?'#e08a00':null});});v.set(it);
    $('#gf73').innerHTML=r.facts.length?r.facts.map(function(e){var onp=path.indexOf(G.idx[e.s])>=0&&path.indexOf(G.idx[e.o])>=0;return '<li class="'+(onp?'ok':'nt')+'"><small>'+e.doc+'</small>'+VL.esc(factText(e))+'</li>'}).join(''):'<li class="nt">0걸음: 입구 점만 고르고 사실은 아직 모으지 않았습니다.</li>';
    var vh=VL.retrieve(CH,q.q,{k:2,alpha:.3,newest:true});$('#vc73').innerHTML=vh.map(function(x){return '<li class="'+(q.docs.indexOf(x.c.doc)>=0?'ok':'no')+'"><span class="sc">'+x.s.toFixed(2)+'</span><small>'+x.c.title+'</small>'+VL.esc(x.c.text)+'</li>'}).join('');
    var gok=path.every(function(i){return on[i]})&&h>0,vok=q.docs.every(function(d){return vh.some(function(x){return x.c.doc===d})}),gch=r.facts.map(factText).join(' / ').length,vch=vh.reduce(function(a,x){return a+x.c.text.length},0);
    VL.kpis($('#k73'),[[gok?'모음':'못 모음','그래프: 답에 이르는 길',gok?'g':'r'],[vok?'모음':'못 모음','벡터만: 필요한 문서 '+q.docs.length+'개',vok?'g':'r'],[r.facts.length+'개 · '+gch+'자','그래프가 넘긴 사실','i'],[vch+'자','벡터가 넘긴 글','a']]);
    $('#in73').innerHTML='<p class="m">입구: '+Object.keys(r.entries).map(function(i){return '"'+G.nodes[i].label+'"('+r.entries[i]+')'}).join(', ')+'. 정답: '+q.ans+'.</p><p class="'+(gok?'g':'a')+'">'+(gok?'초록 굵은 선이 답에 이르는 길입니다. 사실마다 출처 문서가 붙어 근거를 그대로 보여 줄 수 있습니다.':'아직 길이 다 모이지 않았습니다. 걸음을 늘려 보세요.')+'</p>';}
  $('#q73').addEventListener('change',run);$('#h73').addEventListener('input',run);run();
})();
/* 7-4 */
(function(){var inf=true,bad=false,cls='긴장감 장르',Q=D.searchq,ON=G.ont,alts=false;$('#q74').innerHTML=Q.map(function(q,i){return '<option value="'+i+'"'+(q.id==='acting'?' selected':'')+'>'+q.q+'</option>'}).join('');
  function kids(c){return ON.filter(function(o){return o.parent===c}).map(function(o){return o.c});}
  function expand(c){var out=[c];kids(c).forEach(function(k){out=out.concat(inf?expand(k):[k])});return out;}
  function tree(c,d){var k=kids(c);return '<div style="margin-left:'+(d*14)+'px"><button class="bt" data-c="'+c+'" aria-pressed="'+(c===cls)+'" style="padding:2px 10px;font-size:13.5px;margin:2px 0">'+c+'</button></div>'+k.map(function(x){return tree(x,d+1)}).join('');}
  $('#tr74').innerHTML=tree('장르',0);
  function run(){var q=Q[+$('#q74').value],qv=VL.embed(q.q).v,scope=inf?expand(cls):[cls],G2=D.movies.filter(function(m){return scope.indexOf(m.genre)>=0}).map(function(m){return m.id}),pool=RV.filter(function(r){return G2.indexOf(r.movie)>=0});
    var top=VL.topk(pool,function(r){return VL.cos(qv,r.vec)},6),all=VL.topk(RV,function(r){return VL.cos(qv,r.vec)},6),out=all.filter(function(x){return G2.indexOf(x.it.movie)<0}).length;
    VL.kpis($('#k74'),[[scope.filter(function(s){return D.movies.some(function(m){return m.genre===s})}).length+'개','범위에 든 실제 장르','i'],[pool.length+'개','검색 범위의 리뷰','g'],[out+' / 6','범위 없이 찾으면 섞이는 다른 장르','r']]);
    $('#rs74').innerHTML=top.length?top.map(function(x){return '<li class="'+(VL.rel(x.it,q.asp)?'ok':'no')+'"><span class="sc">'+x.s.toFixed(2)+'</span><small>'+x.it.title+' · '+x.it.genre+' · '+VL.stars(x.it.stars)+'</small>'+VL.esc(x.it.text)+'</li>'}).join(''):'<li class="no">검색 범위가 0건입니다. 영화 표에 "'+cls+'"라는 장르 값은 없습니다. "하위 개념 포함"을 켜 보세요.</li>';
    $('#al74').innerHTML=alts?'<b>'+D.aspect_ko[q.asp[0]]+'</b>의 다른 이름: '+(D.graph.aspect_alt[q.asp[0]]||[]).join(', ')+' — 이 목록으로 글자 검색을 넓히면 '+VL.likeAny(RV,D.graph.aspect_alt[q.asp[0]]||[]).length+'개, 대표 낱말 하나("'+q.like+'")로는 '+VL.like(RV,q.like).length+'개.':'';
    var cur=D.kb.filter(function(k){return /환불/.test(k.title)&&(bad||!k.old)}).length,rules=[[D.graph.rules[0].ko,cur===1,'현행 환불 규정 '+cur+'개'],[D.graph.rules[1].ko,/6월 30일까지/.test(D.kb.filter(function(k){return k.id==='refund_v1'})[0].text),'구버전 문서에 "2026년 6월 30일까지 적용"'],
      [D.graph.rules[2].ko,['basic','standard','premium'].every(function(p){return G.edges.filter(function(e){return e.s===p&&e.p==='가격'}).length===1}),'요금제 3개 모두 가격 1개']];
    $('#ru74').innerHTML=rules.map(function(r){return '<div class="mission'+(r[1]?' ok':'')+'"><span class="st">'+(r[1]?'통과':'위반')+'</span><p>'+r[0]+' <span class="small muted">('+r[2]+')</span></p></div>'}).join('');
    $('#in74').innerHTML='<p class="'+(pool.length?'g':'r')+'">"'+cls+'"'+(inf?'의 하위 개념을 모두 펼친':'만 그대로 쓴')+' 범위: '+(scope.join(', '))+'.</p>'+(bad?'<p class="r">규칙 위반! 현행 환불 규정이 둘이면 RAG가 3일과 7일을 섞어 답할 수 있습니다(4-5·6-5). 데이터를 넣기 전에 잡아야 합니다.</p>':'');}
  $('#tr74').addEventListener('click',function(e){var b=e.target.closest('[data-c]');if(!b)return;cls=b.dataset.c;$$('#tr74 [data-c]').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});run();});
  $('#inf74').addEventListener('click',function(){inf=!inf;this.setAttribute('aria-pressed',inf?'true':'false');run();});
  $('#alt74').addEventListener('click',function(){alts=!alts;this.setAttribute('aria-pressed',alts?'true':'false');run();});
  $('#bad74').addEventListener('click',function(){bad=!bad;this.setAttribute('aria-pressed',bad?'true':'false');run();});$('#q74').addEventListener('change',run);run();
})();
/* 7-5 */
(function(){var S=[['이번 달 결제 건수와 금액 합계는?','tab','정확한 집계라 표(SQL)가 맡습니다.'],['"화면이 어두워요" 같은 불만과 비슷한 문의 모아 줘','vec','말투가 다양한 "비슷한 것" 찾기입니다. 문의 날짜는 표로 함께 거릅니다.'],
  ['4K로 보면서 다운로드도 되는 요금제는 얼마?','graph','4K → 프리미엄 → 다운로드 → 가격, 여러 걸음 관계입니다. 입구는 좌표로 찾습니다.'],['긴장감 장르 영화의 리뷰 전부','ont','"긴장감 장르"는 표에 없는 범주라 온톨로지로 펼칩니다. 그 안의 검색은 좌표로.'],
  ['회원 1029번의 현재 요금제는?','tab','정확한 한 건 조회입니다.'],['"꿀잼", "존잼"도 "재미"로 묶어 세어 줘','ont','다른 이름(altLabel)을 한 개념으로 묶는 약속입니다.'],
  ['이 리뷰와 분위기가 비슷한 영화 추천','vec','뜻이 닮은 것을 찾는 일입니다(5-1).'],['LP-204가 주말에 뜨면 어디에 물어야 빨라?','graph','오류 → 문의 유형 → 상담 창구 → 운영 일정, 여러 걸음입니다.']],L={tab:'표 (SQL)',vec:'좌표 (벡터 DB)',graph:'지식 그래프',ont:'온톨로지'},ans={};
  $('#sc75').innerHTML=S.map(function(s,i){return '<div class="mission" data-i="'+i+'"><span class="st">질문 '+(i+1)+'</span><div><p><b>'+s[0]+'</b></p><div class="chips">'+['tab','vec','graph','ont'].map(function(k){return '<button class="bt" data-k="'+k+'" aria-pressed="false">'+L[k]+'</button>'}).join('')+'</div><p class="small fb" aria-live="polite"></p></div></div>'}).join('');
  function score(){var n=Object.keys(ans).length,ok=Object.keys(ans).filter(function(i){return ans[i]}).length;VL.kpis($('#k75'),[[ok+' / '+S.length,'맞힌 질문','g'],[n+'개','고른 질문','i']]);}
  $$('#sc75 .mission').forEach(function(m){var i=+m.dataset.i;$$('.bt',m).forEach(function(b){b.addEventListener('click',function(){$$('.bt',m).forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});var good=b.dataset.k===S[i][1];ans[i]=good;m.classList.toggle('ok',good);$('.fb',m).textContent=(good?'맞아요. ':'가장 먼저 꺼낼 도구는 "'+L[S[i][1]]+'". ')+S[i][2];score();});});});score();
})();
/* 대결 7 */
Duel({el:'#d7',run:function(){var f=0,r=0;G.mq.forEach(function(q){var h=VL.retrieve(CH,q.q,{k:2,alpha:.3,newest:true});if(q.docs.every(function(d){return h.some(function(x){return x.c.doc===d})}))f++;
    var g=VL.graphRAG(G,q.q,{hops:2});if(q.path.every(function(p){return g.nodes.indexOf(G.idx[p])>=0}))r++;});return {fly:f,robo:r}},scale:G.mq.length,fmt:function(v){return v+' / '+G.mq.length},bigGap:2,
  report:function(r){return '벡터만(조각 2개) '+r.fly+'개, GraphRAG(2걸음) '+r.robo+'개. 넘긴 글은 평균 '+'%d'+'자 대 '+'%d'+'자예요.'},
  verdict:{robo:'주판봇 승. 문서 두 개를 이어야 하는 질문에서는 관계를 따라가는 쪽이 빠짐없이 모읍니다. 다만 차이는 한 문제이고, 그래프를 만들고 고치는 비용은 이 점수에 들어 있지 않습니다. 한 문서로 답하는 질문이 대부분이라면 벡터만으로 충분합니다.',fly:'초파리 승.',draw:'무승부.'}});
''' % (R['graph7']['vec2']['chars'], R['graph7']['graph']['chars'])


def build_page():
    nav = [('#s1', '7-1 코사인'), ('#s2', '7-2 그래프'), ('#s3', '7-3 GraphRAG'), ('#s4', '7-4 온톨로지'), ('#s5', '7-5 함께'), ('#duel', '대결'), ('#sum', '정리')]
    cov = cover('cover_08', '벡터 DB 연구실 · 7장', '좌표와 관계 — 지식 그래프와 온톨로지', chars=(('doc', 'front'), ('asst', 'e01'), ('fly', 'point'), ('robo', 'happy')))
    hr = hero('벡터 DB 연구실 · 7장 · 코사인 유사도 실전, 지식 그래프, 온톨로지', '좌표와 관계',
              '좌표는 "닮음"만 안다. 관계와 약속은 어디에 두고, 벡터 DB와 어떻게 함께 쓸까?',
              '특강 둘째 날. 하루는 인턴들과 코사인 점수를 읽는 법부터 다시 짚고, 랩플릭스 안내 문서로 지식 그래프를 3D로 그리고, 온톨로지로 검색 범위를 정합니다.',
              [('%d개 · %d개' % (G7['nodes'], G7['edges']), '지식 그래프의 점 · 사실', 'i'), ('%d개' % G7['classes'], '온톨로지 클래스', 'm'),
               ('%d → %d개' % (G7['vec2']['ok'], G7['graph']['ok']), '여러 걸음 질문 %d개: 벡터만 → GraphRAG' % G7['mq'], 'g'), (num((CD['rel_med'] + CD['irr_med']) / 2, 2), '"재밌는 리뷰" 출발 문턱 (0.7이 아님)', 'a')],
              [('doc', 'front', '특강 둘째 날입니다. 좌표만으로는 부족한 곳, 오늘 채웁니다.'),
               ('asst', 'e16', '오늘은 3D 그래프가 나와요. 시아, 모아, 선 따라가기 준비됐죠?'),
               ('sia', 'smile', '노선도 같은 거죠? 자신 있어요.'), ('moa', 'report', '개념 나무도 그려 왔어요!')],
              crowd('"하루, 이제 완전 선생님이다." "오늘도 3D래!"', moods=('e16', 'e01', 'e04')))
    return build(P, title='7장 · 좌표와 관계 — 코사인 유사도 실전, 지식 그래프, 온톨로지 | 벡터 DB 연구실',
                 desc='코사인 점수 분포와 문턱, 지식 그래프 3D, 좌표로 입구를 찾고 관계를 따라가는 GraphRAG, 온톨로지로 검색 범위를 정하는 법을 실험으로 봅니다.',
                 nav=nav, cover_html=cov, hero=hr,
                 body=body() + footer([('지식 그래프·온톨로지 데이터', '랩플릭스 가상 안내 문서에서 사람이 뽑은 사실 (code/make_graph.py)'),
                                       ('GraphRAG', 'Edge 외 (2024) From Local to Global: A Graph RAG Approach to Query-Focused Summarization, arXiv:2404.16130'),
                                       ('지식 그래프 개관', 'Hogan 외 (2021) Knowledge Graphs, ACM Computing Surveys 54(4)'),
                                       ('RDF·OWL·SKOS', 'W3C 권고안 (RDF 1.1, OWL 2, SKOS Reference)'),
                                       ('지식 색인', '이 연구실 페이지 맨 아래의 #kg (ahnboat_lab_explainer 온톨로지)')],
                                      ['온톨로지와 지식 그래프는 설명용으로 작게 만들었습니다.', '"다른 모델 눈금"은 점수가 한쪽으로 몰리는 모델을 흉내 낸 가정입니다.', '질문 나누기 정답은 "가장 먼저 꺼낼 도구" 기준입니다.'],
                                      prev=('06_attention_3d.html', '6장 · LLM은 찾은 자료를 어떻게 읽나'), nxt=('practice/index.html', '마지막 장 · 실전 연습장')),
                 gloss=GLOSS, quizzes=QUIZ, page_js=JS, og='og_08')


if __name__ == '__main__':
    print(build_page())
