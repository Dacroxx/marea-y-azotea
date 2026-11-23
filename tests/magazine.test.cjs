/* Browser contract. Uses installed Playwright; no npm install required. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium} = require(process.env.PLAYWRIGHT_PATH || 'C:/Users/D/node_modules/playwright');
const root = path.resolve(__dirname, '..');
const catalog = JSON.parse(fs.readFileSync(path.join(root,'audit/thematic-catalog.json'),'utf8'));
const verified = catalog.filter(r=>r.mediaType==='photo' && r.reviewStatus==='verified');
const categories = fs.readFileSync(path.join(root,'audit/TAXONOMY.md'),'utf8').split('\n').filter(l=>/^\d\. /.test(l)).map(l=>l.replace(/^\d\. /,'').split(':')[0]);
(async()=>{
 const browser = await chromium.launch({executablePath:process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
 try {
  const page = await browser.newPage({viewport:{width:1440,height:1000}});
  await page.route('https://**/*',r=>r.abort());
  await page.goto(pathToFileURL(path.join(root,'index.html')).href);
  assert.deepEqual(await page.locator('[data-axis] h2').allTextContents(),categories,'Five exact thematic headings must replace the old chapters');
  assert.equal(await page.locator('#archive-grid [data-source-id]').count(),verified.length,'Only the full verified selection is published');
  console.log('PASS: five thematic axes and verified selection');
 } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
