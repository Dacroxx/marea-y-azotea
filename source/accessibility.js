/* Accessible behavior supplements; keep the reference's interaction design. */
const syncHeaderHeight=()=>document.documentElement.style.setProperty('--header-height',document.querySelector('header').getBoundingClientRect().height+'px');
syncHeaderHeight();
if('ResizeObserver' in window)new ResizeObserver(syncHeaderHeight).observe(document.querySelector('header'));

// Skip link for keyboard navigation
if(!document.querySelector('.skip-to-content')){
  const skip=document.createElement('a');
  skip.href='#editorial';
  skip.className='skip-to-content no-print';
  skip.textContent='Saltar al contenido';
  document.body.prepend(skip);
}

// Landmark & form control accessibility attributes
const mainNav=document.querySelector('header nav');
if(mainNav&&!mainNav.getAttribute('aria-label'))mainNav.setAttribute('aria-label','Navegación principal');
const glossarySearch=document.getElementById('glossary-search');
if(glossarySearch&&!glossarySearch.getAttribute('aria-label'))glossarySearch.setAttribute('aria-label','Buscar término en el glosario');
document.querySelectorAll('svg').forEach(svg=>{
  if(!svg.getAttribute('aria-label')&&!svg.querySelector('title'))svg.setAttribute('aria-hidden','true');
});
['glossary-modal','lightbox-modal'].forEach(id=>{
  const m=document.getElementById(id);
  if(m){m.setAttribute('role','dialog');m.setAttribute('aria-modal','true');m.setAttribute('aria-labelledby',id==='glossary-modal'?'gm-title':'lb-caption');}
});
const a11yLive=document.createElement('div');
a11yLive.id='a11y-live-status';
a11yLive.setAttribute('aria-live','polite');
a11yLive.setAttribute('aria-atomic','true');
a11yLive.style.cssText='position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap';
document.body.appendChild(a11yLive);
const announceGlossaryCount=()=>{
  const n=document.querySelectorAll('#glossary-grid > button').length;
  a11yLive.textContent=n===1?'Mostrando 1 término en el glosario':`Mostrando ${n} términos en el glosario`;
};
if(glossarySearch)glossarySearch.addEventListener('input',()=>setTimeout(announceGlossaryCount,50));

// Accessible reading progress bar
const progressBar=document.getElementById('reading-progress');
if(progressBar){
  progressBar.setAttribute('role','progressbar');
  progressBar.setAttribute('aria-label','Progreso de lectura');
  progressBar.setAttribute('aria-valuemin','0');
  progressBar.setAttribute('aria-valuemax','100');
  progressBar.setAttribute('aria-valuenow','0');
}

// Body scroll lock for modals
let savedOverflow='';
const lockScroll=()=>{savedOverflow=document.documentElement.style.overflow;document.documentElement.style.overflow='hidden';};
const unlockScroll=()=>{document.documentElement.style.overflow=savedOverflow;};

let modalReturnFocus = null;
const focusModal = (id) => {
  const el=document.getElementById(id);
  modalReturnFocus=document.activeElement;
  lockScroll();
  el.setAttribute('role','dialog');el.setAttribute('aria-modal','true');
  el.setAttribute('aria-labelledby',id==='glossary-modal'?'gm-title':'lb-caption');
  el.querySelector('button').focus();
};
const originalOpenLightbox=openLightbox, originalCloseLightbox=closeLightbox;
openLightbox=function(index){originalOpenLightbox(index);focusModal('lightbox-modal');};
closeLightbox=function(){originalCloseLightbox();unlockScroll();modalReturnFocus?.focus({preventScroll:true});};
const originalOpenGlossary=openGlossary,originalCloseGlossary=closeGlossary;
openGlossary=function(key){originalOpenGlossary(key);focusModal('glossary-modal');};
closeGlossary=function(){originalCloseGlossary();unlockScroll();modalReturnFocus?.focus({preventScroll:true});};
const originalUpdateLightbox=updateLightbox;
updateLightbox=function(){originalUpdateLightbox();const item=flatLightboxPhotos[currentLightboxIdx];if(!item)return;
 let name=document.getElementById('lb-original-name');
 if(!name){name=document.createElement('p');name.id='lb-original-name';name.className='text-xs text-coco/70 mt-2 text-center';document.getElementById('lb-caption').after(name);}
 name.textContent=item.originalName+' · '+item.primaryCategory;
};

