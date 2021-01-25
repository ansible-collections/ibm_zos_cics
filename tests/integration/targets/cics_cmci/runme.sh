#!/usr/bin/env bash
# Copyright (c) IBM Corporation 2020
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
set -eux # This is important to ensure that return codes from failing tests are propagated
ansible-playbook -e "@cmci-variables.yml" playbooks/cics_cmci.yml
ansible-playbook -e "@cmci-variables.yml" playbooks/cmci_insecure_false.yml
ansible-playbook -e "@cmci-variables.yml" playbooks/cmci_incorrect_port.yml