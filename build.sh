#!/usr/bin/env bash
# (c) Copyright IBM Corp. 2020,2021
trap "exit" INT
set -e

if [[ -z "$CMCI_PYTHON_38" ]]; then
    echo "Must provide CMCI_PYTHON_38 in environment" 1>&2
    exit 1
fi

if [[ -z "$CMCI_PYTHON_27" ]]; then
    echo "Must provide CMCI_PYTHON_27 in environment" 1>&2
    exit 1
fi

export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

source "$CMCI_PYTHON_38/bin/activate"
(set -x; pip install -r requirements.txt)

(set -x; ANSIBLE_COLLECTIONS_PATHS=../../.. ansible-lint)
(set -x; python3 -m yamllint -c yamllint.yaml .)

echo "/* -------------------------------------------------------------------------- */"
echo "/*                           ansible-test Sanity Tests                        */"
echo "/* -------------------------------------------------------------------------- */"
(set -x; ansible-test sanity 2>&1 --python 3.8)

echo "/* -------------------------------------------------------------------------- */"
echo "/*                          Unit tests Python 3.8                             */"
echo "/* -------------------------------------------------------------------------- */"
(set -x; ansible-test units --python 3.8)

echo "/* -------------------------------------------------------------------------- */"
echo "/*                          Integration tests Python 3.8                      */"
echo "/* -------------------------------------------------------------------------- */"
(set -x; ansible-test integration cics_cmci --python 3.8)

echo "/* -------------------------------------------------------------------------- */"
echo "/*               Integration tests for missing libraries Python 3.8           */"
echo "/* -------------------------------------------------------------------------- */"
(set -x; pip uninstall xmltodict -y)
(set -x; ansible-test integration cics_cmci_missing_xmltodict_library --python 3.8)
(set -x; pip install -r prod-requirements.txt)
(set -x; pip uninstall requests -y)
(set -x; ansible-test integration cics_cmci_missing_requests_library --python 3.8)
(set -x; pip install -r prod-requirements.txt)

echo $?
deactivate


echo "/* -------------------------------------------------------------------------- */"
echo "/*                          Unit tests Python 2.7                             */"
echo "/* -------------------------------------------------------------------------- */"
source "$CMCI_PYTHON_27/bin/activate"
pip install -r requirements.txt
(set -x; ansible-test units --python 2.7)

echo "/* -------------------------------------------------------------------------- */"
echo "/*                          Integration tests Python 2.7                      */"
echo "/* -------------------------------------------------------------------------- */"
(set -x; ansible-test integration cics_cmci --python 2.7)
deactivate

source "$CMCI_PYTHON_38/bin/activate"
echo "/* -------------------------------------------------------------------------- */"
echo "/*                   Collection Build and Install                             */"
echo "/* -------------------------------------------------------------------------- */"
(set -x; ansible-galaxy collection build . --force)
(set -x; ansible-galaxy collection install ibm-ibm_zos_cics* --force)
