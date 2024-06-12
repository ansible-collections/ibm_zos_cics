# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023,2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function
from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.data_set_helper import (
    PYTHON_LANGUAGE_FEATURES_MESSAGE,
    IDCAMS_create_already_exists_stdout,
    IDCAMS_create_stdout,
    IDCAMS_delete_not_found,
    IDCAMS_delete,
    IDCAMS_run_cmd,
    IEFBR14_get_run_name,
    LISTDS_data_set,
    LISTDS_data_set_doesnt_exist,
    LISTDS_member_doesnt_exist,
    LISTDS_run_name
)
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.dd_statement import DatasetDefinition
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.zos_mvs_raw import MVSCmdResponse
__metaclass__ = type
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import _data_set_utils as data_set_utils
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils._response import MVSExecutionException, _execution
import pytest
import sys

try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock


def test_unit_size_m():
    unit = "M"
    unit_string = data_set_utils._get_dataset_size_unit(unit)
    assert unit_string == "MEGABYTES"


def test_unit_size_k():
    unit = "K"
    unit_string = data_set_utils._get_dataset_size_unit(unit)
    assert unit_string == "KILOBYTES"


def test_unit_size_cyl():
    unit = "CYL"
    unit_string = data_set_utils._get_dataset_size_unit(unit)
    assert unit_string == "CYLINDERS"


def test_unit_size_rec():
    unit = "REC"
    unit_string = data_set_utils._get_dataset_size_unit(unit)
    assert unit_string == "RECORDS"


def test_unit_size_trk():
    unit = "TRK"
    unit_string = data_set_utils._get_dataset_size_unit(unit)
    assert unit_string == "TRACKS"


def test_unit_size_bad_unit():
    unit = "FISHES"
    unit_string = data_set_utils._get_dataset_size_unit(unit)
    assert unit_string == "MEGABYTES"


def test_unit_size_empty():
    unit = ""
    unit_string = data_set_utils._get_dataset_size_unit(unit)
    assert unit_string == "MEGABYTES"


def test__run_idcams_create():
    location = "ANSIBIT.CICS.IYTWYD03.DFHGCD"
    rc = 0
    stdout = IDCAMS_create_stdout(location)
    stderr = ""
    data_set_utils._execute_idcams = MagicMock(return_value=MVSCmdResponse(rc, stdout, stderr))

    cmd = IDCAMS_run_cmd(location)

    result_exececutions = data_set_utils._run_idcams(
        cmd=cmd,
        name="Create Catalog",
        location=location,
        delete=False)

    assert len(result_exececutions) == 1
    assert result_exececutions[0] == {
        "name": "IDCAMS - Create Catalog - Run 1",
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr,
    }


def test__run_idcams_create_exists():
    location = "ANSIBIT.CICS.IYTWYD01.DFHGCD"
    rc = 12
    stdout = IDCAMS_create_already_exists_stdout(location)
    stderr = ""
    data_set_utils._execute_idcams = MagicMock(return_value=MVSCmdResponse(rc, stdout, stderr))

    cmd = IDCAMS_run_cmd(location)

    result_exececutions = data_set_utils._run_idcams(
        cmd=cmd,
        name="Create Catalog",
        location=location,
        delete=False)

    assert len(result_exececutions) == 1
    assert result_exececutions[0] == {
        "name": "IDCAMS - Create Catalog - Run 1",
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr,
    }


def test__run_idcams_delete():
    location = "ANSIBIT.CICS.IYTWYD03.DFHGCD"
    rc = 0
    stdout = IDCAMS_delete(location)
    stderr = ""
    data_set_utils._execute_idcams = MagicMock(return_value=MVSCmdResponse(rc, stdout, stderr))

    cmd = '''
        DELETE {0}
    '''.format(location)

    result_exececutions = data_set_utils._run_idcams(
        cmd=cmd,
        name="Remove Catalog",
        location=location,
        delete=True)

    assert len(result_exececutions) == 1
    assert result_exececutions[0] == {
        "name": "IDCAMS - Remove Catalog - Run 1",
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr,
    }


