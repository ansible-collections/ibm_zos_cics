# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function

__metaclass__ = type
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import dataset_utils
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import global_catalog
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.response import (
    _execution,
)
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.zos_mvs_raw import (
    MVSCmdResponse,
)
import pytest
import sys

try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock


@pytest.mark.skipif(
    sys.version_info.major < 3, reason="Requires python 3 language features"
)
def test_get_idcams_cmd_megabytes():
    catalog_size = dataset_utils._dataset_size(unit="M", primary=10, secondary=1)
    catalog = dataset_utils._data_set(
        size=catalog_size,
        name="ANSI.TEST.DFHGCD",
        sdfhload="CICSTS.IN56.SDFHLOAD",
        state="initial",
        autostart_override="",
        nextstart="",
        exists=False,
        vsam=False,
    )
    idcams_cmd_gcd = dataset_utils._build_idcams_define_cmd(
        global_catalog._get_idcams_cmd_gcd(catalog)
    )
    assert (
        idcams_cmd_gcd
        == """
    DEFINE CLUSTER (NAME(ANSI.TEST.DFHGCD) -
    MEGABYTES(10 1) -
    RECORDSIZE(4089 32760) -
    INDEXED -
    KEYS(52 0) -
    FREESPACE(10 10) -
    SHAREOPTIONS(2) -
    REUSE) -
    DATA (NAME(ANSI.TEST.DFHGCD.DATA) -
    CONTROLINTERVALSIZE(32768)) -
    INDEX(NAME(ANSI.TEST.DFHGCD.INDEX))
    """
    )


@pytest.mark.skipif(
    sys.version_info.major < 3, reason="Requires python 3 language features"
)
def test_get_idcams_cmd_cylinders():
    catalog_size = dataset_utils._dataset_size(unit="CYL", primary=3, secondary=1)
    catalog = dataset_utils._data_set(
        size=catalog_size,
        name="ANSI.CYLS.DFHGCD",
        sdfhload="CICSTS.IN56.SDFHLOAD",
        state="initial",
        autostart_override="",
        nextstart="",
        exists=False,
        vsam=False,
    )
    idcams_cmd_gcd = dataset_utils._build_idcams_define_cmd(
        global_catalog._get_idcams_cmd_gcd(catalog)
    )
    assert (
        idcams_cmd_gcd
        == """
    DEFINE CLUSTER (NAME(ANSI.CYLS.DFHGCD) -
    CYLINDERS(3 1) -
    RECORDSIZE(4089 32760) -
    INDEXED -
    KEYS(52 0) -
    FREESPACE(10 10) -
    SHAREOPTIONS(2) -
    REUSE) -
    DATA (NAME(ANSI.CYLS.DFHGCD.DATA) -
    CONTROLINTERVALSIZE(32768)) -
    INDEX(NAME(ANSI.CYLS.DFHGCD.INDEX))
    """
    )


def test_global_catalog_class():
    catalog_size = dataset_utils._dataset_size(unit="M", primary=10, secondary=1)
    catalog = dataset_utils._data_set(
        size=catalog_size,
        name="ANSI.TEST.DFHGCD",
        sdfhload="CICSTS.IN56.SDFHLOAD",
        state="initial",
        autostart_override="",
        nextstart="",
        exists=False,
        vsam=False,
    )
    assert catalog == {
        "size": {"unit": "M", "primary": 10, "secondary": 1},
        "name": "ANSI.TEST.DFHGCD",
        "sdfhload": "CICSTS.IN56.SDFHLOAD",
        "state": "initial",
        "autostart_override": "",
        "nextstart": "",
        "exists": False,
        "vsam": False,
    }


def test_global_catalog_get_records_autoinit_unknown():
    stdout = """ ===DFHRMUTL CICS RECOVERY MANAGER BATCH UTILITY===

 SET_AUTO_START=AUTOINIT

 ---DFHRMUTL:   DFHGCD information
    No recovery manager record found. GCD assumed empty.

 ---DFHRMUTL:   DFHGCD updated information
    Recovery manager auto-start override   : AUTOINIT
    Recovery manager next start type       : UNKNOWN

 Note: a CICS system that was shutdown warm, and which
 has no indoubt, commit-failed or backout-failed Units
 Of Work keypointed at that time, can safely be restarted
 cold without loss of data integrity.


"""
    resp = global_catalog._get_catalog_records(stdout=stdout)
    assert resp == {
        "autostart_override": "AUTOINIT",
        "next_start": "UNKNOWN",
    }


