const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
class Element {
 constructor(tag) { this.tag=tag; this.children=[]; this.textContent=''; }
 append(...nodes) { this.children.push(...nodes); }
 replaceChildren(...nodes) { this.children=nodes; }
 set innerHTML(_) { throw Error('Unsafe HTML insertion'); }
}
async function render(payload, products={schema_version:1,products:[]}, fail=false) {
 const els=Object.fromEntries(['year','news','updated','products'].map(id=>[id,new Element('div')]));
 const context=vm.createContext({URL,Date,document:{getElementById:id=>els[id],createElement:tag=>new Element(tag)},fetch:async url=>({ok:!fail,json:async()=>url.includes('published')?payload:products})});
 vm.runInContext(fs.readFileSync('docs/app.js','utf8'),context);
 await new Promise(resolve=>setImmediate(resolve));
 return els;
}
(async()=>{
 const article={id:'fixture',headline:'<img src=x onerror=alert(1)>',draft:'<script>alert(1)</script>',source_url:'https://example.org',status:'approved',approved_by:'Tester',approved_at:'2026-10-26T00:00:00Z'};
 let dom=await render({items:[article,{...article,status:'needs_human_review'},{...article,source_url:'javascript:alert(1)'}]});
 assert.equal(dom.news.children.length,1);
 assert.equal(dom.news.children[0].children[1].textContent,article.headline);
 const a=dom.news.children[0].children[3]; assert.equal(a.href,'https://example.org/'); assert.match(a.rel,/noopener/);
 dom=await render({items:[]}); assert.match(dom.news.children[0].textContent,/Chưa có bài/);
 dom=await render({items:{} }); assert.match(dom.news.children[0].textContent,/Không tải/);
 dom=await render({},undefined,true); assert.match(dom.news.children[0].textContent,/Không tải/);
 dom=await render({items:[]},{schema_version:1,products:[{name:'Fixture',source_name:'Fixture',source_url:'https://example.org',verified_at:'2026-10-26',affiliate_url:'https://example.org/offer'}]});
 assert.match(dom.products.children[0].children[4].rel,/sponsored/);
 console.log('PASS: DOM escaping, approval filter, HTTPS links, empty/error states, affiliate disclosure');
})().catch(err=>{console.error(err);process.exitCode=1});
