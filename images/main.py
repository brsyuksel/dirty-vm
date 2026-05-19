#!/usr/bin/env python3

import os
import sys
import json
import platform

ARCH_MAP = {
    "x86_64": "amd64",
    "aarch64": "arm64",
}

host_arch = platform.machine()
ARCH = ARCH_MAP.get(host_arch)

if ARCH is None:
    print(f"unsupported architecture: {host_arch}")
    sys.exit(1)

DIRTY_VM_PATH = os.path.expanduser(os.environ.get("DIRTY_VM_HOME", "~/.dirty-vm"))
STATE_FILE = os.path.join(DIRTY_VM_PATH, "dirty-vm.json")

with open(STATE_FILE, "r", encoding="utf-8") as f:
    state = json.load(f)

output = []

for img in state.get("images", []):
    if img.get("arch") == ARCH:
        key = img["name"]
        size = "-"
        for pimg in state.get("pulled_images", []):
            if pimg.get("name") == key:
                size = pimg.get("size", "-")
                break
        output.append({
            "name": key,
            "downloaded": any(pimg.get("name") == key for pimg in state.get("pulled_images", [])),
            "size": size
        })

if len(output) == 0:
    sys.exit(0)

headers = output[0].keys()
tabs = '\t' * 4

print(tabs.join(headers))

for row in output:
    print(tabs.join([str(v) for v in row.values()]))
