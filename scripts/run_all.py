#!/usr/bin/env python3
"""Chạy trọn quy trình: tạo ảnh → xử lý ảnh → dựng trang → kiểm tra.

  python scripts/run_all.py                       # provider theo cấu hình (auto)
  python scripts/run_all.py --provider placeholder
  python scripts/run_all.py --skip-images          # chỉ dựng lại trang (sau khi sửa chữ/template)
"""
import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run(name, *args):
    print(f"\n━━ {name} ━━")
    return subprocess.call([sys.executable, str(HERE / name), *args])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--skip-images", action="store_true")
    a, rest = ap.parse_known_args()
    if not a.skip_images:
        gen_args = (["--provider", a.provider] if a.provider else []) + (["--force"] if a.force else []) + rest
        if run("generate_images.py", *gen_args) != 0:
            print("! Một số ảnh lỗi — tiếp tục với ảnh đang có.")
    run("process_images.py")  # luôn xử lý lại ảnh (kể cả --skip-images) để dist/ không dùng ảnh cũ
    if run("build_page.py") != 0:
        return 1
    run("check.py")
    print("\nMở dist/index.html bằng Chrome để xem (cần Internet để tải font và thư viện chuyển động).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
