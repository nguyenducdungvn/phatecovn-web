#!/usr/bin/env python3
"""Sinh website tĩnh PHATECO (bản thử nghiệm) vào thư mục docs/.

Chạy:  python3 build.py
Nội dung các trang dịch vụ nằm ở src/pages/dich-vu/*.html; nội dung khác nằm ngay trong file này.
Mọi liên kết được sinh dạng tương đối nên site chạy được ở tên miền gốc (phateco.vn)
lẫn ở đường dẫn con (GitHub Pages: /phatecovn-web/).
"""
import os, re, shutil, html, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'docs')
UP = 'https://phateco.com/wp-content/uploads/'
SITE = 'https://phateco.vn/'
TODAY = datetime.date.today().isoformat()

LOGO = UP + '2025/01/phateco-new-2-2-e1736138637956-300x167.png'
HERO = UP + '2025/01/z4724203369946_0e1082a2769ffd3808bbc4a39552b41a-2048x650-1.jpg'

# ---------- Dữ liệu ----------
SERVICES = [
    # slug, tên, mô tả ngắn, ảnh, icon, nhóm
    ('kiem-tra-khong-pha-huy', 'Kiểm tra không phá hủy (NDT)', 'VT, RT, UT, PT, MT đến PAUT, TOFD, ECT, LRUT – phát hiện khuyết tật mà không dừng sản xuất.', UP + '2025/01/kiemtra.jpg', 'scan'),
    ('khao-sat-kiem-tra-thiet-bi', 'Khảo sát, kiểm tra & đánh giá thiết bị', 'Thiết bị nâng, bình bồn áp lực, Fitness-for-Service, vật rơi, tuabin gió.', UP + '2025/01/3.jpg', 'gauge'),
    ('khao-sat-an-mon-do-chieu-day', 'Khảo sát ăn mòn & đo chiều dày tôn', 'Theo quy phạm DNV, LR, ABS, ClassNK, BV, KR, RINA, VR; chương trình CAP, CAS.', UP + '2025/01/6.jpg', 'ship'),
    ('co-khi-che-tao-sua-chua', 'Chế tạo, sửa chữa & bảo dưỡng cơ khí', 'Kết cấu thép, đường ống, bình bồn; sửa chữa công trình biển; điện gió.', UP + '2025/01/5.jpg', 'wrench'),
    ('phong-thi-nghiem', 'Phòng thí nghiệm VILAS 404', 'Thử nghiệm cơ tính vật liệu và mẫu hàn; LAS-XD 269.', UP + '2025/01/9.jpg', 'flask'),
    ('dao-tao-chung-nhan-ndt', 'Đào tạo & chứng nhận NDT', 'ISO 9712, SNT-TC-1A qua trung tâm PNIC; ôn luyện API, AWS, IIW.', UP + '2025/01/PNIC-9712-1.png', 'cap'),
    ('cong-nghe-han-dao-tao', 'Công nghệ hàn & đào tạo thợ hàn', 'Chứng nhận thợ hàn ISO/IEC 17024, thẩm định WPS/PQR, PWHT.', UP + '2025/01/8.jpg', 'flame'),
    ('tu-van-quan-ly-giam-sat', 'Tư vấn quản lý & giám sát', 'Giám sát chế tạo, lắp đặt; thanh tra hàn CWI, CSWIP; tư vấn ASME Stamp.', UP + '2025/01/9.-Management.jpg', 'clip'),
    ('thuong-mai-giai-phap-ky-thuat', 'Thương mại & giải pháp kỹ thuật', 'Vật tư, thiết bị, C&I, hóa chất cho nhà máy nhiệt điện và công nghiệp.', UP + '2025/01/7.jpg', 'box'),
    ('dich-vu-tiep-can', 'Dịch vụ tiếp cận IRATA', 'Leo dây IRATA, tiếp cận bằng bè, giàn giáo BS 1139 / EN 74.', UP + '2025/01/10.jpg', 'rope'),
]

PROJECTS = [
    # tên, mô tả, ảnh, link, nhóm lọc
    ('Nhiệt điện Vũng Áng 2', 'NDT và PAUT · Liên danh Doosan – Samsung · Chủ đầu tư VAPCO', UP + '2025/11/ND-VA2.jpg', 'https://phateco.com/du-an-nhiet-dien-vung-ang-2/', 'dien ndt'),
    ('Nhiệt điện Quảng Trạch 1', 'Dịch vụ NDT · Liên danh MC – HDEC – CC1 · Chủ đầu tư EVN', UP + '2025/11/ND-QT-1.jpg', 'https://phateco.com/du-an-nhiet-dien-quang-trach-1/', 'dien ndt'),
    ('Phao neo một thân mỏ Đại Hùng', 'Chế tạo trong nước đầu tiên · PVEP POC · 2023–2024', UP + '2025/11/Phao-Calm.jpg', 'du-an/phao-neo-dai-hung/', 'dau-khi co-khi'),
    ('Nhiệt điện Vân Phong 1', 'Chủ đầu tư Sumitomo Corporation · Khách hàng Lilama 18', UP + '2025/01/nha-may-nhiet-dien-bot-van-phong-1-14.jpg', 'https://phateco.com/du-an-nhiet-dien-van-phong-1/', 'dien ndt'),
    ('Nhiệt điện Nghi Sơn 2', 'Dịch vụ NDT cho dự án BOT', None, 'https://phateco.com/du-an-nhiet-dien-nghi-son-2/', 'dien ndt'),
    ('Lọc hóa dầu Nghi Sơn', 'Kiểm tra, giám sát chất lượng', None, 'https://phateco.com/du-an-loc-hoa-dau-nghi-son/', 'dau-khi ndt'),
    ('Nhà máy Lọc dầu Dung Quất', 'NDT, khảo sát trong các kỳ bảo dưỡng', None, 'https://phateco.com/nha-may-loc-dau-dung-quat-2/', 'dau-khi ndt'),
    ('Nhiệt điện Vĩnh Tân 4 mở rộng', 'Dịch vụ NDT', None, 'https://phateco.com/du-an-nhiet-dien-vinh-tan-4-mo-rong/', 'dien ndt'),
    ('Nhiệt điện Thái Bình 1', 'Dịch vụ NDT', None, 'https://phateco.com/du-an-nhiet-dien-thai-binh-1/', 'dien ndt'),
    ('Nhiệt điện Duyên Hải 3 mở rộng', 'Dịch vụ NDT', None, 'https://phateco.com/du-an-nhiet-dien-duyen-hai-3-mo-rong/', 'dien ndt'),
    ('FPSO Ruby II, TB-VN, PTSC Lam Sơn, PTSC Biển Đông 01', 'Khảo sát, NDT ngoài khơi', None, 'https://phateco.com/ruby-ii-tb-vn-ptsc-lam-son-ptsc-bien-dong-01/', 'dau-khi hang-hai'),
    ('FPSO Lewek Emas', 'Khảo sát, kiểm tra ngoài khơi', None, 'https://phateco.com/tau-fpso-lewek-emas/', 'dau-khi hang-hai'),
    ('FPSO Armada TGT 1', 'Khảo sát, kiểm tra ngoài khơi', None, 'https://phateco.com/fpso-armada-tgt-1/', 'dau-khi hang-hai'),
    ('Giàn Mộc Tinh 1', 'Khảo sát, kiểm tra', None, 'https://phateco.com/gian-moc-tinh-1/', 'dau-khi'),
    ('Tàu PV Oil Venus', 'Đo chiều dày tôn theo quy phạm DNV', None, 'https://phateco.com/khao-sat-do-do-day-ton-tau-pv-oil-venus-theo-quy-pham-dang-kiem-dnv/', 'hang-hai'),
    ('Tàu Vosco Unity', 'Đo chiều dày tôn theo quy phạm LR & VR', None, 'https://phateco.com/khao-sat-do-do-day-ton-tau-vosco-unity-theo-quy-pham-dang-kiem-lrvr/', 'hang-hai'),
    ('Đánh giá ASME tại LILAMA 10', 'Tư vấn, đánh giá ASME', None, 'https://phateco.com/du-an-danh-gia-asme-tai-cong-ty-cp-lilama-10/', 'tu-van'),
    ('Đánh giá ASME tại PTSC PPS', 'Tư vấn, đánh giá ASME', None, 'https://phateco.com/du-an-danh-gia-asme-tai-cong-ty-co-phan-dich-vu-khai-thac-dau-khi-ptsc-pps/', 'tu-van'),
]

