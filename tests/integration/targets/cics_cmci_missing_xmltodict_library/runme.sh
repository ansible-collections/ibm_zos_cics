#!/usr/bin/env bash
# (c) Copyright IBM Corp. 2021,2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
set -eux # This is important to ensure that return codes from failing tests are propagated

export ANSIBLE_INVENTORY="$ANSIBLE_COLLECTIONS_PATH/ansible_collections/ibm/ibm_zos_cics/tests/integration/inventory_zos.yml"

if pip show xmltodict 2>&1 | grep -q 'Package(s) not found'; then 
    ansible-playbook playbooks/cmci_missing_xmltodict.yml
else
    CURRENT_PKG=$(pip freeze | grep xmltodict=)
    pip uninstall xmltodict -y
    ansible-playbook playbooks/cmci_missing_xmltodict.yml
    pip install "$CURRENT_PKG"
fi
