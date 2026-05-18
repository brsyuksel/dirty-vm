#!/usr/bin/env python3

import os
import sys
import json

DIRTY_VM_PATH = os.path.expanduser("~/.dirty-vm")
STATE_FILE = f"{DIRTY_VM_PATH}/dirty-vm.json"

if not os.path.exists(STATE_FILE):
    sys.exit(0)

if len(sys.argv) < 2:
    print("vm_name is required")
    sys.exit(1)

name = sys.argv[1]
# TODO: check if vm is running

with open(STATE_FILE, "r+", encoding="utf-8") as f:
    state = json.load(f)
    f.seek(0)

    vm = next((vm for vm in state.get("virtual_machines", []) if vm.get("name") == name), None)
    if vm is None:
        print(f"virtual machine {name} not found")
        sys.exit(0)

    disc = vm["disc"]
    cdrom = vm["cdrom"]

    if os.path.exists(disc):
        os.remove(disc)

    if os.path.exists(cdrom):
        os.remove(cdrom)

    state["virtual_machines"] = [vm for vm in state["virtual_machines"] if vm.get("name") != name]
    json.dump(state, f, indent=4, ensure_ascii=False)
    f.truncate()
