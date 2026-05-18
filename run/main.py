#!/usr/bin/env python3

import os
import sys
import json
import getpass
import subprocess

DIRTY_VM_PATH = os.path.expanduser("~/.dirty-vm")
STATE_FILE = f"{DIRTY_VM_PATH}/dirty-vm.json"

if len(sys.argv) < 4:
    print("vm_name is required")
    sys.exit(1)

name = sys.argv[1]

with open(STATE_FILE, "r", encoding="utf-8") as f:
    state = json.load(f)

if name not in state["virtual_machines"]:
    print(f"virtual machine {name} not found")
    sys.exit(1)

vm_ip = state["virtual_machines"][name]["ip"]

vm_pid = f"{DIRTY_VM_PATH}/run/{name}.pid"

if not os.path.exists(vm_pid):
    print("vm is not running")
    sys.exit(1)

user_name = getpass.getuser()
cmd = ["ssh", "-i", "~/.ssh/dirty-vm", f"{user_name}@{vm_ip}", " ".join(sys.argv[3:])]
subprocess.run(cmd, check=False)
