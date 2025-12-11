#!/bin/bash

get_default_interface() {
    ip route | grep default | awk '{print $5}' | head -n 1
}

BRIDGE_NAME="virbr0"
BRIDGE_IP="192.168.4.1/24"

NAT_INTERFACE=$(get_default_interface)

if [ -z "$NAT_INTERFACE" ]; then
    exit 1
fi

if ip link show $BRIDGE_NAME &> /dev/null; then
    exit 0
fi

brctl addbr $BRIDGE_NAME

ip addr add $BRIDGE_IP dev $BRIDGE_NAME
ip link set $BRIDGE_NAME up

iptables -A FORWARD -i $BRIDGE_NAME -o $NAT_INTERFACE -j ACCEPT
iptables -t nat -A POSTROUTING -o $NAT_INTERFACE -j MASQUERADE
iptables -A FORWARD -i $NAT_INTERFACE -o $BRIDGE_NAME -m state --state RELATED,ESTABLISHED -j ACCEPT

echo 1 > /proc/sys/net/ipv4/ip_forward
