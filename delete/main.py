#!/usr/bin/env python3

import os
import sys
import json

DIRTY_VM_PATH = os.path.expanduser("~/.dirty-vm")
vms_json = f"{DIRTY_VM_PATH}/vms.json"

if not os.path.exists(vms_json):
    sys.exit(0)

if len(sys.argv) < 2:
    print("vm_name is required")
    sys.exit(1)

name = sys.argv[1]
# TODO: check if vm is running

with open(vms_json, "r+", encoding="utf-8") as f:
    vms = json.load(f)
    f.seek(0)

    if name not in vms["virtual_machines"]:
        print(f"virtual machine {name} not found")
        sys.exit(0)
    
    vm = vms["virtual_machines"][name]
    disc = vm["disc"]
    cdrom = vm["cdrom"]

    if os.path.exists(disc):
        os.remove(disc)

    if os.path.exists(cdrom):
        os.remove(cdrom)
    
    del vms["virtual_machines"][name]
    json.dump(vms, f, indent=4, ensure_ascii=False)
    f.truncate()
