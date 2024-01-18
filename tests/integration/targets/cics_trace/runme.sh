#!/usr/bin/env bash
# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

set -eux

VAR_PATH="$ANSIBLE_COLLECTIONS_PATH/ansible_collections/ibm/ibm_zos_cics/tests/integration/variables/provisioning.yml"
INV_PATH="$ANSIBLE_COLLECTIONS_PATH/ansible_collections/ibm/ibm_zos_cics/tests/integration/inventory_zos.yml"
ZOS_ENV="$ANSIBLE_COLLECTIONS_PATH/ansible_collections/ibm/ibm_zos_cics/tests/integration/variables/zos.yml"

ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" playbooks/absent_trace_data_sets.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" playbooks/check_output.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" playbooks/initial_trace.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" playbooks/check_bad_trace_location.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" playbooks/check_uppercase_location.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" playbooks/incompatible_destination.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" playbooks/template_lowest_precedence.yml