#cloud-config

users:
  - name: ${user}
    ssh_authorized_keys:
      - ${pubkey}
    sudo: ['ALL=(ALL) NOPASSWD:ALL']
    shell: /bin/bash

hostname: ${vm_name}

bootcmd:
  - echo ${host_ip} dirty-vm.host >> /etc/hosts

packages:
  - git
  - curl
