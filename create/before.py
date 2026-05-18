#!/usr/bin/env python3

import os
import sys
import json
import shutil
import subprocess

DIRTY_VM_PATH = os.path.expanduser("~/.dirty-vm")
STATE_FILE = f"{DIRTY_VM_PATH}/dirty-vm.json"

subprocess.run(["bash", "../check/validate.sh"], check=True)

if len(sys.argv) < 6:
    print("not enough args")
    sys.exit(1)

if not shutil.which("mkisofs"):
    print("mkisofs is not found")
    sys.exit(1)

if not os.path.exists(f"{DIRTY_VM_PATH}/run"):
    os.mkdir(f"{DIRTY_VM_PATH}/run")

if not os.path.exists(f"{DIRTY_VM_PATH}/discs"):
    os.mkdir(f"{DIRTY_VM_PATH}/discs")

if not os.path.exists(f"{DIRTY_VM_PATH}/cdroms"):
    os.mkdir(f"{DIRTY_VM_PATH}/cdroms")

with open(STATE_FILE, "r", encoding="utf-8") as f:
    state = json.load(f)

name = sys.argv[1]
if any(vm.get("name") == name for vm in state.get("virtual_machines", [])):
    print(f"virtual machine {name} already exists")
    sys.exit(1)

image_name = sys.argv[2]
if not any(img.get("name") == image_name for img in state.get("pulled_images", [])):
    print(f"no pulled image found with name {image_name}")
    sys.exit(1)
