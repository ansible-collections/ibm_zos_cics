#!/usr/bin/env bash
# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

set -eux
export ANSIBLE_COLLECTIONS_PATH=/root/.ansible/collections:$ANSIBLE_COLLECTIONS_PATH
ansible-playbook -i zos_inventory -e "@provisioning-variables.yml" playbooks/initial_catalog.yml
ansible-playbook -i zos_inventory -e "@provisioning-variables.yml" playbooks/absent_catalog.yml
ansible-playbook -i zos_inventory -e "@provisioning-variables.yml" playbooks/check_output.yml
ansible-playbook -i zos_inventory -e "@provisioning-variables.yml" playbooks/check_bad_gcd_location.yml
ansible-playbook -i zos_inventory -e "@provisioning-variables.yml" playbooks/check_uppercase_location.yml
