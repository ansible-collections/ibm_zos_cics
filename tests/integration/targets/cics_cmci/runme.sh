#!/usr/bin/env bash
# (c) Copyright IBM Corp. 2020,2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
set -eux # This is important to ensure that return codes from failing tests are propagated

VAR_PATH="$ANSIBLE_COLLECTIONS_PATH/ansible_collections/ibm/ibm_zos_cics/tests/integration/variables/cmci.yml"

ansible-playbook -e "@$VAR_PATH" playbooks/cics_cmci_https.yml
ansible-playbook -e "@$VAR_PATH" playbooks/cmci_insecure_false.yml
ansible-playbook -e "@$VAR_PATH" playbooks/cmci_incorrect_port.yml
ansible-playbook -e "@$VAR_PATH" playbooks/cmci_incorrect_host.yml
ansible-playbook -e "@$VAR_PATH" playbooks/cmci_invalid_credentials.yml
ansible-playbook -e "@$VAR_PATH" playbooks/cmci_incorrect_scope.yml
ansible-playbook -e "@$VAR_PATH" playbooks/cmci_incorrect_context.yml
ansible-playbook -e "@$VAR_PATH" playbooks/cics_cmci_http.yml
ansible-playbook -e "@$VAR_PATH" playbooks/cmci_install_bundle_failure.yml
ansible-playbook -e "@$VAR_PATH" playbooks/cmci_create_pipeline_failure.yml
ansible-playbook -e "@$VAR_PATH" playbooks/cmci_incorrect_scheme.yml
ansible-playbook -e "@$VAR_PATH" playbooks/cmci_bas_link.yml
ansible-playbook -e "@$VAR_PATH" playbooks/cmci_bas_install.yml
ansible-playbook -e "@$VAR_PATH" playbooks/cmci_bas_install_error.yml
ansible-playbook -e "@$VAR_PATH" playbooks/cics_cmci_module_defaults_cmci.yml
ansible-playbook -e "@$VAR_PATH" playbooks/cics_cmci_module_defaults_cmci_group.yml
