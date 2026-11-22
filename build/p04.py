# -*- coding: utf-8 -*-
"""4장 · 찾아서 답하는 AI — LLM과 RAG"""
from lib import *

P = '04_llm_rag.html'
RG = {(x['size'], x['alpha'], x['k']): x for x in R['rag']}; D4 = R['duel4']; LP = R['lp204']; BG = R['bigram']; BT = R['bigram_tot']


def body():
    b = three([
        ('무엇을', 'LLM(대형 언어 모델)이 "다음 말 잇기"로 답을 만든다는 것과 그 한계를 보고, 벡터 DB에서 근거를 찾아 붙여 주는 RAG를 여섯 걸음으로 직접 돌려 봅니다.'),
        ('왜 중요한가', 'LLM은 회사 안 문서나 최근 바뀐 규정을 모릅니다. 모르는 것도 그럴듯하게 지어냅니다(환각). RAG는 "찾아서, 근거와 함께 답하게" 해서 이 문제를 줄이는 가장 널리 쓰이는 방법입니다.'),
        ('업무에서는', '사내 규정 챗봇, 고객센터 자동 답변, 문서 요약을 만들 때 조각 크기·찾을 개수·글자 검색 섞기·날짜 필터를 어떻게 정할지 판단할 수 있습니다.')],
        '코드·수식을 몰라도 됩니다. 가상 OTT 서비스 「랩플릭스」의 고객 안내 문서 %d개와 질문 %d개로 실험합니다. LLM이 문장을 쓰는 부분은 미리 적어 둔 답으로 흉내 냅니다(찾는 부분은 실제로 계산).' % (R['n']['kb'], R['n']['ragq']),
        [('LLM', 'Large Language Model, 대형 언어 모델'), ('RAG', 'Retrieval-Augmented Generation, 검색 증강 생성'), ('BM25', '글자(낱말) 일치로 점수를 매기는 전통 검색 공식'),
         ('k', '찾아서 붙여 줄 문서 조각 수'), ('α', '알파, 뜻 점수와 글자 점수를 섞는 비율')])

    b += section('map', '큰 그림 — 이 장은 어디쯤인가',
                 '<div class="mapbar"><span>1장 · 표의 한계</span><i>→</i><span>2장 · 임베딩</span><i>→</i><span>3장 · 벡터 창고</span><i>→</i><span class="on">4장 · LLM과 RAG</span><i>→</i><span>5장 · 현장 사례</span></div>'
                 '<p>1~3장에서 만든 것(좌표, 창고, 메타데이터 필터)이 이 장에서 한 줄로 이어집니다. 목차의 "그림 아홉 개" 대응표 6번(작업 흐름)과 9번(RAG)이 이 장의 지도입니다.</p>'
                 '<div class="flowsteps" aria-label="RAG 여섯 걸음"><span>① 문서 넣기</span><span>② 잘게 쪼개기</span><span>③ 좌표 만들기·저장</span><span>④ 질문을 좌표로</span><span>⑤ 가까운 조각 k개 찾기</span><span>⑥ 조각을 붙여 LLM이 답하기</span></div>'
                 + say('doc', 'front', 'LLM(4-1) → RAG 여섯 걸음(4-2) → 쪼개는 크기(4-3) → 글자 검색 섞기(4-4) → 오래된 문서와 근거 확인(4-5) 순서로 갑니다.'))

    # ── 4-1 LLM
    s = say('doc', 'think', '상황 하나. 랩플릭스 고객센터에서 "챗봇 하나 만들어 주세요. ChatGPT 같은 걸 붙이면 끝 아닌가요?"라는 요청이 왔습니다. 정말 끝일까요?')
    s += duo(why([('문제 상황', '고객 질문에 사람처럼 문장으로 답하는 AI가 필요합니다.'),
                  ('앞 방법의 한계', '1~3장의 검색은 "가까운 리뷰 목록"을 줄 뿐, 답을 문장으로 써 주지 않습니다.'),
                  ('해법과 그 한계', 'LLM은 엄청난 양의 글로 "앞말 다음에 올 말"을 맞히도록 배워, 그럴듯한 문장을 이어 씁니다. 그러나 배운 글에 없던 것(우리 회사 요금, 지난달 바뀐 규정)은 모르고, 모를 때도 그럴듯하게 지어냅니다.')],
                 '책을 아주 많이 읽은 친구에게 "우리 회사 휴가 규정"을 물으면, 다른 회사 이야기를 섞어 자신 있게 답할 수 있습니다.'),
             mathbox('"다음 말 맞히기"를 숫자로 쓰면 어떻게 돼요?', '조건부 확률 (고등학교 확률과 통계) — "앞말이 A일 때 다음 말이 B일 확률"',
                     'P(다음 말 | 앞말) = (앞말 뒤에 그 말이 나온 횟수) ÷ (앞말이 나온 횟수)',
                     [('P( | )', '피, 조건부', '세로줄 오른쪽이 주어졌을 때 왼쪽의 확률'), ('앞말', '', '지금까지 쓴 말. 실제 LLM은 앞말 수천 토큰을 한꺼번에 봄'), ('횟수', '', '배운 글에서 센 값')],
                     '이 연구실 리뷰에서 "연기" 뒤에 온 말을 세면 모두 %d번, 그중 "차력쇼"가 %d번입니다. P(차력쇼 | 연기) = %d ÷ %d ≈ <b>%s</b>. 다음 말로 "차력쇼"를 가장 먼저 고릅니다.' % (BT['연기'], BG['연기'][0][1], BG['연기'][0][1], BT['연기'], pct(BG['연기'][0][1] / BT['연기'])),
                     '자주 나온 말을 고를 뿐이니까, 사실인지는 따지지 않는 거네요. 그래서 그럴듯한 거짓말이 나오는군요!'))
    s += talk([('asst', 'e15', '시아, LLM한테 "랩플릭스 프리미엄 요금이 얼마야?"라고 물으면 맞힐까?'),
               ('sia', 'think', 'LLM은 똑똑하니까… 알지 않을까요?'),
               ('robo', 'wow', '큰 모델은 세상 모든 걸 알아! 질문만 넣으면 끝!'),
               ('fly', 'point', '랩플릭스는 이 연구실이 만든 가상 회사야. 배운 글에 있을 리가 없지. 아래 "LLM 혼자 답하기"를 눌러 봐.'),
               ('asst', 'report', '"월 15,900원"이라고 자신 있게 답했어요. 안내 문서에는 17,000원이에요…')])
    s += crowd('"하루, 여기서 긴장 다시 올라온 거 같아." "LLM 이야기는 어렵지…" "그래도 차근차근 잘하네."', moods=('e15', 'e02', 'e13'))
    s += panel('p41', '실험 · 아주 작은 언어 모델과 "LLM 혼자 답하기"', '리뷰로 센 두 낱말 빈도 · 답은 흉내',
               '<h4>① 리뷰 %d개로 만든 아주 작은 언어 모델 — 앞 낱말 하나만 보고 다음 낱말 고르기</h4>' % R['n']['reviews'] +
               '<div class="ctrl"><div class="group"><span class="glabel">첫 낱말</span><select class="sel" id="w41"></select></div>'
               '<div class="group"><span class="glabel">고르는 법</span><button class="bt" data-m="top" aria-pressed="true">가장 자주 나온 말</button><button class="bt" data-m="rand" aria-pressed="false">확률대로 뽑기</button></div>'
               '<div class="group"><button class="bt primary" id="go41">이어 쓰기</button></div></div>'
               '<div class="grid2"><div><h4>다음 말 후보와 확률</h4><div class="vbars" id="vb41"></div></div><div><h4>이어 쓴 문장</h4><p class="ansbox" id="out41"></p></div></div>'
               '<h4 style="margin-top:16px">② LLM 혼자 답하기 (흉내) — 랩플릭스 질문</h4><div class="chips" id="q41"></div><div id="a41"></div>', real=True)
    s += explain(['언어 모델은 앞말이 주어졌을 때 다음 말의 확률을 배우고, 그 확률대로 한 말씩 이어 씁니다. 실제 LLM은 앞말 수천 토큰을 한꺼번에 보고, 수십억~수천억 개의 숫자(가중치)로 그 확률을 계산합니다.',
                  '"자주 나온 말"은 "사실인 말"과 다릅니다. 배운 글에 없던 랩플릭스 요금을 물으면, 요금 이야기에 흔히 나오는 숫자 모양을 그럴듯하게 이어 씁니다(환각).',
                  '해결책은 두 가지입니다. ① 우리 문서로 모델을 다시 학습시키기(파인튜닝, 비싸고 문서가 바뀌면 또 해야 함) ② 질문할 때마다 관련 문서를 찾아 붙여 주기(RAG, 이 장의 주제).'],
                 '이 아주 작은 모델은 낱말 둘의 빈도만 세었습니다. 실제 LLM의 능력과는 규모가 전혀 다르지만, "확률이 높은 말을 잇는다"는 원리는 같습니다. ②의 LLM 답은 미리 적어 둔 흉내입니다.')
    s += bridge('gen', '생성 AI로 치면', 'ChatGPT·Claude·Gemini 같은 LLM이 문장을 만드는 원리가 이 "다음 말 잇기"입니다. 그 뒤에 사람의 피드백 등으로 대화에 맞게 다듬습니다.',
                '실제 LLM은 학습한 내용 일부를 "기억"하지만, 어디서 배웠는지 출처를 대지 못하고, 학습 뒤에 생긴 일은 모릅니다.')
    s += wrapup('LLM은 말을 잘 잇지만, 모르는 것을 모른다고 말하지 않을 수 있습니다. 그래서 "근거를 찾아서 붙여 주는" 단계가 필요합니다.')
    s += quiz('q41')
    b += step('s1', '4-1', 'LLM은 다음 말을 잇는다 — 그리고 우리 회사 일은 모른다', ['방법: 언어 모델 · 다음 말 예측', '일상: 책 많이 읽은 친구'], s)

    # ── 4-2 RAG 여섯 걸음
    s = say('doc', 'think', 'LLM이 모르는 건 우리 문서에 다 있습니다. 시험 볼 때 교과서를 펴 놓게 해 주면 어떨까요? 그것도 딱 필요한 쪽만 펴서요.')
    s += duo(why([('문제 상황', '회사 문서에 근거한 정확한 답이 필요합니다. 문서는 자주 바뀝니다.'),
                  ('앞 방법의 한계', 'LLM 혼자는 환각을 일으키고, 문서로 다시 학습시키는 일은 비싸고 느립니다.'),
                  ('해법', 'RAG: 문서를 조각내 좌표로 저장해 두고(①~③), 질문이 오면 가까운 조각 k개를 찾아(④~⑤), "이 자료로만 답하고 없으면 모른다고 하라"는 지시와 함께 LLM에게 넘깁니다(⑥).')],
                 '오픈북 시험입니다. 다만 책 전체가 아니라, 문제와 관련된 쪽을 사서가 골라 펼쳐 줍니다.'),
             pair('대응표 9번 그림(RAG)에서는', '문서 → 쪼개기 → 임베딩 → 벡터 DB → 질문 → 가까운 조각 k개 → LLM(찾은 자료와 함께) → 답. 마지막 줄: "벡터 DB는 자료를 찾고, LLM은 그 자료로 더 정확한 답을 만든다."',
                  '이 연구실에서는', '랩플릭스 안내 문서 %d개(요금제, 환불, 해지, 오류 코드 등)를 조각내 교육용 임베딩으로 저장했습니다. 찾기는 실제 계산, 답 쓰기는 "찾은 자료에 정답 문구가 있으면 그 자료로 쓴 답"을 보여 주는 흉내입니다.' % R['n']['kb']))
    s += talk([('asst', 'e15', '모아, RAG 여섯 걸음을 순서대로 말해 볼래?'),
               ('moa', 'report', '문서 넣기, 쪼개기, 좌표 만들어 저장하기, 질문을 좌표로, 가까운 조각 찾기, 붙여서 답하기!'),
               ('robo', 'happy', '자료만 붙이면 환각 끝! RAG 만세!'),
               ('fly', 'point', '찾은 자료가 엉뚱하면? 아래에서 "랩플릭스 회사 주가는 얼마야?"를 눌러 봐. 자료에 없는 질문이야.'),
               ('asst', 'report', '"%s" 조각을 %s점으로 찾아왔어요. 문턱보다 높아서 엉뚱한 답을 쓸 뻔했어요.' % (R['stock_q']['top'], num(R['stock_q']['s'], 2)))])
    s += panel('p42', '실험 · RAG 시뮬레이터 — 찾고, 붙이고, 답하기', '가상 안내 문서 · 찾기는 실제 계산, 답 쓰기는 흉내',
               '<div class="chips" id="qs42" aria-label="질문 고르기"></div>'
               '<div class="ctrl"><div class="group"><span class="glabel">직접 질문</span><input type="text" class="wide" id="t42" placeholder="예: 학생 할인 받으려면 뭐가 필요해?" aria-label="직접 질문"></div></div>'
               '<div class="ctrl"><div class="group"><span class="glabel">찾을 조각 수 k</span><input type="range" id="k42" min="1" max="5" value="3" aria-label="k"><span class="val" id="kv42"></span></div>'
               '<div class="group"><span class="glabel">근거 문턱</span><input type="range" id="th42" min="0" max="80" value="35" aria-label="근거 문턱"><span class="val" id="thv42"></span></div></div>'
               '<p class="small muted">이 시뮬레이터는 문서를 250자 조각(이 짧은 문서들은 거의 문서 하나가 조각 하나)으로 넣고 뜻 점수만으로 찾습니다. 조각 크기와 글자 검색 섞기는 4-3·4-4에서 바꿔 봅니다.</p><div class="flowsteps" id="fl42"></div><div class="grid2"><div><h4>⑤ 찾은 조각 (점수 = 뜻 점수)</h4><ul class="res" id="rs42"></ul></div>'
               '<div><h4>⑥ LLM에게 넘기는 글 (프롬프트)</h4><div class="prompt" id="pr42"></div></div></div>'
               '<div class="grid2"><div><h4>RAG 답 (자료를 읽고 쓴 답 · 흉내)</h4><div class="ansbox" id="an42"></div></div><div><h4>LLM 혼자 답 (흉내)</h4><div class="ansbox bad" id="lo42"></div></div></div>'
               '<section class="kpis" id="k42" aria-label="숫자 요약"></section>', real=True)
    s += explain(['④ 질문을 같은 임베딩으로 좌표로 바꾸고, ⑤ 조각들과 코사인을 재서 위에서 k개를 고릅니다. 점수가 "근거 문턱"보다 낮은 조각은 버립니다.',
                  '⑥ 프롬프트에는 "자료로만 답하라, 없으면 모른다고 하라"는 지시, 찾은 조각(제목·날짜와 함께), 질문이 들어갑니다. 출처를 함께 넣어야 답에 근거를 달 수 있습니다.',
                  '문턱이 너무 낮으면 엉뚱한 조각으로 답을 지어내고(주가 질문), 너무 높으면 답할 수 있는 질문에도 "모릅니다"라고 합니다.'],
                 'RAG는 "찾기"가 틀리면 답도 틀립니다. 그리고 LLM이 지시를 어기고 자료 밖 내용을 섞을 수도 있습니다. 이 페이지의 답 쓰기는 흉내라 그 위험은 보여 주지 못합니다.')
    s += aicheck('주가를 물었는데 엉뚱한 근거가?',
                 ('<p>근거 문턱이 기본값(0.35)일 때 "랩플릭스 회사 주가는 얼마야?"를 물으면, RAG가 "%s" 조각을 근거로 들고 옵니다(점수 약 %s). 그 조각의 금액·할인율 같은 숫자를 LLM이 주가처럼 쓸 위험이 있습니다.</p>' % (R['stock_q']['top'], num(R['stock_q']['s'], 2))) +
                 '<p><b>확인 질문</b> ① 이 근거는 질문에 맞는 근거일까요? ② 사람이 답을 내보내기 전에 무엇을 확인하면 될까요?</p>'
                 '<details><summary>생각해 본 뒤 열어 보기</summary><p>① 아닙니다. "회사"(일)와 "얼마"(요금) 같은 말 때문에 가깝게 나왔을 뿐, 주가와는 무관합니다. '
                 '② 답에 붙은 출처 조각을 열어, 질문의 핵심(주가)이 정말 거기 있는지 봅니다. 출처가 질문과 어긋나면 "모릅니다"가 맞는 답입니다.</p></details>')
    s += codefold([('hits = vector_db.query(embed(question), k=3)', '⑤ 질문 좌표로 가까운 조각 3개 찾기'),
                   ('prompt = SYSTEM + "\\n".join(h.text for h in hits) + question', '⑥ 지시 + 찾은 조각 + 질문을 이어 붙이기'),
                   ('answer = llm.generate(prompt)', 'LLM이 자료를 읽고 답을 씁니다')])
    s += wrapup('RAG는 "검색 + 생성"입니다. 검색이 좋은 근거를 가져오고, 생성이 그 근거로만 답하게 하는 것이 핵심입니다. 이제 검색 쪽 손잡이를 하나씩 봅니다.')
    s += quiz('q42')
    b += step('s2', '4-2', 'RAG의 여섯 걸음 — 찾아서 붙여 주고 답하게 하기', ['방법: 검색 증강 생성(RAG)', '일상: 오픈북 시험'], s)

    # ── 4-3 청킹
    a80, a150, a250 = RG[(80, .5, 3)], RG[(150, .5, 3)], RG[(250, .5, 3)]
    s = say('doc', 'think', '문서를 통째로 창고에 넣을까요, 문장 하나씩 넣을까요? 조각의 크기가 답의 질을 바꿉니다.')
    s += duo(why([('문제 상황', '문서 하나에는 여러 이야기가 섞여 있습니다. 질문과 맞는 부분만 정확히 찾아 넘겨야 합니다.'),
                  ('앞 방법의 한계', '문서 통째로는 좌표가 여러 뜻의 평균이 되어 흐려지고, LLM에게 넘기는 글도 길어집니다. 너무 잘게 자르면 답에 필요한 앞뒤 문장이 잘립니다.'),
                  ('해법', '목표 글자 수까지 문장을 모아 조각을 만들고(청킹), 경계에서 문장 하나를 겹쳐(오버랩) 앞뒤 맥락이 끊기지 않게 합니다. 크기는 실험으로 정합니다.')],
                 '요리책을 쪽 단위로 찢어 두면 필요한 쪽만 꺼내기 쉽습니다. 한 줄씩 자르면 재료와 순서가 따로 놀고, 책을 통째로 주면 찾는 데 오래 걸립니다.'),
             mathbox('조각 크기를 키우면 LLM에게 넘기는 글은 얼마나 늘어요?', '곱셈 — 개수 × 크기',
                     '넘기는 글자 수 ≈ 찾을 조각 수 k × 조각 크기',
                     [('k', '케이', '붙여 줄 조각 수'), ('조각 크기', '', '목표 글자 수 (문장 단위로 끊어서 조금씩 다름)'), ('글자 수', '', 'LLM 비용·속도와 비례 (실제로는 토큰 수)')],
                     'k = 3, 조각 150자면 약 3 × 150 = 450자를 목표로 하지만, 문장 단위로 끊어 실제 평균은 <b>%s자</b>입니다. 조각 80자면 평균 %s자, 250자면 %s자입니다.' % (num(a150['tokens']), num(a80['tokens']), num(a250['tokens'])),
                     '크게 자르면 정답률은 오르는데 넘기는 글도 늘어요. 공짜가 아니네요!'))
    s += talk([('asst', 'e20', '시아, 조각을 아주 잘게, 한 문장씩 자르면 어떨까?'),
               ('sia', 'explain', '찾기는 정확해질 것 같아요. 그런데 "3일 이내"와 "재생하지 않았다면"이 다른 조각으로 갈라지면…'),
               ('robo', 'chart', '그럼 문서 통째로 넣자. 다 들어 있으니 무조건 정답!'),
               ('fly', 'point', '아래 막대에서 크기를 80, 150, 250으로 바꿔 가며 정답률과 넘기는 글자 수를 같이 봐.'),
               ('asst', 'report', '80자면 정답률 %s, 150자면 %s, 250자면 %s예요. 넘기는 글은 %s자 → %s자 → %s자로 늘고요.' % (pct(a80['acc'], 0), pct(a150['acc'], 0), pct(a250['acc'], 0), num(a80['tokens']), num(a150['tokens']), num(a250['tokens'])))])
    s += panel('p43', '실험 · 조각 크기 실험실 — 질문 %d개로 채점' % R['n']['ragq'], '가상 안내 문서 · 페이지가 직접 계산',
               '<div class="ctrl"><div class="group"><span class="glabel">조각 크기</span><input type="range" id="sz43" min="60" max="400" step="10" value="150" aria-label="조각 크기"><span class="val" id="szv43"></span></div>'
               '<div class="group"><span class="glabel">문장 겹치기</span><button class="bt" id="ov43" aria-pressed="false">경계에서 한 문장 겹치기</button></div>'
               '<div class="group"><span class="glabel">k</span><input type="range" id="k43" min="1" max="5" value="3" aria-label="k"><span class="val" id="kv43"></span></div></div>'
               + canvas('cv43', 230, '문서 12개를 조각으로 나눈 모습') + canvas('cv43b', 240, '조각 크기에 따른 정답률과 넘기는 글자 수 곡선') +
               '<section class="kpis" id="k43" aria-label="채점"></section><div class="insight" id="in43" aria-live="polite"></div>', real=True)
    s += explain(['조각이 작으면 좌표가 한 가지 뜻에 가까워 찾기는 날카롭지만, 답에 필요한 앞뒤 문장이 다른 조각으로 갈라질 수 있습니다.',
                  '조각이 크면 답이 한 조각 안에 들어갈 가능성이 높지만, 여러 뜻이 섞여 좌표가 흐려지고 LLM에게 넘기는 글이 늘어 비용과 시간이 듭니다.',
                  '이 문서들은 짧아서 250자 이상에서는 문서 하나가 통째로 조각 하나가 됩니다. 실제 문서는 훨씬 길어서, 보통 수백 토큰 크기와 약간의 겹침으로 시작해 실험으로 조정합니다.'],
                 '정답률은 질문 %d개로 잰 작은 숫자라 한두 문제에 크게 흔들립니다. 실제로는 질문 수백 개짜리 평가 묶음을 따로 만들어 잽니다.' % R['n']['ragq'])
    s += codefold([('RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)', '글자 수와 겹침으로 문서를 쪼개는 흔한 도구 설정 (LangChain)')])
    s += wrapup('조각 크기는 "찾기의 날카로움"과 "답에 필요한 맥락" 사이의 맞바꿈입니다. 정답은 데이터와 질문에 달렸으니, 질문 묶음을 만들어 재 보고 정합니다.')
    s += quiz('q43')
    b += step('s3', '4-3', '쪼개는 크기 — 청킹', ['설정: 조각 크기 · 겹침 · k', '일상: 요리책 쪽 단위'], s)

    # ── 4-4 하이브리드
    e503, e204 = LP[0], LP[1]
    s = say('doc', 'think', '실제로 있었던(가상의) 일. 고객이 "LP-204 오류가 떠요"라고 물었는데, 챗봇이 LP-503(서버 점검) 안내를 내밀었습니다. 무엇이 잘못됐을까요?')
    s += duo(why([('문제 상황', '오류 코드, 상품 코드, 사람 이름처럼 "글자 그대로"가 중요한 질문이 있습니다.'),
                  ('앞 방법의 한계', '임베딩은 LP-204와 LP-503을 모두 "오류"로 읽어 구별하지 못합니다(1장 특징 ⑥ 사전에 없는 말). 이 조각에서는 오류 이야기만 있는 LP-503 쪽이 뜻 점수가 더 높습니다.'),
                  ('해법', '글자 일치 검색(BM25)의 점수를 뜻 점수와 섞습니다(하이브리드 검색). 섞는 비율 α를 실험으로 정합니다.')],
                 '사람 이름으로 책을 찾을 때는 제목 글자 검색이, "우울할 때 읽을 책"을 찾을 때는 뜻 검색이 낫습니다. 도서관은 둘 다 씁니다.'),
             mathbox('뜻 점수랑 글자 점수를 어떻게 섞어요?', '가중 평균 (중학교) — 비율을 정해 두 점수를 섞기',
                     '섞은 점수 = α × 뜻 점수 + (1 − α) × 글자 점수',
                     [('α', '알파', '뜻 점수의 몫 (0~1). 1이면 뜻만, 0이면 글자만'), ('뜻 점수', '', '임베딩 코사인'), ('글자 점수', '', 'BM25 점수를 0~1로 줄인 값')],
                     '질문 "LP-204 오류가 떠요". LP-503 조각: 뜻 %s, 글자 %s. LP-204 조각: 뜻 %s, 글자 %s. '
                     'α = 1이면 LP-503(%s)이 1등. α = 0.3이면 LP-503 = 0.3×%s + 0.7×%s ≈ <b>%s</b>, LP-204 = 0.3×%s + 0.7×%s ≈ <b>%s</b>로 LP-204가 1등입니다.' % (
                         num(e503['vec'], 2), num(e503['bm'], 2), num(e204['vec'], 2), num(e204['bm'], 2), num(e503['vec'], 2),
                         num(e503['vec'], 2), num(e503['bm'], 2), num(.3 * e503['vec'] + .7 * e503['bm'], 3), num(e204['vec'], 2), num(e204['bm'], 2), num(.3 * e204['vec'] + .7 * e204['bm'], 3)),
                     '글자 점수를 조금 섞으니까 코드가 정확히 맞는 조각이 올라왔어요!'))
    s += talk([('asst', 'e15', '모아, 1장에서 버렸던 글자 검색을 다시 꺼내 써도 될까?'),
               ('moa', 'think', '1장에선 글자 검색이 뜻을 놓쳤지만… 코드는 글자 그대로가 중요하니까 될 것 같아요.'),
               ('robo', 'coin', '구식 글자 검색을 왜 섞어? 최신 벡터 검색이면 충분해!'),
               ('fly', 'point', 'α 막대를 1에서 0까지 내려 보면서, 오른쪽 곡선에서 질문 %d개 정답률이 어디서 가장 높은지 봐.' % R['n']['ragq']),
               ('asst', 'report', 'k = 1일 때 뜻만(α=1) %d개, 섞기(α=0.3) %d개, 글자만(α=0) %d개 맞혀요. 가운데가 가장 좋아요.' % (D4['vec_right'], D4['hyb_right'], round(RG[(150, 0, 1)]['acc'] * R['n']['ragq'])))])
    s += panel('p44', '실험 · 하이브리드 검색 — 뜻과 글자를 섞는 비율', '가상 안내 문서 · 페이지가 직접 계산',
               '<div class="ctrl"><div class="group"><span class="glabel">질문</span><select class="sel" id="q44"></select></div>'
               '<div class="group"><span class="glabel">뜻 점수 몫 α</span><input type="range" id="al44" min="0" max="100" step="10" value="100" aria-label="알파"><span class="val" id="alv44"></span></div>'
               '<div class="group"><span class="glabel">k</span><button class="bt" data-k="1" aria-pressed="true">1</button><button class="bt" data-k="3" aria-pressed="false">3</button></div></div>'
               '<div class="grid2"><div><div class="tw"><table class="tb mini-table" id="t44"></table></div></div><div>' + canvas('cv44', 240, 'α에 따른 질문 16개 정답률 곡선') + '</div></div>'
               '<section class="kpis" id="k44" aria-label="채점"></section><div class="insight" id="in44" aria-live="polite"></div>', real=True)
    s += explain(['뜻 점수는 "환불"과 "돈 돌려받기"를 잇고, 글자 점수는 "LP-204"와 "베트남어"처럼 글자 그대로를 잡습니다. 섞으면 서로의 빈틈을 메웁니다.',
                  '이 질문 묶음에서는 k = 1일 때 α 0.3 근처가 가장 좋았습니다. k = 3이면 위 3개 안에 정답 조각이 들어가기 쉬워 차이가 줄어듭니다.',
                  '현장에서는 섞은 뒤 위 몇십 개를 더 정밀한 모델로 다시 줄 세우는 재정렬(re-ranking)을 덧붙이기도 합니다.'],
                 'α의 가장 좋은 값은 데이터와 질문 종류에 따라 다릅니다. 코드·이름이 많은 질문이면 글자 쪽, 말투가 다양한 질문이면 뜻 쪽으로 기웁니다.')
    s += codefold([('score = alpha * cosine(q, c) + (1 - alpha) * bm25_norm(q, c)', '섞은 점수 계산'),
                   ('reciprocal_rank_fusion([vector_hits, keyword_hits])', '점수 대신 순위로 섞는 방법(RRF)도 많이 씁니다')])
    s += wrapup('글자 검색은 낡은 것이 아니라 다른 일을 잘하는 도구입니다. 뜻과 글자를 섞으면 RAG의 찾기가 단단해집니다.')
    s += quiz('q44')
    b += step('s4', '4-4', '글자 검색과 섞기 — 하이브리드 검색', ['방법: BM25 + 임베딩 · 가중 평균', '일상: 제목 검색과 주제 검색'], s)

    # ── 4-5 오래된 문서와 근거 확인
    s = say('doc', 'think', '마지막 함정. 환불 규정이 7월에 바뀌었는데, 창고에는 옛 규정 문서도 남아 있습니다. 고객이 "어제 결제했는데 안 봤어요, 환불되나요?"라고 묻는다면?')
    s += duo(why([('문제 상황', '같은 주제의 문서가 여러 판(버전)으로 남아 있고, 내용이 서로 다릅니다.'),
                  ('앞 방법의 한계', '뜻 점수는 "어느 판이 최신인가"를 모릅니다. 옛 문서가 위로 올라오면 LLM은 그대로 옛 규정을 답합니다.'),
                  ('해법', '메타데이터(작성일·버전·폐기 여부)로 먼저 거르고(3장), 답에 출처와 날짜를 달게 하고, 사람이 출처를 확인할 수 있게 합니다.')],
                 '개정된 교과서와 옛 교과서가 한 책꽂이에 섞여 있으면, 표지의 연도를 먼저 봐야 합니다.'),
             pair('구버전 (2025-03)', '"결제 후 7일 이내이고 재생하지 않았다면 전액 환불. 2026년 6월 30일까지 적용."',
                  '현행 (2026-07)', '"결제 후 3일 이내이고 한 편도 재생하지 않았다면 전액 환불. 재생했다면 남은 기간만큼 일할 계산."'))
    s += talk([('asst', 'e15', '시아, 옛 문서랑 새 문서가 둘 다 찾아지면 LLM은 어느 걸 믿을까?'),
               ('sia', 'think', '둘 다 자료니까… 헷갈려서 섞어 답할 것 같아요.'),
               ('robo', 'coin', '많이 찾을수록 좋은 거 아냐? 다 붙여 줘!'),
               ('fly', 'point', '아래에서 "구버전 함께 넣기"를 켜고 "날짜 필터"를 껐다 켜 봐. 찾은 조각의 날짜를 확인해.'),
               ('asst', 'report', '필터가 꺼져 있으면 "환불 규정(구버전)"이 같이 올라와요. 7일과 3일이 한 프롬프트에 섞여요.')])
    s += panel('p45', '실험 · 오래된 문서와 근거 확인 점검표', '가상 안내 문서 · 페이지가 직접 계산',
               '<div class="ctrl"><div class="group"><span class="glabel">질문</span><select class="sel" id="q45"><option>어제 결제했는데 아무것도 안 봤어요. 돈 돌려받을 수 있나요?</option><option>환불 신청은 어디서 해요?</option><option>해지하면 바로 못 보게 되나요?</option></select></div></div>'
               '<div class="ctrl"><div class="group"><button class="bt" id="old45" aria-pressed="true">구버전 문서도 창고에 함께 넣기</button><button class="bt" id="new45" aria-pressed="false">날짜 필터: 최신 판만</button></div></div>'
               '<ul class="res" id="rs45"></ul><div id="ck45"></div><div class="insight" id="in45" aria-live="polite"></div>', real=True)
    s += explain(['구버전 문서를 지우지 못하는 경우(감사 기록 등)가 많습니다. 그래서 창고에는 남겨 두되 "폐기됨·적용 기간" 메타데이터로 거르는 것이 기본입니다.',
                  '답에 출처 조각의 제목과 날짜를 함께 보여 주면, 고객과 상담원이 근거를 바로 확인할 수 있습니다.',
                  '개인정보나 사내 기밀 문서는 질문한 사람에게 볼 권한이 있는 조각만 찾도록, 권한 정보도 메타데이터로 함께 겁니다.'],
                 '이 점검표는 기본 중의 기본입니다. 실제 서비스에서는 답의 정확도·근거 일치도를 질문 묶음으로 정기적으로 다시 재고, 문서가 바뀌면 창고도 다시 만듭니다.')
    s += wrapup('RAG의 실패는 대부분 "찾기"에서 납니다. 최신 판만, 권한 있는 것만, 출처와 함께. 이 세 가지를 메타데이터로 지키면 환각이 크게 줄어듭니다.')
    s += quiz('q45')
    b += step('s5', '4-5', '오래된 문서와 근거 확인 — RAG의 함정 피하기', ['방법: 날짜·버전 필터 · 출처 표시', '일상: 개정판 교과서'], s)

    b += duel('d4', '랩플릭스 질문 %d개, 조각 1개만 붙여 답하기 — 뜻만 검색 vs 뜻 + 글자 섞기' % R['n']['ragq'], '하이브리드 (α = 0.3, 뜻 3 : 글자 7)', '벡터만 (α = 1, 뜻 점수만)',
              '"코드랑 고유명사는 글자 그대로가 중요해. 구식이라도 섞자."', '"최신은 벡터 검색이야. 글자 검색은 1장에서 졌잖아!"',
              '질문 %d개 중 맞힌 수 (조각 150자, k = 1, 근거 문턱 0.35, 최신 판만)' % R['n']['ragq'])

    b += section('sum', '정리 — RAG 손잡이 점검표',
                 '<div class="tw"><table class="tb"><tr><th>손잡이</th><th>너무 작으면</th><th>너무 크면</th><th>이 장의 결과</th></tr>'
                 '<tr><td>조각 크기</td><td>답에 필요한 맥락이 잘림</td><td>뜻이 흐려지고 넘기는 글이 늚</td><td>k=3에서 80자 %s → 150자 %s → 250자 %s</td></tr>'
                 '<tr><td>k (붙일 조각 수)</td><td>정답 조각을 놓침</td><td>엉뚱한 조각이 섞이고 비용 증가</td><td>150자·α 0.5에서 k=1 %s → k=3 %s</td></tr>'
                 '<tr><td>α (뜻 몫)</td><td>말투가 다른 질문을 놓침</td><td>코드·고유명사를 놓침</td><td>k=1에서 α=1 %d개 → α=0.3 %d개 맞힘</td></tr>'
                 '<tr><td>근거 문턱</td><td>엉뚱한 근거로 지어냄</td><td>답할 수 있는 것도 "모릅니다"</td><td>주가 질문의 1위 점수 %s</td></tr>'
                 '<tr><td>날짜·버전 필터</td><td colspan="2">끄면 옛 규정과 새 규정이 섞임</td><td>구버전 문서가 함께 찾아짐: %s</td></tr></table></div>' % (
                     pct(a80['acc'], 0), pct(a150['acc'], 0), pct(a250['acc'], 0), pct(RG[(150, .5, 1)]['acc'], 0), pct(RG[(150, .5, 3)]['acc'], 0),
                     D4['vec_right'], D4['hyb_right'], num(R['stock_q']['s'], 2), '예' if R['old_doc']['retrieved_old'] else '아니오')
                 + bridge('gen', '생성 AI로 치면', 'ChatGPT·Claude 같은 서비스의 "파일 올려서 묻기", "웹 검색해서 답하기"도 넓게 보면 RAG입니다. 찾은 자료를 붙여서 답하게 합니다.',
                          '서비스마다 쪼개기·검색·문턱 설정이 다르고 밖에서 보이지 않습니다. 중요한 답은 붙은 출처를 직접 열어 확인해야 합니다.'))

    b += outro([('doc', 'front', '오늘 세 줄 정리. ① LLM은 다음 말을 잇는 기계라 모르는 것도 그럴듯하게 쓴다. ② RAG는 벡터 DB에서 근거를 찾아 붙여 "자료로만" 답하게 한다. ③ 조각 크기·k·α·문턱·날짜 필터를 질문 묶음으로 재 보고 정한다.'),
                ('fly', 'arms', '구식 글자 검색이 결승골을 넣었지. 도구는 신구가 아니라 쓰임새야.'),
                ('robo', 'sigh', '벡터만 믿었는데… 섞는 게 정답이었네. 그래도 RAG 만세는 취소 안 해.'),
                ('sia', 'proud', 'RAG 점검표, 실전 연습장 가기 전에 한 번 더 볼게요.'),
                ('moa', 'sparkle', '노트에 "옛 문서는 지우지 말고 메타데이터로 거른다" 적었어요!'),
                ('asst', 'e16', '제일 어려운 장이었는데 끝까지 왔어요. 다음 장은 진짜 현장 사례예요!')],
               '랩플릭스 고객센터 모니터 앞에서 하루가 인턴들에게 RAG 흐름도를 가리키는 장면',
               crowd('"하루, LLM 설명까지 해냈어!" "이제 진짜 선생님이네."', moods=('e16', 'e01', 'e16')))
    return b


