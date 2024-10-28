# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023,2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils._data_set import CYLINDERS, MEGABYTES

from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.data_set_helper import (
    PYTHON_LANGUAGE_FEATURES_MESSAGE,
    RMUTL_get_run_name,
    RMUTL_stdout,
    RMUTL_update_run_name,
    get_sample_job_output as JOB_OUTPUT
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


def test_global_catalog_get_records_autoinit_unknown():
    stdout = RMUTL_stdout("AUTOINIT", "UNKNOWN")
    resp = global_catalog._get_catalog_records(stdout=stdout)
    assert resp == ("AUTOINIT", "UNKNOWN")


def test_global_catalog_get_records_autoasis_emergency():
    stdout = RMUTL_stdout("AUTOASIS", "EMERGENCY")
    resp = global_catalog._get_catalog_records(stdout=stdout)
    assert resp == ("AUTOASIS", "EMERGENCY")


def test_global_catalog_get_records_autocold_emergency():
    stdout = RMUTL_stdout("AUTOCOLD", "EMERGENCY")
    resp = global_catalog._get_catalog_records(stdout=stdout)
    assert resp == ("AUTOCOLD", "EMERGENCY")


def test_global_catalog_run_rmutl_with_cmd():
    executions = [
        [],
        _execution(
            name=RMUTL_update_run_name(1),
            rc=0,
            stdout="",
            stderr="CC"
        )
    ]

    global_catalog._execute_dfhrmutl = MagicMock(
        return_value=(
            JOB_OUTPUT(),
            []
        ))

    result = global_catalog._run_dfhrmutl(
        location="DATA.SET", sdfhload="SDFH.LOAD", cmd="HI"
    )

    assert result == executions


def test_global_catalog_run_rmutl_with_cmd_and_failure():
    executions = [
        [],
        _execution(
            name=RMUTL_update_run_name(1),
            rc=16,
            stdout=" ABC \n REASON: X'A8'",
            stderr="CC",
        ),
        [],
        _execution(
            name=RMUTL_update_run_name(2),
            rc=0,
            stdout="",
            stderr="CC",
        ),
    ]
    global_catalog._execute_dfhrmutl = MagicMock(
        side_effect=[
            (JOB_OUTPUT(" ABC \n REASON: X'A8'", 16), []),
            (JOB_OUTPUT(), [])
        ])
    result = global_catalog._run_dfhrmutl(
        location="DATA.SET", sdfhload="SDFH.LOAD", cmd="HI"
    )

    assert result == executions


def test_global_catalog_run_rmutl_no_cmd():
    rmutl_stdout = RMUTL_stdout("AUTOASIS", "EMERGENCY")

    global_catalog._execute_dfhrmutl = MagicMock(
        return_value=(
            JOB_OUTPUT(rmutl_stdout),
            []
        ))

    expected_executions = [
        [],
        _execution(
            name=RMUTL_get_run_name(1),
            rc=0,
            stdout=rmutl_stdout,
            stderr="CC",
        )
    ]
    expected_details = ("AUTOASIS", "EMERGENCY")
    actual_executions, actual_details = global_catalog._run_dfhrmutl(
        location="DATA.SET", sdfhload="SDFH.LOAD"
    )

    assert actual_executions == expected_executions
    assert actual_details == expected_details


def test_global_catalog_run_rmutl_no_cmd_with_failure():
    rmutl_stdout = RMUTL_stdout("AUTOASIS", "EMERGENCY")

    expected_executions = [
        [],
        _execution(
            name=RMUTL_get_run_name(1),
            rc=16,
            stdout=" ABC \n REASON: X'A8'",
            stderr="CC",
        ),
        [],
        _execution(
            name=RMUTL_get_run_name(2),
            rc=0,
            stdout=rmutl_stdout,
            stderr="CC",
        ),
    ]
    expected_details = ("AUTOASIS", "EMERGENCY")
    global_catalog._execute_dfhrmutl = MagicMock(
        side_effect=[
            (JOB_OUTPUT(" ABC \n REASON: X'A8'", 16), []),
            (JOB_OUTPUT(rmutl_stdout), [])
        ]
    )
    actual_executions, actual_details = global_catalog._run_dfhrmutl(
        location="DATA.SET", sdfhload="SDFH.LOAD"
    )

    assert actual_executions == expected_executions
    assert actual_details == expected_details


def test_global_catalog_run_rmutl_no_cmd_many_failures():
    rmutl_stdout = RMUTL_stdout("AUTOINIT", "UNKNOWN")

    expected_executions = [
        [],
        _execution(
            name=RMUTL_get_run_name(1),
            rc=16,
            stdout=" ABC \n REASON: X'A8'",
            stderr="CC",
        ),
        [],
        _execution(
            name=RMUTL_get_run_name(2),
            rc=16,
            stdout="\n\n\n REASON: X'A8'",
            stderr="CC",
        ),
        [],
        _execution(
            name=RMUTL_get_run_name(3),
            rc=16,
            stdout="REASON:X'A8'",
            stderr="CC",
        ),
        [],
        _execution(
            name=RMUTL_get_run_name(4),
            rc=16,
            stdout="\n REASON:X'A8'",
            stderr="CC",
        ),
        [],
        _execution(
            name=RMUTL_get_run_name(5),
            rc=16,
            stdout=" ABC \n REASON:   X 'A8'",
            stderr="CC",
        ),
        [],
        _execution(
            name=RMUTL_get_run_name(6),
            rc=0,
            stdout=rmutl_stdout,
            stderr="CC",
        ),
    ]
    expected_details = ("AUTOINIT", "UNKNOWN")
    global_catalog._execute_dfhrmutl = MagicMock(
        side_effect=[
            (JOB_OUTPUT(" ABC \n REASON: X'A8'", 16), []),
            (JOB_OUTPUT("\n\n\n REASON: X'A8'", 16), []),
            (JOB_OUTPUT("REASON:X'A8'", 16), []),
            (JOB_OUTPUT("\n REASON:X'A8'", 16), []),
            (JOB_OUTPUT(" ABC \n REASON:   X 'A8'", 16), []),
            (JOB_OUTPUT(rmutl_stdout), [])
        ]
    )
    global_catalog._get_rmutl_dds = MagicMock(return_value=[])
    actual_executions, actual_details = global_catalog._run_dfhrmutl(
        location="DATA.SET", sdfhload="SDFH.LOAD"
    )

    assert actual_executions == expected_executions
    assert actual_details == expected_details


def test_global_catalog_run_rmutl_rc16_error():
    global_catalog._execute_dfhrmutl = MagicMock(
        return_value=(JOB_OUTPUT(" ABC \n REASON: X'12'", 16), [])
    )

    expected_executions = [
        [],
        _execution(
            name=RMUTL_update_run_name(1),
            rc=16,
            stdout=" ABC \n REASON: X'12'",
            stderr="CC"
        )
    ]

    with pytest.raises(MVSExecutionException) as e:
        global_catalog._run_dfhrmutl(
            location="DATA.SET", sdfhload="SDFH.LOAD", cmd="HI"
        )
        assert e.message == "DFHRMUTL failed with RC 16 - REASON:X'12'"
        assert e.executions == expected_executions


def test_global_catalog_run_rmutl_many_rc16_error():
    global_catalog._execute_dfhrmutl = MagicMock(
        side_effect=[
            (JOB_OUTPUT(" ABC \n REASON: X'A8'", 16), []),
            (JOB_OUTPUT("\n\n\n REASON: X'A8'", 16), []),
            (JOB_OUTPUT("REASON:X'B2'", 16), [])
        ]
    )

    expected_executions = [
        [], _execution(name=RMUTL_update_run_name(1), rc=16, stdout=" ABC \n REASON: X'A8'", stderr="CC"),
        [], _execution(name=RMUTL_update_run_name(2), rc=16, stdout="\n\n\n REASON: X'A8'", stderr="CC"),
        [], _execution(name=RMUTL_update_run_name(3), rc=16, stdout="REASON:X'B2'", stderr="CC"),
    ]

    with pytest.raises(MVSExecutionException) as e:
        global_catalog._run_dfhrmutl(
            location="DATA.SET", sdfhload="SDFH.LOAD", cmd="HI"
        )
        assert e.message == "DFHRMUTL failed with RC 16 - REASON:X'B2'"
        assert e.executions == expected_executions


def test_global_catalog_run_rmutl_many_rc_error():
    global_catalog._execute_dfhrmutl = MagicMock(
        side_effect=[
            (JOB_OUTPUT(" ABC \n REASON: X'A8'", 16), []),
            (JOB_OUTPUT("\n\n\n REASON: X'A8'", 16), []),
            (JOB_OUTPUT("REASON:X'A8'", 15), [])
        ]
    )

    expected_executions = [
        [], _execution(name=RMUTL_update_run_name(1), rc=16, stdout=" ABC \n REASON: X'A8'", stderr="CC"),
        [], _execution(name=RMUTL_update_run_name(2), rc=16, stdout="\n\n\n REASON: X'A8'", stderr="CC"),
        [], _execution(name=RMUTL_update_run_name(3), rc=15, stdout="REASON:X'A8'", stderr="CC")
    ]

    with pytest.raises(MVSExecutionException) as e:
        global_catalog._run_dfhrmutl(
            location="DATA.SET", sdfhload="SDFH.LOAD", cmd="HI"
        )
        assert e.message == "DFHRMUTL failed with RC 15"
        assert e.executions == expected_executions


def test_global_catalog_run_rmutl_rc_not_0():
    global_catalog._execute_dfhrmutl = MagicMock(
        return_value=(JOB_OUTPUT(rc=123), [])
    )
    expected_executions = [[], _execution(name=RMUTL_update_run_name(1), rc=123, stdout="", stderr="CC")]

    with pytest.raises(MVSExecutionException) as e:
        global_catalog._run_dfhrmutl(
            location="DATA.SET", sdfhload="SDFH.LOAD", cmd="HI"
        )
        assert e.message == "DFHRMUTL failed with RC 123"
        assert e.executions == expected_executions
