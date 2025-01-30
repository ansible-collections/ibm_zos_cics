#!/usr/bin/env bash
# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
set -eux # This is important to ensure that return codes from failing tests are propagated

export ANSIBLE_LIBRARY=./library
export ANSIBLE_INVENTORY="$ANSIBLE_COLLECTIONS_PATH/ansible_collections/ibm/ibm_zos_cics/tests/integration/inventory_zos.yml"

ansible-playbook playbooks/success.yml
ansible-playbook playbooks/failure.yml
