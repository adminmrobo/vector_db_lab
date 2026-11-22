# -*- coding: utf-8 -*-
"""1장 · 표에 담기지 않는 말 — 관계형 DB의 한계와 자연어 데이터의 특징"""
from lib import *

P = '01_why_not_table.html'
S0 = R['search'][0]  # '재밌는 영화 리뷰'
FL_ = R['fun_like']; WL = R['waste_like']; SM = R['search_mean']


def body():
    b = three([
        ('무엇을', '영화 별점과 리뷰 문장, SNS 글을 관계형 데이터베이스(표)에 넣고 찾아보며, 표가 잘하는 일과 못하는 일을 나눠 봅니다.'),
        ('왜 중요한가', '회사 데이터의 대부분은 문장·사진·소리처럼 정해진 항목이 없는 데이터입니다. 표만으로는 그 "뜻"을 찾기 어렵습니다. 이 어려움이 벡터 DB가 나온 이유입니다.'),
        ('업무에서는', '"불만 리뷰만 모아 줘", "결제 오류 이야기가 늘고 있나?" 같은 요청을 받았을 때, SQL 검색으로 어디까지 되고 어디서 막히는지 판단할 수 있습니다.')],
        '코드·수식을 몰라도 됩니다. 버튼을 누르고 결과를 보며 따라오면 됩니다. 수식이 나오면 조수 하루가 하나씩 물어봅니다.',
        [('DB', 'Database, 데이터베이스'), ('SQL', 'Structured Query Language, 표에 묻는 질문 언어'), ('LIKE', 'SQL에서 글자 일부가 들어 있는지 찾는 조건'), ('F1', '정밀도와 재현율을 함께 본 점수')])

    b += ('<section class="level" id="cast"><div class="wrap"><h2>이 장의 식구와 사용법</h2>' + cast_cards([
        ('asst', 'e15', '이번 시리즈의 진행자. 박사에게 처음으로 인턴 교육을 맡아 조금 긴장했습니다. 인턴에게 질문하며 수업을 끌고 갑니다.'),
        ('sia', 'explain', '인턴1. 순서와 규칙을 좋아합니다. 데이터베이스 설계 강좌를 막 끝냈습니다.'),
        ('moa', 'report', '인턴2. 꼼꼼한 기록 담당. 「DB 설계 노트」로 표로 할 때와 벡터로 할 때를 나란히 보여 줍니다.'),
        ('fly', 'magnify', '의심하는 쪽. "그 숫자, 정말 그럴듯해?"를 입에 달고 삽니다. 막히면 실험 버튼을 가리켜 줍니다.'),
        ('robo', 'smile', '확신하는 쪽. 크고 빠른 것을 좋아합니다. 악역은 아니고, 성급할 뿐입니다.'),
        ('doc', 'board', '상황을 던지고, 단계마다 정리합니다. 판정은 언제나 숫자대로.')]) +
        '<p>밑줄 친 말을 누르거나 마우스를 올리면 뜻이 나옵니다. 오른쪽 아래 도우미에서 밑줄을 끌 수 있습니다. '
        '이 장은 <a href="%s">「데이터베이스 설계」</a> 강좌의 표·SQL과 <a href="%s">「인공지능과 자연어 데이터 분석」</a> 강좌의 자연어 특징을 이어 붙입니다. 두 강좌를 보지 않았어도 읽을 수 있게 썼습니다.</p></div></section>' % (DBD, NLP))

    b += section('why', '왜 이 주제인가', '<div class="steps">'
                 '<div><span class="n">1</span><h4>별점은 쉽다</h4><p>별점 4점은 숫자 하나입니다. 평균·정렬·조건 검색이 SQL 한 줄로 정확하게 됩니다.</p></div>'
                 '<div><span class="n">2</span><h4>문장은 어렵다</h4><p>"시간 가는 줄 몰랐다"와 "꿀잼"은 글자가 하나도 겹치지 않는데 뜻이 같습니다. 표는 이 둘을 같다고 알아보지 못합니다.</p></div>'
                 '<div><span class="n">3</span><h4>그래서 벡터</h4><p>문장의 뜻을 숫자 좌표로 바꿔 두고, 가까운 좌표를 찾는 창고가 벡터 DB입니다. 2장에서 시작해 이 창고를 직접 만듭니다.</p></div></div>'
                 + say('doc', 'front', '이 시리즈는 한계 보기(1장) → 뜻을 좌표로(2장) → 창고 만들기(3장) → LLM과 RAG(4장) → 현장 사례(5장) → 실전 연습장 순서로 갑니다. 1장은 "왜 표만으로는 안 되나"를 숫자로 확인합니다.'))

    b += section('map', '큰 그림 — 이 장은 어디쯤인가',
                 '<div class="mapbar" aria-label="시리즈 흐름"><span class="on">1장 · 표의 한계</span><i>→</i><span>2장 · 임베딩</span><i>→</i>'
                 '<span>3장 · 벡터 창고</span><i>→</i><span>4장 · LLM과 RAG</span><i>→</i><span>5장 · 현장 사례</span><i>→</i><span>실전 연습장</span></div>'
                 '<div class="tw"><table class="tb"><tr><th>이 시리즈의 데이터 (모두 가상)</th><th>내용</th></tr>'
                 '<tr><td>영화 8편</td><td>「별빛 정거장」(SF)부터 「검은 서버실」(스릴러)까지. 제목·장르·개봉 연도·상영 시간</td></tr>'
                 '<tr><td>리뷰 %s개</td><td>별점 1~5점 + 리뷰 문장. 표준어·줄임말·신조어·부정어·비꼬는 말이 섞여 있습니다</td></tr>'
                 '<tr><td>SNS 글 %s개</td><td>14일 동안 올라온 영화 이야기·음식·날씨·일상, 말만 바꾼 광고, 9일째부터 늘어나는 결제 오류 이야기</td></tr>'
                 '<tr><td>사람이 붙인 이름표</td><td>리뷰마다 "무엇을 좋다·나쁘다고 했나"(재미·감동·공포·연기 등)를 따로 적어 두었습니다. 검색을 채점할 때만 씁니다</td></tr></table></div>' % (R['n']['reviews'], R['n']['sns']))

    # ── 1-1 별점은 표에 잘 들어간다
    s = say('doc', 'think', '상황 하나. 영화 앱에 별점과 리뷰가 하루 수천 건씩 들어옵니다. 영화별 평균 별점을 내일 아침 회의에 가져가야 한다면, 어디에 어떻게 저장해 둘까요?')
    s += recap('관계형 데이터베이스', '<p>데이터를 행(한 건)과 열(항목)로 된 표에 담고, 표끼리는 번호(키)로 잇습니다. 영화 표의 <b>영화 번호</b>를 리뷰 표가 함께 적어 두면, 두 표를 이어 "영화별 평균"을 낼 수 있습니다. '
               '질문은 SQL이라는 정해진 문장으로 합니다. 자세한 내용은 <a href="%s">데이터베이스 설계 강좌</a>의 6·9·10주차에 있습니다.</p>' % DBD)
    s += duo(why([('문제 상황', '기록이 많고 매일 늘어납니다. 같은 숫자를 누가 물어도 똑같이, 빠르게 답해야 합니다.'),
                  ('앞 방법의 한계', '엑셀 파일을 여기저기 두면 버전이 갈리고, 동시에 고치다 기록이 깨집니다.'),
                  ('해법', '관계형 DB에 표로 저장하고 SQL로 묻습니다. 별점·날짜처럼 항목이 정해진 데이터(정형 데이터)에 가장 강합니다.')],
                 '도서관 대출 기록처럼, 항목이 정해진 기록은 "3월에 빌린 책 수"를 바로 셉니다.'),
             pair('일상으로 치면', '시험 점수표는 "평균", "80점 이상 몇 명"을 바로 셉니다. 점수가 숫자이고 자리가 정해져 있기 때문입니다.',
                  '영화 앱에서는', '리뷰 표에 리뷰 번호·영화 번호·별점·날짜·문장을 열로 둡니다. 별점 열로는 평균·정렬·조건 검색이 모두 정확합니다.'))
    s += dbnote('영화 표와 리뷰 표를 나누고 영화 번호로 잇습니다(정규화). 영화별 평균 별점은 <code>AVG(stars) … GROUP BY</code> 한 줄입니다.',
                '이 표를 버리지 않습니다. 별점·날짜·장르는 그대로 표에 두고, <b>문장의 뜻</b>만 따로 숫자 좌표로 만들어 함께 저장합니다(3장).')
    s += talk([('asst', 'e15', '(목소리가 살짝 떨린다) 그, 그럼 첫 질문! 시아, 영화별 평균 별점을 구하려면 SQL에서 무엇을 쓰면 될까?'),
               ('sia', 'explain', '영화 번호로 묶는 GROUP BY와 평균을 내는 AVG요. 강좌에서 배웠어요!'),
               ('robo', 'coin', '봐, 표만 있으면 뭐든 한 줄이야. 리뷰 문장도 똑같이 찾으면 되지!'),
               ('fly', 'point', '숫자는 그렇지. 아래 실습실에서 "영화별 평균"을 눌러 보고, 그다음 문장 조건도 걸어 봐.'),
               ('asst', 'report', '평균 별점이 영화마다 바로 나와요. 전체 평균은 %s점이에요.' % num(R['avg_all'], 2))])
    s += crowd('"하루 목소리 떨리는 거 들려?" "그래도 첫 질문은 잘 던졌어."')
    s += panel('p11', '실험 · 페이지 안 SQL 실습실 — 별점 표에 묻기', '가상 데이터 · 페이지가 직접 계산',
               '<div class="ctrl"><div class="group"><span class="glabel">영화</span><select class="sel" id="mv11"></select></div>'
               '<div class="group"><span class="glabel">별점</span><input type="range" id="st11" min="1" max="5" value="1" aria-label="최소 별점"><span class="val" id="stv11">1점 이상</span></div>'
               '<div class="group"><span class="glabel">묻는 것</span><button class="bt" data-g="avg" aria-pressed="true">영화별 평균</button><button class="bt" data-g="dist" aria-pressed="false">별점 분포</button>'
               '<button class="bt" data-g="rows" aria-pressed="false">원문 보기</button></div></div>'
               '<div class="sqlbox" id="sql11" aria-live="polite"></div>' + canvas('cv11', 280, '영화별 평균 별점 또는 별점 분포 막대그래프') +
               '<ul class="res" id="rs11"></ul><section class="kpis" id="k11" aria-label="숫자 요약"></section><div class="insight" id="in11" aria-live="polite"></div>', real=True)
    s += explain(['별점은 숫자 하나라서 평균·정렬·조건(4점 이상)이 정확하고 빠릅니다. 같은 SQL은 언제 실행해도 같은 답을 냅니다.',
                  '영화 표와 리뷰 표를 영화 번호로 이어서, 장르별·영화별 집계도 한 줄로 됩니다.',
                  '관계형 DB는 돈·주문·재고처럼 한 건도 틀리면 안 되는 기록에 강합니다(트랜잭션). 이 장점은 벡터 DB 시대에도 그대로입니다.'],
                 'SQL은 리뷰 문장 열을 "글자들의 줄"로만 봅니다. "이 리뷰가 재밌다는 뜻인가"는 묻지 못합니다. 다음 단계에서 확인합니다.')
    s += codefold([('SELECT m.title, AVG(r.stars) FROM review r JOIN movie m ON r.movie_id = m.id GROUP BY m.title;', '영화 표와 리뷰 표를 이어 영화별 평균 별점을 냅니다'),
                   ('SELECT stars, COUNT(*) FROM review GROUP BY stars;', '별점별 리뷰 수(분포)')])
    s += wrapup('숫자로 된 항목은 표가 가장 잘 다룹니다. 이 장점은 벡터 DB가 나와도 사라지지 않습니다. 문제는 그 옆의 문장 열입니다.')
    s += quiz('q11')
    b += step('s1', '1-1', '별점은 표에 잘 들어간다 — 정형 데이터와 SQL', ['방법: 관계형 DB · SQL 집계', '일상: 시험 점수표'], s)

    # ── 1-2 LIKE로 찾으면
    lk = S0['like']
    s = say('doc', 'think', '마케팅팀에서 연락이 왔습니다. "광고에 쓸 테니 재밌다는 리뷰만 다 모아 주세요." 리뷰 문장은 표의 한 열에 들어 있습니다. 어떻게 찾을까요?')
    s += duo(why([('문제 상황', '문장 속 "뜻"으로 찾고 싶습니다. 재밌다는 말은 "재밌어요", "꿀잼", "시간 가는 줄 몰랐다"처럼 여러 모양으로 옵니다.'),
                  ('앞 방법의 한계', 'SQL의 LIKE는 정한 글자가 문장 안에 "그대로" 들어 있는지만 봅니다. 다른 말투는 놓치고, "안 재밌어요"는 잘못 데려옵니다.'),
                  ('해법(예고)', '글자가 아니라 뜻으로 찾는 방법이 필요합니다. 그 방법이 2장의 임베딩입니다. 이 단계에서는 먼저 얼마나 놓치는지 숫자로 잽니다.')],
                 '"사과"라는 글자로만 책을 찾으면, "애플"과 "능금"이 적힌 책은 영영 못 찾습니다.'),
             mathbox('정밀도, 재현율… 이름이 너무 비슷해요. 뭐가 뭐예요?', '확률과 통계(고등학교) — 비율, 그리고 조건부 확률의 생각',
                     '정밀도 = 맞게 찾은 수 ÷ 찾은 수<br>재현율 = 맞게 찾은 수 ÷ 정답 전체 수',
                     [('정밀도', '정밀도', '데려온 것 중 진짜가 몇 %인가. "헛걸음이 적은가"'), ('재현율', '재현율', '진짜 전체 중 몇 %를 데려왔나. "빠뜨림이 적은가"'),
                      ('F1', '에프원', '둘을 함께 본 점수. 둘 중 하나라도 낮으면 낮아집니다')],
                     'LIKE \'%%재밌%%\'로 찾으면 %d개가 나오고, 그중 진짜 재밌다는 리뷰는 %d개입니다. 정밀도 = %d ÷ %d ≈ <b>%s</b>. '
                     '그런데 재밌다는 리뷰는 전부 %d개라서 재현율 = %d ÷ %d ≈ <b>%s</b>입니다.' % (lk['n'], lk['tp'], lk['tp'], lk['n'], pct(lk['p']), S0['rel'], lk['tp'], S0['rel'], pct(lk['r'])),
                     '찾은 것은 대부분 맞는데, 찾아야 할 것의 %s밖에 못 찾았네요. 정밀도만 보면 속겠어요!' % pct(lk['r'], 0)))
    s += talk([('asst', 'e20', '모, 모아! LIKE \'%재밌%\'로 찾으면 재밌다는 리뷰를 다 찾을 수 있을까?'),
               ('moa', 'ok', '네! "재밌"이라는 글자가 들어 있으면 다 나오니까요.'),
               ('robo', 'happy', '%d개 나왔다! 마케팅팀에 보내고 퇴근하자.' % lk['n']),
               ('fly', 'point', '이름표로 세면 재밌다는 리뷰는 %d개야. 아래에서 "놓친 리뷰 보기"를 켜고, 빨간 물결 밑줄도 찾아봐.' % S0['rel']),
               ('asst', 'report', '놓친 리뷰에 "꿀잼", "몰입감 최고"가 잔뜩 있어요. 그리고 찾은 것 중 %d개는 "안 재밌어요"였어요.' % FL_['neg'])])
    s += crowd('"하루 얼굴 빨개졌어…" "괜찮아, 숫자는 정확하게 읽었잖아."', moods=('e02', 'e15', 'e01'))
    s += panel('p12', '실험 · LIKE 검색기 — 글자로 뜻 찾기', '가상 데이터 · 이름표로 채점',
               '<div class="ctrl"><div class="group"><span class="glabel">찾을 뜻 (채점 기준)</span><select class="sel" id="q12"></select></div>'
               '<div class="group"><span class="glabel">LIKE 낱말</span><input type="text" id="w12" value="재밌" aria-label="LIKE에 넣을 낱말" style="width:120px"></div>'
               '<div class="group"><button class="bt" id="miss12" aria-pressed="false">놓친 리뷰 보기</button></div></div>'
               '<div class="chips" id="ch12" aria-label="낱말 빨리 넣기"></div>'
               '<div class="sqlbox" id="sql12"></div><section class="kpis" id="k12" aria-label="채점"></section>'
               '<ul class="res" id="rs12"></ul><div class="insight" id="in12" aria-live="polite"></div>', real=True)
    s += explain(['LIKE는 글자 모양이 같은지만 봅니다. "꿀잼", "존잼", "시간 가는 줄 몰랐다"는 "재밌"이라는 글자가 없어 모두 빠집니다.',
                  '"안 재밌어요", "별로 재미없었음"처럼 부정어가 붙은 문장도 글자가 같으면 함께 딸려 옵니다(빨간 물결 밑줄).',
                  '여덟 가지 뜻(재미·지루·감동·공포·연기·음악·돈 아까움·스토리)에 낱말 하나씩 LIKE를 걸면 F1 평균이 <b>%s</b>입니다.' % num(SM['like'], 3)],
                 '낱말을 여러 개 넣으면 놓침은 줄지만, 사람이 그 낱말 목록을 계속 만들고 고쳐야 합니다. 다음 단계에서 그 비용을 봅니다.')
    s += aicheck('주판봇의 "돈 아까운 영화" 목록',
                 '<p>주판봇이 LIKE \'%%아깝%%\'으로 "돈 아까운 영화" 리뷰 %d개를 뽑아 보고서를 냈습니다. "이 영화들은 관객이 돈 아까워한 영화입니다!"</p>'
                 '<p><b>확인 질문</b> ① 이 %d개가 모두 "돈이 아깝다"는 뜻일까요? ② 무엇을 확인하면 될까요?</p>'
                 '<details><summary>생각해 본 뒤 열어 보기</summary><p>① 아닙니다. 그중 %d개는 "배우가 아깝다" — 배우는 좋은데 영화가 아쉽다는 뜻입니다. 같은 글자가 다른 뜻으로 쓰였습니다(다의어). '
                 '② 결과 몇 개를 직접 열어 읽어 보는 것이 가장 빠른 확인입니다. 위 검색기에 "아깝"을 넣고 결과를 훑어보세요.</p></details>' % (WL['n'], WL['n'], WL['actor']))
    s += codefold([("SELECT text FROM review WHERE text LIKE '%재밌%';", '"재밌"이라는 글자가 들어 있는 리뷰를 모두 찾습니다'),
                   ("... WHERE text LIKE '%재밌%' OR text LIKE '%꿀잼%' OR ...", '말투마다 조건을 하나씩 늘리는 방법. 목록은 사람이 관리합니다')])
    s += wrapup('글자로 찾으면 "찾은 것"은 그럴듯해 보여도 "놓친 것"이 많습니다. 검색 결과는 정밀도와 재현율을 함께 봐야 합니다.')
    s += quiz('q12')
    b += step('s2', '1-2', '리뷰 문장을 LIKE로 찾으면 — 글자와 뜻은 다르다', ['방법: SQL LIKE · 정밀도·재현율', '일상: 글자로만 책 찾기'], s)

    # ── 1-3 항목·규칙을 늘리면
    s = say('doc', 'think', '그럼 사람이 규칙을 만들어 주면 어떨까요? 리뷰마다 "재미" "감동" 항목을 두고, SNS 글은 "영화" "음식" 태그로 나누는 규칙을 짜는 겁니다.')
    s += duo(why([('문제 상황', '문장의 뜻을 표의 항목(열)이나 태그로 옮겨 두면 SQL로 찾을 수 있습니다.'),
                  ('앞 방법의 한계', 'LIKE 낱말 하나로는 말투가 조금만 달라도 놓칩니다.'),
                  ('해법(사람의 규칙)', '주제별 낱말 목록(분류 규칙)이나 동의어 사전을 만들어 태그를 붙입니다. 잘 만들면 꽤 정확합니다. 대신 말이 바뀔 때마다 사람이 고쳐야 합니다.')],
                 '서랍마다 이름표를 붙여 정리하면 찾기 쉽습니다. 그런데 이름표에 없는 물건이 들어오면 서랍을 새로 짜야 합니다.'),
             pair('일상으로 치면', '가계부 항목을 "식비·교통·통신"으로 정해 두면 정리는 쉽지만, 새로운 지출(구독료·후원)이 생길 때마다 항목을 늘려야 합니다.',
                  'SNS 분석에서는', '"영화·음식·날씨·일·광고" 태그 규칙을 첫 주에 만들었습니다. 둘째 주에 결제 오류 이야기와 새 말투의 광고가 들어오면 규칙이 따라가지 못합니다.'))
    s += dbnote('감정·주제마다 열을 늘리거나 태그 표를 따로 만들어 리뷰와 잇습니다. 새 주제가 생기면 표 구조를 바꾸고(ALTER TABLE) 규칙을 다시 짭니다.',
                '뜻을 미리 정한 항목에 나눠 담지 않고, 문장 전체를 좌표 하나로 저장합니다. 새 말투가 들어와도 표 구조는 그대로이고, "가까운 글"로 찾습니다.')
    s += talk([('asst', 'e15', '시, 시아! SNS 글을 주제 태그로 나누는 규칙을 만들어 볼래?'),
               ('sia', 'firm', '영화·음식·날씨·일·광고 다섯 개면 충분해요. 낱말 목록도 다 짰어요!'),
               ('robo', 'chart', '첫 주 분류율 보라고. 규칙만 잘 짜면 끝이야.'),
               ('fly', 'point', '날짜 막대를 둘째 주로 넘겨 봐. 처음 보는 이야기가 들어오면 어떻게 될까?'),
               ('asst', 'report', '9일째부터 "결제 오류" 글이 미분류로 쌓여요. 새 말투 광고는 "영화"로 잘못 들어갔어요.')])
    s += panel('p13', '실험 · SNS 태그 규칙 설계기 — 사람이 만든 체계는 얼마나 버티나', '가상 데이터 · 페이지가 직접 계산',
               '<div class="ctrl"><div class="group"><span class="glabel">보는 날</span><input type="range" id="d13" min="1" max="14" value="7" aria-label="날짜"><span class="val" id="dv13">1~7일</span></div>'
               '<div class="group"><span class="glabel">규칙 고치기</span><button class="bt" id="add13" aria-pressed="false">새 태그 "결제 오류" 추가</button>'
               '<button class="bt" id="dm13" aria-pressed="false">광고 규칙에 "DM" 추가</button></div></div>'
               + canvas('cv13', 260, '날짜별 SNS 글의 분류 결과 쌓은 막대') +
               '<div class="legend" id="lg13"></div><section class="kpis" id="k13" aria-label="숫자 요약"></section><ul class="res" id="rs13"></ul>'
               '<div class="insight" id="in13" aria-live="polite"></div>', real=True)
    s += explain(['첫 주 글로 만든 규칙은 첫 주에는 잘 맞습니다. 처음 보는 이야기(결제 오류)와 새 말투(DM 광고)가 들어오면 미분류·오분류가 늘어납니다.',
                  '버튼으로 규칙을 고치면 다시 좋아집니다. 그 버튼을 누르는 일이 현장에서는 사람의 시간입니다.',
                  '리뷰 검색도 같습니다. 사람이 동의어 사전을 잘 만들면 F1 평균이 <b>%s</b>까지 오릅니다(낱말 하나 LIKE는 %s). 사전을 만들고 고치는 비용을 감당할 수 있느냐가 문제입니다.' % (num(SM['dict'], 3), num(SM['like'], 3))],
                 '규칙은 사람이 미리 생각한 것만 잡습니다. "아직 이름이 없는 새 이야기"를 알아차리려면 규칙이 아니라 "기존 글과 얼마나 다른가"를 재야 합니다(5장).')
    s += wrapup('사람이 만든 체계는 정확하지만, 말이 바뀌는 속도를 따라가려면 계속 손봐야 합니다. 체계를 미리 정하지 않고 뜻으로 묶는 방법이 필요합니다.')
    s += quiz('q13')
    b += step('s3', '1-3', '항목과 규칙을 늘리면 될까 — 사람이 만든 체계의 한계', ['방법: 태그 규칙 · 동의어 사전', '일상: 가계부 항목'], s)

    # ── 1-4 자연어의 특징
    s = say('doc', 'think', '왜 문장은 이렇게 다루기 어려울까요? 「인공지능과 자연어 데이터 분석」 강의에서 정리한 특징을 이 연구실의 리뷰와 SNS 글로 다시 확인해 봅시다.')
    s += recap('정형 데이터와 비정형 데이터', '<p>정형 데이터는 정해진 항목에 담깁니다(별점, 날짜, 금액). 비정형 데이터는 정해진 항목이 없습니다(문장, 사진, 소리). '
               '<a href="%s">자연어 데이터 분석 강좌</a> 1-2쪽은 "자연어는 정해진 자리가 없어 분석 전에 쪼개고 숫자로 바꾸는 일이 먼저"라고 설명합니다.</p>' % NLP)
    s += duo(why([('문제 상황', '같은 뜻이 여러 모양으로 오고, 같은 모양이 여러 뜻으로 쓰입니다.'),
                  ('앞 방법의 한계', '글자 일치(LIKE)와 사람의 규칙은 "모양"만 봅니다.'),
                  ('해법(예고)', '문장의 뜻을 숫자 좌표로 바꿔 "뜻이 가까운가"를 재면, 모양이 달라도 찾을 수 있습니다. 카드마다 오른쪽 "뜻 점수"가 그 맛보기입니다.')],
                 '외국어를 배울 때 단어 철자가 아니라 "무슨 뜻으로 쓰였나"를 익혀야 대화가 되는 것과 같습니다.'),
             pair('강의에서는', '자연어 데이터 분석 강좌는 비정형, 맥락 의존, 시대·유행에 따른 변화, 단위 없음, 어순·문법, 사전에 없는 말, 같은 뜻 다른 표현, 잡음, 다의어를 짚습니다.',
                  '이 연구실에서는', '아홉 가지를 리뷰·SNS 문장 쌍으로 하나씩 보여 줍니다. "글자 겹침"은 낮은데 "같은 뜻"인 쌍, 글자는 같은데 "다른 뜻"인 쌍이 핵심입니다.'))
    s += talk([('asst', 'e15', '모아, "꿀잼"이랑 "시간 가는 줄 몰랐다"는 글자가 몇 개 겹쳐?'),
               ('moa', 'think', '하나도 안 겹쳐요. 그런데 뜻은 같아요… 이상하네요.'),
               ('robo', 'coin', '글자가 안 겹치면 다른 말이지. 컴퓨터는 글자를 보는 거야!'),
               ('fly', 'point', '카드 ⑦을 눌러서 가운데 "글자 겹침"과 오른쪽 "뜻 점수"를 나란히 봐.'),
               ('asst', 'report', '글자 겹침은 0인데 뜻 점수는 거의 1이에요. 2장에서 이 점수를 만드는 법을 배워요.')])
    s += panel('p14', '실험 · 자연어 특징 카드 9장 — 글자 겹침 vs 뜻 점수', '가상 데이터 · 페이지가 직접 계산',
               '<div class="chips" id="cards14" role="group" aria-label="특징 카드"></div><div id="view14"></div>'
               '<p class="small muted">글자 겹침: 두 문장을 글자 두 개씩 끊은 조각이 얼마나 겹치나(0~1). 뜻 점수: 2장에서 만들 교육용 임베딩의 코사인 유사도(−1~1). 사람 판단은 이 연구실이 붙인 것입니다.</p>', real=True)
    s += explain(['①~⑨는 서로 겹칩니다. 예를 들어 "핵노잼"은 신조어(③)이면서 같은 뜻 다른 표현(⑦)이고, 사전에 없는 말(⑥)일 수도 있습니다.',
                  '글자 겹침은 "모양이 같은가"를, 뜻 점수는 "뜻이 가까운가"를 잽니다. 둘이 엇갈리는 카드(③⑤⑦⑨)가 표·LIKE가 실패하는 자리입니다.',
                  '뜻 점수도 완벽하지 않습니다. 카드 ⑨의 비꼬는 말은 뜻 점수로도 잘 안 잡힙니다. AI 판단이 필요한 자리입니다.'],
                 '이 장의 뜻 점수는 사람이 만든 작은 사전(교육용 임베딩)으로 계산합니다. 실제 서비스의 임베딩 모델은 수많은 문장에서 스스로 배우며, 그래도 부정어·비꼼에서 자주 틀립니다.')
    s += bridge('gen', '생성 AI로 치면', 'ChatGPT 같은 대형 언어 모델(LLM)도 문장을 먼저 토큰(조각)으로 자르고 숫자로 바꿔 다룹니다. 이 장의 아홉 가지 특징은 LLM에게도 그대로 어려운 문제입니다.',
                '사람은 맥락과 말투로 비꼼을 알아채지만, 숫자 좌표 하나에 그 모든 것이 담기지는 않습니다.')
    s += wrapup('자연어는 정해진 자리가 없고, 모양과 뜻이 자주 엇갈립니다. 그래서 "모양이 같은가"가 아니라 "뜻이 가까운가"를 재는 도구가 필요합니다.')
    s += quiz('q14')
    b += step('s4', '1-4', '자연어 데이터의 아홉 가지 특징 — 모양과 뜻이 엇갈린다', ['방법: 특징 카드 · 글자 겹침', '일상: 철자와 뜻'], s)

    b += duel('d1', '"재밌다는 리뷰" 찾기 — 낱말 하나 LIKE vs 사람이 만든 동의어 사전', '동의어 사전 (재밌·재미있·꿀잼·존잼·몰입)', "LIKE '%재밌%' 하나",
              '"말투가 여러 가지면 사전을 만들어야지. 하나로는 다 못 잡아."', '"재밌다는 말엔 다 재밌이 들어가. 한 단어면 충분해!"',
              'F1 (정밀도와 재현율을 함께 본 점수, 사람이 붙인 이름표로 채점)')

    b += section('sum', '정리 — 표가 잘하는 일과 못하는 일',
                 '<div class="tw"><table class="tb"><tr><th></th><th>관계형 DB (표·SQL)</th><th>벡터 DB (2장에서 시작)</th></tr>'
                 '<tr><td>잘 다루는 데이터</td><td>별점·날짜·금액처럼 항목이 정해진 데이터</td><td>문장·사진·소리처럼 항목이 정해지지 않은 데이터</td></tr>'
                 '<tr><td>찾는 방식</td><td>정확히 같은 값, 범위, 글자 포함(LIKE)</td><td>뜻이 가까운 것 (가장 가까운 좌표 k개)</td></tr>'
                 '<tr><td>강점</td><td>정확한 집계, 한 건도 틀리면 안 되는 기록(트랜잭션)</td><td>말투가 달라도 같은 뜻을 찾음, 새 말에도 구조를 안 바꿈</td></tr>'
                 '<tr><td>약점</td><td>같은 뜻 다른 표현, 부정어, 다의어, 신조어</td><td>정확한 값 일치, 오류 코드 같은 고유 기호(4장), 비꼼</td></tr></table></div>'
                 '<div class="steps"><div><span class="n">1</span><h4>표는 버리지 않는다</h4><p>별점·날짜·권한 같은 정형 정보는 계속 표가 맡습니다. 실제 서비스는 둘을 함께 씁니다.</p></div>'
                 '<div><span class="n">2</span><h4>글자 ≠ 뜻</h4><p>LIKE는 정밀도가 높아 보여도 재현율이 낮습니다. 두 숫자를 함께 봐야 합니다.</p></div>'
                 '<div><span class="n">3</span><h4>규칙은 늙는다</h4><p>사람이 만든 체계는 말이 바뀌면 고쳐야 합니다. 뜻으로 재는 도구가 다음 장의 주제입니다.</p></div></div>'
                 + bridge('field', '현장에 옮기면', '고객 문의 게시판에서 "환불" 글을 LIKE로 모으면 "돈 돌려받고 싶어요", "결제 취소해 주세요"를 놓칩니다. 검색 결과를 보고할 때는 "몇 개 찾았다"와 함께 "몇 개를 놓쳤을까"를 표본으로 확인합니다.',
                          '현장의 정답 이름표는 비싸서, 전부가 아니라 일부 표본에만 붙여 재현율을 어림합니다.'))

    b += outro([('doc', 'front', '오늘 세 줄 정리. ① 별점 같은 정형 데이터는 표와 SQL이 가장 잘한다. ② 문장은 모양과 뜻이 엇갈려 LIKE와 규칙으로는 놓친다. ③ 그래서 뜻을 숫자 좌표로 바꾸는 도구가 필요하다.'),
                ('fly', 'arms', '찾은 것만 세면 늘 잘한 것 같아. 놓친 것을 세는 습관, 잊지 마.'),
                ('robo', 'sigh', '한 단어면 될 줄 알았는데… 이번 판은 손절. 2장에서 큰 숫자로 본전 찾는다.'),
                ('sia', 'proud', '규칙이 늙는다는 말, 노트에 적었어요.'),
                ('moa', 'cheer', 'DB 설계 노트에 "벡터로 할 때" 항목을 새로 만들게요!'),
                ('asst', 'e01', '휴, 첫 수업 끝! 다음 장에서는 문장을 진짜 숫자 좌표로 바꿔 볼게요.')],
               '연구실 화이트보드 앞에서 하루가 인턴 둘과 함께 안도하고, 방청석의 X1~X3가 박수 치는 장면',
               crowd('"하루 첫 수업 무사히 끝났다!" "박수!"', moods=('e01', 'e16', 'e01')))
    return b


