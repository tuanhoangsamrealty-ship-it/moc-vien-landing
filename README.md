# Mộc Viên · Landing Page Kit

Bộ thư mục để **một AI agent** (Claude Code, Codex, Gemini CLI, Cursor…) tự tạo ảnh và dựng landing page biệt thự cao cấp theo phong cách ảnh tham chiếu, chỉ với **một câu lệnh**:

> **Làm landing page theo START_HERE.md**

Nếu muốn đổi dự án, thêm thông tin vào câu lệnh, ví dụ:
> *Làm landing page theo START_HERE.md cho dự án "Lam Sơn Villas", biệt thự ven biển Quy Nhơn, dự án concept.*

## Có gì bên trong
| | |
|---|---|
| `START_HERE.md` | Quy trình từng bước cho AI agent |
| `docs/01_PLAYBOOK.md` | Phân tích mẫu, 8 điểm khó, hệ thiết kế, 5 section, kịch bản animation & scroll, QA |
| `docs/02_IMAGE_PROMPTS.md` | 16 prompt ảnh + quy trình đồng bộ + tiêu chí duyệt |
| `project.config.json` · `content/content.json` | Thông tin dự án và toàn bộ chữ trên trang |
| `template/index.html.j2` | Template trang (HTML/CSS/GSAP) đã kiểm thử desktop và mobile |
| `scripts/` | Tạo ảnh (Gemini / OpenAI / Replicate / thủ công / ảnh tạm), xử lý ảnh, dựng trang, kiểm tra |
| `dist/` | Kết quả: `index.html` + `assets/` |

## Tự chạy bằng tay
```bash
pip install -r requirements.txt
cp .env.example .env                     # điền 1 API key tạo ảnh (không bắt buộc)
python scripts/run_all.py                # tạo ảnh → xử lý → dựng → kiểm tra
```
Không có API key thì script tự dựng bằng ảnh tạm, đồng thời xuất `prompts/_manual_prompts.md` để anh tạo ảnh thủ công rồi lưu vào `assets/raw/<ID>.png`.

Mở `dist/index.html` bằng Chrome (cần Internet để tải font và thư viện chuyển động).
