# forward

Sets up an SSH port-forward from a local port to a port on a running virtual machine.

## Usage

```bash
dirty-vm forward <vm_name> <vm_port> <local_port>
```

## Example

```bash
# Forward local port 9090 to port 8000 on the VM
dirty-vm forward my-vm 8000 9090
# Then: curl http://localhost:9090
```

## What It Does

1. Finds the VM in `dirty-vm.json`
2. Verifies the VM is running by checking its PID file
3. Opens an SSH tunnel: `localhost:<local_port>` → `<vm>:<vm_port>`
4. The tunnel stays open until you interrupt it (Ctrl+C)

## Notes

- Uses SSH `-N` so no shell session is started — just the tunnel
- Interrupt with Ctrl+C when done