GLOSS = {
    '관계형 데이터베이스': ['관계형 데이터베이스 (RDB)', '데이터를 행과 열의 표에 담고, 표끼리 키(번호)로 잇는 데이터베이스. MySQL·PostgreSQL 등.'],
    'SQL': ['SQL', '표에 묻는 정해진 질문 문장. SELECT(꺼내기), WHERE(조건), GROUP BY(묶기) 등.'],
    'LIKE': ['LIKE', 'SQL에서 "이 글자가 들어 있나"를 보는 조건. %는 "아무 글자나"라는 뜻.'],
    '정형 데이터': ['정형 데이터 (structured data)', '정해진 항목(열)에 담기는 데이터. 별점, 날짜, 금액.'],
    '비정형 데이터': ['비정형 데이터 (unstructured data)', '정해진 항목이 없는 데이터. 문장, 사진, 소리, 영상.'],
    '정밀도': ['정밀도 (precision)', '찾아온 것 중 진짜 정답의 비율. 헛걸음이 적은가.'],
    '재현율': ['재현율 (recall)', '진짜 정답 전체 중 찾아온 비율. 빠뜨림이 적은가.'],
    'F1': ['F1 점수', '정밀도와 재현율의 조화 평균. 둘 중 하나라도 낮으면 낮아집니다.'],
    '동의어 사전': ['동의어 사전', '같은 뜻의 여러 표현을 사람이 모아 둔 목록. 검색 조건을 늘릴 때 씁니다.'],
    '부정어': ['부정어', '"안", "못", "~지 않다"처럼 뜻을 뒤집는 말.'],
    '다의어': ['다의어', '모양은 같은데 뜻이 여럿인 말. "아깝다"(돈이 아깝다 / 배우가 아깝다).'],
    '신조어': ['신조어', '새로 생긴 말. 꿀잼, 존잼, 핵노잼 등. 사전과 규칙이 늦게 따라갑니다.'],
    '트랜잭션': ['트랜잭션 (transaction)', '여러 작업을 "모두 되거나 모두 안 되거나"로 묶는 단위. 돈·주문 기록에 필수.'],
    '정규화': ['정규화 (normalization)', '같은 정보가 여러 표에 반복되지 않게 표를 나누는 설계. 데이터베이스 설계 강좌 12주차.'],
    '임베딩': ['임베딩 (embedding)', '문장·단어·그림의 뜻을 숫자 좌표(벡터)로 바꾼 것. 2장의 주제.'],
}

