document.documentElement.classList.add('js');
var RM=matchMedia('(prefers-reduced-motion:reduce)').matches;
var io=new IntersectionObserver(function(es){es.forEach(function(e){
  if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},
  {rootMargin:'0px 0px -6% 0px',threshold:.1});
document.querySelectorAll('.rv,[data-stg]').forEach(function(el){io.observe(el);});

var shots=document.querySelectorAll('.shot'),th=document.querySelectorAll('.thumb');
function go(i){shots.forEach(function(s,n){s.classList.toggle('on',n===i);});
  th.forEach(function(t,n){t.setAttribute('aria-selected',n===i?'true':'false');});}
th.forEach(function(t){t.addEventListener('click',function(){go(+t.dataset.g);});
  t.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();go(+t.dataset.g);}});});

var ti=document.querySelectorAll('.tier'),ap=document.getElementById('ap'),bp=document.getElementById('bp');
function pick(t){ti.forEach(function(x){x.setAttribute('aria-checked',x===t?'true':'false');});
  var p='$'+Number(t.dataset.p).toFixed(2);ap.textContent=p;bp.textContent=p;}
ti.forEach(function(t){t.addEventListener('click',function(){pick(t);});
  t.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();pick(t);}});});

(function(){var f=function(d){return d.toLocaleDateString('en-US',{month:'short',day:'numeric'});},
  a=new Date(),b=new Date();a.setDate(a.getDate()+6);b.setDate(b.getDate()+12);
  document.getElementById('eta').textContent=f(a)+' – '+f(b);})();

new IntersectionObserver(function(es){
  document.getElementById('bar').classList.toggle('up',!es[0].isIntersecting);
},{threshold:0}).observe(document.getElementById('atc'));

if(!RM){var sio=new IntersectionObserver(function(es){es.forEach(function(e){
  if(!e.isIntersecting)return;sio.unobserve(e.target);
  var el=e.target,to=+el.dataset.to,suf=el.dataset.suf||'',t0=null,D=1500;
  if(to===0){el.textContent='0'+suf;return;}
  requestAnimationFrame(function step(t){if(!t0)t0=t;var p=Math.min((t-t0)/D,1);
    el.textContent=Math.round(to*(1-Math.pow(1-p,3)))+suf;if(p<1)requestAnimationFrame(step);});
});},{threshold:.6});
document.querySelectorAll('.stat b').forEach(function(b){sio.observe(b);});}

/* Shopify: keep the hidden variant input and button price in sync with the tier */
(function(){
  var vid=document.getElementById('variant-id');
  if(!vid) return;
  var ap=document.getElementById('ap');
  function sync(t){
    if(t.dataset.id) vid.value=t.dataset.id;
    if(ap && t.dataset.p) ap.textContent='$'+Number(t.dataset.p).toFixed(2);
    var bp=document.getElementById('bp');
    if(bp && t.dataset.p) bp.textContent='$'+Number(t.dataset.p).toFixed(2);
  }
  var tiers=document.querySelectorAll('.tier');
  tiers.forEach(function(t){
    t.addEventListener('click',function(){sync(t);});
    t.addEventListener('keydown',function(e){
      if(e.key==='Enter'||e.key===' '){e.preventDefault();sync(t);}
    });
  });
  var checked=document.querySelector('.tier[aria-checked="true"]');
  if(checked) sync(checked);
})();
