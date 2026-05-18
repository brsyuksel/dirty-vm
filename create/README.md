# create

Creates a new virtual machine with a cloud-init seed ISO, a resized disc image, and a unique MAC/IP address.

## Usage

```bash
dirty-vm create --name <vm_name> --image-name <image_name> --vcpu <cores> --mem <gb> --disc-size <gb>
```

## Arguments

- `--name` — name of the VM (only letters, numbers, `_`, `-` allowed)
- `--image-name` — name of a previously pulled image
- `--vcpu` — number of virtual CPU cores
- `--mem` — memory size in gigabytes
- `--disc-size` — disc size in gigabytes

## What It Does

1. Validates the VM name format and checks for duplicates
2. Verifies the requested image has been pulled
3. Generates a cloud-init ISO with SSH key injection and hostname
4. Copies the pulled image and resizes it to the requested disc size
5. Allocates the next available MAC and IP address
6. Registers the VM in `dirty-vm.json`
7. Regenerates the dnsmasq configuration with the new DHCP host entry
8. Restarts dnsmasq to pick up the new config

## Files Created

- `DIRTY_VM_HOME/cdroms/<name>_cloud_init.iso`
- `DIRTY_VM_HOME/discs/<name>.qcow2`
