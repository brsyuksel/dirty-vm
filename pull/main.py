#!/usr/bin/env python3

import os
import sys
import json
import subprocess

ARCH = "amd64"

if len(sys.argv) < 2:
    sys.exit(1)

image_name = sys.argv[1]

dirty_vm_path = os.path.expanduser("~/.dirty-vm")

with open(os.path.join(dirty_vm_path, "config.json")) as f:
    config = json.load(f)

if image_name not in config["images"][ARCH]:
    print(f"image not found: {image_name}")
    sys.exit(1)

image_url = config["images"][ARCH][image_name]
target_file = os.path.join(dirty_vm_path, "images", f"{image_name}.img")
wget_cmd = ["wget", "-O", target_file, image_url]
result = subprocess.run(wget_cmd, check=True)

if result.returncode != 0:
    sys.exit(1)

file_size = os.path.getsize(target_file)
file_size_mb = file_size / (1024 * 1024)

with open(os.path.join(dirty_vm_path, "images.json"), "r+", encoding="utf-8") as f:
    images = json.load(f)
    images[image_name] = {"file_path": target_file, "size": f"{file_size_mb:.2f} MB"}

    f.seek(0)
    json.dump(images, f, indent=4, ensure_ascii=False)
    f.truncate()
