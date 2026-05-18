#!/usr/bin/env python3

import os
import sys
import json

DIRTY_VM_PATH = os.path.expanduser(os.environ.get("DIRTY_VM_HOME", "~/.dirty-vm"))
STATE_FILE = os.path.join(DIRTY_VM_PATH, "dirty-vm.json")

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

vm_pid_file = os.path.join(DIRTY_VM_PATH, "run", f"{name}.pid")

if not os.path.exists(vm_pid_file):
    print("vm is not running")
    sys.exit(1)

with open(vm_pid_file, "r") as f:
    vm_pid = f.read().strip()

try:
    os.kill(int(vm_pid), 9)
    os.remove(vm_pid_file)
except (ValueError, ProcessLookupError, OSError):
    os.remove(vm_pid_file)
    print("vm is not running")
    sys.exit(1)
