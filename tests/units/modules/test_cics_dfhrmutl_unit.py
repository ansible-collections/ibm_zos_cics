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
IMPORT_NAME = 'ibm_zos_cics.plugins.modules.cics_dfhrmutl'

dummy_dict1_check_setautostart = {
    'steplib': 'CICS720.SDFHLOAD',
    'dfhgcd': 'BJMAXY.CICS.IYK3ZMX7.DFHGCD',
    'set_auto_start': None,
    'cold_copy': None,
}

dummy_dict2_valid_setautostart = {
    'steplib': 'CICS720.SDFHLOAD',
    'dfhgcd': 'BJMAXY.CICS.IYK3ZMX7.DFHGCD',
    'set_auto_start': "AUTOASIS",
    'cold_copy': None,
}

dummy_dict2_valid_cold_copy = {
    'steplib': 'CICS720.SDFHLOAD',
    'dfhgcd': 'BJMAXY.CICS.IYK3ZMX7.DFHGCD',
    'set_auto_start': "AUTOCOLD",
    'cold_copy': [{'newgcd': 'BJMAXY.CICS.IYK3ZMX7.NEWGCD'}],
}

dummy_dict3_invalid_setautostart = {
    'steplib': 'CICS720.SDFHLOAD',
    'dfhgcd': 'BJMAXY.CICS.IYK3ZMX7.DFHGCD',
    'set_auto_start': "XXXX",
    'cold_copy': [{'newgcd': 'BJMAXY.CICS.IYK3ZMX7.NEWGCD'}],
}

dummy_dict3_invalid_steplib = {
    'steplib': 'CICS720.SDFHLOAD.**',
    'dfhgcd': 'BJMAXY.CICS.IYK3ZMX7.DFHGCD',
    'set_auto_start': "AUTOCOLD",
    'cold_copy': [{'newgcd': 'BJMAXY.CICS.IYK3ZMX7.NEWGCD'}],
}

dummy_dict3_invalid_dfhgcd = {
    'steplib': 'CICS720.SDFHLOAD',
    'dfhgcd': 'BJMAXY.*.IYK3ZMX7,,DFHGCD',
    'set_auto_start': "AUTOCOLD",
    'cold_copy': [{'newgcd': 'BJMAXY.CICS.IYK3ZMX7.NEWGCD'}],
}

dummy_dict3_invalid_newgcd = {
    'steplib': 'CICS720.SDFHLOAD',
    'dfhgcd': 'BJMAXY.IYK3ZMX7.DFHGCD',
    'set_auto_start': None,
    'cold_copy': [{'newgcd': 'BJMAXY.CICS.IYK3ZMX7,NEWGCD'}],
}

dummy_dict3_invalid_set_auto_start_imcompile_with_cold_copy = {
    'steplib': 'CICS720.SDFHLOAD',
    'dfhgcd': 'BJMAXY.IYK3ZMX7.DFHGCD',
    'set_auto_start': 'AUTODIAG',
    'cold_copy': [{'newgcd': 'BJMAXY.CICS.IYK3ZMX7.NEWGCD'}],
}

test_data1 = [
    (dummy_dict1_check_setautostart, True),
    (dummy_dict2_valid_setautostart, True),
    (dummy_dict2_valid_cold_copy, True),
    (dummy_dict3_invalid_setautostart, False),
    (dummy_dict3_invalid_steplib, False),
    (dummy_dict3_invalid_dfhgcd, False),
    (dummy_dict3_invalid_newgcd, False),
    (dummy_dict3_invalid_set_auto_start_imcompile_with_cold_copy, False)
]


@pytest.mark.parametrize("args,expected", test_data1)
def test_cics_dfhrmutl(zos_import_mocker, args, expected):
    mocker, importer = zos_import_mocker
    cics_dfhrmutl = importer(IMPORT_NAME)
    passed = True
    try:
        cics_dfhrmutl.validate_module_params(args)
    except Exception:
        passed = False
    assert passed == expected
