#!/usr/bin/env python3
"""Sinh toàn bộ ảnh của landing page từ prompts/images.json.

Cách dùng:
  python scripts/generate_images.py                     # provider = cấu hình (mặc định auto)
  python scripts/generate_images.py --provider gemini   # gemini | openai | replicate | placeholder | manual
  python scripts/generate_images.py --only H1,S2 --force
  python scripts/generate_images.py --dry-run           # chỉ in prompt cuối cùng

Provider "auto": dùng provider đầu tiên có API key trong .env hoặc biến môi trường
  GEMINI_API_KEY (hoặc GOOGLE_API_KEY) → gemini
  OPENAI_API_KEY                      → openai
  REPLICATE_API_TOKEN                 → replicate
  không có key nào                    → placeholder (ảnh tạm có nhãn) + xuất prompts/_manual_prompts.md
Provider "manual": chỉ xuất prompts/_manual_prompts.md để AI có công cụ tạo ảnh tích hợp
  (hoặc con người) tự tạo ảnh và lưu vào assets/raw/<ID>.png.
"""
import argparse
import base64
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, RAW, compose_prompt, config, find_raw, ordered_images, prompts, ratio  # noqa: E402


# ---------------------------------------------------------------- .env
def load_dotenv():
    f = ROOT / ".env"
    if not f.exists():
        return
    for line in f.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def key_for(provider):
    return {
        "gemini": os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"),
        "openai": os.environ.get("OPENAI_API_KEY"),
        "replicate": os.environ.get("REPLICATE_API_TOKEN"),
    }.get(provider)


# ---------------------------------------------------------------- HTTP
def http_json(url, payload, headers, timeout=300):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json", **headers}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "ignore")[:800]
        raise RuntimeError(f"HTTP {e.code} từ {url.split('?')[0]}: {body}") from None


def http_get_json(url, headers, timeout=60):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def download(url, timeout=120):
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return r.read()


# ---------------------------------------------------------------- providers
def gen_gemini(img, text, cfg, anchor_path):
    model = cfg["images"]["gemini_model"]
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    parts = []
    if anchor_path is not None:
        mime = "image/png" if anchor_path.suffix == ".png" else "image/jpeg" if anchor_path.suffix in (".jpg", ".jpeg") else "image/webp"
        parts.append({"inlineData": {"mimeType": mime, "data": base64.b64encode(anchor_path.read_bytes()).decode()}})
        text = ("The attached photograph is a STYLE REFERENCE only: match its colour grade, light quality, "
                "warmth and material palette. Do NOT copy its composition, subject or layout.\n\n" + text)
    parts.append({"text": text})
    payload = {
        "contents": [{"role": "user", "parts": parts}],
        "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": img["aspect"]}},
    }
    res = http_json(url, payload, {"x-goog-api-key": key_for("gemini")})
    for cand in res.get("candidates", []):
        for p in cand.get("content", {}).get("parts", []):
            blob = p.get("inlineData") or p.get("inline_data")
            if blob and blob.get("data"):
                return base64.b64decode(blob["data"]), ".png"
    raise RuntimeError("Gemini không trả về ảnh: " + json.dumps(res)[:600])


def gen_openai(img, text, cfg, anchor_path):
    r = ratio(img["aspect"])
    size = "1536x1024" if r > 1.2 else "1024x1536" if r < 0.85 else "1024x1024"
    payload = {"model": cfg["images"]["openai_model"], "prompt": text[:31000], "size": size,
               "quality": cfg["images"].get("openai_quality", "high"), "n": 1}
    res = http_json("https://api.openai.com/v1/images/generations", payload,
                    {"Authorization": f"Bearer {key_for('openai')}"})
    d = res["data"][0]
    if d.get("b64_json"):
        return base64.b64decode(d["b64_json"]), ".png"
    if d.get("url"):
        return download(d["url"]), ".png"
    raise RuntimeError("OpenAI không trả về ảnh")


REPLICATE_RATIOS = ["1:1", "16:9", "3:2", "2:3", "4:5", "5:4", "9:16", "3:4", "4:3"]


