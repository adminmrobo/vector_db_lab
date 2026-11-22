# -*- coding: utf-8 -*-
"""마지막 장 · 실전 연습장 — 랩플릭스 운영실 (리뷰 검색 · 고객센터 RAG · SNS 상황실 · 창고 관리)"""
from lib import *

P = 'practice/index.html'


def scene(sid, title, situation, env_html, me_html, links):
    return ('<section class="level scene-sec" id="%s" data-scene="%s"><div class="wrap"><h2>%s</h2>'
            '<div class="note">%s</div>'
            '<div class="grid2"><div class="ctl-env"><h4 style="color:var(--gfp)">운영 환경 (초록)</h4>%s</div><div class="ctl-me"><h4 style="color:var(--info)">내 결정 (파랑)</h4>%s</div></div>'
            '<section class="kpis" id="kp_%s" aria-label="성적표"></section>'
            '<div class="grid2"><div>%s</div><div>%s</div></div>'
            '<div class="chat" id="ch_%s" aria-live="polite"></div>'
            '<h3>미션</h3><div id="ms_%s"></div>'
            '<p class="small">배운 곳 다시 보기: %s</p></div></section>') % (
        sid, sid, title, situation, env_html, me_html, sid,
        canvas('g1_' + sid, 280, title + ' 첫째 그래프'), canvas('g2_' + sid, 280, title + ' 둘째 그래프'), sid, sid, links)


