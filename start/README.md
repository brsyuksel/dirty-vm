# start

Starts a virtual machine with QEMU/KVM.

## Usage

```bash
dirty-vm start <vm_name>
```

## What It Does

1. Sets up networking: enables IP forwarding, creates the bridge interface if missing, configures iptables NAT rules, starts dnsmasq
2. Finds the VM in `dirty-vm.json`
3. Detects SMT (Simultaneous Multi-Threading / Hyper-Threading) status to compute optimal CPU topology
4. Launches the VM with QEMU:
   - KVM acceleration enabled
   - CPU topology: cores × threads
   - VirtIO disc + cloud-init CDROM
   - Bridge networking with pre-assigned MAC
   - Headless (`-display none`), daemonized

If the VM is already running, the command exits with an error.
