# keep-in-foreground
interface=${interface}
bind-interfaces
no-resolv
server=${upstream}
dhcp-range=192.168.4.0,static

# dhcp-host=[mac],[name],[ip],infinite
${dhcp_hosts}