def test_global_catalog_get_records_autoasis_emergency():
    stdout = """ ===DFHRMUTL CICS RECOVERY MANAGER BATCH UTILITY===


 ---DFHRMUTL:   DFHGCD information
    Recovery manager auto-start override   : AUTOASIS
    Recovery manager next start type       : EMERGENCY

 Note: a CICS system that was shutdown warm, and which
 has no indoubt, commit-failed or backout-failed Units
 Of Work keypointed at that time, can safely be restarted
 cold without loss of data integrity.


"""
    resp = global_catalog._get_catalog_records(stdout=stdout)
    assert resp == {
        "autostart_override": "AUTOASIS",
        "next_start": "EMERGENCY",
    }


def test_global_catalog_get_records_autocold_emergency():
    stdout = """ ===DFHRMUTL CICS RECOVERY MANAGER BATCH UTILITY===


 ---DFHRMUTL:   DFHGCD information
    Recovery manager auto-start override   : AUTOCOLD
    Recovery manager next start type       : EMERGENCY

 Note: a CICS system that was shutdown warm, and which
 has no indoubt, commit-failed or backout-failed Units
 Of Work keypointed at that time, can safely be restarted
 cold without loss of data integrity.


"""
    resp = global_catalog._get_catalog_records(stdout=stdout)
    assert resp == {
        "autostart_override": "AUTOCOLD",
        "next_start": "EMERGENCY",
    }


def test_global_catalog_run_rmutl_with_cmd():
    executions = [
        _execution(
            name="DFHRMUTL - Updating autostart override - Run 1",
            rc=0,
            stdout="",
            stderr="",
        )
    ]
    global_catalog.MVSCmd.execute = MagicMock(
        return_value=MVSCmdResponse(rc=0, stdout="", stderr="")
    )
    global_catalog._get_rmutl_dds = MagicMock(return_value=[])
    result = global_catalog._run_dfhrmutl(
        location="DATA.SET", sdfhload="SDFH.LOAD", cmd="HI"
    )

    assert result == executions


def test_global_catalog_run_rmutl_with_cmd_and_failure():
    executions = [
        _execution(
            name="DFHRMUTL - Updating autostart override - Run 1",
            rc=16,
            stdout=" ABC \n REASON: X'A8'",
            stderr="",
        ),
        _execution(
            name="DFHRMUTL - Updating autostart override - Run 2",
            rc=0,
            stdout="",
            stderr="",
        ),
    ]
    global_catalog.MVSCmd.execute = MagicMock(
        side_effect=[
            MVSCmdResponse(rc=16, stdout=" ABC \n REASON: X'A8'", stderr=""),
            MVSCmdResponse(rc=0, stdout="", stderr=""),
        ]
    )
    global_catalog._get_rmutl_dds = MagicMock(return_value=[])
    result = global_catalog._run_dfhrmutl(
        location="DATA.SET", sdfhload="SDFH.LOAD", cmd="HI"
    )

    assert result == executions


def test_global_catalog_run_rmutl_no_cmd():
    rmutl_response = MVSCmdResponse(
        rc=0,
        stdout=""" ===DFHRMUTL CICS RECOVERY MANAGER BATCH UTILITY===


 ---DFHRMUTL:   DFHGCD information
    Recovery manager auto-start override   : AUTOASIS
    Recovery manager next start type       : EMERGENCY

 Note: a CICS system that was shutdown warm, and which
 has no indoubt, commit-failed or backout-failed Units
 Of Work keypointed at that time, can safely be restarted
 cold without loss of data integrity.

""",
        stderr="",
    )

    expected_executions = [
        _execution(
            name="DFHRMUTL - Get current catalog - Run 1",
            rc=rmutl_response.rc,
            stdout=rmutl_response.stdout,
            stderr=rmutl_response.stderr,
        )
    ]
    expected_details = {
        "autostart_override": "AUTOASIS",
        "next_start": "EMERGENCY",
    }
    global_catalog.MVSCmd.execute = MagicMock(return_value=rmutl_response)
    global_catalog._get_rmutl_dds = MagicMock(return_value=[])
    actual_executions, actual_details = global_catalog._run_dfhrmutl(
        location="DATA.SET", sdfhload="SDFH.LOAD"
    )

    assert actual_executions == expected_executions
    assert actual_details == expected_details


