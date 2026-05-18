# images

Lists available distro images for the host architecture and shows which ones have already been pulled.

## Usage

```bash
dirty-vm images
```

## What It Shows

- **name** — the distro image name (e.g. `debian-trixie`)
- **downloaded** — whether the image has been pulled locally
- **size** — the size of the pulled image, or `-` if not yet downloaded

## Architecture Detection

Automatically detects the host architecture (`amd64` or `arm64`) and filters the image list accordingly.