GLOSS = {
    'LLM': ['대형 언어 모델 (LLM)', '아주 많은 글로 "다음 말 맞히기"를 배운 모델. ChatGPT·Claude·Gemini 등이 이를 바탕으로 합니다.'],
    '환각': ['환각 (hallucination)', 'LLM이 사실이 아닌 내용을 그럴듯하게 지어내는 현상.'],
    'RAG': ['검색 증강 생성 (RAG)', '질문과 관련된 문서 조각을 찾아 LLM에게 함께 넘겨, 그 자료로 답하게 하는 방법.'],
    '프롬프트': ['프롬프트 (prompt)', 'LLM에게 넘기는 글 전체. 지시, 자료, 질문이 들어갑니다.'],
    '토큰': ['토큰 (token)', 'LLM이 글을 다루는 조각 단위. 낱말이나 낱말 일부. 비용과 길이 제한이 토큰으로 계산됩니다.'],
    '청킹': ['청킹 (chunking)', '긴 문서를 검색하기 좋은 크기의 조각으로 나누는 일.'],
    '파인튜닝': ['파인튜닝 (fine-tuning)', '이미 학습된 모델을 우리 데이터로 조금 더 학습시키는 일. 비용이 들고, 문서가 바뀌면 다시 해야 합니다.'],
    'BM25': ['BM25', '질문 낱말이 문서에 얼마나 자주, 얼마나 드물게 나오는지로 점수를 매기는 전통 검색 공식.'],
    '하이브리드 검색': ['하이브리드 검색', '글자 일치 점수와 뜻 점수를 섞어 쓰는 검색.'],
    '재정렬': ['재정렬 (re-ranking)', '먼저 찾은 몇십 개를 더 정밀한 모델로 다시 줄 세우는 단계.'],
    '조건부 확률': ['조건부 확률', '어떤 일이 일어났다는 조건에서 다른 일이 일어날 확률. P(B | A).'],
}

