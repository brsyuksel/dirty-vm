#!/usr/bin/env python3

import os
import sys
import json
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

vm = vms["virtual_machines"][name]

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
