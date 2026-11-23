/* Exact reference / standalone regression. No installs. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const {pathToFileURL}=require('node:url');
const {chromium}=require(process.env.PLAYWRIGHT_PATH||'C:/Users/D/node_modules/playwright');
const root=path.resolve(__dirname,'..');
(async()=>{const browser=await chromium.launch({executablePath:process.env.CHROME_PATH||'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});try{
 const dir=fs.mkdtempSync(path.join(process.env.TMPDIR||os.tmpdir(),'marea-single-'));fs.copyFileSync(path.join(root,'index.html'),path.join(dir,'index.html'));
 const page=await browser.newPage({viewport:{width:1440,height:1000}});const errors=[];page.on('pageerror',e=>errors.push(e.message));await page.route(/^https?:/,r=>r.abort());await page.goto(pathToFileURL(path.join(dir,'index.html')).href);
 assert.equal(await page.locator('[id^="mosaic-c"]').count(),5,'Preserve five editorial mosaics, not a replacement gallery');
 assert.equal(await page.locator('#glossary-grid > button').count(),44);
 assert.equal(await page.locator('script[src],link[rel="stylesheet"][href^="assets"]').count(),0);
 assert.equal(await page.locator('[id^="mosaic-c"] figure').count(),58);
 assert.equal(await page.locator('#mosaic-c1').evaluate(el=>getComputedStyle(el).gridTemplateColumns.split(' ').length),4);
 assert.equal(await page.locator('#portada').evaluate(el=>getComputedStyle(el).backgroundColor),'rgb(16, 78, 107)');
 assert.deepEqual(errors,[]);console.log('PASS editorial reference + 44 glossary entries + 58 photos + standalone offline CSS');
}finally{await browser.close()}})().catch(e=>{console.error(e);process.exitCode=1});
