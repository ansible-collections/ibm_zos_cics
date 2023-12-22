# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import dataset_utils
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.response import _execution
try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock


def test_catalog_size_class():
    catalog_size = dataset_utils._dataset_size(unit="M", primary=10, secondary=1)
    assert catalog_size == {
        'unit': "M",
        'primary': 10,
        'secondary': 1
    }


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

    rc = 0
    stdout = (
        "1IDCAMS  SYSTEM SERVICES                                           TIME: 10:04:57  "
        "      06/29/23     PAGE      1\n"
        "0        \n"
        "    DEFINE CLUSTER -\n"
        "        (NAME(ANSIBIT.CICS.IYTWYD03.DFHGCD) -\n"
        "        INDEXED                      -\n"
        "        MEGABYTES(5 1)             -\n"
        "        SHR(2)              -\n"
        "        FREESPACE(10 10)              -\n"
        "        RECORDSIZE(4089 32760)       -\n"
        "        REUSE)              -\n"
        "        DATA                           -\n"
        "        (NAME(ANSIBIT.CICS.IYTWYD03.DFHGCD.DATA)  -\n"
        "        CONTROLINTERVALSIZE(32768)    -\n"
        "        KEYS(52 0))  -\n"
        "        INDEX                          -\n"
        "        (NAME(ANSIBIT.CICS.IYTWYD03.DFHGCD.INDEX))\n"
        "0IDC0508I DATA ALLOCATION STATUS FOR VOLUME P2P0D5 IS 0\n"
        "0IDC0509I INDEX ALLOCATION STATUS FOR VOLUME P2P0D5 IS 0\n"
        "IDC0181I STORAGECLASS USED IS STANDARD\n"
        "IDC0181I MANAGEMENTCLASS USED IS STANDARD\n"
        "0IDC0001I FUNCTION COMPLETED, HIGHEST CONDITION CODE WAS 0\n"
        "0        \n"
        "        \n"
        "0IDC0002I IDCAMS PROCESSING COMPLETE. MAXIMUM CONDITION CODE WAS 0")
    stderr = ""
    dataset_utils.idcams = MagicMock(return_value=[rc, stdout, stderr])

    cmd = '''
    DEFINE CLUSTER -
        (NAME(ANSIBIT.CICS.IYTWYD03.DFHGCD) -
        INDEXED                      -
        MEGABYTES(5 1)             -
        SHR(2)              -
        FREESPACE(10 10)              -
        RECORDSIZE(4089 32760)       -
        REUSE)              -
        DATA                           -
        (NAME(ANSIBIT.CICS.IYTWYD03.DFHGCD.DATA)  -
        CONTROLINTERVALSIZE(32768)    -
        KEYS(52 0))  -
        INDEX                          -
        (NAME(ANSIBIT.CICS.IYTWYD03.DFHGCD.INDEX))
    '''

    result_exececutions = dataset_utils._run_idcams(
        cmd=cmd,
        name="Create Catalog",
        location="ANSIBIT.CICS.IYTWYD03.DFHGCD",
        delete=False)

    assert len(result_exececutions) == 1
    assert result_exececutions[0] == {
        "name": "IDCAMS - Create Catalog - Run 1",
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr,
    }