def body():
    b = three([
        ('무엇을', '가상 OTT 「랩플릭스」의 운영실을 직접 맡습니다. 리뷰 검색 창구, 고객센터 RAG 창구, SNS 상황실, 창고(벡터 DB) 관리실 네 곳의 손잡이를 돌려 봅니다.'),
        ('왜 중요한가', '배운 도구는 조건이 바뀌어도 결론이 유지되는지 확인해야 현장에서 씁니다. 함정도 직접 밟아 봐야 기억에 남습니다.'),
        ('어떻게', '초록 조작판은 운영 환경, 파랑 조작판은 내 결정입니다. 성적표와 그래프를 보며 장면마다 미션 세 개를 통과하세요. 기록은 이 탭에만 남고 저장되지 않습니다.')],
        '숫자는 가상 데이터로 계산한 교육용 예시입니다. 실제 서비스 운영·투자 권고가 아닙니다.', title='실전 연습장 — 3줄 안내')
    b += ('<section class="level" style="padding-top:40px"><div class="wrap"><div class="tabs" role="tablist">'
          '<button class="bt" data-tab="search" role="tab" aria-pressed="true">① 리뷰 검색 창구</button>'
          '<button class="bt" data-tab="rag" role="tab" aria-pressed="false">② 고객센터 RAG 창구</button>'
          '<button class="bt" data-tab="sns" role="tab" aria-pressed="false">③ SNS 상황실</button>'
          '<button class="bt" data-tab="store" role="tab" aria-pressed="false">④ 창고 관리실</button></div>'
          '<p class="small muted">주소 끝에 #search, #rag, #sns, #store를 붙이면 그 장면이 바로 열립니다.</p>'
          + say('asst', 'e16', '이번엔 제가 아니라 여러분이 운영자예요. 시아·모아도 옆에서 같이 해 볼 거예요. 막히면 초파리와 주판봇이 한마디씩 거들어요.') + '</div></section>')
    b += scene('search', '① 리뷰 검색 창구 — 마케팅팀의 요청에 답하기',
               '마케팅팀이 매일 다른 요청을 보냅니다. "재밌다는 리뷰", "돈 아깝다는 리뷰"… 검색 방식과 개수, 별점 조건을 골라 정확하고 빠짐없이 모아 주세요.',
               '<div class="group"><span class="glabel">오늘의 요청</span><select class="sel" id="q_s"></select></div><p class="small muted">요청마다 정답 리뷰(이름표)가 정해져 있습니다.</p>',
               '<div class="group"><span class="glabel">검색 방식</span><button class="bt" data-me="like" aria-pressed="false">LIKE 하나</button><button class="bt" data-me="dict" aria-pressed="false">동의어 사전</button><button class="bt" data-me="vec" aria-pressed="true">좌표 검색</button></div>'
               '<div class="group"><span class="glabel">좌표 검색 개수</span><input type="range" id="k_s" min="10" max="150" step="5" value="60" aria-label="개수"><span class="val" id="kv_s"></span></div>'
               '<div class="group"><span class="glabel">별점 조건</span><button class="bt" id="f_s" aria-pressed="false">요청이 긍정이면 3점 이상, 부정이면 3점 이하만</button></div>',
               '<a href="../01_why_not_table.html#s2">1-2 LIKE</a> · <a href="../02_embedding.html#s4">2-4 의미 검색</a> · <a href="../03_vector_store.html#s4">3-4 메타데이터 필터</a>')
    b += scene('rag', '② 고객센터 RAG 창구 — 근거 있는 답만 내보내기',
               '랩플릭스 챗봇이 고객 질문 %d개에 답합니다. 맞게 답하되, 엉뚱한 근거로 지어내면 안 됩니다. LLM에게 넘기는 글이 길수록 비용이 듭니다.' % R['n']['ragq'],
               '<div class="group"><span class="glabel">창고 상태</span><button class="bt" id="old_r" aria-pressed="true">구버전 환불 규정도 남아 있음</button></div>'
               '<div class="group"><span class="glabel">질문 묶음</span><button class="bt" data-qs="all" aria-pressed="true">전체 %d개</button><button class="bt" data-qs="code" aria-pressed="false">오류 코드·결제 질문만</button></div>' % R['n']['ragq'],
               '<div class="group"><span class="glabel">조각 크기</span><input type="range" id="sz_r" min="60" max="300" step="10" value="80" aria-label="조각 크기"><span class="val" id="szv_r"></span></div>'
               '<div class="group"><span class="glabel">k</span><input type="range" id="k_r" min="1" max="5" value="1" aria-label="k"><span class="val" id="kv_r"></span></div>'
               '<div class="group"><span class="glabel">뜻 몫 α</span><input type="range" id="a_r" min="0" max="10" value="10" aria-label="알파"><span class="val" id="av_r"></span></div>'
               '<div class="group"><span class="glabel">근거 문턱</span><input type="range" id="t_r" min="10" max="80" step="5" value="35" aria-label="문턱"><span class="val" id="tv_r"></span></div>'
               '<div class="group"><button class="bt" id="n_r" aria-pressed="false">날짜 필터: 최신 판만</button></div>',
               '<a href="../04_llm_rag.html#s3">4-3 쪼개기</a> · <a href="../04_llm_rag.html#s4">4-4 섞기</a> · <a href="../04_llm_rag.html#s5">4-5 오래된 문서</a> · <a href="../06_attention_3d.html#duel">6장 근거 개수</a>')
    b += scene('sns', '③ SNS 상황실 — 광고는 거르고, 새 이야기는 빨리',
               '14일 동안 SNS 글 %d개가 들어옵니다. 광고 문턱은 첫 주로 정해 둘째 주에 씁니다. 결제 오류 이야기를 빨리 알아채되, 괜한 알림은 줄이세요.' % R['n']['sns'],
               '<div class="group"><span class="glabel">관찰 날짜</span><input type="range" id="d_n" min="8" max="14" value="14" aria-label="날짜"><span class="val" id="dv_n"></span></div>',
               '<div class="group"><span class="glabel">광고 문턱 (좌표)</span><input type="range" id="p_n" min="50" max="99" value="60" aria-label="광고 문턱"><span class="val" id="pv_n"></span></div>'
               '<div class="group"><span class="glabel">같은 이야기로 볼 닮음</span><input type="range" id="g_n" min="40" max="98" value="90" aria-label="닮음 문턱"><span class="val" id="gv_n"></span></div>'
               '<div class="group"><span class="glabel">알림 기준 (새 묶음 글 수)</span><input type="range" id="a_n" min="2" max="8" value="2" aria-label="알림 기준"><span class="val" id="av_n"></span></div>',
               '<a href="../01_why_not_table.html#s3">1-3 규칙의 한계</a> · <a href="../05_cases.html#s2">5-2 SNS 모니터링</a> · <a href="../07_graph_ontology.html#s1">7-1 문턱 정하기</a>')
    b += scene('store', '④ 창고 관리실 — 빠르고 빠짐없이',
               '리뷰 좌표가 계속 늘어 창고가 붐빕니다. 질문 60개를 기준으로, 진짜 가장 가까운 10개를 놓치지 않으면서(재현율) 비교 횟수를 줄이는 색인 설정을 찾으세요.',
               '<div class="group"><span class="glabel">창고의 점 수</span><button class="bt" data-n="2000" aria-pressed="false">2,000개</button><button class="bt" data-n="5000" aria-pressed="true">5,000개</button><button class="bt" data-n="8000" aria-pressed="false">8,000개</button></div>',
               '<div class="group"><span class="glabel">색인</span><button class="bt" data-ix="flat" aria-pressed="true">전수 비교</button><button class="bt" data-ix="ivf" aria-pressed="false">서랍 (IVF 64개)</button><button class="bt" data-ix="hnsw" aria-pressed="false">그래프 (HNSW)</button></div>'
               '<div class="group"><span class="glabel">nprobe (서랍)</span><input type="range" id="np_t" min="1" max="16" value="1" aria-label="nprobe"><span class="val" id="npv_t"></span></div>'
               '<div class="group"><span class="glabel">ef (그래프)</span><input type="range" id="ef_t" min="10" max="80" step="10" value="10" aria-label="ef"><span class="val" id="efv_t"></span></div>',
               '<a href="../03_vector_store.html#s2">3-2 서랍 색인</a> · <a href="../03_vector_store.html#s3">3-3 그래프 색인</a>')
    b += section('close', '마무리 — 네 창구가 함께 묻는 질문',
                 '<p>네 장면은 모두 같은 질문을 던집니다. <b>"무엇으로 채점하는가, 그리고 조건이 바뀌어도 그 점수가 유지되는가."</b> 좌표 검색은 개수를 늘리면 빠짐없이 모으지만 엉뚱한 것도 섞이고, RAG는 문턱을 낮추면 답을 많이 하지만 지어낼 위험이 커지고, '
                 'SNS 알림은 예민하면 시끄럽고 둔하면 늦고, 색인은 빠르면 놓칩니다. 어느 손잡이든 "한쪽을 얻으면 다른 쪽을 내준다"는 맞바꿈이고, 그 균형점은 우리 데이터와 우리 질문으로 재 봐야 찾을 수 있습니다.</p>'
                 + note('모형의 한계: 데이터는 가상이고 작으며, 임베딩은 사람이 만든 24차원 교육용입니다. LLM 답 쓰기는 흉내입니다. 숫자는 교육용 예시이며 실제 서비스 운영·투자 권고가 아닙니다.', True)
                 + crowd('"하루, 첫 인턴 교육 완주!" "다음엔 우리도 가르쳐 줘!" "박수!"', moods=('e01', 'e16', 'e01'))
                 + say('doc', 'judge', '<b>박사의 마지막 정리</b> 표는 사실을, 벡터는 뜻을 맡습니다. 벡터 DB는 마법 상자가 아니라 "가까운 것을 빨리 찾는 창고"이고, 그 창고가 좋은지 나쁜지는 늘 숫자로 확인합니다. 하루, 첫 교육 수고했어요.')
                 + say('asst', 'e01', '감사합니다! 처음엔 떨렸는데, 질문하고 같이 실험하니까 괜찮아졌어요. 시아, 모아, 고마워요!'))
    # 장면 대사에 쓸 표정을 미리 싣는다 (화면에는 보이지 않음)
    b += '<div hidden>' + ''.join(img(w, m) for w, m in [('doc', 'think'), ('doc', 'judge'), ('asst', 'report'), ('fly', 'point'), ('robo', 'coin'), ('robo', 'wow'), ('robo', 'chart'), ('robo', 'happy')]) + '</div>'
    return b


