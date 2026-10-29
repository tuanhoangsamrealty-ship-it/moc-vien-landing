# START HERE — hướng dẫn cho AI agent

> Người dùng chỉ cần nói một câu, ví dụ: **"Làm landing page theo START_HERE.md"**.
> Bạn (AI agent) đọc file này và tự thực hiện toàn bộ các bước dưới đây, **không hỏi lại** trừ những chỗ được đánh dấu ❓.

## Mục tiêu
Tạo `dist/index.html`: landing page biệt thự cao cấp 5 section theo phong cách ảnh tham chiếu `docs/reference/reference-forma-stairs.jpg`, cùng bộ ảnh đồng bộ trong `dist/assets/`.

## Bản đồ thư mục
```
project.config.json      ← tên dự án, liên hệ, màu, font, provider ảnh (sửa khi đổi dự án)
content/content.json     ← toàn bộ chữ trên trang (tiếng Việt)
prompts/images.json      ← 16 prompt ảnh (nguồn chuẩn), Style DNA, block, series
template/index.html.j2   ← HTML/CSS/JS (Jinja2): bố cục + chuyển động
scripts/                 ← run_all.py (chạy hết), generate_images.py, process_images.py, build_page.py, check.py, render_prompt_doc.py
docs/01_PLAYBOOK.md      ← lý do thiết kế, 5 section, kịch bản animation, QA
docs/02_IMAGE_PROMPTS.md ← bộ prompt dạng đọc được
assets/raw/              ← ảnh gốc (<ID>.png|jpg|webp)
assets/web/              ← ảnh đã xử lý
dist/                    ← KẾT QUẢ: index.html + assets/
```

## Quy trình (làm theo thứ tự)

### Bước 0 — Chuẩn bị
```bash
pip install -r requirements.txt        # pillow, jinja2
```
Đọc lướt `docs/01_PLAYBOOK.md` mục 3–5 để nắm câu chuyện.

**Nếu người dùng nêu dự án khác** (tên, vị trí, số liệu…): cập nhật `project.config.json` (`project.*`, `contact.*`, `is_concept`) và các chuỗi liên quan trong `content/content.json`, giữ nguyên cấu trúc JSON. Tên dự án tách thành `name_serif` (phần serif) và `name_script` (phần chữ viết tay). Nếu dự án thật thì đặt `is_concept: false` và đọc mục "Dự án thật" bên dưới.

### Bước 1 — Tạo ảnh (chọn nhánh đầu tiên phù hợp)
**A. Bạn có công cụ tạo ảnh tích hợp** (ví dụ tạo ảnh trong ChatGPT/Gemini, hoặc MCP tạo ảnh):
1. Chạy `python scripts/generate_images.py --provider manual` để xuất `prompts/_manual_prompts.md` (prompt đã ghép sẵn).
2. Tạo **H1 trước**. Sau đó tạo từng ảnh còn lại theo prompt, **đính kèm H1 làm ảnh tham chiếu phong cách** nếu công cụ cho phép.
3. Lưu đúng tên `assets/raw/<ID>.png` (H1, H1M, S2, G0, G1…G6, V1…V4, B1, F1).

**B. Có API key** trong `.env` hoặc biến môi trường (`GEMINI_API_KEY`, `OPENAI_API_KEY`, hoặc `REPLICATE_API_TOKEN`):
```bash
python scripts/generate_images.py          # provider auto, tự tạo H1 trước rồi dùng làm style reference (Gemini)
```
**C. Không có cả hai:** chạy `python scripts/generate_images.py --provider placeholder` để có ảnh tạm, rồi báo người dùng: *"Trang đã dựng bằng ảnh tạm. Để có ảnh thật, thêm API key vào `.env` (xem `.env.example`) hoặc tạo ảnh theo `prompts/_manual_prompts.md` rồi chạy lại."*

❓ Chỉ hỏi người dùng nếu họ muốn ảnh thật mà nhánh A và B đều không khả dụng.

### Bước 2 — Xử lý ảnh, dựng trang, kiểm tra
```bash
python scripts/run_all.py --skip-images     # process → build → check
```
(Hoặc chạy `python scripts/run_all.py` một lệnh cho cả Bước 1 và 2 nếu đi theo nhánh B/C.)

### Bước 3 — Tự duyệt trước khi báo xong
1. Đọc kết quả của `check.py`: phải có dòng `KẾT QUẢ: ĐẠT`. Lưu ý về ảnh tạm và `[Cập nhật …]` là chấp nhận được.
2. Nếu có trình duyệt hoặc Playwright: mở `dist/index.html` ở 1440×900 và 390×844, chụp hero, S3 (giữa đoạn ghim) và S5. Kiểm tra:
   - Tên dự án là cụm chữ lớn nhất, dấu tiếng Việt không đè nhau.
   - Ô vòm nở đều hai bên, bộ đếm 01→06 chạy đúng.
   - Không có lỗi console.
3. Xem ảnh theo checklist trong `docs/02_IMAGE_PROMPTS.md` mục 6. Ảnh nào lạc tông thì chạy `python scripts/generate_images.py --only ID --force` rồi `python scripts/run_all.py --skip-images`.

### Bước 4 — Báo cáo cho người dùng (ngắn gọn)
- Đường dẫn `dist/index.html`. Mở bằng Chrome, cần Internet để tải font và GSAP.
- Ảnh thật hay ảnh tạm, provider đã dùng.
- Những mục còn `[Cập nhật …]`.

## Quy tắc không được phá
- **Không** sửa chữ trực tiếp trong template; chữ nằm ở `content/content.json`.
- **Không** thay font khi chưa kiểm tra bộ dấu tiếng Việt (Newsreader + Allura + Manrope đã được kiểm chứng).
- Mỗi màn hình **tối đa một cụm chữ script** (`<em>`).
- Giữ màu nhấn duy nhất là caramel; không thêm màu UI mới.
- **Dự án thật** (`is_concept: false`): ảnh `product: true` (G0, V1–V4) phải là ảnh hoặc phối cảnh chính thức do người dùng cung cấp; không bịa số liệu hay giá; giữ ghi chú nguồn.
- Không xoá ghi chú concept khi `is_concept: true`.

## Lệnh nhanh
| Việc | Lệnh |
|---|---|
| Làm tất cả | `python scripts/run_all.py` |
| Chỉ dựng lại trang sau khi sửa chữ/template | `python scripts/run_all.py --skip-images` |
| Tạo lại 1–2 ảnh | `python scripts/generate_images.py --only H1,S2 --force` |
| Xem prompt cuối cùng | `python scripts/generate_images.py --dry-run --only H1` |
| Cập nhật tài liệu prompt sau khi sửa JSON | `python scripts/render_prompt_doc.py` |
