# -*- coding: utf-8 -*-
"""목차 · 벡터 DB 연구실"""
from lib import *

P = 'index.html'
SM = R['search_mean']; IVF = {x['nprobe']: x for x in R['ivf']}; D4 = R['duel4']; SP = R['spam']

WORK = {'01_why_not_table.html': '"불만 리뷰만 모아 줘" 같은 요청에 SQL로 어디까지 되고 어디서 막히는지 판단합니다.',
        '02_embedding.html': '고객 문의·리뷰를 뜻이 비슷한 것끼리 찾는 모든 기능의 출발점입니다.',
        '03_vector_store.html': '벡터 DB를 고를 때 용량·속도·재현율·필터를 숫자로 비교합니다.',
        '04_llm_rag.html': '사내 규정 챗봇을 만들 때 조각 크기·검색 방식·날짜 필터를 정합니다.',
        '05_cases.html': '추천·SNS 감시·챗봇 기억에 끼워 쓰고, 도입이 필요한지 판단합니다.',
        '06_attention_3d.html': 'RAG 답이 틀렸을 때 "찾기"와 "읽기" 중 어디서 틀렸는지 나눠 봅니다.',
        '07_graph_ontology.html': '유사도 문턱을 정하고, 여러 걸음 질문과 범주 검색에 그래프·온톨로지를 더할지 판단합니다.',
        'practice/index.html': '조건을 바꿔도 결론이 유지되는지 직접 운영해 보며 확인합니다.'}