QUIZ = {
    'q11': [{'q': '관계형 DB와 SQL이 가장 잘하는 일은?', 'o': ['"재밌다는 뜻"의 리뷰 찾기', '영화별 평균 별점 정확히 내기', '비꼬는 말 알아채기'], 'a': 1,
             'why': '별점은 정해진 항목의 숫자라서 평균·조건 검색이 정확합니다.', 'hint': '숫자 열과 문장 열 중 어느 쪽이 SQL과 잘 맞을까요?'},
            {'q': '벡터 DB를 쓰면 별점·날짜를 담은 표는 어떻게 되나?', 'o': ['버린다', '그대로 두고 문장의 뜻만 좌표로 따로 저장한다', '모두 문장으로 바꾼다'], 'a': 1,
             'why': '정형 정보는 표가 계속 맡고, 벡터는 문장의 뜻을 맡습니다. 실제 서비스는 둘을 함께 씁니다.', 'hint': '"표는 버리지 않는다"를 떠올려 보세요.'}],
    'q12': [{'q': 'LIKE로 찾은 17개 중 14개가 맞았고, 정답은 모두 121개다. 재현율은?', 'o': ['약 82%', '약 12%', '약 14%'], 'a': 1,
             'why': '재현율 = 맞게 찾은 수 ÷ 정답 전체 = 14 ÷ 121 ≈ 11.6%. 정밀도(14 ÷ 17 ≈ 82%)와 헷갈리기 쉽습니다.', 'hint': '분모가 "정답 전체"입니다.'},
            {'q': '"안 재밌어요"가 LIKE \'%재밌%\'에 걸리는 이유는?', 'o': ['LIKE는 부정어를 이해한다', 'LIKE는 글자 모양만 보기 때문', '데이터가 잘못되어서'], 'a': 1,
             'why': '"재밌"이라는 글자가 들어 있으니 걸립니다. 앞의 "안"이 뜻을 뒤집는다는 것은 모릅니다.', 'hint': 'LIKE가 보는 것은 뜻일까요, 글자일까요?'}],
    'q13': [{'q': '첫 주 글로 만든 태그 규칙이 둘째 주에 흔들린 가장 큰 이유는?', 'o': ['글이 너무 많아서', '처음 보는 이야기와 새 말투가 들어와서', '날짜가 바뀌어서'], 'a': 1,
             'why': '규칙은 사람이 미리 생각한 낱말만 잡습니다. 결제 오류 이야기와 DM 광고는 규칙에 없었습니다.', 'hint': '9일째부터 무엇이 늘었나요?'},
            {'q': '동의어 사전 LIKE의 F1이 꽤 높은데도 한계로 꼽히는 것은?', 'o': ['계산이 느리다', '사람이 계속 만들고 고쳐야 한다', '정밀도가 0이다'], 'a': 1,
             'why': '잘 만든 사전은 정확하지만, 말이 바뀔 때마다 사람이 손봐야 합니다.', 'hint': '버튼을 누르는 일이 현장에서는 누구의 시간인가요?'}],
    'q14': [{'q': '"꿀잼"과 "시간 가는 줄 몰랐다"처럼 글자는 안 겹치는데 뜻이 같은 경우는 어떤 특징인가?', 'o': ['다의어', '같은 뜻 다른 표현', '단위 없음'], 'a': 1,
             'why': '같은 뜻을 다른 모양으로 말하는 경우입니다. 글자 일치 검색이 가장 크게 놓치는 자리입니다.', 'hint': '모양이 다르고 뜻이 같습니다.'},
            {'q': '"배우가 아깝다"가 "돈 아깝다" 검색에 섞여 들어오는 문제는?', 'o': ['다의어(같은 모양, 다른 뜻)', '잡음', '신조어'], 'a': 0,
             'why': '"아깝다"라는 같은 모양이 다른 뜻(배우 칭찬 + 영화 아쉬움)으로 쓰였습니다.', 'hint': '모양이 같고 뜻이 다릅니다.'}],
}

