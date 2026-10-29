#!/usr/bin/env python3
"""Kiểm tra trước khi bàn giao: ảnh đủ, alt đủ, chữ chờ cập nhật, vùng đặt chữ đủ tối, dung lượng."""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, WEB, config, prompts  # noqa: E402


def main():
    cfg, pr = config(), prompts()
    out = ROOT / cfg["build"]["output_dir"]
    page = out / "index.html"
    errs, warns = [], []
    if not page.exists():
        print("✗ Chưa có dist/index.html — chạy scripts/build_page.py"); return 1
    html = page.read_text(encoding="utf-8")

    for src in sorted(set(re.findall(r'(?:src|srcset|href)="(assets/[^"]+)"', html))):
        clean_src = src.split("?")[0]
        if not (out / clean_src).exists():
            errs.append(f"Thiếu file {clean_src}")
    for tag in re.findall(r"<img\b[^>]*>", html):
        if "alt=" not in tag:
            errs.append("Ảnh thiếu thuộc tính alt: " + tag[:80])
    todo = sorted(set(re.findall(r"\[Cập nhật[^\]]*\]", html)))
    if todo:
        warns.append("Còn thông tin chờ cập nhật: " + ", ".join(todo))
    if cfg["project"].get("is_concept") and cfg["project"]["concept_note"] not in html:
        errs.append("Dự án concept nhưng chưa hiện ghi chú concept ở footer")

    rep_f = WEB / "_report.json"
    rep = json.loads(rep_f.read_text(encoding="utf-8")) if rep_f.exists() else {}
    log_f = ROOT / "assets" / "raw" / "_generation_log.json"
    log = json.loads(log_f.read_text(encoding="utf-8")) if log_f.exists() else {}
    import hashlib
    from common import find_raw
    def still_placeholder(k, v):
        f = find_raw(k)
        return v.get("provider") == "placeholder" and f is not None and hashlib.sha1(f.read_bytes()).hexdigest()[:12] == v.get("file_sha1")
    placeholders = [k for k, v in log.items() if still_placeholder(k, v)]
    if placeholders:
        warns.append(f"{len(placeholders)} ảnh đang là ảnh TẠM: {', '.join(placeholders)} — tạo ảnh thật bằng prompts/_manual_prompts.md hoặc API key")
    for k, v in rep.items():
        if v.get("text_space_luma", 0) > 0.30:
            warns.append(f"{k}: vùng đặt chữ sáng (luma {v['text_space_luma']}) — kiểm tra độ đọc của chữ")
        if v.get("kb", 0) > 600:
            warns.append(f"{k}: {v['kb']} KB — cân nhắc giảm chất lượng/kích thước")
    total = sum(f.stat().st_size for f in (out / "assets").glob("*")) / 1024 / 1024 if (out / "assets").exists() else 0

    print("── KIỂM TRA ──")
    for e in errs: print("✗", e)
    for w in warns: print("!", w)
    print(f"Tổng dung lượng ảnh: {total:.1f} MB · Số ảnh khai báo: {len(pr['images'])}")
    print("KẾT QUẢ:", "LỖI — cần sửa" if errs else ("ĐẠT (có lưu ý)" if warns else "ĐẠT"))
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