def test__run_idcams_create_exists():

    rc = 12
    stdout = (
        "1IDCAMS  SYSTEM SERVICES                                           TIME: 10:04:51  "
        "      06/29/23     PAGE      1\n"
        "0        \n"
        "    DEFINE CLUSTER -\n"
        "        (NAME(ANSIBIT.CICS.IYTWYD01.DFHGCD) -\n"
        "        INDEXED                      -\n"
        "        MEGABYTES(5 1)             -\n"
        "        SHR(2)              -\n"
        "        FREESPACE(10 10)              -\n"
        "        RECORDSIZE(4089 32760)       -\n"
        "        REUSE)              -\n"
        "        DATA                           -\n"
        "        (NAME(ANSIBIT.CICS.IYTWYD01.DFHGCD.DATA)  -\n"
        "        CONTROLINTERVALSIZE(32768)    -\n"
        "        KEYS(52 0))  -\n"
        "        INDEX                          -\n"
        "        (NAME(ANSIBIT.CICS.IYTWYD01.DFHGCD.INDEX))\n"
        "0IGD17101I DATA SET ANSIBIT.CICS.IYTWYD01.DFHGCD\n"
        "NOT DEFINED BECAUSE DUPLICATE NAME EXISTS IN CATALOG\n"
        "RETURN CODE IS 8 REASON CODE IS 38 IGG0CLEH\n"
        "IGD17219I UNABLE TO CONTINUE DEFINE OF DATA SET\n"
        "ANSIBIT.CICS.IYTWYD01.DFHGCD\n"
        "0IDC3013I DUPLICATE DATA SET NAME\n"
        "IDC3009I ** VSAM CATALOG RETURN CODE IS 8 - REASON CODE IS IGG0CLEH-38\n"
        "0IDC3003I FUNCTION TERMINATED. CONDITION CODE IS 12\n"
        "0        \n"
        "\n"
        "0IDC0002I IDCAMS PROCESSING COMPLETE. MAXIMUM CONDITION CODE WAS 12")
    stderr = ""
    dataset_utils.idcams = MagicMock(return_value=[rc, stdout, stderr])

    cmd = '''
    DEFINE CLUSTER -
        (NAME(ANSIBIT.CICS.IYTWYD01.DFHGCD) -
        INDEXED                      -
        MEGABYTES(5 1)             -
        SHR(2)              -
        FREESPACE(10 10)              -
        RECORDSIZE(4089 32760)       -
        REUSE)              -
        DATA                           -
        (NAME(ANSIBIT.CICS.IYTWYD01.DFHGCD.DATA)  -
        CONTROLINTERVALSIZE(32768)    -
        KEYS(52 0))  -
        INDEX                          -
        (NAME(ANSIBIT.CICS.IYTWYD01.DFHGCD.INDEX))
    '''

    result_exececutions = dataset_utils._run_idcams(
        cmd=cmd,
        name="Create Catalog",
        location="ANSIBIT.CICS.IYTWYD01.DFHGCD",
        delete=False)

    assert len(result_exececutions) == 1
    assert result_exececutions[0] == {
        "name": "IDCAMS - Create Catalog - Run 1",
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr,
    }


def test__run_idcams_delete():

    rc = 0
    stdout = (
        "1IDCAMS  SYSTEM SERVICES                                           TIME: 10:15:27"
        "        06/29/23     PAGE      1\n"
        "0        \n"
        "        DELETE ANSIBIT.CICS.IYTWYD03.DFHGCD\n"
        "0IDC0550I ENTRY (D) ANSIBIT.CICS.IYTWYD03.DFHGCD.DATA DELETED\n"
        "0IDC0550I ENTRY (I) ANSIBIT.CICS.IYTWYD03.DFHGCD.INDEX DELETED\n"
        "0IDC0550I ENTRY (C) ANSIBIT.CICS.IYTWYD03.DFHGCD DELETED\n"
        "0IDC0001I FUNCTION COMPLETED, HIGHEST CONDITION CODE WAS 0\n"
        "0        \n"
        "\n"
        "0IDC0002I IDCAMS PROCESSING COMPLETE. MAXIMUM CONDITION CODE WAS 0")
    stderr = ""
    dataset_utils.idcams = MagicMock(return_value=[rc, stdout, stderr])

    cmd = '''
        DELETE ANSIBIT.CICS.IYTWYD03.DFHGCD
    '''

    result_exececutions = dataset_utils._run_idcams(
        cmd=cmd,
        name="Remove Catalog",
        location="ANSIBIT.CICS.IYTWYD03.DFHGCD",
        delete=True)

    assert len(result_exececutions) == 1
    assert result_exececutions[0] == {
        "name": "IDCAMS - Remove Catalog - Run 1",
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr,
    }


def test__run_idcams_delete_no_exist():

    rc = 8
    stdout = (
        "1IDCAMS  SYSTEM SERVICES                                           TIME: 10:15:24"
        "        06/29/23     PAGE      1\n"
        "0        \n"
        "        DELETE ANSIBIT.CICS.IYTWYD02.DFHGCD\n"
        "0IDC3012I ENTRY ANSIBIT.CICS.IYTWYD02.DFHGCD NOT FOUND\n"
        "IDC3009I ** VSAM CATALOG RETURN CODE IS 8 - REASON CODE IS IGG0CLEG-42\n"
        "IDC0551I ** ENTRY ANSIBIT.CICS.IYTWYD02.DFHGCD NOT DELETED\n"
        "0IDC0001I FUNCTION COMPLETED, HIGHEST CONDITION CODE WAS 8\n"
        "0        \n"
        "    \n"
        "0IDC0002I IDCAMS PROCESSING COMPLETE. MAXIMUM CONDITION CODE WAS 8")
    stderr = ""
    dataset_utils.idcams = MagicMock(return_value=[rc, stdout, stderr])

    cmd = '''
        DELETE ANSIBIT.CICS.IYTWYD02.DFHGCD
    '''

    result_exececutions = dataset_utils._run_idcams(
        cmd=cmd,
        name="Remove Catalog",
        location="ANSIBIT.CICS.IYTWYD02.DFHGCD",
        delete=True)

    assert len(result_exececutions) == 1
    assert result_exececutions[0] == {
        "name": "IDCAMS - Remove Catalog - Run 1",
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr,
    }


