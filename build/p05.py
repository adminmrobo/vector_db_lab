# -*- coding: utf-8 -*-
"""5장 · 현장 사례 — 영화 추천, SNS 모니터링, LLM의 기억, 도입 판단"""
from lib import *

P = '05_cases.html'
SP = R['spam']; MS = {x['title']: x['best'] for x in R['movie_sim']}; PR = R['pref_rank']


def body():
    b = three([
        ('무엇을', '1~4장에서 만든 도구로 현장 문제 네 가지를 풉니다. 영화 추천(별점 + 리뷰 좌표), SNS 모니터링(광고 걸러내기·새 이슈 알아차리기), 챗봇의 기억(대화 기억 창고), 그리고 "우리 회사에 벡터 DB가 필요한가" 판단.'),
        ('왜 중요한가', '벡터 DB는 그 자체가 목적이 아니라, 추천·검색·감시·기억 같은 기능의 부품입니다. 어느 자리에 끼우면 효과가 있고, 어디서는 표만으로 충분한지 가르는 눈이 필요합니다.'),
        ('업무에서는', '기획서에 "벡터 DB 도입"이 나오면 무엇을 저장하고, 어떤 질문을 받고, 무엇으로 채점할지 바로 물을 수 있게 됩니다.')],
        '코드·수식을 몰라도 됩니다. 장면마다 조작판을 움직여 결과가 어떻게 바뀌는지 보세요.',
        [('pgvector', 'PostgreSQL의 벡터 확장'), ('CLIP', '그림과 글을 같은 좌표 공간에 놓는 임베딩 모델'), ('F1', '정밀도·재현율을 함께 본 점수')])

    b += section('map', '큰 그림 — 이 장은 어디쯤인가',
                 '<div class="mapbar"><span>1장 · 표의 한계</span><i>→</i><span>2장 · 임베딩</span><i>→</i><span>3장 · 벡터 창고</span><i>→</i><span>4장 · LLM과 RAG</span><i>→</i><span class="on">5장 · 현장 사례</span><i>→</i><span>6장 · 어텐션 3D</span><i>→</i><span>7장 · 그래프·온톨로지</span><i>→</i><span>실전 연습장</span></div>'
                 '<div class="tw"><table class="tb"><tr><th>사례</th><th>표(관계형 DB)가 맡는 것</th><th>벡터가 맡는 것</th><th>다시 쓰는 장</th></tr>'
                 '<tr><td>5-1 영화 추천</td><td>별점, 장르, 상영 시간</td><td>리뷰로 만든 영화의 분위기 좌표</td><td>2장 임베딩, 3장 필터</td></tr>'
                 '<tr><td>5-2 SNS 모니터링</td><td>날짜, 신고 기록</td><td>광고와 닮은 글, 처음 보는 이야기</td><td>1장 규칙의 한계, 2장 유사도</td></tr>'
                 '<tr><td>5-3 챗봇의 기억</td><td>대화 날짜, 사용자 번호</td><td>지금 질문과 가까운 지난 대화</td><td>4장 RAG</td></tr>'
                 '<tr><td>5-4 도입 판단</td><td colspan="2">질문 종류·데이터 양·보안으로 구조를 고름</td><td>3장 역할 분담</td></tr></table></div>')

    # ── 5-1 추천
    s = say('doc', 'think', '상황 하나. 랩플릭스가 "이 영화를 좋아한 사람에게 비슷한 영화를 추천"하고 싶어 합니다. 별점 평균만 보면 될까요?')
    s += duo(why([('문제 상황', '좋아한 영화와 "분위기가 비슷한" 영화를 골라야 합니다.'),
                  ('앞 방법의 한계', '별점 평균순 추천은 모두에게 같은 영화(평균 높은 영화)를 내밉니다. 공포를 좋아한 사람에게 가족 애니메이션을 추천하기도 합니다.'),
                  ('해법', '영화마다 별점 4점 이상 리뷰의 좌표를 평균해 "그 영화를 좋아한 이유"의 좌표를 만듭니다. 이 좌표끼리 가까운 영화를 추천하고, 별점·장르는 표에서 조건으로 겁니다.')],
                 '"이 책 좋아했으면 이것도"는 책의 줄거리가 아니라, 그 책을 좋아한 사람들이 남긴 말이 닮은 책을 고르는 것입니다.'),
             mathbox('영화 하나의 좌표는 어떻게 만들어요?', '평균 (중학교) — 성분끼리 더해서 개수로 나누기',
                     '영화 좌표 = (별점 4점 이상 리뷰 좌표들의 합) ÷ 리뷰 수',
                     [('리뷰 좌표', '', '2장의 문장 임베딩'), ('4점 이상', '', '표(별점)로 먼저 거른 조건 — "좋아한 이유"만 모으려고'), ('÷ 리뷰 수', '', '성분마다 평균')],
                     '리뷰 두 개 (재미 0.8, 좋음 0.6)과 (감동 0.8, 좋음 0.6)의 평균 = <b>(재미 0.4, 감동 0.4, 좋음 0.6)</b>. 재미와 감동이 반반인 영화 좌표가 됩니다.',
                     '별점(표)으로 거르고, 좌표(벡터)로 평균 내고. 두 창고를 같이 쓰는 거네요!'))
    s += talk([('asst', 'e13', '시아, 「검은 서버실」을 좋아한 사람한테 뭘 추천하면 좋을까?'),
               ('sia', 'think', '별점 평균이 제일 높은 「주판왕의 비밀」이요?'),
               ('robo', 'chart', '맞아, 평균 높은 게 최고야. 다 그거 추천하면 돼!'),
               ('fly', 'point', '평균은 모두에게 같아. 아래에서 「검은 서버실」을 고르고 좌표로 가까운 영화를 봐. 「붉은 계단」을 고르면 결과가 달라지나?'),
               ('asst', 'report', '「검은 서버실」엔 「%s」(%s), 「붉은 계단」엔 「%s」(%s)가 가장 가까워요. 영화마다 다르게 나와요.' % (MS['검은 서버실'][0], num(MS['검은 서버실'][1], 2), MS['붉은 계단'][0], num(MS['붉은 계단'][1], 2)))])
    s += panel('p51', '실험 · 리뷰 좌표로 만든 영화 추천기', '가상 데이터 · 페이지가 직접 계산',
               '<div class="ctrl"><div class="group"><span class="glabel">좋아한 영화</span><select class="sel" id="m51"></select></div>'
               '<div class="group"><span class="glabel">또는 취향 문장</span><input type="text" id="t51" placeholder="예: 무섭고 반전 있는 영화" aria-label="취향 문장"></div></div>'
               '<div class="ctrl"><div class="group"><span class="glabel">평균 별점 조건</span><input type="range" id="s51" min="1" max="4.5" step="0.1" value="3" aria-label="평균 별점 이상"><span class="val" id="sv51"></span></div>'
               '<div class="group"><span class="glabel">상영 시간</span><button class="bt" id="r51" aria-pressed="false">2시간 이하만</button></div></div>'
               '<div class="sqlbox" id="sql51"></div>' + canvas('cv51', 260, '영화별 닮음 점수 막대그래프') + '<div class="insight" id="in51" aria-live="polite"></div>', real=True)
    s += explain(['영화 좌표는 "그 영화를 좋아한 사람들이 무엇을 말했나"의 평균입니다. 같은 장르가 아니어도 좋아한 이유가 닮으면 가깝게 나옵니다.',
                  '취향 문장("무섭고 반전 있는 영화")을 좌표로 바꾸면 그 자리에서 맞춤 추천이 됩니다. 이 데이터에서는 %s.' % ', '.join('「%s」 %s' % (t, num(v, 2)) for t, v in PR),
                  '실제 음악·영상 서비스도 사용자와 작품을 좌표로 바꿔 가까운 것을 찾는 방식을 씁니다. 예를 들어 Spotify가 공개한 근사 이웃 검색 라이브러리 Annoy는 음악 추천에서 비슷한 사용자·곡 좌표를 찾는 데 쓰였다고 소개되어 있습니다.'],
                 '리뷰가 적은 새 영화는 좌표가 불안정합니다(콜드 스타트). 줄거리·장르 같은 다른 정보로 첫 좌표를 만들어 보완합니다.')
    s += codefold([("SELECT title FROM movie WHERE avg_stars >= 3 AND runtime <= 120 ORDER BY profile_vec <=> (SELECT profile_vec FROM movie WHERE title = '검은 서버실') LIMIT 3;", '표 조건 + 좌표 거리 정렬 (pgvector)')])
    s += wrapup('추천은 "좌표로 닮은 것 찾기 + 표 조건으로 거르기"입니다. 별점(표)은 거르는 데, 리뷰 좌표(벡터)는 닮음을 재는 데 씁니다.')
    s += quiz('q51')
    b += step('s1', '5-1', '영화 추천 — 별점은 표에서, 분위기는 좌표에서', ['사례: 추천 · 콘텐츠 좌표', '일상: "이 책 좋아했으면"'], s)

    # ── 5-2 SNS
    s = say('doc', 'think', '랩플릭스 SNS 담당자의 고민 두 가지. "광고 글이 말만 바꿔 계속 올라와요. 그리고 무슨 일이 터지면 늘 늦게 알아요." 1장의 태그 규칙으로는 둘 다 버거웠죠.')
    s += duo(why([('문제 상황', '① 말만 바꾼 광고를 걸러내야 하고 ② 아직 이름이 없는 새 이야기가 늘어나는 것을 빨리 알아야 합니다.'),
                  ('앞 방법의 한계', '1장의 낱말 규칙은 새 말투(DM 광고)와 처음 보는 주제(결제 오류)를 놓쳤습니다.'),
                  ('해법', '① 신고된 광고 예시 3개와 좌표가 가까운 글을 걸러냅니다. ② 새 글을 기존 "이야기 묶음" 중 가장 가까운 곳에 넣고, 어디와도 멀면 새 묶음을 만듭니다. 새 묶음이 빠르게 커지면 알립니다.')],
                 '경비원이 수배 사진(신고된 광고)과 닮은 얼굴을 찾고, 처음 보는 무리가 갑자기 늘면 무전을 치는 것과 같습니다.'),
             pair('1장 규칙으로는', '첫 주 글로 만든 태그 규칙이 둘째 주에 흔들렸습니다. 결제 오류 글은 미분류, DM 광고는 다른 태그로 들어갔습니다.',
                  '좌표로는', '첫 주 글로 문턱만 정해 두고, 둘째 주에 그대로 썼습니다. 광고 걸러내기 F1: 글자 겹침 %s, 좌표 %s.' % (num(SP['jac']['f1'], 3), num(SP['cos']['f1'], 3))))
    s += talk([('asst', 'e13', '모아, "DM 주시면 영화 공짜로 보는 방법 알려드림"은 신고된 광고랑 글자가 많이 겹칠까?'),
               ('moa', 'think', '"공짜", "영화" 정도만 겹치고… 나머지는 처음 보는 말투예요.'),
               ('robo', 'happy', '그러니까 좌표지! 뜻이 광고면 광고야.'),
               ('fly', 'point', '좌표도 문턱을 잘못 잡으면 평범한 글을 잡아. 아래에서 문턱을 움직이며 둘째 주 결과를 봐. 그리고 "새 이야기" 쪽에서 9일째를 지켜봐.'),
               ('asst', 'report', '9일째 결제 오류 묶음이 새로 생기고, 하루하루 커져요. 규칙 없이도 알아챘어요.')])
    s += crowd('"하루, 이제 인턴한테 질문하는 게 자연스럽다." "처음엔 목소리 떨렸는데."', moods=('e16', 'e01', 'e13'))
    s += panel('p52', '실험 · SNS 상황실 — 광고 걸러내기와 새 이야기 알림', '가상 SNS 글 %d개 · 페이지가 직접 계산' % R['n']['sns'],
               '<div class="tabs" role="tablist"><button class="bt" data-tab="spam" aria-pressed="true">① 광고 걸러내기</button><button class="bt" data-tab="novel" aria-pressed="false">② 새 이야기 알림</button></div>'
               '<div id="spam52"><div class="ctrl"><div class="group"><span class="glabel">닮음 재는 법</span><button class="bt" data-me="cos" aria-pressed="true">좌표 (코사인)</button><button class="bt" data-me="jac" aria-pressed="false">글자 겹침</button></div>'
               '<div class="group"><span class="glabel">문턱</span><input type="range" id="th52" min="0" max="100" value="79" aria-label="문턱"><span class="val" id="thv52"></span></div>'
               '<div class="group"><button class="bt" id="tn52">첫 주로 문턱 맞추기</button></div></div>'
               '<p class="small muted">신고된 광고 예시 3개: <span id="rep52"></span></p><section class="kpis" id="k52" aria-label="둘째 주 채점"></section><ul class="res" id="rs52"></ul></div>'
               '<div id="nov52" hidden><div class="ctrl"><div class="group"><span class="glabel">같은 이야기로 볼 닮음</span><input type="range" id="nt52" min="40" max="95" value="60" aria-label="닮음 문턱"><span class="val" id="ntv52"></span></div>'
               '<div class="group"><span class="glabel">보는 날</span><input type="range" id="d52" min="1" max="14" value="14" aria-label="날짜"><span class="val" id="dv52"></span></div></div>'
               + canvas('cv52', 260, '날짜별 이야기 묶음 크기 변화 선그래프') + '<section class="kpis" id="kn52" aria-label="알림"></section><ul class="res" id="rn52"></ul></div>'
               '<div class="insight" id="in52" aria-live="polite"></div>', real=True)
    s += explain(['광고 걸러내기: 문턱은 첫 주(1~7일) 글로 정하고, 둘째 주(8~14일)에 그대로 적용해 채점했습니다. 둘째 주에는 처음 보는 말투의 광고 %d개가 섞여 있습니다.' % SP['newstyle2'],
                  '글자 겹침은 같은 낱말을 쓴 광고만 잡아 재현율이 %s, 좌표는 말투가 달라도 "홍보·이벤트" 성분이 커서 재현율 %s입니다. 대신 좌표는 평범한 글을 잘못 잡을 위험도 있습니다(정밀도 %s).' % (pct(SP['jac']['r'], 0), pct(SP['cos']['r'], 0), pct(SP['cos']['p'], 0)),
                  '새 이야기 알림: 글마다 가장 가까운 기존 묶음과의 닮음이 문턱보다 낮으면 새 묶음을 만듭니다. 9일째 생긴 결제 오류 묶음이 매일 커지는 것이 보입니다.'],
                 '문턱 하나로 모든 것을 정할 수는 없습니다. 실제 상황실은 사람의 확인, 신고 기록, 계정 정보(표)를 함께 씁니다. 그리고 비꼬는 글, 새로 생긴 은어는 좌표도 자주 놓칩니다.')
    s += aicheck('"결제 오류 급증! 서비스 장애 확정"',
                 '<p>주판봇이 새 이야기 알림을 보고 사내 메신저에 올렸습니다. "결제 오류 묶음이 6개 → 21개. 서비스 장애 확정!"</p>'
                 '<p><b>확인 질문</b> ① 글 수가 늘었다는 것만으로 "장애 확정"이라고 할 수 있을까요? ② 무엇을 함께 봐야 할까요?</p>'
                 '<details><summary>생각해 본 뒤 열어 보기</summary><p>① 아닙니다. 묶음이 커졌다는 것은 "같은 이야기를 하는 글이 늘었다"는 뜻입니다. 같은 사람이 여러 번 썼을 수도, 다른 회사 이야기일 수도 있습니다. '
                 '② 묶음 안의 글 몇 개를 직접 읽고, 결제 시스템의 실제 오류 기록(표)과 맞춰 봅니다. SNS 신호는 "확인할 곳"을 알려 주는 것이지 "확정"이 아닙니다. 4장 안내 문서의 LP-204(결제 수단 만료)일 수도 있습니다.</p></details>')
    s += wrapup('좌표는 "닮음"과 "다름"을 재는 자입니다. 닮음으로 광고를 걸러내고, 다름으로 새 이야기를 알아챕니다. 문턱은 지난 데이터로 정하고, 새 데이터로 채점합니다.')
    s += quiz('q52')
    b += step('s2', '5-2', 'SNS 모니터링 — 광고 걸러내기와 새 이야기 알림', ['사례: 중복·스팸 탐지 · 이상 징후', '일상: 수배 사진과 무전'], s)

    # ── 5-3 기억
    s = say('doc', 'think', '랩플릭스 챗봇 이용자가 말했습니다. "지난주에 공포 영화 못 본다고 했는데, 오늘 또 공포 영화를 추천하네요." 챗봇은 왜 잊었을까요?')
    s += duo(why([('문제 상황', '대화가 몇 주에 걸쳐 쌓이면, 챗봇이 이용자의 취향·사정을 기억해야 합니다.'),
                  ('앞 방법의 한계', 'LLM은 한 번에 읽을 수 있는 글의 길이(컨텍스트 창)에 한계가 있고, 대화가 끝나면 기본적으로 잊습니다. 지난 대화를 전부 붙이면 길고 비쌉니다.'),
                  ('해법', '지난 대화를 조각으로 벡터 DB에 저장해 두고(기억 창고), 새 질문이 오면 가까운 기억 몇 개만 꺼내 붙입니다. 4장 RAG를 "문서" 대신 "대화"에 쓰는 것입니다.')],
                 '단골 가게 사장님이 손님 수첩을 넘겨 "이 분은 매운 걸 못 드시지"를 찾아보는 것과 같습니다.'),
             pair('4장 RAG에서는', '창고에 회사 안내 문서를 넣고, 질문과 가까운 문서 조각을 찾았습니다.',
                  '기억 창고에서는', '창고에 이용자의 지난 말을 날짜와 함께 넣고, 지금 질문과 가까운 기억을 찾습니다. 오래된 기억, 지워 달라고 한 기억은 메타데이터로 거릅니다.'))
    s += talk([('asst', 'e13', '시아, 챗봇에게 지난 대화를 전부 붙여 주면 안 될까?'),
               ('sia', 'explain', '대화가 몇 달 쌓이면 너무 길어요. 비용도 들고요. 필요한 것만 꺼내야 해요.'),
               ('robo', 'coin', '그냥 전부 기억시키면 되지. 많이 기억할수록 똑똑해!'),
               ('fly', 'point', '많이 기억할수록 엉뚱한 기억도 끼어들어. 아래에서 질문을 바꿔 가며 어떤 기억이 꺼내지는지 봐. "기억 지우기"도 눌러 보고.'),
               ('asst', 'report', '"무서운 영화 추천해 줘"에는 "공포 영화 못 봐" 기억이 1위로 나와요. 그 기억을 지우면 다시 공포 영화를 추천하고요.')])
    s += panel('p53', '실험 · 챗봇의 기억 창고 — 지금 질문과 가까운 기억 꺼내기', '가상 대화 · 찾기는 실제 계산, 답은 흉내',
               '<div class="chips" id="q53"></div><div class="grid2"><div><h4>기억 창고 (이용자의 지난 말)</h4><ul class="res" id="mem53"></ul></div>'
               '<div><h4>꺼낸 기억 3개 (점수 = 뜻 점수)</h4><ul class="res" id="hit53"></ul><h4>챗봇 답 (흉내)</h4><div class="ansbox" id="ans53"></div></div></div>'
               '<div class="insight" id="in53" aria-live="polite"></div>', real=True)
    s += explain(['기억도 좌표로 저장해 두면, 오래전 대화라도 지금 질문과 뜻이 가까우면 꺼낼 수 있습니다. 날짜 순서가 아니라 뜻 순서입니다.',
                  '"기억 지우기"는 창고에서 그 레코드(좌표 포함)를 지우는 일입니다. 이용자가 잊어 달라고 하면 원문뿐 아니라 좌표도 지워야 합니다.',
                  '이 연구실의 「LLM은 어디까지 기억할 수 있을까」처럼, 대화 기억은 요약·압축·벡터 검색을 섞어 설계하는 주제입니다.'],
                 '꺼낸 기억이 지금 상황과 맞지 않을 수 있습니다(지난달엔 바빴지만 이번 주는 한가함). 기억에는 날짜를 붙이고, 오래된 기억의 무게를 낮추는 장치가 필요합니다.')
    s += wrapup('챗봇의 기억은 "대화를 넣어 둔 벡터 창고 + 가까운 기억만 꺼내 붙이기"입니다. 무엇을 기억하고 무엇을 지울지는 이용자의 권리와 함께 설계합니다.')
    s += quiz('q53')
    b += step('s3', '5-3', 'LLM의 기억 — 대화를 넣어 둔 벡터 창고', ['사례: 장기 기억 · 개인화', '일상: 단골 가게 수첩'], s)

    # ── 5-4 도입 판단
    s = say('doc', 'think', '마지막 사례는 여러분 회사입니다. 팀장이 "우리도 벡터 DB 도입하죠"라고 합니다. 무엇부터 물어야 할까요?')
    s += duo(why([('문제 상황', '벡터 DB는 유행어가 되었지만, 모든 문제에 필요한 것은 아닙니다.'),
                  ('앞 방법의 한계', '"남들이 쓰니까"는 판단 근거가 아닙니다. 질문의 종류와 데이터의 모양을 먼저 봐야 합니다.'),
                  ('해법', '다섯 가지를 묻습니다. ① 질문이 "정확히 이것"인가 "이것과 비슷한 것"인가 ② 데이터가 문장·사진처럼 비정형인가 ③ 얼마나 많은가 ④ 얼마나 자주 바뀌는가 ⑤ 개인정보·기밀이 있는가.')],
                 '망치를 샀다고 모든 것이 못으로 보이면 곤란합니다. 먼저 못인지 나사인지 봅니다.'),
             pair('표만으로 충분할 때', '질문이 대부분 정확한 값·범위·집계이고(주문 조회, 재고, 정산), 문장 검색은 가끔 LIKE·전문 검색으로 충분할 때.',
                  '벡터가 필요할 때', '"비슷한 것", "이런 뜻의 것"을 묻는 질문이 많고(고객 문의, 리뷰, 사내 문서, 상품 사진), LLM에게 근거를 붙여 줘야 할 때.'))
    s += talk([('asst', 'e16', '모아, 마지막 질문! 우리 회사에 벡터 DB가 필요한지 어떻게 판단할까?'),
               ('moa', 'report', '질문이 "정확히"인지 "비슷한"인지, 데이터가 표인지 문장인지부터 볼래요!'),
               ('robo', 'wow', '요즘 대세니까 무조건 전용 벡터 DB부터 사자!'),
               ('fly', 'point', '아래 다섯 개를 회사 상황대로 골라 봐. 결론이 "표만으로 충분"일 수도 있어.'),
               ('asst', 'report', '고객 문의 위주·문장 많음·10만 건이면 "PostgreSQL + pgvector로 작게 시작"이 나와요.')])
    s += panel('p54', '실험 · 우리 회사에 벡터 DB가 필요할까 — 도입 판단 도우미', '설명용 판단 규칙',
               '<div id="f54"></div><div class="ansbox" id="ans54" aria-live="polite"></div><ul class="res" id="why54"></ul>', real=True)
    s += explain(['처음에는 이미 쓰는 관계형 DB에 벡터 확장(pgvector 등)을 붙여 작게 시작하고, 질문 수·데이터 양이 커지면 전용 벡터 DB를 검토하는 순서가 무난합니다.',
                  '임베딩을 외부 API로 만들면 문장이 회사 밖으로 나갑니다. 개인정보·기밀은 내부에서 돌리는 임베딩 모델을 검토합니다. 좌표만으로도 원문 내용이 상당 부분 되살아날 수 있다는 연구가 있어, 좌표도 원문처럼 보호합니다.',
                  '어떤 구조든 "우리 질문 묶음"으로 정답률·재현율·응답 시간을 재는 평가부터 만듭니다. 이 시리즈에서 대결마다 숫자를 잰 것처럼요.'],
                 '이 도우미는 설명용 규칙입니다. 실제 도입은 비용, 운영 인력, 기존 시스템, 법·규정을 함께 따져야 합니다.')
    s += wrapup('벡터 DB 도입의 첫 질문은 "무엇을 묻는가"입니다. 비슷한 것을 묻는다면 벡터, 정확한 것을 묻는다면 표, 대부분은 둘 다입니다.')
    s += quiz('q54')
    b += step('s4', '5-4', '도입 판단 — 우리 회사에 벡터 DB가 필요할까', ['판단: 질문 종류 · 데이터 · 보안', '일상: 못인가 나사인가'], s)

    b += duel('d5', '둘째 주 SNS 광고 걸러내기 — 글자 겹침 vs 좌표 닮음', '글자 겹침 (글자 두 개씩 끊은 조각이 얼마나 겹치나)', '좌표 닮음 (교육용 임베딩 코사인)',
              '"단순한 게 오래 가. 같은 글자를 쓰면 같은 광고야."', '"말투는 바꿔도 뜻은 못 바꾸지! 좌표로 잡아."',
              '둘째 주 F1 (문턱은 첫 주 글로 각자 가장 좋게 맞춤)')

    b += section('sum', '정리 — 현장 사례 네 가지에서 본 것',
                 '<div class="tw"><table class="tb"><tr><th>사례</th><th>벡터가 한 일</th><th>표가 한 일</th><th>조심할 점</th></tr>'
                 '<tr><td>영화 추천</td><td>좋아한 이유가 닮은 영화 찾기</td><td>별점·상영 시간 조건</td><td>리뷰 적은 새 영화(콜드 스타트)</td></tr>'
                 '<tr><td>SNS 모니터링</td><td>광고와 닮은 글, 처음 보는 이야기</td><td>날짜·신고 기록</td><td>문턱, 알림 ≠ 확정</td></tr>'
                 '<tr><td>챗봇의 기억</td><td>지금 질문과 가까운 지난 말</td><td>날짜·사용자·지우기 요청</td><td>오래된 기억, 잊힐 권리</td></tr>'
                 '<tr><td>도입 판단</td><td colspan="2">질문 종류로 역할 나누기</td><td>보안, 평가 묶음 먼저</td></tr></table></div>'
                 + bridge('field', '더 넓은 현장', '사진·소리도 임베딩으로 좌표가 됩니다. 글과 그림을 같은 좌표 공간에 놓는 모델(예: CLIP)을 쓰면 "빨간 운동화" 글로 사진을 찾는 쇼핑 검색이 됩니다. 이상 거래 탐지, 비슷한 특허·논문 찾기, 코드 검색도 같은 원리입니다.',
                          '이 연구실은 글만 다뤘습니다. 사진·소리는 임베딩 모델이 달라질 뿐, 창고와 색인·필터의 원리는 같습니다.'))

    b += outro([('doc', 'front', '오늘 세 줄 정리. ① 벡터 DB는 추천·감시·기억·검색의 부품이다. ② 표는 사실과 조건을, 벡터는 닮음과 다름을 맡는다. ③ 도입은 "무엇을 묻는가"와 "무엇으로 채점하나"부터.'),
                ('robo', 'happy', '마지막 대결은 내 승리! 전적은 2승 3패. 실전 연습장에서 역전이다.'),
                ('fly', 'arms', '그래, 이번엔 좌표가 잘 잡았어. 문턱을 첫 주로 맞춘 게 공정했지.'),
                ('sia', 'proud', '다섯 가지 도입 질문, 회사 가서 바로 써먹을래요.'),
                ('moa', 'cheer', 'DB 설계 노트 마지막 장에 "둘 다"라고 크게 썼어요!'),
                ('asst', 'e01', '인턴 교육 정규 과정 끝! 다음은 특강 두 개예요. LLM이 찾은 자료를 어떻게 읽는지 3D로 보고, 지식 그래프와 온톨로지까지 가요.')],
               '연구실 식구 모두와 방청석의 X1~X3가 함께 박수 치며 수료를 축하하는 장면',
               crowd('"하루 첫 인턴 교육, 대성공!" "처음 떨던 거 생각하면 감동이다…" "박수!"', moods=('e01', 'e16', 'e01')))
    return b


