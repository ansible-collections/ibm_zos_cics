#!/usr/bin/env bash

set -e

git config --global --add safe.directory /root/ansible_collections/ibm/ibm_zos_cics

pip install -r /root/ansible_collections/ibm/ibm_zos_cics/dev-requirements.txt

# ansible-lint requires python >= 3.9
if [ "$TRAVIS_PYTHON_VERSION" != "2.7" ] && [ "$TRAVIS_PYTHON_VERSION" != "3.8" ]; then
    echo ""
    echo "##########################################################"
    echo "###################### Ansible-lint ######################"
    echo "##########################################################"
    echo ""
    ansible-lint --profile production
fi

echo ""
echo "##########################################################"
echo "################## Ansible Sanity Tests ##################"
echo "##########################################################"
echo ""
ansible-test sanity --python "$TRAVIS_PYTHON_VERSION"

echo ""
echo "##########################################################"
echo "################### Ansible Unit Tests ###################"
echo "##########################################################"
echo ""
ansible-test units --python "$TRAVIS_PYTHON_VERSION"

echo ""
echo "###########################################################"
echo "################ Ansible Integration Tests ################"
echo "###########################################################"
echo ""
ansible-test integration cics_cmci --python "$TRAVIS_PYTHON_VERSION"

echo ""
echo "##########################################################"
echo "############## Ansible Missing Module Tests ##############"
echo "##########################################################"
echo ""
pip uninstall xmltodict -y
ansible-test integration cics_cmci_missing_xmltodict_library --python "$TRAVIS_PYTHON_VERSION"

pip install -r /root/ansible_collections/ibm/ibm_zos_cics/dev-requirements.txt
pip uninstall requests -y
ansible-test integration cics_cmci_missing_requests_library --python "$TRAVIS_PYTHON_VERSION"

echo ""
echo "###########################################################"
echo "#################### Build Collection #####################"
echo "###########################################################"
echo ""
pip install -r /root/ansible_collections/ibm/ibm_zos_cics/dev-requirements.txt
ansible-galaxy collection build /root/ansible_collections/ibm/ibm_zos_cics --output-path /root/ansible_collections/ibm/ibm_zos_cics --force
ansible-galaxy collection install /root/ansible_collections/ibm/ibm_zos_cics/ibm-ibm_zos_cics-* --force
