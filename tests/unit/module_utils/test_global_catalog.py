# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023,2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils._data_set import CYLINDERS, MEGABYTES

from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.data_set_helper import (
    PYTHON_LANGUAGE_FEATURES_MESSAGE,
    RMUTL_get_run_name,
    RMUTL_stdout,
    RMUTL_update_run_name
)
__metaclass__ = type
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import _data_set_utils as data_set_utils
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import _global_catalog as global_catalog
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils._response import (
    MVSExecutionException,
    _execution,
)
from ansible_collections.ibm.ibm_zos_cics.plugins.modules.global_catalog import SPACE_PRIMARY_DEFAULT, SPACE_SECONDARY_DEFAULT
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
    sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE
)
def test_get_idcams_cmd_megabytes():
    catalog = dict(
        name="ANSI.TEST.DFHGCD",
        sdfhload="CICSTS.IN56.SDFHLOAD",
        state="initial",
        autostart_override="",
        nextstart="",
        exists=False,
        data_set_organization="NONE",
        unit=MEGABYTES,
        primary=SPACE_PRIMARY_DEFAULT,
        secondary=SPACE_SECONDARY_DEFAULT
    )
    idcams_cmd_gcd = data_set_utils._build_idcams_define_cmd(
        global_catalog._get_idcams_cmd_gcd(catalog)
    )
    assert (
        idcams_cmd_gcd
        == """
    DEFINE CLUSTER (NAME(ANSI.TEST.DFHGCD) -
    MEGABYTES(5 1) -
    RECORDSIZE(4089 32760) -
    INDEXED -
    KEYS(52 0) -
    FREESPACE(10 10) -
    SHAREOPTIONS(2) -
    REUSE) -
    DATA (NAME(ANSI.TEST.DFHGCD.DATA) -
    CONTROLINTERVALSIZE(32768)) -
    INDEX (NAME(ANSI.TEST.DFHGCD.INDEX))
    """
    )


@pytest.mark.skipif(
    sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE
)
def test_get_idcams_cmd_cylinders():
    catalog = dict(
        name="ANSI.CYLS.DFHGCD",
        sdfhload="CICSTS.IN56.SDFHLOAD",
        state="initial",
        autostart_override="",
        nextstart="",
        exists=False,
        data_set_organization="NONE",
        unit=CYLINDERS,
        primary=SPACE_PRIMARY_DEFAULT,
        secondary=SPACE_SECONDARY_DEFAULT
    )
    idcams_cmd_gcd = data_set_utils._build_idcams_define_cmd(
        global_catalog._get_idcams_cmd_gcd(catalog)
    )
    assert (
        idcams_cmd_gcd
        == """
    DEFINE CLUSTER (NAME(ANSI.CYLS.DFHGCD) -
    CYLINDERS(5 1) -
    RECORDSIZE(4089 32760) -
    INDEXED -
    KEYS(52 0) -
    FREESPACE(10 10) -
    SHAREOPTIONS(2) -
    REUSE) -
    DATA (NAME(ANSI.CYLS.DFHGCD.DATA) -
    CONTROLINTERVALSIZE(32768)) -
    INDEX (NAME(ANSI.CYLS.DFHGCD.INDEX))
    """
    )


@pytest.mark.skipif(
    sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE
)
def test_get_idcams_cmd_volumes():
    catalog = dict(
        name="ANSI.CYLS.DFHGCD",
        sdfhload="CICSTS.IN56.SDFHLOAD",
        state="initial",
        autostart_override="",
        nextstart="",
        exists=False,
        data_set_organization="NONE",
        unit=CYLINDERS,
        primary=SPACE_PRIMARY_DEFAULT,
        secondary=SPACE_SECONDARY_DEFAULT,
        volumes=["vserv1"]
    )
    idcams_cmd_gcd = data_set_utils._build_idcams_define_cmd(
        global_catalog._get_idcams_cmd_gcd(catalog)
    )
    assert (
        idcams_cmd_gcd
        == """
    DEFINE CLUSTER (NAME(ANSI.CYLS.DFHGCD) -
    CYLINDERS(5 1) -
    RECORDSIZE(4089 32760) -
    INDEXED -
    KEYS(52 0) -
    FREESPACE(10 10) -
    SHAREOPTIONS(2) -
    REUSE -
    VOLUMES(vserv1)) -
    DATA (NAME(ANSI.CYLS.DFHGCD.DATA) -
    CONTROLINTERVALSIZE(32768)) -
    INDEX (NAME(ANSI.CYLS.DFHGCD.INDEX))
    """
    )


