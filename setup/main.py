#!/usr/bin/env python3

import os
import json
import shutil
import subprocess

DIRTY_VM_PATH = os.path.expanduser(os.environ.get("DIRTY_VM_HOME", "~/.dirty-vm"))
STATE_FILE = os.path.join(DIRTY_VM_PATH, "dirty-vm.json")
TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dirty-vm.json.tpl")

os.makedirs(DIRTY_VM_PATH, exist_ok=True)
os.makedirs(os.path.join(DIRTY_VM_PATH, "images"), exist_ok=True)
os.makedirs(os.path.join(DIRTY_VM_PATH, "discs"), exist_ok=True)
os.makedirs(os.path.join(DIRTY_VM_PATH, "cdroms"), exist_ok=True)
os.makedirs(os.path.join(DIRTY_VM_PATH, "run"), exist_ok=True)

if not os.path.exists(STATE_FILE):
    with open(TEMPLATE, "r", encoding="utf-8") as f:
        template = json.load(f)

    state = {
        "images": template,
        "pulled_images": [],
        "virtual_machines": [],
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
