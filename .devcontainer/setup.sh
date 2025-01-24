#!/usr/bin/env bash
# Copy contents to the .ssh directory
python3 -m pip install --user ansible-core==2.16

ansible-galaxy collection install ibm.ibm_zos_core:==1.9.1 -p /workspace/collections
ansible-galaxy collection install community.general -p /workspace/collections

pip install -r /workspace/collections/ansible_collections/ibm/ibm_zos_cics/dev-requirements.txt
pip install -r /workspace/collections/ansible_collections/ibm/ibm_zos_cics/doc-requirements.txt