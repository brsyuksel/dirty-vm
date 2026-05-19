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

with open(STATE_FILE, "r+", encoding="utf-8") as f:
    state = json.load(f)
    f.seek(0)

    vm = next((vm for vm in state.get("virtual_machines", []) if vm.get("name") == name), None)
    if vm is None:
        print(f"virtual machine {name} not found")
        sys.exit(1)

    vm_pid_file = os.path.join(DIRTY_VM_PATH, "run", f"{name}.pid")
    if os.path.exists(vm_pid_file):
        with open(vm_pid_file, "r") as pf:
            pid = pf.read().strip()
        if pid:
            try:
                os.kill(int(pid), 0)
                print(f"vm {name} is running. stop it first.")
                sys.exit(1)
            except (ValueError, ProcessLookupError, OSError):
                pass

    disc = vm["disc"]
    cdrom = vm["cdrom"]

    try:
        os.remove(disc)
    except FileNotFoundError:
        pass

    try:
        os.remove(cdrom)
    except FileNotFoundError:
        pass

    state["virtual_machines"] = [vm for vm in state["virtual_machines"] if vm.get("name") != name]
    json.dump(state, f, indent=4, ensure_ascii=False)
    f.truncate()
