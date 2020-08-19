# -*- coding: utf-8 -*-​
# Copyright (c) IBM Corporation 2019, 2020

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from unittest.mock import Mock
import pytest
# from unittest import mock
# from pytest_mock import mocker

IMPORT_NAME = 'ansible_collections_ibm_zos_cics.plugins.modules.cics_dfhcsdup'

LONG_STR = ['''
    XXXXXXXXX1XXXXXXXXX2XXXXXXXXX3XXXXXXXXX4XXXXXXXXX5XXXXXXXXX6XXXXXXXXX7X''']

dummy_dict_check_cmd_str = {
    'steplib': 'CTS550.CICS710.SDFHLOAD',
    'dfhcsd': 'ZLBJLU.DTEST.DFHCSD',
    'cmd_str': ['LIST'],
}

dummy_dict_check_cmd_str_long = {
    'steplib': 'CTS550.CICS710.SDFHLOAD',
    'dfhcsd': 'ZLBJLU.DTEST.DFHCSD',
    'cmd_str': LONG_STR,
}


dummy_dict_check_userprog_dd = {
    'steplib': 'CTS550.CICS710.SDFHLOAD',
    'dfhcsd': 'ZLBJLU.DTEST.DFHCSD',
    'userprog_dd': 'XXXXXXXX',
}

dummy_dict_check_userprog_dd_long = {
    'steplib': 'CTS550.CICS710.SDFHLOAD',
    'dfhcsd': 'ZLBJLU.DTEST.DFHCSD',
    'userprog_dd': 'XXXXXXXXXX',
}

dummy_dict_check_steplib = {
    'steplib': 'CTS550.CICS710.SDFHLOAD',
    'dfhcsd': 'ZLBJLU.DTEST.DFHCSD',
}

dummy_dict_check_steplib_invalid = {
    'steplib': 'CTS550.123456.SDFHLOAD',
    'dfhcsd': 'ZLBJLU.DTEST.DFHCSD',
}

dummy_dict_check_dfhcsd = {
    'steplib': 'CTS550.CICS710.SDFHLOAD',
    'dfhcsd': 'ZLBJLU.DTEST.DFHCSD',
}

dummy_dict_check_dfhcsd_invalid = {
    'steplib': 'CTS550.CICS710.SDFHLOAD',
    'dfhcsd': '1ZLBJLU.DTEST.DFHCSD',
}

dummy_dict_check_seccsd = {
    'steplib': 'CTS550.CICS710.SDFHLOAD',
    'dfhcsd': 'ZLBJLU.DTEST.DFHCSD',
    'seccsd': 'ZLBJLU.ETEST.DFHCSD',
}

dummy_dict_check_seccsd_invalid = {
    'steplib': 'CTS550.CICS710.SDFHLOAD',
    'dfhcsd': 'ZLBJLU.DTEST.DFHCSD',
    'seccsd': 'ZLBJLU.XXXXXXXXXXX.DFHCSD',
}

dummy_dict_check_ussprog_lib = {
    'steplib': 'CTS550.CICS710.SDFHLOAD',
    'userprog_lib': 'CTS550.CICS710.SDFHAUTH',
    'dfhcsd': 'ZLBJLU.DTEST.DFHCSD',
}

dummy_dict_check_ussprog_lib_invalid = {
    'steplib': 'CTS550.CICS710.SDFHLOAD',
    'userprog_lib': 'CTS550.CICS710.SDFHLXXXXXX',
    'dfhcsd': 'ZLBJLU.DTEST.DFHCSD',
}

check_data = [
    (dummy_dict_check_cmd_str, True),
    (dummy_dict_check_cmd_str_long, False),
    (dummy_dict_check_userprog_dd, True),
    (dummy_dict_check_userprog_dd_long, False),
    (dummy_dict_check_dfhcsd, True),
    (dummy_dict_check_dfhcsd_invalid, False),
    (dummy_dict_check_seccsd, True),
    (dummy_dict_check_seccsd_invalid, False),
    (dummy_dict_check_steplib, True),
    (dummy_dict_check_steplib_invalid, False),
    (dummy_dict_check_ussprog_lib, True),
    (dummy_dict_check_ussprog_lib_invalid, False),
]


@pytest.mark.parametrize("args,expected", check_data)
def test_cics_dfhcsdup(zos_import_mocker, args, expected):
    mocker, importer = zos_import_mocker
    cics_dfhcsdup = importer(IMPORT_NAME)
    passed = True
    try:
        cics_dfhcsdup.check_parms(args)
    except Exception:
        passed = False
    assert passed == expected


run_cmd = [
    (0, '', ''),
    (8, ' NOT IN CATALOG ', ''),
]

ERR_MSG = "Data set ZLBJLU.BTEST.DFHCSD does not exist."
check_ds_data = [
    ('ZLBJLU.ATEST.DFHCSD', run_cmd[0], (True, None)),
    ('ZLBJLU.BTEST.DFHCSD', run_cmd[1], (False, ERR_MSG)),
]


@pytest.mark.parametrize("dsn, return_value, expected", check_ds_data)
def test_check_ds(zos_import_mocker, dsn, return_value, expected):
    mocker, importer = zos_import_mocker
    ds = importer(IMPORT_NAME)
    module = Mock()
    module.run_command = Mock(return_value=return_value)
    patched_run_command = mocker.patch('{0}.run_command'.format(IMPORT_NAME),
                                       create=True, return_value=return_value)
    assert ds.check_ds(dsn, module) == expected