GLOSS = {
    '추천': ['추천 시스템', '이용자가 좋아할 만한 것을 골라 보여 주는 시스템. 좌표로 닮은 것을 찾는 방식이 널리 쓰입니다.'],
    '콜드 스타트': ['콜드 스타트 (cold start)', '기록이 거의 없는 새 이용자·새 작품이라 추천이 어려운 문제.'],
    '문턱': ['문턱 (threshold)', '이 값보다 크면(작으면) 걸러내거나 알리는 기준값.'],
    '컨텍스트 창': ['컨텍스트 창 (context window)', 'LLM이 한 번에 읽을 수 있는 글의 최대 길이(토큰 수).'],
    '기억 창고': ['기억 창고', '지난 대화를 좌표로 저장해 두고, 지금 질문과 가까운 기억만 꺼내 쓰는 벡터 DB 쓰임새.'],
    'pgvector': ['pgvector', 'PostgreSQL에 벡터 열과 색인을 더하는 확장. 작게 시작하기 좋습니다.'],
    'CLIP': ['CLIP', '그림과 글을 같은 좌표 공간에 놓도록 학습한 임베딩 모델(OpenAI, 2021).'],
    'Annoy': ['Annoy', 'Spotify가 공개한 근사 이웃 검색 라이브러리. 음악 추천에서 비슷한 좌표를 찾는 데 쓰였습니다.'],
}

