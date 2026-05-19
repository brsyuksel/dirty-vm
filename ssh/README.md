# ssh

Opens an interactive SSH session into a running virtual machine.

## Usage

```bash
dirty-vm ssh <vm_name>
```

## What It Does

1. Finds the VM in `dirty-vm.json`
2. Verifies the VM is running by checking its PID file
3. Connects via SSH using the `dirty-vm` keypair
4. Opens an interactive shell session on the VM

## Notes

- Exits with an error if the VM is not running
- Type `exit` to leave the SSH session