@pytest.mark.skipif(
    sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE
)
def test_get_idcams_cmd_multiple_volumes():
    catalog = dict(
        name="ANSI.CYLS.DFHGCD",
        sdfhload="CICSTS.IN56.SDFHLOAD",
        state="initial",
        autostart_override="",
        nextstart="",
        exists=False,
        data_set_organization="NONE",
        unit=CYLINDERS,
        primary=SPACE_PRIMARY_DEFAULT,
        secondary=SPACE_SECONDARY_DEFAULT,
        volumes=["vserv1", "vserv2"]
    )
    idcams_cmd_gcd = data_set_utils._build_idcams_define_cmd(
        global_catalog._get_idcams_cmd_gcd(catalog)
    )
    assert (
        idcams_cmd_gcd
        == """
    DEFINE CLUSTER (NAME(ANSI.CYLS.DFHGCD) -
    CYLINDERS(5 1) -
    RECORDSIZE(4089 32760) -
    INDEXED -
    KEYS(52 0) -
    FREESPACE(10 10) -
    SHAREOPTIONS(2) -
    REUSE -
    VOLUMES(vserv1 vserv2)) -
    DATA (NAME(ANSI.CYLS.DFHGCD.DATA) -
    CONTROLINTERVALSIZE(32768)) -
    INDEX (NAME(ANSI.CYLS.DFHGCD.INDEX))
    """
    )


def test_get_records_autoinit_unknown():
    stdout = RMUTL_stdout("AUTOINIT", "UNKNOWN")
    resp = global_catalog._get_catalog_records(stdout=stdout)
    assert resp == ("AUTOINIT", "UNKNOWN")


def test_get_records_autoasis_emergency():
    stdout = RMUTL_stdout("AUTOASIS", "EMERGENCY")
    resp = global_catalog._get_catalog_records(stdout=stdout)
    assert resp == ("AUTOASIS", "EMERGENCY")


def test_get_records_autocold_emergency():
    stdout = RMUTL_stdout("AUTOCOLD", "EMERGENCY")
    resp = global_catalog._get_catalog_records(stdout=stdout)
    assert resp == ("AUTOCOLD", "EMERGENCY")


