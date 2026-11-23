/* Accessible behavior supplements; keep the reference's interaction design. */
const syncHeaderHeight=()=>document.documentElement.style.setProperty('--header-height',document.querySelector('header').getBoundingClientRect().height+'px');
syncHeaderHeight();
if('ResizeObserver' in window)new ResizeObserver(syncHeaderHeight).observe(document.querySelector('header'));

let modalReturnFocus = null;
const focusModal = (id) => {
  const el=document.getElementById(id);
  modalReturnFocus=document.activeElement;
  el.setAttribute('role','dialog');el.setAttribute('aria-modal','true');
  el.setAttribute('aria-labelledby',id==='glossary-modal'?'gm-title':'lb-caption');
  el.querySelector('button').focus();
};
const originalOpenLightbox=openLightbox, originalCloseLightbox=closeLightbox;
openLightbox=function(index){originalOpenLightbox(index);focusModal('lightbox-modal');};
closeLightbox=function(){originalCloseLightbox();modalReturnFocus?.focus({preventScroll:true});};
const originalOpenGlossary=openGlossary,originalCloseGlossary=closeGlossary;
openGlossary=function(key){originalOpenGlossary(key);focusModal('glossary-modal');};
closeGlossary=function(){originalCloseGlossary();modalReturnFocus?.focus({preventScroll:true});};
const originalUpdateLightbox=updateLightbox;
updateLightbox=function(){originalUpdateLightbox();const item=flatLightboxPhotos[currentLightboxIdx];if(!item)return;
 let name=document.getElementById('lb-original-name');
 if(!name){name=document.createElement('p');name.id='lb-original-name';name.className='text-xs text-coco/70 mt-2 text-center';document.getElementById('lb-caption').after(name);}
 name.textContent=item.originalName+' · '+item.primaryCategory;
};
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
