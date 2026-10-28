"""Phòng Giao Diện & Trải Nghiệm UI (Robot Astro-Cinema):
Tự động phân tích nội dung bài đăng điện ảnh, nhận diện thể loại/tâm trạng phim
và sinh cấu hình giao diện (poster, bảng màu, nhãn chủ đề, gợi ý thiết bị) thu hút người xem.
"""
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

THEME_RULES = [
    {
        'theme_id': 'scifi',
        'genre_label': 'Phim khoa học viễn tưởng & AI',
        'mood_tag': 'Viễn tưởng · Công nghệ điện ảnh',
        'poster': 'assets/poster-scifi.png',
        'accent_color': '#38bdf8',
        'device_hint': 'Phù hợp xem trên: Máy chiếu màn ảnh rộng',
        'keywords': ('ai', 'gò tam tinh', 'tương lai', 'hoạt hình', 'kỹ xảo', 'khoa học', 'viễn tưởng', 'robot', 'elon musk', 'không gian')
    },
    {
        'theme_id': 'mystery',
        'genre_label': 'Phim hành động và bí ẩn',
        'mood_tag': 'Kịch tính · Tâm điểm phòng vé',
        'poster': 'assets/poster-mystery.png',
        'accent_color': '#f59e0b',
        'device_hint': 'Phù hợp nghe với: Loa Soundbar âm trầm rõ thoại',
        'keywords': ('trại buôn người', 'án mạng', 'phòng vé', 'tỷ đồng', 'hành động', 'bí ẩn', 'kịch tính', 'tội phạm', 'kinh dị', '18+', 'lật mặt')
    },
    {
        'theme_id': 'festival',
        'genre_label': 'Liên hoan phim & Điện ảnh Quốc tế',
        'mood_tag': 'Nghệ thuật · Giao lưu điện ảnh',
        'poster': 'assets/hero-cinema-room.png',
        'accent_color': '#2dd4bf',
        'device_hint': 'Phù hợp thưởng thức: Tai nghe chống ồn chi tiết cao',
        'keywords': ('tokyo', 'liên hoan phim', 'châu á', 'đức', 'kinofest', 'quốc tế', 'nhà làm phim', 'đạo diễn', 'tiff', 'crosscut')
    }
]

def classify_article_content(headline, draft=''):
    """Tự động phân tích tiêu đề và tóm tắt bài viết để chọn giao diện phù hợp."""
    text = f"{headline or ''} {draft or ''}".lower()
    for rule in THEME_RULES:
        matched = [kw for kw in rule['keywords'] if kw in text]
        if matched:
            return {
                'theme_id': rule['theme_id'],
                'genre_label': rule['genre_label'],
                'mood_tag': rule['mood_tag'],
                'poster': rule['poster'],
                'accent_color': rule['accent_color'],
                'device_hint': rule['device_hint'],
                'matched_keywords': matched
            }
    return {
        'theme_id': 'cinema',
        'genre_label': 'Tiêu điểm Điện ảnh',
        'mood_tag': 'Góc nhìn điện ảnh',
        'poster': 'assets/hero-cinema-room.png',
        'accent_color': '#5eead4',
        'device_hint': 'Phù hợp trải nghiệm: Thiết bị giải trí tại gia',
        'matched_keywords': []
    }

def run_ui_designer(root=ROOT):
    """Quét danh sách bài đã duyệt và xuất cấu hình giao diện phù hợp nội dung phim."""
    root = Path(root)
    pub_path = root / 'docs/data/published.json'
    out_path = root / 'docs/data/ui_themes.json'
    items = []
    if pub_path.exists():
        try:
            data = json.loads(pub_path.read_text(encoding='utf-8'))
            if isinstance(data.get('items'), list):
                items = data['items']
        except Exception:
            items = []

    article_themes = {}
    genre_counts = {'scifi': 0, 'mystery': 0, 'festival': 0, 'cinema': 0}
    for item in items:
        if not isinstance(item, dict) or not item.get('id'):
            continue
        profile = classify_article_content(item.get('headline', ''), item.get('draft', ''))
        article_themes[item['id']] = profile
        genre_counts[profile['theme_id']] = genre_counts.get(profile['theme_id'], 0) + 1

    dominant_theme = max(genre_counts, key=genre_counts.get) if any(genre_counts.values()) else 'cinema'
    payload = {
        'schema_version': 1,
        'updated_at': datetime.now(timezone(timedelta(hours=7))).isoformat(),
        'dominant_theme': dominant_theme,
        'genre_counts': genre_counts,
        'articles': article_themes
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    return {
        'status': 'PASS',
        'themed_articles': len(article_themes),
        'dominant_theme': dominant_theme,
        'output': str(out_path.relative_to(root))
    }

if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    res = run_ui_designer()
    print(f"UI Designer: Đã tự động thiết kế giao diện cho {res['themed_articles']} bài phim (Chủ đề nổi bật: {res['dominant_theme']}).")

