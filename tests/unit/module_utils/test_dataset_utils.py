# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function
from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.data_set_helper import (
    PYTHON_LANGUAGE_FEATURES_MESSAGE,
    IDCAMS_create_already_exists_stdout,
    IDCAMS_create_stdout,
    IDCAMS_delete_not_found,
    IDCAMS_delete_vsam,
    IDCAMS_run_cmd,
    LISTDS_data_set,
    LISTDS_data_set_doesnt_exist,
    LISTDS_run_name
)
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.dd_statement import DatasetDefinition
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.zos_mvs_raw import MVSCmdResponse
__metaclass__ = type
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import dataset_utils
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.response import _execution
import pytest
import sys

try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock


def test_unit_size_m():
    unit = "M"
    unit_string = dataset_utils._get_dataset_size_unit(unit)
    assert unit_string == "MEGABYTES"


def test_unit_size_k():
    unit = "K"
    unit_string = dataset_utils._get_dataset_size_unit(unit)
    assert unit_string == "KILOBYTES"


def test_unit_size_cyl():
    unit = "CYL"
    unit_string = dataset_utils._get_dataset_size_unit(unit)
    assert unit_string == "CYLINDERS"


def test_unit_size_rec():
    unit = "REC"
    unit_string = dataset_utils._get_dataset_size_unit(unit)
    assert unit_string == "RECORDS"


def test_unit_size_trk():
    unit = "TRK"
    unit_string = dataset_utils._get_dataset_size_unit(unit)
    assert unit_string == "TRACKS"


def test_unit_size_bad_unit():
    unit = "FISHES"
    unit_string = dataset_utils._get_dataset_size_unit(unit)
    assert unit_string == "MEGABYTES"


def test_unit_size_empty():
    unit = ""
    unit_string = dataset_utils._get_dataset_size_unit(unit)
    assert unit_string == "MEGABYTES"