def test__run_idcams_delete_no_exist():
    location = "ANSIBIT.CICS.IYTWYD02.DFHGCD"
    rc = 8
    stdout = IDCAMS_delete_not_found(location)
    stderr = ""
    data_set_utils._execute_idcams = MagicMock(return_value=MVSCmdResponse(rc, stdout, stderr))

    cmd = '''
        DELETE {0}
    '''.format(location)

    result_exececutions = data_set_utils._run_idcams(
        cmd=cmd,
        name="Remove Catalog",
        location=location,
        delete=True)

    assert len(result_exececutions) == 1
    assert result_exececutions[0] == {
        "name": "IDCAMS - Remove Catalog - Run 1",
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr,
    }


def test__run_idcams_bad_return_code_when_creating():
    location = "ANSIBIT.CICS.IYTWYD02.DFHGCD"
    rc = 99
    stdout = IDCAMS_create_stdout(location)
    stderr = ""
    data_set_utils._execute_idcams = MagicMock(return_value=MVSCmdResponse(rc, stdout, stderr))

    cmd = '''
    DEFINE CLUSTER -
        (NAME({0}) -
        INDEXED                      -
        MEGABYTES(5 1)             -
        SHR(2)              -
        FREESPACE(10 10)              -
        RECORDSIZE(4089 32760)       -
        REUSE)              -
        DATA                           -
        (NAME({0}.DATA)  -
        CONTROLINTERVALSIZE(32768)    -
        KEYS(52 0))  -
        INDEX                          -
        (NAME({0}.INDEX))
    '''.format(location)

    expected_executions = [
        _execution(name="IDCAMS - Create Catalog - Run 1", rc=rc, stdout=stdout, stderr=stderr)
    ]

    try:
        data_set_utils._run_idcams(
            cmd=cmd,
            name="Create Catalog",
            location=location,
            delete=False)
    except MVSExecutionException as e:
        assert e.message == "RC 99 when creating data set"
        assert e.executions == expected_executions
    else:
        assert False


def test__run_idcams_bad_return_code_when_deleting():
    location = "ANSIBIT.CICS.IYTWYD02.DFHGCD"
    rc = 99
    stdout = IDCAMS_delete(location)
    stderr = ""
    data_set_utils._execute_idcams = MagicMock(return_value=MVSCmdResponse(rc, stdout, stderr))

    cmd = '''
        DELETE {0}
    '''.format(location)

    expected_executions = [
        _execution(name="IDCAMS - Remove Catalog - Run 1", rc=rc, stdout=stdout, stderr=stderr)
    ]

    try:
        data_set_utils._run_idcams(
            cmd=cmd,
            name="Remove Catalog",
            location=location,
            delete=True)
    except MVSExecutionException as e:
        assert e.message == "RC 99 when deleting data set"
        assert e.executions == expected_executions
    else:
        assert False


def test__run_listds_exists_vsam():
    location = "ANSIBIT.CICS.TESTS.A365D7A.DFHGCD"
    rc = 0
    stdout = LISTDS_data_set(location, "VSAM")
    stderr = ""
    data_set_utils._execute_listds = MagicMock(return_value=MVSCmdResponse(rc, stdout, stderr))

    result_exececutions, exists, ds_org = data_set_utils._run_listds(location)

    assert len(result_exececutions) == 1
    assert result_exececutions[0] == {
        "name": LISTDS_run_name(1),
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr,
    }
    assert exists is True
    assert ds_org == "VSAM"


def test__run_listds_exists_sequential():
    location = "ANSIBIT.CICS.TESTS.A365D7A.DFHGCD"
    rc = 0
    stdout = LISTDS_data_set(location, "PS")
    stderr = ""
    data_set_utils._execute_listds = MagicMock(return_value=MVSCmdResponse(rc, stdout, stderr))

    result_exececutions, exists, ds_org = data_set_utils._run_listds(location)

    assert len(result_exececutions) == 1
    assert result_exececutions[0] == {
        "name": LISTDS_run_name(1),
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr,
    }
    assert exists is True
    assert ds_org == "Sequential"


def test__run_listds_exists_partitioned():
    location = "ANSIBIT.CICS.TESTS.A365D7A.DFHGCD"
    rc = 0
    stdout = LISTDS_data_set(location, "PO")
    stderr = ""
    data_set_utils._execute_listds = MagicMock(return_value=MVSCmdResponse(rc, stdout, stderr))

    result_exececutions, exists, ds_org = data_set_utils._run_listds(location)

    assert len(result_exececutions) == 1
    assert result_exececutions[0] == {
        "name": LISTDS_run_name(1),
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr,
    }
    assert exists is True
    assert ds_org == "Partitioned"


