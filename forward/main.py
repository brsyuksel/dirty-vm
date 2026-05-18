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

name, vm_port, local_port = sys.argv[1], sys.argv[2], sys.argv[3]

with open(STATE_FILE, "r", encoding="utf-8") as f:
    state = json.load(f)

vm = next((vm for vm in state.get("virtual_machines", []) if vm.get("name") == name), None)
if vm is None:
    print(f"virtual machine {name} not found")
    sys.exit(1)

vm_ip = vm["ip"]

vm_pid = f"{DIRTY_VM_PATH}/run/{name}.pid"

if not os.path.exists(vm_pid):
    print("vm is not running")
    sys.exit(1)

user_name = getpass.getuser()
cmd = ["ssh", "-L", f"{local_port}:localhost:{vm_port}", "-i", "~/.ssh/dirty-vm", "-N", f"{user_name}@{vm_ip}"]
subprocess.run(cmd, check=False)
