#!/bin/bash

DIRTY_VM_PATH="${DIRTY_VM_HOME:-$HOME/.dirty-vm}"
# collection.yml sets DIRTY_VM_HOME to "~/.dirty-vm" literally; bash does not expand ~ in variables
DIRTY_VM_PATH="${DIRTY_VM_PATH/#\~/$HOME}"
PID_FILE="$DIRTY_VM_PATH/dnsmasq.pid"
DNSMASQ_CONF_FILE="$DIRTY_VM_PATH/dnsmasq.conf"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if [ -n "$PID" ] && ps -p "$PID" > /dev/null; then
        sudo kill "$PID"
    fi
fi

sudo dnsmasq -C "$DNSMASQ_CONF_FILE" --pid-file="$PID_FILE" --dhcp-leasefile="$DIRTY_VM_PATH/dnsmasq.leases"