def test__run_listds_exists_indexed_sequential():
    location = "ANSIBIT.CICS.TESTS.A365D7A.DFHGCD"
    rc = 0
    stdout = LISTDS_data_set(location, "IS")
    stderr = ""
    data_set_utils._execute_listds = MagicMock(return_value=MVSCmdResponse(rc, stdout, stderr))

    result_exececutions, exists, ds_org = data_set_utils._run_listds(location)

    assert len(result_exececutions) == 1
    assert result_exececutions[0] == {
        "name": LISTDS_run_name(1),
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr,
    }
    assert exists is True
    assert ds_org == "Indexed Sequential"


def test__run_listds_exists_direct_access():
    location = "ANSIBIT.CICS.TESTS.A365D7A.DFHGCD"
    rc = 0
    stdout = LISTDS_data_set(location, "DA")
    stderr = ""
    data_set_utils._execute_listds = MagicMock(return_value=MVSCmdResponse(rc, stdout, stderr))

    result_exececutions, exists, ds_org = data_set_utils._run_listds(location)

    assert len(result_exececutions) == 1
    assert result_exececutions[0] == {
        "name": LISTDS_run_name(1),
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr,
    }
    assert exists is True
    assert ds_org == "Direct Access"


def test__run_listds_exists_other():
    location = "ANSIBIT.CICS.TESTS.A365D7A.DFHGCD"
    rc = 0
    stdout = LISTDS_data_set(location, "??")
    stderr = ""
    data_set_utils._execute_listds = MagicMock(return_value=MVSCmdResponse(rc, stdout, stderr))

    result_exececutions, exists, ds_org = data_set_utils._run_listds(location)

    assert len(result_exececutions) == 1
    assert result_exececutions[0] == {
        "name": LISTDS_run_name(1),
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr,
    }
    assert exists is True
    assert ds_org == "Other"


def test__run_listds_exists_unspecified():
    location = "ANSIBIT.CICS.TESTS.A365D7A.DFHGCD"
    rc = 0
    stdout = LISTDS_data_set(location, "**")
    stderr = ""
    data_set_utils._execute_listds = MagicMock(return_value=MVSCmdResponse(rc, stdout, stderr))

    result_exececutions, exists, ds_org = data_set_utils._run_listds(location)

    assert len(result_exececutions) == 1
    assert result_exececutions[0] == {
        "name": LISTDS_run_name(1),
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr,
    }
    assert exists is True
    assert ds_org == "Unspecified"


def test__run_listds_exists_unknown():
    location = "ANSIBIT.CICS.TESTS.A365D7A.DFHGCD"
    rc = 0
    stdout = LISTDS_data_set(location, "NOT_REAL_DSORG")
    stderr = ""
    data_set_utils._execute_listds = MagicMock(return_value=MVSCmdResponse(rc, stdout, stderr))

    result_exececutions, exists, ds_org = data_set_utils._run_listds(location)

    assert len(result_exececutions) == 1
    assert result_exececutions[0] == {
        "name": LISTDS_run_name(1),
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr,
    }
    assert exists is True
    assert ds_org == "Unspecified"


def test__run_listds_bad_rc():
    location = "ANSIBIT.CICS.TESTS.A365D7A.DFHGCD"
    name = LISTDS_run_name(1)
    rc = 16
    stdout = LISTDS_data_set(location, "VSAM")
    stderr = ""
    data_set_utils._execute_listds = MagicMock(return_value=MVSCmdResponse(rc, stdout, stderr))

    expected_executions = [_execution(name=name, rc=rc, stdout=stdout, stderr=stderr)]

    try:
        data_set_utils._run_listds(location)
    except MVSExecutionException as e:
        assert e.message == "RC 16 running LISTDS Command"
        assert e.executions == expected_executions
    else:
        assert False


def test__run_listds_not_exists():
    location = "ANSIBIT.CICS.TESTS.A294D11B.DFHGaCD"
    rc = 8
    stdout = LISTDS_data_set_doesnt_exist(location)
    stderr = ""
    data_set_utils._execute_listds = MagicMock(return_value=MVSCmdResponse(rc, stdout, stderr))

    result_exececutions, exists, ds_org = data_set_utils._run_listds(location)

    assert len(result_exececutions) == 1
    assert result_exececutions[0] == {
        "name": LISTDS_run_name(1),
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr,
    }
    assert exists is False
    assert ds_org == "NONE"


