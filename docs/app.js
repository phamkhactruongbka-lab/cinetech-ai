document.getElementById('year').textContent = new Date().getFullYear();
function node(tag, text, className) { const el=document.createElement(tag); if(text!==undefined) el.textContent=text; if(className) el.className=className; return el; }
function safeURL(value) { try { const u=new URL(value); return u.protocol==='https:' && !u.username && !u.password ? u.href : null; } catch { return null; } }
function link(text, url, affiliate=false) { const a=node('a',text); a.href=url; a.target='_blank'; a.rel=affiliate?'sponsored noopener noreferrer':'noopener noreferrer nofollow'; return a; }

function analyzeMovieContent(headline, draft, idx) {
 const text = ((headline || '') + ' ' + (draft || '')).toLowerCase();
 if (text.includes('ai') || text.includes('gò tam tinh') || text.includes('tương lai') || text.includes('hoạt hình') || text.includes('kỹ xảo') || text.includes('khoa học')) {
  return {
   themeId: 'scifi',
   cardClass: 'card news-card theme-scifi',
   poster: 'assets/poster-scifi.png',
   genre: 'Phim khoa học viễn tưởng & AI',
   deviceHint: 'Gợi ý: Máy chiếu màn ảnh rộng'
  };
 }
 if (text.includes('trại buôn người') || text.includes('án mạng') || text.includes('phòng vé') || text.includes('tỷ đồng') || text.includes('hành động') || text.includes('bí ẩn')) {
  return {
   themeId: 'mystery',
   cardClass: 'card news-card theme-mystery',
   poster: 'assets/poster-mystery.png',
   genre: 'Phim hành động và bí ẩn',
   deviceHint: 'Gợi ý: Loa Soundbar rõ thoại'
  };
 }
 if (text.includes('tokyo') || text.includes('đức') || text.includes('liên hoan') || text.includes('châu á') || text.includes('quốc tế')) {
  return {
   themeId: 'festival',
   cardClass: 'card news-card theme-festival',
   poster: 'assets/hero-cinema-room.png',
   genre: 'Liên hoan phim Quốc tế',
   deviceHint: 'Gợi ý: Tai nghe chống ồn'
  };
 }
 const pool = ['assets/poster-scifi.png', 'assets/poster-mystery.png', 'assets/hero-cinema-room.png'];
 return {
  themeId: 'cinema',
  cardClass: 'card news-card theme-cinema',
  poster: pool[idx % pool.length],
  genre: 'Tiêu điểm Điện ảnh',
  deviceHint: 'Gợi ý: Thiết bị giải trí tại gia'
 };
}

function pickDeviceIconClass(category, name) {
 const c = ((category || '') + ' ' + (name || '')).toLowerCase();
 if (c.includes('tai nghe') || c.includes('sony')) return 'device-icon-box icon-headphones';
 if (c.includes('máy chiếu') || c.includes('benq')) return 'device-icon-box icon-projector';
 if (c.includes('loa') || c.includes('sonos') || c.includes('soundbar')) return 'device-icon-box icon-speaker';
 return 'device-icon-box icon-projector';
}

let cachedApprovedArticles = [];
let activeGenreFilter = 'all';
let activeSearchQuery = '';

function renderNewsCards(items) {
 const box = document.getElementById('news');
 if (!box) return;
 box.replaceChildren();
 let idx = 0;
 for (const item of items) {
  const profile = analyzeMovieContent(item.headline, item.draft, idx);
  if (activeGenreFilter !== 'all' && profile.themeId !== activeGenreFilter) continue;
  if (activeSearchQuery) {
   const haystack = (item.headline + ' ' + item.draft + ' ' + (item.source || '') + ' ' + profile.genre).toLowerCase();
   if (!haystack.includes(activeSearchQuery)) continue;
  }
  const card = node('article', undefined, profile.cardClass);
  const visual = node('div', undefined, 'card-visual');
  const img = node('img', undefined, 'card-thumb');
  img.src = profile.poster;
  img.alt = item.headline;
  img.loading = 'lazy';
  const badge = node('span', profile.genre, 'card-genre-badge');
  const hint = node('span', profile.deviceHint, 'card-device-hint');
  visual.append(img, badge, hint);
  card.append(
   node('p', item.source || 'Nguồn bên ngoài', 'meta'),
   node('h3', item.headline),
   node('p', item.draft),
   link('Đọc nguồn gốc ↗', safeURL(item.source_url)),
   visual
  );
  box.append(card);
  idx++;
 }
 if (!box.children.length) {
  const msg = (activeGenreFilter !== 'all' || activeSearchQuery)
   ? 'Không tìm thấy bài viết khớp bộ lọc chủ đề này. Hãy thử từ khóa hoặc chủ đề khác.'
   : 'Chưa có bài được duyệt. Vui lòng quay lại sau.';
  box.append(node('p', msg, 'card'));
 }
}

