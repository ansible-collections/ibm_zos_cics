#!/usr/bin/env bash
# Copyright (c) IBM Corporation 2020
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
ansible-playbook -e "@cmci-variables.yml" playbooks/cics_cmci.yml
ansible-playbook -e "@cmci-variables.yml" playbooks/cmci_insecure_false.yml