JS = r'''
var D=VL.load(),RV=D.reviews,RQ=D.ragq,S=D.sns;
function charLines(sid,lines){$('#ch_'+sid).innerHTML=lines.map(function(l){var n={doc:'박사',asst:'조수 하루',fly:'초파리 연구원',robo:'주판봇',sia:'인턴1 시아',moa:'인턴2 모아'}[l[0]];
  return '<div class="say" data-who="'+l[0]+'"><img data-who="'+l[0]+'" data-mood="'+l[1]+'" alt="" aria-hidden="true" src="'+Cast.src(l[0],l[1])+'"><div><b class="name">'+n+'</b><p>'+l[2]+'</p></div></div>'}).join('');}
function missions(sid,list,state){$('#ms_'+sid).innerHTML=list.map(function(m,i){var ok=state.done[i];return '<div class="mission'+(ok?' ok':'')+'"><span class="st">'+(ok?'통과':'미션 '+(i+1))+'</span><p>'+m+'</p></div>'}).join('');}
/* 탭 */
(function(){function show(t){$$('.scene-sec').forEach(function(s){s.hidden=s.id!==t});$$('[data-tab]').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.tab===t?'true':'false')});window.dispatchEvent(new Event('resize'));if(SCN[t])SCN[t]();}
  $$('[data-tab]').forEach(function(b){b.addEventListener('click',function(){show(b.dataset.tab);if(history.replaceState)history.replaceState(null,'','#'+b.dataset.tab);})});
  window.SHOWTAB=show;})();
var SCN={};
/* ① 리뷰 검색 */
(function(){var Q=D.searchq,me='vec',filt=false,st={done:[0,0,0],touched:false,good:{}};$('#q_s').innerHTML=Q.map(function(q,i){return '<option value="'+i+'">'+q.q+'</option>'}).join('');
  var M=['"재밌는 영화 리뷰" 요청에서 F1 0.88 이상 만들기 (방식·개수·별점 조건을 조합해 보세요)','함정 관찰: "돈 아까운 영화"를 LIKE 하나로 찾아 "배우가 아깝다" 리뷰가 섞이는 것 확인하기','조건이 바뀌어도: 좌표 검색으로 서로 다른 요청 3개 이상에서 F1 0.85 이상 내기'];
  function found(q){var qv=VL.embed(q.q).v,k=+$('#k_s').value,out;if(me==='like')out=VL.like(RV,q.like);else if(me==='dict')out=VL.likeAny(RV,q.dict);else out=VL.topk(RV,function(r){return VL.cos(qv,r.vec)},k).map(function(x){return x.it});
    if(filt)out=out.filter(function(r){return q.asp[1]>0?r.stars>=3:r.stars<=3});return out;}
  function run(){var qi=+$('#q_s').value,q=Q[qi],f=found(q),m=VL.prf(f,RV,q.asp);$('#kv_s').textContent=$('#k_s').value+'개'+(me==='vec'?'':' (좌표 검색일 때만)');
    VL.kpis($('#kp_search'),[[m.f1.toFixed(3),'F1',m.f1>=.85?'g':'r'],[VL.pct(m.p),'정밀도','i'],[VL.pct(m.r),'재현율 (정답 '+m.all+'개)','m'],[(m.n-m.tp)+'개','엉뚱하게 섞인 리뷰','a']]);
    var g1=fit($('#g1_search')),c=g1.c,A=VL.axes(c,g1.W,g1.H,{xmin:0,xmax:3,ymin:0,ymax:1,noTicks:true,ylab:'점수'});var ms=['like','dict','vec'],lb=['LIKE','사전','좌표'];
    ms.forEach(function(x,i){var keep=me;me=x;var mm=VL.prf(found(q),RV,q.asp);me=keep;var bx=A.L+i*(g1.W-A.L-A.R)/3+10,bw=((g1.W-A.L-A.R)/3-20)/3;[[mm.p,'#1e55c8'],[mm.r,'#9b3fb5'],[mm.f1,'#13733a']].forEach(function(v,j){c.fillStyle=v[1];c.globalAlpha=x===me?1:.35;c.fillRect(bx+j*bw,A.sy(v[0]),bw-3,A.sy(0)-A.sy(v[0]));});c.globalAlpha=1;c.fillStyle='#16212b';c.font='12px sans-serif';c.fillText(lb[i],bx+bw,A.sy(0)+16);});
    c.fillStyle='#5b6874';c.fillText('파랑 정밀도 · 보라 재현율 · 초록 F1',A.L+6,A.T+12);stamp(c,g1.W,'세 방식 비교');
    var g2=fit($('#g2_search')),c2=g2.c,B=VL.axes(c2,g2.W,g2.H,{xmin:10,xmax:150,ymin:0,ymax:1,xlab:'좌표 검색 개수',ylab:'점수'}),qv=VL.embed(q.q).v,sorted=VL.topk(RV,function(r){return VL.cos(qv,r.vec)},150).map(function(x){return x.it});
    [['p','#1e55c8'],['r','#9b3fb5'],['f1','#13733a']].forEach(function(s){c2.strokeStyle=s[1];c2.lineWidth=2;c2.beginPath();for(var k=10;k<=150;k+=5){var ff=sorted.slice(0,k);if(filt)ff=ff.filter(function(r){return q.asp[1]>0?r.stars>=3:r.stars<=3});var v=VL.prf(ff,RV,q.asp)[s[0]];k===10?c2.moveTo(B.sx(k),B.sy(v)):c2.lineTo(B.sx(k),B.sy(v));}c2.stroke();});c2.lineWidth=1;
    c2.strokeStyle='#c9302c';c2.beginPath();c2.moveTo(B.sx(+$('#k_s').value),B.T);c2.lineTo(B.sx(+$('#k_s').value),B.sy(0));c2.stroke();stamp(c2,g2.W,'개수를 늘리면');
    if(st.touched){if(qi===0&&m.f1>=.88)st.done[0]=1;if(me==='like'&&q.id==='waste'&&f.some(function(r){return r.text.indexOf('배우가 아깝')>=0}))st.done[1]=1;if(me==='vec'&&m.f1>=.85){st.good[q.id]=1;if(Object.keys(st.good).length>=3)st.done[2]=1;}}
    missions('search',M,st);
    charLines('search',[['doc',m.f1>=.85?'judge':'think',m.f1>=.85?'F1 '+m.f1.toFixed(2)+'. 이 정도면 마케팅팀에 보내도 됩니다. 정밀도와 재현율이 둘 다 괜찮은지도 확인했죠?':'F1 '+m.f1.toFixed(2)+'. 아직 부족합니다. 놓친 것(재현율)과 섞인 것(정밀도) 중 어느 쪽 문제인가요?'],
      ['asst','report','찾은 '+m.n+'개 중 '+m.tp+'개가 정답, 정답 '+m.all+'개 중 '+VL.pct(m.r,0)+'를 모았어요.'],
      ['fly','point',me==='vec'?'개수를 무작정 늘리면 재현율은 오르지만 정밀도가 떨어져. 오른쪽 그래프에서 초록 선이 가장 높은 곳을 찾아.':'글자로 찾으면 부정어와 다의어에 속아. 빨간 테두리가 몇 개인지 세어 봐.'],
      ['robo','coin',me==='vec'?'개수 150개로 다 긁어 오면 끝 아냐?':'LIKE 하나면 충분하다니까!']]);}
  $$('#search [data-me]').forEach(function(b){b.addEventListener('click',function(){me=b.dataset.me;st.touched=true;$$('#search [data-me]').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});run();})});
  $('#q_s').addEventListener('change',function(){st.touched=true;run()});$('#k_s').addEventListener('input',function(){st.touched=true;run()});$('#f_s').addEventListener('click',function(){filt=!filt;st.touched=true;this.setAttribute('aria-pressed',filt?'true':'false');run();});
  SCN.search=run;window._mis_search=st;
})();
/* ② RAG */
(function(){var old=true,newest=false,qs='all',st={done:[0,0,0],touched:false,seen:{}},cache={};
  var M=['전체 질문에서 15개 이상 맞히고, 엉뚱한 근거 답 0개, 넘긴 글자 평균 350자 이하로 운영하기','함정 관찰: 구버전이 남아 있고 날짜 필터가 꺼진 상태에서 구버전 조각이 근거로 올라오는 것 확인하기','조건이 바뀌어도: 구버전이 있을 때와 없을 때 모두 정답 15개 이상 유지하기 (같은 설정으로)'];
  function ev(){var sz=+$('#sz_r').value,key=sz+'|'+old;if(!cache[key])cache[key]=VL.chunk(D.kb,sz,0,old);var e=VL.ragEval(cache[key],{k:+$('#k_r').value,alpha:+$('#a_r').value/10,thr:+$('#t_r').value/100,newest:newest});
    if(qs==='code'){e.res=e.res.filter(function(r){return /LP-|결제/.test(r.q.q)});}return e;}
  function run(){$('#szv_r').textContent=$('#sz_r').value+'자';$('#kv_r').textContent=$('#k_r').value+'개';$('#av_r').textContent=(+$('#a_r').value/10).toFixed(1);$('#tv_r').textContent=(+$('#t_r').value/100).toFixed(2);
    var e=ev(),right=e.res.filter(function(r){return r.right}).length,hall=e.res.filter(function(r){return r.wrong}).length,tok=Math.round(e.res.reduce(function(s,r){return s+r.hits.filter(function(h){return h.s>=+$('#t_r').value/100}).reduce(function(t,h){return t+h.c.text.length},0)},0)/e.res.length);
    var oldHit=e.res.some(function(r){return r.hits.some(function(h){return h.c.old&&h.s>=+$('#t_r').value/100})});
    VL.kpis($('#kp_rag'),[[right+' / '+e.res.length,'맞힌 질문',right>=e.res.length-1?'g':'r'],[hall+'개','엉뚱한 근거로 답함',hall?'r':'g'],[tok+'자','질문당 넘긴 글자 (비용)',tok<=350?'g':'a'],[oldHit?'있음':'없음','구버전 조각이 근거로 쓰임',oldHit?'r':'g']]);
    var g1=fit($('#g1_rag')),c=g1.c;c.fillStyle='#fff';c.fillRect(0,0,g1.W,g1.H);var n=e.res.length,cols=4,cw=(g1.W-20)/cols,rh=(g1.H-20)/Math.ceil(n/cols);c.font='11px "IBM Plex Sans KR",sans-serif';
    e.res.forEach(function(r,i){var x=10+(i%cols)*cw,y=10+Math.floor(i/cols)*rh;c.fillStyle=r.right?'#e7f5ec':r.wrong?'#fcebea':'#fdf3e1';c.fillRect(x+2,y+2,cw-4,rh-4);c.fillStyle=r.right?'#13733a':r.wrong?'#c9302c':'#a35c00';c.fillText((r.right?'○ ':r.wrong?'✕ ':'△ ')+r.q.q.slice(0,Math.floor(cw/11)-2),x+6,y+rh/2+4);});stamp(c,g1.W,'○ 맞음 · ✕ 지어냄 · △ 모른다고 함');
    var g2=fit($('#g2_rag')),c2=g2.c,B=VL.axes(c2,g2.W,g2.H,{xmin:0,xmax:1,ymin:0,ymax:RQ.length,xlab:'뜻 몫 α',ylab:'맞힌 수'}),keep=$('#a_r').value;c2.strokeStyle='#1e55c8';c2.lineWidth=2;c2.beginPath();
    for(var a=0;a<=10;a++){$('#a_r').value=a;var ee=ev(),rr=ee.res.filter(function(r){return r.right}).length;a?c2.lineTo(B.sx(a/10),B.sy(rr)):c2.moveTo(B.sx(0),B.sy(rr));}c2.stroke();c2.lineWidth=1;$('#a_r').value=keep;VL.dot2(c2,B.sx(keep/10),B.sy(right),6,'#c9302c',1);stamp(c2,g2.W,'α를 바꾸면');
    if(st.touched){if(qs==='all'&&right>=15&&hall===0&&tok<=350)st.done[0]=1;if(old&&!newest&&oldHit)st.done[1]=1;if(qs==='all'&&right>=15){var sig=[$('#sz_r').value,$('#k_r').value,$('#a_r').value,$('#t_r').value,newest].join('|');st.seen[sig]=st.seen[sig]||{};st.seen[sig][old]=1;if(st.seen[sig][true]&&st.seen[sig][false])st.done[2]=1;}}
    missions('rag',M,st);
    charLines('rag',[['doc',hall?'think':'judge',hall?'엉뚱한 근거로 답한 질문이 '+hall+'개 있습니다. 고객에게 틀린 안내가 나가는 것이 "모릅니다"보다 나쁩니다.':'지어낸 답이 없습니다. 이제 비용(넘긴 글자)과 정답 수의 균형을 보세요.'],
      ['asst','report',e.res.length+'개 중 '+right+'개 맞힘, 질문당 '+tok+'자를 넘겼어요.'],
      ['fly','point',oldHit?'구버전 환불 규정이 근거로 올라왔어. 날짜 필터는 켰어?':'오류 코드 질문만 골라서 α를 낮춰 봐. 글자 점수가 왜 필요한지 보일 거야.'],
      ['robo','wow','k를 5로 올리면 다 맞지 않을까? 많이 붙일수록 좋잖아!']]);}
  ['#sz_r','#k_r','#a_r','#t_r'].forEach(function(s){$(s).addEventListener('input',function(){st.touched=true;run()})});
  $('#old_r').addEventListener('click',function(){old=!old;st.touched=true;this.setAttribute('aria-pressed',old?'true':'false');run();});
  $('#n_r').addEventListener('click',function(){newest=!newest;st.touched=true;this.setAttribute('aria-pressed',newest?'true':'false');run();});
  $$('#rag [data-qs]').forEach(function(b){b.addEventListener('click',function(){qs=b.dataset.qs;st.touched=true;$$('#rag [data-qs]').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});run();})});
  SCN.rag=run;window._mis_rag=st;
})();
/* ③ SNS */
(function(){var st={done:[0,0,0],touched:false},REP=[1,2,3].map(function(g){return S.filter(function(s){return s.dup===g})[0]});
  var M=['둘째 주 광고 걸러내기 F1 0.95 이상 만들기','함정 관찰: "같은 이야기로 볼 닮음"을 너무 높여 이야기 묶음이 40개 넘게 쪼개지는 것 확인하기','결제 오류 알림을 11일째 이전에 띄우면서, 14일 동안 결제 오류가 아닌 알림은 1개 이하로 줄이기'];
  var pool=S.filter(function(s){return REP.indexOf(s)<0}).map(function(s){return {s:s,y:s.topic==='promo',c:Math.max.apply(null,REP.map(function(r){return VL.cos(s.vec,r.vec)}))}});
  function groups(th,upto){var G=[];S.filter(function(s){return s.topic!=='promo'&&s.day<=upto}).forEach(function(s){var b=-1,bs=-2;G.forEach(function(g,i){var c=VL.cos(s.vec,g.c);if(c>bs){bs=c;b=i}});
      if(b<0||bs<th){G.push({c:s.vec.slice(),n:1,born:s.day,items:[s],days:{}});G[G.length-1].days[s.day]=1;}else{var g=G[b];g.items.push(s);g.n++;g.days[s.day]=(g.days[s.day]||0)+1;g.c=g.c.map(function(x,i){return x+(s.vec[i]-x)/g.n});}});return G;}
  function alertsOf(G,need,upto){var out=[];G.forEach(function(g){if(g.born<3)return;var acc=0;for(var d=g.born;d<=upto;d++){acc+=g.days[d]||0;if(acc>=need){out.push({g:g,day:d,issue:g.items.filter(function(s){return s.issue}).length>g.n/2});break;}}});return out;}
  function run(){var day=+$('#d_n').value,pt=+$('#p_n').value/100,gt=+$('#g_n').value/100,need=+$('#a_n').value;$('#dv_n').textContent=day+'일째까지';$('#pv_n').textContent=pt.toFixed(2);$('#gv_n').textContent=gt.toFixed(2);$('#av_n').textContent=need+'개';
    var w2=pool.filter(function(p){return p.s.day>=8&&p.s.day<=day}),tp=0,fp=0,fn=0;w2.forEach(function(p){var h=p.c>=pt;if(h&&p.y)tp++;else if(h)fp++;else if(p.y)fn++;});var pr=tp/(tp+fp||1),rc=tp/(tp+fn||1),f1=pr+rc?2*pr*rc/(pr+rc):0;
    var G=groups(gt,day),AL=alertsOf(G,need,day),iss=AL.filter(function(a){return a.issue}).sort(function(a,b){return a.day-b.day})[0],noise=AL.filter(function(a){return !a.issue}).length;
    VL.kpis($('#kp_sns'),[[f1.toFixed(3),'둘째 주 광고 F1',f1>=.95?'g':'r'],[iss?iss.day+'일째':'없음','결제 오류 알림',iss&&iss.day<=10?'g':'a'],[noise+'개','결제 오류가 아닌 알림',noise<=1?'g':'r'],[G.length+'개','이야기 묶음 수','i']]);
    var g1=fit($('#g1_sns')),c=g1.c,A=VL.axes(c,g1.W,g1.H,{xmin:.5,xmax:14.5,ymin:0,ymax:16,xlab:'날짜',ylab:'글 수',xt:14}),bw=(A.sx(1)-A.sx(0))*.7;
    for(var d=1;d<=14;d++){var a=S.filter(function(s){return s.day===d}),pf=a.filter(function(s){return REP.indexOf(s)<0&&Math.max.apply(null,REP.map(function(r){return VL.cos(s.vec,r.vec)}))>=pt}).length,x=A.sx(d)-bw/2;
      c.globalAlpha=d<=day?1:.25;c.fillStyle='#d5dbe2';c.fillRect(x,A.sy(a.length),bw,A.sy(0)-A.sy(a.length));c.fillStyle='#a35c00';c.fillRect(x,A.sy(pf),bw,A.sy(0)-A.sy(pf));c.globalAlpha=1;}stamp(c,g1.W,'회색 전체 · 주황 광고로 걸러낸 글');
    var g2=fit($('#g2_sns')),c2=g2.c,B=VL.axes(c2,g2.W,g2.H,{xmin:1,xmax:14,ymin:0,ymax:Math.max(6,Math.max.apply(null,G.map(function(g){return g.n}))),xlab:'날짜',ylab:'묶음 글 수',xt:14});
    G.forEach(function(g){var acc=0,hot=AL.some(function(a){return a.g===g});c2.strokeStyle=hot?(g.items.some(function(s){return s.issue})?'#c9302c':'#a35c00'):'#9aa6b2';c2.globalAlpha=hot?1:.4;c2.lineWidth=hot?2.5:1;c2.beginPath();
      for(var d=g.born;d<=day;d++){acc+=g.days[d]||0;d===g.born?c2.moveTo(B.sx(d),B.sy(acc)):c2.lineTo(B.sx(d),B.sy(acc));}c2.stroke();});c2.globalAlpha=1;c2.lineWidth=1;stamp(c2,g2.W,'빨강 결제 오류 알림 · 주황 다른 알림');
    if(st.touched){if(day===14&&f1>=.95)st.done[0]=1;if(G.length>40)st.done[1]=1;if(day===14&&iss&&iss.day<=10&&noise<=1)st.done[2]=1;}missions('sns',M,st);
    charLines('sns',[['doc',iss&&noise<=1?'judge':'think',iss?(noise<=1?iss.day+'일째에 결제 오류를 알아챘고 괜한 알림도 적습니다. 좋은 균형입니다.':'결제 오류는 잡았지만 다른 알림이 '+noise+'개입니다. 상황실이 알림에 지치지 않게 하세요.'):'아직 결제 오류 알림이 없습니다. 묶음 닮음이나 알림 기준을 조정해 보세요.'],
      ['asst','report','광고 F1 '+f1.toFixed(2)+', 이야기 묶음 '+G.length+'개, 알림 '+AL.length+'개예요.'],
      ['fly','point',G.length>40?'묶음이 너무 잘게 쪼개졌어. 같은 이야기도 따로 놀고 있지.':'알림 기준을 2개로 두면 예민하고, 8개로 두면 늦어. 그 사이 어딘가야.'],
      ['robo','chart','광고 문턱을 0.5까지 내리면 광고는 다 잡히잖아!']]);}
  ['#d_n','#p_n','#g_n','#a_n'].forEach(function(s){$(s).addEventListener('input',function(){st.touched=true;run()})});
  SCN.sns=run;window._mis_sns=st;
})();
/* ④ 창고 */
(function(){var n=5000,ix='flat',st={done:[0,0,0],touched:false,ok:{}},cache={},hist=[];
  var M=['재현율 95% 이상을 지키면서 질문당 비교 300번 이하로 만들기','함정 관찰: 서랍 색인에서 nprobe 1로 재현율이 85% 아래로 떨어지는 것 확인하기','조건이 바뀌어도: 점 수 두 가지 이상에서 재현율 95% 이상 + 비교 400번 이하 유지하기'];
  function get(){if(!cache[n]){var P=VL.cloud(n,11,9);cache[n]={P:P,ivf:VL.kmeans(P,64,3,12),g:VL.graph(P,8,5),Q:VL.cloud(60,77,9)};cache[n].T=cache[n].Q.map(function(q){return VL.exact(P,q,10)});}return cache[n];}
  function run(){var c=get(),np=+$('#np_t').value,ef=+$('#ef_t').value;$('#npv_t').textContent=np+(ix==='ivf'?'':' (서랍일 때만)');$('#efv_t').textContent=ef+(ix==='hnsw'?'':' (그래프일 때만)');var rc=0,cmp=0;
    c.Q.forEach(function(q,i){var r;if(ix==='flat'){rc+=1;cmp+=n;return;}r=ix==='ivf'?VL.ivfSearch(c.P,c.ivf,q,10,np):VL.graphSearch(c.P,c.g,q,10,ef);rc+=VL.recall(r.ids,c.T[i]);cmp+=r.cmp;});rc/=c.Q.length;cmp/=c.Q.length;
    var mem=ix==='hnsw'?'점마다 이웃 8~16개 연결':ix==='ivf'?'서랍 중심 64개':'추가 없음';hist.push([cmp,rc,ix]);if(hist.length>40)hist.shift();
    VL.kpis($('#kp_store'),[[VL.pct(rc),'재현율 (질문 60개 평균)',rc>=.95?'g':'r'],[VL.fmt(cmp)+'번','질문당 비교',cmp<=300?'g':'a'],[(n/cmp).toFixed(1)+'배','전수보다 빠름','i'],[mem,'색인이 더 쓰는 메모리','m']]);
    var g1=fit($('#g1_store')),g=g1.c,A=VL.axes(g,g1.W,g1.H,{xmin:0,xmax:Math.max(1000,n),ymin:.5,ymax:1.02,xlab:'질문당 비교 횟수',ylab:'재현율',yfmt:function(v){return Math.round(v*100)+'%'}});
    g.strokeStyle='#13733a';g.setLineDash([4,4]);g.beginPath();g.moveTo(A.sx(0),A.sy(.95));g.lineTo(A.sx(Math.max(1000,n)),A.sy(.95));g.stroke();g.setLineDash([]);
    hist.forEach(function(h,i){VL.dot2(g,A.sx(h[0]),A.sy(Math.max(.5,h[1])),i===hist.length-1?7:4,{flat:'#5b6874',ivf:'#a35c00',hnsw:'#1e55c8'}[h[2]],i===hist.length-1?1:.5)});stamp(g,g1.W,'회색 전수 · 주황 서랍 · 파랑 그래프');
    var g2=fit($('#g2_store')),cc=g2.c,S2=Math.min(g2.W-20,g2.H-20),ox=(g2.W-S2)/2;cc.fillStyle='#fff';cc.fillRect(0,0,g2.W,g2.H);for(var i=0;i<c.P.length;i+=Math.max(1,Math.floor(c.P.length/3000)))VL.dot2(cc,ox+c.P[i][0]*S2,10+(1-c.P[i][1])*S2,1.3,'#8a96a3',.35);
    c.Q.forEach(function(q){cc.fillStyle='#c9302c';cc.fillRect(ox+q[0]*S2-2,10+(1-q[1])*S2-2,4,4)});stamp(cc,g2.W,'점 '+VL.fmt(n)+'개 · 빨강 = 질문 60개');
    if(st.touched){if(rc>=.95&&cmp<=300)st.done[0]=1;if(ix==='ivf'&&np===1&&rc<.85)st.done[1]=1;if(rc>=.95&&cmp<=400){st.ok[n]=1;if(Object.keys(st.ok).length>=2)st.done[2]=1;}}missions('store',M,st);
    charLines('store',[['doc',rc>=.95&&cmp<=300?'judge':'think',rc>=.95?(cmp<=300?'재현율과 속도를 모두 지켰습니다. 점 수를 바꿔도 유지되는지 확인하세요.':'정확하지만 아직 느립니다. 비교를 더 줄일 방법은?'):'재현율이 95% 아래입니다. 빠르기만 한 검색은 고객이 원하는 리뷰를 놓칩니다.'],
      ['asst','report','질문당 '+VL.fmt(cmp)+'번 비교, 재현율 '+VL.pct(rc)+'예요.'],
      ['fly','point',ix==='flat'?'전수 비교는 늘 정확하지만, 점이 늘면 비교도 그만큼 늘어. 점 수를 8,000개로 바꿔 봐.':'설정 하나가 좋아 보여도 점 수가 바뀌면 달라질 수 있어.'],
      ['robo','happy','nprobe 1, ef 10! 가장 빠른 게 최고지!']]);}
  $$('#store [data-n]').forEach(function(b){b.addEventListener('click',function(){n=+b.dataset.n;st.touched=true;$$('#store [data-n]').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});run();})});
  $$('#store [data-ix]').forEach(function(b){b.addEventListener('click',function(){ix=b.dataset.ix;st.touched=true;$$('#store [data-ix]').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});run();})});
  $('#np_t').addEventListener('input',function(){st.touched=true;run()});$('#ef_t').addEventListener('input',function(){st.touched=true;run()});
  SCN.store=run;window._mis_store=st;
})();
(function(){var h=(location.hash||'#search').slice(1);SHOWTAB(['search','rag','sns','store'].indexOf(h)>=0?h:'search');})();
'''


