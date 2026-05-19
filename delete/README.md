# delete

Deletes a virtual machine and its associated files.

## Usage

```bash
dirty-vm delete <vm_name>
```

## What It Does

1. Finds the VM in `dirty-vm.json`
2. **Refuses deletion if the VM is still running** — you must stop it first
3. Deletes the disc file (`discs/<name>.qcow2`)
4. Deletes the cloud-init CDROM (`cdroms/<name>_cloud_init.iso`)
5. Removes the VM entry from `dirty-vm.json`

## Safety

- Cannot delete a running VM
- Gracefully handles already-missing disc or CDROM files

## Exit Codes

- `0` — VM deleted successfully
- `1` — VM not found, or VM is still running