QUIZ = {
    'q41': [{'q': 'LLM이 가상 회사 랩플릭스의 요금을 틀리게 답한 가장 큰 이유는?', 'o': ['계산을 잘못해서', '배운 글에 그 정보가 없는데도 그럴듯한 말을 이어서', '질문이 짧아서'], 'a': 1,
             'why': 'LLM은 자주 나온 말을 잇습니다. 배운 글에 없는 사내 정보는 모르고, 모를 때도 그럴듯한 숫자를 지어냅니다.', 'hint': '"자주 나온 말"과 "사실인 말"의 차이.'},
            {'q': '"연기" 뒤에 온 말 29번 중 "차력쇼"가 17번이면 P(차력쇼 | 연기)는?', 'o': ['약 17%', '약 59%', '약 29%'], 'a': 1,
             'why': '17 ÷ 29 ≈ 0.586, 약 59%.', 'hint': '나온 횟수 ÷ 앞말이 나온 횟수'}],
    'q42': [{'q': 'RAG에서 "근거 문턱"을 너무 낮추면?', 'o': ['답할 수 있는 질문에도 모른다고 한다', '엉뚱한 조각을 근거로 답을 지어낸다', '아무 변화 없다'], 'a': 1,
             'why': '점수가 낮은 엉뚱한 조각도 통과해 LLM에게 넘어갑니다(주가 질문).', 'hint': '"랩플릭스 주가" 질문을 떠올려 보세요.'},
            {'q': '프롬프트에 찾은 조각의 제목·날짜를 함께 넣는 이유는?', 'o': ['글자 수를 늘리려고', '답에 출처를 달아 사람이 확인할 수 있게', '임베딩을 바꾸려고'], 'a': 1,
             'why': '출처가 있어야 답이 어디서 왔는지 확인하고, 틀린 근거를 걸러 낼 수 있습니다.', 'hint': 'AI 판단 코너의 확인 방법.'}],
    'q43': [{'q': '조각을 너무 잘게 자를 때의 위험은?', 'o': ['답에 필요한 앞뒤 문장이 다른 조각으로 갈라진다', '좌표를 만들 수 없다', 'LLM이 더 똑똑해진다'], 'a': 0,
             'why': '"3일 이내"와 "재생하지 않았다면"이 갈라지면 한 조각만으로는 답이 불완전합니다.', 'hint': '맥락이 어디로 가나요?'},
            {'q': 'k = 3, 조각 200자면 LLM에게 넘기는 글은 대략?', 'o': ['약 200자', '약 600자', '약 6,000자'], 'a': 1,
             'why': '3 × 200 = 600자 안팎. 문장 단위로 끊어 조금 달라집니다.', 'hint': 'k × 조각 크기'}],
    'q44': [{'q': '"LP-204"처럼 코드가 든 질문에 하이브리드 검색이 유리한 이유는?', 'o': ['글자 점수가 코드를 정확히 맞추기 때문', '뜻 점수가 코드를 잘 알아서', '조각이 짧아서'], 'a': 0,
             'why': '임베딩은 LP-204와 LP-503을 모두 "오류"로 읽지만, 글자 점수는 "LP-204" 글자 그대로를 잡습니다.', 'hint': '1장 특징 ⑥ 사전에 없는 말.'},
            {'q': 'α = 1이면?', 'o': ['글자 점수만 쓴다', '뜻 점수만 쓴다', '둘을 반씩 섞는다'], 'a': 1,
             'why': '섞은 점수 = α × 뜻 + (1 − α) × 글자. α = 1이면 뜻 점수만 남습니다.', 'hint': '식에 1을 넣어 보세요.'}],
    'q45': [{'q': '옛 환불 규정 문서가 함께 찾아지는 문제를 막는 기본 방법은?', 'o': ['문서를 모두 지운다', '작성일·폐기 여부 메타데이터로 최신 판만 거른다', 'k를 늘린다'], 'a': 1,
             'why': '감사 등으로 지우지 못하는 경우가 많아, 메타데이터로 거르는 것이 기본입니다.', 'hint': '3장의 메타데이터 필터.'},
            {'q': '사내 기밀 문서를 RAG에 넣을 때 함께 걸어야 할 조건은?', 'o': ['질문한 사람의 열람 권한', '문장 길이', '임베딩 차원'], 'a': 0,
             'why': '권한이 없는 사람에게 기밀 조각이 답으로 나가지 않도록 권한 정보를 메타데이터로 겁니다.', 'hint': '누가 볼 수 있나요?'}],
}

