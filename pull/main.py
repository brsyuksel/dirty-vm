#!/usr/bin/env python3

import os
import sys
import json
import subprocess

ARCH = "amd64"

if len(sys.argv) < 2:
    sys.exit(1)

image_name = sys.argv[1]

DIRTY_VM_PATH = os.path.expanduser("~/.dirty-vm")
STATE_FILE = os.path.join(DIRTY_VM_PATH, "dirty-vm.json")

with open(STATE_FILE, "r", encoding="utf-8") as f:
    state = json.load(f)

if image_name not in state.get("images", {}).get(ARCH, {}):
    print(f"image not found: {image_name}")
    sys.exit(1)

image_url = state["images"][ARCH][image_name]
target_file = os.path.join(DIRTY_VM_PATH, "images", f"{image_name}.img")
wget_cmd = ["wget", "-O", target_file, image_url]
result = subprocess.run(wget_cmd, check=True)

if result.returncode != 0:
    sys.exit(1)

file_size = os.path.getsize(target_file)
file_size_mb = file_size / (1024 * 1024)

with open(STATE_FILE, "r+", encoding="utf-8") as f:
    state = json.load(f)
    state["pulled_images"][image_name] = {"file_path": target_file, "size": f"{file_size_mb:.2f} MB"}

    f.seek(0)
    json.dump(state, f, indent=4, ensure_ascii=False)
    f.truncate()
