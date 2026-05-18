# stop

Stops a running virtual machine and removes its PID file.

## Usage

```bash
dirty-vm stop <vm_name>
```

## What It Does

1. Finds the VM in `dirty-vm.json`
2. Reads the PID from `DIRTY_VM_HOME/run/<vm_name>.pid`
3. Sends `SIGKILL` to the QEMU process
4. Removes the PID file

## Exit Codes

- `0` — VM stopped successfully
- `1` — VM not found or not running