QUIZ = {
    'q51': [{'q': '영화 좌표를 "별점 4점 이상 리뷰"의 평균으로 만든 이유는?', 'o': ['계산이 빨라서', '그 영화를 "좋아한 이유"만 모으려고', '리뷰 수를 줄이려고'], 'a': 1,
             'why': '좋아한 사람들의 말만 모아야 "이 영화를 좋아했다면 이것도"에 맞는 좌표가 됩니다.', 'hint': '추천의 목적을 떠올려 보세요.'},
            {'q': '별점 평균순 추천의 약점은?', 'o': ['모두에게 같은 영화를 추천한다', '계산이 불가능하다', '좌표가 필요하다'], 'a': 0,
             'why': '평균은 사람마다 같습니다. 취향(좋아한 이유)을 반영하지 못합니다.', 'hint': '공포를 좋아한 사람에게도 같은 1위를 줍니다.'}],
    'q52': [{'q': '광고 걸러내기 문턱을 첫 주 글로 정하고 둘째 주로 채점한 이유는?', 'o': ['둘째 주가 더 쉬워서', '채점할 데이터로 문턱을 맞추면 점수가 부풀려지기 때문', '첫 주에 광고가 없어서'], 'a': 1,
             'why': '같은 데이터로 맞추고 채점하면 실제보다 좋아 보입니다. 지난 데이터로 정하고 새 데이터로 재야 공정합니다.', 'hint': '시험 문제를 미리 보고 공부한 셈이 됩니다.'},
            {'q': '새 이야기 묶음이 빠르게 커질 때 맞는 대응은?', 'o': ['바로 장애라고 발표한다', '묶음 안 글을 읽고 실제 시스템 기록과 맞춰 본다', '무시한다'], 'a': 1,
             'why': 'SNS 신호는 확인할 곳을 알려 줄 뿐, 확정이 아닙니다.', 'hint': 'AI 판단 코너를 떠올려 보세요.'}],
    'q53': [{'q': '챗봇에게 지난 대화를 전부 붙이지 않고 기억 창고를 쓰는 이유는?', 'o': ['LLM이 한 번에 읽을 수 있는 길이와 비용에 한계가 있어서', '대화가 틀려서', '좌표가 더 정확해서'], 'a': 0,
             'why': '컨텍스트 창과 비용 때문에, 지금 질문과 가까운 기억만 꺼내 붙입니다.', 'hint': '대화가 몇 달 쌓이면?'},
            {'q': '이용자가 "그 기억 지워 줘"라고 하면?', 'o': ['원문만 지운다', '원문과 좌표를 모두 지운다', '좌표만 지운다'], 'a': 1,
             'why': '좌표만으로도 내용이 상당 부분 되살아날 수 있어, 원문과 좌표를 함께 지워야 합니다.', 'hint': '좌표도 원문처럼 보호합니다.'}],
    'q54': [{'q': '질문 대부분이 주문 조회·재고·정산이라면?', 'o': ['전용 벡터 DB가 꼭 필요하다', '관계형 DB(표)만으로 충분할 가능성이 크다', 'LLM만 있으면 된다'], 'a': 1,
             'why': '정확한 값·범위·집계 질문은 표가 가장 잘합니다.', 'hint': '"정확히 이것" 질문인가요?'},
            {'q': '개인정보가 든 문장을 외부 임베딩 API로 보낼 때의 위험은?', 'o': ['없다', '문장이 회사 밖으로 나간다', '좌표가 너무 작다'], 'a': 1,
             'why': '임베딩을 만들려면 원문을 보내야 합니다. 내부 모델이나 비식별 처리를 검토합니다.', 'hint': '좌표를 누가 만드나요?'}],
}