def test__run_listds_member_not_exists():
    base_ds_name = "ANSIBIT.CICS.TESTS.A294D11B"
    member_name = "MEMB"
    location = "{0}({1})".format(base_ds_name, member_name)
    rc = 4
    stdout = LISTDS_member_doesnt_exist(base_ds_name, member_name)
    stderr = ""
    data_set_utils._execute_listds = MagicMock(return_value=MVSCmdResponse(rc, stdout, stderr))

    result_exececutions, exists, ds_org = data_set_utils._run_listds(location)

    assert len(result_exececutions) == 1
    assert result_exececutions[0] == {
        "name": LISTDS_run_name(1),
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr,
    }
    assert exists is False
    assert ds_org == "NONE"


def test__run_listds_with_no_zoau_response():
    rc = 0
    stdout = ""
    stderr = ""
    data_set_utils._execute_listds = MagicMock(return_value=MVSCmdResponse(rc, stdout, stderr))

    expected_executions = [
        _execution(name=LISTDS_run_name(1), rc=rc, stdout=stdout, stderr=stderr),
        _execution(name=LISTDS_run_name(2), rc=rc, stdout=stdout, stderr=stderr),
        _execution(name=LISTDS_run_name(3), rc=rc, stdout=stdout, stderr=stderr),
        _execution(name=LISTDS_run_name(4), rc=rc, stdout=stdout, stderr=stderr),
        _execution(name=LISTDS_run_name(5), rc=rc, stdout=stdout, stderr=stderr),
        _execution(name=LISTDS_run_name(6), rc=rc, stdout=stdout, stderr=stderr),
        _execution(name=LISTDS_run_name(7), rc=rc, stdout=stdout, stderr=stderr),
        _execution(name=LISTDS_run_name(8), rc=rc, stdout=stdout, stderr=stderr),
        _execution(name=LISTDS_run_name(9), rc=rc, stdout=stdout, stderr=stderr),
        _execution(name=LISTDS_run_name(10), rc=rc, stdout=stdout, stderr=stderr)
    ]

    try:
        data_set_utils._run_listds("LOCATION THATS NOT IN STDOUT")
    except MVSExecutionException as e:
        assert e.message == "LISTDS Command output not recognised"
        assert e.executions == expected_executions
    else:
        assert False


@pytest.mark.skipif(sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE)
def test__run_iefbr14():
    rc = 0
    stdout = "stdout"
    stderr = "stderr"
    data_set_utils.MVSCmd.execute = MagicMock(return_value=MVSCmdResponse(rc, stdout, stderr))

    definition = DatasetDefinition(
        dataset_name="DFHTEST",
        block_size=4096,
        record_length=4096,
        record_format="FB",
        disposition="NEW",
        normal_disposition="catalog",
        conditional_disposition="delete",
        primary=15,
        secondary=3,
        primary_unit="MB",
        type="SEQ"
    )

    result_exececutions = data_set_utils._run_iefbr14(
        ddname="DFHIEFT",
        definition=definition
    )

    assert len(result_exececutions) == 1
    assert result_exececutions[0] == {
        "name": "IEFBR14 - DFHIEFT - Run 1",
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr,
    }


def test__run_iefbr14_bad_rc():
    rc = 99
    stdout = "stdout"
    stderr = "stderr"
    data_set_utils.MVSCmd.execute = MagicMock(return_value=MVSCmdResponse(rc, stdout, stderr))

    definition = DatasetDefinition(
        dataset_name="DFHTEST",
        block_size=4096,
        record_length=4096,
        record_format="FB",
        disposition="NEW",
        normal_disposition="catalog",
        conditional_disposition="delete",
        primary=15,
        secondary=3,
        primary_unit="MB",
        type="SEQ"
    )

    expected_executions = [{
        "name": "IEFBR14 - DFHIEFT - Run 1",
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr,
    }]

    try:
        data_set_utils._run_iefbr14(
            ddname="DFHIEFT",
            definition=definition
        )
    except MVSExecutionException as e:
        assert e.message == "RC {0} when creating sequential data set".format(99)
        assert e.executions == expected_executions
    else:
        assert False


