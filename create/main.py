#!/usr/bin/env python3

import os
import sys
import getpass
from string import Template
from uuid import uuid4
import tempfile
import subprocess
import socket
import struct
import json
import shutil

DIRTY_VM_PATH = os.path.expanduser("~/.dirty-vm")
BRIDGE_IP = "192.168.4.1"
QEMU_MAC_ADDR = "52:54:00:00:00:00"

if len(sys.argv) < 6:
    print("not enough args")
    sys.exit(1)

(name, image_name, vcpu, mem, disc_size) = sys.argv[1:]

user_name = getpass.getuser()

with open("user-data.tpl") as f:
    user_data_template = f.read()

with open(os.path.expanduser("~/.ssh/dirty-vm.pub")) as f:
    pubkey = f.read()

user_data_content = Template(user_data_template).substitute({
    "user": user_name,
    "pubkey": pubkey,
    "vm_name": name,
    "host_ip": BRIDGE_IP,
})

with open("meta-data.tpl") as f:
    meta_data_template = f.read()

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

vms_json = f"{DIRTY_VM_PATH}/vms.json"
if not os.path.exists(vms_json):
    with open(vms_json, "w", encoding="utf-8") as f:
        f.write("{}")

with open(vms_json, "r+", encoding="utf-8") as f:
    vms = json.load(f)
    f.seek(0)

    last_mac = vms.get("mac", QEMU_MAC_ADDR)
    last_ip = vms.get("ipv4", BRIDGE_IP)

    next_mac_int = int(last_mac.replace(":", ""), 16) + 1
    next_mac_hex = f"{next_mac_int:012x}"
    next_mac = ":".join(next_mac_hex[i:i+2] for i in range(0, 12, 2))
    vms["mac"] = next_mac

    packed_ip = socket.inet_aton(last_ip)
    packed_ip_int = struct.unpack("!I", packed_ip)[0]
    next_ip_int = packed_ip_int + 1
    next_ip_packed = struct.pack("!I", next_ip_int)
    next_ip = socket.inet_ntoa(next_ip_packed)
    vms["ipv4"] = next_ip

    with open(f"{DIRTY_VM_PATH}/images.json") as f2:
        images = json.load(f2)

    image_path = images[image_name]["file_path"]
    disc_path = f"{DIRTY_VM_PATH}/discs/{name}.qcow2"
    shutil.copy(image_path, disc_path)
    qemu_img_cmd = ["qemu-img", "resize", disc_path, f"{disc_size}G"]
    result = subprocess.run(qemu_img_cmd, check=True)
    if result.returncode != 0:
        sys.exit(1)

    if "virtual_machines" not in vms:
        vms["virtual_machines"] = {}

    vms["virtual_machines"][name] = {
        "image": image_name,
        "mac": next_mac,
        "ip": next_ip,
        "disc": disc_path,
        "cdrom": cdrom_path,
        "vcpu": vcpu,
        "memory": mem,
        "disc_size": disc_size
    }
    json.dump(vms, f, indent=4, ensure_ascii=False)
    f.truncate()

dhcp_hosts = "\n".join([
    f"dhcp-host={v['mac']},{k},{v['ip']},infinite"
    for k, v in vms["virtual_machines"].items()
])

with open("dnsmasq.conf.tpl") as f:
    dnsmasq_conf = Template(f.read()).substitute({
        "dhcp_hosts": dhcp_hosts
    })

dnsmasq_conf_file = f"{DIRTY_VM_PATH}/dnsmasq.conf"
with open(dnsmasq_conf_file, "w") as f:
    f.write(dnsmasq_conf)