def build_page():
    nav = [('#search', '① 리뷰 검색'), ('#rag', '② RAG 창구'), ('#sns', '③ SNS 상황실'), ('#store', '④ 창고 관리'), ('#close', '마무리')]
    cov = cover('cover_06', '벡터 DB 연구실 · 마지막 장', '실전 연습장 — 랩플릭스 운영실', band=True, depth=1,
                chars=(('asst', 'e16'), ('sia', 'firm'), ('moa', 'cheer'), ('robo', 'happy')))
    hr = hero('벡터 DB 연구실 · 마지막 장', '실전 연습장 — 랩플릭스 운영실',
              '조건이 바뀌어도, 내가 고른 설정의 점수는 유지될까?',
              '정규 수업을 마친 인턴들이 랩플릭스 운영실에 앉았습니다. 검색 창구, 고객센터 RAG, SNS 상황실, 창고 관리실의 손잡이를 직접 돌립니다.',
              [('4곳', '운영 장면', 'i'), ('12개', '미션 (장면마다 3개)', 'g'), ('%d개' % R['n']['reviews'], '리뷰', 'm'), ('%d개' % R['n']['ragq'], '고객 질문', 'a')],
              [('doc', 'front', '이번엔 여러분이 운영자입니다. 숫자로 판단하세요.'), ('asst', 'e16', '시아, 모아, 이번엔 제가 질문 안 할게요. 직접 해 봐요!')])
    return build(P, title='마지막 장 · 실전 연습장 — 랩플릭스 운영실 | 벡터 DB 연구실',
                 desc='리뷰 검색, 고객센터 RAG, SNS 상황실, 벡터 창고 색인을 시뮬레이터로 운영하며 미션 12개를 통과합니다.',
                 nav=nav, cover_html=cov, hero=hr,
                 body=body() + footer([('데이터', '이 연구실이 만든 가상 데이터'), ('배운 곳', '1~5장')],
                                      ['모든 숫자는 가상 데이터로 계산한 교육용 예시입니다. 실제 서비스 운영·투자 권고가 아닙니다.', 'RAG 답 쓰기는 흉내입니다.'],
                                      prev=('07_graph_ontology.html', '7장 · 좌표와 관계'), nxt=('index.html', '목차로'), depth=1),
                 gloss={'재현율': ['재현율', '찾아야 할 것 중 찾아온 비율.'], '정밀도': ['정밀도', '찾아온 것 중 맞은 비율.'], '문턱': ['문턱', '걸러내거나 알리는 기준값.']},
                 quizzes={}, page_js=JS, depth=1, og='og_06')


if __name__ == '__main__':
    print(build_page())
