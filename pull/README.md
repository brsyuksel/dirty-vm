# pull

Downloads a cloud image for a supported distro and registers it in the dirty-vm state file.

## Usage

```bash
dirty-vm pull <image_name>
```

## What It Does

1. Looks up the image URL in `dirty-vm.json` for the host architecture
2. Downloads the image to `DIRTY_VM_HOME/images/<image_name>.img` using `wget`
3. Records the image in the `pulled_images` array of `dirty-vm.json`

If the image is already pulled, it will be overwritten and re-registered.

## Architecture

Automatically detects the host architecture (`amd64` or `arm64`) and pulls the matching image.

## Requirements

- `images/` directory must exist inside `DIRTY_VM_HOME`
- `wget` must be installed
