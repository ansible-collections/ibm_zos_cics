#!/usr/bin/env bash
# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

set -eux

VAR_PATH="$ANSIBLE_COLLECTIONS_PATH/ansible_collections/ibm/ibm_zos_cics/tests/integration/variables/provisioning.yml"
INV_PATH="$ANSIBLE_COLLECTIONS_PATH/ansible_collections/ibm/ibm_zos_cics/tests/integration/inventory_zos.yml"
ZOS_ENV="$ANSIBLE_COLLECTIONS_PATH/ansible_collections/ibm/ibm_zos_cics/tests/integration/variables/zos.yml"


ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "state=initial" playbooks/handle_datasets.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" playbooks/start_cics_golden.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "mode=normal" playbooks/stop_cics.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" playbooks/start_cics_with_more_customisation.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV"  -e "mode=immediate" playbooks/stop_cics.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" playbooks/start_cics_golden.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV"  -e "mode=cancel" playbooks/stop_cics.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" playbooks/start_cics_with_invalid_entries.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "state=absent" playbooks/handle_datasets.yml