def test__run_idcams_bad_return_code_when_creating():

    rc = 99
    stdout = "ANSIBIT.CICS.IYTWYD02.DFHGCD"
    stderr = ""
    dataset_utils.idcams = MagicMock(return_value=[rc, stdout, stderr])

    cmd = '''
    DEFINE CLUSTER -
        (NAME(ANSIBIT.CICS.IYTWYD01.DFHGCD) -
        INDEXED                      -
        MEGABYTES(5 1)             -
        SHR(2)              -
        FREESPACE(10 10)              -
        RECORDSIZE(4089 32760)       -
        REUSE)              -
        DATA                           -
        (NAME(ANSIBIT.CICS.IYTWYD01.DFHGCD.DATA)  -
        CONTROLINTERVALSIZE(32768)    -
        KEYS(52 0))  -
        INDEX                          -
        (NAME(ANSIBIT.CICS.IYTWYD01.DFHGCD.INDEX))
    '''

    expected_executions = [
        _execution(name="IDCAMS - Create Catalog - Run 1", rc=rc, stdout=stdout, stderr=stderr)
    ]

    try:
        dataset_utils._run_idcams(
            cmd=cmd,
            name="Create Catalog",
            location="ANSIBIT.CICS.IYTWYD02.DFHGCD",
            delete=False)
    except Exception as e:
        assert e.args[0] == "RC 99 when creating data set"
        assert e.args[1] == expected_executions


def test__run_idcams_bad_return_code_when_deleting():

    rc = 99
    stdout = "ANSIBIT.CICS.IYTWYD02.DFHGCD"
    stderr = ""
    dataset_utils.idcams = MagicMock(return_value=[rc, stdout, stderr])

    cmd = '''
        DELETE ANSIBIT.CICS.IYTWYD02.DFHGCD
    '''

    expected_executions = [
        _execution(name="IDCAMS - Remove Catalog - Run 1", rc=rc, stdout=stdout, stderr=stderr)
    ]

    try:
        dataset_utils._run_idcams(
            cmd=cmd,
            name="Remove Catalog",
            location="ANSIBIT.CICS.IYTWYD02.DFHGCD",
            delete=True)
    except Exception as e:
        assert e.args[0] == "RC 99 when deleting data set"
        assert e.args[1] == expected_executions


def test__run_listds_exists_vsam():

    rc = 0
    stdout = (
        "1READY                                                                    "
        "                                               \n  LISTDS 'ANSIBIT.CICS.TE"
        "STS.A365D7A.DFHGCD'                                                       "
        "                      \n ANSIBIT.CICS.TESTS.A365D7A.DFHGCD                "
        "                                                                       \n "
        "--LRECL--DSORG-                                                           "
        "                                              \n   **     VSAM            "
        "                                                                          "
        "                     \n --VOLUMES-BLKSIZE                                 "
        "                                                                      \n  "
        "           **                                                             "
        "                                             \n READY                     "
        "                                                                          "
        "                    \n END                                                "
        "                                                                     \n")
    stderr = ""
    dataset_utils.ikjeft01 = MagicMock(return_value=[rc, stdout, stderr])

    result_exececutions, result_status = dataset_utils._run_listds(
        "ANSIBIT.CICS.TESTS.A365D7A.DFHGCD")

    assert len(result_exececutions) == 1
    assert result_exececutions[0] == {
        "name": "IKJEFT01 - Get Data Set Status - Run 1",
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr,
    }
    assert result_status == {
        "exists": True,
        "vsam": True,
    }