APPROVALS = [
    ('DNV', 'NDT · UTM · RIT'), ('Bureau Veritas', 'NDT · UTM · RIT'), ('ABS', 'NDT · UTM · RIT'),
    ('ClassNK', 'NDT · UTM · RIT'), ('Lloyd’s Register', 'UTM'), ('KR', 'NDT · UTM · RIT'),
    ('RINA', 'UTM · RIT'), ('Đăng kiểm Việt Nam (VR)', 'NDT · UTM'),
]

PARTNER_LOGOS = [
    ('DNV', UP + '2025/01/DNV.jpg'), ('BoA', UP + '2025/01/boa.jpg'), ('ILAC MRA', UP + '2025/01/ilac-mra.jpg'),
    ("Lloyd's Register", UP + '2025/01/lloyd-r.jpg'), ('ASNT', UP + '2025/01/ASNT-logo-461x300-1.jpg'),
    ('ClassNK', UP + '2025/01/classnk.png'), ('Đăng kiểm Việt Nam', UP + '2025/01/logo.jpg'), ('KR', UP + '2025/01/KR.jpg'),
]

CLIENTS = ['PVN', 'EVN', 'Vinachem', 'VIMC', 'SBIC', 'Vinacomin', 'PVEP POC', 'Doosan', 'Hyundai', 'Samsung', 'JEL', 'Modec', 'Sumitomo', 'Lilama']

OFFICES = [
    ('Trụ sở chính – Hải Phòng', 'Số 5A/613 Đường Thiên Lôi, Phường An Biên, TP. Hải Phòng', '+84 225 3 870 870', '+842253870870', 'Fax: +84 225 3 559 448', 'admin@phateco.com'),
    ('Văn phòng đại diện Hà Nội', 'Số 54/6B, KĐT Mỗ Lao, Phường Hà Đông, TP. Hà Nội', '+84 24 3513 1944', '+842435131944', 'Fax: +84 24 3513 1945', 'adminhn@phateco.com'),
    ('Văn phòng giao dịch TP. Hồ Chí Minh', '29.14D Block A2, Chung cư Đức Khải, Đường 15B, Phường Tân Mỹ, TP. Hồ Chí Minh', '+84 28 3773 3346', '+842837733346', 'Tel/Fax chung', 'adminhcm@phateco.com'),
    ('Văn phòng & Xưởng cơ khí Vũng Tàu', 'Đường số 8, KCN Đông Xuyên, Phường Rạch Dừa (Vũng Tàu), TP. Hồ Chí Minh', '+84 254 6 288 588', '+842546288588', 'Fax: +84 254 6 252 080', 'adminvt@phateco.com'),
    ('Phòng thí nghiệm & Xưởng cơ khí Hải Phòng', 'Số 24 Đường Dầu Lửa, Phường Hồng Bàng, TP. Hải Phòng', '+84 225 2 689 289', '+842252689289', 'Fax: +84 225 3 559 448', 'vilas404@phateco.com'),
]

ICONS = {
    'scan': '<path d="M3 7V5a2 2 0 0 1 2-2h2M17 3h2a2 2 0 0 1 2 2v2M21 17v2a2 2 0 0 1-2 2h-2M7 21H5a2 2 0 0 1-2-2v-2M7 12h10"/>',
    'gauge': '<circle cx="12" cy="13" r="8"/><path d="M12 13l4-4M12 5V3"/>',
    'ship': '<path d="M3 17l2 4h14l2-4-9-3-9 3zM12 14V4M8 8h8"/>',
    'wrench': '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.6 2.6-2.4-.6-.6-2.4z"/>',
    'flask': '<path d="M9 3h6M10 3v6L4 20h16l-6-11V3"/>',
    'cap': '<path d="M2 9l10-5 10 5-10 5L2 9zM6 11v5c3 2 9 2 12 0v-5"/>',
    'flame': '<path d="M12 22c4 0 7-3 7-7 0-4-3-6-4-9-2 2-2 4-3 5-1-2-2-3-2-5-3 3-5 6-5 9 0 4 3 7 7 7z"/>',
    'clip': '<path d="M9 4h6v3H9zM7 5H5v16h14V5h-2M9 13l2 2 4-4"/>',
    'box': '<path d="M3 7l9-4 9 4v10l-9 4-9-4V7zM3 7l9 4 9-4M12 11v10"/>',
    'rope': '<path d="M12 2v8M8 10h8l-1 6H9l-1-6zM10 16l-2 6M14 16l2 6"/>',
}

def icon(k):
    return f'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICONS[k]}</svg>'

CTA = '''<section class="section"><div class="wrap"><div class="band">
<div><h2>Cần báo giá hoặc tư vấn kỹ thuật?</h2><p>Gửi phạm vi công việc, địa điểm và thời gian dự kiến – kỹ sư PHATECO sẽ liên hệ lại với phương án và báo giá phù hợp.</p></div>
<div><a class="btn btn-red" href="/lien-he/#bao-gia">Yêu cầu báo giá</a> <a class="btn btn-ghost" href="tel:+842253870870">0225 3 870 870</a></div>
</div></div></section>'''

STEPS = '''<h2>Quy trình làm việc</h2><ol class="steps">
<li><strong>Tiếp nhận yêu cầu</strong><br>Nắm phạm vi, tiêu chuẩn áp dụng, tiến độ và điều kiện hiện trường.</li>
<li><strong>Phương án &amp; báo giá</strong><br>Đề xuất phương pháp, nhân sự, thiết bị và quy trình kiểm tra.</li>
<li><strong>Triển khai</strong><br>Nhân sự có chứng chỉ, tuân thủ nghiêm ngặt quy định an toàn dự án.</li>
<li><strong>Báo cáo &amp; bàn giao</strong><br>Báo cáo theo tiêu chuẩn, hỗ trợ làm việc với chủ đầu tư và đăng kiểm.</li></ol>'''

NAV = [('', 'Trang chủ'), ('gioi-thieu/', 'Giới thiệu'), ('dich-vu/', 'Dịch vụ'), ('du-an/', 'Dự án'),
       ('nang-luc/', 'Năng lực'), ('tuyen-dung/', 'Tuyển dụng'), ('lien-he/', 'Liên hệ')]

