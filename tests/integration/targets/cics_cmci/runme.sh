#!/usr/bin/env bash
# (c) Copyright IBM Corp. 2020,2021
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
set -eux # This is important to ensure that return codes from failing tests are propagated
ansible-playbook -e "@cmci-variables.yml" playbooks/cics_cmci_https.yml
ansible-playbook -e "@cmci-variables.yml" playbooks/cmci_insecure_false.yml
ansible-playbook -e "@cmci-variables.yml" playbooks/cmci_incorrect_port.yml
ansible-playbook -e "@cmci-variables.yml" playbooks/cmci_incorrect_host.yml
ansible-playbook -e "@cmci-variables.yml" playbooks/cmci_invalid_credentials.yml
ansible-playbook -e "@cmci-variables.yml" playbooks/cmci_incorrect_scope.yml
ansible-playbook -e "@cmci-variables.yml" playbooks/cmci_incorrect_context.yml
ansible-playbook -e "@cmci-variables.yml" playbooks/cics_cmci_http.yml
ansible-playbook -e "@cmci-variables.yml" playbooks/cmci_install_bundle_failure.yml
ansible-playbook -e "@cmci-variables.yml" playbooks/cmci_create_pipeline_failure.yml
ansible-playbook -e "@cmci-variables.yml" playbooks/cmci_incorrect_scheme.yml
ansible-playbook -e "@cmci-variables.yml" playbooks/cmci_bas_link.yml
ansible-playbook -e "@cmci-variables.yml" playbooks/cmci_bas_install.yml
ansible-playbook -e "@cmci-variables.yml" playbooks/cmci_bas_install_error.yml