#!/usr/bin/env python3

import os
import sys
import json

ARCH = "amd64"

if len(sys.argv) < 2:
    sys.exit(1)

image_name = sys.argv[1]

DIRTY_VM_PATH = os.path.expanduser("~/.dirty-vm")
STATE_FILE = os.path.join(DIRTY_VM_PATH, "dirty-vm.json")

with open(STATE_FILE, "r+", encoding="utf-8") as f:
    state = json.load(f)
    if image_name not in state.get("pulled_images", {}):
        print(f"no image found for {image_name}")
        sys.exit(1)

    file_path = state["pulled_images"][image_name]["file_path"]
    os.remove(file_path)
    del state["pulled_images"][image_name]

    f.seek(0)
    json.dump(state, f, indent=4, ensure_ascii=False)
    f.truncate()
