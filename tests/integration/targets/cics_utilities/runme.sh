#!/usr/bin/env bash
# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
set -eux # This is important to ensure that return codes from failing tests are propagated

export ANSIBLE_COLLECTIONS_PATH=/root/.ansible/collections:$ANSIBLE_COLLECTIONS_PATH
export ANSIBLE_LIBRARY=./library

VAR_PATH="/root/ansible_collections/ibm/ibm_zos_cics/tests/integration/variables/utilities.yml"
INV_PATH="/root/ansible_collections/ibm/ibm_zos_cics/tests/integration/zos_inventory"
ZOAU_ENV="/root/ansible_collections/ibm/ibm_zos_cics/tests/integration/variables/zoau.yml"

ansible-playbook -i $INV_PATH -e "@$ZOAU_ENV" playbooks/success.yml
ansible-playbook -i $INV_PATH -e "@$VAR_PATH" -e "@$ZOAU_ENV" playbooks/failure.yml