JS = r'''
var D=VL.load(),RV=D.reviews,MV=D.movies;
var CORE={g:'#13733a',b:'#1e55c8',r:'#c9302c',a:'#a35c00',m:'#9b3fb5',gray:'#8a96a3'};
/* 1-1 SQL 실습실 */
(function(){var cv=$('#cv11'),mode='avg',sel=$('#mv11');sel.innerHTML='<option value="0">전체 영화</option>'+MV.map(function(m){return '<option value="'+m.id+'">'+m.title+' ('+m.genre+')</option>'}).join('');
  function rows(){var mv=+sel.value,ms=+$('#st11').value;return RV.filter(function(r){return (!mv||r.movie===mv)&&r.stars>=ms});}
  function sql(){var mv=+sel.value,ms=+$('#st11').value,w=[];if(mv)w.push('m.title = <span class="s">\''+VL.movie(mv).title+'\'</span>');if(ms>1)w.push('r.stars &gt;= '+ms);var wh=w.length?'\n<span class="k">WHERE</span> '+w.join(' <span class="k">AND</span> '):'';
    if(mode==='avg')return '<span class="k">SELECT</span> m.title, <span class="k">AVG</span>(r.stars), <span class="k">COUNT</span>(*)\n<span class="k">FROM</span> review r <span class="k">JOIN</span> movie m <span class="k">ON</span> r.movie_id = m.id'+wh+'\n<span class="k">GROUP BY</span> m.title;';
    if(mode==='dist')return '<span class="k">SELECT</span> r.stars, <span class="k">COUNT</span>(*)\n<span class="k">FROM</span> review r <span class="k">JOIN</span> movie m <span class="k">ON</span> r.movie_id = m.id'+wh+'\n<span class="k">GROUP BY</span> r.stars;';
    return '<span class="k">SELECT</span> m.title, r.stars, r.text\n<span class="k">FROM</span> review r <span class="k">JOIN</span> movie m <span class="k">ON</span> r.movie_id = m.id'+wh+'\n<span class="k">ORDER BY</span> r.date <span class="k">DESC LIMIT</span> 8;';}
  function draw(){var rs=rows(),f=fit(cv),g=f.c;$('#sql11').innerHTML=sql();$('#stv11').textContent=$('#st11').value+'점 이상';
    var items;if(mode==='dist'){items=[1,2,3,4,5].map(function(s){return [s+'점',rs.filter(function(r){return r.stars===s}).length]});}
    else{items=MV.filter(function(m){return !+sel.value||m.id===+sel.value}).map(function(m){var a=rs.filter(function(r){return r.movie===m.id});return [m.title,a.length?a.reduce(function(s,r){return s+r.stars},0)/a.length:0,a.length]});}
    var mx=mode==='dist'?Math.max.apply(null,items.map(function(x){return x[1]}).concat([1])):5;var A=VL.axes(g,f.W,f.H,{xmin:0,xmax:items.length,ymin:0,ymax:mx,noTicks:true,padB:44,ylab:mode==='dist'?'리뷰 수':'평균 별점'});
    var bw=(f.W-A.L-A.R)/items.length;items.forEach(function(it,i){var x=A.L+i*bw+bw*.15,y=A.sy(it[1]);g.fillStyle=mode==='dist'?CORE.b:CORE.g;g.fillRect(x,y,bw*.7,A.sy(0)-y);g.fillStyle='#16212b';g.font='12px "IBM Plex Sans KR",sans-serif';g.textAlign='center';
      g.fillText(mode==='dist'?it[1]:it[1].toFixed(2),x+bw*.35,y-4);g.save();g.translate(x+bw*.35,A.sy(0)+14);g.fillText(it[0].length>6?it[0].slice(0,6)+'…':it[0],0,0);g.restore();});g.textAlign='left';
    stamp(g,f.W,'가상 데이터 · 표로 집계');
    if(mode==='rows'){$('#rs11').innerHTML=rs.slice().sort(function(a,b){return a.date<b.date?1:-1}).slice(0,8).map(function(r){return '<li class="nt"><small>'+r.title+' · '+VL.stars(r.stars)+' · '+r.date+'</small>'+VL.esc(r.text)+'</li>'}).join('');}else $('#rs11').innerHTML='';
    var av=rs.length?rs.reduce(function(s,r){return s+r.stars},0)/rs.length:0;
    VL.kpis($('#k11'),[[rs.length+'개','조건에 맞는 리뷰','g'],[av.toFixed(2)+'점','평균 별점','i'],['언제나 같은 답','같은 SQL을 다시 실행해도','m'],['문장 열','SQL이 뜻을 못 보는 열','r']]);
    $('#in11').innerHTML='<p class="g">별점 조건과 묶기(GROUP BY)는 숫자 그대로라 틀릴 일이 없습니다.</p><p class="m">이제 마케팅팀의 질문 "재밌다는 리뷰만"을 SQL로 바꿔 보세요. 어느 열에 무슨 조건을 걸어야 할까요? 다음 단계에서 해 봅니다.</p>';}
  sel.addEventListener('change',draw);$('#st11').addEventListener('input',draw);
  $$('#p11 [data-g]').forEach(function(bt){bt.addEventListener('click',function(){mode=bt.dataset.g;$$('#p11 [data-g]').forEach(function(x){x.setAttribute('aria-pressed',x===bt?'true':'false')});draw();});});
  Loop.add(cv,function(dt){if(dt===0)draw();});
})();
/* 1-2 LIKE 검색기 */
(function(){var Q=D.searchq,sel=$('#q12'),miss=false;sel.innerHTML=Q.map(function(q,i){return '<option value="'+i+'">'+q.q+' ('+D.aspect_ko[q.asp[0]]+(q.asp[1]>0?' 좋다':' 나쁘다')+')</option>'}).join('');
  function chips(){var q=Q[+sel.value];$('#ch12').innerHTML=q.dict.map(function(w){return '<button class="bt" data-w="'+w+'">'+w+'</button>'}).join('');$$('#ch12 [data-w]').forEach(function(b){b.addEventListener('click',function(){$('#w12').value=b.dataset.w;run();})});}
  function run(){var q=Q[+sel.value],w=$('#w12').value.trim();var found=w?VL.like(RV,w):[];var m=VL.prf(found,RV,q.asp);
    $('#sql12').innerHTML='<span class="k">SELECT</span> text <span class="k">FROM</span> review <span class="k">WHERE</span> text <span class="k">LIKE</span> <span class="s">\'%'+VL.esc(w)+'%\'</span>;';
    VL.kpis($('#k12'),[[found.length+'개','찾은 리뷰','i'],[m.tp+'개','그중 진짜 정답','g'],[VL.pct(m.p),'정밀도 (헛걸음이 적은가)','m'],[VL.pct(m.r),'재현율 (정답 '+m.all+'개 중 몇 %)','r']]);
    var list=miss?RV.filter(function(r){return VL.rel(r,q.asp)&&found.indexOf(r)<0}).slice(0,10):found.slice(0,12);
    $('#rs12').innerHTML=list.map(function(r){var ok=VL.rel(r,q.asp),neg=VL.embed(r.text).hits.filter(function(h){return h.flip&&r.text.slice(h.s,h.e).indexOf(w)>=0}).length;
      var html=miss?VL.esc(r.text):VL.markWord(r.text,[w]);if(neg&&!miss)html=VL.mark(r.text,VL.embed(r.text).hits.filter(function(h){return h.flip}));
      return '<li class="'+(ok?'ok':'no')+'"><small>'+r.title+' · '+VL.stars(r.stars)+' · '+(miss?'놓친 정답':(ok?'정답':'정답 아님'))+'</small>'+html+'</li>'}).join('')||'<li class="nt">결과가 없습니다.</li>';
    $('#in12').innerHTML=miss?'<p class="r">LIKE \''+VL.esc(w)+'\'로는 나오지 않은 정답 리뷰입니다. 같은 뜻을 다른 말투로 썼습니다.</p>':
      '<p class="'+(m.r<.5?'r':'g')+'">정밀도 '+VL.pct(m.p)+'에 재현율 '+VL.pct(m.r)+'. '+(m.r<.5?'찾은 것은 그럴듯해도 정답의 대부분을 놓쳤습니다. "놓친 리뷰 보기"를 눌러 보세요.':'이 낱말은 꽤 많이 잡습니다. 그래도 정답 아닌 것(빨간 테두리)이 섞였는지 확인하세요.')+'</p><p class="m">빨간 물결 밑줄은 앞뒤의 부정어 때문에 뜻이 뒤집힌 낱말입니다.</p>';}
  sel.addEventListener('change',function(){$('#w12').value=Q[+sel.value].like;chips();run();});$('#w12').addEventListener('input',run);
  $('#miss12').addEventListener('click',function(){miss=!miss;this.setAttribute('aria-pressed',miss?'true':'false');run();});chips();run();
})();
/* 1-3 태그 규칙 설계기 */
(function(){var cv=$('#cv13'),S=D.sns,addIssue=false,addDM=false;
  var BASE=[['영화',['#','봤','영화','연기','재밌','꿀잼','무서','감동','OST','스토리','반전','눈물','지루']],['음식',['마라탕','김치찌개','치킨','떡볶이','라떼','카페','맛집','배고','점심','저녁']],
    ['날씨',['비 와','하늘','미세먼지','추워','패딩','눈 온','첫눈','햇살','산책']],['일',['출근','퇴근','야근','회의','발표','팀장','회사']],['광고',['무료','공짜','이벤트','쿠폰','부업','링크','증정','팔로우','관람권','기프티콘']]];
  var TRUE={movie:'영화',food:'음식',weather:'날씨',work:'일',promo:'광고',issue:'결제 오류'};
  function rules(){var r=BASE.map(function(x){return [x[0],x[1].slice()]});if(addDM){r.splice(0,0,['광고',['DM']]);}if(addIssue)r.push(['결제 오류',['결제','오류','LP-']]);return r;}
  function tag(t,rl){for(var i=0;i<rl.length;i++)for(var j=0;j<rl[i][1].length;j++)if(t.indexOf(rl[i][1][j])>=0)return rl[i][0];return null;}
  function draw(){var day=+$('#d13').value,rl=rules(),f=fit(cv),g=f.c;$('#dv13').textContent=day<=7?'1~'+day+'일':'1~'+day+'일 (둘째 주 포함)';
    var per=[];for(var d=1;d<=14;d++){var a=S.filter(function(s){return s.day===d}),c={ok:0,bad:0,none:0};a.forEach(function(s){var t=tag(s.text,rl);if(!t)c.none++;else if(t===TRUE[s.topic])c.ok++;else c.bad++;});per.push(c);}
    var mx=Math.max.apply(null,per.map(function(c){return c.ok+c.bad+c.none}));var A=VL.axes(g,f.W,f.H,{xmin:.5,xmax:14.5,ymin:0,ymax:mx+1,xlab:'날짜 (일째)',ylab:'글 수',xt:14});
    var bw=(A.sx(1)-A.sx(0))*.7;per.forEach(function(c,i){var x=A.sx(i+1)-bw/2,y0=A.sy(0);var al=i+1<=day?1:.22;[['ok',CORE.g],['bad',CORE.a],['none',CORE.r]].forEach(function(k){var h=A.sy(0)-A.sy(c[k[0]]);g.globalAlpha=al;g.fillStyle=k[1];g.fillRect(x,y0-h,bw,h);y0-=h;});g.globalAlpha=1;});
    g.strokeStyle='#16212b';g.setLineDash([4,4]);g.beginPath();g.moveTo(A.sx(7.5),A.T);g.lineTo(A.sx(7.5),A.sy(0));g.stroke();g.setLineDash([]);g.fillStyle='#16212b';g.font='12px "IBM Plex Sans KR",sans-serif';g.fillText('← 규칙을 만든 첫 주 | 둘째 주 →',A.sx(7.5)-92,A.T+12);
    stamp(g,f.W,'가상 SNS 글 '+S.length+'개');
    VL.legend($('#lg13'),[['맞게 분류',CORE.g],['잘못 분류',CORE.a],['미분류',CORE.r]]);
    function rate(lo,hi){var a=S.filter(function(s){return s.day>=lo&&s.day<=hi}),ok=a.filter(function(s){return tag(s.text,rl)===TRUE[s.topic]}).length;return a.length?ok/a.length:0;}
    var w1=rate(1,7),w2=rate(8,Math.max(8,day));VL.kpis($('#k13'),[[VL.pct(w1),'첫 주 맞게 분류','g'],[day>=8?VL.pct(w2):'—','둘째 주 맞게 분류 (8일~)','r'],[rl.length+'개','태그 수','i'],[rl.reduce(function(s,x){return s+x[1].length},0)+'개','사람이 적은 낱말','m']]);
    var bad=S.filter(function(s){return s.day<=day&&tag(s.text,rl)!==TRUE[s.topic]}).slice(-6);
    $('#rs13').innerHTML=bad.map(function(s){var t=tag(s.text,rl);return '<li class="no"><small>'+s.day+'일째 · 실제 주제: '+TRUE[s.topic]+' · 규칙: '+(t||'미분류')+'</small>'+VL.esc(s.text)+'</li>'}).join('');
    $('#in13').innerHTML=day<8?'<p class="g">첫 주는 규칙을 만든 기간이라 대부분 맞습니다. 날짜를 8일 이후로 넘겨 보세요.</p>':
      '<p class="'+(w2<.85?'r':'g')+'">둘째 주 맞게 분류 '+VL.pct(w2)+'. '+(addIssue&&addDM?'규칙을 고치니 회복했습니다. 그 고침은 사람이 문제를 발견한 뒤에야 가능했습니다.':'처음 보는 "결제 오류" 글은 미분류로, "DM" 광고는 다른 태그로 들어갑니다. 위 버튼으로 규칙을 고쳐 보세요.')+'</p>';}
  $('#d13').addEventListener('input',draw);
  $('#add13').addEventListener('click',function(){addIssue=!addIssue;this.setAttribute('aria-pressed',addIssue?'true':'false');draw();});
  $('#dm13').addEventListener('click',function(){addDM=!addDM;this.setAttribute('aria-pressed',addDM?'true':'false');draw();});
  Loop.add(cv,function(dt){if(dt===0)draw();});
})();
/* 1-4 자연어 특징 카드 */
(function(){var C=[
  ['① 정해진 자리가 없다 (비정형)','별점 4점','어제 퇴근하고 봤어요. 각본이 훌륭하다 한 번은 볼 만함','다름','별점은 자리 하나에 숫자 하나. 문장은 무엇이 몇 개 들어올지 정해져 있지 않아 표의 항목으로 바로 옮길 수 없습니다.'],
  ['② 뜻은 맥락이 정한다','진짜 무서워요 소름 돋았다','노래 듣고 소름','다름','같은 "소름"이 공포 영화에서는 무섭다는 뜻, 음악 이야기에서는 감동이라는 뜻입니다.'],
  ['③ 시대·유행에 따라 바뀐다','재밌어요','핵노잼','반대','줄임말·신조어는 해마다 늘어납니다. 첫 주에 만든 규칙이 둘째 주에 흔들린 이유입니다.'],
  ['④ 길이·단위가 없다','꿀잼','주말에 친구랑 봤는데 한순간도 눈을 못 뗐다 그리고 영상미가 예술 강추!!','비슷','글에는 길이의 기준이 없습니다. 긴 글은 낱말이 많아 낱말 수를 세는 방법에서 유리해집니다(2장 대결).'],
  ['⑤ 어순·조사·부정어','재밌어요','안 재밌어요','반대','글자는 거의 같은데 "안" 하나가 뜻을 뒤집습니다. LIKE \'%재밌%\'은 둘 다 데려옵니다.'],
  ['⑥ 사전에 없는 말','LP-204 오류가 떠요','LP-503 오류가 떠요','다름','오류 코드·상품 코드·고유명사는 사전에 없거나 모두 "오류"로만 읽힙니다. 4장에서 다시 봅니다.'],
  ['⑦ 같은 뜻, 다른 표현','꿀잼','시간 가는 줄 몰랐다','같음','글자는 하나도 안 겹치는데 뜻은 같습니다. 글자 일치 검색이 가장 크게 놓치는 자리입니다.'],
  ['⑧ 잡음과 비표준 표현','ㅋㅋㅋㅋ 개웃김','빵 터졌다','같음','ㅋㅋ, 느낌표, 줄임말은 분석 전에 다듬거나, 뜻을 아는 도구로 읽어야 합니다.'],
  ['⑨ 다의어와 비꼼','돈 아깝다','배우가 아깝다','다름','같은 "아깝다"가 다른 뜻입니다. "참 대단한 영화다... 2시간 날렸네" 같은 비꼼은 뜻 점수로도 잘 안 잡힙니다.']];
  var box=$('#cards14');box.innerHTML=C.map(function(c,i){return '<button class="bt" data-i="'+i+'" aria-pressed="'+(i===6)+'">'+c[0].split(' ')[0]+' '+c[0].split(' ').slice(1).join(' ')+'</button>'}).join('');
  function jac(a,b){var A={},B={},i=0,u=0;VL.grams(a).forEach(function(x){A[x]=1});VL.grams(b).forEach(function(x){B[x]=1});for(var k in A){u++;if(B[k])i++;}for(k in B)if(!A[k])u++;return u?i/u:0;}
  function show(i){var c=C[i],j=jac(c[1],c[2]),e1=VL.embed(c[1]),e2=VL.embed(c[2]),cs=VL.cos(e1.v,e2.v);
    $('#view14').innerHTML='<h4 style="margin-top:12px">'+c[0]+'</h4><div class="cols3"><div><h4>문장 A</h4><p>'+VL.mark(c[1],e1.hits)+'</p></div><div><h4>문장 B</h4><p>'+VL.mark(c[2],e2.hits)+'</p></div>'
      +'<div><h4>사람이 보기에 뜻은</h4><p><b>'+c[3]+'</b></p></div></div><div class="vbars"><div class="vb"><span>글자 겹침</span><div class="tr"><div class="fl" style="width:'+Math.round(j*100)+'%;background:#a35c00"></div></div><span class="v">'+j.toFixed(2)+'</span></div>'
      +'<div class="vb"><span>뜻 점수</span><div class="tr"><div class="fl'+(cs<0?' neg':'')+'" style="width:'+Math.round(Math.abs(cs)*100)+'%"></div></div><span class="v">'+cs.toFixed(2)+'</span></div></div><p>'+c[4]+'</p>';
    $$('#cards14 .bt').forEach(function(b){b.setAttribute('aria-pressed',+b.dataset.i===i?'true':'false')});}
  $$('#cards14 .bt').forEach(function(b){b.addEventListener('click',function(){show(+b.dataset.i)})});show(6);
})();
/* 대결 1 */
Duel({el:'#d1',run:function(){var q=D.searchq[0];return {fly:VL.prf(VL.likeAny(RV,q.dict),RV,q.asp).f1,robo:VL.prf(VL.like(RV,q.like),RV,q.asp).f1}},scale:1,fmt:function(v){return v.toFixed(3)},
  report:function(r){var q=D.searchq[0],a=VL.prf(VL.likeAny(RV,q.dict),RV,q.asp),b=VL.prf(VL.like(RV,q.like),RV,q.asp);return '동의어 사전: '+a.n+'개 찾고 '+a.tp+'개 맞음(재현율 '+VL.pct(a.r)+'). LIKE 하나: '+b.n+'개 찾고 '+b.tp+'개 맞음(재현율 '+VL.pct(b.r)+'). F1은 '+a.f1.toFixed(3)+' 대 '+b.f1.toFixed(3)+'이에요.';},
  verdict:{fly:'초파리 승. 말투가 여럿이면 낱말 하나로는 대부분을 놓칩니다. 다만 사전도 사람이 만든 목록이라 "안 재밌어요"를 데려오고, 새 말이 나오면 다시 고쳐야 합니다. 다음 장에서는 목록 대신 뜻 좌표로 찾습니다.',
    robo:'주판봇 승.',draw:'무승부.'}});
'''


