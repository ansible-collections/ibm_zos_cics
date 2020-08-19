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
IMPORT_NAME = 'ibm_zos_cics.plugins.modules.cics_dfhccutl'

dummy_dict1 = {
    'steplib': 'CTS550.CICS720.SDFHLOAD',
    'dfhlcd': 'CTS550.CICS720.XXXXXXX',
}
dummy_dict2_invalid_steplib = {
    'steplib': '*.CICS720.SDFHLOAD',
    'dfhlcd': 'CTS550.CICS720.XXXXXXX',
}
dummy_dict3_invalid_dfhlcd = {
    'steplib': 'CICS.CICS720.SDFHLOAD',
    'dfhlcd': 'CTS550.CICS720,XXXXXXX',
}

test_data1 = [
    (dummy_dict1, True),
    (dummy_dict2_invalid_steplib, False),
    (dummy_dict3_invalid_dfhlcd, False)
]


@pytest.mark.parametrize("args,expected", test_data1)
def test_cics_dfhccutl(zos_import_mocker, args, expected):
    mocker, importer = zos_import_mocker
    cics_dfhccutl = importer(IMPORT_NAME)
    passed = True
    try:
        cics_dfhccutl.validate_module_params(args)
    except Exception:
        passed = False
    assert passed == expected