JS = r'''
var D=VL.load(),RV=D.reviews,MV=D.movies,S=D.sns;
/* 5-1 */
(function(){var cv=$('#cv51'),sh=false;var prof=MV.map(function(m){var rs=RV.filter(function(r){return r.movie===m.id&&r.stars>=4}),v=new Array(24).fill(0);rs.forEach(function(r){r.vec.forEach(function(x,i){v[i]+=x/rs.length})});
    var all=RV.filter(function(r){return r.movie===m.id});return {m:m,v:v,avg:all.reduce(function(s,r){return s+r.stars},0)/all.length}});
  $('#m51').innerHTML=MV.map(function(m){return '<option value="'+m.id+'"'+(m.id===8?' selected':'')+'>'+m.title+' ('+m.genre+')</option>'}).join('');
  function draw(){var t=$('#t51').value.trim(),mid=+$('#m51').value,mn=+$('#s51').value;$('#sv51').textContent=mn.toFixed(1)+'점 이상';var q=t?VL.embed(t).v:prof.filter(function(p){return p.m.id===mid})[0].v;
    var rows=prof.filter(function(p){return t||p.m.id!==mid}).map(function(p){return {p:p,s:VL.cos(q,p.v),ok:p.avg>=mn&&(!sh||p.m.runtime<=120)}}).sort(function(a,b){return b.s-a.s});
    $('#sql51').innerHTML='<span class="k">SELECT</span> title <span class="k">FROM</span> movie <span class="k">WHERE</span> avg_stars &gt;= '+mn.toFixed(1)+(sh?' <span class="k">AND</span> runtime &lt;= 120':'')+'\n<span class="k">ORDER BY</span> profile_vec &lt;=&gt; '+(t?'<span class="s">embed(\''+VL.esc(t)+'\')</span>':'(<span class="k">SELECT</span> profile_vec <span class="k">FROM</span> movie <span class="k">WHERE</span> id = '+mid+')')+' <span class="k">LIMIT</span> 3;';
    var f=fit(cv),g=f.c;g.fillStyle='#fff';g.fillRect(0,0,f.W,f.H);var L=130,bh=(f.H-16)/rows.length;g.font='12px "IBM Plex Sans KR",sans-serif';
    rows.forEach(function(r,i){var y=8+i*bh,w=Math.max(0,r.s)*(f.W-L-70);g.fillStyle=r.ok?'#16212b':'#9aa6b2';g.fillText(r.p.m.title,6,y+bh*.65);g.fillStyle=r.ok?(i<3?'#1e55c8':'#8fb0e8'):'#e2e6ea';g.fillRect(L,y+3,w,bh-6);g.fillStyle=r.ok?'#16212b':'#9aa6b2';g.fillText(r.s.toFixed(2)+'  ★'+r.p.avg.toFixed(1)+(r.ok?'':' (조건 밖)'),L+w+6,y+bh*.65);});stamp(g,f.W,'가상 데이터 · 리뷰 좌표 평균');
    var top=rows.filter(function(r){return r.ok}).slice(0,3);$('#in51').innerHTML='<p class="g">추천 3편: '+top.map(function(r){return '「'+r.p.m.title+'」('+r.p.m.genre+', 닮음 '+r.s.toFixed(2)+')'}).join(', ')+'</p><p class="m">회색 막대는 별점·상영 시간 조건(표)에서 걸러진 영화입니다. 닮음(벡터)과 조건(표)이 함께 일합니다.</p>';}
  ['#m51','#s51','#t51'].forEach(function(s){$(s).addEventListener('input',draw);$(s).addEventListener('change',draw)});$('#r51').addEventListener('click',function(){sh=!sh;this.setAttribute('aria-pressed',sh?'true':'false');draw();});
  Loop.add(cv,function(dt){if(dt===0)draw();});
})();
/* 5-2 */
(function(){var me='cos',REP=[1,2,3].map(function(g){return S.filter(function(s){return s.dup===g})[0]});$('#rep52').textContent=REP.map(function(r){return '"'+r.text+'"'}).join(' · ');
  function jac(a,b){var A={},B={},i=0,u=0;VL.grams(a).forEach(function(x){A[x]=1});VL.grams(b).forEach(function(x){B[x]=1});for(var k in A){u++;if(B[k])i++;}for(k in B)if(!A[k])u++;return u?i/u:0;}
  var pool=S.filter(function(s){return REP.indexOf(s)<0}).map(function(s){return {s:s,y:s.topic==='promo',cos:Math.max.apply(null,REP.map(function(r){return VL.cos(s.vec,r.vec)})),jac:Math.max.apply(null,REP.map(function(r){return jac(s.text,r.text)}))}});
  function score(arr,t){var tp=0,fp=0,fn=0;arr.forEach(function(p){var h=p[me]>=t;if(h&&p.y)tp++;else if(h)fp++;else if(p.y)fn++;});var pr=tp/(tp+fp||1),rc=tp/(tp+fn||1);return {tp:tp,fp:fp,fn:fn,p:pr,r:rc,f1:pr+rc?2*pr*rc/(pr+rc):0};}
  function tune(){var b={f1:-1,t:0};for(var t=5;t<=100;t++){var x=score(pool.filter(function(p){return p.s.day<=7}),t/100);if(x.f1>b.f1){b=x;b.t=t;}}return b.t;}
  function spam(){var t=+$('#th52').value/100;$('#thv52').textContent=t.toFixed(2);var w2=pool.filter(function(p){return p.s.day>=8}),sc=score(w2,t);
    VL.kpis($('#k52'),[[sc.f1.toFixed(3),'둘째 주 F1','g'],[sc.tp+' / '+(sc.tp+sc.fn),'잡은 광고 / 전체 광고','i'],[sc.fp+'개','광고 아닌데 잡은 글','r'],[w2.filter(function(p){return p.s.dup===4}).filter(function(p){return p[me]>=t}).length+' / '+w2.filter(function(p){return p.s.dup===4}).length,'처음 보는 말투(DM) 광고 잡은 수','a']]);
    var show=w2.filter(function(p){return p.y||p[me]>=t}).sort(function(a,b){return b[me]-a[me]}).slice(0,10);
    $('#rs52').innerHTML=show.map(function(p){var h=p[me]>=t;return '<li class="'+(h===p.y?'ok':'no')+'"><span class="sc">'+p[me].toFixed(2)+'</span><small>'+p.s.day+'일째 · '+(p.y?'광고':'광고 아님')+' · '+(h?'걸러냄':'통과시킴')+'</small>'+VL.esc(p.s.text)+'</li>'}).join('');
    $('#in52').innerHTML='<p class="'+(sc.f1>.9?'g':'a')+'">'+(me==='cos'?'좌표는 말투가 달라도 "홍보·이벤트" 성분으로 광고를 알아봅니다.':'글자 겹침은 같은 낱말을 쓴 광고만 잡습니다. 처음 보는 말투(DM 광고)를 보세요.')+' "첫 주로 문턱 맞추기"를 누르면 공정한 문턱으로 돌아갑니다.</p>';}
  $$('#spam52 [data-me]').forEach(function(b){b.addEventListener('click',function(){me=b.dataset.me;$$('#spam52 [data-me]').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});$('#th52').value=tune();spam();})});
  $('#th52').addEventListener('input',spam);$('#tn52').addEventListener('click',function(){$('#th52').value=tune();spam();});
  /* 새 이야기 알림: 가장 가까운 묶음에 넣거나 새 묶음을 만든다 */
  var cv=$('#cv52');
  function groups(th){var G=[];S.filter(function(s){return s.topic!=='promo'}).forEach(function(s){var b=-1,bs=-2;G.forEach(function(g,i){var c=VL.cos(s.vec,g.c);if(c>bs){bs=c;b=i}});
      if(b<0||bs<th){G.push({c:s.vec.slice(),n:1,born:s.day,items:[s],days:{}});G[G.length-1].days[s.day]=1;}else{var g=G[b];g.items.push(s);g.n++;g.days[s.day]=(g.days[s.day]||0)+1;g.c=g.c.map(function(x,i){return x+(s.vec[i]-x)/g.n});}});return G;}
  function novel(){var th=+$('#nt52').value/100,day=+$('#d52').value;$('#ntv52').textContent=th.toFixed(2);$('#dv52').textContent=day+'일째까지';var G=groups(th);
    var f=fit(cv),g=f.c,A=VL.axes(g,f.W,f.H,{xmin:1,xmax:14,ymin:0,ymax:Math.max(6,Math.max.apply(null,G.map(function(x){return x.n}))),xlab:'날짜 (일째)',ylab:'묶음의 누적 글 수',xt:14});
    var cols=['#1e55c8','#13733a','#a35c00','#9b3fb5','#0b7a86','#5b6874'];var alerts=[];
    G.forEach(function(gr,gi){var acc=0,pts=[];for(var d=1;d<=day;d++){acc+=gr.days[d]||0;if(d>=gr.born)pts.push([d,acc]);}var young=gr.born>=3,fast=young&&pts.length&&pts[pts.length-1][1]>=3&&(day-gr.born)<=3;
      var hot=young&&pts.length&&(pts[pts.length-1][1]>=4);if(hot)alerts.push(gr);g.strokeStyle=hot?'#c9302c':cols[gi%cols.length];g.globalAlpha=hot?1:.45;g.lineWidth=hot?3:1.5;g.beginPath();pts.forEach(function(p,i){var x=A.sx(p[0]),y=A.sy(p[1]);i?g.lineTo(x,y):g.moveTo(x,y)});g.stroke();g.globalAlpha=1;g.lineWidth=1;});
    stamp(g,f.W,'이야기 묶음 '+G.length+'개');
    var iss=G.filter(function(gr){return gr.items.some(function(s){return s.issue})}).sort(function(a,b){return b.n-a.n})[0];
    VL.kpis($('#kn52'),[[G.length+'개','이야기 묶음 수','i'],[alerts.length+'개','알림 (3일째 이후 생겨 4개 이상으로 큰 묶음)','r'],[iss?iss.born+'일째':'—','결제 오류 묶음이 생긴 날','a']]);
    $('#rn52').innerHTML=alerts.slice(0,3).map(function(gr){return '<li class="no"><small>'+gr.born+'일째 생김 · 글 '+gr.items.filter(function(s){return s.day<=day}).length+'개</small>'+gr.items.slice(0,3).map(function(s){return VL.esc(s.text)}).join(' / ')+'</li>'}).join('')||'<li class="nt">알림이 없습니다. 날짜를 9일 이후로 넘겨 보세요.</li>';
    $('#in52').innerHTML='<p class="'+(alerts.length?'r':'g')+'">'+(alerts.length?'빨간 선이 새로 생겨 빠르게 큰 이야기 묶음입니다. 사람이 읽고 확인할 차례입니다.':'아직 새로 생겨 빠르게 큰 묶음이 없습니다.')+' 닮음 문턱을 너무 높이면 같은 이야기가 여러 묶음으로 쪼개지고, 너무 낮추면 다른 이야기가 한 묶음에 섞입니다.</p>';}
  $('#nt52').addEventListener('input',novel);$('#d52').addEventListener('input',novel);
  $$('#p52 [data-tab]').forEach(function(b){b.addEventListener('click',function(){$$('#p52 [data-tab]').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});var sp=b.dataset.tab==='spam';$('#spam52').hidden=!sp;$('#nov52').hidden=sp;sp?spam():novel();})});
  $('#th52').value=tune();spam();Loop.add(cv,function(dt){if(dt===0&&!$('#nov52').hidden)novel();});
})();
/* 5-3 */
(function(){var M=[['3주 전','나 공포 영화는 진짜 못 봐. 밤에 잠을 못 자.'],['3주 전','OST 좋은 영화 좋아해.'],['2주 전','주말엔 보통 가족이랑 같이 봐.'],['2주 전','프리미엄 요금제 쓰고 있어.'],
    ['지난주','베트남어 자막으로 보는 친구가 놀러 와.'],['지난주','회사 일이 바빠서 러닝타임 긴 영화는 부담돼.'],['지난주','점심은 보통 회사 앞 김치찌개.'],['3일 전','LP-204 결제 오류 떴었는데 카드 다시 등록해서 해결했어.'],
    ['어제','「주판왕의 비밀」 반전 미쳤더라.'],['어제','눈물 나는 영화도 가끔 좋아.']].map(function(m,i){return {i:i,when:m[0],text:m[1],vec:VL.embed(m[1]).v,on:true}});
  var Q=[['무서운 영화 추천해 줘','(기억 없이) 「붉은 계단」, 「검은 서버실」 어떠세요? 소름 돋는 공포 영화예요.','지난번에 공포 영화는 잠을 못 잔다고 하셨죠. 대신 반전이 있는 「주판왕의 비밀」이나 OST가 좋은 「별빛 정거장」은 어떠세요?',0],
    ['음악 좋은 영화 뭐 있어?','(기억 없이) 「별빛 정거장」을 추천해요.','OST 좋은 영화를 좋아하신다고 했죠. 「별빛 정거장」이요. 다만 러닝타임이 168분이라, 바쁘시면 주말에 보세요.',1],
    ['자막 설정 어떻게 바꿔?','(기억 없이) 재생 화면의 설정 버튼에서 바꿀 수 있어요.','재생 화면의 설정 버튼에서 바꿀 수 있어요. 친구분이 오시면 베트남어 자막도 지원해요.',4],
    ['러닝타임 긴 영화 괜찮을까?','(기억 없이) 「별빛 정거장」(168분)도 볼 만해요!','요즘 회사 일이 바쁘다고 하셨죠. 100분 안팎인 「바다로 간 초파리」(96분)나 「붉은 계단」(97분)… 아, 공포는 빼고 「바다로 간 초파리」를 권해요.',5],
    ['결제 오류 또 나면 어떡해?','(기억 없이) 앱을 다시 설치해 보세요.','지난번 LP-204 때처럼 결제 수단 메뉴에서 카드를 다시 등록하면 돼요. 안 되면 채팅 상담이 가장 빨라요.',7],
    ['반전 있는 영화 또 없어?','(기억 없이) 「주판왕의 비밀」을 추천해요!','「주판왕의 비밀」은 이미 보셨죠. 긴장감 있는 「검은 서버실」도 스토리가 탄탄하다는 평이 있어요. 다만 공포 분위기가 조금 있어요.',8]],cur=0;
  $('#q53').innerHTML=Q.map(function(q,i){return '<button class="bt" data-i="'+i+'" aria-pressed="'+(i===0)+'">'+q[0]+'</button>'}).join('');
  function run(){var q=Q[cur],qv=VL.embed(q[0]).v,live=M.filter(function(m){return m.on}),hits=VL.topk(live,function(m){return VL.cos(qv,m.vec)},3);
    $('#mem53').innerHTML=M.map(function(m){return '<li class="'+(m.on?'nt':'no')+'"><small>'+m.when+(m.on?'':' · 지움')+' <button class="bt" data-m="'+m.i+'" style="float:right;padding:1px 8px;font-size:12px">'+(m.on?'기억 지우기':'되살리기')+'</button></small>'+VL.esc(m.text)+'</li>'}).join('');
    $$('#mem53 [data-m]').forEach(function(b){b.addEventListener('click',function(){var m=M[+b.dataset.m];m.on=!m.on;run();})});
    $('#hit53').innerHTML=hits.map(function(h){return '<li class="'+(h.it.i===q[3]?'ok':'nt')+'"><span class="sc">'+h.s.toFixed(2)+'</span><small>'+h.it.when+'</small>'+VL.esc(h.it.text)+'</li>'}).join('');
    var used=hits.length&&hits[0].it.i===q[3]&&hits[0].s>.3;$('#ans53').className='ansbox'+(used?'':' none');$('#ans53').innerHTML=VL.esc(used?q[2]:q[1])+'<br><small class="muted">'+(used?'꺼낸 기억을 붙여 쓴 답 (흉내)':'관련 기억을 못 꺼내 쓴 답 (흉내)')+'</small>';
    $('#in53').innerHTML='<p class="'+(used?'g':'a')+'">'+(used?'질문과 가장 가까운 기억이 1위로 꺼내졌습니다. 날짜가 오래되어도 뜻이 가까우면 꺼냅니다.':'그 기억이 꺼내지지 않았습니다. 지웠거나, 다른 기억이 더 가까웠습니다.')+'</p>';}
  $$('#q53 .bt').forEach(function(b){b.addEventListener('click',function(){cur=+b.dataset.i;$$('#q53 .bt').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});run();})});run();
})();
/* 5-4 */
(function(){var F=[['q','① 받는 질문은 주로?',[['exact','정확히 이것 (주문 번호, 재고, 금액)'],['mix','반반'],['sim','이것과 비슷한 것 (뜻·분위기)']]],
    ['d','② 데이터는 주로?',[['table','표 (숫자·코드)'],['mix','표 + 문장'],['text','문장·사진·소리']]],
    ['n','③ 찾을 대상은 몇 건?',[['s','10만 건 이하'],['m','10만~1,000만 건'],['l','1,000만 건 이상']]],
    ['u','④ 얼마나 자주 바뀌나?',[['rare','거의 안 바뀜'],['daily','매일'],['live','실시간']]],
    ['p','⑤ 개인정보·기밀이 있나?',[['no','없음'],['yes','있음']]]],A={q:'sim',d:'mix',n:'s',u:'daily',p:'yes'};
  $('#f54').innerHTML=F.map(function(f){return '<div class="ctrl"><div class="group"><span class="glabel">'+f[1]+'</span>'+f[2].map(function(o){return '<button class="bt" data-f="'+f[0]+'" data-v="'+o[0]+'" aria-pressed="'+(A[f[0]]===o[0])+'">'+o[1]+'</button>'}).join('')+'</div></div>'}).join('');
  function run(){var why=[],rec;
    if(A.q==='exact'&&A.d==='table'){rec='관계형 DB로 충분합니다. 문장 검색이 가끔 필요하면 LIKE나 전문 검색(글자 색인)으로 시작하세요.';why.push(['ok','질문이 정확한 값 중심이고 데이터가 표입니다 (1장).']);}
    else if(A.n==='l'||A.u==='live'){rec='관계형 DB(사실) + 전용 벡터 DB(검색)를 함께 검토하세요. 색인 종류와 재현율·응답 시간을 우리 질문 묶음으로 먼저 재 보세요.';why.push(['no','건수가 많거나 실시간 갱신이라 전용 색인·확장이 필요할 수 있습니다 (3장).']);}
    else{rec='이미 쓰는 PostgreSQL 같은 관계형 DB에 벡터 확장(pgvector 등)을 붙여 작게 시작하세요. 필요하면 RAG(4장)로 LLM과 잇습니다.';why.push(['ok','"비슷한 것" 질문이 있고 규모가 감당할 만합니다. 표와 벡터를 한곳에서 함께 쓰면 단순합니다 (3-5).']);}
    if(A.q!=='exact')why.push(['ok','"비슷한 것" 질문은 임베딩 + 좌표 검색이 맡습니다 (2장).']);
    if(A.d!=='table')why.push(['ok','문장·사진이 있으면 임베딩 모델을 골라야 합니다. 한국어·업무 용어를 잘 아는지 우리 데이터로 시험하세요.']);
    if(A.p==='yes')why.push(['no','개인정보·기밀: 외부 임베딩 API로 원문이 나가지 않는지, 권한 필터(메타데이터)와 지우기 요청 처리(원문 + 좌표)가 되는지 확인하세요.']);
    if(A.u!=='rare')why.push(['nt','자주 바뀌면 문서를 다시 쪼개고 좌표를 다시 만드는 흐름(갱신 파이프라인)과 날짜·버전 필터가 필요합니다 (4-5).']);
    why.push(['nt','어떤 구조든 "우리 질문 묶음 + 정답"을 먼저 만들어 정답률·재현율·응답 시간을 재세요.']);
    $('#ans54').innerHTML='<b>권하는 출발점</b><br>'+rec;$('#why54').innerHTML=why.map(function(w){return '<li class="'+w[0]+'">'+w[1]+'</li>'}).join('');}
  $$('#f54 .bt').forEach(function(b){b.addEventListener('click',function(){A[b.dataset.f]=b.dataset.v;$$('#f54 [data-f='+b.dataset.f+']').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});run();})});run();
})();
/* 대결 5 */
Duel({el:'#d5',run:function(){var REP=[1,2,3].map(function(g){return S.filter(function(s){return s.dup===g})[0]});function jac(a,b){var A={},B={},i=0,u=0;VL.grams(a).forEach(function(x){A[x]=1});VL.grams(b).forEach(function(x){B[x]=1});for(var k in A){u++;if(B[k])i++;}for(k in B)if(!A[k])u++;return u?i/u:0;}
    var pool=S.filter(function(s){return REP.indexOf(s)<0}).map(function(s){return {d:s.day,y:s.topic==='promo',cos:Math.max.apply(null,REP.map(function(r){return VL.cos(s.vec,r.vec)})),jac:Math.max.apply(null,REP.map(function(r){return jac(s.text,r.text)}))}});
    function sc(arr,k,t){var tp=0,fp=0,fn=0;arr.forEach(function(p){var h=p[k]>=t;if(h&&p.y)tp++;else if(h)fp++;else if(p.y)fn++;});var pr=tp/(tp+fp||1),rc=tp/(tp+fn||1);return pr+rc?2*pr*rc/(pr+rc):0;}
    function best(k){var b=-1,bt=0;for(var t=5;t<=100;t++){var x=sc(pool.filter(function(p){return p.d<=7}),k,t/100);if(x>b){b=x;bt=t/100;}}return sc(pool.filter(function(p){return p.d>=8}),k,bt);}
    return {fly:best('jac'),robo:best('cos')}},scale:1,fmt:function(v){return v.toFixed(3)},
  report:function(r){return '둘째 주 F1: 글자 겹침 '+r.fly.toFixed(3)+', 좌표 '+r.robo.toFixed(3)+'. 글자 겹침은 처음 보는 말투의 DM 광고를 놓쳤어요.'},
  verdict:{robo:'주판봇 승. 말투를 바꾼 광고는 글자가 아니라 뜻으로 닮았습니다. 다만 문턱을 첫 주로 맞추고 둘째 주로 채점했기에 공정한 승리입니다. 채점할 데이터로 문턱을 맞췄다면 둘 다 만점처럼 보였을 겁니다.',fly:'초파리 승.',draw:'무승부.'}});
'''


