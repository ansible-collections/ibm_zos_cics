#!/usr/bin/env bash
# (c) Copyright IBM Corp. 2023,2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

set -eux

VAR_PATH="$ANSIBLE_COLLECTIONS_PATH/ansible_collections/ibm/ibm_zos_cics/tests/integration/variables/provisioning.yml"
INV_PATH="$ANSIBLE_COLLECTIONS_PATH/ansible_collections/ibm/ibm_zos_cics/tests/integration/inventory_zos.yml"
ZOS_ENV="$ANSIBLE_COLLECTIONS_PATH/ansible_collections/ibm/ibm_zos_cics/tests/integration/variables/zos.yml"


if [ -z "$(ansible-galaxy collection list ibm.ibm_zos_core)" ]; then
    ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" playbooks/missing_core.yml
else
    json_output=$(ansible-galaxy collection list ibm.ibm_zos_core --format json | jq -r)
    collection_path=$(echo "$json_output" | jq -r 'keys[0]')
    version=$(echo "$json_output" | jq -r .\""$collection_path"\".\"ibm.ibm_zos_core\".\"version\")
    rm -r "$collection_path"/ibm/ibm_zos_core 
    ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" playbooks/missing_core.yml
    ansible-galaxy collection install ibm.ibm_zos_core=="$version" -p"$collection_path"
fi
