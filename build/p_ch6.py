# -*- coding: utf-8 -*-
"""6장 · LLM은 찾은 자료를 어떻게 읽나 — 어텐션과 트랜스포머를 3D로"""
from lib import *

P = '06_attention_3d.html'
AT = R['att']; SX = R['softmax_ex']


def body():
    b = three([
        ('무엇을', '벡터 DB에서 찾아온 자료 조각이 프롬프트에 붙은 뒤, LLM(트랜스포머) 안에서 어텐션이 그 글을 어떻게 "읽는지"를 3D로 돌려 봅니다. 토큰과 위치, Q·K·V, 여러 머리와 층, 다음 말 고르기까지 갑니다.'),
        ('왜 중요한가', '"LLM이 어텐션으로 벡터 DB에서 말을 가져온다"는 오해가 흔합니다. 실제로는 찾기(벡터 DB, 모델 밖)와 읽기(어텐션, 모델 안)가 따로 일어납니다. 둘 다 "내적으로 닮음을 잰다"는 같은 생각을 쓰기 때문에 헷갈립니다.'),
        ('업무에서는', 'RAG 답이 틀렸을 때 "찾기가 틀렸나, 읽기가 틀렸나"를 나눠 볼 수 있습니다. 근거를 너무 많이 붙이면 왜 답이 흐려지는지도 설명할 수 있습니다.')],
        '코드·수식을 몰라도 됩니다. 3D 그림은 마우스(손가락)로 좌우로 끌면 돌아가고, 점을 누르면 고를 수 있습니다. 어텐션 계산은 이 연구실의 24차원 교육용 좌표로 흉내 낸 설명용입니다.',
        [('Q·K·V', 'Query·Key·Value, 묻는 좌표·찾아보는 좌표·가져오는 내용'), ('softmax', '점수를 합이 1인 비율로 바꾸는 계산'), ('β', '베타, 점수를 키우는 배율'),
         ('FFN', 'Feed-Forward Network, 어텐션 뒤의 계산 층'), ('PE', 'Positional Encoding, 위치 정보')])

    b += section('map', '큰 그림 — 이 장은 어디쯤인가',
                 '<div class="mapbar"><span>4장 · LLM과 RAG</span><i>→</i><span>5장 · 현장 사례</span><i>→</i><span class="on">6장 · 어텐션 3D</span><i>→</i><span>7장 · 그래프·온톨로지</span><i>→</i><span>실전 연습장</span></div>'
                 '<div class="tw"><table class="tb"><tr><th></th><th>벡터 DB 검색 (3·4장)</th><th>어텐션 (이 장)</th></tr>'
                 '<tr><td>어디서</td><td>모델 밖, 창고 안</td><td>모델 안, 프롬프트 토큰끼리</td></tr>'
                 '<tr><td>무엇과 무엇을 재나</td><td>질문 좌표 ↔ 수백만 조각 좌표</td><td>지금 토큰의 Q ↔ 프롬프트 토큰들의 K (수천~수십만 개)</td></tr>'
                 '<tr><td>재는 법</td><td>코사인(내적)</td><td>내적 ÷ √d</td></tr>'
                 '<tr><td>고르는 법</td><td>위에서 k개만 딱 가져옴 (딱딱한 선택)</td><td>모두에게 비율을 나눠 섞음 (부드러운 선택)</td></tr>'
                 '<tr><td>결과</td><td>프롬프트에 붙일 글 조각</td><td>토큰마다 새로 섞인 좌표 → 다음 말</td></tr></table></div>'
                 + say('doc', 'front', '오늘의 결론부터 말하면, 어텐션은 "모델 안의 작은 벡터 검색"입니다. 다만 창고에서 가져오는 게 아니라, 이미 프롬프트에 올라온 글 안에서 찾습니다. 그 프롬프트에 무엇을 올릴지 정하는 게 벡터 DB입니다.'))

    # ── 6-1
    s = say('doc', 'think', '상황 하나. 인턴 시아가 이렇게 물었습니다. "LLM이 어텐션으로 벡터 DB에서 말을 꺼내 오는 거죠?" 반은 맞고 반은 틀립니다. 어디까지가 맞을까요?')
    s += duo(why([('문제 상황', 'RAG를 쓰는데 답이 틀렸습니다. 고치려면 어디서 틀렸는지 알아야 합니다.'),
                  ('흔한 오해', '"LLM이 어텐션으로 창고를 뒤진다." 실제 LLM은 창고에 직접 손대지 않습니다. 프로그램(검색기)이 먼저 창고에서 조각을 찾아 글로 붙여 주면, LLM은 그 글만 읽습니다.'),
                  ('맞는 부분', '창고에 넣을 좌표를 만드는 임베딩 모델도 안에 트랜스포머와 어텐션이 있습니다. 그리고 LLM은 붙여 받은 글을 어텐션으로 읽습니다. 어텐션은 "넣을 때"와 "읽을 때" 쓰이고, "찾을 때"는 코사인과 색인이 씁니다.')],
                 '도서관 사서(벡터 DB)가 책 몇 쪽을 복사해 책상에 올려 주면, 학생(LLM)은 그 복사본만 읽고 답을 씁니다. 학생이 서고에 들어가지는 않습니다.'),
             pair('찾기 (모델 밖)', '질문 → 임베딩 모델(안에 어텐션 있음) → 질문 좌표 → 벡터 DB에서 코사인·색인으로 가까운 조각 k개 → 글 그대로 꺼냄.',
                  '읽기 (모델 안)', '지시 + 조각 글 + 질문 → 토큰으로 자름 → 토큰 좌표 → 어텐션이 토큰끼리 닮음을 재서 섞음(층마다 반복) → 다음 말.'))
    s += talk([('asst', 'e15', '시아, 방금 질문… 좋은 질문이에요! 그럼 거꾸로 물어볼게요. LLM이 창고 안의 조각 좌표를 직접 볼까?'),
               ('sia', 'think', '음… 좌표가 아니라 조각의 "글"을 받는 거면, 좌표는 못 보겠네요.'),
               ('robo', 'wow', '어텐션이 창고까지 손을 뻗는 거라고! 그래야 멋있잖아!'),
               ('fly', 'point', '아래 3D에서 창고 지도를 돌려 보고, 아래 "프롬프트 줄"에서 경계선이 어디 있는지 봐. 좌표는 경계를 못 넘어.'),
               ('asst', 'report', '경계 왼쪽은 창고(좌표), 오른쪽은 모델(글 → 토큰)이에요. 넘어가는 건 조각의 글뿐이에요.')])
    s += crowd('"하루, 시아 질문에 당황 안 하고 되물었어!" "많이 늘었다."', moods=('e04', 'e16', 'e01'))
    s += panel('p61', '실험 · 3D 창고 지도와 프롬프트 줄 — 찾기와 읽기의 경계', '교육용 좌표 · 페이지가 직접 계산',
               '<div class="ctrl"><div class="group"><span class="glabel">질문</span><select class="sel" id="q61"></select></div>'
               '<div class="group"><span class="glabel">가져올 조각 k</span><input type="range" id="k61" min="1" max="5" value="2" aria-label="k"><span class="val" id="kv61"></span></div>'
               '<div class="group"><button class="bt" id="rot61" aria-pressed="true">자동 회전</button></div></div>'
               + canvas('cv61', 380, '랩플릭스 안내 문서 조각들을 3차원 좌표로 그린 창고 지도와 질문 별, 가져온 조각으로 이어진 선') +
               '<p class="small muted">점 = 안내 문서 조각(24차원 좌표를 PCA로 3축에 눌러 담음), 색 = 문서, ★ = 질문 좌표, 빨간 선 = 가져온 조각. 끌어서 돌려 보세요.</p>'
               '<h4>프롬프트 줄 — LLM이 실제로 받는 것</h4><div class="flowsteps" id="pr61"></div><div class="insight" id="in61" aria-live="polite"></div>', real=True)
    s += explain(['3D 지도는 창고 안입니다. 질문 별에서 가까운 조각을 코사인으로 골라 빨간 선으로 이었습니다(4장과 같은 계산).',
                  '프롬프트 줄은 모델이 받는 것입니다. 지시, 가져온 조각의 <b>글</b>, 질문이 한 줄로 이어집니다. 조각의 좌표는 넘어가지 않습니다.',
                  '그래서 RAG 답이 틀리면 두 곳을 나눠 봅니다. ① 찾기: 정답 조각이 프롬프트 줄에 있었나 ② 읽기: 있었는데도 모델이 다른 곳을 봤나.'],
                 '3D 지도는 24차원을 세 축으로 눌러 담은 그림이라 실제 거리와 조금 다릅니다. 순위는 24차원 코사인으로 계산했습니다.')
    s += wrapup('벡터 DB는 "무엇을 읽힐지" 고르고, 어텐션은 "읽힌 것 중 어디를 볼지" 정합니다. 둘을 잇는 것은 좌표가 아니라 글입니다.')
    s += quiz('q61')
    b += step('s1', '6-1', '찾기와 읽기는 다른 곳에서 — 벡터 DB와 LLM의 경계', ['방법: RAG 프롬프트 · 3D 창고 지도', '일상: 사서가 복사해 준 쪽'], s)

    # ── 6-2 토큰과 위치
    s = say('doc', 'think', '프롬프트 줄이 모델 안으로 들어가면 가장 먼저 무슨 일이 생길까요? 글은 숫자가 아니니, 2장에서처럼 좌표로 바꿔야겠죠.')
    s += duo(why([('문제 상황', '모델은 글자를 읽지 못합니다. 토큰마다 좌표가 필요하고, 토큰의 순서도 알아야 합니다.'),
                  ('앞 방법의 한계', '2장의 문장 임베딩은 문장 전체를 좌표 하나로 눌렀습니다. 그러면 "어느 낱말이 어디서 무엇과 이어지는지"가 사라집니다.'),
                  ('해법', '글을 토큰(낱말 조각)으로 자르고, 토큰마다 좌표(토큰 임베딩)를 줍니다. 여기에 "몇 번째 자리인가"를 나타내는 위치 좌표를 더합니다. 같은 낱말이라도 자리가 다르면 조금 다른 좌표가 됩니다.')],
                 '같은 "네"라도 대답의 "네"와 숫자 "네 대"는 앞뒤 자리와 함께 읽어야 뜻이 갈립니다.'),
             mathbox('위치 좌표는 어떻게 만들어요? 사인, 코사인이 나와서 무서워요.', '삼각함수 (고등학교) — 사인·코사인은 일정하게 되풀이되는 물결',
                     '토큰의 입력 좌표 = 토큰 좌표 + 위치 좌표, 위치 좌표의 한 성분 = sin(자리 ÷ 물결 길이)',
                     [('자리', 'pos', '0, 1, 2 … 몇 번째 토큰인가'), ('물결 길이', '', '성분마다 다르게 정한 주기. 짧은 물결·긴 물결을 섞음'), ('sin', '사인', '−1과 1 사이를 오가는 값')],
                     '물결 길이를 2로 두면 자리 0, 1, 2, 3의 값은 sin(0) = <b>0</b>, sin(0.5) ≈ <b>0.48</b>, sin(1) ≈ <b>0.84</b>, sin(1.5) ≈ <b>1.00</b>. 자리마다 다른 값이 붙어 순서가 좌표에 새겨집니다.',
                     '자리마다 물결 위의 다른 점을 더해 주는 거네요. 원래 논문은 이런 물결 수백 개를 겹친대요!'))
    s += talk([('asst', 'e13', '모아, "환불"이 문장에 두 번 나오면 두 토큰의 좌표는 같을까?'),
               ('moa', 'think', '낱말이 같으니까 같을 것 같은데… 자리가 다르면 다르게 해야 하나요?'),
               ('robo', 'coin', '같은 낱말은 같은 좌표! 간단하잖아.'),
               ('fly', 'point', '아래에서 "위치 정보 더하기"를 껐다 켜 봐. 두 "환불" 점이 어떻게 되는지.'),
               ('asst', 'report', '끄면 두 점이 완전히 겹치고, 켜면 나선을 따라 떨어져요. 순서가 좌표에 들어갔어요.')])
    s += panel('p62', '실험 · 토큰 좌표와 위치 나선 3D', '교육용 좌표 · 위치 좌표는 설명용 나선',
               '<div class="ctrl"><div class="group"><span class="glabel">문장</span><input type="text" class="wide" id="t62" value="환불은 결제 내역 메뉴에서 신청하고 환불 금액은 남은 기간만큼 계산합니다" aria-label="토큰으로 자를 문장"></div></div>'
               '<div class="ctrl"><div class="group"><button class="bt" id="pe62" aria-pressed="true">위치 정보 더하기</button><button class="bt" id="rot62" aria-pressed="true">자동 회전</button></div></div>'
               + canvas('cv62', 360, '문장의 토큰들을 3차원 좌표로 그리고 순서대로 이은 선') +
               '<div class="flowsteps" id="tk62"></div><div class="insight" id="in62" aria-live="polite"></div>', real=True)
    s += explain(['이 페이지는 띄어쓰기로 토큰을 잘랐습니다. 실제 LLM은 "환불은"을 "환불 + 은"처럼 더 잘게(서브워드) 자릅니다.',
                  '위치 정보를 끄면 같은 낱말은 같은 점이라 순서가 사라집니다. 켜면 자리마다 나선 위의 다른 점이 더해져, 같은 낱말도 떨어지고 순서대로 이은 선이 나선을 그립니다.',
                  '최근 LLM은 사인 물결을 더하는 대신 좌표를 자리만큼 "돌리는" 방법(RoPE) 등을 많이 씁니다. 생각은 같습니다. 순서를 좌표에 새긴다.'],
                 '사전에 없는 토큰("신청하고" 등)은 교육용 좌표가 0이라 위치 좌표만 남아 나선 위에 놓입니다. 실제 모델은 모든 토큰에 학습된 좌표가 있습니다.')
    s += codefold([('ids = tokenizer("환불은 결제 내역 메뉴에서…")', '글 → 토큰 번호들'), ('x = token_embedding[ids] + position(ids)', '토큰 좌표 + 위치 좌표')])
    s += wrapup('모델 안에서 글은 "토큰 좌표 + 위치 좌표"의 줄이 됩니다. 이제 이 줄 안에서 토큰끼리 서로를 찾아보는 어텐션 차례입니다.')
    s += quiz('q62')
    b += step('s2', '6-2', '토큰과 위치 — 글이 좌표의 줄이 된다', ['방법: 토큰 임베딩 · 위치 정보', '일상: 같은 "네", 다른 자리'], s)

    # ── 6-3 어텐션 Q K V
    s = say('doc', 'think', '이제 핵심입니다. 질문 토큰 "얼마"가 답을 쓰려면, 프롬프트 줄 어디를 봐야 할까요? 모든 토큰을 다 같은 무게로 볼 수는 없습니다.')
    s += duo(why([('문제 상황', '토큰 하나가 다음 계산을 하려면, 앞의 수백~수천 토큰 중 관련 있는 곳을 골라 그 내용을 가져와야 합니다.'),
                  ('앞 방법의 한계', '모두를 똑같이 평균 내면 중요한 근거가 흐려집니다. 앞 토큰 몇 개만 보면 먼 곳의 근거를 놓칩니다.'),
                  ('해법 (어텐션)', '토큰마다 세 좌표를 만듭니다. Q(무엇을 찾나), K(나는 이런 내용이야), V(나를 고르면 가져갈 내용). Q와 모든 K의 내적으로 점수를 매기고, softmax로 합이 1인 비율을 만든 뒤, 그 비율로 V를 섞습니다. 벡터 검색을 "부드럽게" 한 것입니다.')],
                 '회의에서 질문이 나오면, 모든 사람의 이름표(K)를 보고 질문(Q)과 맞는 사람에게 더 귀를 기울여, 그 사람들의 말(V)을 비율대로 받아 적는 것과 같습니다.'),
             mathbox('softmax가 뭐예요? e의 몇 제곱… 너무 어려워요.', '지수함수 (고등학교) — 큰 점수는 더 크게, 그리고 전체를 1로 나눠 비율로',
                     '점수 = β × (Q · K),&nbsp;&nbsp; 비율 = e<sup>점수</sup> ÷ (모든 e<sup>점수</sup>의 합),&nbsp;&nbsp; 결과 = Σ 비율 × V',
                     [('Q · K', '큐 내적 케이', '찾는 것과 이름표의 닮음 (2장의 내적)'), ('β', '베타', '점수 배율. 실제 모델은 1/√d로 나눔'), ('e<sup>x</sup>', '이의 엑스 제곱', 'e ≈ 2.718. 점수 차이를 키워 줌'),
                      ('Σ', '시그마', '모두 더하기')],
                     '점수 2, 1, 0이면 e² ≈ 7.39, e¹ ≈ 2.72, e⁰ = 1, 합 11.11. 비율은 <b>%s, %s, %s</b>. 가장 닮은 토큰이 2/3을 받고, 나머지도 조금씩 받습니다.' % (num(SX[0], 3), num(SX[1], 3), num(SX[2], 3)),
                     '3장의 "위에서 k개만"과 달리, 모두에게 조금씩 나눠 주는구나. 그래서 "부드러운 검색"이군요!'))
    s += talk([('asst', 'e13', '시아, "프리미엄 요금제는 한 달에 얼마예요?"에서 질문이 가장 많이 봐야 할 토큰은 뭘까?'),
               ('sia', 'explain', '"17,000원으로"요! 답이 거기 있으니까요.'),
               ('robo', 'happy', '뜻이 비슷한 "요금제"를 제일 많이 보겠지. 내적이 크니까!'),
               ('fly', 'point', '둘 다 일리 있어. 아래에서 "Q 변환" 버튼을 껐다 켜 봐. 실제 모델은 Q를 학습된 행렬로 바꿔서 "무엇을 찾을지"를 바꿔.'),
               ('asst', 'report', '변환을 끄면 "요금제" 같은 비슷한 낱말을 보고, 켜면 숫자가 든 "17,000원으로"에 비율이 몰려요.')])
    s += crowd('"하루 설명 들으니 softmax가 무섭지 않다." "회의 비유 좋았어."', moods=('e01', 'e13', 'e16'))
    s += panel('p63', '실험 · 어텐션 3D — 질문 토큰이 프롬프트를 훑는 모습', '교육용 좌표 · Q 변환은 손으로 만든 설명용',
               '<div class="ctrl"><div class="group"><span class="glabel">질문</span><select class="sel" id="q63"></select></div>'
               '<div class="group"><span class="glabel">배율 β</span><input type="range" id="b63" min="1" max="16" value="8" aria-label="베타"><span class="val" id="bv63"></span></div></div>'
               '<div class="ctrl"><div class="group"><button class="bt" id="wq63" aria-pressed="false">Q 변환 켜기 (얼마·며칠·속도 → 숫자 토큰을 찾게)</button><button class="bt" id="rot63" aria-pressed="true">자동 회전</button></div></div>'
               + canvas('cv63', 400, '프롬프트 토큰들을 3차원 점으로 그리고 질문에서 각 토큰으로 이은 선의 굵기가 어텐션 비율인 그림') +
               '<div class="grid2"><div><h4>어텐션 비율 위 8개</h4><div class="vbars" id="vb63"></div></div><div><h4>섞어 가져온 결과 좌표 (Σ 비율 × V)</h4><div class="vbars" id="ov63"></div></div></div>'
               '<section class="kpis" id="k63" aria-label="숫자 요약"></section><div class="insight" id="in63" aria-live="polite"></div>', real=True)
    s += explain(['Q·K 내적은 2장의 내적, 3장의 벡터 검색과 같은 계산입니다. 다른 점은 위에서 몇 개만 고르지 않고 softmax로 모두에게 비율을 나눈다는 것입니다.',
                  'β를 키우면 큰 점수 쪽으로 비율이 쏠리고(딱딱한 선택에 가까워짐), 줄이면 고르게 퍼집니다. 실제 모델은 1/√d로 나눠 너무 쏠리지 않게 합니다.',
                  'Q 변환을 켜면 같은 질문이 "닮은 낱말"이 아니라 "숫자가 든 토큰"을 찾습니다. 실제 모델의 Q·K·V 행렬은 이런 "무엇을 찾을지"를 수많은 글에서 스스로 배웁니다.'],
                 '이 실험은 Q = K = V = 교육용 좌표(숫자 표시 성분 하나를 더한 25차원)로 둔 단순화입니다. 실제 모델은 토큰마다 수천 차원이고, Q·K·V가 서로 다른 학습된 행렬로 만들어집니다.')
    s += codefold([('scores = (Q @ K.T) / sqrt(d)', '모든 토큰 쌍의 닮음 점수'), ('weights = softmax(scores)', '합이 1인 비율'), ('out = weights @ V', '비율대로 내용을 섞음')])
    s += wrapup('어텐션 = Q로 묻고, K와 내적으로 닮음을 재고, softmax 비율로 V를 섞는 것. 벡터 DB의 검색과 같은 뿌리이고, 다른 점은 "모델 안, 프롬프트 안, 부드럽게"입니다.')
    s += quiz('q63')
    b += step('s3', '6-3', '어텐션 — 모델 안의 부드러운 벡터 검색 (Q·K·V)', ['방법: 셀프 어텐션 · softmax', '일상: 회의에서 귀 기울이기'], s)

    # ── 6-4 머리와 층
    s = say('doc', 'think', '어텐션 한 번이면 충분할까요? "LP-204"는 글자가 같은 곳을, "오류"는 뜻이 비슷한 곳을, 조사 "는"은 바로 앞 낱말을 봐야 합니다. 보는 눈이 하나면 모자랍니다.')
    s += duo(why([('문제 상황', '토큰 사이에는 여러 종류의 관계가 동시에 있습니다. 뜻, 순서, 글자, 문법.'),
                  ('앞 방법의 한계', '어텐션 하나는 한 가지 기준의 비율만 만듭니다.'),
                  ('해법', '어텐션을 여러 개(머리, head) 나란히 두고 각자 다른 Q·K·V로 다른 관계를 보게 합니다. 이것을 한 층으로 묶어 여러 층 쌓으면(트랜스포머), 위층으로 갈수록 토큰 좌표에 주변 정보가 점점 섞입니다.')],
                 '같은 서류를 법무팀(문법), 재무팀(숫자), 영업팀(뜻)이 동시에 검토하고, 그 의견을 모아 다음 회의(다음 층)로 넘기는 것과 같습니다.'),
             pair('4장 하이브리드 검색에서는', '뜻 점수와 글자 점수를 α로 섞었습니다. 사람이 두 기준을 정하고 섞는 비율을 골랐습니다.',
                  '트랜스포머에서는', '머리 수십 개가 각자 기준을 배우고, 층 수십 개가 그 결과를 되풀이해 섞습니다. 이 페이지의 세 머리(뜻·위치·글자)는 그 생각을 보여 주려고 손으로 정한 것입니다.'))
    s += talk([('asst', 'e16', '모아, 머리가 셋이면 "LP-204" 토큰은 각 머리에서 어디를 볼까?'),
               ('moa', 'report', '글자 머리는 앞의 "LP-204는"을, 뜻 머리는 "오류"나 "결제"를, 위치 머리는 바로 앞 토큰을 볼 것 같아요.'),
               ('robo', 'chart', '머리를 100개, 층을 100개! 많을수록 똑똑하지!'),
               ('fly', 'point', '많으면 계산도 그만큼 들어. 아래 3층 탑에서 위층 토큰을 눌러 보고, 머리를 바꿔 가며 선이 어디로 가는지 봐.'),
               ('asst', 'report', '글자 머리는 같은 "LP-204", 위치 머리는 바로 앞, 뜻 머리는 "오류·결제" 쪽으로 선이 가요. 모아 예상이 다 맞았어요!')])
    s += panel('p64', '실험 · 트랜스포머 3층 탑 — 머리 셋이 보는 곳', '교육용 좌표 · 세 머리는 손으로 정한 설명용',
               '<div class="ctrl"><div class="group"><span class="glabel">머리</span><button class="bt" data-h="mean" aria-pressed="true">뜻 머리</button><button class="bt" data-h="pos" aria-pressed="false">위치 머리</button><button class="bt" data-h="char" aria-pressed="false">글자 머리</button><button class="bt" data-h="all" aria-pressed="false">세 머리 평균</button></div>'
               '<div class="group"><button class="bt" id="rot64" aria-pressed="true">자동 회전</button></div></div>'
               + canvas('cv64', 420, '세 층의 판 위에 토큰들이 놓이고, 위층 토큰에서 아래층 토큰으로 어텐션 선이 이어진 탑') +
               '<p class="small muted">아래판 = 1층 입력, 가운데 = 2층, 위판 = 3층. 위판의 점을 누르면 그 토큰이 아래층에서 어디를 봤는지 선이 바뀝니다. 선은 자기와 앞쪽 토큰으로만 갑니다(인과 마스크).</p>'
               '<div class="flowsteps" id="tk64"></div><div class="insight" id="in64" aria-live="polite"></div>', real=True)
    s += explain(['층마다 "자기 좌표 + 어텐션으로 섞어 온 좌표"를 더해 다음 층으로 넘깁니다(잔차 연결). 그래서 위층 토큰일수록 주변 토큰의 정보가 더 많이 섞여 있습니다.',
                  '실제 트랜스포머는 어텐션 뒤에 토큰마다 계산 층(FFN)을 하나 더 거칩니다. 학습한 지식의 상당 부분이 이 층에 담긴다고 봅니다.',
                  '머리마다 보는 관계가 다르다는 것은 실제 모델을 분석한 연구에서도 관찰됩니다. 다만 사람이 이름 붙이기 어려운 머리도 많습니다.',
                  '글을 쓰는 LLM은 토큰마다 <b>자기와 앞쪽 토큰만</b> 봅니다(인과 마스크). 아직 쓰지 않은 뒤쪽 말을 미리 보면 안 되기 때문입니다. 그래서 탑에서 선은 늘 왼쪽(앞)으로만 갑니다. 문장 임베딩 모델은 앞뒤를 모두 봅니다.'],
                 '세 머리의 규칙(뜻 = 교육용 코사인, 위치 = 바로 앞 토큰 선호, 글자 = 글자 조각 겹침)은 이해를 돕기 위해 사람이 정했습니다. 실제 머리는 학습으로 정해집니다.')
    s += wrapup('트랜스포머는 "여러 머리의 어텐션 + 계산 층"을 여러 층 쌓은 것입니다. 층을 지날수록 토큰마다 프롬프트 전체의 정보가 섞인 좌표가 됩니다.')
    s += quiz('q64')
    b += step('s4', '6-4', '여러 머리와 층 쌓기 — 트랜스포머', ['방법: 멀티헤드 어텐션 · 층 쌓기', '일상: 여러 팀의 동시 검토'], s)

    # ── 6-5 다음 말
    s = say('doc', 'think', '마지막 걸음. 층을 다 지난 마지막 토큰의 좌표로 "다음 말"을 고릅니다. 4장의 환불 질문에서, 프롬프트에 붙인 근거가 답을 어떻게 바꾸는지 봅시다.')
    s += duo(why([('문제 상황', '"어제 결제했는데 안 봤어요. 돌려받을 수 있나요?"에 답하려면 "3일"을 써야 합니다.'),
                  ('앞 방법의 한계', '근거가 없으면 모델은 학습 때 자주 본 말(예: 다른 서비스의 "14일")을 고를 수 있습니다(4장 환각).'),
                  ('해법', '마지막 좌표와 모든 낱말 좌표의 내적으로 다음 말 점수를 매기고 softmax로 확률을 냅니다. 프롬프트에 근거가 있으면, 어텐션이 그 근거를 섞어 와서 근거 속 낱말의 점수가 올라갑니다.')],
                 '시험 문제를 풀 때 펼쳐 둔 쪽에 답이 있으면 그 쪽을 따르고, 없으면 기억나는 대로 쓰는 것과 같습니다. 옛 교과서와 새 교과서가 함께 펼쳐져 있으면 헷갈립니다.'),
             pair('근거가 없을 때', '"평소에 자주 본 말"의 확률이 그대로 남습니다. 그럴듯하지만 틀린 "14일"이 이길 수 있습니다.',
                  '근거가 있을 때', '어텐션이 근거 토큰("3일")에 비율을 주고, 그 내용이 섞여 "3일"의 점수가 올라갑니다. 옛 판까지 있으면 "7일"도 함께 올라가 둘이 다툽니다.'))
    s += talk([('asst', 'e13', '시아, 프롬프트에 현행 환불 규정만 붙이면 다음 말로 뭐가 나올까?'),
               ('sia', 'firm', '"3일"이요. 근거에 그렇게 써 있으니까요.'),
               ('robo', 'coin', '많이 붙일수록 좋지! 옛 규정까지 다 붙이자!'),
               ('fly', 'point', '아래에서 "둘 다 붙이기"를 골라 봐. 3일과 7일이 어떻게 갈리는지.'),
               ('asst', 'report', '둘 다 붙이면 7일도 확률이 꽤 올라가요. 4장에서 날짜 필터가 필요했던 이유가 모델 안에서도 보여요.')])
    s += panel('p65', '실험 · 다음 말 고르기 — 붙인 근거가 확률을 바꾼다', '설명용 장난감 계산',
               '<div class="ctrl"><div class="group"><span class="glabel">프롬프트에 붙인 근거</span><button class="bt" data-c="none" aria-pressed="false">없음</button><button class="bt" data-c="new" aria-pressed="true">현행 규정</button>'
               '<button class="bt" data-c="old" aria-pressed="false">구버전 규정</button><button class="bt" data-c="both" aria-pressed="false">둘 다</button></div>'
               '<div class="group"><span class="glabel">근거를 따르는 정도 γ</span><input type="range" id="g65" min="0" max="12" value="6" aria-label="감마"><span class="val" id="gv65"></span></div></div>'
               '<div class="grid2"><div><h4>근거 토큰에 간 어텐션</h4><div class="vbars" id="at65"></div></div><div><h4>다음 말 확률</h4><div class="vbars" id="pb65"></div></div></div>'
               '<div class="insight" id="in65" aria-live="polite"></div>', real=True)
    s += explain(['다음 말 점수 = (학습 때 자주 본 정도) + γ × (어텐션이 그 말이 든 근거 토큰에 준 비율). 이것을 softmax로 확률로 바꿨습니다.',
                  '근거가 없으면 "14일"(자주 본 말이라고 가정)이 이기고, 현행 규정을 붙이면 "3일"이 이깁니다. 옛 판까지 붙이면 "7일"이 함께 올라 확률이 갈립니다.',
                  '실제 LLM에서도 프롬프트 안의 근거끼리 서로 다르면 답이 흔들린다는 보고가 많습니다. 붙일 것을 고르는 일(필터·문턱)이 그래서 중요합니다.'],
                 '"자주 본 정도"의 숫자(14일 > 7일 > 3일)와 γ는 이해를 돕기 위한 가정입니다. 실제 모델의 확률은 수천 차원 좌표와 어휘 수만 개로 계산합니다.')
    s += wrapup('근거는 어텐션을 거쳐 다음 말의 확률을 움직입니다. 좋은 근거만 골라 붙이면 답이 단단해지고, 서로 다른 근거를 섞으면 답이 흔들립니다.')
    s += quiz('q65')
    b += step('s5', '6-5', '다음 말 고르기 — 붙인 근거가 답을 바꾼다', ['방법: 다음 토큰 확률 · softmax', '일상: 펼쳐 둔 교과서'], s)

    b += duel('d6', '근거 조각을 몇 개 붙일까 — 2개 vs 5개 (어텐션이 정답 조각에 머무는 비율)', '2개만 (필요한 만큼)', '5개 (많이 붙일수록 안전)',
              '"엉뚱한 조각이 많으면 어텐션이 흩어져. 필요한 만큼만."', '"5개 붙이면 정답 조각이 거의 꼭 들어가잖아! 많을수록 안전하지!"',
              '답할 수 있는 질문 %d개에서, 질문 좌표의 어텐션 비율 중 정답 문구가 든 조각에 간 몫의 평균 (β = 8)' % AT['k2']['n'])

    b += section('sum', '정리 — 찾기와 읽기, 같은 뿌리 다른 자리',
                 '<div class="tw"><table class="tb"><tr><th>걸음</th><th>무엇이</th><th>무엇으로</th><th>이 장의 실험</th></tr>'
                 '<tr><td>넣기</td><td>임베딩 모델 (안에 트랜스포머)</td><td>어텐션으로 문장을 좌표 하나로</td><td>2장</td></tr>'
                 '<tr><td>찾기</td><td>벡터 DB (모델 밖)</td><td>코사인 + 색인, 위에서 k개</td><td>6-1 창고 지도</td></tr>'
                 '<tr><td>붙이기</td><td>프로그램</td><td>조각의 글을 프롬프트에</td><td>6-1 프롬프트 줄</td></tr>'
                 '<tr><td>읽기</td><td>LLM (트랜스포머)</td><td>토큰 + 위치 → 여러 머리 어텐션 × 여러 층</td><td>6-2 ~ 6-4</td></tr>'
                 '<tr><td>쓰기</td><td>LLM</td><td>마지막 좌표 · 낱말 좌표 내적 → softmax</td><td>6-5</td></tr></table></div>'
                 '<p>근거 조각 수에 따른 어텐션 집중도 (β = 8): k = 1 → %s (정답 조각을 가져온 질문 %d/%d), k = 2 → %s (%d/%d), k = 3 → %s, k = 5 → %s (%d/%d). 많이 붙이면 정답 조각이 들어갈 가능성은 오르지만, 어텐션은 흩어집니다.</p>' % (
                     num(AT['k1']['focus'], 3), AT['k1']['hit'], AT['k1']['n'], num(AT['k2']['focus'], 3), AT['k2']['hit'], AT['k2']['n'], num(AT['k3']['focus'], 3), num(AT['k5']['focus'], 3), AT['k5']['hit'], AT['k5']['n'])
                 + bridge('gen', '생성 AI로 치면', '긴 문서를 통째로 붙여 물어보면 앞이나 뒤의 내용은 잘 쓰고 가운데 내용은 놓치는 경향이 보고되었습니다. 어텐션이 긴 프롬프트에서 고르게 머물지 않는다는 뜻입니다. 그래서 RAG는 "많이"보다 "알맞게" 붙입니다.',
                          '이 장의 3D 그림과 계산은 원리를 보이는 장난감입니다. 실제 모델의 어텐션 모양은 모델·층·머리마다 크게 다릅니다.'))

    b += outro([('doc', 'front', '오늘 세 줄 정리. ① 벡터 DB는 "무엇을 읽힐지" 고르고, 어텐션은 "읽힌 것 중 어디를 볼지" 정한다. ② 어텐션은 Q·K 내적 → softmax → V 섞기, 모델 안의 부드러운 벡터 검색이다. ③ 근거는 알맞게, 서로 다르지 않게 붙인다.'),
                ('fly', 'arms', '많이 붙인다고 많이 읽는 게 아니야. 어텐션도 한정된 비율을 나눠 쓰니까.'),
                ('robo', 'sigh', '5개면 안전할 줄 알았는데… 정답이 들어가도 묻혀 버리는구나.'),
                ('sia', 'proud', '제 질문 "어텐션이 창고를 뒤지나요?"에 이제 답할 수 있어요. 아니요, 붙여 준 글을 읽어요!'),
                ('moa', 'sparkle', '3층 탑 그림, 노트에 옮겨 그렸어요.'),
                ('asst', 'e16', '오늘이 제일 어려웠는데, 3D로 돌려 보니 저도 처음으로 확실히 알았어요. 다음은 지식 그래프예요!')],
               '하루와 인턴들이 3D 홀로그램처럼 떠 있는 토큰 탑을 둘러싸고 선을 가리키는 장면',
               crowd('"3D 탑 멋있다!" "하루가 시아 질문 덕분에 더 깊이 설명했어."', moods=('e04', 'e01', 'e16')))
    return b