# ---------- Khung trang ----------
def layout(path, title, desc, body, lang='vi'):
    depth = path.count('/')
    pre = '../' * depth if depth else './'
    def fix(s):
        s = re.sub(r'(href|src)="/(?!/)', lambda m: f'{m.group(1)}="{pre}', s)
        return s
    def _act(p):
        return ' class="active"' if (p and path.startswith(p)) or (p == '' and path == '') else ''
    nav = ''.join('<li><a href="/' + p + '"' + _act(p) + '>' + t + '</a></li>' for p, t in NAV)
    if lang == 'en':
        nav = '<li><a href="/en/">Home</a></li><li><a href="/en/#services">Services</a></li><li><a href="/en/#projects">Projects</a></li><li><a href="/en/#contact">Contact</a></li>'
    other = '<li><a class="lang" href="/en/">EN</a></li>' if lang == 'vi' else '<li><a class="lang" href="/">VI</a></li>'
    quote = '<li><a class="btn btn-red" href="/lien-he/#bao-gia">Yêu cầu báo giá</a></li>' if lang == 'vi' else '<li><a class="btn btn-red" href="/en/#contact">Request a quote</a></li>'
    svc_links = ''.join(f'<li><a href="/dich-vu/{s[0]}/">{s[1]}</a></li>' for s in SERVICES[:6])
    canonical = SITE + path
    page = f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="robots" content="noindex">
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="{HERO}">
<meta property="og:type" content="website">
<link rel="icon" href="{LOGO}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Organization","name":"Công ty Cổ phần Dịch vụ Kỹ thuật PHATECO","alternateName":"PHATECO Technical Services JSC","url":"https://phateco.com/","logo":"{LOGO}","foundingDate":"2006-08-31","telephone":"+84-225-3870870","email":"admin@phateco.com","address":{{"@type":"PostalAddress","streetAddress":"Số 5A/613 Đường Thiên Lôi, Phường An Biên","addressLocality":"Hải Phòng","addressCountry":"VN"}},"sameAs":["https://www.youtube.com/watch?v=A8uCa5sMb9g"]}}</script>
</head>
<body>
<div class="notice-test">{"Bản thử nghiệm website PHATECO – nội dung chính thức tại" if lang=="vi" else "PHATECO website preview – official site:"} <a href="https://phateco.com">phateco.com</a></div>
<div class="topbar"><div class="wrap"><span class="hide-sm">{"Kiểm tra – Giám định – Đào tạo kỹ thuật · ISO 9001:2015 (DNV)" if lang=="vi" else "Inspection · Testing · Engineering Services · ISO 9001:2015 (DNV)"}</span><span><a href="tel:+842253870870">0225 3 870 870</a> · <a href="mailto:admin@phateco.com">admin@phateco.com</a></span></div></div>
<header class="site"><div class="wrap">
<a class="brand" href="/{"en/" if lang=="en" else ""}"><img src="{LOGO}" alt="Logo PHATECO" width="80" height="44"><span>PHATECO<small>{"Công ty CP Dịch vụ Kỹ thuật" if lang=="vi" else "Technical Services JSC"}</small></span></a>
<button class="menu-toggle" aria-label="Menu">☰</button>
<nav class="main"><ul>{nav}{other}{quote}</ul></nav>
</div></header>
<main>
{body}
</main>
<footer class="site"><div class="wrap">
<div class="cols">
<div><h4>Công ty CP Dịch vụ Kỹ thuật PHATECO</h4><p>Số 5A/613 Đường Thiên Lôi, Phường An Biên, TP. Hải Phòng</p><p>Tel: <a href="tel:+842253870870">+84 225 3 870 870</a><br>Email: <a href="mailto:admin@phateco.com">admin@phateco.com</a></p><p>ISO 9001:2015 · DNV C813459</p></div>
<div><h4>Dịch vụ</h4><ul>{svc_links}<li><a href="/dich-vu/">Tất cả dịch vụ →</a></li></ul></div>
<div><h4>Công ty</h4><ul><li><a href="/gioi-thieu/">Giới thiệu</a></li><li><a href="/gioi-thieu/#lich-su">Lịch sử 20 năm</a></li><li><a href="/nang-luc/">Năng lực &amp; chứng nhận</a></li><li><a href="/du-an/">Dự án</a></li><li><a href="https://phateco.com/tin-tuc/">Tin tức</a></li></ul></div>
<div><h4>Liên hệ</h4><ul><li><a href="/lien-he/#bao-gia">Yêu cầu báo giá</a></li><li><a href="/tuyen-dung/">Tuyển dụng</a></li><li><a href="/lien-he/">5 văn phòng &amp; cơ sở</a></li><li><a href="https://www.youtube.com/watch?v=A8uCa5sMb9g" target="_blank" rel="noopener">Phim PHATECO 20 năm</a></li></ul></div>
</div>
<div class="bottom"><span>© 2006–{datetime.date.today().year} PHATECO Technical Services JSC</span><span>phateco.com · phateco.vn</span></div>
</div></footer>
<a class="float-call" href="tel:+842253870870">☎ 0225 3 870 870</a>
<script src="/assets/js/config.js"></script>
<script src="/assets/js/site.js"></script>
</body>
</html>'''
    page = fix(page)
    dest = os.path.join(OUT, path, 'index.html')
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, 'w', encoding='utf-8').write(page)
    PAGES.append(path)

PAGES = []

def page_hero(title, sub, crumbs=''):
    return f'<section class="page-hero"><div class="wrap">{crumbs}<h1>{title}</h1><p>{sub}</p></div></section>'

def crumbs(*items):
    parts = ['<a href="/">Trang chủ</a>'] + [f'<a href="/{p}">{t}</a>' if p else t for p, t in items]
    return '<div class="crumbs">' + ' / '.join(parts) + '</div>'

def video(title='Phim PHATECO 20 năm'):
    return f'<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/A8uCa5sMb9g" title="{title}" loading="lazy" allow="accelerometer; encrypted-media; picture-in-picture" allowfullscreen></iframe></div>'

def svc_cards(limit=None):
    out = ''
    for slug, name, short, img, ic, *_ in SERVICES[:limit]:
        out += f'<a class="icon-card" href="/dich-vu/{slug}/"><div class="ic">{icon(ic)}</div><h3>{name}</h3><p>{short}</p></a>'
    return out

def proj_cards(items, with_filter=False):
    out = ''
    for name, desc, img, link, cat in items:
        href = link if link.startswith('http') else '/' + link
        ext = ' target="_blank" rel="noopener"' if link.startswith('http') else ''
        im = f'<img src="{img}" alt="{html.escape(name)}" loading="lazy">' if img else ''
        out += f'<a class="card" data-cat="{cat}" href="{href}"{ext}>{im}<div class="body"><h3>{name}</h3><p>{desc}</p><span class="more">Xem dự án →</span></div></a>'
    return out

def offices_html():
    return '<div class="offices">' + ''.join(
        f'<div class="office"><h3>{n}</h3><p>{a}</p><p>Tel: <a href="tel:{t2}">{t}</a> · {fx}</p><p>Email: <a href="mailto:{e}">{e}</a></p></div>'
        for n, a, t, t2, fx, e in OFFICES) + '</div>'

# ---------- Trang chủ ----------
def build_home():
    stats = '''<div class="stats"><div><strong>20 năm</strong><span>Từ 2006 tại Hải Phòng</span></div><div><strong>8</strong><span>Tổ chức đăng kiểm phê duyệt dịch vụ</span></div><div><strong>ISO 9001</strong><span>DNV chứng nhận liên tục từ 2007</span></div><div><strong>5</strong><span>Văn phòng &amp; cơ sở trên cả nước</span></div></div>'''
    logos = ''.join(f'<img src="{u}" alt="{n}" loading="lazy">' for n, u in PARTNER_LOGOS)
    clients = ''.join(f'<span class="chip">{c}</span>' for c in CLIENTS)
    feat = [p for p in PROJECTS if p[2]][:3]
    body = f'''
<section class="hero" style="background-image:url('{HERO}')"><div class="wrap">
<span class="eyebrow" style="color:#ffb3b5">PHATECO · Từ 2006</span>
<h1>Kiểm tra – Giám định – Đào tạo kỹ thuật cho những công trình không được phép sai</h1>
<p>Dịch vụ NDT, khảo sát, giám sát chất lượng, chế tạo cơ khí và đào tạo – chứng nhận cho các dự án năng lượng, dầu khí, hàng hải và công nghiệp trên cả nước.</p>
<div class="btns"><a class="btn btn-red" href="/lien-he/#bao-gia">Yêu cầu báo giá</a><a class="btn btn-ghost" href="/nang-luc/">Xem năng lực</a></div>
</div></section>
<div class="wrap">{stats}</div>

