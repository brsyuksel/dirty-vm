#!/usr/bin/env python3

import os
import sys
import json
import shutil

DIRTY_VM_PATH = os.path.expanduser("~/.dirty-vm")

if len(sys.argv) < 6:
    print("not enough args")
    sys.exit(1)

if not shutil.which("mkisofs"):
    print("mkisofs is not found")
    sys.exit(1)

if not os.path.exists(f"{DIRTY_VM_PATH}/config.json"):
    print("dirty-vm is not configured. run setup first.")
    sys.exit(1)

if not os.path.exists(f"{DIRTY_VM_PATH}/images.json"):
    print("no pulled image.")
    sys.exit(1)

if not os.path.exists(f"{DIRTY_VM_PATH}/run"):
    os.mkdir(f"{DIRTY_VM_PATH}/run")

if not os.path.exists(f"{DIRTY_VM_PATH}/discs"):
    os.mkdir(f"{DIRTY_VM_PATH}/discs")

if not os.path.exists(f"{DIRTY_VM_PATH}/cdroms"):
    os.mkdir(f"{DIRTY_VM_PATH}/cdroms")

if not os.path.exists(f"{DIRTY_VM_PATH}/vms.json"):
    with open(f"{DIRTY_VM_PATH}/vms.json", "w", encoding="utf-8") as f:
        f.write("{}")

with open(f"{DIRTY_VM_PATH}/vms.json") as f:
    vms = json.load(f)

name = sys.argv[1]
if name in vms.get("virtual_machines", {}):
    print(f"virtual machine {name} already exists")
    sys.exit(1)

with open(f"{DIRTY_VM_PATH}/images.json") as f:
    images = json.load(f)

image_name = sys.argv[2]
if image_name not in images:
    print(f"no pulled image found with name {image_name}")
    sys.exit(1)
