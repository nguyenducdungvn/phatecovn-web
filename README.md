# PHATECO – website thử nghiệm (phateco.vn)

Bản thử nghiệm giao diện mới cho Công ty CP Dịch vụ Kỹ thuật PHATECO. Website **tĩnh** (HTML/CSS/JS thuần), không cần cơ sở dữ liệu, chạy được trên GitHub Pages hoặc bất kỳ hosting nào.

- Nội dung lấy từ phateco.com (bản đã viết lại tháng 11/2026) và clip "PHATECO 20 năm".
- Ảnh và logo đang **dẫn trực tiếp từ phateco.com** (`wp-content/uploads`), nên phateco.com phải còn hoạt động.
- Form "Yêu cầu báo giá" và "Ứng tuyển" gửi về **Contact Form 7 trên phateco.com** (form số 2189 và 2236) → email về admin@phateco.com, có đính kèm file.
- Đang **chặn Google lập chỉ mục** (`robots.txt` + thẻ `noindex`) để không trùng nội dung với phateco.com trong thời gian thử.

## Cấu trúc

```
build.py                 # sinh toàn bộ trang vào docs/
src/pages/dich-vu/*.html # nội dung 10 trang dịch vụ
assets/css/site.css      # giao diện
assets/js/site.js        # menu điện thoại, lọc dự án, gửi form, Google Analytics
assets/js/config.js      # cấu hình: mã Google Analytics, máy chủ nhận form
docs/                    # KẾT QUẢ – đây là thư mục đem lên hosting
```

Trang đã có: Trang chủ · Giới thiệu (kèm lịch sử 20 năm, video) · Dịch vụ + 10 trang dịch vụ · Dự án (có bộ lọc) · Case study phao neo Đại Hùng · Năng lực & chứng nhận · Tuyển dụng (form ứng tuyển có CV) · Liên hệ (form báo giá, bản đồ, 5 văn phòng) · Trang chủ tiếng Anh · 404.

## Sửa nội dung

1. Sửa chữ trong `build.py` (trang chủ, giới thiệu, dự án, tuyển dụng…) hoặc `src/pages/dich-vu/<tên>.html` (trang dịch vụ).
2. Chạy `python3 build.py` (Python 3.8+, không cần cài thêm gì).
3. Commit cả thư mục `docs/`.

## Chạy thử

### Cách 1 – GitHub Pages (xem ngay, không cần tên miền)
Settings → Pages → *Build and deployment*: Source = **Deploy from a branch**, Branch = **main**, thư mục **/docs** → Save.
Sau 1–2 phút: `https://nguyenducdungvn.github.io/phatecovn-web/`

### Cách 2 – Gắn tên miền phateco.vn vào GitHub Pages
1. Settings → Pages → *Custom domain*: nhập `phateco.vn` → Save (GitHub tự tạo file `docs/CNAME`).
2. Tại nơi quản lý DNS của phateco.vn (hiện là Turbify), tạo bản ghi:
   - `A` @ → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `CNAME` www → `nguyenducdungvn.github.io`
3. Chờ DNS cập nhật (vài phút đến vài giờ), quay lại Settings → Pages bật **Enforce HTTPS**.

> Lưu ý: nếu phateco.vn đang chuyển hướng về phateco.com hoặc đang dùng cho email, kiểm tra kỹ các bản ghi hiện có (MX, TXT) trước khi sửa – chỉ thay bản ghi A/CNAME của website.

### Cách 3 – Hosting riêng
Tải toàn bộ nội dung thư mục `docs/` lên thư mục web của tên miền (ví dụ `public_html` trong DirectAdmin).

## Google Analytics

Mở `assets/js/config.js`, điền mã đo lường GA4 (dạng `G-XXXXXXXXXX`) vào `gaId`, chạy lại `python3 build.py`. Site sẽ tự đo lượt xem và các hành động: bấm gọi điện, bấm email, bấm "Yêu cầu báo giá", gửi form.

## Khi chuyển thành website chính thức

- Sửa `docs/robots.txt` thành `Allow: /` (sửa trong hàm `main()` của `build.py`) và bỏ thẻ `noindex` trong `layout()`.
- Bỏ dải thông báo "Bản thử nghiệm" (`notice-test`) trong `layout()`.
- Chép ảnh về thư mục `assets/img/` thay cho dẫn link từ phateco.com.
