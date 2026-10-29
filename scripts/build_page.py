#!/usr/bin/env python3
"""Dựng trang: project.config.json + content/content.json + template/index.html.j2 → dist/index.html
   và chép ảnh web vào dist/assets/."""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, WEB, config, load_json, prompts  # noqa: E402

try:
    from jinja2 import Environment, FileSystemLoader, StrictUndefined
except ImportError:
    sys.exit("Thiếu thư viện Jinja2. Chạy: pip install -r requirements.txt")


def render_strings(obj, env, ctx):
    """Cho phép dùng {{ project.* }} / {{ contact.* }} ngay trong content.json."""
    if isinstance(obj, str):
        return env.from_string(obj).render(**ctx) if "{{" in obj else obj
    if isinstance(obj, list):
        return [render_strings(x, env, ctx) for x in obj]
    if isinstance(obj, dict):
        return {k: render_strings(v, env, ctx) for k, v in obj.items() if not k.startswith("_")}
    return obj


def main():
    cfg = config()
    content = load_json("content/content.json")
    pr = prompts()
    env = Environment(loader=FileSystemLoader(str(ROOT)), autoescape=False, undefined=StrictUndefined,
                      trim_blocks=False, lstrip_blocks=False)
    env.filters["tojson"] = lambda v: json.dumps(v, ensure_ascii=False)
    c = render_strings(content, env, {"project": cfg["project"], "contact": cfg["contact"]})
    out_dir = ROOT / cfg["build"]["output_dir"]
    (out_dir / "assets").mkdir(parents=True, exist_ok=True)
    copied = 0
    for f in WEB.glob("*"):
        if f.suffix.lower() in (".webp", ".jpg", ".png", ".svg"):
            shutil.copy2(f, out_dir / "assets" / f.name); copied += 1

    import hashlib
    def versioned(fname: str) -> str:
        p = out_dir / "assets" / fname
        h = hashlib.sha1(p.read_bytes()).hexdigest()[:8] if p.exists() else "1"
        return f"assets/{fname}?v={h}"

    img = {i["id"]: versioned(i["file"]) for i in pr["images"]}
    html = env.get_template(cfg["build"]["template"]).render(cfg=cfg, c=c, img=img)
    (out_dir / "index.html").write_text(html, encoding="utf-8")
    print(f"✓ Đã dựng {out_dir.relative_to(ROOT)}/index.html · {copied} ảnh trong {out_dir.relative_to(ROOT)}/assets/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