def test_global_catalog_run_rmutl_no_cmd_with_failure():
    rmutl_response = MVSCmdResponse(
        rc=0,
        stdout=""" ===DFHRMUTL CICS RECOVERY MANAGER BATCH UTILITY===


 ---DFHRMUTL:   DFHGCD information
    Recovery manager auto-start override   : AUTOASIS
    Recovery manager next start type       : EMERGENCY

 Note: a CICS system that was shutdown warm, and which
 has no indoubt, commit-failed or backout-failed Units
 Of Work keypointed at that time, can safely be restarted
 cold without loss of data integrity.

""",
        stderr="",
    )

    expected_executions = [
        _execution(
            name="DFHRMUTL - Get current catalog - Run 1",
            rc=16,
            stdout=" ABC \n REASON: X'A8'",
            stderr="",
        ),
        _execution(
            name="DFHRMUTL - Get current catalog - Run 2",
            rc=rmutl_response.rc,
            stdout=rmutl_response.stdout,
            stderr=rmutl_response.stderr,
        ),
    ]
    expected_details = {
        "autostart_override": "AUTOASIS",
        "next_start": "EMERGENCY",
    }
    global_catalog.MVSCmd.execute = MagicMock(
        side_effect=[
            MVSCmdResponse(rc=16, stdout=" ABC \n REASON: X'A8'", stderr=""),
            rmutl_response,
        ]
    )
    global_catalog._get_rmutl_dds = MagicMock(return_value=[])
    actual_executions, actual_details = global_catalog._run_dfhrmutl(
        location="DATA.SET", sdfhload="SDFH.LOAD"
    )

    assert actual_executions == expected_executions
    assert actual_details == expected_details


def test_global_catalog_run_rmutl_no_cmd_many_failures():
    rmutl_response = MVSCmdResponse(
        rc=0,
        stdout=""" ===DFHRMUTL CICS RECOVERY MANAGER BATCH UTILITY===


 ---DFHRMUTL:   DFHGCD information
    Recovery manager auto-start override   : AUTOINIT
    Recovery manager next start type       : UNKNOWN

 Note: a CICS system that was shutdown warm, and which
 has no indoubt, commit-failed or backout-failed Units
 Of Work keypointed at that time, can safely be restarted
 cold without loss of data integrity.

""",
        stderr="",
    )

    expected_executions = [
        _execution(
            name="DFHRMUTL - Get current catalog - Run 1",
            rc=16,
            stdout=" ABC \n REASON: X'A8'",
            stderr="",
        ),
        _execution(
            name="DFHRMUTL - Get current catalog - Run 2",
            rc=16,
            stdout="\n\n\n REASON: X'A8'",
            stderr="",
        ),
        _execution(
            name="DFHRMUTL - Get current catalog - Run 3",
            rc=16,
            stdout="REASON:X'A8'",
            stderr="",
        ),
        _execution(
            name="DFHRMUTL - Get current catalog - Run 4",
            rc=16,
            stdout="\n REASON:X'A8'",
            stderr="",
        ),
        _execution(
            name="DFHRMUTL - Get current catalog - Run 5",
            rc=16,
            stdout=" ABC \n REASON:   X 'A8'",
            stderr="",
        ),
        _execution(
            name="DFHRMUTL - Get current catalog - Run 6",
            rc=rmutl_response.rc,
            stdout=rmutl_response.stdout,
            stderr=rmutl_response.stderr,
        ),
    ]
    expected_details = {
        "autostart_override": "AUTOINIT",
        "next_start": "UNKNOWN",
    }
    global_catalog.MVSCmd.execute = MagicMock(
        side_effect=[
            MVSCmdResponse(rc=16, stdout=" ABC \n REASON: X'A8'", stderr=""),
            MVSCmdResponse(rc=16, stdout="\n\n\n REASON: X'A8'", stderr=""),
            MVSCmdResponse(rc=16, stdout="REASON:X'A8'", stderr=""),
            MVSCmdResponse(rc=16, stdout="\n REASON:X'A8'", stderr=""),
            MVSCmdResponse(rc=16, stdout=" ABC \n REASON:   X 'A8'", stderr=""),
            rmutl_response,
        ]
    )
    global_catalog._get_rmutl_dds = MagicMock(return_value=[])
    actual_executions, actual_details = global_catalog._run_dfhrmutl(
        location="DATA.SET", sdfhload="SDFH.LOAD"
    )

    assert actual_executions == expected_executions
    assert actual_details == expected_details
