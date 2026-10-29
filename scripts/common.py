"""Tiện ích dùng chung cho các script của kit."""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "assets" / "raw"
WEB = ROOT / "assets" / "web"
RAW_EXTS = (".png", ".jpg", ".jpeg", ".webp")


def load_json(rel):
    with open(ROOT / rel, encoding="utf-8") as f:
        return json.load(f)


def config():
    return load_json("project.config.json")


def prompts():
    return load_json("prompts/images.json")


def ratio(aspect: str) -> float:
    a, b = aspect.split(":")
    return float(a) / float(b)


def find_raw(img_id: str):
    """Trả về file ảnh gốc của một ID (bất kỳ đuôi nào) hoặc None."""
    for ext in RAW_EXTS:
        p = RAW / f"{img_id}{ext}"
        if p.exists():
            return p
    return None


def compose_prompt(img: dict, pr: dict) -> str:
    """Ghép prompt cuối cùng: nội dung → bố cục → block → series → style DNA → avoid."""
    parts = [img["prompt"].strip()]
    if img.get("composition"):
        parts.append("COMPOSITION — " + img["composition"].strip())
    for b in img.get("uses", []):
        parts.append(pr["blocks"][b])
    if img.get("series"):
        parts.append(pr["series"][img["series"]])
    parts.append(pr["style_dna"])
    parts.append("Avoid: " + pr["negative"])
    return "\n\n".join(parts)


def ordered_images(pr: dict):
    """Ảnh neo (anchor) luôn đứng đầu."""
    imgs = pr["images"]
    return sorted(imgs, key=lambda i: 0 if i.get("anchor") else 1)


def need_pillow():
    try:
        import PIL  # noqa: F401
    except ImportError:
        sys.exit("Thiếu thư viện Pillow. Chạy: pip install -r requirements.txt")


def env(*names):
    for n in names:
        v = os.environ.get(n)
        if v:
            return v
    return None
