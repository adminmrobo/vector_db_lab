

(function(){
'use strict';
var $=function(s,el){return (el||document).querySelector(s)}, $$=function(s,el){return Array.prototype.slice.call((el||document).querySelectorAll(s))};
window.$=$;window.$$=$$;
window.rng=function(seed){var s=seed>>>0||1;return function(){s^=s<<13;s>>>=0;s^=s>>>17;s^=s<<5;s>>>=0;return (s>>>0)/4294967296}};
window.fit=function(cv,h){var dpr=Math.min(window.devicePixelRatio||1,2);var w=cv.clientWidth||cv.parentNode.clientWidth||600;var H=h||cv.getAttribute('data-h')||300;cv.width=Math.round(w*dpr);cv.height=Math.round(H*dpr);cv.style.height=H+'px';var c=cv.getContext('2d');c.setTransform(dpr,0,0,dpr,0,0);return {c:c,W:w,H:+H}};
/* 캐릭터 */
window.Cast={
  src:function(who,mood){var k=who+'_'+mood;var a=(window.SPRITE_ALIAS||{})[k]||k;var s=(window.SPRITE||{})[a];if(!s){var base={doc:'front',asst:'smile',fly:'clip',robo:'smile',sia:'smile',moa:'smile',x1:'hint',x2:'hint',x3:'hint'}[who];a=(window.SPRITE_ALIAS||{})[who+'_'+base];s=(window.SPRITE||{})[a]}return s||''},
  fill:function(){$$('img[data-who][data-mood]').forEach(function(im){if(!im.getAttribute('src'))im.src=Cast.src(im.getAttribute('data-who'),im.getAttribute('data-mood'))})},
  set:function(im,who,mood){if(!im)return;var s=Cast.src(who,mood);im.style.transition='opacity .2s';im.style.opacity=0;setTimeout(function(){im.src=s;im.style.opacity=1},200)}
};
/* 용어 말풍선 */
window.Gloss=function(dict){
  var tip=document.createElement('div');tip.id='tip';tip.setAttribute('role','tooltip');document.body.appendChild(tip);
  var keys=Object.keys(dict).sort(function(a,b){return b.length-a.length});
  var scope=$$('section.level p, section.level li, header.hero p');
  var seenK={};scope.forEach(function(el){var sec=el.closest('section.level,header.hero');var sid=sec?(sec.id||'hero'):'x';
    if(el.closest('.code,.tb,.quiz,.talk,.say,#kg,#export,.duel'))return;
    keys.forEach(function(k){
      if(seenK[sid+'|'+k])return;if(el.getAttribute('data-gl-'+k.length+k.charCodeAt(0)))return;
      var w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT,null);var n;
      while((n=w.nextNode())){if(n.parentNode.closest&&n.parentNode.closest('.jt,a,b.name'))continue;var i=n.nodeValue.indexOf(k);if(i<0)continue;
        var sp=document.createElement('span');sp.className='jt';sp.tabIndex=0;sp.setAttribute('data-k',k);sp.textContent=k;
        var after=n.splitText(i);after.nodeValue=after.nodeValue.slice(k.length);n.parentNode.insertBefore(sp,after);
        el.setAttribute('data-gl-'+k.length+k.charCodeAt(0),'1');seenK[sid+'|'+k]=1;break;}
    });
  });
  function show(e){var t=e.target.closest&&e.target.closest('.jt');if(!t)return;var d=dict[t.getAttribute('data-k')];tip.innerHTML='<b>'+d[0]+'</b><br>'+d[1];tip.style.display='block';var r=t.getBoundingClientRect();var x=Math.min(r.left,window.innerWidth-340);tip.style.left=Math.max(8,x)+'px';tip.style.top=(r.bottom+8)+'px'}
  function hide(){tip.style.display='none'}
  document.addEventListener('mouseover',show);document.addEventListener('focusin',show);
  document.addEventListener('mouseout',function(e){if(e.target.closest&&e.target.closest('.jt'))hide()});
  document.addEventListener('click',function(e){if(e.target.closest&&e.target.closest('.jt'))show(e);else hide()});
  document.addEventListener('keydown',function(e){if(e.key==='Escape')hide()});
  window.addEventListener('scroll',hide,{passive:true});
};
/* 퀴즈 */
window.Quiz=function(data){
  $$('.quiz[data-quiz]').forEach(function(box){
    var list=data[box.getAttribute('data-quiz')]||[];var h='<h4>확인 퀴즈</h4>';
    list.forEach(function(q,qi){h+='<div class="qq"><p>'+(qi+1)+'. '+q.q+'</p><div class="opts">'+q.o.map(function(o,oi){return '<button class="bt" data-q="'+qi+'" data-o="'+oi+'">'+o+'</button>'}).join('')+'</div><p class="fb" aria-live="polite"></p></div>'});
    box.innerHTML=h;
    box.addEventListener('click',function(e){var b=e.target.closest('button[data-q]');if(!b)return;var q=list[+b.getAttribute('data-q')];var qq=b.closest('.qq');$$('button',qq).forEach(function(x){x.classList.remove('right','wrong')});
      var ok=+b.getAttribute('data-o')===q.a;b.classList.add(ok?'right':'wrong');$('.fb',qq).textContent=(ok?'맞아요. ':'다시 생각해 봐요. ')+(ok?q.why:(q.hint||q.why))});
  });
};
/* 대결 */
window.Duel=function(o){
  var el=$(o.el);if(!el)return;
  $$('.guess',el).forEach(function(b){b.addEventListener('click',function(){$$('.guess',el).forEach(function(x){x.setAttribute('aria-pressed','false')});b.setAttribute('aria-pressed','true')})});
  function reset(){$$('.bar .fill',el).forEach(function(f){f.style.width='0'});$$('.bar .v',el).forEach(function(v){v.textContent='?'});$('.verdict',el).classList.remove('on');
    Cast.set($('.side.fly img',el),'fly','point');Cast.set($('.side.robo img',el),'robo','coin');}
  $('.run',el).addEventListener('click',function(){
    var res=o.run();var sc=o.scale||Math.max(Math.abs(res.fly),Math.abs(res.robo))||1;
    $('.bar.f .fill',el).style.width=(Math.max(0,res.fly)/sc*100)+'%';$('.bar.r .fill',el).style.width=(Math.max(0,res.robo)/sc*100)+'%';
    $('.bar.f .v',el).textContent=o.fmt(res.fly);$('.bar.r .v',el).textContent=o.fmt(res.robo);
    var hib=o.higherIsBetter!==false;var d=res.fly-res.robo;var win=Math.abs(d)<=(o.drawMargin||0)?'draw':((d>0)===hib?'fly':'robo');
    var v=$('.verdict',el);v.classList.add('on');
    $('.vreport',v).innerHTML=o.report(res);$('.vtext',v).innerHTML=o.verdict[win];
    var fi=$('.side.fly img',el),ri=$('.side.robo img',el);
    if(win==='fly'){Cast.set(fi,'fly','arms');Cast.set(ri,'robo','sigh')}
    else if(win==='robo'){Cast.set(fi,'fly',Math.abs(d)>=(o.bigGap||0.1)?'cry':'coffee');Cast.set(ri,'robo','happy')}
    else{Cast.set(fi,'fly','coffee');Cast.set(ri,'robo','meh')}
    var g=$('.guess[aria-pressed=true]',el);$('.gtext',v).textContent=g?(g.getAttribute('data-side')===win?'예상이 맞았어요.':'예상과 달랐어요. 왜 그런지 아래 판정을 읽어 보세요.'):'';
  });
  var rb=$('.reset',el);if(rb)rb.addEventListener('click',reset);
};
/* 그리기 박자: 보이는 캔버스만 */
var subs=[];window.Loop={add:function(cv,fn){subs.push({cv:cv,fn:fn,vis:false});return fn}};
var io=('IntersectionObserver' in window)?new IntersectionObserver(function(es){es.forEach(function(e){subs.forEach(function(s){if(s.cv===e.target)s.vis=e.isIntersecting})})},{rootMargin:'80px'}):null;
var last=0;function tick(t){var dt=Math.min(.05,(t-last)/1000||0);last=t;subs.forEach(function(s){if(s.vis&&s.anim!==false)try{s.fn(dt)}catch(err){console.error(err)}});requestAnimationFrame(tick)}
window.LoopStart=function(){subs.forEach(function(s){if(io)io.observe(s.cv);else s.vis=true;try{s.fn(0)}catch(err){console.error(err)}});requestAnimationFrame(tick);
  var rt;window.addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(function(){subs.forEach(function(s){try{s.fn(0,true)}catch(e){}})},150)})};
window.REDUCED=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
/* 진행 막대 */
window.addEventListener('scroll',function(){var h=document.documentElement;var p=h.scrollTop/(h.scrollHeight-h.clientHeight);var b=$('#prog');if(b)b.style.width=(p*100)+'%'},{passive:true});
/* 표지 그림: img/cover_NN.webp가 있으면 대체 표지 대신 보여 준다 (18-15) */
$$('img.cimg[data-cover]').forEach(function(im){var p=im.getAttribute('data-src');if(!p)return;var t=new Image();t.onload=function(){im.src=p;im.hidden=false;var fb=im.parentNode.querySelector('.fallback');if(fb)fb.style.display='none';};t.src=p;});
/* 숨은 식구 */
document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('[data-toggle-hidden]');if(!b)return;var t=$(b.getAttribute('data-toggle-hidden'));if(t){var on=t.classList.toggle('on');b.setAttribute('aria-pressed',on?'true':'false');b.textContent=on?'미공개 식구 숨기기':'미공개 식구 보기 (No.007~009)'}});
})();
