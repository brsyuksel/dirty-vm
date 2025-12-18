# dirty-vm

> ⚠️ **Development Status:** This project is under active development. Expect bugs and breaking changes. Currently, it only supports **Linux** on **amd64** architecture.

**dirty-vm** is a [shellican](https://github.com/brsyuksel/shellican) collection for managing virtual machines, built on top of QEMU/KVM for Linux. It bypasses the complexity and runtime dependencies of heavy virtualization managers, providing a lightweight and efficient way to spin up "disposable" virtual machines.

## Prerequisites

- **QEMU/KVM**
- **bridge-utils**
- **iptables**
- **shellican**

## Installation

### Install Shellican

Follow the [shellican installation guide](https://github.com/brsyuksel/shellican?tab=readme-ov-file#installation).

### Import Collection

run command to import collection: `shellican import https://github.com/brsyuksel/dirty-vm.git`

### Create Helper Shell (Optional)

Running `shellican create-shell dirty-vm` will create a helper script named `dirty-vm-shell`.

If you prefer to avoid the -shell suffix, use this command instead: `shellican create-shell dirty-vm dirty-vm`

## Commands

List all subcommands via shellican: `shellican list dirty-vm`

```
NAME          DESCRIPTION
setup         creates workdir for dirty-vm, sets configuration file and creates ssh key for connections
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

Before creating any virtual machine, you must run the setup: `dirty-vm setup`

## Usage

- List supported distro images: `dirty-vm images`
- Pull an image `dirty-vm pull <image_name>`
- Create a VM: `dirty-vm create <vm_name> <image_name> <vcpu-cores> <memory_in_gb> <disc_size_in_gb>`
- Start VM: `dirty-vm start <vm_name>`
- Stop VM: `dirty-vm stop <vm_name>`
- SSH connection: `dirty-vm ssh <vm_name>`
- Execute a command: `dirty-vm run <vm_name> -- <shell_cmd>`

## How It Works

- **CPU Optimization**: Automatically detects SMT (Hyper-Threading) status on the host to calculate optimal -smp parameters.
- **Networking**: Uses a dedicated dnsmasq instance managing 192.168.4.0/24 on virbr0, assigns static ip and mac address each vm.
- **cloud-init**: Automatically attaches a seed iso for user-data and ssh key injection.

## Quick Start Example

```bash
dirty-vm setup

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
