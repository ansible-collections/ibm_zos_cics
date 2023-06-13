#!/usr/bin/env bash
# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
set -eux # This is important to ensure that return codes from failing tests are propagated

export ANSIBLE_COLLECTIONS_PATH=/root/.ansible/collections:$ANSIBLE_COLLECTIONS_PATH
ANSIBLE_LIBRARY=./library ansible-playbook -e "@variables.yml" -i zos_inventory playbooks/cics_get_version.yml