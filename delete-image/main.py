#!/usr/bin/env python3

import os
import sys
import json

if len(sys.argv) < 2:
    sys.exit(1)

image_name = sys.argv[1]

DIRTY_VM_PATH = os.path.expanduser(os.environ.get("DIRTY_VM_HOME", "~/.dirty-vm"))
STATE_FILE = os.path.join(DIRTY_VM_PATH, "dirty-vm.json")

with open(STATE_FILE, "r+", encoding="utf-8") as f:
    state = json.load(f)

    found = None
    for idx, pimg in enumerate(state.get("pulled_images", [])):
        if pimg.get("name") == image_name:
            found = idx
            break

    if found is None:
        print(f"no image found for {image_name}")
        sys.exit(1)

    file_path = state["pulled_images"][found]["file_path"]

    try:
        os.remove(file_path)
    except FileNotFoundError:
        pass

    del state["pulled_images"][found]

    f.seek(0)
    json.dump(state, f, indent=4, ensure_ascii=False)
    f.truncate()
