# dirty-vm

> ⚠️ **Development Status:** This project is under active development. Expect bugs and breaking changes. Currently, it only supports **amd64** architecture and has been tested on **Debian** (and Debian-based distributions like Ubuntu).

**dirty-vm** is a [shellican](https://github.com/brsyuksel/shellican) collection for managing disposable virtual machines with QEMU/KVM on Linux. It bypasses the complexity and runtime dependencies of heavy virtualization managers, providing a lightweight and efficient way to spin up VMs for dirty jobs.

## Prerequisites

- **QEMU/KVM**
- **bridge-utils**
- **iptables**
- **dnsmasq**
- **shellican**

Run `dirty-vm check` to verify all dependencies are installed on your system.

## Installation

### Install Shellican

Follow the [shellican installation guide](https://github.com/brsyuksel/shellican?tab=readme-ov-file#installation).

### Import Collection

```bash
shellican import https://github.com/brsyuksel/dirty-vm.git
```

### Create Helper Shell (Optional)

```bash
# Creates ~/.local/bin/dirty-vm-shell
shellican create-shell dirty-vm

# Or without the -shell suffix:
shellican create-shell dirty-vm dirty-vm
```

## Commands

List all subcommands via shellican: `shellican list dirty-vm`

```
NAME          DESCRIPTION
setup         creates workdir for dirty-vm, sets configuration file and creates ssh key for connections
check         checks if required dependencies are installed
images        list distro images
pull          downloads distro image
delete-image  deletes downloaded image
create        creates a new virtual machine
list          lists virtual machines
start         starts virtual machine
stop          stops virtual machine
delete        deletes virtual machine
run           executes command in virtual machine
ssh           ssh to virtual machine
forward       port forward to virtual machine's port
```

## Setup

Before creating any virtual machine, run the setup:

```bash
dirty-vm setup
```

This creates `~/.dirty-vm/` and its subdirectories, generates the unified state file (`dirty-vm.json`), and creates an SSH keypair at `~/.ssh/dirty-vm`.

## Environment Variables

The collection exposes these environment variables (all have sensible defaults):

- `DIRTY_VM_HOME` — where dirty-vm stores its state (default: `~/.dirty-vm`)
- `BRIDGE_IF_NAME` — bridge interface name (default: `dirtyvmbr0`)
- `DNS_UPSTREAM` — upstream DNS server for dnsmasq (default: `1.1.1.1`)

## Usage

- Check dependencies: `dirty-vm check`
- List supported distro images: `dirty-vm images`
- Pull an image: `dirty-vm pull <image_name>`
- Create a VM: `dirty-vm create <name> <image_name> <vcpu> <mem> <disc_size>`
- List VMs: `dirty-vm list`
- Start VM: `dirty-vm start <vm_name>`
- Stop VM: `dirty-vm stop <vm_name>`
- SSH connection: `dirty-vm ssh <vm_name>`
- Execute a command: `dirty-vm run <vm_name> -- <shell_cmd>`
- Port forward: `dirty-vm forward <vm_name> <vm_port> <local_port>`

## How It Works

- **CPU Optimization**: Automatically detects SMT (Hyper-Threading) status on the host to calculate optimal `-smp` parameters.
- **Networking**: Uses a dedicated dnsmasq instance managing `192.168.4.0/24` on the configured bridge interface. Assigns static MAC and IP to each VM.
- **cloud-init**: Automatically attaches a seed ISO for user-data and SSH key injection.
- **Unified State**: All VM, image, and network state lives in a single JSON file (`dirty-vm.json`).

## Quick Start Example

```bash
dirty-vm setup

# Check everything is in order
dirty-vm check

# pull debian-trixie image
dirty-vm pull debian-trixie

# create a new virtual machine named my-first-vm with 4 cores, 8gb ram and 40gb disc
dirty-vm create my-first-vm debian-trixie 4 8 40

# start virtual machine
dirty-vm start my-first-vm

# ssh connect to the vm
dirty-vm ssh my-first-vm

# run python http server inside vm
dirty-vm run my-first-vm -- python3 -m http.server

# port forward to vm's 8000 port
dirty-vm forward my-first-vm 8000 9090
curl http://localhost:9090

# stop vm
dirty-vm stop my-first-vm

# delete vm
dirty-vm delete my-first-vm
```
