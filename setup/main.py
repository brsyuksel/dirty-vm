#!/usr/bin/env python3

import os
import json
import subprocess

DIRTY_VM_PATH = os.path.expanduser("~/.dirty-vm")
STATE_FILE = os.path.join(DIRTY_VM_PATH, "dirty-vm.json")
CONFIG_TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

os.makedirs(DIRTY_VM_PATH, exist_ok=True)

with open(CONFIG_TEMPLATE, "r", encoding="utf-8") as f:
    config = json.load(f)

state = {
    "images": config.get("images", {}),
    "pulled_images": {},
    "virtual_machines": {},
    "mac": "52:54:00:00:00:00",
    "ipv4": "192.168.4.1"
}

with open(STATE_FILE, "w", encoding="utf-8") as f:
    json.dump(state, f, indent=4, ensure_ascii=False)

ssh_key_path = os.path.expanduser("~/.ssh/dirty-vm")
if not os.path.exists(ssh_key_path):
    subprocess.run(
        ["ssh-keygen", "-t", "ed25519", "-f", ssh_key_path, "-N", ""],
        check=True
    )