function setupSmartUIControls() {
 if (typeof document.querySelectorAll !== 'function') return;
 const searchInput = document.getElementById('movie-search');
 if (searchInput && searchInput.addEventListener) {
  searchInput.addEventListener('input', e => {
   activeSearchQuery = (e.target.value || '').trim().toLowerCase();
   renderNewsCards(cachedApprovedArticles);
  });
 }
 const genreBtns = document.querySelectorAll('.genre-btn');
 genreBtns.forEach(btn => {
  btn.addEventListener('click', () => {
   genreBtns.forEach(b => b.classList.remove('active'));
   btn.classList.add('active');
   activeGenreFilter = btn.getAttribute('data-genre') || 'all';
   if (document.body) document.body.setAttribute('data-ui-theme', activeGenreFilter);
   renderNewsCards(cachedApprovedArticles);
  });
 });
 const posterCards = document.querySelectorAll('.poster-showcase-card');
 posterCards.forEach(card => {
  card.addEventListener('click', () => {
   const filter = card.getAttribute('data-filter');
   if (!filter) return;
   activeGenreFilter = activeGenreFilter === filter ? 'all' : filter;
   genreBtns.forEach(b => {
    b.classList.toggle('active', b.getAttribute('data-genre') === activeGenreFilter);
   });
   if (document.body) document.body.setAttribute('data-ui-theme', activeGenreFilter);
   renderNewsCards(cachedApprovedArticles);
  });
 });
}

async function loadNews() {
 const box=document.getElementById('news');
 try {
  const response=await fetch('data/published.json'); if(!response.ok) throw new Error();
  const data=await response.json(); if(!Array.isArray(data.items)) throw new Error();
  const approved = [];
  for(const item of data.items.slice(0,12)) {
   if(!item || item.status!=='approved' || !item.approved_by || !Number.isFinite(Date.parse(item.approved_at)) || !safeURL(item.source_url) || typeof item.headline!=='string' || typeof item.draft!=='string') continue;
   approved.push(item);
  }
  cachedApprovedArticles = approved;
  activeGenreFilter = 'all';
  activeSearchQuery = '';
  renderNewsCards(approved);
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
   const card=node('article',undefined,'card product-card');
   card.append(
    node('h3',p.name),
    node('p',p.category||'Thiết bị','meta'),
    node('p','Nguồn: '+p.source_name+' · Xác minh: '+new Date(p.verified_at).toLocaleDateString('vi-VN')),
    link('Thông tin từ nguồn ↗',safeURL(p.source_url))
   );
   if(safeURL(p.affiliate_url)) card.append(node('p','CineTech AI có thể nhận hoa hồng từ liên kết này.'),link('Liên kết tiếp thị liên kết ↗',safeURL(p.affiliate_url),true));
   const iconBox=node('div',undefined,pickDeviceIconClass(p.category,p.name));
   card.append(iconBox);
   box.append(card);
  }
  if(!box.children.length) box.append(node('p','Chưa có sản phẩm được xác minh. Các gợi ý bên dưới chỉ là nhóm thiết bị, không phải đánh giá sản phẩm.','card'));
 } catch { box.replaceChildren(node('p','Không tải được danh mục sản phẩm.','card')); }
}

setupSmartUIControls();
loadNews();
loadProducts();
