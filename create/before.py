#!/usr/bin/env python3

import os
import sys
import json
import re

DIRTY_VM_PATH = os.path.expanduser(os.environ.get("DIRTY_VM_HOME", "~/.dirty-vm"))
STATE_FILE = os.path.join(DIRTY_VM_PATH, "dirty-vm.json")

NAME_RE = re.compile(r"^[a-zA-Z0-9_-]+$")

if len(sys.argv) < 6:
    print("usage: dirty-vm create <name> <image_name> <vcpu> <mem> <disc_size>")
    sys.exit(1)

(name, image_name, vcpu, mem, disc_size) = sys.argv[1:6]

if not NAME_RE.match(name):
    print("invalid vm name: use only ascii letters, numbers, underscore, dash")
    sys.exit(1)

with open(STATE_FILE, "r", encoding="utf-8") as f:
    state = json.load(f)

if any(vm.get("name") == name for vm in state.get("virtual_machines", [])):
    print(f"virtual machine {name} already exists")
    sys.exit(1)

if not any(img.get("name") == image_name for img in state.get("pulled_images", [])):
    print(f"no pulled image found with name {image_name}")
    sys.exit(1)
