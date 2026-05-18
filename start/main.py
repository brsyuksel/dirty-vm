#!/usr/bin/env python3

import os
import sys
import json
import subprocess
import platform

QEMU_BIN_MAP = {
    "amd64": "qemu-system-x86_64",
    "arm64": "qemu-system-aarch64",
}

host_arch = platform.machine()
ARCH = {"x86_64": "amd64", "aarch64": "arm64"}.get(host_arch)
if ARCH is None:
    print(f"unsupported architecture: {host_arch}")
    sys.exit(1)

QEMU_BIN = QEMU_BIN_MAP.get(ARCH)

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

if os.path.exists(vm_pid_file):
    with open(vm_pid_file, "r") as f:
        pid = f.read().strip()
    if pid:
        try:
            os.kill(int(pid), 0)
            print(f"vm {name} is already running (pid {pid})")
            sys.exit(1)
        except (ValueError, ProcessLookupError, OSError):
            pass

try:
    with open("/sys/devices/system/cpu/smt/active", "r") as f:
        threads = 2 if f.read().strip() == "1" else 1
except:
    threads = 1

qemu_cmd = [
    QEMU_BIN,
    "-enable-kvm",
    "-cpu", "host,topoext=on",
    "-smp", f"cpus={int(vm['vcpu']) * threads},sockets=1,cores={vm['vcpu']},threads={threads}",
    "-m", f"{vm['memory']}G",
    "-drive", f"file={vm['disc']},if=virtio",
    "-drive", f"file={vm['cdrom']},format=raw,if=ide,index=2,media=cdrom",
    "-nic", f"bridge,br={os.environ.get('BRIDGE_IF_NAME', 'dirtyvmbr0')},mac={vm['mac']}",
    "-display", "none",
    "-pidfile", vm_pid_file,
    "-daemonize"
]

subprocess.run(qemu_cmd, check=True)