GLOSS = {
    '어텐션': ['어텐션 (attention)', '토큰마다 Q로 묻고 다른 토큰의 K와 내적해 비율을 정한 뒤, 그 비율로 V를 섞어 가져오는 계산.'],
    '트랜스포머': ['트랜스포머 (Transformer)', '여러 머리의 어텐션과 계산 층을 여러 층 쌓은 모델 구조. 2017년 「Attention Is All You Need」에서 제안.'],
    '토큰': ['토큰 (token)', '모델이 글을 다루는 조각. 낱말이나 낱말 일부.'],
    '위치 정보': ['위치 정보 (positional encoding)', '토큰이 몇 번째인지를 좌표에 새기는 방법. 사인 물결, 좌표 돌리기(RoPE) 등.'],
    'softmax': ['softmax', '점수들을 e의 거듭제곱으로 키운 뒤 합으로 나눠, 합이 1인 비율로 바꾸는 계산.'],
    'Q·K·V': ['Q·K·V', 'Query(무엇을 찾나)·Key(나는 이런 내용)·Value(가져갈 내용). 토큰 좌표에 서로 다른 학습된 행렬을 곱해 만듭니다.'],
    '머리': ['머리 (attention head)', '서로 다른 Q·K·V로 서로 다른 관계를 보는 어텐션 하나. 여러 개를 나란히 씁니다.'],
    '잔차 연결': ['잔차 연결 (residual connection)', '층의 출력을 입력에 더해 넘기는 구조. 원래 정보를 잃지 않게 합니다.'],
    'FFN': ['계산 층 (FFN)', '어텐션 뒤 토큰마다 따로 거치는 두 겹짜리 계산 층.'],
    '임베딩 모델': ['임베딩 모델', '문장을 좌표 하나로 바꾸는 모델. 안에 트랜스포머(어텐션)가 있습니다. 벡터 DB에 넣을 좌표를 만듭니다.'],
}

