#!/usr/bin/env bash
# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

set -eux

export ANSIBLE_INVENTORY="$ANSIBLE_COLLECTIONS_PATH/ansible_collections/ibm/ibm_zos_cics/tests/integration/inventory_zos.yml"

ansible-playbook playbooks/provisioning_and_deprovisioning.yml
ansible-playbook playbooks/validate_console_not_defined.yml
ansible-playbook playbooks/validate_console_autoinstall_fail.yml
ansible-playbook playbooks/stop_args.yml
ansible-playbook playbooks/missing_jobs.yml
ansible-playbook playbooks/start_from_PDS.yml
