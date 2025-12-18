#!/usr/bin/env python3

import os
import sys
import json
import getpass
import subprocess

DIRTY_VM_PATH = os.path.expanduser("~/.dirty-vm")

if len(sys.argv) < 2:
    print("vm_name is required")
    sys.exit(1)

name = sys.argv[1]

with open(f"{DIRTY_VM_PATH}/vms.json") as f:
    vms = json.load(f)

if name not in vms["virtual_machines"]:
    print(f"virtual machine {name} not found")
    sys.exit(1)

vm_ip = vms["virtual_machines"][name]["ip"]

vm_pid = f"{DIRTY_VM_PATH}/run/{name}.pid"

if not os.path.exists(vm_pid):
    print("vm is not running")
    sys.exit(1)

user_name = getpass.getuser()
subprocess.run(["ssh", "-i", "~/.ssh/dirty-vm", f"{user_name}@{vm_ip}"], check=False)