<section class="section"><div class="wrap center">
<span class="eyebrow">Được công nhận và phê duyệt bởi</span>
<h2>Đăng kiểm quốc tế và tổ chức công nhận</h2>
<p class="lead">DNV, Bureau Veritas, ABS, ClassNK, Lloyd’s Register, KR, RINA và Đăng kiểm Việt Nam phê duyệt dịch vụ NDT, đo chiều dày và tiếp cận dây của PHATECO. Phòng thí nghiệm VILAS 404, đối tác doanh nghiệp ASNT.</p>
<div class="logos">{logos}</div>
</div></section>

<section class="section alt" id="dich-vu"><div class="wrap">
<span class="eyebrow">Dịch vụ</span><h2>Một đầu mối cho kiểm tra, giám sát và chế tạo</h2>
<p class="lead">Từ kiểm tra không phá hủy đến chế tạo, sửa chữa – giảm đầu mối và rút ngắn tiến độ cho chủ đầu tư, nhà thầu.</p>
<div class="grid g3" style="margin-top:28px">{svc_cards(9)}<a class="icon-card" href="/dich-vu/" style="background:var(--navy);color:#fff"><h3 style="color:#fff">Xem tất cả 10 dịch vụ →</h3><p style="color:#cfe0f5">Bao gồm dịch vụ tiếp cận IRATA, bè và giàn giáo.</p></a></div>
</div></section>

<section class="section"><div class="wrap">
<div style="display:flex;justify-content:space-between;align-items:end;gap:16px;flex-wrap:wrap"><div><span class="eyebrow">Dự án tiêu biểu</span><h2>Có mặt tại các dự án trọng điểm quốc gia</h2></div><a class="btn btn-outline" href="/du-an/">Tất cả dự án</a></div>
<div class="grid g3" style="margin-top:24px">{proj_cards(feat)}</div>
<div class="chips">{clients}</div>
</div></section>

<section class="section alt"><div class="wrap split">
<div><span class="eyebrow">20 năm PHATECO</span><h2>Phát triển niềm tin, đoàn kết và hợp tác</h2>
<p>Khai trương ngày 27/09/2006 tại Hải Phòng, chỉ sáu tháng sau PHATECO đã được DNV chứng nhận ISO 9001 và được VR, DNV, ABS, NK, BV, RINA phê duyệt nghiệp vụ. Từ đóng tàu, chúng tôi mở rộng sang dầu khí, nhiệt điện, lọc hóa dầu – và năm 2023–2024 chế tạo phao neo một thân thế hệ mới đầu tiên của Việt Nam cho mỏ Đại Hùng.</p>
<ul class="checks"><li>Không thỏa hiệp với sai lệch tiêu chuẩn</li><li>An toàn và môi trường là tiêu chí hàng đầu</li><li>Chuyên gia ASNT Level III, API, AWS CWI, CSWIP, IRATA</li></ul>
<a class="btn btn-outline" href="/gioi-thieu/">Về PHATECO</a></div>
<div>{video()}</div>
</div></section>

<section class="section"><div class="wrap split">
<img src="{UP}2026/10/aT7500303-scaled.jpg" alt="Tập thể PHATECO dịp kỷ niệm 20 năm" loading="lazy">
<div><span class="eyebrow">Tuyển dụng</span><h2>Làm việc ở những công trình lớn nhất Việt Nam</h2>
<p>PHATECO luôn tuyển kỹ thuật viên NDT, kỹ sư cơ khí, điện – tự động hóa, kỹ sư dự án và nhân viên kinh doanh. Bạn được đào tạo, thi chứng chỉ quốc tế và có lộ trình lên Level III, quản lý dự án.</p>
<a class="btn btn-red" href="/tuyen-dung/#ung-tuyen">Ứng tuyển ngay</a> <a class="btn btn-outline" href="/tuyen-dung/">Vì sao chọn PHATECO</a></div>
</div></section>
{CTA}'''
    layout('', 'PHATECO – Kiểm tra NDT, giám định, giám sát chất lượng và đào tạo kỹ thuật',
           'PHATECO: 20 năm dịch vụ kiểm tra không phá hủy (NDT), khảo sát, giám sát chất lượng, chế tạo cơ khí, đào tạo – chứng nhận cho năng lượng, dầu khí, hàng hải.', body)

# ---------- Giới thiệu ----------
TIMELINE = [
    ('31/08/2006', 'Được cấp Giấy chứng nhận đăng ký kinh doanh, thành lập công ty (tiền thân là Công ty Cổ phần Dịch vụ Kỹ thuật Phà Rừng); vốn Nhà nước chi phối 51%.'),
    ('27/09/2006', 'Lễ khai trương tại Hải Phòng – ngày truyền thống của PHATECO.'),
    ('30/01/2007', 'DNV chứng nhận ISO 9001; cùng giai đoạn được VR, DNV, ABS, NK, BV, RINA phê duyệt nghiệp vụ.'),
    ('2007–2008', 'Mở văn phòng đại diện tại TP. Hồ Chí Minh (19/04/2007), Vũng Tàu (02/05/2008), Hà Nội (06/06/2008).'),
    ('2010–2014', 'Vốn Nhà nước giảm còn 29% (2010); từ 04/08/2014 toàn bộ vốn thuộc cổ đông cá nhân.'),
    ('Từ 2008 đến nay', 'Mở rộng sang dầu khí, nhiệt điện, lọc hóa dầu: Nghi Sơn 1 & 2, Thái Bình 1, Mông Dương 1 & 2, Hải Phòng 2, Vũng Áng 1, Duyên Hải 3 MR, Vĩnh Tân 4 MR, Lọc hóa dầu Nghi Sơn, Lọc dầu Dung Quất, giàn Hải Thạch, Mộc Tinh, Đại Hùng.'),
    ('2022', 'Nâng cấp toàn diện xưởng cơ khí Vũng Tàu tại KCN Đông Xuyên.'),
    ('2023–2024', 'Liên danh với Công ty đóng tàu Phà Rừng chế tạo phao neo một thân thế hệ mới đầu tiên trong nước cho mỏ Đại Hùng; giải thưởng đổi mới sáng tạo và bằng khen cấp trung ương.'),
    ('Gần đây', 'Nhiệt điện Vũng Áng 2 (Doosan – Samsung), Quảng Trạch 1 (EVN), Vân Phong 1 (Sumitomo).'),
    ('2026', 'Đưa vào hoạt động xưởng Nghi Sơn. Kỷ niệm 20 năm thành lập.'),
]

def build_about():
    tl = ''.join(f'<li><strong>{d}</strong> – {html.escape(t)}</li>' for d, t in TIMELINE)
    body = page_hero('Về PHATECO', 'Công ty dịch vụ kỹ thuật Việt Nam chuyên kiểm tra không phá hủy, giám định – khảo sát, giám sát chất lượng, đào tạo – chứng nhận và chế tạo cơ khí.', crumbs(('', 'Giới thiệu'))) + f'''
