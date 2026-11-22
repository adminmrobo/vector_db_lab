
window.stamp=function(g,W,t){g.save();g.font='12px IBM Plex Sans KR, sans-serif';var w=g.measureText(t).width+14;g.fillStyle='#fdf3e1';g.fillRect(W-w-8,6,w,22);g.strokeStyle='#a35c00';g.strokeRect(W-w-8,6,w,22);g.fillStyle='#a35c00';g.textAlign='left';g.fillText(t,W-w-1,21);g.restore()};
(function(){'use strict';
var box=document.createElement('div');box.id='study';box.setAttribute('aria-live','polite');
box.innerHTML='<span id="st_r">읽은 곳 0%</span><span id="st_q">퀴즈 0/0</span><button class="bt" id="st_g" aria-pressed="true">밑줄: 켜짐</button>';
document.body.appendChild(box);
function upd(){var h=document.documentElement;var p=Math.round(h.scrollTop/Math.max(1,h.scrollHeight-h.clientHeight)*100);document.getElementById('st_r').textContent='읽은 곳 '+p+'%';
 var n=document.querySelectorAll('.quiz .qq').length,ok=document.querySelectorAll('.quiz .bt.right').length;document.getElementById('st_q').textContent='퀴즈 '+ok+'/'+n}
window.addEventListener('scroll',upd,{passive:true});document.addEventListener('click',function(){setTimeout(upd,30)});setTimeout(upd,300);
document.getElementById('st_g').addEventListener('click',function(){var off=document.body.classList.toggle('gl-off');this.setAttribute('aria-pressed',off?'false':'true');this.textContent=off?'밑줄: 꺼짐':'밑줄: 켜짐'});
})();