def build_page():
    nav = [('#s1', '1-1 표'), ('#s2', '1-2 LIKE'), ('#s3', '1-3 규칙'), ('#s4', '1-4 자연어'), ('#duel', '대결'), ('#sum', '정리')]
    cov = cover('cover_01', '벡터 DB 연구실 · 1장', '표에 담기지 않는 말')
    hr = hero('벡터 DB 연구실 · 1장 · 관계형 DB의 한계와 자연어 데이터의 특징', '표에 담기지 않는 말',
              '영화 별점은 표에 잘 들어가는데, 리뷰 문장의 "뜻"은 왜 표로 찾기 어려울까?',
              '박사가 조수 하루에게 처음으로 인턴 교육을 맡겼습니다. 첫 수업은 하루가 인턴 시아·모아와 함께 영화 리뷰와 SNS 글을 표에 넣어 보는 일. 별점은 SQL 한 줄이면 되는데, "재밌다는 리뷰"는 좀처럼 찾아지지 않습니다.',
              [('%d개' % R['n']['reviews'], '가상 영화 리뷰 (별점 + 문장)', 'g'), ('%s점' % num(R['avg_all'], 2), '전체 평균 별점 — SQL 한 줄', 'i'),
               ('%s' % pct(S0['like']['r']), "LIKE '%재밌%'의 재현율", 'r'), ('9가지', '자연어 데이터의 특징', 'm')],
              [('doc', 'front', '하루, 이번 주부터 인턴 교육을 맡아 줘요. 주제는 벡터 DB. 인턴 둘은 데이터베이스 설계 강좌를 막 끝냈습니다.'),
               ('asst', 'e15', '제, 제가요? …네! 시아, 모아, 잘 부탁해요. 먼저 질문부터 할게요!'),
               ('sia', 'smile', '표랑 SQL은 자신 있어요!'), ('moa', 'report', 'DB 설계 노트도 챙겨 왔어요.')],
              crowd('"하루가 강의를? 손 떨리는 거 보여…" "괜찮을까?" "응원하자!"'))
    return build(P, title='1장 · 표에 담기지 않는 말 — 관계형 DB의 한계와 자연어 데이터의 특징 | 벡터 DB 연구실',
                 desc='영화 별점과 리뷰 문장, SNS 글로 관계형 DB(표·SQL)가 잘하는 일과 못하는 일을 확인하고, 자연어 데이터의 아홉 가지 특징을 실험으로 봅니다.',
                 nav=nav, cover_html=cov, hero=hr,
                 body=body() + footer([('리뷰·SNS 글·영화', '이 연구실이 만든 가상 데이터 (code/make_data.py)'), ('관계형 DB·SQL', '<a href="%s">데이터베이스 설계 강좌</a> (안상선)' % DBD),
                                       ('자연어 데이터의 특징', '<a href="%s">인공지능과 자연어 데이터 분석 강좌</a> 1-1·1-2·3-3·6-1쪽 (안상선)' % NLP),
                                       ('정밀도·재현율', 'Manning, Raghavan, Schütze (2008) Introduction to Information Retrieval, 8장')],
                                      ['모든 영화·리뷰·SNS 글은 가상이며, "재미·감동" 같은 이름표는 이 연구실이 붙였습니다.', '뜻 점수는 사람이 만든 24차원 교육용 임베딩으로 계산했습니다(2장).'],
                                      prev=('index.html', '목차'), nxt=('02_embedding.html', '2장 · 말을 좌표로')),
                 gloss=GLOSS, quizzes=QUIZ, page_js=JS, og='og_01')


if __name__ == '__main__':
    print(build_page())
