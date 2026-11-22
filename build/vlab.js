/* 벡터 DB 연구실 — 공용 계산·그리기 모듈 (외부 라이브러리 없음, 브라우저와 node 모두에서 동작) */
var VL=(function(){
'use strict';
var D=null,LEX=null,KEYS=null,DIMS=null,NEGPRE=null,NEGPOST=null;
/* ── 준비 ── */
function init(data){
  D=data;LEX=data.lexicon.lex;DIMS=data.lexicon.dims;NEGPRE=data.lexicon.negPre;NEGPOST=data.lexicon.negPost;
  KEYS=Object.keys(LEX).map(function(k){return {k:k,t:'w'}}).concat(NEGPRE.map(function(k){return {k:k,t:'pre'}}),NEGPOST.map(function(k){return {k:k,t:'post'}}));
  KEYS.sort(function(a,b){return b.k.length-a.k.length});
  D.reviews.forEach(function(r){r.vec=embed(r.text).v;r.title=movie(r.movie).title;r.genre=movie(r.movie).genre;});
  D.sns.forEach(function(s){s.vec=embed(s.text).v;});
  return D;
}
function load(){if(D)return D;var el=typeof document!=='undefined'&&document.getElementById('vlab-data');if(!el)return null;return init(JSON.parse(el.textContent));}
function movie(id){for(var i=0;i<D.movies.length;i++)if(D.movies[i].id===id)return D.movies[i];return null;}
/* ── 교육용 임베딩: 사전에서 가장 긴 낱말부터 찾아 더한다 ── */
function tokenize(text){
  var out=[],i=0,n=text.length;
  while(i<n){var hit=null;for(var j=0;j<KEYS.length;j++){var k=KEYS[j].k;if(text.substr(i,k.length)===k){hit=KEYS[j];break;}}
    if(hit){out.push({s:i,e:i+hit.k.length,k:hit.k,t:hit.t});i+=hit.k.length;}else i++;}
  var words=out.filter(function(m){return m.t==='w'});
  out.forEach(function(m){
    if(m.t==='pre'){for(var q=0;q<words.length;q++){if(words[q].s>=m.e&&words[q].s-m.e<=1){words[q].flip=true;break;}}}
    if(m.t==='post'){for(q=words.length-1;q>=0;q--){if(words[q].e<=m.s&&m.s-words[q].e<=1){words[q].flip=true;break;}}}
  });
  return out;
}
function embed(text){
  var v=new Array(DIMS.length).fill(0),toks=tokenize(text),hits=[];
  toks.forEach(function(m){if(m.t!=='w')return;var w=LEX[m.k];w.forEach(function(p){var val=p[1];if(p[0]===0&&m.flip)val=-val;v[p[0]]+=val;});hits.push({k:m.k,flip:!!m.flip,s:m.s,e:m.e});});
  var raw=v.slice(),nr=norm(v);if(nr>0)for(var i=0;i<v.length;i++)v[i]/=nr;
  return {v:v,raw:raw,hits:hits,negs:toks.filter(function(m){return m.t!=='w'}),len:nr};
}
function wordVec(k){var v=new Array(DIMS.length).fill(0);(LEX[k]||[]).forEach(function(p){v[p[0]]+=p[1]});var n=norm(v);return n?v.map(function(x){return x/n}):v;}
function dot(a,b){var s=0;for(var i=0;i<a.length;i++)s+=a[i]*b[i];return s;}
function norm(a){return Math.sqrt(dot(a,a));}
function cos(a,b){var na=norm(a),nb=norm(b);return na&&nb?dot(a,b)/(na*nb):0;}
function euclid(a,b){var s=0;for(var i=0;i<a.length;i++){var t=a[i]-b[i];s+=t*t;}return Math.sqrt(s);}
function topk(items,score,k){return items.map(function(it,i){return {it:it,i:i,s:score(it,i)}}).sort(function(a,b){return b.s-a.s}).slice(0,k);}
/* ── 글자 검색 (SQL LIKE 흉내) ── */
function like(docs,word){return docs.filter(function(d){return d.text.indexOf(word)>=0});}
function likeAny(docs,words){return docs.filter(function(d){return words.some(function(w){return d.text.indexOf(w)>=0})});}
/* ── 정답 조건과 채점 ── */
function rel(doc,asp){return doc.asp&&doc.asp[asp[0]]===asp[1];}
function prf(found,docs,asp){var tp=found.filter(function(d){return rel(d,asp)}).length,all=docs.filter(function(d){return rel(d,asp)}).length;
  var p=found.length?tp/found.length:0,r=all?tp/all:0;return {tp:tp,n:found.length,all:all,p:p,r:r,f1:p+r?2*p*r/(p+r):0};}
/* ── BM25 (글자 두 개씩 끊은 조각으로, 키워드 검색 대표) ── */
function grams(t){var g=[];t.replace(/[.,!?~()\[\]·:]/g,' ').split(/\s+/).forEach(function(w){if(!w)return;if(w.length===1)g.push(w);for(var i=0;i<w.length-1;i++)g.push(w.substr(i,2));});return g;}
function bm25Index(texts){var docs=texts.map(grams),df={},N=docs.length,avg=0;docs.forEach(function(g){avg+=g.length;var seen={};g.forEach(function(x){if(!seen[x]){seen[x]=1;df[x]=(df[x]||0)+1;}})});avg/=N||1;
  return {score:function(q){var qg=grams(q);return docs.map(function(g){var tf={};g.forEach(function(x){tf[x]=(tf[x]||0)+1});var s=0;qg.forEach(function(x){if(!tf[x])return;var idf=Math.log(1+(N-df[x]+.5)/(df[x]+.5));s+=idf*tf[x]*2.2/(tf[x]+1.2*(1-.75+.75*g.length/avg));});return s;});}};}
/* ── 시드 고정 난수 ── */
function rng(seed){var s=seed>>>0||1;return function(){s^=s<<13;s>>>=0;s^=s>>>17;s^=s<<5;s>>>=0;return (s>>>0)/4294967296}}
function gauss(r){var u=r()||1e-9,v=r();return Math.sqrt(-2*Math.log(u))*Math.cos(6.2832*v);}
/* ── 창고 실험용 점 구름 (2차원, 무리 지어 흩어진 점) ── */
function cloud(n,seed,nc){var r=rng(seed||11),C=[],P=[];nc=nc||9;for(var c=0;c<nc;c++)C.push([.1+.8*r(),.1+.8*r(),.03+.06*r()]);
  for(var i=0;i<n;i++){var c2=C[Math.floor(r()*nc)];P.push([Math.min(.99,Math.max(.01,c2[0]+gauss(r)*c2[2])),Math.min(.99,Math.max(.01,c2[1]+gauss(r)*c2[2]))]);}return P;}
function d2(a,b){var s=0;for(var j=0;j<a.length;j++){var t=a[j]-b[j];s+=t*t;}return s;}
function exact(P,q,k){var a=P.map(function(p,i){return [d2(p,q),i]});a.sort(function(x,y){return x[0]-y[0]});return a.slice(0,k).map(function(x){return x[1]});}
/* k-평균 (IVF 서랍 만들기) */
function kmeans(P,k,seed,it){var r=rng(seed||3),C=[];for(var i=0;i<k;i++)C.push(P[Math.floor(r()*P.length)].slice());var lab=new Array(P.length);
  for(var t=0;t<(it||12);t++){for(i=0;i<P.length;i++){var b=0,bd=Infinity;for(var c=0;c<k;c++){var dd=d2(P[i],C[c]);if(dd<bd){bd=dd;b=c;}}lab[i]=b;}
    var S=C.map(function(){return [0,0,0]});for(i=0;i<P.length;i++){S[lab[i]][0]+=P[i][0];S[lab[i]][1]+=P[i][1];S[lab[i]][2]++;}
    for(c=0;c<k;c++)if(S[c][2])C[c]=[S[c][0]/S[c][2],S[c][1]/S[c][2]];}
  var lists=C.map(function(){return []});for(i=0;i<P.length;i++)lists[lab[i]].push(i);return {C:C,lab:lab,lists:lists};}
function ivfSearch(P,ivf,q,k,nprobe){var order=ivf.C.map(function(c,i){return [d2(c,q),i]}).sort(function(a,b){return a[0]-b[0]}).slice(0,nprobe);var cand=[],cmp=ivf.C.length;
  order.forEach(function(o){ivf.lists[o[1]].forEach(function(i){cand.push([d2(P[i],q),i]);cmp++;})});cand.sort(function(a,b){return a[0]-b[0]});
  return {ids:cand.slice(0,k).map(function(x){return x[1]}),cmp:cmp,probed:order.map(function(o){return o[1]})};}
/* 그래프 색인 (HNSW를 줄인 두 층 그래프: 위층은 듬성듬성, 아래층은 촘촘) */
function graph(P,M,seed){var r=rng(seed||5),n=P.length,low=[],top=[],topIds=[];
  /* 2차원 격자로 가까운 점 후보를 빨리 찾는다 */
  var g=Math.max(4,Math.round(Math.sqrt(n/2))),cell={};P.forEach(function(p,i){var k=Math.min(g-1,Math.floor(p[0]*g))+','+Math.min(g-1,Math.floor(p[1]*g));(cell[k]=cell[k]||[]).push(i);});
  function near(i){var p=P[i],cx=Math.min(g-1,Math.floor(p[0]*g)),cy=Math.min(g-1,Math.floor(p[1]*g)),c=[];
    for(var ring=0;ring<g;ring++){for(var x=cx-ring;x<=cx+ring;x++)for(var y=cy-ring;y<=cy+ring;y++){if(Math.max(Math.abs(x-cx),Math.abs(y-cy))!==ring)continue;(cell[x+','+y]||[]).forEach(function(j){if(j!==i)c.push([d2(p,P[j]),j]);});}
      if(c.length>=M+2){c.sort(function(a,b){return a[0]-b[0]});var lim=(ring/g);if(c[M-1][0]<=lim*lim)break;}}
    c.sort(function(a,b){return a[0]-b[0]});return c.slice(0,M-1).map(function(x){return x[1]});}
  for(var i=0;i<n;i++){var nb=near(i);nb.push(Math.floor(r()*n));low.push(nb);if(r()<.04)topIds.push(i);}
  /* 길은 양쪽으로 낸다 (HNSW처럼 양방향 연결, 한 점당 최대 2M개) */
  for(i=0;i<n;i++)low[i].slice(0,M).forEach(function(j){if(j!==i&&low[j].indexOf(i)<0&&low[j].length<2*M)low[j].push(i);});
  topIds.forEach(function(i){var a=topIds.filter(function(j){return j!==i}).map(function(j){return [d2(P[i],P[j]),j]}).sort(function(x,y){return x[0]-y[0]}).slice(0,6).map(function(x){return x[1]});top.push([i,a]);});
  var topMap={};top.forEach(function(t){topMap[t[0]]=t[1]});return {low:low,top:topMap,topIds:topIds,entry:topIds[0]};}
function graphSearch(P,G,q,k,ef){var cmp=0,path=[],cur=G.entry,cd=d2(P[cur],q);cmp++;path.push(cur);
  var moved=true;while(moved){moved=false;(G.top[cur]||[]).forEach(function(j){var dd=d2(P[j],q);cmp++;if(dd<cd){cd=dd;cur=j;moved=true;}});if(moved)path.push(cur);}
  var top=path.slice();
  /* 아래층: 후보 ef개를 들고 이웃을 넓혀 간다 */
  var seen={},cand=[[cd,cur]],res=[[cd,cur]];seen[cur]=1;
  while(cand.length){cand.sort(function(a,b){return a[0]-b[0]});var c=cand.shift();res.sort(function(a,b){return a[0]-b[0]});if(res.length>=ef&&c[0]>res[res.length-1][0])break;
    G.low[c[1]].forEach(function(j){if(seen[j])return;seen[j]=1;var dd=d2(P[j],q);cmp++;if(res.length<ef||dd<res[res.length-1][0]){cand.push([dd,j]);res.push([dd,j]);res.sort(function(a,b){return a[0]-b[0]});if(res.length>ef)res.pop();path.push(j);}});}
  res.sort(function(a,b){return a[0]-b[0]});return {ids:res.slice(0,k).map(function(x){return x[1]}),cmp:cmp,path:path,top:top};}
function recall(a,b){var s={};b.forEach(function(x){s[x]=1});return a.filter(function(x){return s[x]}).length/(b.length||1);}
/* ── 문서 쪼개기 (청킹): 문장 단위로 자르고, 목표 글자 수까지 모은다 ── */
function sentences(t){return t.match(/[^.!?]+[.!?]?/g).map(function(s){return s.trim()}).filter(Boolean);}
function chunk(kb,size,overlap,useOld){var out=[];kb.forEach(function(d){if(d.old&&!useOld)return;var ss=sentences(d.text),cur=[],len=0;
  function push(){if(cur.length)out.push({doc:d.id,title:d.title,date:d.date,old:!!d.old,text:cur.join(' ')});}
  ss.forEach(function(s){if(len&&len+s.length>size){push();cur=overlap?cur.slice(-overlap):[];len=cur.join(' ').length;}cur.push(s);len+=s.length+1;});push();});
  out.forEach(function(c,i){c.id=i;c.vec=embed(c.title+' '+c.text).v;});return out;}
/* ── RAG: 찾고(검색) → 붙이고(프롬프트) → 답하기(여기서는 찾은 문장을 골라 답하는 흉내) ── */
function retrieve(chunks,q,o){o=o||{};var k=o.k||3,alpha=o.alpha==null?1:o.alpha,qv=embed(q).v;
  var bm=bm25Index(chunks.map(function(c){return c.title+' '+c.text})).score(q);
  var sc=chunks.map(function(c,i){var v=Math.max(0,cos(qv,c.vec)),b=bm[i]/(bm[i]+6);return {c:c,vec:v,bm:b,s:alpha*v+(1-alpha)*b};});
  if(o.newest){sc=sc.filter(function(x){return !x.c.old});}
  sc.sort(function(a,b){return b.s-a.s});return sc.slice(0,k);}
function answer(q,hits,thr,gold){thr=thr==null?.35:thr;var ok=hits.filter(function(h){return h.s>=thr});
  if(!ok.length)return {text:'안내 문서에서 근거를 찾지 못했습니다. 답하지 않겠습니다.',src:null,none:true,ctx:false};
  /* 미리 준비한 질문이면: 넘겨받은 자료에 정답 문구가 있을 때만 '자료를 읽고 쓴 답'을 보여 준다 (생성 부분은 흉내) */
  if(gold&&gold.key){var g=ok.filter(function(h){return h.c.text.indexOf(gold.key)>=0})[0];if(g)return {text:gold.ans,src:g.c,none:false,ctx:true};}
  var qv=embed(q).v,qb=grams(q),best=null;
  ok.forEach(function(h){sentences(h.c.text).forEach(function(s){var sb=grams(s),ov=qb.filter(function(x){return sb.indexOf(x)>=0}).length/(qb.length||1);var v=cos(qv,embed(h.c.title+' '+s).v)*.6+ov*.4+h.s*.3;if(!best||v>best.v)best={v:v,s:s,h:h};});});
  return {text:best.s,src:best.h.c,none:false,ctx:false};}
function prompt(q,hits){return '[시스템] 아래 자료에 있는 내용으로만 답하세요. 자료에 없으면 "모릅니다"라고 답하세요.\n'+hits.map(function(h,i){return '[자료 '+(i+1)+' · '+h.c.title+' · '+h.c.date+'] '+h.c.text}).join('\n')+'\n[질문] '+q;}
function ragEval(chunks,o){var res=D.ragq.map(function(x){var h=retrieve(chunks,x.q,o),a=answer(x.q,h,o.thr,x);var right;
    if(!x.doc)right=a.none;else right=a.ctx;
    var hit=x.doc?h.some(function(y){return y.c.doc===x.doc&&y.c.text.indexOf(x.key)>=0}):null;
    var wrong=!right&&!a.none;return {q:x,hits:h,ans:a,right:!!right,hit:hit,wrong:wrong};});
  return {res:res,acc:res.filter(function(r){return r.right}).length/res.length,hall:res.filter(function(r){return r.wrong}).length,
          hit:res.filter(function(r){return r.hit}).length/res.filter(function(r){return r.q.doc}).length,tokens:Math.round(res.reduce(function(s,r){return s+r.hits.reduce(function(t,h){return t+h.c.text.length},0)},0)/res.length)};}
/* ── 아주 작은 언어 모델: 리뷰에서 '다음 말' 세기 (어절 두 개짜리 빈도) ── */
function bigram(){var m={};D.reviews.forEach(function(r){var w=r.text.replace(/[.,!]/g,'').split(/\s+/).filter(Boolean);w.unshift('<시작>');w.push('<끝>');for(var i=0;i<w.length-1;i++){(m[w[i]]=m[w[i]]||{})[w[i+1]]=(m[w[i]][w[i+1]]||0)+1;}});return m;}
/* ── PCA 두 축 (지도 그리기) ── */
function pca2(V){var n=V.length,p=V[0].length,mu=new Array(p).fill(0);V.forEach(function(v){for(var j=0;j<p;j++)mu[j]+=v[j]/n});var X=V.map(function(v){return v.map(function(x,j){return x-mu[j]})});
  function power(defl){var r=rng(9),b=[];for(var j=0;j<p;j++)b.push(r()-.5);for(var it=0;it<80;it++){var nb=new Array(p).fill(0);X.forEach(function(x){var s=dot(x,b);defl.forEach(function(d){s-=dot(x,d)*dot(d,b)});for(var j=0;j<p;j++)nb[j]+=s*x[j];});
      defl.forEach(function(d){var t=dot(nb,d);for(var j=0;j<p;j++)nb[j]-=t*d[j]});var nn=norm(nb)||1;b=nb.map(function(x){return x/nn});}return b;}
  var a=power([]),b=power([a]);return {a:a,b:b,mu:mu,xy:X.map(function(x){return [dot(x,a),dot(x,b)]}),proj:function(v){var x=v.map(function(t,j){return t-mu[j]});return [dot(x,a),dot(x,b)];}};}
/* ── 그리기 ── */
function niceTicks(lo,hi,n){var span=hi-lo,step=Math.pow(10,Math.floor(Math.log10(span/n))),err=span/n/step;if(err>=7.5)step*=10;else if(err>=3.5)step*=5;else if(err>=1.5)step*=2;var t=[],s=Math.ceil(lo/step)*step;for(var v=s;v<=hi+1e-9;v+=step)t.push(+v.toFixed(10));return t;}
function axes(g,W,H,o){var L=o.padL||54,R=o.padR||14,T=o.padT||14,B=o.padB||40;var x0=o.xmin,x1=o.xmax,y0=o.ymin,y1=o.ymax;
  function sx(v){return L+(v-x0)/(x1-x0)*(W-L-R)}function sy(v){return H-B-(v-y0)/(y1-y0)*(H-T-B)}
  g.fillStyle='#fff';g.fillRect(0,0,W,H);g.strokeStyle='#e6ebf1';g.lineWidth=1;g.fillStyle='#5b6874';g.font='12px "IBM Plex Sans KR",sans-serif';
  if(!o.noTicks){niceTicks(x0,x1,o.xt||6).forEach(function(t){var x=sx(t);g.beginPath();g.moveTo(x,T);g.lineTo(x,H-B);g.stroke();g.textAlign='center';g.fillText(o.xfmt?o.xfmt(t):t,x,H-B+16);});
  niceTicks(y0,y1,o.yt||5).forEach(function(t){var y=sy(t);g.beginPath();g.moveTo(L,y);g.lineTo(W-R,y);g.stroke();g.textAlign='right';g.fillText(o.yfmt?o.yfmt(t):t,L-6,y+4);});}
  g.strokeStyle='#9aa6b2';g.beginPath();g.moveTo(L,T);g.lineTo(L,H-B);g.lineTo(W-R,H-B);g.stroke();g.fillStyle='#16212b';g.textAlign='center';if(o.xlab)g.fillText(o.xlab,(L+W-R)/2,H-6);
  if(o.ylab){g.save();g.translate(13,(T+H-B)/2);g.rotate(-Math.PI/2);g.fillText(o.ylab,0,0);g.restore();}g.textAlign='left';return {sx:sx,sy:sy,L:L,R:R,T:T,B:B};}
function dotp(g,x,y,r,c,alpha){g.globalAlpha=alpha==null?.85:alpha;g.fillStyle=c;g.beginPath();g.arc(x,y,r,0,6.2832);g.fill();g.globalAlpha=1;}
function legend(el,items){el.innerHTML=items.map(function(a){return '<span><i style="background:'+a[1]+'"></i>'+a[0]+'</span>'}).join('');}
function fmt(v,d){return (+v).toLocaleString('ko-KR',{minimumFractionDigits:d||0,maximumFractionDigits:d||0});}
function pct(v,d){return (v*100).toFixed(d==null?1:d)+'%';}
function kpis(el,arr){el.innerHTML=arr.map(function(a){return '<div class="kpi '+(a[2]||'')+'"><b>'+a[0]+'</b><span>'+a[1]+'</span></div>';}).join('');}
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]});}
function mark(text,hits,cls){var h=hits.slice().sort(function(a,b){return a.s-b.s}),out='',p=0;h.forEach(function(m){if(m.s<p)return;out+=esc(text.slice(p,m.s))+'<mark class="'+(m.flip?'flip ':'')+(cls||'')+'">'+esc(text.slice(m.s,m.e))+'</mark>';p=m.e;});return out+esc(text.slice(p));}
function markWord(text,words){var out=esc(text);words.forEach(function(w){if(!w)return;out=out.split(esc(w)).join('<mark>'+esc(w)+'</mark>');});return out;}
function stars(n){return '★★★★★'.slice(0,n)+'<span class="muted">'+'☆☆☆☆☆'.slice(0,5-n)+'</span>';}
/* 차원 막대 (임베딩 해부) */
function dimBars(el,v,o){o=o||{};var idx=v.map(function(x,i){return [Math.abs(x),i]}).sort(function(a,b){return b[0]-a[0]}).filter(function(x){return x[0]>1e-6}).slice(0,o.top||8);
  if(!idx.length){el.innerHTML='<p class="small muted">사전에 있는 낱말이 하나도 없어 모든 차원이 0입니다 (영벡터).</p>';return;}
  el.innerHTML=idx.map(function(x){var i=x[1],val=v[i],w=Math.round(Math.abs(val)*100);return '<div class="vb"><span>'+DIMS[i]+'</span><div class="tr"><div class="fl'+(val<0?' neg':'')+'" style="width:'+w+'%"></div></div><span class="v">'+val.toFixed(2)+'</span></div>';}).join('');}
var api={init:init,load:load,movie:movie,tokenize:tokenize,embed:embed,wordVec:wordVec,dot:dot,norm:norm,cos:cos,euclid:euclid,topk:topk,like:like,likeAny:likeAny,rel:rel,prf:prf,
  grams:grams,bm25Index:bm25Index,rng:rng,gauss:gauss,cloud:cloud,d2:d2,exact:exact,kmeans:kmeans,ivfSearch:ivfSearch,graph:graph,graphSearch:graphSearch,recall:recall,
  sentences:sentences,chunk:chunk,retrieve:retrieve,answer:answer,prompt:prompt,ragEval:ragEval,bigram:bigram,pca2:pca2,
  niceTicks:niceTicks,axes:axes,dot2:dotp,legend:legend,fmt:fmt,pct:pct,kpis:kpis,esc:esc,mark:mark,markWord:markWord,stars:stars,dimBars:dimBars,
  get D(){return D},get DIMS(){return DIMS},get LEX(){return LEX}};
return api;
})();
if(typeof module!=='undefined')module.exports=VL;
