#!/usr/bin/env python3

import os
import sys
import getpass
import tempfile
import subprocess
import socket
import struct
import json
import shutil
from string import Template
from uuid import uuid4

DIRTY_VM_PATH = os.path.expanduser(os.environ.get("DIRTY_VM_HOME", "~/.dirty-vm"))
STATE_FILE = os.path.join(DIRTY_VM_PATH, "dirty-vm.json")
BRIDGE_IF_NAME = os.environ.get("BRIDGE_IF_NAME", "dirtyvmbr0")
DNS_UPSTREAM = os.environ.get("DNS_UPSTREAM", "1.1.1.1")

if len(sys.argv) < 6:
    print("usage: dirty-vm create <name> <image_name> <vcpu> <mem> <disc_size>")
    sys.exit(1)

(name, image_name, vcpu, mem, disc_size) = sys.argv[1:6]

user_name = getpass.getuser()

with open("user-data.tpl") as f:
    user_data_template = f.read()

with open(os.path.expanduser("~/.ssh/dirty-vm.pub")) as f:
    pubkey = f.read()

with open("meta-data.tpl") as f:
    meta_data_template = f.read()

with open(STATE_FILE, "r", encoding="utf-8") as f:
    state = json.load(f)

bridge_ip = state.get("ipv4", "192.168.4.1")
base_mac = state.get("mac", "52:54:00:00:00:00")

user_data_content = Template(user_data_template).substitute({
    "user": user_name,
    "pubkey": pubkey,
    "vm_name": name,
    "host_ip": bridge_ip,
})

vm_uuid = str(uuid4())
meta_data_content = Template(meta_data_template).substitute({
    "instance_id": f"{name}-{vm_uuid}",
    "vm_name": name
})

with tempfile.TemporaryDirectory() as temp_dir:
    user_data_path = os.path.join(temp_dir, "user-data")
    with open(user_data_path, "w", encoding="utf-8") as f:
        f.write(user_data_content)

    meta_data_path = os.path.join(temp_dir, "meta-data")
    with open(meta_data_path, "w", encoding="utf-8") as f:
        f.write(meta_data_content)

    cdrom_path = os.path.join(DIRTY_VM_PATH, "cdroms", f"{name}_cloud_init.iso")
    mkisofs_cmd = [
        "mkisofs",
        "-output", cdrom_path,
        "-V", "cidata",
        "-r",
        "-J",
        temp_dir,
    ]

    result = subprocess.run(mkisofs_cmd, check=True)
    if result.returncode != 0:
        sys.exit(1)

with open(STATE_FILE, "r+", encoding="utf-8") as f:
    state = json.load(f)
    f.seek(0)

    last_mac = state.get("mac", base_mac)
    last_ip = state.get("ipv4", bridge_ip)

    next_mac_int = int(last_mac.replace(":", ""), 16) + 1
    next_mac_hex = f"{next_mac_int:012x}"
    next_mac = ":".join(next_mac_hex[i:i+2] for i in range(0, 12, 2))
    state["mac"] = next_mac

    packed_ip = socket.inet_aton(last_ip)
    packed_ip_int = struct.unpack("!I", packed_ip)[0]
    next_ip_int = packed_ip_int + 1
    next_ip_packed = struct.pack("!I", next_ip_int)
    next_ip = socket.inet_ntoa(next_ip_packed)
    state["ipv4"] = next_ip

    image_path = None
    for img in state.get("pulled_images", []):
        if img.get("name") == image_name:
            image_path = img["file_path"]
            break

    if image_path is None:
        print(f"image {image_name} not found")
        sys.exit(1)

    disc_path = os.path.join(DIRTY_VM_PATH, "discs", f"{name}.qcow2")
    try:
        shutil.copy(image_path, disc_path)
    except OSError as e:
        print(f"failed to copy image: {e}")
        sys.exit(1)

    qemu_img_cmd = ["qemu-img", "resize", disc_path, f"{disc_size}G"]
    result = subprocess.run(qemu_img_cmd, check=True)
    if result.returncode != 0:
        if os.path.exists(disc_path):
            os.remove(disc_path)
        sys.exit(1)

    if "virtual_machines" not in state:
        state["virtual_machines"] = []

    state["virtual_machines"].append({
        "name": name,
        "image": image_name,
        "mac": next_mac,
        "ip": next_ip,
        "disc": disc_path,
        "cdrom": cdrom_path,
        "vcpu": vcpu,
        "memory": mem,
        "disc_size": disc_size
    })
    json.dump(state, f, indent=4, ensure_ascii=False)
    f.truncate()

dhcp_hosts = "\n".join([
    f"dhcp-host={v['mac']},{v['name']},{v['ip']},infinite"
    for v in state["virtual_machines"]
])

with open("dnsmasq.conf.tpl") as f:
    dnsmasq_conf = Template(f.read()).substitute({
        "interface": BRIDGE_IF_NAME,
        "upstream": DNS_UPSTREAM,
        "dhcp_hosts": dhcp_hosts
    })

dnsmasq_conf_file = os.path.join(DIRTY_VM_PATH, "dnsmasq.conf")
with open(dnsmasq_conf_file, "w") as f:
    f.write(dnsmasq_conf)