JS = r'''
var D=VL.load(),RQ=D.ragq,CH150=VL.chunk(D.kb,150,0,true),CH250=VL.chunk(D.kb,250,0,true);
/* 4-1 */
(function(){var BG=VL.bigram(),mode='top',rr=VL.rng(3);var starts=Object.keys(BG['<시작>']).sort(function(a,b){return BG['<시작>'][b]-BG['<시작>'][a]}).slice(0,8).concat(['연기','진짜','스토리가','OST가']);
  $('#w41').innerHTML=starts.map(function(w){return '<option>'+w+'</option>'}).join('');
  function nexts(w){var m=BG[w]||{},t=0,k;for(k in m)t+=m[k];return Object.keys(m).map(function(x){return [x,m[x]/t]}).sort(function(a,b){return b[1]-a[1]});}
  function bars(w){var n=nexts(w).slice(0,6);$('#vb41').innerHTML=n.map(function(x){return '<div class="vb"><span>'+VL.esc(x[0])+'</span><div class="tr"><div class="fl" style="width:'+Math.round(x[1]*100)+'%"></div></div><span class="v">'+VL.pct(x[1],0)+'</span></div>'}).join('')||'<p class="small muted">다음 말이 없습니다.</p>';}
  function gen(){var w=$('#w41').value,out=[w];for(var i=0;i<12;i++){var n=nexts(w);if(!n.length)break;var pick=n[0][0];if(mode==='rand'){var u=rr(),acc=0;for(var j=0;j<n.length;j++){acc+=n[j][1];if(u<=acc){pick=n[j][0];break;}}}if(pick==='<끝>')break;out.push(pick);w=pick;}
    $('#out41').textContent=out.join(' ');bars($('#w41').value);}
  $('#w41').addEventListener('change',gen);$('#go41').addEventListener('click',gen);
  $$('#p41 [data-m]').forEach(function(b){b.addEventListener('click',function(){mode=b.dataset.m;$$('#p41 [data-m]').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});gen();})});gen();
  $('#q41').innerHTML=RQ.map(function(q,i){return '<button class="bt" data-i="'+i+'">'+q.q+'</button>'}).join('');
  $$('#q41 .bt').forEach(function(b){b.addEventListener('click',function(){var q=RQ[+b.dataset.i];$$('#q41 .bt').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});
    $('#a41').innerHTML='<div class="ansbox bad"><b>LLM 혼자 답 (흉내)</b><br>'+VL.esc(q.llm)+'</div><details><summary>안내 문서의 실제 내용 보기</summary><p>'+(q.doc?VL.esc(q.ans):'안내 문서에 없는 내용입니다. "모릅니다"가 맞는 답입니다.')+'</p></details>';})});
})();
/* 4-2 */
(function(){var cur=0;$('#qs42').innerHTML=RQ.map(function(q,i){return '<button class="bt" data-i="'+i+'" aria-pressed="'+(i===0)+'">'+q.q+'</button>'}).join('');
  var steps=['① 문서 넣기','② 잘게 쪼개기','③ 좌표 저장','④ 질문 → 좌표','⑤ 조각 k개 찾기','⑥ 붙여서 답하기'];
  function run(){var k=+$('#k42').value,th=+$('#th42').value/100;$('#kv42').textContent=k+'개';$('#thv42').textContent=th.toFixed(2);
    var t=$('#t42').value.trim(),q=t?{q:t}:RQ[cur],h=VL.retrieve(CH250,q.q,{k:k,alpha:1,newest:true}),a=VL.answer(q.q,h,th,t?null:q);
    $('#fl42').innerHTML=steps.map(function(s){return '<span class="on">'+s+'</span>'}).join('');
    $('#rs42').innerHTML=h.map(function(x){var pass=x.s>=th;return '<li class="'+(pass?(q.key&&x.c.text.indexOf(q.key)>=0?'ok':'nt'):'no')+'"><span class="sc">'+x.s.toFixed(2)+'</span><small>'+x.c.title+' · '+x.c.date+(pass?'':' · 문턱 아래, 버림')+'</small>'+VL.esc(x.c.text)+'</li>'}).join('');
    var used=h.filter(function(x){return x.s>=th});$('#pr42').textContent=VL.prompt(q.q,used);
    $('#an42').className='ansbox'+(a.none?' none':(!t&&!a.ctx?' bad':''));$('#an42').innerHTML=VL.esc(a.text)+(a.src?'<br><small class="muted">출처: '+a.src.title+' · '+a.src.date+'</small>':'');
    $('#lo42').innerHTML=t?'<span class="muted">직접 쓴 질문에는 흉내 답을 준비하지 않았습니다.</span>':VL.esc(q.llm);
    var len=used.reduce(function(s,x){return s+x.c.text.length},0);
    VL.kpis($('#k42'),[[used.length+' / '+k,'문턱을 넘은 조각',used.length?'g':'a'],[len+'자','LLM에게 넘긴 자료 글자 수','i'],[h.length?h[0].s.toFixed(2):'—','1위 조각 점수','m'],[t?'—':(q.doc?(a.ctx?'근거 있음':'근거 못 찾음'):(a.none?'모른다고 함 (정답)':'지어낼 위험')),'판정',t?'i':(q.doc?(a.ctx?'g':'r'):(a.none?'g':'r'))]]);}
  $$('#qs42 .bt').forEach(function(b){b.addEventListener('click',function(){cur=+b.dataset.i;$('#t42').value='';$$('#qs42 .bt').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});run();})});
  ['#k42','#th42','#t42'].forEach(function(s){$(s).addEventListener('input',run)});run();
})();
/* 4-3 */
(function(){var cv=$('#cv43'),cv2=$('#cv43b'),ov=false,curve=null,ck='';
  function ev(size,k){return VL.ragEval(VL.chunk(D.kb,size,ov?1:0,true),{k:k,alpha:.5,thr:.35,newest:true});}
  function draw(){var size=+$('#sz43').value,k=+$('#k43').value;$('#szv43').textContent=size+'자';$('#kv43').textContent=k+'개';var ch=VL.chunk(D.kb,size,ov?1:0,true);
    var f=fit(cv),g=f.c;g.fillStyle='#fff';g.fillRect(0,0,f.W,f.H);var docs=D.kb,rowH=(f.H-20)/docs.length,mx=Math.max.apply(null,docs.map(function(d){return d.text.length}));var L=120,Wd=f.W-L-14,cols=['#1e55c8','#13733a','#c42a6e','#a35c00','#9b3fb5'];
    g.font='11px "IBM Plex Sans KR",sans-serif';docs.forEach(function(d,i){var y=10+i*rowH;g.fillStyle=d.old?'#c9302c':'#16212b';g.fillText((d.old?'[구] ':'')+d.title,4,y+rowH*.7);var x=L;ch.filter(function(c){return c.doc===d.id}).forEach(function(c,j){var w=c.text.length/mx*Wd;g.fillStyle=cols[j%5];g.globalAlpha=.75;g.fillRect(x,y+2,Math.max(2,w-2),rowH-4);g.globalAlpha=1;x+=w;});});
    stamp(g,f.W,'조각 '+ch.length+'개');
    var key=k+'|'+ov;if(ck!==key){ck=key;curve=[];for(var s=60;s<=400;s+=20){var e=ev(s,k);curve.push([s,e.acc,e.tokens]);}}
    var f2=fit(cv2),g2=f2.c,A=VL.axes(g2,f2.W,f2.H,{xmin:60,xmax:400,ymin:0,ymax:1,xlab:'조각 크기 (자)',ylab:'정답률',yfmt:function(v){return Math.round(v*100)+'%'}});
    g2.strokeStyle='#13733a';g2.lineWidth=2.5;g2.beginPath();curve.forEach(function(p,i){var x=A.sx(p[0]),y=A.sy(p[1]);i?g2.lineTo(x,y):g2.moveTo(x,y);});g2.stroke();
    var mt=Math.max.apply(null,curve.map(function(p){return p[2]}));g2.strokeStyle='#a35c00';g2.setLineDash([5,4]);g2.beginPath();curve.forEach(function(p,i){var x=A.sx(p[0]),y=A.sy(p[2]/mt);i?g2.lineTo(x,y):g2.moveTo(x,y);});g2.stroke();g2.setLineDash([]);g2.lineWidth=1;
    g2.strokeStyle='#c9302c';g2.beginPath();g2.moveTo(A.sx(size),A.T);g2.lineTo(A.sx(size),A.sy(0));g2.stroke();g2.fillStyle='#a35c00';g2.font='12px sans-serif';g2.fillText('점선: 넘기는 글자 수 (최대 '+mt+'자 = 위 끝)',A.L+6,A.T+12);
    var e=ev(size,k);VL.kpis($('#k43'),[[ch.length+'개','조각 수','i'],[VL.pct(e.acc,0),'질문 '+RQ.length+'개 정답률 (근거 조각을 맞게 찾음)','g'],[e.hall+'개','엉뚱한 근거로 답한 수','r'],[e.tokens+'자','질문당 넘긴 글자 수 평균','a']]);
    $('#in43').innerHTML='<p class="m">정답률(초록)과 넘기는 글자 수(주황 점선)를 함께 보세요. 정답률이 같다면 글자 수가 적은 쪽이 싸고 빠릅니다.</p>';}
  $('#sz43').addEventListener('input',draw);$('#k43').addEventListener('input',draw);$('#ov43').addEventListener('click',function(){ov=!ov;this.setAttribute('aria-pressed',ov?'true':'false');draw();});
  Loop.add(cv,function(dt){if(dt===0)draw();});
})();
/* 4-4 */
(function(){var cv=$('#cv44'),k=1,curve={};$('#q44').innerHTML=RQ.map(function(q,i){return '<option value="'+i+'"'+(q.q.indexOf('LP-204')===0?' selected':'')+'>'+q.q+'</option>'}).join('');
  function acc(al){return VL.ragEval(CH150,{k:k,alpha:al,thr:.35,newest:true});}
  function draw(){var al=+$('#al44').value/100;$('#alv44').textContent=al.toFixed(1);var q=RQ[+$('#q44').value],h=VL.retrieve(CH150,q.q,{k:5,alpha:al,newest:true});
    $('#t44').innerHTML='<tr><th>순위</th><th>조각</th><th class="n">뜻</th><th class="n">글자</th><th class="n">섞은 점수</th></tr>'+h.map(function(x,i){return '<tr'+(q.key&&x.c.text.indexOf(q.key)>=0?' class="hl"':'')+'><td>'+(i+1)+'</td><td>'+x.c.title+'</td><td class="n">'+x.vec.toFixed(2)+'</td><td class="n">'+x.bm.toFixed(2)+'</td><td class="n"><b>'+x.s.toFixed(2)+'</b></td></tr>'}).join('');
    if(!curve[k]){curve[k]=[];for(var a=0;a<=10;a++){var e=acc(a/10);curve[k].push([a/10,e.res.filter(function(r){return r.right}).length]);}}
    var f=fit(cv),g=f.c,A=VL.axes(g,f.W,f.H,{xmin:0,xmax:1,ymin:0,ymax:RQ.length,xlab:'α (뜻 점수 몫)',ylab:'맞힌 질문 수'});
    g.strokeStyle='#1e55c8';g.lineWidth=2.5;g.beginPath();curve[k].forEach(function(p,i){var x=A.sx(p[0]),y=A.sy(p[1]);i?g.lineTo(x,y):g.moveTo(x,y);});g.stroke();g.lineWidth=1;curve[k].forEach(function(p){VL.dot2(g,A.sx(p[0]),A.sy(p[1]),3,'#1e55c8',1)});
    var me=curve[k].filter(function(p){return Math.abs(p[0]-al)<1e-6})[0];VL.dot2(g,A.sx(al),A.sy(me[1]),7,'#c9302c',1);stamp(g,f.W,'질문 '+RQ.length+'개 · k = '+k);
    var best=curve[k].reduce(function(a,b){return b[1]>a[1]?b:a});var top=h[0],okTop=q.key&&top.c.text.indexOf(q.key)>=0;
    VL.kpis($('#k44'),[[me[1]+' / '+RQ.length,'지금 α의 맞힌 질문','g'],[best[1]+'개 (α '+best[0].toFixed(1)+')','가장 좋은 α','i'],[top.c.title,'이 질문의 1위 조각',okTop?'g':'r']]);
    $('#in44').innerHTML='<p class="'+(okTop?'g':'r')+'">'+(okTop?'1위 조각에 정답 문구("'+q.key+'")가 있습니다.':q.key?'1위 조각에 정답 문구("'+q.key+'")가 없습니다. α를 바꿔 보세요.':'안내 문서에 없는 질문입니다. 1위 점수가 문턱(0.35)보다 낮아야 "모릅니다"로 답합니다.')+'</p>';}
  $('#al44').addEventListener('input',draw);$('#q44').addEventListener('change',draw);
  $$('#p44 [data-k]').forEach(function(b){b.addEventListener('click',function(){k=+b.dataset.k;$$('#p44 [data-k]').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});draw();})});
  Loop.add(cv,function(dt){if(dt===0)draw();});
})();
/* 4-5 */
(function(){var useOld=true,newest=false;
  function run(){var q=$('#q45').value,ch=VL.chunk(D.kb,150,0,useOld),h=VL.retrieve(ch,q,{k:3,alpha:.5,newest:newest});var hasOld=h.some(function(x){return x.c.old}),hasNew=h.some(function(x){return x.c.doc==='refund_v2'});
    $('#rs45').innerHTML=h.map(function(x){return '<li class="'+(x.c.old?'no':'ok')+'"><span class="sc">'+x.s.toFixed(2)+'</span><small>'+x.c.title+' · 작성일 '+x.c.date+(x.c.old?' · 구버전 (2026-06-30까지)':'')+'</small>'+VL.esc(x.c.text)+'</li>'}).join('');
    var checks=[['출처 조각에 제목과 날짜가 붙어 있나',true],['찾은 조각이 모두 현행 판인가',!hasOld],['서로 다른 규정이 한 프롬프트에 섞이지 않았나',!(hasOld&&hasNew)],['질문의 핵심(환불·해지)이 근거 조각에 실제로 있나',h.some(function(x){return /환불|해지/.test(x.c.text)})]];
    $('#ck45').innerHTML='<h4>근거 확인 점검표</h4>'+checks.map(function(c){return '<div class="mission'+(c[1]?' ok':'')+'"><span class="st">'+(c[1]?'통과':'확인 필요')+'</span><p>'+c[0]+'</p></div>'}).join('');
    $('#in45').innerHTML='<p class="'+(hasOld?'r':'g')+'">'+(hasOld?'구버전 조각이 함께 올라왔습니다. LLM이 "7일 이내"를 답할 수 있습니다. "날짜 필터: 최신 판만"을 켜 보세요.':'현행 판만 남았습니다. 답의 근거가 하나로 모였습니다.')+'</p>';}
  $('#q45').addEventListener('change',run);
  $('#old45').addEventListener('click',function(){useOld=!useOld;this.setAttribute('aria-pressed',useOld?'true':'false');run();});
  $('#new45').addEventListener('click',function(){newest=!newest;this.setAttribute('aria-pressed',newest?'true':'false');run();});run();
})();
/* 대결 4 */
Duel({el:'#d4',run:function(){var f=VL.ragEval(CH150,{k:1,alpha:.3,thr:.35,newest:true}),r=VL.ragEval(CH150,{k:1,alpha:1,thr:.35,newest:true});window._d4=[f,r];
    return {fly:f.res.filter(function(x){return x.right}).length,robo:r.res.filter(function(x){return x.right}).length}},scale:RQ.length,fmt:function(v){return v+' / '+RQ.length},bigGap:3,
  report:function(r){var f=window._d4[0],b=window._d4[1],diff=f.res.filter(function(x,i){return x.right&&!b.res[i].right}).map(function(x){return '"'+x.q.q+'"'});return '섞기 '+r.fly+'개, 벡터만 '+r.robo+'개 맞혔어요. 섞기만 맞힌 질문: '+(diff.join(', ')||'없음')+'.'},
  verdict:{fly:'초파리 승. 오류 코드처럼 글자 그대로가 중요한 질문에서 글자 점수가 정답 조각을 1위로 올렸습니다. 1장에서 진 글자 검색이 4장에서 쓸모를 찾았습니다. 도구는 낡고 새것이 아니라, 무엇을 잘하느냐로 고릅니다.',robo:'주판봇 승.',draw:'무승부.'}});
'''


