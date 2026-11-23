/* Network smoke: actual Drive requests, never fixtures or image substitutions. */
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {pathToFileURL}=require('node:url');
const {chromium}=require(process.env.PLAYWRIGHT_PATH||'C:/Users/D/node_modules/playwright');
const root=path.resolve(__dirname,'..');
const out=process.env.ARTIFACT_DIR||path.join(process.env.USERPROFILE,'AppData/Local/hermes/profiles/null/cache/scratch/marea-editorial-qa');
fs.mkdirSync(out,{recursive:true});
const report={transport:'REAL Drive network (no image interception)',loaded:[],requestsFailed:[],responses:[],jsErrors:[],viewports:[]};
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:process.env.CHROME_PATH||'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 try{
  const page=await browser.newPage({viewport:{width:1440,height:1000}});
  page.on('pageerror',e=>report.jsErrors.push(e.message));
  page.on('requestfailed',r=>report.requestsFailed.push({url:r.url(),error:r.failure()?.errorText}));
  page.on('response',r=>{if(r.url().includes('thumbnail?'))report.responses.push({url:r.url(),status:r.status()});});
  await page.goto(process.env.MAGAZINE_URL||pathToFileURL(path.join(root,'index.html')).href,{waitUntil:'load',timeout:60000});
  await page.locator('#mosaic-c1 img').evaluateAll(images=>images.slice(0,6).forEach(i=>i.loading='eager'));
  await page.waitForFunction(()=>new Set([...document.querySelectorAll('[id^="mosaic-c"] img')].filter(i=>i.complete&&i.naturalWidth>0).map(i=>i.dataset.driveId)).size>=5,{},{timeout:60000});
  await page.evaluate(()=>document.fonts.ready);
  report.loaded=await page.locator('[id^="mosaic-c"] img').evaluateAll(images=>images.filter(i=>i.complete&&i.naturalWidth>0).map(i=>({id:i.dataset.driveId,src:i.currentSrc,width:i.naturalWidth,height:i.naturalHeight})));
  for(const width of [1440,390,360]){
   await page.setViewportSize({width,height:width===1440?1000:900});
   await page.evaluate(()=>{document.documentElement.style.scrollBehavior='auto';scrollTo(0,0);});
   await page.screenshot({path:path.join(out,`real-cover-${width}.png`)});
   const d=await page.evaluate(()=>({viewport:innerWidth,scroll:document.documentElement.scrollWidth}));
   assert.ok(d.scroll<=d.viewport);report.viewports.push(d);
  }
  await page.setViewportSize({width:1440,height:1000});
  await page.locator('#mosaic-c1').scrollIntoViewIfNeeded();await page.waitForTimeout(800);
  await page.screenshot({path:path.join(out,'real-mosaic-1440.png')});
  await page.locator('#mosaic-c1 [data-open]').first().click();
  await page.waitForFunction(()=>{const i=document.querySelector('#lb-stage img');return i.complete&&i.naturalWidth>0;},{},{timeout:45000});
  report.lightboxLoaded=await page.locator('#lb-stage img').evaluate(i=>i.complete&&i.naturalWidth>0);
  await page.screenshot({path:path.join(out,'real-lightbox-1440.png')});
  await page.keyboard.press('Escape');
  assert.deepEqual(report.jsErrors,[]);
  assert.ok(new Set(report.loaded.map(i=>i.id)).size>=5,'Need five distinct real Drive IDs loaded; inspect network report if blocked');
  assert.equal(report.lightboxLoaded,true);
  report.status='passed';
 }catch(e){report.status='failed';report.failure=e.stack;throw e;}
 finally{fs.writeFileSync(path.join(out,'browser-real-results.json'),JSON.stringify(report,null,2));await browser.close();console.log(JSON.stringify(report,null,2));console.log('Artifacts:',out);}
})().catch(e=>{console.error(e);process.exitCode=1;});
