/* Compare original-reference computed design tokens to standalone output. */
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');const {pathToFileURL}=require('node:url');
const {chromium}=require(process.env.PLAYWRIGHT_PATH||'C:/Users/D/node_modules/playwright');const root=path.resolve(__dirname,'..');
const out=process.env.ARTIFACT_DIR||path.join(process.env.USERPROFILE,'AppData/Local/hermes/profiles/null/cache/scratch/marea-editorial-qa');fs.mkdirSync(out,{recursive:true});
const selectors=['header','h1','#portada','#editorial','#editorial h2','#cronica-1','#cronica-2','#cronica-3','#cronica-4','#cronica-5','#mosaic-c1','#mosaic-c3','#glossary-grid','footer'];
const props=['backgroundColor','color','fontFamily','fontSize','fontWeight','lineHeight','display','gridTemplateColumns','columnGap','paddingLeft','paddingRight','borderRadius'];
(async()=>{const b=await chromium.launch({executablePath:process.env.CHROME_PATH||'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});try{
 const reference=await b.newPage({viewport:{width:1440,height:1000}}),final=await b.newPage({viewport:{width:1440,height:1000}});
 // Do not load uninspected MOV previews or the other unreviewed reference photos.
 await reference.route(/https:\/\/(drive\.google|lh3\.googleusercontent)/,r=>r.request().url().includes('1r4OYEQtf00TzGKc7I8qH2Dg-lIHsKg9o')?r.continue():r.abort());
 await Promise.all([reference.goto(pathToFileURL(path.join(root,'source/editorial-template.html')).href,{waitUntil:'domcontentloaded'}),final.goto(pathToFileURL(path.join(root,'index.html')).href,{waitUntil:'domcontentloaded'})]);
 await reference.waitForFunction(()=>getComputedStyle(document.querySelector('#mosaic-c1')).display==='grid',{},{timeout:60000});
 await Promise.all([reference.evaluate(()=>document.fonts.ready),final.evaluate(()=>document.fonts.ready)]);
 const results=[];
 for(const width of [1440,390,360]){
  await Promise.all([reference.setViewportSize({width,height:1000}),final.setViewportSize({width,height:1000})]);
  const sample=async p=>p.evaluate(({selectors,props})=>Object.fromEntries(selectors.map(s=>[s,Object.fromEntries(props.map(k=>[k,getComputedStyle(document.querySelector(s))[k]]))])),{selectors,props});
  const [a,z]=await Promise.all([sample(reference),sample(final)]);assert.deepEqual(z,a,`Reference computed design mismatch at ${width}`);results.push({width,matchedSelectors:selectors.length,matchedProperties:props.length,reference:a,standalone:z});
  await reference.evaluate(()=>{document.documentElement.style.scrollBehavior='auto';scrollTo(0,0)});await reference.screenshot({path:path.join(out,`reference-cover-${width}.png`)});
 }
 // The original editorial paragraphs, headings and footer credit remain verbatim.
 const original=await reference.locator('#editorial p,article > div > .max-w-4xl h2,article .space-y-4 p,footer p').allTextContents();
 const delivered=await final.locator('#editorial p,article > div > .max-w-4xl h2,article .space-y-4 p,footer p').allTextContents();
 assert.deepEqual(delivered,original);
 fs.writeFileSync(path.join(out,'reference-style-comparison.json'),JSON.stringify({status:'passed',editorialTextNodesPreserved:original.length,results},null,2));console.log('PASS original reference styles match standalone: 14 components × 12 properties × 3 viewports; '+original.length+' editorial text nodes preserved');
}finally{await b.close()}})().catch(e=>{console.error(e);process.exitCode=1});
