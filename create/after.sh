#!/bin/bash

PID_FILE="$HOME/.dirty-vm/run/dnsmasq.pid"

if [ ! -f "$PID_FILE" ]; then
    exit 0
fi

PID=$(cat "$PID_FILE")
if [ -z "$PID" ]; then
    exit 0
fi

if ps -p "$PID" > /dev/null; then
    sudo kill -HUP "$PID"
fi
