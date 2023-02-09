#!/usr/bin/env bash
# (c) Copyright IBM Corp. 2021
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
set -eux # This is important to ensure that return codes from failing tests are propagated
ansible-playbook playbooks/cmci_missing_xmltodict.yml
