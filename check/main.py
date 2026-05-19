#!/usr/bin/env python3

import os
import shutil
import sys


def check_binary(name):
    return shutil.which(name) is not None


def check_module(name):
    try:
        with open("/proc/modules", "r") as f:
            for line in f:
                mod = line.split()[0]
                if mod == name:
                    return True
    except FileNotFoundError:
        pass
    return False


def check_kvm_device():
    exists = os.path.exists("/dev/kvm")
    if not exists:
        return False, "device not found"
    if not os.access("/dev/kvm", os.R_OK | os.W_OK):
        return False, "permission denied (add user to kvm group)"
    return True, "KVM acceleration available"


def get_cpu_vendor():
    try:
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if line.startswith("vendor_id"):
                    return line.split(":")[1].strip()
    except FileNotFoundError:
        pass
    return None


def check_bridge(ifname):
    return os.path.exists(f"/sys/class/net/{ifname}")


def print_result(ok, label, detail=""):
    status = "[OK]" if ok else "[MISSING]"
    print(f"  {status:<10} {label:<22} {detail}")


def main():
    print("dirty-vm dependency check")
    print("==========================\n")

    all_ok = True
    missing_packages = []
    missing_modules = []
    missing_system = []

    # Virtualization
    print("Virtualization:")
    qemu_ok = check_binary("qemu-system-x86_64")
    print_result(qemu_ok, "qemu-system-x86_64", "(package: qemu-system-x86)")
    if not qemu_ok:
        missing_packages.append("qemu-system-x86")
    all_ok &= qemu_ok

    qemu_img_ok = check_binary("qemu-img")
    print_result(qemu_img_ok, "qemu-img", "(package: qemu-utils)")
    if not qemu_img_ok:
        missing_packages.append("qemu-utils")
    all_ok &= qemu_img_ok

    kvm_dev_ok, kvm_dev_detail = check_kvm_device()
    print_result(kvm_dev_ok, "/dev/kvm", f"({kvm_dev_detail})")
    if not kvm_dev_ok:
        missing_system.append("/dev/kvm access")
    all_ok &= kvm_dev_ok

    kvm_mod_ok = check_module("kvm")
    print_result(kvm_mod_ok, "kvm module", "(kernel module loaded)")
    if not kvm_mod_ok:
        missing_modules.append("kvm")
    all_ok &= kvm_mod_ok

    vendor = get_cpu_vendor()
    kvm_intel_ok = check_module("kvm_intel")
    kvm_amd_ok = check_module("kvm_amd")
    kvm_cpu_ok = kvm_intel_ok or kvm_amd_ok

    if kvm_cpu_ok:
        cpu_label = "kvm_intel module" if kvm_intel_ok else "kvm_amd module"
        print_result(True, cpu_label, "(kernel module loaded)")
    else:
        expected = "kvm_intel / kvm_amd"
        if vendor == "AuthenticAMD":
            expected = "kvm_amd"
        elif vendor == "GenuineIntel":
            expected = "kvm_intel"
        print_result(False, f"{expected} module", "(kernel module loaded)")
        if vendor == "AuthenticAMD":
            missing_modules.append("kvm_amd")
        elif vendor == "GenuineIntel":
            missing_modules.append("kvm_intel")
        else:
            missing_modules.append("kvm_intel or kvm_amd")
    all_ok &= kvm_cpu_ok

    # Networking
    print("\nNetworking:")
    brctl_ok = check_binary("brctl")
    print_result(brctl_ok, "brctl", "(package: bridge-utils)")
    if not brctl_ok:
        missing_packages.append("bridge-utils")
    all_ok &= brctl_ok

    iptables_ok = check_binary("iptables")
    print_result(iptables_ok, "iptables", "(package: iptables)")
    if not iptables_ok:
        missing_packages.append("iptables")
    all_ok &= iptables_ok

    dnsmasq_ok = check_binary("dnsmasq")
    print_result(dnsmasq_ok, "dnsmasq", "(package: dnsmasq)")
    if not dnsmasq_ok:
        missing_packages.append("dnsmasq")
    all_ok &= dnsmasq_ok

    bridge_if_name = os.environ.get("BRIDGE_IF_NAME", "dirtyvmbr0")
    bridge_ok = check_bridge(bridge_if_name)
    print_result(bridge_ok, f"{bridge_if_name} interface", "(bridge interface)")
    if not bridge_ok:
        missing_system.append(f"{bridge_if_name} bridge (created by start)")
    all_ok &= bridge_ok

    # Data Files
    print("\nData Files:")
    DIRTY_VM_PATH = os.path.expanduser(os.environ.get("DIRTY_VM_HOME", "~/.dirty-vm"))
    dirty_vm_json = os.path.join(DIRTY_VM_PATH, "dirty-vm.json")
    dirty_vm_json_ok = os.path.exists(dirty_vm_json)
    print_result(dirty_vm_json_ok, "dirty-vm.json", "(state database)")
    if not dirty_vm_json_ok:
        missing_system.append("dirty-vm.json not found (run setup)")
    all_ok &= dirty_vm_json_ok

    # Utilities
    print("\nUtilities:")
    mkisofs_ok = check_binary("mkisofs")
    print_result(mkisofs_ok, "mkisofs", "(package: genisoimage)")
    if not mkisofs_ok:
        missing_packages.append("genisoimage")
    all_ok &= mkisofs_ok

    wget_ok = check_binary("wget")
    print_result(wget_ok, "wget", "(package: wget)")
    if not wget_ok:
        missing_packages.append("wget")
    all_ok &= wget_ok

    ssh_ok = check_binary("ssh")
    print_result(ssh_ok, "ssh", "(package: openssh-client)")
    if not ssh_ok:
        missing_packages.append("openssh-client")
    all_ok &= ssh_ok

    ssh_keygen_ok = check_binary("ssh-keygen")
    print_result(ssh_keygen_ok, "ssh-keygen", "(package: openssh-client)")
    if not ssh_keygen_ok:
        missing_packages.append("openssh-client")
    all_ok &= ssh_keygen_ok

    # Summary
    print()
    if all_ok:
        print("All dependencies satisfied!")
        sys.exit(0)
    else:
        print("Some dependencies are missing.\n")

        if missing_packages:
            print("Install missing packages with:")
            print(f"  sudo apt install {' '.join(sorted(set(missing_packages)))}")

        if missing_modules:
            print("\nLoad missing kernel modules with:")
            for mod in sorted(set(missing_modules)):
                print(f"  sudo modprobe {mod}")

        if missing_system:
            print("\nOther issues to address:")
            for issue in missing_system:
                print(f"  - {issue}")

        sys.exit(1)


if __name__ == "__main__":
    main()