def body():
    b = three([
        ('무엇을', '영화 별점은 표(관계형 DB)에 잘 들어가는데 리뷰 문장의 "뜻"은 왜 표로 찾기 어려운지 확인하고, 뜻을 숫자 좌표로 바꿔 저장·검색하는 벡터 DB를 만들어 LLM·RAG까지 잇습니다.'),
        ('왜 중요한가', '회사 데이터의 대부분은 문장·사진처럼 정해진 항목이 없는 데이터입니다. 생성 AI가 회사 문서로 답하게 하려면(RAG) 벡터 DB가 거의 반드시 들어갑니다.'),
        ('업무에서는', '"벡터 DB 도입" 기획서를 읽고 무엇을 저장하고, 무엇을 묻고, 무엇으로 채점할지 물을 수 있게 됩니다.')],
        '코드·수식을 몰라도 됩니다. 모든 장에 직접 움직이는 실험 도구가 여러 개 있고, 수식은 조수 하루가 하나씩 물어봅니다.',
        [('DB', '데이터베이스'), ('SQL', '표에 묻는 질문 언어'), ('LLM', '대형 언어 모델'), ('RAG', '검색 증강 생성'), ('ANN', '근사 최근접 이웃 검색')],
        title='처음 오신 분께 — 이 시리즈를 3줄로')

    b += ('<section class="level" id="cast"><div class="wrap"><h2>연구실 식구와 이야기</h2>'
          '<p>박사가 조수 하루에게 처음으로 인턴 교육을 맡겼습니다. 주제는 벡터 DB. 하루는 긴장한 채 인턴 시아·모아에게 질문을 던지며 수업을 이끌고, 막히면 초파리 연구원과 주판봇이 실험으로 돕고, 단계마다 박사가 정리합니다. '
          '방청석의 미공개 식구 X1~X3는 떨리는 하루를 걱정하며 지켜봅니다. 장이 갈수록 하루가 조금씩 덜 떨게 됩니다.</p>' + cast_cards([
              ('asst', 'e15', '진행자. 첫 인턴 교육이라 긴장했지만, 질문으로 수업을 끌고 갑니다. 수식이 나오면 여러분 대신 묻습니다.'),
              ('sia', 'explain', '인턴1. 순서와 규칙을 좋아합니다. 데이터베이스 설계 강좌를 막 끝냈습니다.'),
              ('moa', 'report', '인턴2. 꼼꼼한 기록 담당. 「DB 설계 노트」로 표로 할 때와 벡터로 할 때를 나란히 보여 줍니다.'),
              ('fly', 'magnify', '의심하는 쪽. 단순한 방법, 검증, 숨은 함정을 고릅니다. 막히면 실험 버튼을 가리킵니다.'),
              ('robo', 'smile', '확신하는 쪽. 크고 빠르고 새로운 것에 겁니다. 악역은 아니고 성급할 뿐입니다.'),
              ('doc', 'board', '상황을 던지고, 단계마다 정리합니다. 판정은 언제나 숫자대로.')]) + '</div></section>')

    b += section('picture', '벡터 DB 인포그래픽의 그림 아홉 개 — 이 시리즈 어디서 다루나',
                 '<p>벡터 DB를 한 장에 정리할 때 흔히 쓰는 아홉 개 그림(정의, 임베딩, 유사도 검색, 색인, 메타데이터 필터, 작업 흐름, 거리 재는 법, 관계형 DB와 비교, RAG)을 이 시리즈가 어디서 다루는지 모았습니다. 본문에서 "○번 그림"이라고 하면 이 표의 번호입니다.</p>'
                 '<div class="tw"><table class="tb"><tr><th>인포그래픽 그림</th><th>이 시리즈</th><th>직접 해 보는 실험</th></tr>'
                 '<tr><td>1. 벡터 DB란 (임베딩을 저장·검색)</td><td>1장 전체, 3-1</td><td>SQL 실습실, 레코드 미리보기</td></tr>'
                 '<tr><td>2. 임베딩 (뜻을 담은 고차원 좌표)</td><td>2-1, 2-2</td><td>낱말 세기 vs 뜻 좌표, 임베딩 해부실</td></tr>'
                 '<tr><td>3. 유사도 검색 (가장 가까운 이웃)</td><td>2-3, 2-4</td><td>화살표 두 개, 의미 검색기</td></tr>'
                 '<tr><td>4. 색인 (HNSW, IVF, 근사 검색)</td><td>3-2, 3-3</td><td>서랍 색인, 길 찾기 그래프</td></tr>'
                 '<tr><td>5. 메타데이터 필터</td><td>3-4, 4-5</td><td>좌표 + 표 조건, 날짜 필터</td></tr>'
                 '<tr><td>6. 작업 흐름 (넣기 → 상위 k개)</td><td>3장, 4-2, 6-1</td><td>RAG 시뮬레이터, 3D 창고 지도와 프롬프트 줄</td></tr>'
                 '<tr><td>7. 거리 재는 법 (코사인·유클리드·내적)</td><td>2-3, 2장 대결</td><td>세 가지 자, 코사인 vs 내적</td></tr>'
                 '<tr><td>8. 벡터 DB vs 관계형 DB</td><td>1장, 3-5, 5-4</td><td>어디에 저장할까, 도입 판단 도우미</td></tr>'
                 '<tr><td>9. RAG</td><td>4장, 5-3, 6장, 7-3</td><td>조각 크기, 하이브리드 검색, 기억 창고, 어텐션 3D, GraphRAG</td></tr>'
                 '<tr><td>(더 나아가) 지식 그래프·온톨로지·코사인 문턱</td><td>7장</td><td>점수 분포, 지식 그래프 3D, 개념 나무로 거르기</td></tr></table></div>')

    b += section('preview', '미리 보기 — 글자로 찾기 vs 뜻으로 찾기',
                 panel('p0', '미리 보기 · 리뷰 %d개에서 찾기' % R['n']['reviews'], '가상 데이터 · 페이지가 직접 계산',
                       '<div class="ctrl"><div class="group"><span class="glabel">찾을 말</span><input type="text" class="wide" id="t0" value="시간 가는 줄 모르는 영화" aria-label="찾을 말"></div></div>'
                       '<div class="chips" id="c0"></div><div class="grid2"><div><h4>글자로 (LIKE, 첫 낱말)</h4><ul class="res" id="a0"></ul></div><div><h4>뜻으로 (좌표 검색)</h4><ul class="res" id="b0"></ul></div></div>'
                       '<div class="insight" id="in0" aria-live="polite"></div>', real=True))

    toc = [('01_why_not_table.html', '1장', '표에 담기지 않는 말 — 관계형 DB의 한계와 자연어 데이터의 특징', ['1-1 별점은 표에 잘 들어간다', '1-2 리뷰를 LIKE로 찾으면', '1-3 항목과 규칙을 늘리면', '1-4 자연어 데이터의 아홉 가지 특징', '대결: LIKE 하나 vs 동의어 사전 (F 승)']),
           ('02_embedding.html', '2장', '말을 좌표로 — 임베딩과 유사도', ['2-1 낱말 세기', '2-2 뜻의 좌표, 임베딩', '2-3 세 가지 자', '2-4 의미 검색', '대결: 코사인 vs 내적 (F 승)']),
           ('03_vector_store.html', '3장', '벡터 창고 — 저장·색인·검색', ['3-1 레코드와 용량', '3-2 서랍 색인 IVF', '3-3 길 찾기 그래프 HNSW', '3-4 메타데이터 필터', '3-5 관계형 DB와 함께', '대결: 전수 비교 vs IVF (R 승)']),
           ('04_llm_rag.html', '4장', '찾아서 답하는 AI — LLM과 RAG', ['4-1 LLM은 다음 말을 잇는다', '4-2 RAG 여섯 걸음', '4-3 쪼개는 크기', '4-4 하이브리드 검색', '4-5 오래된 문서와 근거 확인', '대결: 벡터만 vs 섞기 (F 승)']),
           ('05_cases.html', '5장', '현장 사례 — 추천, 감시, 기억, 도입', ['5-1 영화 추천', '5-2 SNS 모니터링', '5-3 챗봇의 기억', '5-4 도입 판단', '대결: 글자 겹침 vs 좌표 (R 승)']),
           ('06_attention_3d.html', '6장', 'LLM은 찾은 자료를 어떻게 읽나 — 어텐션과 트랜스포머 3D', ['6-1 찾기와 읽기의 경계', '6-2 토큰과 위치', '6-3 어텐션 Q·K·V', '6-4 여러 머리와 층', '6-5 다음 말 고르기', '대결: 근거 2개 vs 5개 (F 승)']),
           ('07_graph_ontology.html', '7장', '좌표와 관계 — 코사인 실전, 지식 그래프, 온톨로지', ['7-1 점수 분포와 문턱', '7-2 지식 그래프 3D', '7-3 GraphRAG', '7-4 온톨로지', '7-5 셋을 함께', '대결: 벡터만 vs GraphRAG (R 승)']),
           ('practice/index.html', '마지막 장', '실전 연습장 — 랩플릭스 운영실', ['① 리뷰 검색 창구', '② 고객센터 RAG 창구', '③ SNS 상황실', '④ 창고 관리실'])]
    b += section('toc', '목차',
                 '<div class="mapbar"><span>표의 한계</span><i>→</i><span>임베딩</span><i>→</i><span>벡터 창고</span><i>→</i><span>LLM과 RAG</span><i>→</i><span>현장 사례</span><i>→</i><span class="on">실전 연습장</span></div>'
                 '<div class="toc">' + ''.join('<a href="%s"><span class="k">%s</span><b>%s</b><ul>%s</ul><span class="small"><b>업무에서는</b> %s</span></a>' % (h, k, t, ''.join('<li>%s</li>' % x for x in li), WORK[h]) for h, k, t, li in toc) + '</div>'
                 + say('sia', 'guide', '1장에서 시작해 차례로 읽기를 권해요. 앞 장의 한계가 다음 장의 이유가 됩니다. 관계형 DB를 이미 잘 안다면 1장은 1-2부터 봐도 괜찮아요.'))

    b += section('record', '대결 전적 — 초파리 연구원 vs 주판봇 (4승 3패)',
                 '<div class="tw"><table class="tb"><tr><th>장</th><th>대결 질문</th><th>판정 기준</th><th>결과</th></tr>'
                 '<tr><td>1장</td><td>LIKE 하나 vs 동의어 사전</td><td>"재밌다는 리뷰" F1</td><td>초파리 승 (%s 대 %s)</td></tr>'
                 '<tr><td>2장</td><td>코사인 vs 길이 그대로 내적</td><td>여덟 가지 뜻 F1 평균</td><td>초파리 승 (%s 대 %s)</td></tr>'
                 '<tr><td>3장</td><td>전수 비교 vs 서랍 색인</td><td>비교 횟수 (재현율 95%% 이상만 인정)</td><td>주판봇 승 (%s번 대 5,000번)</td></tr>'
                 '<tr><td>4장</td><td>벡터만 vs 뜻 + 글자 섞기</td><td>질문 %d개 중 맞힌 수 (k = 1)</td><td>초파리 승 (%d 대 %d)</td></tr>'
                 '<tr><td>5장</td><td>글자 겹침 vs 좌표 닮음</td><td>둘째 주 광고 걸러내기 F1</td><td>주판봇 승 (%s 대 %s)</td></tr>'
                 '<tr><td>6장</td><td>근거 조각 2개 vs 5개</td><td>정답 조각에 머문 어텐션 몫</td><td>초파리 승 (%s 대 %s)</td></tr>'
                 '<tr><td>7장</td><td>벡터만 vs GraphRAG</td><td>여러 걸음 질문 %d개 중 필요한 사실을 모은 수</td><td>주판봇 승 (%d 대 %d)</td></tr></table></div>'
                 '<p>어느 쪽도 늘 이기지 않습니다. 단순한 방법이 이길 때(1·2·4·6장)와 크고 빠르고 새로운 방법이 이길 때(3·5·7장)를 가르는 것은 늘 "무엇으로 채점했나"였습니다.</p>' % (
                     num(R['search'][0]['dict']['f1'], 3), num(R['search'][0]['like']['f1'], 3), num(SM['vec'], 3), num(SM['dotraw'], 3), num(IVF[4]['cmp']),
                     R['n']['ragq'], D4['hyb_right'], D4['vec_right'], num(SP['cos']['f1'], 3), num(SP['jac']['f1'], 3),
                     pct(R['att']['k2']['focus']), pct(R['att']['k5']['focus']), R['graph7']['mq'], R['graph7']['graph']['ok'], R['graph7']['vec2']['ok']))

    b += section('data', '데이터와 원칙',
                 '<div class="tw"><table class="tb"><tr><th>데이터 (모두 가상)</th><th>내용</th></tr>'
                 '<tr><td>영화 8편 · 리뷰 %d개</td><td>별점 1~5점과 리뷰 문장. 리뷰마다 "무엇을 좋다·나쁘다고 했나"(재미·감동·공포·연기 등) 이름표가 있어 검색을 채점합니다. 비꼬는 리뷰 3개 포함</td></tr>'
                 '<tr><td>SNS 글 %d개 (14일)</td><td>영화 이야기·음식·날씨·일상, 말만 바꾼 광고(둘째 주에는 처음 보는 말투 포함), 9일째부터 늘어나는 결제 오류 이야기</td></tr>'
                 '<tr><td>랩플릭스 안내 문서 %d개 · 질문 %d개</td><td>가상 OTT 서비스의 요금제·환불·해지·오류 코드 안내. 환불 규정은 구버전·현행 두 판. 질문 중 2개는 문서에 없는 질문</td></tr>'
                 '<tr><td>교육용 임베딩</td><td>사람이 뜻을 정한 %d개 낱말, 24차원(차원마다 "재미", "감동" 같은 이름). 실제 임베딩 모델(384~1,536차원, 이름 없음)의 원리를 눈으로 보이게 만든 설명용입니다</td></tr></table></div>'
                 '<ul><li>모든 숫자는 페이지가 브라우저에서 직접 계산하고, 같은 계산을 <code>code/analysis.js</code>가 <code>data/results.json</code>에 남깁니다.</li>'
                 '<li>LLM이 문장을 쓰는 부분(4·5장)은 미리 적어 둔 답으로 흉내 냅니다. 찾기·점수·채점은 실제 계산입니다.</li>'
                 '<li>연결 강좌: <a href="%s">데이터베이스 설계</a>(표·SQL·정규화), <a href="%s">인공지능과 자연어 데이터 분석</a>(자연어의 특징·임베딩·LLM).</li></ul>' % (
                     R['n']['reviews'], R['n']['sns'], R['n']['kb'], R['n']['ragq'], R['n']['lex'], DBD, NLP))
    return b