def test__run_iefbr14_no_response():
    rc = 0
    stdout = ""
    stderr = ""
    data_set_utils.MVSCmd.execute = MagicMock(return_value=MVSCmdResponse(rc, stdout, stderr))

    definition = DatasetDefinition(
        dataset_name="DFHTEST",
        block_size=4096,
        record_length=4096,
        record_format="FB",
        disposition="NEW",
        normal_disposition="catalog",
        conditional_disposition="delete",
        primary=15,
        secondary=3,
        primary_unit="MB",
        type="SEQ"
    )

    expected_executions = [
        _execution(name=IEFBR14_get_run_name(1), rc=rc, stdout=stdout, stderr=stderr),
        _execution(name=IEFBR14_get_run_name(2), rc=rc, stdout=stdout, stderr=stderr),
        _execution(name=IEFBR14_get_run_name(3), rc=rc, stdout=stdout, stderr=stderr),
        _execution(name=IEFBR14_get_run_name(4), rc=rc, stdout=stdout, stderr=stderr),
        _execution(name=IEFBR14_get_run_name(5), rc=rc, stdout=stdout, stderr=stderr),
        _execution(name=IEFBR14_get_run_name(6), rc=rc, stdout=stdout, stderr=stderr),
        _execution(name=IEFBR14_get_run_name(7), rc=rc, stdout=stdout, stderr=stderr),
        _execution(name=IEFBR14_get_run_name(8), rc=rc, stdout=stdout, stderr=stderr),
        _execution(name=IEFBR14_get_run_name(9), rc=rc, stdout=stdout, stderr=stderr),
        _execution(name=IEFBR14_get_run_name(10), rc=rc, stdout=stdout, stderr=stderr)
    ]

    try:
        data_set_utils._run_iefbr14(
            ddname="DFHIEFT",
            definition=definition
        )
    except MVSExecutionException as e:
        assert e.message == "IEFBR14 Command output not recognised"
        assert e.executions == expected_executions
    else:
        assert False


@pytest.mark.skipif(sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE)
def test__build_idcams_volumes():
    volumes = ["vserv1", "vserv2", "vserv3"]

    assert data_set_utils._build_idcams_volumes(volumes) == " -\n    VOLUMES(vserv1 vserv2 vserv3)"


def test__read_data_set_content():
    rc = 0
    stdout = "stdout"
    stderr = "stderr"

    data_set_name = "TEST.DATA.SET"
    data_set_utils._execute_command = MagicMock(return_value=(rc, stdout, stderr))
    result_executions, result_data_set_content = data_set_utils._read_data_set_content(data_set_name)

    assert result_data_set_content == stdout
    assert result_executions[0] == {
        "name": "Read data set {0}".format(data_set_name),
        "rc": 0,
        "stdout": stdout,
        "stderr": stderr
    }


def test__read_data_set_content_bad_rc():
    rc = 99
    stdout = "stdout"
    stderr = "stderr"

    data_set_name = "TEST.DATA.SET"
    data_set_utils._execute_command = MagicMock(return_value=(rc, stdout, stderr))

    expected_executions = [{
        "name": "Read data set {0}".format(data_set_name),
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr
    }]

    try:
        data_set_utils._read_data_set_content(data_set_name)
    except MVSExecutionException as e:
        assert e.message == "RC {0} when reading content from data set {1}".format(rc, data_set_name)
        assert e.executions == expected_executions
    else:
        assert False


def test__write_jcl_to_data_set():
    data_set_name = "TEST.DATA.SET"
    jcl = ""

    rc = 0
    stdout = ""
    stderr = ""
    data_set_utils._execute_command = MagicMock(return_value=(rc, stdout, stderr))

    expected_executions = [{
        "name": "Copy JCL contents to data set",
        "rc": 0,
        "stdout": "",
        "stderr": ""
    }]

    executions = data_set_utils._write_jcl_to_data_set(jcl, data_set_name)

    assert expected_executions == executions


def test__write_jcl_to_data_set_fail():
    data_set_name = "TEST.DATA.SET"
    jcl = ""
    rc = 99
    stdout = "cp failed"
    stderr = "stderr"
    data_set_utils._execute_command = MagicMock(return_value=(rc, stdout, stderr))

    expected_executions = [{
        "name": "Copy JCL contents to data set",
        "rc": 99,
        "stdout": "cp failed",
        "stderr": "stderr"
    }]

    with pytest.raises(MVSExecutionException) as e:
        data_set_utils._write_jcl_to_data_set(jcl, data_set_name)

    assert e.value.message == "Failed to copy JCL content to data set"
    assert e.value.executions == expected_executions