def build_page():
    nav = [('#s1', '4-1 LLM'), ('#s2', '4-2 RAG'), ('#s3', '4-3 쪼개기'), ('#s4', '4-4 섞기'), ('#s5', '4-5 함정'), ('#duel', '대결'), ('#sum', '정리')]
    cov = cover('cover_04', '벡터 DB 연구실 · 4장', '찾아서 답하는 AI — LLM과 RAG', chars=(('doc', 'front'), ('asst', 'e15'), ('fly', 'magnify'), ('robo', 'wow')))
    hr = hero('벡터 DB 연구실 · 4장 · LLM과 RAG', '찾아서 답하는 AI',
              'LLM이 모르는 우리 회사 이야기를, 지어내지 않고 근거와 함께 답하게 하려면 무엇이 필요할까?',
              '네 번째 수업은 가장 어려운 주제. 하루는 인턴들에게 LLM이 어떻게 문장을 만드는지, 그리고 벡터 DB에서 근거를 찾아 붙여 주는 RAG를 묻습니다. 가상 OTT 「랩플릭스」 고객센터가 실험 무대입니다.',
              [('%d개' % R['n']['kb'], '랩플릭스 안내 문서 (구버전 1개 포함)', 'i'), ('%d개' % R['n']['ragq'], '채점용 질문 (문서에 없는 질문 2개 포함)', 'm'),
               ('%s' % pct(RG[(150, .5, 3)]['acc'], 0), 'RAG 정답률 (150자·k 3·α 0.5)', 'g'), ('%d → %d개' % (D4['vec_right'], D4['hyb_right']), 'k 1일 때 벡터만 → 섞기 맞힌 수', 'a')],
              [('doc', 'front', '오늘은 1~3장에서 만든 것이 한 줄로 이어집니다. 좌표, 창고, 필터, 그리고 LLM.'),
               ('asst', 'e15', '(심호흡) LLM은 저도 아직 공부 중이라… 같이 실험하면서 알아봐요!'),
               ('sia', 'smile', '저희도 ChatGPT는 써 봤어요.'), ('moa', 'report', '9번 그림(RAG) 크게 뽑아 왔어요.')],
              crowd('"하루 또 심호흡한다." "4장은 어렵대." "그래도 같이 실험하자는 말, 좋다."', moods=('e15', 'e02', 'e16')))
    return build(P, title='4장 · 찾아서 답하는 AI — LLM과 RAG | 벡터 DB 연구실',
                 desc='LLM의 다음 말 잇기와 환각, RAG의 여섯 걸음, 조각 크기, 뜻·글자 하이브리드 검색, 오래된 문서 거르기를 가상 고객센터 문서로 실험합니다.',
                 nav=nav, cover_html=cov, hero=hr,
                 body=body() + footer([('랩플릭스 안내 문서·질문', '이 연구실이 만든 가상 데이터 (가상 OTT 서비스)'),
                                       ('RAG', 'Lewis 외 (2020) Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks, NeurIPS 2020'),
                                       ('BM25', 'Robertson & Zaragoza (2009) The Probabilistic Relevance Framework: BM25 and Beyond, Foundations and Trends in IR 3(4)'),
                                       ('언어 모델·트랜스포머', '<a href="%s">인공지능과 자연어 데이터 분석 강좌</a> 7~9장 (9-3 LLM과 RAG)' % NLP)],
                                      ['"LLM 혼자 답"과 "RAG 답"의 문장은 미리 적어 둔 흉내입니다. 조각 찾기·점수·정답 판정은 실제 계산입니다.',
                                       '아주 작은 언어 모델은 리뷰의 두 낱말 빈도만 센 설명용입니다.', '정답률은 질문 %d개로 잰 작은 숫자입니다.' % R['n']['ragq']],
                                      prev=('03_vector_store.html', '3장 · 벡터 창고'), nxt=('05_cases.html', '5장 · 현장 사례')),
                 gloss=GLOSS, quizzes=QUIZ, page_js=JS, og='og_04')


if __name__ == '__main__':
    print(build_page())