def gen_replicate(img, text, cfg, anchor_path):
    model = cfg["images"]["replicate_model"]
    want = ratio(img["aspect"])
    ar = min(REPLICATE_RATIOS, key=lambda a: abs(ratio(a) - want))
    headers = {"Authorization": f"Bearer {key_for('replicate')}", "Prefer": "wait"}
    res = http_json(f"https://api.replicate.com/v1/models/{model}/predictions",
                    {"input": {"prompt": text, "aspect_ratio": ar, "output_format": "png", "safety_tolerance": 2}}, headers)
    t0 = time.time()
    while res.get("status") not in ("succeeded", "failed", "canceled"):
        if time.time() - t0 > 300:
            raise RuntimeError("Replicate quá thời gian chờ")
        time.sleep(3)
        res = http_get_json(res["urls"]["get"], {"Authorization": headers["Authorization"]})
    if res.get("status") != "succeeded":
        raise RuntimeError("Replicate lỗi: " + str(res.get("error")))
    out = res["output"]
    url = out[0] if isinstance(out, list) else out
    return download(url), ".png"


def gen_placeholder(img, text, cfg, anchor_path):
    """Ảnh tạm có thẩm mỹ gần bảng màu, ghi ID + vai trò — để dựng và duyệt bố cục khi chưa có ảnh thật."""
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
    W, H = img["target"]
    W, H = min(W, 1600), int(min(W, 1600) * H / W)
    c = cfg["brand"]["colors"]
    hx = lambda h: tuple(int(h.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    dark, mid, light = hx(c["espresso"]), hx(c["caramel_deep"]), hx(c["caramel"])
    if "BLEND_CREAM" in img.get("uses", []):
        dark, mid, light = hx(c["card"]), hx("#E9DDD0"), hx("#D9C6B1")
    im = Image.new("RGB", (W, H), dark)
    px = im.load()
    seed = int(hashlib.md5(img["id"].encode()).hexdigest()[:6], 16)
    cx = 0.62 + ((seed % 20) - 10) / 100
    cy = 0.55
    if "TEXT_SPACE_TOP" in img.get("uses", []):
        cy = 0.75
    for y in range(H):
        for x in range(0, W, 2):
            d = ((x / W - cx) ** 2 * 1.4 + (y / H - cy) ** 2) ** 0.5
            t = max(0.0, 1 - d * 1.6)
            if "TEXT_SPACE_LEFT" in img.get("uses", []) or img["id"] == "B1":
                t *= min(1.0, max(0.0, (x / W - 0.25) / 0.35))
            col = tuple(int(dark[i] + (mid[i] - dark[i]) * min(1, t * 1.4) + (light[i] - mid[i]) * max(0, t - 0.55)) for i in range(3))
            px[x, y] = col
            if x + 1 < W:
                px[x + 1, y] = col
    im = im.filter(ImageFilter.GaussianBlur(2))
    dr = ImageDraw.Draw(im)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", max(16, W // 40))
        small = ImageFont.truetype("DejaVuSans.ttf", max(12, W // 75))
    except OSError:
        font = small = ImageFont.load_default()
    on = (40, 30, 22) if "BLEND_CREAM" in img.get("uses", []) else (243, 236, 228)
    dr.text((W * 0.66, H * 0.80), f"{img['id']} · placeholder", fill=on, font=font)
    dr.text((W * 0.66, H * 0.80 + W // 30), img["section"], fill=on, font=small)
    import io
    buf = io.BytesIO()
    im.save(buf, "PNG")
    return buf.getvalue(), ".png"


PROVIDERS = {"gemini": gen_gemini, "openai": gen_openai, "replicate": gen_replicate, "placeholder": gen_placeholder}


# ---------------------------------------------------------------- manual export
def write_manual(pr, imgs):
    out = ROOT / "prompts" / "_manual_prompts.md"
    lines = ["# Prompt cuối cùng — tạo thủ công (đã ghép sẵn Style DNA)", "",
             "Lưu mỗi ảnh vào `assets/raw/<ID>.png` (hoặc .jpg/.webp). Tạo **H1 trước**, rồi đính kèm H1 làm ảnh tham chiếu phong cách cho các ảnh còn lại.", ""]
    for img in imgs:
        lines += [f"## {img['id']} — {img['section']}", f"- Lưu thành: `assets/raw/{img['id']}.png`", f"- Tỉ lệ: **{img['aspect']}** · Xuất tối thiểu {img['target'][0]}×{img['target'][1]}px",
                  "", "```text", compose_prompt(img, pr), "```", ""]
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


# ---------------------------------------------------------------- main
def main():
    load_dotenv()
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider")
    ap.add_argument("--only", help="danh sách ID, ví dụ H1,S2")
    ap.add_argument("--force", action="store_true", help="tạo lại cả ảnh đã có")
    ap.add_argument("--allow-product-ai", action="store_true", help="cho phép AI tạo ảnh sản phẩm khi dự án là dự án THẬT")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    cfg, pr = config(), prompts()
    imgs = ordered_images(pr)
    if a.only:
        ids = {x.strip() for x in a.only.split(",")}
        imgs = [i for i in imgs if i["id"] in ids]

    provider = a.provider or cfg["images"].get("provider", "auto")
    if provider == "auto":
        provider = next((p for p in cfg["images"]["provider_order"] if key_for(p)), "placeholder")
        if provider == "placeholder":
            print("! Không tìm thấy API key tạo ảnh (GEMINI_API_KEY / OPENAI_API_KEY / REPLICATE_API_TOKEN).")
            print("  → Tạo ảnh TẠM để dựng bố cục, và xuất prompts/_manual_prompts.md để tạo ảnh thật sau.")
    print(f"Provider: {provider}")

    manual = write_manual(pr, imgs)
    if provider == "manual" or a.dry_run:
        print(f"Đã xuất prompt cuối cùng: {manual.relative_to(ROOT)}")
        if a.dry_run:
            for img in imgs:
                print(f"\n===== {img['id']} =====\n{compose_prompt(img, pr)}")
        return 0
    if provider not in PROVIDERS:
        sys.exit(f"Provider không hợp lệ: {provider}")
    if provider != "placeholder" and not key_for(provider):
        sys.exit(f"Thiếu API key cho {provider}. Thêm vào file .env (xem .env.example).")

    RAW.mkdir(parents=True, exist_ok=True)
    log_f = RAW / "_generation_log.json"
    log = json.loads(log_f.read_text(encoding="utf-8")) if log_f.exists() else {}
    anchor_id = cfg["images"].get("style_anchor_id", "H1")
    use_ref = cfg["images"].get("use_anchor_as_reference", True) and provider == "gemini"
    real_project = not cfg["project"].get("is_concept", True)
    ok, fail, skip = [], [], []

    for img in imgs:
        existing = find_raw(img["id"])
        entry = log.get(img["id"], {})
        was_placeholder = bool(existing) and entry.get("provider") == "placeholder" and \
            hashlib.sha1(existing.read_bytes()).hexdigest()[:12] == entry.get("file_sha1")
        if existing and was_placeholder and provider != "placeholder":
            existing = None  # ảnh tạm luôn được thay khi đã có provider thật
        if existing and not a.force:
            skip.append(img["id"]); continue
        if real_project and img.get("product") and not a.allow_product_ai and provider != "placeholder":
            print(f"- {img['id']}: BỎ QUA — ảnh sản phẩm của dự án thật cần phối cảnh chính thức (đặt vào assets/raw/{img['id']}.jpg)")
            skip.append(img["id"]); continue
        text = compose_prompt(img, pr)
        anchor_path = find_raw(anchor_id) if (use_ref and img["id"] != anchor_id) else None
        for attempt in range(3):
            try:
                print(f"- {img['id']}: đang tạo ({img['aspect']})…", flush=True)
                data, ext = PROVIDERS[provider](img, text, cfg, anchor_path)
                for e in (".png", ".jpg", ".jpeg", ".webp"):
                    (RAW / f"{img['id']}{e}").unlink(missing_ok=True)
                (RAW / f"{img['id']}{ext}").write_bytes(data)
                log[img["id"]] = {"provider": provider, "at": time.strftime("%Y-%m-%d %H:%M:%S"), "file_sha1": hashlib.sha1(data).hexdigest()[:12],
                                  "prompt_sha1": hashlib.sha1(text.encode()).hexdigest()[:12], "style_reference": bool(anchor_path)}
                ok.append(img["id"]); break
            except Exception as e:  # noqa: BLE001
                print(f"  lỗi lần {attempt + 1}: {e}")
                time.sleep(4 * (attempt + 1))
        else:
            fail.append(img["id"])
        log_f.write_text(json.dumps(log, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"\nXong. Tạo mới: {len(ok)} · Giữ nguyên: {len(skip)} · Lỗi: {len(fail)} {fail if fail else ''}")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
