#!/bin/bash

bash ../check/validate.sh || exit 1

DIRTY_VM_PATH="${DIRTY_VM_HOME:-$HOME/.dirty-vm}"
STATE_FILE="$DIRTY_VM_PATH/dirty-vm.json"

if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ] || [ -z "$4" ] || [ -z "$5" ]; then
    echo "usage: dirty-vm create <name> <image_name> <vcpu> <mem> <disc_size>"
    exit 1
fi

NAME="$1"
IMAGE_NAME="$2"

if ! echo "$NAME" | grep -qE '^[a-zA-Z0-9_-]+$'; then
    echo "invalid vm name: use only ascii letters, numbers, underscore, dash"
    exit 1
fi

python3 -c "
import json, sys, os
state = json.load(open(os.path.expanduser('$STATE_FILE')))
if any(vm.get('name') == '$NAME' for vm in state.get('virtual_machines', [])):
    print(f'virtual machine $NAME already exists')
    sys.exit(1)
if not any(img.get('name') == '$IMAGE_NAME' for img in state.get('pulled_images', [])):
    print(f'no pulled image found with name $IMAGE_NAME')
    sys.exit(1)
"
