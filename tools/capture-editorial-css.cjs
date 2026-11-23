/* Browser-only compilation of the reference's Tailwind CDN; never shell-evaluate it.
   No npm install. The committed CSS is sufficient for deterministic offline builds.
   Run after python tools/build_magazine.py --runtime. */
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {pathToFileURL}=require('node:url');
const {chromium}=require(process.env.PLAYWRIGHT_PATH||'C:/Users/D/node_modules/playwright');
const root=path.resolve(__dirname,'..');
(async()=>{const b=await chromium.launch({executablePath:process.env.CHROME_PATH||'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});try{
 const page=await b.newPage({viewport:{width:1440,height:1000}});
 // Styles are compiled with real CDN; images/fonts are irrelevant to compilation.
 await page.route(/https:\/\/(drive\.google|lh3\.googleusercontent|fonts\.)/,r=>r.abort());
 let runtimeHash=null;page.on('response',async r=>{if(r.url().includes('cdn.tailwindcss.com')&&r.status()===200){try{runtimeHash=crypto.createHash('sha256').update(await r.body()).digest('hex')}catch{}}});
 await page.goto(pathToFileURL(path.join(root,'source/build-runtime.html')).href,{waitUntil:'domcontentloaded'});
 await page.waitForFunction(()=>getComputedStyle(document.querySelector('#mosaic-c1')).display==='grid',{timeout:60000});
 await page.evaluate(async()=>{
  for(const cat of ['all',...Object.keys(glossaryCategories)]){setGlossaryCategory(cat);await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));}
  setGlossaryCategory('all');
  for(const key of Object.keys(glossaryEntries)){openGlossary(key);await new Promise(r=>requestAnimationFrame(r));closeGlossary();}
  openLightbox(0);await new Promise(r=>requestAnimationFrame(r));navigateLightbox(1);closeLightbox();
  mobileMenu.classList.remove('hidden');
  // All source literal utility tokens, including untouched reference mosaics/cards,
  // are safelisted in a temporary DOM node. Runtime modifiers compile responsive,
  // hover, group, arbitrary values, opacity variants without needing those states.
  const node=document.createElement('div');node.id='compile-safelist';
  const tokens=new Set();
  for(const el of document.querySelectorAll('[class]'))for(const token of el.classList)tokens.add(token);
  node.className=[...tokens].sort().join(' ');document.body.append(node);
 });
 await page.waitForTimeout(1000);
 const css=await page.locator('style').evaluateAll(els=>els.filter(e=>e.textContent.includes('--tw-border-spacing-x')).map(e=>e.textContent).join('\n'));
 if(css.length<15000||!css.includes('lg\\:grid-cols-4')||!css.includes('bg-selva'))throw Error('Incomplete compilation');
 fs.writeFileSync(path.join(root,'source/tailwind.generated.css'),css+'\n');
 fs.writeFileSync(path.join(root,'source/css-build.json'),JSON.stringify({method:'Browser Tailwind CDN compilation; exercised glossary categories/modal, lightbox, fallback, menu; actual DOM class safelist',runtimeSha256:runtimeHash,cssSha256:crypto.createHash('sha256').update(css+'\n').digest('hex'),bytes:Buffer.byteLength(css+'\n')},null,2)+'\n');
 console.log('Compiled static inline utilities:',css.length,'characters; CDN SHA256',runtimeHash);
}finally{await b.close()}})().catch(e=>{console.error(e);process.exitCode=1});