def test_run_rmutl_with_cmd():
    executions = [
        _execution(
            name=RMUTL_update_run_name(1),
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


def test_run_rmutl_with_cmd_and_failure():
    executions = [
        _execution(
            name=RMUTL_update_run_name(1),
            rc=16,
            stdout=" ABC \n REASON: X'A8'",
            stderr="",
        ),
        _execution(
            name=RMUTL_update_run_name(2),
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


def test_run_rmutl_no_cmd():
    rmutl_response = MVSCmdResponse(
        rc=0,
        stdout=RMUTL_stdout("AUTOASIS", "EMERGENCY"),
        stderr="",
    )

    expected_executions = [
        _execution(
            name=RMUTL_get_run_name(1),
            rc=rmutl_response.rc,
            stdout=rmutl_response.stdout,
            stderr=rmutl_response.stderr,
        )
    ]
    expected_details = ("AUTOASIS", "EMERGENCY")
    global_catalog.MVSCmd.execute = MagicMock(return_value=rmutl_response)
    global_catalog._get_rmutl_dds = MagicMock(return_value=[])
    actual_executions, actual_details = global_catalog._run_dfhrmutl(
        location="DATA.SET", sdfhload="SDFH.LOAD"
    )

    assert actual_executions == expected_executions
    assert actual_details == expected_details


def test_run_rmutl_no_cmd_with_failure():
    rmutl_response = MVSCmdResponse(
        rc=0,
        stdout=RMUTL_stdout("AUTOASIS", "EMERGENCY"),
        stderr="",
    )

    expected_executions = [
        _execution(
            name=RMUTL_get_run_name(1),
            rc=16,
            stdout=" ABC \n REASON: X'A8'",
            stderr="",
        ),
        _execution(
            name=RMUTL_get_run_name(2),
            rc=rmutl_response.rc,
            stdout=rmutl_response.stdout,
            stderr=rmutl_response.stderr,
        ),
    ]
    expected_details = ("AUTOASIS", "EMERGENCY")
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


def test_run_rmutl_no_cmd_many_failures():
    rmutl_response = MVSCmdResponse(
        rc=0,
        stdout=RMUTL_stdout("AUTOINIT", "UNKNOWN"),
        stderr="",
    )

    expected_executions = [
        _execution(
            name=RMUTL_get_run_name(1),
            rc=16,
            stdout=" ABC \n REASON: X'A8'",
            stderr="",
        ),
        _execution(
            name=RMUTL_get_run_name(2),
            rc=16,
            stdout="\n\n\n REASON: X'A8'",
            stderr="",
        ),
        _execution(
            name=RMUTL_get_run_name(3),
            rc=16,
            stdout="REASON:X'A8'",
            stderr="",
        ),
        _execution(
            name=RMUTL_get_run_name(4),
            rc=16,
            stdout="\n REASON:X'A8'",
            stderr="",
        ),
        _execution(
            name=RMUTL_get_run_name(5),
            rc=16,
            stdout=" ABC \n REASON:   X 'A8'",
            stderr="",
        ),
        _execution(
            name=RMUTL_get_run_name(6),
            rc=rmutl_response.rc,
            stdout=rmutl_response.stdout,
            stderr=rmutl_response.stderr,
        ),
    ]
    expected_details = ("AUTOINIT", "UNKNOWN")
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


def test_run_rmutl_rc16_error():
    global_catalog.MVSCmd.execute = MagicMock(
        return_value=MVSCmdResponse(rc=16, stdout=" ABC \n REASON: X'12'", stderr="")
    )
    global_catalog._get_rmutl_dds = MagicMock(return_value=[])

    expected_executions = [
        _execution(
            name=RMUTL_update_run_name(1),
            rc=16,
            stdout=" ABC \n REASON: X'12'",
            stderr=""
        )
    ]

    error_raised = False
    try:
        global_catalog._run_dfhrmutl(
            location="DATA.SET", sdfhload="SDFH.LOAD", cmd="HI"
        )
    except MVSExecutionException as e:
        error_raised = True
        assert e.message == "DFHRMUTL failed with RC 16 - REASON:X'12'"
        assert e.executions == expected_executions

    assert error_raised is True


def test_run_rmutl_many_rc16_error():
    global_catalog.MVSCmd.execute = MagicMock(
        side_effect=[
            MVSCmdResponse(rc=16, stdout=" ABC \n REASON: X'A8'", stderr=""),
            MVSCmdResponse(rc=16, stdout="\n\n\n REASON: X'A8'", stderr=""),
            MVSCmdResponse(rc=16, stdout="REASON:X'B2'", stderr=""),
        ]
    )
    global_catalog._get_rmutl_dds = MagicMock(return_value=[])

    expected_executions = [
        _execution(name=RMUTL_update_run_name(1), rc=16, stdout=" ABC \n REASON: X'A8'", stderr=""),
        _execution(name=RMUTL_update_run_name(2), rc=16, stdout="\n\n\n REASON: X'A8'", stderr=""),
        _execution(name=RMUTL_update_run_name(3), rc=16, stdout="REASON:X'B2'", stderr=""),
    ]

    error_raised = False
    try:
        global_catalog._run_dfhrmutl(
            location="DATA.SET", sdfhload="SDFH.LOAD", cmd="HI"
        )
    except MVSExecutionException as e:
        error_raised = True
        assert e.message == "DFHRMUTL failed with RC 16 - REASON:X'B2'"
        assert e.executions == expected_executions

    assert error_raised is True


def test_run_rmutl_many_rc_error():
    global_catalog.MVSCmd.execute = MagicMock(
        side_effect=[
            MVSCmdResponse(rc=16, stdout=" ABC \n REASON: X'A8'", stderr=""),
            MVSCmdResponse(rc=16, stdout="\n\n\n REASON: X'A8'", stderr=""),
            MVSCmdResponse(rc=15, stdout="REASON:X'A8'", stderr=""),
        ]
    )
    global_catalog._get_rmutl_dds = MagicMock(return_value=[])

    expected_executions = [
        _execution(name=RMUTL_update_run_name(1), rc=16, stdout=" ABC \n REASON: X'A8'", stderr=""),
        _execution(name=RMUTL_update_run_name(2), rc=16, stdout="\n\n\n REASON: X'A8'", stderr=""),
        _execution(name=RMUTL_update_run_name(3), rc=15, stdout="REASON:X'A8'", stderr="")
    ]

    error_raised = False
    try:
        global_catalog._run_dfhrmutl(
            location="DATA.SET", sdfhload="SDFH.LOAD", cmd="HI"
        )
    except MVSExecutionException as e:
        error_raised = True
        assert e.message == "DFHRMUTL failed with RC 15"
        assert e.executions == expected_executions

    assert error_raised is True


def test_run_rmutl_rc_not_0():
    global_catalog.MVSCmd.execute = MagicMock(
        return_value=MVSCmdResponse(rc=123, stdout="", stderr="")
    )
    global_catalog._get_rmutl_dds = MagicMock(return_value=[])

    expected_executions = [_execution(name=RMUTL_update_run_name(1), rc=123, stdout="", stderr="")]

    error_raised = False
    try:
        global_catalog._run_dfhrmutl(
            location="DATA.SET", sdfhload="SDFH.LOAD", cmd="HI"
        )
    except MVSExecutionException as e:
        error_raised = True
        assert e.message == "DFHRMUTL failed with RC 123"
        assert e.executions == expected_executions

    assert error_raised is True

def test_run_rmutl_failed_while_running_mvscmd():
    global_catalog.MVSCmd.execute = MagicMock(
        return_value = MVSCmdResponse(
            rc = 123, 
            stdout = global_catalog.DFHRMUTL_PROGRAM_HEADER, 
            stderr = global_catalog.SUBPROCESS_EXIT_MESSAGE
        )
    )
    global_catalog._get_rmutl_dds = MagicMock(return_value=[])

    expected_executions = [
        _execution(
            name=RMUTL_update_run_name(1), 
            rc=123, stdout=global_catalog.DFHRMUTL_PROGRAM_HEADER, 
            stderr=global_catalog.SUBPROCESS_EXIT_MESSAGE
        )
    ]

    actual_executions = global_catalog._run_dfhrmutl(
            location="DATA.SET", sdfhload="SDFH.LOAD", cmd="HI"
        )

    assert actual_executions == expected_executions
