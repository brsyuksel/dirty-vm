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

with open(os.path.join(dirty_vm_path, "images.json"), "r+", encoding="utf-8") as f:
    images = json.load(f)
    if image_name not in images:
        print(f"no image found for {image_name}")
        sys.exit(1)

    file_path = images[image_name]["file_path"]
    os.remove(file_path)
    del images[image_name]

    f.seek(0)
    json.dump(images, f, indent=4, ensure_ascii=False)
    f.truncate()