def test__run_idcams_create():
    location = "ANSIBIT.CICS.IYTWYD03.DFHGCD"
    rc = 0
    stdout = IDCAMS_create_stdout(location)
    stderr = ""
    dataset_utils.idcams = MagicMock(return_value=[rc, stdout, stderr])

    cmd = IDCAMS_run_cmd(location)

    result_exececutions = dataset_utils._run_idcams(
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
    dataset_utils.idcams = MagicMock(return_value=[rc, stdout, stderr])

    cmd = IDCAMS_run_cmd(location)

    result_exececutions = dataset_utils._run_idcams(
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
    stdout = IDCAMS_delete_vsam(location)
    stderr = ""
    dataset_utils.idcams = MagicMock(return_value=[rc, stdout, stderr])

    cmd = '''
        DELETE {0}
    '''.format(location)

    result_exececutions = dataset_utils._run_idcams(
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
    dataset_utils.idcams = MagicMock(return_value=[rc, stdout, stderr])

    cmd = '''
        DELETE {0}
    '''.format(location)

    result_exececutions = dataset_utils._run_idcams(
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
    dataset_utils.idcams = MagicMock(return_value=[rc, stdout, stderr])

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
        dataset_utils._run_idcams(
            cmd=cmd,
            name="Create Catalog",
            location=location,
            delete=False)
    except Exception as e:
        assert e.args[0] == "RC 99 when creating data set"
        assert e.args[1] == expected_executions


def test__run_idcams_bad_return_code_when_deleting():
    location = "ANSIBIT.CICS.IYTWYD02.DFHGCD"
    rc = 99
    stdout = IDCAMS_delete_vsam(location)
    stderr = ""
    dataset_utils.idcams = MagicMock(return_value=[rc, stdout, stderr])

    cmd = '''
        DELETE {0}
    '''.format(location)

    expected_executions = [
        _execution(name="IDCAMS - Remove Catalog - Run 1", rc=rc, stdout=stdout, stderr=stderr)
    ]

    try:
        dataset_utils._run_idcams(
            cmd=cmd,
            name="Remove Catalog",
            location=location,
            delete=True)
    except Exception as e:
        assert e.args[0] == "RC 99 when deleting data set"
        assert e.args[1] == expected_executions


def test__run_listds_exists_vsam():
    location = "ANSIBIT.CICS.TESTS.A365D7A.DFHGCD"
    rc = 0
    stdout = LISTDS_data_set(location, "VSAM")
    stderr = ""
    dataset_utils.ikjeft01 = MagicMock(return_value=[rc, stdout, stderr])

    result_exececutions, result_status = dataset_utils._run_listds(location)

    assert len(result_exececutions) == 1
    assert result_exececutions[0] == {
        "name": LISTDS_run_name(1),
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr,
    }
    assert result_status == {
        "exists": True,
        "data_set_organization": "VSAM"
    }


def test__run_listds_exists_sequential():
    location = "ANSIBIT.CICS.TESTS.A365D7A.DFHGCD"
    rc = 0
    stdout = LISTDS_data_set(location, "PS")
    stderr = ""
    dataset_utils.ikjeft01 = MagicMock(return_value=[rc, stdout, stderr])

    result_exececutions, result_status = dataset_utils._run_listds(location)

    assert len(result_exececutions) == 1
    assert result_exececutions[0] == {
        "name": LISTDS_run_name(1),
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr,
    }
    assert result_status == {
        "exists": True,
        "data_set_organization": "Sequential"
    }


def test__run_listds_exists_partitioned():
    location = "ANSIBIT.CICS.TESTS.A365D7A.DFHGCD"
    rc = 0
    stdout = LISTDS_data_set(location, "PO")
    stderr = ""
    dataset_utils.ikjeft01 = MagicMock(return_value=[rc, stdout, stderr])

    result_exececutions, result_status = dataset_utils._run_listds(location)

    assert len(result_exececutions) == 1
    assert result_exececutions[0] == {
        "name": LISTDS_run_name(1),
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr,
    }
    assert result_status == {
        "exists": True,
        "data_set_organization": "Partitioned"
    }


def test__run_listds_exists_indexed_sequential():
    location = "ANSIBIT.CICS.TESTS.A365D7A.DFHGCD"
    rc = 0
    stdout = LISTDS_data_set(location, "IS")
    stderr = ""
    dataset_utils.ikjeft01 = MagicMock(return_value=[rc, stdout, stderr])

    result_exececutions, result_status = dataset_utils._run_listds(location)

    assert len(result_exececutions) == 1
    assert result_exececutions[0] == {
        "name": LISTDS_run_name(1),
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr,
    }
    assert result_status == {
        "exists": True,
        "data_set_organization": "Indexed Sequential"
    }


def test__run_listds_exists_direct_access():
    location = "ANSIBIT.CICS.TESTS.A365D7A.DFHGCD"
    rc = 0
    stdout = LISTDS_data_set(location, "DA")
    stderr = ""
    dataset_utils.ikjeft01 = MagicMock(return_value=[rc, stdout, stderr])

    result_exececutions, result_status = dataset_utils._run_listds(location)

    assert len(result_exececutions) == 1
    assert result_exececutions[0] == {
        "name": LISTDS_run_name(1),
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr,
    }
    assert result_status == {
        "exists": True,
        "data_set_organization": "Direct Access"
    }


def test__run_listds_exists_other():
    location = "ANSIBIT.CICS.TESTS.A365D7A.DFHGCD"
    rc = 0
    stdout = LISTDS_data_set(location, "??")
    stderr = ""
    dataset_utils.ikjeft01 = MagicMock(return_value=[rc, stdout, stderr])

    result_exececutions, result_status = dataset_utils._run_listds(location)

    assert len(result_exececutions) == 1
    assert result_exececutions[0] == {
        "name": LISTDS_run_name(1),
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr,
    }
    assert result_status == {
        "exists": True,
        "data_set_organization": "Other"
    }


def test__run_listds_exists_unspecified():
    location = "ANSIBIT.CICS.TESTS.A365D7A.DFHGCD"
    rc = 0
    stdout = LISTDS_data_set(location, "**")
    stderr = ""
    dataset_utils.ikjeft01 = MagicMock(return_value=[rc, stdout, stderr])

    result_exececutions, result_status = dataset_utils._run_listds(location)

    assert len(result_exececutions) == 1
    assert result_exececutions[0] == {
        "name": LISTDS_run_name(1),
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr,
    }
    assert result_status == {
        "exists": True,
        "data_set_organization": "Unspecified"
    }


def test__run_listds_bad_rc():
    location = "ANSIBIT.CICS.TESTS.A365D7A.DFHGCD"
    name = LISTDS_run_name(1)
    rc = 16
    stdout = LISTDS_data_set(location, "VSAM")
    stderr = ""
    dataset_utils.ikjeft01 = MagicMock(return_value=[rc, stdout, stderr])

    expected_executions = [_execution(name=name, rc=rc, stdout=stdout, stderr=stderr)]

    try:
        dataset_utils._run_listds(location)
    except Exception as e:
        assert e.args[0] == "RC 16 running LISTDS Command"
        assert e.args[1] == expected_executions


def test__run_listds_not_exists():
    location = "ANSIBIT.CICS.TESTS.A294D11B.DFHGaCD"
    rc = 8
    stdout = LISTDS_data_set_doesnt_exist(location)
    stderr = ""
    dataset_utils.ikjeft01 = MagicMock(return_value=[rc, stdout, stderr])

    result_exececutions, result_status = dataset_utils._run_listds(
        location)

    assert len(result_exececutions) == 1
    assert result_exececutions[0] == {
        "name": LISTDS_run_name(1),
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr,
    }
    assert result_status == {
        "exists": False,
        "data_set_organization": "NONE",
    }


def test__run_listds_with_no_zoau_response():
    rc = 0
    stdout = ""
    stderr = ""
    dataset_utils.ikjeft01 = MagicMock(return_value=[rc, stdout, stderr])

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
        dataset_utils._run_listds("LOCATION THATS NOT IN STDOUT")
    except Exception as e:
        assert e.args[0] == "LISTDS Command output not recognised"
        assert e.args[1] == expected_executions


@pytest.mark.skipif(sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE)
def test__run_iefbr14():
    rc = 0
    stdout = ""
    stderr = ""
    dataset_utils.MVSCmd.execute = MagicMock(return_value=MVSCmdResponse(rc, stdout, stderr))

    definition = DatasetDefinition(
        dataset_name="DFHTEST",
        block_size=4096,
        record_length=4096,
        record_format="FB",
        disposition="NEW",
        normal_disposition="catalog",
        conditional_disposition="delete",
        primary=15,
        primary_unit="MB",
        type="SEQ"
    )

    result_exececutions = dataset_utils._run_iefbr14(
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
