#!/bin/bash

DIRTY_VM_PATH="${DIRTY_VM_HOME:-$HOME/.dirty-vm}"
PID_FILE="$DIRTY_VM_PATH/run/dnsmasq.pid"
DNSMASQ_CONF_FILE="$DIRTY_VM_PATH/dnsmasq.conf"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if [ -n "$PID" ] && ps -p "$PID" > /dev/null; then
        sudo kill "$PID"
    fi
fi

sudo dnsmasq -C "$DNSMASQ_CONF_FILE" --pid-file="$PID_FILE"
