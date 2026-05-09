#!/bin/bash
# if [ $# -eq 0 ]; then
#     echo "You must provide the IP or hostname of the Raspberry Pi to configure."
#     exit 1
# fi
# ansible-playbook install.yml --ask-pass -u pi -i $1,
ansible-playbook --ask-become-pass -vv -i simpletv_hosts.yaml simpletv_playbook.yml

