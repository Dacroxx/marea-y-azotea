/* Real DOM/CSS/JS with explicitly mocked image transport. No npm install. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {pathToFileURL}=require('node:url');
const {chromium}=require(process.env.PLAYWRIGHT_PATH||'C:/Users/D/node_modules/playwright');
const root=path.resolve(__dirname,'..');
const catalog=JSON.parse(fs.readFileSync(path.join(root,'audit/thematic-catalog.json'),'utf8'));
const verified=catalog.filter(r=>r.mediaType==='photo'&&r.reviewStatus==='verified');
const categories=fs.readFileSync(path.join(root,'audit/TAXONOMY.md'),'utf8').split('\n').filter(l=>/^\d\. /.test(l)).map(l=>l.replace(/^\d\. /,'').split(':')[0]);
const slugs=['territorio','hierbas','mar','fogon','cultura'];
const out=process.env.ARTIFACT_DIR||path.join(process.env.USERPROFILE,'AppData/Local/hermes/profiles/null/cache/scratch/marea-magazine-qa');
fs.mkdirSync(out,{recursive:true});
const tiny=Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aP1sAAAAASUVORK5CYII=','base64');
const report={transport:'mock image fixture (not photographic evidence)',checks:[],viewports:[],errors:[]};
const check=name=>{report.checks.push(name);console.log('PASS:',name);};
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROME_PATH||'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
 try{
  const page=await browser.newPage({viewport:{width:1440,height:1000}});
  page.on('pageerror',e=>report.errors.push(e.message));
  await page.route('https://**/*',r=>r.request().url().includes('/thumbnail?')?r.fulfill({contentType:'image/png',body:tiny}):r.abort());
  await page.goto(pathToFileURL(path.join(root,'index.html')).href);
  assert.deepEqual(await page.locator('[data-axis] h2').allTextContents(),categories);
  const actual=await page.locator('#archive-grid .photo-card').evaluateAll(cards=>cards.map(c=>({id:c.dataset.sourceId,category:c.dataset.category,description:c.querySelector('.description').textContent,alt:c.querySelector('img').alt,name:c.querySelector('.original-name').textContent,link:c.querySelector('a').href})));
  assert.deepEqual(actual,verified.map(r=>({id:r.sourceId,category:r.primaryCategory,description:r.visualDescription,alt:r.visualDescription,name:r.originalName,link:`https://drive.google.com/file/d/${r.sourceId}/view`})));
  const published=await page.locator('figure[data-source-id]').evaluateAll(cards=>cards.map(c=>({id:c.dataset.sourceId,category:c.dataset.category,description:c.querySelector('.description').textContent,alt:c.querySelector('img').alt,name:c.querySelector('.original-name').textContent})));
  for(const p of published){const r=verified.find(r=>r.sourceId===p.id);assert.ok(r);assert.equal(p.category,r.primaryCategory);assert.equal(p.description,r.visualDescription);assert.equal(p.alt,r.visualDescription);assert.equal(p.name,r.originalName);}
  assert.equal(await page.locator('#archive-grid .image-open').first().evaluate(el=>getComputedStyle(el).backgroundColor),'rgb(239, 231, 214)','Gallery image loading surface must remain neutral, not transparent');
  assert.ok(await page.locator('a[href="audit/thematic-catalog.json"]').count());
  assert.equal(await page.locator('[contenteditable=true],input[type=file]').count(),0);
  check('Five exact axes; all 58 IDs, captions, alts, names and Drive links equal verified catalog; cover and section photos verified');
  for(const key of ['all',...slugs]){
   await page.locator(`[data-filter="${key}"]`).click();
   const expected=key==='all'?verified:verified.filter(r=>r.primaryCategory===categories[slugs.indexOf(key)]);
   assert.deepEqual(await page.locator('#archive-grid .photo-card:visible').evaluateAll(cs=>cs.map(c=>c.dataset.sourceId)),expected.map(r=>r.sourceId));
   assert.match(await page.locator('#gallery-count').textContent(),new RegExp(`^${expected.length} de ${verified.length} fotografías`));
   assert.equal(await page.locator(`[data-filter="${key}"]`).getAttribute('aria-pressed'),'true');
   assert.equal(await page.locator('#gallery-empty').isVisible(),expected.length===0);
  }
  check('Six filters with exact IDs/counts: 58 / 29 / 15 / 9 / 5 / 0; honest empty state');
  await page.locator('[data-filter="mar"]').click();
  const marine=verified.filter(r=>r.primaryCategory===categories[2]);
  const first=page.locator('#archive-grid .photo-card:visible [data-open]').first();
  await first.focus();await page.keyboard.press('Enter');
  assert.equal(await page.locator('#lightbox').isVisible(),true);
  assert.equal(await page.locator('#lightbox-name').textContent(),marine[0].originalName);
  assert.equal(await page.locator('#lightbox-close').evaluate(el=>el===document.activeElement),true);
  await page.keyboard.press('ArrowRight');
  assert.equal(await page.locator('#lightbox-description').textContent(),marine[1].visualDescription);
  await page.locator('#lightbox-prev').click();
  assert.equal(await page.locator('#lightbox-drive').getAttribute('href'),`https://drive.google.com/file/d/${marine[0].sourceId}/view`);
  await page.locator('#lightbox-next').click();await page.keyboard.press('ArrowLeft');
  await page.keyboard.press('Shift+Tab');
  assert.equal(await page.locator('#lightbox').evaluate(el=>el.contains(document.activeElement)),true);
  await page.keyboard.press('Escape');
  assert.equal(await page.locator('#lightbox').isVisible(),false);
  assert.equal(await first.evaluate(el=>el===document.activeElement),true);
  await first.click();await page.locator('#lightbox-close').click();
  assert.equal(await first.evaluate(el=>el===document.activeElement),true);
  check('Lightbox keyboard, next/previous buttons and arrows, filtered sequence, modal focus, Esc, close and focus return');
  for(const width of [1440,390,360]){
   await page.setViewportSize({width,height:900});
   for(const slug of slugs){await page.locator(`.site-header nav a[href="#${slug}"]`).click();await page.waitForFunction(s=>location.hash===`#${s}`,slug);assert.equal(await page.locator(`#${slug} h2`).isVisible(),true);}
   const dimensions=await page.evaluate(()=>({scroll:document.documentElement.scrollWidth,viewport:innerWidth}));
   assert.ok(dimensions.scroll<=dimensions.viewport,`overflow at ${width}: ${JSON.stringify(dimensions)}`);
   report.viewports.push({width,...dimensions,navAnchors:5});
  }
  check('Desktop 1440 and mobile 390/360: five working navigation anchors, no document overflow');
  await page.locator('.cover-photo [data-open]').click();
  await page.locator('#lightbox-next').click();
  const modalBounds=await page.locator('#lightbox').boundingBox();
  assert.ok(modalBounds.x>=0 && modalBounds.x+modalBounds.width<=360);
  await page.keyboard.press('Escape');
  check('Mobile 360: lightbox opens, next works, modal stays within viewport and closes');
  await page.locator('[data-gallery-filter="hierbas"]').click();
  assert.match(await page.locator('#gallery-count').textContent(),/^15 de 58/);
  await page.emulateMedia({media:'print'});
  assert.equal(await page.locator('#archive-grid .photo-card:visible').count(),58);
  assert.equal(await page.locator('.site-header').isVisible(),false);
  assert.equal(await page.locator('#print-button').isVisible(),false);
  await page.setViewportSize({width:1440,height:1000});
  await page.pdf({path:path.join(out,'print-layout-MOCK.pdf'),printBackground:true});
  await page.emulateMedia({media:'screen'});
  assert.equal(await page.locator('#archive-grid .photo-card:visible').count(),15);
  check('Print includes all 58 records, hides controls; PDF generated (mock images); screen filter preserved');
  await page.evaluate(()=>{window.print=()=>{window.__printCalled=true;};});
  await page.locator('#print-button').click();
  await page.waitForFunction(()=>window.__printCalled===true);
  assert.equal(await page.locator('#print-button').isDisabled(),false);
  check('Print button prepares images, invokes browser print API, and restores its enabled state');
  const failed=await browser.newPage({viewport:{width:390,height:900}});
  failed.on('pageerror',e=>report.errors.push(e.message));
  await failed.route('https://**/*',r=>r.abort());
  await failed.goto(pathToFileURL(path.join(root,'index.html')).href);
  await failed.locator('.cover-photo .image-fallback').waitFor({state:'visible'});
  assert.match(await failed.locator('.cover-photo .image-fallback').textContent(),/conexión, al servicio o al acceso/);
  assert.equal(await failed.locator('.cover-photo a').isVisible(),true);
  await failed.locator('.cover-photo [data-open]').click();
  await failed.locator('#lightbox-fallback').waitFor({state:'visible'});
  assert.equal(await failed.locator('#lightbox-drive').isVisible(),true);
  await failed.keyboard.press('Escape');
  await failed.screenshot({path:path.join(out,'fallback-390.png')});
  check('Aborted Drive requests: neutral fallback in cover/modal, usable original link');
  assert.deepEqual(report.errors,[]);check('No uncaught JavaScript errors');
  report.status='passed';
 }catch(e){report.status='failed';report.failure=e.stack;throw e;}
 finally{fs.writeFileSync(path.join(out,'browser-mock-results.json'),JSON.stringify(report,null,2));await browser.close();console.log('Artifacts:',out);}
})().catch(e=>{console.error(e);process.exitCode=1;});