<section class="section"><div class="wrap split">
<div><span class="eyebrow">Chúng tôi là ai</span><h2>Ở đâu có công trình cần chất lượng cao, ở đó có PHATECO</h2>
<p>Công ty Cổ phần Dịch vụ Kỹ thuật PHATECO (tiền thân là Công ty Cổ phần Dịch vụ Kỹ thuật Phà Rừng) được cấp đăng ký kinh doanh ngày 31/08/2006 và khai trương ngày 27/09/2006 tại Hải Phòng. Chỉ sáu tháng sau, hệ thống quản lý chất lượng ISO 9001 và các phê duyệt nghiệp vụ của VR, DNV, ABS, NK, BV, RINA đã được chứng nhận.</p>
<p>Từ đóng tàu và hàng hải, PHATECO sớm mở rộng sang dầu khí, nhiệt điện và lọc hóa dầu – những lĩnh vực đòi hỏi chất lượng khắt khe và an toàn tuyệt đối. Hôm nay, chúng tôi có văn phòng tại Hải Phòng, Hà Nội, TP. Hồ Chí Minh, Vũng Tàu, xưởng cơ khí KCN Đông Xuyên và xưởng Nghi Sơn.</p></div>
<div>{video()}</div></div></section>
<section class="section alt"><div class="wrap">
<div class="grid g3">
<div class="icon-card"><h3>Tầm nhìn</h3><p>Trở thành thương hiệu uy tín, có sự khác biệt nổi trội với vị thế cạnh tranh đứng đầu trong ngành dịch vụ kỹ thuật, nhờ năng lực cốt lõi là nguồn nhân lực, sản phẩm và dịch vụ chất lượng cao.</p></div>
<div class="icon-card"><h3>Sứ mệnh</h3><p>Mang lại giá trị cao nhất cho khách hàng và lợi ích tốt nhất cho nhân viên; đóng góp vào một xã hội ổn định và một nền kinh tế bền vững.</p></div>
<div class="icon-card"><h3>Triết lý kinh doanh</h3><p>Đoàn kết – Hợp tác – Phát triển và Cùng thành công.</p></div>
</div></div></section>
<section class="section"><div class="wrap split">
<div><span class="eyebrow">Vì sao khách hàng chọn PHATECO</span><h2>Năng lực được kiểm chứng độc lập</h2>
<ul class="checks">
<li><strong>Không thỏa hiệp với sai lệch tiêu chuẩn</strong> – điều làm nên uy tín PHATECO suốt 20 năm.</li>
<li><strong>Được công nhận độc lập</strong> – ISO 9001:2015 (DNV), 8 tổ chức đăng kiểm phê duyệt, VILAS 404 / LAS-XD 269, chương trình chứng nhận ISO/IEC 17024.</li>
<li><strong>Chuyên gia chứng chỉ quốc tế</strong> – ASNT NDT Level III, API 510/570/653, AWS CWI, CSWIP 3.1, PCN, IRATA.</li>
<li><strong>Một đầu mối, nhiều năng lực</strong> – kiểm tra, thử nghiệm, giám sát, chế tạo, sửa chữa.</li>
<li><strong>Vì con người và cộng đồng</strong> – phụng dưỡng Mẹ Việt Nam anh hùng, quỹ sinh viên nghèo vượt khó Đại học Hàng hải Việt Nam, ủng hộ đồng bào vùng thiên tai.</li>
</ul></div>
<div id="lich-su"><span class="eyebrow">Lịch sử</span><h2>20 năm phát triển</h2><ul class="timeline">{tl}</ul></div>
</div></section>
<section class="section alt"><div class="wrap center"><span class="eyebrow">Quản trị</span><h2>Hội đồng quản trị và Ban kiểm soát</h2>
<p class="lead">Chủ tịch HĐQT: Ông Trịnh Văn Ngư · Thành viên HĐQT: Bà Nguyễn Thị Ngọc Quỳnh, Ông Trần Văn Vượng · Trưởng Ban kiểm soát: Bà Vũ Thị Thu Hiền · Thành viên BKS: Bà Nguyễn Thị Nguyệt, Ông Nguyễn Đức Dũng.</p></div></section>
{CTA}'''
    layout('gioi-thieu/', 'Giới thiệu PHATECO – 20 năm dịch vụ kỹ thuật', 'Công ty CP Dịch vụ Kỹ thuật PHATECO: thành lập 2006 tại Hải Phòng, ISO 9001 DNV từ 2007, 8 tổ chức đăng kiểm phê duyệt.', body)

# ---------- Dịch vụ ----------
def build_services():
    body = page_hero('Dịch vụ', 'Kiểm tra, giám định, giám sát chất lượng, chế tạo và đào tạo – theo tiêu chuẩn ASME, API, AWS, ISO và quy phạm đăng kiểm.', crumbs(('', 'Dịch vụ'))) + f'''
<section class="section"><div class="wrap"><div class="grid g3">''' + ''.join(
        f'<a class="card" href="/dich-vu/{s}/"><img src="{img}" alt="{html.escape(n)}" loading="lazy"><div class="body"><h3>{n}</h3><p>{sh}</p><span class="more">Chi tiết →</span></div></a>'
        for s, n, sh, img, ic in SERVICES) + f'</div></div></section>{CTA}'
    layout('dich-vu/', 'Dịch vụ – PHATECO', 'Dịch vụ NDT, khảo sát, đo chiều dày, chế tạo cơ khí, phòng thí nghiệm, đào tạo NDT, hàn, tư vấn giám sát, tiếp cận IRATA.', body)
    side = ''.join(f'<li><a href="/dich-vu/{s}/" class="__{s}">{n}</a></li>' for s, n, *_ in SERVICES)
    for slug, name, short, img, ic in SERVICES:
        content = open(os.path.join(ROOT, 'src/pages/dich-vu', slug + '.html'), encoding='utf-8').read()
        sd = side.replace(f'class="__{slug}"', 'class="active"')
        sd = re.sub(r' class="__[^"]+"', '', sd)
        body = page_hero(name, short, crumbs(('dich-vu/', 'Dịch vụ'), ('', name))) + f'''
<section class="section"><div class="wrap layout">
<aside class="side"><h4>Dịch vụ</h4><ul>{sd}</ul><div class="box"><h4 style="color:#fff">Cần báo giá?</h4><p>Kỹ sư PHATECO phản hồi với phương án và báo giá phù hợp.</p><a class="btn btn-red" href="/lien-he/#bao-gia">Yêu cầu báo giá</a></div></aside>
<article class="content">{content}{STEPS}</article>
</div></section>{CTA}'''
        layout(f'dich-vu/{slug}/', f'{name} – PHATECO', short, body)

# ---------- Dự án ----------
def build_projects():
    filters = '<div class="filters"><button class="on" data-f="all">Tất cả</button><button data-f="dien">Nhiệt điện</button><button data-f="dau-khi">Dầu khí</button><button data-f="hang-hai">Hàng hải</button><button data-f="co-khi">Chế tạo</button><button data-f="tu-van">Tư vấn ASME</button></div>'
    body = page_hero('Dự án', 'Một số dự án tiêu biểu PHATECO đã và đang thực hiện. Danh mục đầy đủ (khoảng 70 dự án) tại phateco.com.', crumbs(('', 'Dự án'))) + f'''
<section class="section"><div class="wrap">{filters}<div class="grid g3">{proj_cards(PROJECTS)}</div>
<p style="margin-top:28px"><a class="btn btn-outline" href="https://phateco.com/du-an/" target="_blank" rel="noopener">Xem toàn bộ dự án trên phateco.com</a></p></div></section>{CTA}'''
    layout('du-an/', 'Dự án – PHATECO', 'Dự án tiêu biểu của PHATECO: nhiệt điện Vũng Áng 2, Quảng Trạch 1, Nghi Sơn; lọc dầu Dung Quất; phao neo Đại Hùng; FPSO.', body)
    dh = f'''<table class="ptc-table"><tbody>