GLOSS = {
    '벡터 DB': ['벡터 데이터베이스', '뜻을 담은 숫자 좌표(벡터)를 저장하고, 가까운 좌표를 빨리 찾는 데이터베이스.'],
    '관계형 DB': ['관계형 데이터베이스', '행과 열의 표에 데이터를 담고 SQL로 묻는 데이터베이스.'],
    '임베딩': ['임베딩', '문장·그림의 뜻을 숫자 좌표로 바꾼 것.'],
    'RAG': ['RAG (검색 증강 생성)', '관련 문서를 찾아 LLM에게 함께 넘겨 그 자료로 답하게 하는 방법.'],
    'LLM': ['대형 언어 모델', '다음 말 맞히기로 학습한 큰 언어 모델.'],
}

JS = r'''
var D=VL.load(),RV=D.reviews;
(function(){var P=['시간 가는 줄 모르는 영화','돈 아까운 영화','소름 돋는 음악','하나도 안 무서운 공포'];$('#c0').innerHTML=P.map(function(p){return '<button class="bt" data-t="'+p+'">'+p+'</button>'}).join('');
  function run(){var t=$('#t0').value.trim(),w=t.split(/\s+/)[0]||'',L=w?VL.like(RV,w.slice(0,Math.max(1,w.length-1))):[],qv=VL.embed(t).v,V=VL.topk(RV,function(r){return VL.cos(qv,r.vec)},5);
    $('#a0').innerHTML='<li class="nt"><small>LIKE \'%'+VL.esc(w.slice(0,Math.max(1,w.length-1)))+'%\' · '+L.length+'개</small></li>'+L.slice(0,4).map(function(r){return '<li class="nt"><small>'+r.title+' · '+VL.stars(r.stars)+'</small>'+VL.esc(r.text)+'</li>'}).join('');
    $('#b0').innerHTML=V.map(function(x){return '<li class="nt"><span class="sc">'+x.s.toFixed(2)+'</span><small>'+x.it.title+' · '+VL.stars(x.it.stars)+'</small>'+VL.esc(x.it.text)+'</li>'}).join('');
    $('#in0').innerHTML='<p class="m">왼쪽은 첫 낱말의 글자가 들어 있는 리뷰, 오른쪽은 문장 전체의 뜻이 가까운 리뷰입니다. 왜 이렇게 다른지, 1장에서 시작합니다.</p>';}
  $$('#c0 .bt').forEach(function(b){b.addEventListener('click',function(){$('#t0').value=b.dataset.t;run();})});$('#t0').addEventListener('input',run);run();
})();
'''


