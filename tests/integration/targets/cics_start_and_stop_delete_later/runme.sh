#!/usr/bin/env bash
# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

set -eux
export ANSIBLE_COLLECTIONS_PATH=/root/.ansible/collections:$ANSIBLE_COLLECTIONS_PATH

INV_PATH="$ANSIBLE_COLLECTIONS_PATH/ansible_collections/ibm/ibm_zos_cics/tests/integration/inventory_zos.yml"
ZOS_ENV="$ANSIBLE_COLLECTIONS_PATH/ansible_collections/ibm/ibm_zos_cics/tests/integration/variables/zos.yml"


ansible-playbook -i "$INV_PATH" -e "@$ZOS_ENV" playbooks/stop_cics.yml
ansible-playbook -i "$INV_PATH" -e "@$ZOS_ENV" playbooks/stop_cics_immediately.yml

