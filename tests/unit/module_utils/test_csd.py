# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.response import _execution

from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.zos_mvs_raw import MVSCmdResponse

__metaclass__ = type
from ansible_collections.ibm.ibm_zos_cics.plugins.modules import csd
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import csd as csd_utils
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import dataset_utils
import pytest
import sys

try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_get_idcams_cmd_megabytes():
    csd_size = dataset_utils._dataset_size(
        unit="M", primary=3, secondary=1)
    csd_data_set = csd._data_set(
        size=csd_size,
        name="ANSI.TEST.DFHCSD",
        sdfhload="CICSTS.IN56.SDFHLOAD",
        state="initial",
        exists=False,
        vsam=False)
    idcams_cmd_csd = dataset_utils._build_idcams_define_cmd(csd_utils._get_idcams_cmd_csd(csd_data_set))
    assert idcams_cmd_csd == '''
    DEFINE CLUSTER (NAME(ANSI.TEST.DFHCSD) -
    MEGABYTES(3 1) -
    RECORDSIZE(200 2000) -
    INDEXED -
    KEYS(22 0) -
    FREESPACE(10 10) -
    SHAREOPTIONS(2) -
    REUSE) -
    DATA (NAME(ANSI.TEST.DFHCSD.DATA) -
    CONTROLINTERVALSIZE(8192)) -
    INDEX (NAME(ANSI.TEST.DFHCSD.INDEX))
    '''


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_get_idcams_cmd_cylinders():
    csd_size = dataset_utils._dataset_size(
        unit="CYL", primary=3, secondary=1)
    csd_data_set = csd._data_set(
        size=csd_size,
        name="ANSI.TEST.DFHCSD",
        sdfhload="CICSTS.IN56.SDFHLOAD",
        state="initial",
        exists=False,
        vsam=False)
    idcams_cmd_csd = dataset_utils._build_idcams_define_cmd(csd_utils._get_idcams_cmd_csd(csd_data_set))
    assert idcams_cmd_csd == '''
    DEFINE CLUSTER (NAME(ANSI.TEST.DFHCSD) -
    CYLINDERS(3 1) -
    RECORDSIZE(200 2000) -
    INDEXED -
    KEYS(22 0) -
    FREESPACE(10 10) -
    SHAREOPTIONS(2) -
    REUSE) -
    DATA (NAME(ANSI.TEST.DFHCSD.DATA) -
    CONTROLINTERVALSIZE(8192)) -
    INDEX (NAME(ANSI.TEST.DFHCSD.INDEX))
    '''


def test_csd_class():
    csd_size = dataset_utils._dataset_size(unit="M", primary=10, secondary=1)
    csd_data_set = csd._data_set(
        size=csd_size,
        name="ANSI.TEST.DFHCSD",
        sdfhload="CICSTS.IN56.SDFHLOAD",
        state="initial",
        exists=False,
        vsam=False)
    assert csd_data_set == {
        "size": {
            "unit": "M",
            "primary": 10,
            "secondary": 1
        },
        "name": "ANSI.TEST.DFHCSD",
        "sdfhload": "CICSTS.IN56.SDFHLOAD",
        "state": "initial",
        "exists": False,
        "vsam": False,
    }


def test_csdup_response():
    csd_input = {
        "exists": False,
        "name": "ANSI.TEST.DFHCSD",
        "size": {
            "primary": 5,
            "secondary": 1,
            "unit": "M"
        },
        "state": "initial",
        "vsam": False,
        "sdfhload": "CICSTS.IN56.SDFHLOAD",
    }

    expected_executions = [
        _execution(name="DFHCSDUP - Initialise CSD", rc=0, stdout="stdout", stderr="stderr"),
    ]

    csd_utils._execute_dfhcsdup = MagicMock(return_value=MVSCmdResponse(rc=0, stdout="stdout", stderr="stderr"))
    executions = csd_utils._run_dfhcsdup(csd_input)

    assert executions == expected_executions


def test_bad_csdup_response():
    csd_input = {
        "exists": False,
        "name": "ANSI.TEST.DFHCSD",
        "size": {
            "primary": 5,
            "secondary": 1,
            "unit": "M"
        },
        "state": "initial",
        "vsam": False,
        "sdfhload": "CICSTS.IN56.SDFHLOAD",
    }

    expected_executions = [
        _execution(name="DFHCSDUP - Initialise CSD", rc=99, stdout="stdout", stderr="stderr"),
    ]

    csd_utils._execute_dfhcsdup = MagicMock(return_value=MVSCmdResponse(rc=99, stdout="stdout", stderr="stderr"))

    try:
        csd_utils._run_dfhcsdup(csd_input)
    except Exception as e:
        error_message = e.args[0]
        executions = e.args[1]

        assert error_message == "DFHCSDUP failed with RC 99"
        assert executions == expected_executions
