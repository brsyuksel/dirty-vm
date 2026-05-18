# delete-image

Deletes a pulled cloud image file and removes its entry from the dirty-vm state file.

## Usage

```bash
dirty-vm delete-image <image_name>
```

## What It Does

1. Looks up the image in the `pulled_images` array of `dirty-vm.json`
2. Deletes the image file from `DIRTY_VM_HOME/images/`
3. Removes the entry from the state file

If the image file was already deleted externally, the registry entry is still removed cleanly.

## Exit Codes

- `0` — Image deleted successfully
- `1` — Image not found in the pulled registry
