# setup

Bootstraps the dirty-vm environment by creating the work directory, state database, and SSH credentials.

## What It Does

1. Creates `~/.dirty-vm/` and its subdirectories:
   - `images/` — for pulled cloud images
   - `discs/` — for VM disc files
   - `cdroms/` — for cloud-init ISOs
   - `run/` — for PID files
2. Creates `~/.dirty-vm/dirty-vm.json` (only if it does not already exist) from the bundled template
3. Generates an Ed25519 SSH keypair at `~/.ssh/dirty-vm` (only if it does not already exist)

## Usage

```bash
dirty-vm setup
```

## Environment

- `DIRTY_VM_HOME` — directory where dirty-vm stores its state (default: `~/.dirty-vm`)