QUIZ = {
    'q61': [{'q': 'RAG에서 LLM이 벡터 DB로부터 실제로 받는 것은?', 'o': ['조각의 좌표', '조각의 글(프롬프트에 붙은)', '창고 전체'], 'a': 1,
             'why': '검색기가 찾은 조각의 글을 프롬프트에 붙여 줍니다. LLM은 그 글을 토큰으로 잘라 다시 자기 좌표로 바꿔 읽습니다.', 'hint': '프롬프트 줄의 경계선을 떠올려 보세요.'},
            {'q': '어텐션이 쓰이는 곳으로 맞는 것은?', 'o': ['벡터 DB 색인에서 가까운 조각을 고를 때만', '임베딩 모델 안(넣을 때)과 LLM 안(읽을 때)', '어디에도 안 쓰인다'], 'a': 1,
             'why': '임베딩 모델과 LLM은 둘 다 트랜스포머라 어텐션을 씁니다. 창고에서 고르는 일은 코사인과 색인이 합니다.', 'hint': '넣기·찾기·읽기 중 찾기는 무엇으로 하나요?'}],
    'q62': [{'q': '위치 정보를 더하는 이유는?', 'o': ['토큰 수를 줄이려고', '같은 낱말이라도 몇 번째 자리인지 알게 하려고', '좌표를 0으로 만들려고'], 'a': 1,
             'why': '어텐션 자체는 순서를 모릅니다. 위치 좌표를 더해 순서를 좌표에 새깁니다.', 'hint': '두 "환불" 점이 겹치는지 떨어지는지.'},
            {'q': '물결 길이 2일 때 자리 1의 위치 값 sin(0.5)는 대략?', 'o': ['0', '0.48', '1'], 'a': 1,
             'why': 'sin(0.5) ≈ 0.479.', 'hint': '자리 ÷ 물결 길이 = 0.5'}],
    'q63': [{'q': '점수 2, 1, 0의 softmax 비율로 맞는 것은?', 'o': ['0.67, 0.24, 0.09', '0.5, 0.33, 0.17', '1, 0, 0'], 'a': 0,
             'why': 'e² : e¹ : e⁰ = 7.39 : 2.72 : 1, 합 11.11로 나누면 0.665, 0.245, 0.090.', 'hint': 'e의 거듭제곱으로 키운 뒤 합으로 나눕니다.'},
            {'q': '어텐션과 3장 벡터 검색의 가장 큰 차이는?', 'o': ['어텐션은 내적을 안 쓴다', '어텐션은 위에서 k개만 고르지 않고 모두에게 비율을 나눠 섞는다', '어텐션은 창고 전체를 뒤진다'], 'a': 1,
             'why': '둘 다 내적으로 닮음을 재지만, 어텐션은 softmax로 부드럽게 섞고 프롬프트 안에서만 일합니다.', 'hint': '딱딱한 선택과 부드러운 선택.'}],
    'q64': [{'q': '머리를 여러 개 두는 이유는?', 'o': ['계산을 줄이려고', '뜻·순서·글자 같은 여러 관계를 동시에 보려고', '토큰을 늘리려고'], 'a': 1,
             'why': '머리마다 다른 Q·K·V로 다른 관계를 봅니다.', 'hint': '여러 팀의 동시 검토.'},
            {'q': '층을 지날수록 토큰 좌표는?', 'o': ['처음과 같다', '주변 토큰의 정보가 점점 더 섞인다', '0이 된다'], 'a': 1,
             'why': '층마다 자기 좌표에 어텐션으로 섞어 온 좌표를 더해(잔차 연결) 넘깁니다.', 'hint': '위판의 선이 아래 여러 토큰으로 이어집니다.'}],
    'q65': [{'q': '근거 없이 물었을 때 틀린 "14일"이 나오는 이유(이 실험의 가정)는?', 'o': ['어텐션이 근거에 비율을 줘서', '학습 때 자주 본 말의 점수만 남아서', 'softmax가 틀려서'], 'a': 1,
             'why': '붙인 근거가 없으면 평소 자주 본 말의 점수가 그대로 남습니다. 4장의 환각과 같은 이야기입니다.', 'hint': '근거 토큰에 간 어텐션이 0이면?'},
            {'q': '현행·구버전 규정을 둘 다 붙이면?', 'o': ['3일만 확실히 나온다', '3일과 7일이 함께 올라 답이 흔들린다', '14일이 나온다'], 'a': 1,
             'why': '어텐션이 두 근거에 비율을 나누고, 두 숫자의 점수가 함께 오릅니다. 날짜 필터가 필요한 이유입니다.', 'hint': '4-5의 함정을 떠올려 보세요.'}],
}

