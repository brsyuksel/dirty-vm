# run

Executes a shell command inside a running virtual machine over SSH.

## Usage

```bash
dirty-vm run <vm_name> -- <shell_cmd>
```

## Examples

```bash
dirty-vm run my-vm -- ls -la /
dirty-vm run my-vm -- python3 -m http.server 8000
dirty-vm run my-vm -- sudo apt update
```

## What It Does

1. Finds the VM in `dirty-vm.json`
2. Verifies the VM is running by checking its PID file
3. Connects via SSH using the `dirty-vm` keypair
4. Executes the provided command remotely

## Notes

- Everything after `--` is passed as the remote command
- SSH failures are surfaced directly by the ssh client
