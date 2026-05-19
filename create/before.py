#!/usr/bin/env python3

import os

DIRTY_VM_PATH = os.path.expanduser(os.environ.get("DIRTY_VM_HOME", "~/.dirty-vm"))

os.makedirs(os.path.join(DIRTY_VM_PATH, "run"), exist_ok=True)
os.makedirs(os.path.join(DIRTY_VM_PATH, "discs"), exist_ok=True)
os.makedirs(os.path.join(DIRTY_VM_PATH, "cdroms"), exist_ok=True)