// Lightbox touch swipe on mobile
let lbTouchX=null,lbTouchY=null;
const lbModal=document.getElementById('lightbox-modal');
if(lbModal){
  lbModal.addEventListener('touchstart',e=>{if(e.touches.length===1){lbTouchX=e.touches[0].clientX;lbTouchY=e.touches[0].clientY;}},{passive:true});
  lbModal.addEventListener('touchend',e=>{
    if(lbTouchX===null||e.changedTouches.length!==1)return;
    const dx=e.changedTouches[0].clientX-lbTouchX,dy=e.changedTouches[0].clientY-lbTouchY;
    lbTouchX=null;lbTouchY=null;
    if(Math.abs(dx)>48&&Math.abs(dx)>Math.abs(dy)*1.4){if(dx<0)nextLightbox();else prevLightbox();}
  },{passive:true});
}

document.addEventListener('keydown',e=>{
 const modal=['glossary-modal','lightbox-modal'].map(id=>document.getElementById(id)).find(el=>!el.classList.contains('hidden'));
 if(!modal||e.key!=='Tab')return;
 const els=[...modal.querySelectorAll('button,a[href],input')].filter(el=>el.getClientRects().length);
 const first=els[0],last=els.at(-1);
 if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}
 else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}
});
mobileMenuBtn.setAttribute('aria-controls','mobile-menu');mobileMenuBtn.setAttribute('aria-expanded','false');
new MutationObserver(()=>mobileMenuBtn.setAttribute('aria-expanded',String(!mobileMenu.classList.contains('hidden')))).observe(mobileMenu,{attributes:true,attributeFilter:['class']});
document.querySelectorAll('.g-tab').forEach(btn=>btn.setAttribute('aria-pressed',String(btn.dataset.cat===activeGlossaryCat)));
const originalSetGlossaryCategory=setGlossaryCategory;
setGlossaryCategory=function(cat){originalSetGlossaryCategory(cat);document.querySelectorAll('.g-tab').forEach(btn=>btn.setAttribute('aria-pressed',String(btn.dataset.cat===cat)));};
window.addEventListener('beforeprint',()=>{document.querySelectorAll('[id^="mosaic-c"] img').forEach(img=>img.loading='eager');});

// Bulletproof .reveal visibility + active chapter scroll-spy
const spyIds=['cronica-1','cronica-2','cronica-3','cronica-4','cronica-5','glosario'];
const spyLinks=[...document.querySelectorAll('header nav a[href^="#"], #mobile-menu a[href^="#"]')];
let scrollRaf=false;
const syncScrollUI=()=>{
  scrollRaf=false;
  const vh=window.innerHeight||900;
  document.querySelectorAll('.reveal:not(.visible)').forEach(el=>{
    const r=el.getBoundingClientRect();
    if(r.top < vh + 120 && r.bottom > -120) el.classList.add('visible');
    else if(r.bottom <= 0) el.classList.add('visible');
  });
  if(progressBar){
    const docH=document.documentElement.scrollHeight-vh;
    const pct=docH>0?Math.min(100,Math.max(0,Math.round((window.scrollY/docH)*100))):0;
    progressBar.setAttribute('aria-valuenow',String(pct));
  }
  const offset=(parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--header-height'))||68)+48;
  let activeId='';
  for(const id of spyIds){
    const sec=document.getElementById(id);
    if(sec && sec.getBoundingClientRect().top <= offset) activeId=id;
  }
  spyLinks.forEach(a=>{
    const match=a.getAttribute('href')==='#'+activeId;
    a.classList.toggle('is-active',match);
    if(match)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current');
  });
};
const scheduleScrollUI=()=>{if(!scrollRaf){scrollRaf=true;requestAnimationFrame(syncScrollUI);}};
window.addEventListener('scroll',scheduleScrollUI,{passive:true});
window.addEventListener('hashchange',()=>setTimeout(syncScrollUI,60));
window.addEventListener('DOMContentLoaded',()=>setTimeout(syncScrollUI,80));
syncScrollUI();
