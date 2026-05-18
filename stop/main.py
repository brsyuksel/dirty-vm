#!/usr/bin/env python3

import os
import sys
import json
import subprocess

DIRTY_VM_PATH = os.path.expanduser("~/.dirty-vm")
STATE_FILE = f"{DIRTY_VM_PATH}/dirty-vm.json"

if len(sys.argv) < 2:
    print("vm_name is required")
    sys.exit(1)

name = sys.argv[1]

with open(STATE_FILE, "r", encoding="utf-8") as f:
    state = json.load(f)

vm = next((vm for vm in state.get("virtual_machines", []) if vm.get("name") == name), None)
if vm is None:
    print(f"virtual machine {name} not found")
    sys.exit(1)

vm_pid_file = f"{DIRTY_VM_PATH}/run/{name}.pid"

if not os.path.exists(vm_pid_file):
    print("vm is not running")
    sys.exit(1)

with open(vm_pid_file, "r") as f:
    vm_pid = f.read().strip()

subprocess.run(["kill", "-9", str(vm_pid)], check=False)
