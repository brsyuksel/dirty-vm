#!/usr/bin/env python3

import os
import sys
import json
import argparse
import re

DIRTY_VM_PATH = os.path.expanduser(os.environ.get("DIRTY_VM_HOME", "~/.dirty-vm"))
STATE_FILE = os.path.join(DIRTY_VM_PATH, "dirty-vm.json")

NAME_RE = re.compile(r"^[a-zA-Z0-9_-]+$")

parser = argparse.ArgumentParser()
parser.add_argument("--name", required=True, help="name of the virtual machine")
parser.add_argument("--image-name", required=True, help="name of the pulled image to use")
parser.add_argument("--vcpu", required=True, help="number of vcpu cores")
parser.add_argument("--mem", required=True, help="memory size in GB")
parser.add_argument("--disc-size", required=True, help="disc size in GB")
args = parser.parse_args()

if not NAME_RE.match(args.name):
    print("invalid vm name: use only ascii letters, numbers, underscore, dash")
    sys.exit(1)

with open(STATE_FILE, "r", encoding="utf-8") as f:
    state = json.load(f)

if any(vm.get("name") == args.name for vm in state.get("virtual_machines", [])):
    print(f"virtual machine {args.name} already exists")
    sys.exit(1)

if not any(img.get("name") == args.image_name for img in state.get("pulled_images", [])):
    print(f"no pulled image found with name {args.image_name}")
    sys.exit(1)
