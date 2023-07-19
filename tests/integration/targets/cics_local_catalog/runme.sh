#!/usr/bin/env bash
# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

set -eux
export ANSIBLE_COLLECTIONS_PATH=/root/.ansible/collections:$ANSIBLE_COLLECTIONS_PATH

VAR_PATH="/root/ansible_collections/ibm/ibm_zos_cics/tests/integration/variables/provisioning.yml"
INV_PATH="/root/ansible_collections/ibm/ibm_zos_cics/tests/integration/zos_inventory"
ZOAU_ENV="/root/ansible_collections/ibm/ibm_zos_cics/tests/integration/variables/zoau.yml"

ansible-playbook -i $INV_PATH -e "@$VAR_PATH" -e "@$ZOAU_ENV" playbooks/initial_catalog.yml
ansible-playbook -i $INV_PATH -e "@$VAR_PATH" -e "@$ZOAU_ENV" playbooks/absent_catalog.yml
ansible-playbook -i $INV_PATH -e "@$VAR_PATH" -e "@$ZOAU_ENV" playbooks/check_output.yml
ansible-playbook -i $INV_PATH -e "@$VAR_PATH" -e "@$ZOAU_ENV" playbooks/check_bad_lcd_location.yml
ansible-playbook -i $INV_PATH -e "@$VAR_PATH" -e "@$ZOAU_ENV" playbooks/check_uppercase_location.yml
