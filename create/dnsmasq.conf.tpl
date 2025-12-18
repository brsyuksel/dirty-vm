# keep-in-foreground
interface=virbr0
bind-interfaces
no-resolv
server=1.1.1.1
dhcp-range=192.168.4.0,static

# dhcp-host=[mac],[name],[ip],infinite
${dhcp_hosts}