<tr><td style="width:30%"><strong>Khách hàng</strong></td><td>Chi nhánh Điều hành Dầu khí trong nước (PVEP POC) – Tổng Công ty Thăm dò Khai thác Dầu khí (PVEP), Petrovietnam</td></tr>
<tr><td><strong>Địa điểm</strong></td><td>Mỏ Đại Hùng, Lô 05-1(a), ngoài khơi Việt Nam</td></tr>
<tr><td><strong>Hình thức</strong></td><td>PHATECO liên danh với Công ty đóng tàu Phà Rừng</td></tr>
<tr><td><strong>Thời gian</strong></td><td>2023–2024</td></tr>
<tr><td><strong>Phạm vi</strong></td><td>Thi công, chế tạo đóng mới hệ thống phao neo một thân (CALM buoy) cho tàu chứa dầu</td></tr>
<tr><td><strong>Ghi nhận</strong></td><td>Giải thưởng đổi mới sáng tạo và bằng khen cấp trung ương</td></tr></tbody></table>
<img src="{UP}2025/11/Phao-Calm.jpg" alt="Phao neo một thân mỏ Đại Hùng" style="border-radius:14px;margin:8px 0 24px">
<h2>Ý nghĩa của dự án</h2><p>Đây là phao neo một thân thế hệ mới đầu tiên được chế tạo trực tiếp trong nước, cho thấy năng lực của doanh nghiệp Việt Nam trong chế tạo thiết bị dầu khí ngoài khơi đòi hỏi tiêu chuẩn cao nhất.</p>
<h2>Vai trò của PHATECO</h2><p>PHATECO kết hợp năng lực chế tạo với nền tảng kiểm tra, giám sát chất lượng: hệ thống ISO 9001:2015 (DNV), đội ngũ NDT và thanh tra hàn có chứng chỉ quốc tế, cùng kinh nghiệm khảo sát các giàn Đại Hùng 01, Đại Hùng 02 và phao CALM trước đó.</p>
<p>Xem thêm: <a href="https://phateco.com/le-cat-ton-dong-moi-phao-neo-cho-tau-chua-dau-mo-dai-hung-lo-05-1a/">Lễ cắt tôn đóng mới phao neo</a> · <a href="/dich-vu/co-khi-che-tao-sua-chua/">Dịch vụ chế tạo, sửa chữa cơ khí</a></p>'''
    body = page_hero('Phao neo một thân thế hệ mới cho mỏ Đại Hùng', 'Phao neo thế hệ mới đầu tiên được chế tạo trong nước · PVEP POC · 2023–2024', crumbs(('du-an/', 'Dự án'), ('', 'Phao neo Đại Hùng'))) + f'<section class="section"><div class="wrap"><article class="content">{dh}</article></div></section>{CTA}'
    layout('du-an/phao-neo-dai-hung/', 'Phao neo một thân mỏ Đại Hùng – PHATECO', 'PHATECO liên danh Phà Rừng chế tạo phao neo một thân thế hệ mới đầu tiên trong nước cho mỏ Đại Hùng.', body)

# ---------- Năng lực ----------
def build_capability():
    appr = ''.join(f'<tr><td>{n}</td><td>{s}</td></tr>' for n, s in APPROVALS)
    body = page_hero('Năng lực & chứng nhận', 'Hệ thống chất lượng, phê duyệt đăng kiểm và công nhận độc lập – nền tảng để khách hàng yên tâm giao dự án.', crumbs(('', 'Năng lực'))) + f'''
<section class="section"><div class="wrap split" style="align-items:start">
<div><span class="eyebrow">Hệ thống quản lý chất lượng</span><h2>ISO 9001:2015 – DNV</h2>
<table class="ptc-table"><tbody>
<tr><td><strong>Số chứng chỉ</strong></td><td>C813459</td></tr><tr><td><strong>Chứng nhận lần đầu</strong></td><td>30/01/2007</td></tr>
<tr><td><strong>Hiệu lực</strong></td><td>02/12/2026 – 30/09/2029</td></tr><tr><td><strong>Tổ chức cấp</strong></td><td>DNV – Business Assurance (Hà Lan)</td></tr></tbody></table>
<a class="btn btn-red" href="{UP}2026/11/CC-ISO-9001-2015-30.09.29.pdf" target="_blank" rel="noopener">Xem chứng chỉ (PDF)</a></div>
<div><h3>Phạm vi chứng nhận</h3><ul class="checks">
<li>Dịch vụ kiểm tra không phá hủy (NDT)</li><li>Khảo sát và đo chiều dày thành trong lĩnh vực tàu biển và công nghiệp</li><li>Giám sát chế tạo và lắp đặt thiết bị công nghiệp</li><li>Đào tạo thợ hàn</li><li>Thử nghiệm cơ tính vật liệu xây dựng</li><li>Thẩm định và chứng nhận quy trình hàn</li><li>Chế tạo kết cấu thép và hệ thống đường ống cho dầu khí, hàng hải và công nghiệp</li><li>Thương mại thiết bị, linh kiện, vật tư cho hàng hải, dầu khí và nhiệt điện</li></ul></div>
</div></section>
<section class="section alt"><div class="wrap split" style="align-items:start">
<div><span class="eyebrow">Phê duyệt đăng kiểm</span><h2>8 tổ chức đăng kiểm phê duyệt dịch vụ</h2>
<table class="ptc-table"><thead><tr><th>Tổ chức</th><th>Dịch vụ được phê duyệt</th></tr></thead><tbody>{appr}</tbody></table>
<p style="font-size:14px;color:var(--muted)">NDT: kiểm tra không phá hủy · UTM: đo chiều dày bằng siêu âm · RIT: tiếp cận bằng dây. Số chứng nhận và thời hạn: <a href="https://phateco.com/chung-chi-cong-ty/" target="_blank" rel="noopener">phateco.com/chung-chi-cong-ty</a>.</p></div>
<div><span class="eyebrow">Công nhận khác</span><h2>Phòng thí nghiệm & chương trình chứng nhận</h2>
<ul class="checks"><li><strong>VILAS 404</strong> – phòng thí nghiệm ISO/IEC 17025</li><li><strong>LAS-XD 269</strong> – phòng thí nghiệm chuyên ngành xây dựng</li><li><strong>PNIC</strong> – trung tâm chứng nhận NDT do BoA công nhận theo ISO/IEC 17024</li><li><strong>VICAS 055-PER</strong> – chương trình chứng nhận thợ hàn ISO/IEC 17024</li><li><strong>ASNT Corporate Partner</strong></li></ul>
<h3 style="margin-top:28px">Đội ngũ chuyên gia</h3><p>ASNT NDT Level III, ACCP Level III, ISO 9712 Level 3, PCN, API 510/570/653/936, AWS CWI, CSWIP 3.1, IRATA, Petzl PPE Verifier.</p></div>
</div></section>{CTA}'''
    layout('nang-luc/', 'Năng lực & chứng nhận – PHATECO', 'ISO 9001:2015 DNV C813459; phê duyệt DNV, BV, ABS, ClassNK, LR, KR, RINA, VR; VILAS 404; PNIC ISO/IEC 17024.', body)

# ---------- Tuyển dụng ----------
JOBS = [
    ('Kỹ thuật viên NDT – khảo sát – đo chiều dày', 'Dự án toàn quốc', 'https://phateco.com/tuyen-dung-nhan-vien-ky-thuat-ndt-khao-sat/'),
    ('Nhân viên kỹ thuật chuyên nghiệp', 'Dự án toàn quốc', 'https://phateco.com/tuyen-dung-nhan-vien-ky-thuat-chuyen-nghiep/'),
    ('Kỹ sư cơ khí', 'Vũng Tàu', 'https://phateco.com/phateco-can-tuyen-ky-su-co-khi-lam-viec-tai-vung-tau/'),
    ('Kỹ sư dự án – Phòng Thương mại', 'Hà Nội', 'https://phateco.com/tuyen-dung-ky-su-du-an-phong-thuong-mai/'),
    ('Nhân viên kỹ thuật C&I – Phòng Thương mại', 'Hà Nội', 'https://phateco.com/tuyen-dung-nhan-vien-ky-thuat-ci-phong-thuong-mai/'),
    ('Nhân viên Marketing', 'Hải Phòng', 'https://phateco.com/tuyen-dung-nhan-vien-marketing-lam-viec-tai-hai-phong/'),
    ('Nhân viên kinh doanh', 'Hải Phòng', 'https://phateco.com/tuyen-dung-nhan-vien-kinh-doanh-nam-2026/'),
    ('Nhân viên hỗ trợ kinh doanh', 'Hà Nội', 'https://phateco.com/tuyen-dung-nhan-vien-ho-tro-kinh-doanh/'),
]

def build_careers():
    jobs = ''.join(f'<a class="card" href="{u}" target="_blank" rel="noopener"><div class="body"><span class="tag">{loc}</span><h3>{t}</h3><span class="more">Xem mô tả công việc →</span></div></a>' for t, loc, u in JOBS)
    form = '''<form class="f" data-cf7="2236" enctype="multipart/form-data">
