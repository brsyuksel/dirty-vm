# check

Checks if all required dependencies for dirty-vm are installed on the system.

## Usage

```bash
dirty-vm check
```

## What It Checks

- **Virtualization**: `qemu-system-x86_64`, `qemu-img`, `/dev/kvm` access, KVM kernel modules
- **Networking**: `brctl`, `iptables`, `dnsmasq`, `virbr0` bridge interface
- **Utilities**: `mkisofs`, `wget`, `ssh`, `ssh-keygen`

## Exit Codes

- `0` — All dependencies satisfied
- `1` — One or more dependencies missing

When dependencies are missing, the command prints install instructions for Debian 13 (Trixie).