def build_page():
    nav = [('#s1', '5-1 추천'), ('#s2', '5-2 SNS'), ('#s3', '5-3 기억'), ('#s4', '5-4 도입 판단'), ('#duel', '대결'), ('#sum', '정리')]
    cov = cover('cover_05', '벡터 DB 연구실 · 5장', '현장 사례', chars=(('doc', 'front'), ('asst', 'e01'), ('fly', 'arms'), ('robo', 'happy')))
    hr = hero('벡터 DB 연구실 · 5장 · 현장 사례', '현장 사례 — 추천, 감시, 기억, 도입',
              '벡터 DB는 실제로 어떤 자리에 끼워 쓰고, 어디서는 표만으로 충분할까?',
              '마지막 수업. 하루는 이제 떨지 않고 인턴들에게 현장 문제 네 가지를 던집니다. 영화 추천, SNS 상황실, 챗봇의 기억, 그리고 "우리 회사에 벡터 DB가 필요할까".',
              [('4가지', '현장 사례', 'i'), (num(SP['cos']['f1'], 3), '둘째 주 광고 걸러내기 F1 (좌표)', 'g'), (num(SP['jac']['f1'], 3), '같은 조건 글자 겹침 F1', 'a'), ('9일째', '결제 오류 이야기 묶음이 생긴 날', 'r')],
              [('doc', 'front', '정규 수업 마지막 날입니다. 오늘은 하루가 처음부터 끝까지 진행합니다.'),
               ('asst', 'e16', '네! 시아, 모아, 오늘은 현장 문제예요. 제가 회사 사람이라고 생각하고 답해 줘요.'),
               ('sia', 'firm', '준비됐어요.'), ('moa', 'cheer', '노트 마지막 장이에요!')],
              crowd('"하루, 오늘은 하나도 안 떤다!" "첫날이랑 완전 달라."', moods=('e16', 'e01', 'e16')))
    return build(P, title='5장 · 현장 사례 — 영화 추천, SNS 모니터링, 챗봇의 기억, 도입 판단 | 벡터 DB 연구실',
                 desc='별점과 리뷰 좌표로 하는 영화 추천, 광고 걸러내기와 새 이슈 알림, 대화 기억 창고, 벡터 DB 도입 판단을 실험으로 봅니다.',
                 nav=nav, cover_html=cov, hero=hr,
                 body=body() + footer([('리뷰·SNS·대화', '이 연구실이 만든 가상 데이터'), ('Annoy', 'github.com/spotify/annoy — README Background (음악 추천에 사용)'),
                                       ('CLIP', 'Radford 외 (2021) Learning Transferable Visual Models From Natural Language Supervision, ICML 2021'),
                                       ('임베딩에서 원문 복원', 'Morris 외 (2023) Text Embeddings Reveal (Almost) As Much As Text, EMNLP 2023'),
                                       ('pgvector', 'github.com/pgvector/pgvector')],
                                      ['챗봇 답과 기억 대화는 미리 적어 둔 흉내입니다. 기억 꺼내기 점수는 실제 계산입니다.', '도입 판단 도우미는 설명용 규칙입니다.', '광고·새 이야기 실험의 SNS 글은 가상입니다.'],
                                      prev=('04_llm_rag.html', '4장 · LLM과 RAG'), nxt=('06_attention_3d.html', '6장 · LLM은 찾은 자료를 어떻게 읽나')),
                 gloss=GLOSS, quizzes=QUIZ, page_js=JS, og='og_05')


if __name__ == '__main__':
    print(build_page())