<label>Họ tên *<input name="your-name" required autocomplete="name"></label>
<label>Email *<input type="email" name="your-email" required autocomplete="email"></label>
<label>Điện thoại *<input type="tel" name="your-phone" required autocomplete="tel"></label>
<label>Vị trí ứng tuyển *<select name="your-position" required><option>Kỹ thuật viên NDT / khảo sát / đo chiều dày</option><option>Kỹ sư cơ khí / đóng tàu</option><option>Kỹ sư điện – tự động hóa (C&amp;I)</option><option>Kỹ sư dự án – Phòng Thương mại</option><option>Nhân viên kinh doanh</option><option>Nhân viên Marketing</option><option>Vị trí khác</option></select></label>
<label>Nơi làm việc mong muốn<select name="your-location"><option>Hải Phòng</option><option>Hà Nội</option><option>TP. Hồ Chí Minh</option><option>Vũng Tàu</option><option>Nghi Sơn</option><option>Đi dự án toàn quốc</option></select></label>
<label>Chứng chỉ hiện có<input name="your-certs" placeholder="NDT Level, CWI, CSWIP, IRATA, API…"></label>
<label class="full">Giới thiệu ngắn<textarea name="your-message"></textarea></label>
<label class="full">CV (PDF, Word, ảnh – tối đa 10 MB) *<input type="file" name="your-cv" required accept=".pdf,.doc,.docx,.jpg,.jpeg,.png"></label>
<div class="full"><button class="btn btn-red" type="submit">Gửi hồ sơ ứng tuyển</button></div>
<div class="form-msg"></div></form>'''
    body = page_hero('Nghề nghiệp tại PHATECO', 'Làm việc ở những công trình lớn nhất Việt Nam và được đào tạo để trở thành chuyên gia có chứng chỉ quốc tế. PHATECO luôn tuyển dụng – hồ sơ được nhận thường xuyên.', crumbs(('', 'Tuyển dụng'))) + f'''
<section class="section"><div class="wrap">
<div class="grid g3">
<div class="icon-card"><div class="ic">{icon('ship')}</div><h3>Dự án thật, quy mô lớn</h3><p>Nhiệt điện, lọc hóa dầu, giàn khoan, tàu biển – học nghề từ những công trình đòi hỏi tiêu chuẩn cao nhất.</p></div>
<div class="icon-card"><div class="ic">{icon('cap')}</div><h3>Đào tạo &amp; chứng chỉ quốc tế</h3><p>NDT ASNT / ISO 9712 Level 1, 2; API Inspector; CWI, CSWIP – qua PNIC và chương trình đào tạo của PHATECO.</p></div>
<div class="icon-card"><div class="ic">{icon('gauge')}</div><h3>Lộ trình rõ ràng</h3><p>Kỹ thuật viên → Level 2 → trưởng nhóm, chuyên gia Level III, quản lý dự án.</p></div>
<div class="icon-card"><div class="ic">{icon('box')}</div><h3>Thu nhập ổn định</h3><p>Lương cứng cả thời gian chờ việc, lương dự án, phụ cấp đi biển, lương tháng 13, thưởng hiệu quả, thâm niên.</p></div>
<div class="icon-card"><div class="ic">{icon('clip')}</div><h3>Quan tâm người lao động</h3><p>Bảo hiểm đầy đủ, đúng hạn; quà lễ Tết, sinh nhật, hiếu hỉ; du lịch hàng năm.</p></div>
<div class="icon-card"><div class="ic">{icon('rope')}</div><h3>An toàn là trên hết</h3><p>Huấn luyện an toàn, bảo hộ đầy đủ; thiết bị làm việc trên cao được kiểm định bởi người có chứng chỉ.</p></div>
</div></div></section>
<section class="section alt"><div class="wrap"><span class="eyebrow">Vị trí thường xuyên tuyển</span><h2>Cơ hội đang mở</h2><div class="grid g4" style="margin-top:20px">{jobs}</div></div></section>
<section class="section" id="ung-tuyen"><div class="wrap split" style="align-items:start">
<div><span class="eyebrow">Ứng tuyển trực tuyến</span><h2>Gửi hồ sơ cho PHATECO</h2><p>Điền thông tin và đính kèm CV – Phòng Hành chính Tổ chức sẽ liên hệ khi hồ sơ phù hợp.</p>
<ol class="timeline"><li><strong>Gửi hồ sơ</strong> – qua form này hoặc email admin@phateco.com</li><li><strong>Sàng lọc</strong> – liên hệ hồ sơ phù hợp</li><li><strong>Phỏng vấn</strong> – trao đổi chuyên môn, có thể kiểm tra tay nghề</li><li><strong>Nhận việc</strong> – ký hợp đồng, đào tạo hội nhập và an toàn</li></ol></div>
<div>{form}</div></div></section>'''
    layout('tuyen-dung/', 'Tuyển dụng – Nghề nghiệp tại PHATECO', 'PHATECO luôn tuyển kỹ thuật viên NDT, kỹ sư cơ khí, C&I, kỹ sư dự án, kinh doanh. Đào tạo chứng chỉ quốc tế, lộ trình Level III.', body)

# ---------- Liên hệ ----------
def build_contact():
    opts = ''.join(f'<option>{n}</option>' for _, n, *__ in SERVICES) + '<option>Khác</option>'
    form = f'''<form class="f" data-cf7="2189" enctype="multipart/form-data">
<label>Họ tên *<input name="your-name" required autocomplete="name"></label>
<label>Công ty<input name="your-company" autocomplete="organization"></label>
<label>Email *<input type="email" name="your-email" required autocomplete="email"></label>
<label>Điện thoại *<input type="tel" name="your-phone" required autocomplete="tel"></label>
<label>Dịch vụ cần báo giá<select name="your-service">{opts}</select></label>
<label>Địa điểm và thời gian dự kiến<input name="your-location"></label>
<label class="full">Mô tả phạm vi công việc *<textarea name="your-message" required></textarea></label>
<label class="full">Tài liệu đính kèm (bản vẽ, ITP, hồ sơ mời thầu – tối đa 10 MB)<input type="file" name="your-file" accept=".pdf,.doc,.docx,.xls,.xlsx,.jpg,.jpeg,.png,.zip"></label>
<div class="full"><button class="btn btn-red" type="submit">Gửi yêu cầu báo giá</button></div>
<div class="form-msg"></div></form>'''
    body = page_hero('Liên hệ & yêu cầu báo giá', 'Hãy cho chúng tôi biết công việc bạn cần – kỹ sư PHATECO sẽ liên hệ lại với phương án và báo giá phù hợp.', crumbs(('', 'Liên hệ'))) + f'''
