#!/bin/bash

mkdir -p ~/.dirty-vm/images

if [ ! -f ~/.dirty-vm/images.json ]; then
    echo "{}" > ~/.dirty-vm/images.json
fi
