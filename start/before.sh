#!/bin/bash

../check/validate.sh

echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward > /dev/null

get_default_interface() {
    ip route | grep default | awk '{print $5}' | head -n 1
}

BRIDGE_NAME="${BRIDGE_IF_NAME:-dirtyvmbr0}"
BRIDGE_IP="192.168.4.1/24"

NAT_INTERFACE=$(get_default_interface)

if [ -z "$NAT_INTERFACE" ]; then
    exit 1
fi

if ! ip link show "$BRIDGE_NAME" &> /dev/null; then
    sudo brctl addbr "$BRIDGE_NAME"

    sudo ip addr add "$BRIDGE_IP" dev "$BRIDGE_NAME"
    sudo ip link set "$BRIDGE_NAME" up

    sudo iptables -A FORWARD -i "$BRIDGE_NAME" -o "$NAT_INTERFACE" -j ACCEPT
    sudo iptables -t nat -A POSTROUTING -o "$NAT_INTERFACE" -j MASQUERADE
    sudo iptables -A FORWARD -i "$NAT_INTERFACE" -o "$BRIDGE_NAME" -m state --state RELATED,ESTABLISHED -j ACCEPT
fi

DIRTY_VM_PATH="${DIRTY_VM_HOME:-$HOME/.dirty-vm}"
DNSMASQ_CONF_FILE="$DIRTY_VM_PATH/dnsmasq.conf"
DNSMASQ_PID_FILE="$DIRTY_VM_PATH/dnsmasq.pid"

DNSMASQ_PID=$( [ -f "$DNSMASQ_PID_FILE" ] && cat "$DNSMASQ_PID_FILE" )
if [ -z "$DNSMASQ_PID" ]; then
    sudo dnsmasq -C "$DNSMASQ_CONF_FILE" --pid-file="$DNSMASQ_PID_FILE" --dhcp-leasefile="$DIRTY_VM_PATH/run/dnsmasq.leases"
    exit 0
fi

if [ -n "$DNSMASQ_PID" ] && ! ps -p "$DNSMASQ_PID" > /dev/null; then
    sudo dnsmasq -C "$DNSMASQ_CONF_FILE" --pid-file="$DNSMASQ_PID_FILE" --dhcp-leasefile="$DIRTY_VM_PATH/run/dnsmasq.leases"
    exit 0
fi
