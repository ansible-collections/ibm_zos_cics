# -*- coding: utf-8 -*-

# Copyright (c) IBM Corporation 2019, 2020
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

# from ansible.module_utils.basic import AnsibleModule
import pytest
# import sys
# from mock import call

# Used my some mock modules, should match import directly below
IMPORT_NAME = 'ansible_collections_ibm_zos_cics.plugins.modules.cics_cmci'

# * Tests for zos_operator

dummy_dict1 = {
    'cmci_host': '100.99.99.199',
    'cmci_port': '10080',
    'context': 'iyk3z0r9',
    'scope': 'iyk3z0r8',
    'resource': [{'type': 'cicslocalfile'}],
}

dummy_dict2_invalid_host = {
    'cmci_host': '^*.99.99.199',
    'cmci_port': '10080',
    'context': 'iyk3z0r9',
    'scope': 'iyk3z0r8',
    'resource': [{'type': 'cicslocalfile'}],
}

dummy_dict3_invalid_port = {
    'cmci_host': '100.99.99.199',
    'cmci_port': '^%^080',
    'context': 'iyk3z0r9',
    'scope': 'iyk3z0r8',
    'resource': [{'type': 'cicslocalfile'}],
}

dummy_dict4_invalid_context = {
    'cmci_host': '100.99.99.199',
    'cmci_port': '10080',
    'context': '^&iyk3z0r9',
    'scope': 'iyk3z0r8',
    'resource': [{'type': 'cicslocalfile'}],
}

dummy_dict5_invalid_scope = {
    'cmci_host': '100.99.99.199',
    'cmci_port': '10080',
    'context': 'iyk3z0r9',
    'scope': '&^iyk3z0r8',
    'resource': [{'type': 'cicslocalfile'}],
}

dummy_dict6_invalid_security = {
    'cmci_host': '100.99.99.199',
    'cmci_port': '10080',
    'context': 'iyk3z0r9',
    'scope': '&^iyk3z0r8',
    'security_type': 'yes',
    'resource': [{'type': 'cicslocalfile'}],
}

dummy_dict7_invalid_security = {
    'cmci_host': '100.99.99.199',
    'cmci_port': '10080',
    'context': 'iyk3z0r9',
    'scope': '&^iyk3z0r8',
    'security_type': 'certificate',
    'resource': [{'type': 'cicslocalfile'}],
}


test_data1 = [
    (dummy_dict1, True),
    (dummy_dict2_invalid_host, False),
    (dummy_dict3_invalid_port, False),
    (dummy_dict4_invalid_context, False),
    (dummy_dict5_invalid_scope, False)
]

test_data2 = [
    (dummy_dict6_invalid_security, False),
    (dummy_dict7_invalid_security, False)
]


@pytest.mark.parametrize("args,expected", test_data1)
def test_cics_cmci_various_args(zos_import_mocker, args, expected):
    mocker, importer = zos_import_mocker
    cics_cmci = importer(IMPORT_NAME)
    passed = True
    try:
        cics_cmci.validate_module_params(args)
    except Exception:
        passed = False
    assert passed == expected


@pytest.mark.parametrize("args,expected", test_data2)
def test_cics_cmci_various_args2(zos_import_mocker, args, expected):
    mocker, importer = zos_import_mocker
    cics_cmci = importer(IMPORT_NAME)
    passed = True
    try:
        cics_cmci.get_connect_session(args)
    except Exception:
        passed = False
    assert passed == expected
