#!/usr/bin/env python3
"""Xử lý ảnh gốc (assets/raw) → ảnh web (assets/web).

Với mỗi ảnh trong prompts/images.json:
  1. cắt về đúng tỉ lệ (giữ tâm, hoặc theo "focus": [x, y] 0–1 nếu khai báo)
  2. resize về kích thước "target"
  3. grade chung cho cả bộ (lift blacks, saturation, warmth trong project.config.json) để đồng bộ "một giọng"
  4. xuất WebP (q82) + og.jpg 1200×630 từ ảnh hero
  5. đo độ sáng vùng dành cho chữ (TEXT_SPACE_LEFT / TEXT_SPACE_TOP / B1) và cảnh báo nếu quá sáng
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, WEB, config, find_raw, need_pillow, prompts, ratio  # noqa: E402

need_pillow()
from PIL import Image, ImageEnhance, ImageOps, ImageStat  # noqa: E402


def crop_to(im, ar, focus=(0.5, 0.5)):
    W, H = im.size
    if W / H > ar:
        w, h = int(round(H * ar)), H
    else:
        w, h = W, int(round(W / ar))
    x = int(min(max(focus[0] * W - w / 2, 0), W - w))
    y = int(min(max(focus[1] * H - h / 2, 0), H - h))
    return im.crop((x, y, x + w, y + h))


def grade(im, g):
    if g.get("saturation", 1) != 1:
        im = ImageEnhance.Color(im).enhance(g["saturation"])
    w = g.get("warmth", 0)
    lift = g.get("lift_blacks", 0)
    if w or lift:
        r, gg, b = im.split()
        r = r.point(lambda v: min(255, int(lift * 255 + v * (1 - lift) * (1 + w))))
        gg = gg.point(lambda v: min(255, int(lift * 255 + v * (1 - lift) * (1 + w * .25))))
        b = b.point(lambda v: min(255, int(lift * 255 + v * (1 - lift) * (1 - w))))
        im = Image.merge("RGB", (r, gg, b))
    return im


def region_luma(im, box):
    W, H = im.size
    reg = im.crop((int(box[0] * W), int(box[1] * H), int(box[2] * W), int(box[3] * H))).convert("L")
    return ImageStat.Stat(reg).mean[0] / 255


def main():
    cfg, pr = config(), prompts()
    WEB.mkdir(parents=True, exist_ok=True)
    g = cfg["images"].get("grade", {})
    report, missing = {}, []
    for img in pr["images"]:
        src = find_raw(img["id"])
        if not src:
            missing.append(img["id"]); continue
        im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
        im = crop_to(im, ratio(img["aspect"]), tuple(img.get("focus", (0.5, 0.5))))
        tw, th = img["target"]
        if im.width < tw * 0.6:
            print(f"! {img['id']}: ảnh gốc nhỏ ({im.width}px) — nên upscale ×2 trước khi dùng thật")
        im = im.resize((tw, th), Image.LANCZOS)
        im = grade(im, g)
        out = WEB / img["file"]
        im.save(out, "WEBP", quality=82, method=6)
        note = {"file": img["file"], "size": [tw, th], "kb": round(out.stat().st_size / 1024)}
        uses = img.get("uses", [])
        if "TEXT_SPACE_LEFT" in uses:
            note["text_space_luma"] = round(region_luma(im, (0, 0.15, 0.42, 0.85)), 3)
        elif "TEXT_SPACE_TOP" in uses:
            note["text_space_luma"] = round(region_luma(im, (0, 0, 1, 0.45)), 3)
        elif img["id"] == "B1":
            note["text_space_luma"] = round(region_luma(im, (0, 0, 0.5, 1)), 3)
        if note.get("text_space_luma", 0) > 0.30:
            print(f"! {img['id']}: vùng đặt chữ khá sáng (luma {note['text_space_luma']}) — CSS shade sẽ bù, nhưng nên tạo lại ảnh tối hơn ở vùng đó")
        report[img["id"]] = note
        if img.get("anchor"):
            crop_to(im, 1200 / 630).resize((1200, 630), Image.LANCZOS).save(WEB / "og.jpg", quality=86)
        print(f"✓ {img['id']} → assets/web/{img['file']} ({note['kb']} KB)")
    (WEB / "_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    if missing:
        print(f"\nThiếu ảnh gốc cho: {', '.join(missing)} — chạy generate_images.py hoặc đặt file vào assets/raw/")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
