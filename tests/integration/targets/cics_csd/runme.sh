#!/usr/bin/env bash
# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

set -eux

export ANSIBLE_INVENTORY="$ANSIBLE_COLLECTIONS_PATH/ansible_collections/ibm/ibm_zos_cics/tests/integration/inventory_zos.yml"

ansible-playbook playbooks/csdup_script.yml -vvv
