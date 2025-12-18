#!/bin/bash

if [ ! -f ~/.dirty-vm/vms.json ]; then
    echo "{}" > ~/.dirty-vm/vms.json
fi
