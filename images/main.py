#!/usr/bin/env python3

import os
import sys
import json

ARCH = "amd64"

dirty_vm_path = os.path.expanduser("~/.dirty-vm")

with open(os.path.join(dirty_vm_path, "config.json")) as f:
    config = json.load(f)

with open(os.path.join(dirty_vm_path, "images.json")) as f:
    images = json.load(f)

output = []

for key in config["images"][ARCH].keys():
    output.append({
        "name": key,
        "downloaded": key in images,
        "size": images.get(key, {}).get("size", "-")
    })

if len(output) == 0:
    sys.exit(0)

headers = output[0].keys()
tabs = '\t' * 4

print(tabs.join(headers))

for row in output:
    print(tabs.join([str(v) for v in row.values()]))
