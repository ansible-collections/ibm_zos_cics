# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function

from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.response import MVSExecutionException, _execution
from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.data_set_helper import ICETOOL_name, ICETOOL_stderr, ICETOOL_stdout
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.zos_mvs_raw import MVSCmdResponse
__metaclass__ = type
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import icetool
import pytest
try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock


NAME = "TEST.REGIONS.LCD"


def test__get_record_count_with_invalid_stdout():
    record_count = icetool._get_record_count("Some invalid STDOUT")
    expected = -1
    assert record_count == expected


def test__get_record_count_with_record_count_string():
    record_count = icetool._get_record_count("RECORD COUNT:  000000000000001")
    expected = 1
    assert record_count == expected


def test__get_record_count_with_icetool_stdout():
    record_count = icetool._get_record_count(ICETOOL_stdout(52))
    expected = 52
    assert record_count == expected


def test__get_zero_record_count_with_icetool_stdout():
    record_count = icetool._get_record_count(ICETOOL_stdout(0))
    expected = 0
    assert record_count == expected


def test__run_icetool():
    icetool._execute_icetool = MagicMock(return_value=MVSCmdResponse(rc=0, stdout=ICETOOL_stdout(52), stderr=ICETOOL_stderr()))
    executions, record_count = icetool._run_icetool(NAME)
    expected_record_count = 52
    expected_executions = [
        _execution(name=ICETOOL_name(1), rc=0, stdout=ICETOOL_stdout(52), stderr=ICETOOL_stderr()),
    ]
    assert record_count == expected_record_count
    assert executions == expected_executions


def test__run_icetool_rc_16_no_reason():
    icetool._execute_icetool = MagicMock(return_value=MVSCmdResponse(rc=16, stdout="", stderr=ICETOOL_stderr()))
    with pytest.raises(MVSExecutionException) as e_info:
        icetool._run_icetool(NAME)

    assert (e_info.value).message == "ICETOOL failed with RC 16"


def test__run_icetool_rc_nonzero():
    icetool._execute_icetool = MagicMock(return_value=MVSCmdResponse(rc=99, stdout="", stderr=ICETOOL_stderr()))
    with pytest.raises(MVSExecutionException) as e_info:
        icetool._run_icetool(NAME)

    assert (e_info.value).message == "ICETOOL failed with RC 99"


def test__run_icetool_with_no_zoau_response():
    rc = 0
    stdout = ""
    stderr = ""
    icetool._execute_icetool = MagicMock(return_value=MVSCmdResponse(rc=rc, stdout=stdout, stderr=stderr))

    expected_executions = [
        _execution(name=ICETOOL_name(1), rc=rc, stdout=stdout, stderr=stderr),
        _execution(name=ICETOOL_name(2), rc=rc, stdout=stdout, stderr=stderr),
        _execution(name=ICETOOL_name(3), rc=rc, stdout=stdout, stderr=stderr),
        _execution(name=ICETOOL_name(4), rc=rc, stdout=stdout, stderr=stderr),
        _execution(name=ICETOOL_name(5), rc=rc, stdout=stdout, stderr=stderr),
        _execution(name=ICETOOL_name(6), rc=rc, stdout=stdout, stderr=stderr),
        _execution(name=ICETOOL_name(7), rc=rc, stdout=stdout, stderr=stderr),
        _execution(name=ICETOOL_name(8), rc=rc, stdout=stdout, stderr=stderr),
        _execution(name=ICETOOL_name(9), rc=rc, stdout=stdout, stderr=stderr),
        _execution(name=ICETOOL_name(10), rc=rc, stdout=stdout, stderr=stderr),
    ]

    try:
        icetool._run_icetool(NAME)
    except MVSExecutionException as e:
        assert e.message == "ICETOOL Command output not recognised"
        assert e.executions == expected_executions