JS = r'''
var D=VL.load(),RQ=D.ragq,CH=VL.chunk(D.kb,150,0,true),DOCC=['#1e55c8','#13733a','#c42a6e','#a35c00','#9b3fb5','#0b7a86','#5b6874','#8f5a2e','#2f7d32','#b23a48','#3949ab','#6d4c41'],DOCI={};D.kb.forEach(function(k,i){DOCI[k.id]=i});
function rotBtn(id,v){$(id).addEventListener('click',function(){var on=v.toggleAuto();this.setAttribute('aria-pressed',on?'true':'false');});if(window.REDUCED)$(id).setAttribute('aria-pressed','false');}
function scale3(xyz){var m=1e-9;xyz.forEach(function(p){p.forEach(function(x){m=Math.max(m,Math.abs(x))})});return xyz.map(function(p){return p.map(function(x){return x/m*.95})});}
/* 6-1 */
(function(){var qs=RQ.filter(function(q){return q.doc});$('#q61').innerHTML=qs.map(function(q,i){return '<option value="'+i+'">'+q.q+'</option>'}).join('');
  var pc=VL.pcaK(CH.map(function(c){return c.vec}),3),pts=scale3(pc.xyz.concat(qs.map(function(q){return pc.proj(VL.embed(q.q).v)}))),cp=pts.slice(0,CH.length),qp=pts.slice(CH.length);
  var v=VL.view3d($('#cv61'),{stamp:'24차원 → 3축 (PCA)'});rotBtn('#rot61',v);
  function run(){var i=+$('#q61').value,q=qs[i],k=+$('#k61').value;$('#kv61').textContent=k+'개';var h=VL.retrieve(CH,q.q,{k:k,alpha:.3,newest:true}),ids=h.map(function(x){return x.c.id});
    var it=cp.map(function(p,j){var on=ids.indexOf(j)>=0;return {p:p,r:on?7:4.5,c:DOCC[DOCI[CH[j].doc]%DOCC.length],al:on?1:.45,label:on?CH[j].title:null,bold:on,ring:on?'#c9302c':null}});
    ids.forEach(function(j){it.push({t:'ln',a:qp[i],b:cp[j],c:'#c9302c',w:2.5,al:.9})});it.push({p:qp[i],star:true,c:'#c9302c'});v.set(it);
    $('#pr61').innerHTML='<span>[지시] 자료로만 답하세요</span>'+h.map(function(x,n){return '<span class="on">[자료 '+(n+1)+'] '+VL.esc(x.c.text.slice(0,26))+'…</span>'}).join('')+'<span>[질문] '+VL.esc(q.q)+'</span>';
    var gold=h.some(function(x){return x.c.text.indexOf(q.key)>=0});
    $('#in61').innerHTML='<p class="m"><b>경계</b> 3D 지도(좌표) → 프롬프트 줄(글). 모델은 오른쪽 줄만 받습니다.</p><p class="'+(gold?'g':'r')+'">'+(gold?'정답 문구 "'+q.key+'"가 든 조각이 프롬프트 줄에 올라갔습니다. 이제 읽기(어텐션)의 몫입니다.':'정답 조각이 줄에 없습니다. 이 경우 틀린 답은 "찾기"의 잘못입니다. k를 늘려 보세요.')+'</p>';}
  $('#q61').addEventListener('change',run);$('#k61').addEventListener('input',run);run();
})();
/* 6-2 */
(function(){var pe=true,v=VL.view3d($('#cv62'),{stamp:'토큰 좌표 + 위치 나선'});rotBtn('#rot62',v);
  function run(){var tk=VL.tokens($('#t62').value).slice(0,24),vec=tk.map(function(w){return VL.embed(w).v}),nz=vec.filter(function(x){return VL.norm(x)>0});
    var pc=nz.length>=3?VL.pcaK(nz,3):null,base=vec.map(function(x){return VL.norm(x)>0&&pc?pc.proj(x):[0,0,0]}),m=1e-9;base.forEach(function(p){p.forEach(function(x){m=Math.max(m,Math.abs(x))})});base=base.map(function(p){return p.map(function(x){return x/m*.6})});
    var P=base.map(function(p,i){if(!pe)return p;var a=i*.9;return [p[0]+.35*Math.cos(a),p[1]+(i/(tk.length-1||1))*1.4-.7,p[2]+.35*Math.sin(a)];});
    var seen={},it=[];P.forEach(function(p,i){var dup=tk.filter(function(w){return w===tk[i]}).length>1;it.push({p:p,r:dup?7:5,c:dup?'#c42a6e':(VL.norm(vec[i])>0?'#1e55c8':'#9aa6b2'),label:tk[i],bold:dup});if(i)it.push({t:'ln',a:P[i-1],b:p,c:'#a35c00',w:1.5,al:.6});});v.set(it);
    $('#tk62').innerHTML=tk.map(function(w,i){return '<span'+(tk.filter(function(x){return x===w}).length>1?' class="on"':'')+'>'+i+' · '+VL.esc(w)+'</span>'}).join('');
    var d=null;tk.forEach(function(w,i){var j=tk.indexOf(w);if(j!==i&&d===null)d=[j,i];});
    $('#in62').innerHTML=d?'<p class="'+(pe?'g':'r')+'">"'+VL.esc(tk[d[0]])+'"이 '+d[0]+'번째와 '+d[1]+'번째에 있습니다. 두 점 사이 거리: '+VL.euclid(P[d[0]],P[d[1]]).toFixed(2)+(pe?' — 위치 정보 덕분에 떨어져 있습니다.':' — 위치 정보가 없으면 완전히 겹칩니다.')+'</p>':'<p class="m">같은 낱말을 두 번 넣어 보세요.</p>';}
  $('#t62').addEventListener('input',run);$('#pe62').addEventListener('click',function(){pe=!pe;this.setAttribute('aria-pressed',pe?'true':'false');run();});run();
})();
/* 6-3 */
(function(){var wq=false,qs=RQ.filter(function(q){return q.doc});$('#q63').innerHTML=qs.map(function(q,i){return '<option value="'+i+'">'+q.q+'</option>'}).join('');
  var v=VL.view3d($('#cv63'),{stamp:'굵기 = 어텐션 비율'});rotBtn('#rot63',v);var NUMD=[16,9,22,19];
  function tv(w){var x=VL.embed(w).v.slice();x.push(/[0-9]/.test(w)?1:0);var n=VL.norm(x);return n?x.map(function(a){return a/n}):x;}
  function run(){var q=qs[+$('#q63').value],beta=+$('#b63').value;$('#bv63').textContent=beta;var h=VL.retrieve(CH,q.q,{k:2,alpha:.3,newest:true}),T=[];
    h.forEach(function(x){VL.tokens(x.c.text).forEach(function(w){T.push({w:w,v:tv(w),gold:x.c.text.indexOf(q.key)>=0&&w.indexOf(q.key.split(' ')[0])>=0})})});
    var qv=VL.embed(q.q).v.slice();qv.push(0);if(wq){var s=NUMD.reduce(function(a,d){return a+Math.max(0,qv[d])},0);qv[24]+=1.6*s+.4;}var n=VL.norm(qv)||1;qv=qv.map(function(a){return a/n});
    var w=VL.softmax(T.map(function(t){return VL.dot(qv,t.v)}),beta);T.forEach(function(t,i){t.a=w[i]});
    var nz=T.filter(function(t){return VL.norm(t.v)>0}).map(function(t){return t.v});var pc=VL.pcaK(nz.concat([qv]),3),P=scale3(T.map(function(t){return VL.norm(t.v)>0?pc.proj(t.v):[0,0,0]}).concat([pc.proj(qv)]));
    var jit=VL.rng(5);P=P.map(function(p,i){return i<T.length&&VL.norm(T[i].v)===0?[(jit()-.5)*.5,(jit()-.5)*.5,(jit()-.5)*.5]:p});var qp=P[T.length],mx=Math.max.apply(null,w);
    var it=T.map(function(t,i){return {p:P[i],r:3+9*t.a/mx,c:/[0-9]/.test(t.w)?'#a35c00':'#1e55c8',al:.35+.65*t.a/mx,label:t.a/mx>.35?t.w:null,bold:t.a/mx>.7}});
    T.forEach(function(t,i){if(t.a/mx>.08)it.push({t:'ln',a:qp,b:P[i],c:'#c9302c',w:.5+7*t.a/mx,al:.25+.6*t.a/mx})});it.push({p:qp,star:true,c:'#c9302c'});v.set(it);
    var top=T.map(function(t,i){return [t.a,i]}).sort(function(a,b){return b[0]-a[0]}).slice(0,8);
    $('#vb63').innerHTML=top.map(function(x){var t=T[x[1]];return '<div class="vb"><span>'+VL.esc(t.w)+'</span><div class="tr"><div class="fl" style="width:'+Math.round(x[0]/top[0][0]*100)+'%;'+(/[0-9]/.test(t.w)?'background:#a35c00':'')+'"></div></div><span class="v">'+VL.pct(x[0],1)+'</span></div>'}).join('');
    var out=new Array(25).fill(0);T.forEach(function(t){t.v.forEach(function(a,j){out[j]+=t.a*a})});VL.dimBars($('#ov63'),out.slice(0,24),{top:6});
    var gm=T.filter(function(t){return /[0-9]/.test(t.w)}).reduce(function(a,t){return a+t.a},0),ent=-w.reduce(function(a,x){return a+(x>0?x*Math.log(x):0)},0)/Math.log(w.length);
    VL.kpis($('#k63'),[[T.length+'개','프롬프트 토큰 (조각 2개)','i'],[VL.pct(top[0][0]),'가장 큰 비율 ("'+T[top[0][1]].w+'")','g'],[VL.pct(gm),'숫자가 든 토큰에 간 몫','a'],[ent.toFixed(2),'퍼짐 정도 (1 = 고르게)','m']]);
    $('#in63').innerHTML='<p class="'+(wq?'a':'m')+'">'+(wq?'Q 변환이 켜져 있습니다. 질문의 요금·기간·속도 성분이 "숫자 토큰을 찾아라"로 바뀌어 주황 점(숫자 토큰)에 비율이 몰립니다.':'Q = 질문 좌표 그대로입니다. 뜻이 비슷한 낱말(파랑)에 비율이 갑니다. "Q 변환"을 켜 보세요.')+'</p><p class="m">β를 1로 내리면 고르게 퍼지고(퍼짐 정도 → 1), 16으로 올리면 몇 개로 쏠립니다.</p>';}
  $('#q63').addEventListener('change',run);$('#b63').addEventListener('input',run);$('#wq63').addEventListener('click',function(){wq=!wq;this.setAttribute('aria-pressed',wq?'true':'false');run();});run();
})();
/* 6-4 */
(function(){var head='mean',sel=null,v=VL.view3d($('#cv64'),{stamp:'3층 · 머리 셋',pitch:.55,onPick:function(id){if(typeof id==='number'&&id>=0){sel=id;run();}}});rotBtn('#rot64',v);
  var tk=VL.tokens('[자료] LP-204는 결제 수단이 만료되었거나 한도가 부족할 때 나타나는 결제 오류입니다 [질문] LP-204 오류가 떠요'),n=tk.length;sel=n-3;
  function grams(w){return VL.grams(w)}
  function score(hd,i,j,H){if(hd==='mean')return 4*VL.cos(H[i],H[j]);if(hd==='pos')return j===i-1?3:(j===i?1.5:(Math.abs(i-j)<=2?.8:0));var A=grams(tk[i]),B=grams(tk[j]),c=A.filter(function(x){return B.indexOf(x)>=0}).length;return c?3*c/Math.max(A.length,1):0;}
  function attn(hd,i,H){var heads=hd==='all'?['mean','pos','char']:[hd],out=new Array(n).fill(0);heads.forEach(function(h){var w=VL.softmax(H.map(function(_,j){return j>i?-Infinity:score(h,i,j,H)}),1.6);w.forEach(function(x,j){out[j]+=x/heads.length})});return out;}
  var H0=tk.map(function(w){var x=VL.embed(w).v;return VL.norm(x)?x:new Array(24).fill(0).map(function(_,j){return j===((w.length*7)%24)?.3:0})});
  function layer(H){return H.map(function(h,i){var w=attn('all',i,H),mix=new Array(24).fill(0);w.forEach(function(a,j){H[j].forEach(function(x,d){mix[d]+=a*x})});var o=h.map(function(x,d){return x+mix[d]}),nn=VL.norm(o)||1;return o.map(function(x){return x/nn})});}
  var L=[H0,layer(H0)];L.push(layer(L[1]));
  function pos(l,i){return [(i/(n-1))*1.8-.9,l*.85-.85,Math.sin(i*.7)*.18]}
  function run(){var it=[];[0,1,2].forEach(function(l){it.push({t:'pl',q:[[-1,l*.85-.85,-.5],[1,l*.85-.85,-.5],[1,l*.85-.85,.5],[-1,l*.85-.85,.5]],c:'#1e55c8',al:.06});
      tk.forEach(function(w,i){it.push({p:pos(l,i),r:l===2&&i===sel?8:4,c:l===2&&i===sel?'#c9302c':'#5b6874',al:.85,label:(l===0||(l===2&&i===sel))?w:null,bold:l===2&&i===sel,id:l===2?i:undefined})});});
    var w2=attn(head,sel,L[1]),mx=Math.max.apply(null,w2);w2.forEach(function(a,j){if(a/mx>.1)it.push({t:'ln',a:pos(2,sel),b:pos(1,j),c:'#c9302c',w:.5+5*a/mx,al:.3+.6*a/mx})});
    var w1=attn(head,sel,L[0]),m1=Math.max.apply(null,w1);w1.forEach(function(a,j){if(a/m1>.15)it.push({t:'ln',a:pos(1,sel),b:pos(0,j),c:'#a35c00',w:.5+4*a/m1,al:.25+.5*a/m1})});v.set(it);
    var top=w2.map(function(a,j){return [a,j]}).sort(function(a,b){return b[0]-a[0]}).slice(0,3);
    $('#tk64').innerHTML=tk.map(function(w,i){return '<span'+(i===sel?' class="on"':'')+'>'+VL.esc(w)+'</span>'}).join('');
    $('#in64').innerHTML='<p class="m">"'+VL.esc(tk[sel])+'"이(가) '+{mean:'뜻 머리',pos:'위치 머리',char:'글자 머리',all:'세 머리 평균'}[head]+'로 가장 많이 본 곳: '+top.map(function(x){return '"'+VL.esc(tk[x[1]])+'" '+VL.pct(x[0],0)}).join(', ')+'.</p>';}
  $$('#p64 [data-h]').forEach(function(b){b.addEventListener('click',function(){head=b.dataset.h;$$('#p64 [data-h]').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});run();})});run();
})();
/* 6-5 */
(function(){var ctx='new',q='어제 결제했는데 아무것도 안 봤어요. 돈 돌려받을 수 있나요?',prior={'3일':.2,'7일':.3,'14일':.5},C=['3일','7일','14일'];
  function run(){var g=+$('#g65').value;$('#gv65').textContent=g;var docs=ctx==='none'?[]:ctx==='new'?['refund_v2']:ctx==='old'?['refund_v1']:['refund_v2','refund_v1'],T=[];
    docs.forEach(function(id){var d=D.kb.filter(function(k){return k.id===id})[0];VL.tokens(d.text).forEach(function(w){T.push(w)})});
    VL.tokens(q).forEach(function(w){T.push(w)});var qv=VL.embed(q).v,w=VL.softmax(T.map(function(t){var x=VL.embed(t).v;return VL.dot(qv,x)+(/일/.test(t)&&/[0-9]/.test(t)?.6:0)}),8);
    var mass=C.map(function(c){return T.reduce(function(a,t,i){return a+(t.indexOf(c)===0?w[i]:0)},0)}),sc=C.map(function(c,i){return Math.log(prior[c])+g*mass[i]}),p=VL.softmax(sc,1);
    $('#at65').innerHTML=C.map(function(c,i){return '<div class="vb"><span>"'+c+'" 토큰</span><div class="tr"><div class="fl" style="width:'+Math.round(Math.min(1,mass[i]*3)*100)+'%"></div></div><span class="v">'+VL.pct(mass[i],1)+'</span></div>'}).join('');
    $('#pb65').innerHTML=C.map(function(c,i){return '<div class="vb"><span>'+c+'</span><div class="tr"><div class="fl" style="width:'+Math.round(p[i]*100)+'%;background:'+(c==='3일'?'#13733a':'#c9302c')+'"></div></div><span class="v">'+VL.pct(p[i],0)+'</span></div>'}).join('');
    var win=C[p.indexOf(Math.max.apply(null,p))];
    $('#in65').innerHTML='<p class="'+(win==='3일'?'g':'r')+'">가장 높은 다음 말: <b>'+win+'</b>. '+(ctx==='none'?'근거가 없어 평소 자주 본 말이 이겼습니다(환각).':ctx==='both'?'두 판의 숫자가 함께 올라 답이 흔들립니다. 4-5의 날짜 필터가 필요한 이유입니다.':ctx==='old'?'옛 규정만 붙이니 그대로 옛 답을 씁니다. 모델은 판을 가리지 못합니다.':'현행 근거를 따라 맞는 답이 나옵니다.')+'</p><p class="m">γ를 0으로 내리면 근거를 무시하고 평소 기억만 씁니다.</p>';}
  $$('#p65 [data-c]').forEach(function(b){b.addEventListener('click',function(){ctx=b.dataset.c;$$('#p65 [data-c]').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});run();})});$('#g65').addEventListener('input',run);run();
})();
/* 대결 6 */
Duel({el:'#d6',run:function(){var A=RQ.filter(function(q){return q.doc});function f(k){var t=0;A.forEach(function(q){var h=VL.retrieve(CH,q.q,{k:k,alpha:.3,newest:true}),qv=VL.embed(q.q).v,T=[];
      h.forEach(function(x){VL.tokens(x.c.text).forEach(function(w){T.push({v:VL.embed(w).v,g:x.c.text.indexOf(q.key)>=0})})});var w=VL.softmax(T.map(function(x){return VL.dot(qv,x.v)}),8);t+=T.reduce(function(a,x,i){return a+(x.g?w[i]:0)},0);});return t/A.length;}
    return {fly:f(2),robo:f(5)}},scale:1,fmt:function(v){return VL.pct(v,1)},bigGap:.2,
  report:function(r){return '정답 조각에 머문 어텐션: 2개 붙이면 '+VL.pct(r.fly,1)+', 5개 붙이면 '+VL.pct(r.robo,1)+'. 다만 5개면 정답 조각이 14개 질문 모두에 들어가고, 2개면 13개에 들어가요.'},
  verdict:{fly:'초파리 승. 많이 붙이면 정답 조각이 들어갈 확률은 오르지만, 어텐션은 엉뚱한 조각에도 비율을 나눠 줘서 흩어집니다. 그래서 RAG는 "찾기의 재현율"과 "읽기의 집중"을 함께 봐야 합니다. 이 숫자는 교육용 좌표로 흉내 낸 값입니다.',robo:'주판봇 승.',draw:'무승부.'}});
'''