def test__run_listds_exists_not_vsam():

    rc = 0
    stdout = (
        "1READY                                                                    "
        "                                               \n  LISTDS 'ANSIBIT.CICS.TE"
        "STS.A365D7A.DFHGCD'                                                       "
        "                      \n ANSIBIT.CICS.TESTS.A365D7A.DFHGCD                "
        "                                                                       \n "
        "--LRECL--DSORG-                                                           "
        "                                              \n   **      PO             "
        "                                                                          "
        "                     \n --VOLUMES-BLKSIZE                                 "
        "                                                                      \n  "
        "           **                                                             "
        "                                             \n READY                     "
        "                                                                          "
        "                    \n END                                                "
        "                                                                     \n")
    stderr = ""
    dataset_utils.ikjeft01 = MagicMock(return_value=[rc, stdout, stderr])

    result_exececutions, result_status = dataset_utils._run_listds(
        "ANSIBIT.CICS.TESTS.A365D7A.DFHGCD")

    assert len(result_exececutions) == 1
    assert result_exececutions[0] == {
        "name": "IKJEFT01 - Get Data Set Status - Run 1",
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr,
    }
    assert result_status == {
        "exists": True,
        "vsam": False,
    }


def test__run_listds_bad_rc():

    name = "IKJEFT01 - Get Data Set Status - Run 1"
    rc = 16
    stdout = "ANSIBIT.CICS.TESTS.A365D7A.DFHGCD"
    stderr = ""
    dataset_utils.ikjeft01 = MagicMock(return_value=[rc, stdout, stderr])

    expected_executions = [_execution(name=name, rc=rc, stdout=stdout, stderr=stderr)]

    try:
        dataset_utils._run_listds("ANSIBIT.CICS.TESTS.A365D7A.DFHGCD")
    except Exception as e:
        assert e.args[0] == "RC 16 running LISTDS Command"
        assert e.args[1] == expected_executions


def test__run_listds_not_exists():

    rc = 8
    stdout = (
        "1READY                                                            "
        "                                                       \n"
        "LISTDS 'ANSIBIT.CICS.TESTS.A294D11B.DFHGaCD'                     "
        "                                                      \n"
        "ANSIBIT.CICS.TESTS.A294D11B.DFHGACD                              "
        "                                                       \n"
        "DATA SET 'ANSIBIT.CICS.TESTS.A294D11B.DFHGACD' NOT IN CATALOG    "
        "                                                       \n"
        "READY                                                            "
        "                                                       \n"
        "END")
    stderr = ""
    dataset_utils.ikjeft01 = MagicMock(return_value=[rc, stdout, stderr])

    result_exececutions, result_status = dataset_utils._run_listds(
        "ANSIBIT.CICS.TESTS.A294D11B.DFHGaCD")

    assert len(result_exececutions) == 1
    assert result_exececutions[0] == {
        "name": "IKJEFT01 - Get Data Set Status - Run 1",
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr,
    }
    assert result_status == {
        "exists": False,
        "vsam": False,
    }


def test__run_listds_with_no_zoau_response():
    rc = 0
    stdout = ""
    stderr = ""
    dataset_utils.ikjeft01 = MagicMock(return_value=[rc, stdout, stderr])

    expected_executions = [
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=rc, stdout=stdout, stderr=stderr),
        _execution(name="IKJEFT01 - Get Data Set Status - Run 2", rc=rc, stdout=stdout, stderr=stderr),
        _execution(name="IKJEFT01 - Get Data Set Status - Run 3", rc=rc, stdout=stdout, stderr=stderr),
        _execution(name="IKJEFT01 - Get Data Set Status - Run 4", rc=rc, stdout=stdout, stderr=stderr),
        _execution(name="IKJEFT01 - Get Data Set Status - Run 5", rc=rc, stdout=stdout, stderr=stderr),
        _execution(name="IKJEFT01 - Get Data Set Status - Run 6", rc=rc, stdout=stdout, stderr=stderr),
        _execution(name="IKJEFT01 - Get Data Set Status - Run 7", rc=rc, stdout=stdout, stderr=stderr),
        _execution(name="IKJEFT01 - Get Data Set Status - Run 8", rc=rc, stdout=stdout, stderr=stderr),
        _execution(name="IKJEFT01 - Get Data Set Status - Run 9", rc=rc, stdout=stdout, stderr=stderr),
        _execution(name="IKJEFT01 - Get Data Set Status - Run 10", rc=rc, stdout=stdout, stderr=stderr)
    ]

    try:
        dataset_utils._run_listds("LOCATION THATS NOT IN STDOUT")
    except Exception as e:
        assert e.args[0] == "LISTDS Command output not recognised"
        assert e.args[1] == expected_executions
