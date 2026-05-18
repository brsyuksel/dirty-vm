#!/usr/bin/env python3

import os
import sys
import json

DIRTY_VM_PATH = os.path.expanduser("~/.dirty-vm")
STATE_FILE = f"{DIRTY_VM_PATH}/dirty-vm.json"

with open(STATE_FILE, "r", encoding="utf-8") as f:
    state = json.load(f)

virtual_machines = state.get("virtual_machines", {})

output = []

for key in virtual_machines.keys():
    machine = virtual_machines[key]
    vm = {
        "name": key,
        "ip": machine["ip"],
        "vcpu": machine["vcpu"],
        "memory": f"{machine['memory']}G",
        "disc": f"{machine['disc_size']}G",
    }
    output.append(vm)

if len(output) == 0:
    sys.exit(0)

headers = output[0].keys()

tabs = '\t' * 4
print(tabs.join(headers))

for row in output:
    print(tabs.join([str(v) for v in row.values()]))