def build_page():
    nav = [('#s1', '6-1 경계'), ('#s2', '6-2 토큰'), ('#s3', '6-3 어텐션'), ('#s4', '6-4 층'), ('#s5', '6-5 다음 말'), ('#duel', '대결'), ('#sum', '정리')]
    cov = cover('cover_07', '벡터 DB 연구실 · 6장', 'LLM은 찾은 자료를 어떻게 읽나', chars=(('doc', 'front'), ('asst', 'e16'), ('fly', 'magnify'), ('robo', 'wow')))
    hr = hero('벡터 DB 연구실 · 6장 · 어텐션과 트랜스포머를 3D로', 'LLM은 찾은 자료를 어떻게 읽나',
              '벡터 DB가 찾아 준 글을, LLM은 어텐션으로 어떻게 읽고 답을 고를까?',
              '특강 첫날. 인턴 시아가 "LLM이 어텐션으로 벡터 DB에서 말을 꺼내 오나요?"라고 묻습니다. 하루는 당황하지 않고 3D 그림을 돌리며 찾기와 읽기의 경계부터 짚습니다.',
              [('5개', '3D·동적 실험 (창고 지도, 토큰 나선, 어텐션, 3층 탑, 다음 말)', 'i'), (num(AT['k2']['focus'], 3), '근거 2개일 때 정답 조각에 머문 어텐션', 'g'),
               (num(AT['k5']['focus'], 3), '근거 5개일 때', 'a'), ('%s · %s · %s' % (num(SX[0], 2), num(SX[1], 2), num(SX[2], 2)), '점수 2·1·0의 softmax', 'm')],
              [('doc', 'front', '오늘은 특강입니다. 4장에서 "LLM이 붙여 준 자료를 읽는다"고만 했죠. 그 "읽기"를 열어 봅니다.'),
               ('sia', 'think', '하루 선배, LLM이 어텐션으로 벡터 DB에서 말을 꺼내 오는 거 아니에요?'),
               ('asst', 'e13', '좋은 질문! 반은 맞아요. 3D로 같이 돌려 보면서 어디까지 맞는지 찾아봐요.'), ('moa', 'report', '3D요? 노트 두 쪽 비워 둘게요!')],
              crowd('"하루, 오늘은 시작부터 여유 있다!" "3D 기대돼."', moods=('e16', 'e01', 'e04')))
    return build(P, title='6장 · LLM은 찾은 자료를 어떻게 읽나 — 어텐션과 트랜스포머를 3D로 | 벡터 DB 연구실',
                 desc='벡터 DB 검색(모델 밖)과 어텐션 읽기(모델 안)의 경계, 토큰과 위치, Q·K·V 어텐션, 여러 머리와 층, 다음 말 고르기를 3D 실험으로 봅니다.',
                 nav=nav, cover_html=cov, hero=hr,
                 body=body() + footer([('트랜스포머·어텐션·위치 정보', 'Vaswani 외 (2017) Attention Is All You Need, NeurIPS 2017'),
                                       ('RAG', 'Lewis 외 (2020) Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks, NeurIPS 2020'),
                                       ('긴 프롬프트의 가운데 놓침', 'Liu 외 (2024) Lost in the Middle: How Language Models Use Long Contexts, TACL 12'),
                                       ('좌표 돌리기 위치 정보 (RoPE)', 'Su 외 (2024) RoFormer: Enhanced Transformer with Rotary Position Embedding, Neurocomputing 568'),
                                       ('랩플릭스 안내 문서', '이 연구실이 만든 가상 데이터'), ('트랜스포머 강의', '<a href="%s">인공지능과 자연어 데이터 분석 강좌</a> 8장' % NLP)],
                                      ['어텐션 계산은 24차원 교육용 좌표로 흉내 낸 설명용입니다(Q = K = V, 숫자 표시 성분 하나 추가).', 'Q 변환, 세 머리의 규칙, 다음 말의 "평소 자주 본 정도"와 γ는 사람이 정한 가정입니다.',
                                       '3D 그림은 24차원을 PCA로 세 축에 눌러 담은 것이라 실제 거리와 다릅니다.'],
                                      prev=('05_cases.html', '5장 · 현장 사례'), nxt=('07_graph_ontology.html', '7장 · 좌표와 관계')),
                 gloss=GLOSS, quizzes=QUIZ, page_js=JS, og='og_07')


if __name__ == '__main__':
    print(build_page())
