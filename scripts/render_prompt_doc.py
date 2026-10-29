#!/usr/bin/env python3
"""Sinh lại docs/02_IMAGE_PROMPTS.md từ prompts/images.json (chạy sau mỗi lần sửa prompt)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, compose_prompt, prompts  # noqa: E402

HEAD = """# Bộ prompt tạo ảnh · Mộc Viên

> **Nguồn chuẩn:** `prompts/images.json`. File này được sinh tự động bởi `scripts/render_prompt_doc.py`, nên đừng sửa tay. Muốn đổi prompt thì sửa JSON rồi chạy lại script.
> Mục tiêu: 16 ảnh trông như **một buổi chụp duy nhất**, ấm và tĩnh như ảnh tham chiếu.

## 1. Quy trình để cả bộ ảnh "một giọng"

1. **Tạo H1 trước** (ảnh neo màu). Tạo 3–4 phương án, chọn bản có: nửa trái tối, cầu thang liền mạch, ánh nắng ấm.
2. **Dùng H1 làm ảnh tham chiếu phong cách** cho mọi ảnh sau:
   - Gemini (`gemini-2.5-flash-image`): script tự đính kèm H1, chỉ lấy *màu, ánh sáng, vật liệu*, không lấy bố cục.
   - Midjourney: thêm `--sref <URL ảnh H1>` và `--style raw`.
   - ChatGPT / GPT-Image: đính kèm H1 kèm câu "match the colour grade, light and material palette of the attached image; do not copy its composition".
3. **Khoá series:** V1–V4 dùng chung `VILLA_SERIES` (cùng góc máy, cùng giờ, cùng bầu trời); G1–G6 dùng chung `ROOM_SERIES`. Tạo các ảnh trong cùng một series liên tiếp nhau.
4. **Grade chung:** `process_images.py` áp cùng một mức lift blacks / saturation / warmth (chỉnh trong `project.config.json → images.grade`).
5. **Kiểm tra:** đặt 16 ảnh cạnh nhau. Ảnh nào "lạc tông" thì tạo lại với `--only ID --force`.

## 2. Cấu trúc một prompt

```
[Nội dung cảnh]  →  COMPOSITION — [bố cục, chỗ chừa cho chữ]  →  [block: HANDS / TEXT_SPACE / BLEND_CREAM]
→  [SERIES LOCK nếu có]  →  STYLE DNA  →  Avoid: [negative]
```

Script ghép tự động theo đúng thứ tự trên. Phần **Prompt cuối cùng** ở mỗi ảnh bên dưới là bản đã ghép, dán thẳng vào công cụ tạo ảnh là dùng được.

## 3. Các khối dùng chung
"""


def main():
    pr = prompts()
    out = [HEAD]
    out.append("### STYLE DNA (ghép vào mọi ảnh)\n```text\n" + pr["style_dna"] + "\n```\n")
    out.append("### NEGATIVE (ghép vào mọi ảnh)\n```text\n" + pr["negative"] + "\n```\n")
    for k, v in pr["blocks"].items():
        out.append(f"### Block `{k}`\n```text\n{v}\n```\n")
    for k, v in pr["series"].items():
        out.append(f"### Series `{k}`\n```text\n{v}\n```\n")
    out.append("## 4. Danh sách ảnh\n")
    out.append("| ID | File web | Section | Tỉ lệ | Xuất (px) | Ảnh sản phẩm |\n|---|---|---|---|---|---|")
    for i in pr["images"]:
        out.append(f"| **{i['id']}** | `{i['file']}` | {i['section']} | {i['aspect']} | {i['target'][0]}×{i['target'][1]} | {'có — dự án thật phải dùng ảnh chính thức' if i.get('product') else '—'} |")
    out.append("\n## 5. Prompt từng ảnh\n")
    for i in pr["images"]:
        out.append(f"### {i['id']} · {i['section']}" + (" · ảnh neo màu" if i.get("anchor") else ""))
        out.append(f"- Lưu ảnh gốc: `assets/raw/{i['id']}.png` · Tỉ lệ **{i['aspect']}**")
        if i.get("uses"):
            out.append("- Block: " + ", ".join(f"`{u}`" for u in i["uses"]))
        if i.get("series"):
            out.append(f"- Series: `{i['series']}`")
        out.append("- Kiểm tra sau khi tạo: " + " · ".join(i.get("checks", [])))
        out.append("\n**Cảnh:** " + i["prompt"])
        if i.get("composition"):
            out.append("\n**Bố cục:** " + i["composition"])
        out.append("\n<details><summary>Prompt cuối cùng (đã ghép)</summary>\n\n```text\n" + compose_prompt(i, pr) + "\n```\n</details>\n")
    out.append("""## 6. Tiêu chí duyệt ảnh (chấm 1–5, cần ≥ 4 ở mọi mục)

| Tiêu chí | Câu hỏi |
|---|---|
| Ánh sáng | Có phải nắng chiều ấm, bóng trong, highlight mềm không? |
| Vật liệu | Gỗ sồi mật ong, travertine, vôi kem, kim loại đen mảnh. Có lẫn vật liệu lạ không? |
| Bố cục | Có chừa đúng vùng cho chữ như yêu cầu không? |
| Hình học | Đường đứng có thẳng không? Bậc thang, vòm, hồ bơi có hợp lý không? |
| Đồng bộ | Đặt cạnh H1 có thấy cùng một buổi chụp không? |
| Sạch | Có chữ, logo, watermark hay vật thừa không? |
""")
    (ROOT / "docs" / "02_IMAGE_PROMPTS.md").write_text("\n".join(out), encoding="utf-8")
    print("✓ docs/02_IMAGE_PROMPTS.md")


if __name__ == "__main__":
    main()
