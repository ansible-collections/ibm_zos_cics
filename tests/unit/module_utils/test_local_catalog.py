# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.data_set import CYLINDERS, MEGABYTES
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.response import _execution
from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.data_set_helper import PYTHON_LANGUAGE_FEATURES_MESSAGE, CCUTL_name, CCUTL_stderr

from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.zos_mvs_raw import MVSCmdResponse
__metaclass__ = type
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import local_catalog as local_catalog_utils
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import dataset_utils
from ansible_collections.ibm.ibm_zos_cics.plugins.modules.local_catalog import SPACE_PRIMARY_DEFAULT, SPACE_SECONDARY_DEFAULT
import pytest
import sys

try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock


NAME = "ANSI.TEST.DFHLCD"


@pytest.mark.skipif(sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE)
def test_get_idcams_cmd_megabytes():
    catalog = dict(
        name=NAME,
        sdfhload="CICSTS.IN56.SDFHLOAD",
        state="initial",
        exists=False,
        data_set_organization="NONE",
        unit=MEGABYTES,
        primary=SPACE_PRIMARY_DEFAULT,
        secondary=SPACE_SECONDARY_DEFAULT
    )
    idcams_cmd_lcd = dataset_utils._build_idcams_define_cmd(local_catalog_utils._get_idcams_cmd_lcd(catalog))
    assert idcams_cmd_lcd == '''
    DEFINE CLUSTER (NAME(ANSI.TEST.DFHLCD) -
    MEGABYTES(200 5) -
    RECORDSIZE(70 2041) -
    INDEXED -
    KEYS(52 0) -
    FREESPACE(10 10) -
    SHAREOPTIONS(2) -
    REUSE) -
    DATA (NAME(ANSI.TEST.DFHLCD.DATA) -
    CONTROLINTERVALSIZE(2048)) -
    INDEX (NAME(ANSI.TEST.DFHLCD.INDEX))
    '''


@pytest.mark.skipif(sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE)
def test_get_idcams_cmd_cylinders():
    catalog = dict(
        name=NAME,
        sdfhload="CICSTS.IN56.SDFHLOAD",
        state="initial",
        exists=False,
        data_set_organization="NONE",
        unit=CYLINDERS,
        primary=SPACE_PRIMARY_DEFAULT,
        secondary=SPACE_SECONDARY_DEFAULT
    )
    idcams_cmd_lcd = dataset_utils._build_idcams_define_cmd(local_catalog_utils._get_idcams_cmd_lcd(catalog))
    assert idcams_cmd_lcd == '''
    DEFINE CLUSTER (NAME(ANSI.TEST.DFHLCD) -
    CYLINDERS(200 5) -
    RECORDSIZE(70 2041) -
    INDEXED -
    KEYS(52 0) -
    FREESPACE(10 10) -
    SHAREOPTIONS(2) -
    REUSE) -
    DATA (NAME(ANSI.TEST.DFHLCD.DATA) -
    CONTROLINTERVALSIZE(2048)) -
    INDEX (NAME(ANSI.TEST.DFHLCD.INDEX))
    '''


def test_ccutl_response():
    local_catalog = {
        "exists": False,
        "name": NAME,
        "size": {
            "primary": SPACE_PRIMARY_DEFAULT,
            "secondary": SPACE_SECONDARY_DEFAULT,
            "unit": MEGABYTES
        },
        "state": "initial",
        "vsam": False,
        "sdfhload": "CICSTS.IN56.SDFHLOAD",
    }

    expected_executions = [
        _execution(name=CCUTL_name(), rc=0, stdout="stdout", stderr=CCUTL_stderr(NAME)),
    ]

    local_catalog_utils._execute_dfhccutl = MagicMock(
        return_value=MVSCmdResponse(rc=0, stdout="stdout", stderr=CCUTL_stderr(NAME))
    )
    executions = local_catalog_utils._run_dfhccutl(local_catalog)

    assert executions == expected_executions


def test_bad_ccutl_response():
    local_catalog = {
        "exists": False,
        "name": NAME,
        "size": {
            "primary": SPACE_PRIMARY_DEFAULT,
            "secondary": SPACE_SECONDARY_DEFAULT,
            "unit": MEGABYTES
        },
        "state": "initial",
        "vsam": False,
        "sdfhload": "CICSTS.IN56.SDFHLOAD",
    }

    expected_executions = [
        _execution(name=CCUTL_name(), rc=99, stdout="stdout", stderr=CCUTL_stderr(NAME)),
    ]

    local_catalog_utils._execute_dfhccutl = MagicMock(
        return_value=MVSCmdResponse(rc=99, stdout="stdout", stderr=CCUTL_stderr(NAME))
    )

    try:
        local_catalog_utils._run_dfhccutl(local_catalog)
    except Exception as e:
        error_message = e.args[0]
        executions = e.args[1]

        assert error_message == "DFHCCUTL failed with RC 99"
        assert executions == expected_executions
