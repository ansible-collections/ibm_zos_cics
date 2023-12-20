#!/usr/bin/env bash
# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

set -eux

VAR_PATH="$ANSIBLE_COLLECTIONS_PATH/ansible_collections/ibm/ibm_zos_cics/tests/integration/variables/provisioning.yml"
INV_PATH="$ANSIBLE_COLLECTIONS_PATH/ansible_collections/ibm/ibm_zos_cics/tests/integration/inventory_zos.yml"
ZOS_ENV="$ANSIBLE_COLLECTIONS_PATH/ansible_collections/ibm/ibm_zos_cics/tests/integration/variables/zos.yml"

ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" playbooks/test_auxiliary_temp.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" playbooks/test_global_catalog.yml