<section class="section" id="bao-gia"><div class="wrap split" style="align-items:start">
<div><span class="eyebrow">Yêu cầu báo giá</span><h2>Gửi yêu cầu cho kỹ sư PHATECO</h2>{form}</div>
<div><span class="eyebrow">Liên hệ nhanh</span><h2>Trụ sở chính Hải Phòng</h2><p>Số 5A/613 Đường Thiên Lôi, Phường An Biên, TP. Hải Phòng</p><p><a class="btn btn-red" href="tel:+842253870870">Gọi 0225 3 870 870</a> <a class="btn btn-outline" href="mailto:admin@phateco.com">admin@phateco.com</a></p>
<iframe title="Bản đồ trụ sở PHATECO" src="https://www.google.com/maps?q=5A%2F613+Thi%C3%AAn+L%C3%B4i+H%E1%BA%A3i+Ph%C3%B2ng&output=embed" style="width:100%;height:300px;border:0;border-radius:14px;margin-top:12px" loading="lazy"></iframe></div>
</div></section>
<section class="section alt"><div class="wrap"><span class="eyebrow">Văn phòng và cơ sở</span><h2>5 địa điểm trên cả nước</h2>{offices_html()}</div></section>'''
    layout('lien-he/', 'Liên hệ & yêu cầu báo giá – PHATECO', 'Gửi yêu cầu báo giá dịch vụ NDT, khảo sát, chế tạo, đào tạo. Trụ sở Hải Phòng, văn phòng Hà Nội, TP.HCM, Vũng Tàu.', body)

# ---------- English ----------
def build_en():
    svc_en = [('Non-destructive testing (NDT)', 'Conventional and advanced NDT: PAUT, TOFD, ECT, LRUT and more.'),
              ('Survey & inspection', 'Lifting equipment, pressure equipment, fitness-for-service.'),
              ('Close-up survey & thickness measurement', 'To DNV, LR, ABS, ClassNK, BV, KR, RINA and VR rules.'),
              ('Fabrication, repair & maintenance', 'Steel structures, piping, pressure vessels, offshore repair.'),
              ('Laboratory (VILAS 404)', 'Mechanical testing of materials and weld specimens.'),
              ('NDT training & certification', 'ISO 9712 / SNT-TC-1A through our PNIC centre.'),
              ('Welding technology & welder certification', 'ISO/IEC 17024 welder certification, WPS/PQR, PWHT.'),
              ('Project management & supervision', 'Fabrication and installation supervision, CWI / CSWIP inspectors.'),
              ('Trading & technical solutions', 'Equipment, C&I, spare parts and chemicals for power plants.'),
              ('Access services', 'IRATA rope access, rafting and scaffolding.')]
    cards = ''.join(f'<div class="icon-card"><div class="ic">{icon(SERVICES[i][4])}</div><h3>{n}</h3><p>{d}</p></div>' for i, (n, d) in enumerate(svc_en))
    feat = ''.join(f'<div class="card"><img src="{img}" alt="{n}" loading="lazy"><div class="body"><h3>{n}</h3><p>{d}</p></div></div>' for n, d, img in [
        ('Vung Ang 2 Thermal Power', 'NDT and PAUT for Doosan – Samsung JV', UP + '2025/11/ND-VA2.jpg'),
        ('Quang Trach 1 Thermal Power', 'NDT services · Owner: EVN', UP + '2025/11/ND-QT-1.jpg'),
        ('Dai Hung CALM buoy', 'First new-generation CALM buoy built in Vietnam · PVEP POC', UP + '2025/11/Phao-Calm.jpg')])
    logos = ''.join(f'<img src="{u}" alt="{n}" loading="lazy">' for n, u in PARTNER_LOGOS)
    body = f'''
<section class="hero" style="background-image:url('{HERO}')"><div class="wrap">
<span class="eyebrow" style="color:#ffb3b5">PHATECO · Since 2006</span>
<h1>Inspection, testing and engineering services for projects that cannot afford to fail</h1>
<p>NDT, survey, quality supervision, fabrication, training and certification for energy, oil and gas, marine and industrial projects across Vietnam.</p>
<div class="btns"><a class="btn btn-red" href="#contact">Request a quote</a><a class="btn btn-ghost" href="#services">Our services</a></div>
</div></section>
<div class="wrap"><div class="stats"><div><strong>20 yrs</strong><span>Founded 2006, Hai Phong</span></div><div><strong>8</strong><span>Classification societies approve our services</span></div><div><strong>ISO 9001</strong><span>Certified by DNV since 2007</span></div><div><strong>5</strong><span>Offices and facilities</span></div></div></div>
<section class="section"><div class="wrap center"><span class="eyebrow">Approved by</span><h2>Classification societies and accreditation bodies</h2><div class="logos">{logos}</div></div></section>
<section class="section alt" id="services"><div class="wrap"><span class="eyebrow">Services</span><h2>One partner for testing, supervision and fabrication</h2><div class="grid g3" style="margin-top:24px">{cards}</div></div></section>
<section class="section" id="projects"><div class="wrap"><span class="eyebrow">Selected projects</span><h2>Trusted on Vietnam’s key projects</h2><div class="grid g3" style="margin-top:24px">{feat}</div>
<p style="margin-top:20px">Clients include PVN, EVN, Vinachem, VIMC, SBIC, Vinacomin, Doosan, Hyundai, JEL and Modec.</p></div></section>
<section class="section alt"><div class="wrap split"><div><span class="eyebrow">20 years of PHATECO</span><h2>Trust, solidarity and cooperation</h2><p>Opened on 27 September 2006 in Hai Phong (formerly Pha Rung Technical Services JSC), PHATECO obtained DNV ISO 9001 certification and class approvals within six months, then expanded from shipbuilding into oil and gas, thermal power and refining.</p></div><div>{video('PHATECO 20 years')}</div></div></section>
<section class="section" id="contact"><div class="wrap"><div class="band"><div><h2>Request a quote</h2><p>Email your scope of work, location and schedule to admin@phateco.com or call +84 225 3 870 870.</p></div><div><a class="btn btn-red" href="mailto:admin@phateco.com?subject=Request%20for%20quotation">Email us</a> <a class="btn btn-ghost" href="tel:+842253870870">+84 225 3 870 870</a></div></div></div></section>'''
    layout('en/', 'PHATECO – Inspection, NDT and Engineering Services in Vietnam', 'PHATECO Technical Services JSC: NDT, inspection, quality supervision, fabrication, training and certification since 2006. ISO 9001 (DNV).', body, lang='en')

def build_404():
    body = page_hero('Không tìm thấy trang', 'Trang bạn tìm có thể đã đổi địa chỉ. Hãy quay lại trang chủ hoặc liên hệ PHATECO.') + CTA
    layout('404/', 'Không tìm thấy trang – PHATECO', 'Trang không tồn tại', body)
    t = open(os.path.join(OUT, '404', 'index.html'), encoding='utf-8').read().replace('="../', '="/')
    open(os.path.join(OUT, '404.html'), 'w', encoding='utf-8').write(t)  # 404 gốc dùng đường dẫn tuyệt đối (chạy ở tên miền gốc)

def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(ROOT, 'assets'), os.path.join(OUT, 'assets'))
    build_home(); build_about(); build_services(); build_projects(); build_capability(); build_careers(); build_contact(); build_en(); build_404()
    urls = ''.join(f'<url><loc>{SITE}{p}</loc><lastmod>{TODAY}</lastmod></url>' for p in PAGES if not p.startswith('404'))
    open(os.path.join(OUT, 'sitemap.xml'), 'w').write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nDisallow: /\n# Bản thử nghiệm: chặn Google lập chỉ mục để không trùng nội dung với phateco.com.\n# Khi chính thức thay thế: đổi thành "Allow: /" và thêm Sitemap: {SITE}sitemap.xml\n')
    open(os.path.join(OUT, '.nojekyll'), 'w').write('')
    open(os.path.join(OUT, 'CNAME'), 'w').write('phateco.vn')
    # Chép thêm ra thư mục gốc repo để GitHub Pages chạy được dù nguồn là '/ (root)' hay '/docs'
    for name in os.listdir(OUT):
        if name == 'assets':
            continue
        src, dst = os.path.join(OUT, name), os.path.join(ROOT, name)
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy(src, dst)
    print(f'Đã sinh {len(PAGES)} trang vào docs/ và thư mục gốc')

if __name__ == '__main__':
    main()
