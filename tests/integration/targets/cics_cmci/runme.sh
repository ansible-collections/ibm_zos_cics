#!/usr/bin/env bash
echo "Test cics_cmci"
ansible-playbook -i inventory.yml playbooks/cics_cmci.yml -vvv