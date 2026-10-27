document.getElementById('year').textContent = new Date().getFullYear();
function node(tag, text, className) { const el=document.createElement(tag); if(text!==undefined) el.textContent=text; if(className) el.className=className; return el; }
function safeURL(value) { try { const u=new URL(value); return u.protocol==='https:' && !u.username && !u.password ? u.href : null; } catch { return null; } }
function link(text, url, affiliate=false) { const a=node('a',text); a.href=url; a.target='_blank'; a.rel=affiliate?'sponsored noopener noreferrer':'noopener noreferrer nofollow'; return a; }
async function loadNews() {
 const box=document.getElementById('news');
 try {
  const response=await fetch('data/published.json'); if(!response.ok) throw new Error();
  const data=await response.json(); if(!Array.isArray(data.items)) throw new Error();
  box.replaceChildren();
  for(const item of data.items.slice(0,12)) {
   if(!item || item.status!=='approved' || !item.approved_by || !Number.isFinite(Date.parse(item.approved_at)) || !safeURL(item.source_url) || typeof item.headline!=='string' || typeof item.draft!=='string') continue;
   const card=node('article',undefined,'card'); card.append(node('p',item.source||'Nguồn bên ngoài','meta'),node('h3',item.headline),node('p',item.draft),link('Đọc nguồn gốc ↗',safeURL(item.source_url))); box.append(card);
  }
  if(!box.children.length) box.append(node('p','Chưa có bài được duyệt. Vui lòng quay lại sau.','card'));
  if(data.updated_at && Number.isFinite(Date.parse(data.updated_at))) document.getElementById('updated').textContent='Cập nhật: '+new Date(data.updated_at).toLocaleString('vi-VN');
 } catch { box.replaceChildren(node('p','Không tải được tin. Vui lòng thử lại sau.','card')); }
}
async function loadProducts() {
 const box=document.getElementById('products');
 try {
  const response=await fetch('data/products.json'); if(!response.ok) throw new Error();
  const data=await response.json(); if(data.schema_version!==1 || !Array.isArray(data.products)) throw new Error(); box.replaceChildren();
  for(const p of data.products) {
   if(!p || !safeURL(p.source_url) || !Number.isFinite(Date.parse(p.verified_at)) || typeof p.name!=='string') continue;
   const card=node('article',undefined,'card'); card.append(node('h3',p.name),node('p',p.category||'Thiết bị','meta'),node('p','Nguồn: '+p.source_name+' · Xác minh: '+new Date(p.verified_at).toLocaleDateString('vi-VN')),link('Thông tin từ nguồn ↗',safeURL(p.source_url)));
   if(safeURL(p.affiliate_url)) card.append(node('p','CineTech AI có thể nhận hoa hồng từ liên kết này.'),link('Liên kết tiếp thị liên kết ↗',safeURL(p.affiliate_url),true)); box.append(card);
  }
  if(!box.children.length) box.append(node('p','Chưa có sản phẩm được xác minh. Các gợi ý bên dưới chỉ là nhóm thiết bị, không phải đánh giá sản phẩm.','card'));
 } catch { box.replaceChildren(node('p','Không tải được danh mục sản phẩm.','card')); }
}
loadNews(); loadProducts();