def build_page():
    nav = [('#cast', '식구'), ('#picture', '그림 아홉 개'), ('#preview', '미리 보기'), ('#toc', '목차'), ('#record', '대결 전적'), ('#data', '데이터')]
    cov = cover('cover_00', '벡터 DB 연구실', '표에 담기지 않는 말을 저장하는 법', chars=(('doc', 'front'), ('asst', 'e15'), ('sia', 'smile'), ('moa', 'report'), ('fly', 'point'), ('robo', 'coin')))
    hr = hero('벡터 DB 연구실 · 목차', '벡터 DB 연구실',
              '영화 별점은 표에 넣으면 되는데, 리뷰와 SNS 글의 "뜻"은 어디에 어떻게 저장해야 찾을 수 있을까?',
              '조수 하루의 첫 인턴 교육. 관계형 DB의 한계에서 출발해 임베딩, 벡터 창고, LLM과 RAG, 현장 사례까지 다섯 장, 어텐션 3D와 지식 그래프·온톨로지 특강 두 장, 실전 연습장으로 갑니다.',
              [('7장 + 실전', '장마다 실험 도구 4~5개 (3D 포함)', 'i'), ('%d개' % R['n']['reviews'], '가상 영화 리뷰', 'g'), (num(SM['vec'], 3), '좌표 검색 F1 (LIKE %s)' % num(SM['like'], 3), 'm'), ('4승 3패', '초파리 vs 주판봇 대결 전적', 'a')],
              [('doc', 'front', '하루, 이번 인턴 교육은 하루가 맡아 줘요. 주제는 벡터 DB입니다.'),
               ('asst', 'e15', '제가요?! …네, 해 볼게요. 시아, 모아, 질문 많이 할 테니 잘 부탁해요!'),
               ('sia', 'smile', '데이터베이스 설계 강좌 막 끝냈어요!'), ('moa', 'report', 'DB 설계 노트 챙겨 왔어요.')],
              crowd('"하루가 강의를?" "손 떨리는 거 보여…" "그래도 응원하자!"'))
    return build(P, title='벡터 DB 연구실 — 표에 담기지 않는 말을 저장하는 법 | 목차',
                 desc='관계형 DB의 한계와 자연어 데이터의 특징에서 출발해 임베딩, 벡터 DB 색인, LLM과 RAG, 현장 사례까지 실험으로 배우는 연구실 해설 시리즈.',
                 nav=nav, cover_html=cov, hero=hr,
                 body=body() + footer([('데이터', '이 연구실이 만든 가상 데이터 (code/make_data.py)'), ('연결 강좌', '<a href="%s">데이터베이스 설계</a> · <a href="%s">인공지능과 자연어 데이터 분석</a>' % (DBD, NLP)),
                                       ('저장소', '<a href="%s">%s</a>' % (REPO, REPO))],
                                      ['모든 영화·리뷰·SNS 글·랩플릭스 문서는 가상입니다.', '24차원 교육용 임베딩은 설명용입니다.'], nxt=('01_why_not_table.html', '1장 · 표에 담기지 않는 말')),
                 gloss=GLOSS, quizzes={}, page_js=JS, og='og_00')


if __name__ == '__main__':
    print(build_page())
