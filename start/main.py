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

try:
    with open("/sys/devices/system/cpu/smt/active", "r") as f:
        threads = 2 if f.read().strip() == "1" else 1
except:
    threads = 1

vm_pid_file = f"{DIRTY_VM_PATH}/run/{name}.pid"
qemu_cmd = [
    "qemu-system-x86_64",
    "-enable-kvm",
    "-cpu", "host,topoext=on",
    "-smp", f"cpus={int(vm['vcpu']) * threads},sockets=1,cores={vm['vcpu']},threads={threads}",
    "-m", f"{vm['memory']}G",
    "-drive", f"file={vm['disc']},if=virtio",
    "-drive", f"file={vm['cdrom']},format=raw,if=ide,index=2,media=cdrom",
    "-nic", f"bridge,br=virbr0,mac={vm['mac']}",
    "-display", "none",
    "-pidfile", vm_pid_file,
    "-daemonize"
]

subprocess.run(qemu_cmd, check=True)
