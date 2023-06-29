# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import idcams
try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock


def test_run_idcams_create():

    rc = 0
    stdout = (
        "1IDCAMS  SYSTEM SERVICES                                           TIME: 10:04:57  "
        "      06/29/23     PAGE      1\n"
        "0        \n"
        "    DEFINE CLUSTER -\n"
        "        (NAME(TWYDELL.CICS.IYTWYD03.DFHGCD) -\n"
        "        INDEXED                      -\n"
        "        MEGABYTES(5 1)             -\n"
        "        SHR(2)              -\n"
        "        FREESPACE(10 10)              -\n"
        "        RECORDSIZE(4089 32760)       -\n"
        "        REUSE)              -\n"
        "        DATA                           -\n"
        "        (NAME(TWYDELL.CICS.IYTWYD03.DFHGCD.DATA)  -\n"
        "        CONTROLINTERVALSIZE(32768)    -\n"
        "        KEYS(52 0))  -\n"
        "        INDEX                          -\n"
        "        (NAME(TWYDELL.CICS.IYTWYD03.DFHGCD.INDEX))\n"
        "0IDC0508I DATA ALLOCATION STATUS FOR VOLUME P2P0D5 IS 0\n"
        "0IDC0509I INDEX ALLOCATION STATUS FOR VOLUME P2P0D5 IS 0\n"
        "IDC0181I STORAGECLASS USED IS STANDARD\n"
        "IDC0181I MANAGEMENTCLASS USED IS STANDARD\n"
        "0IDC0001I FUNCTION COMPLETED, HIGHEST CONDITION CODE WAS 0\n"
        "0        \n"
        "        \n"
        "0IDC0002I IDCAMS PROCESSING COMPLETE. MAXIMUM CONDITION CODE WAS 0")
    stderr = ""
    idcams.idcams = MagicMock(return_value=[rc, stdout, stderr])

    cmd = '''
    DEFINE CLUSTER -
        (NAME(TWYDELL.CICS.IYTWYD03.DFHGCD) -
        INDEXED                      -
        MEGABYTES(5 1)             -
        SHR(2)              -
        FREESPACE(10 10)              -
        RECORDSIZE(4089 32760)       -
        REUSE)              -
        DATA                           -
        (NAME(TWYDELL.CICS.IYTWYD03.DFHGCD.DATA)  -
        CONTROLINTERVALSIZE(32768)    -
        KEYS(52 0))  -
        INDEX                          -
        (NAME(TWYDELL.CICS.IYTWYD03.DFHGCD.INDEX))
    '''

    result_exececutions = idcams.run_idcams(
        cmd=cmd,
        name="Create Catalog",
        location="TWYDELL.CICS.IYTWYD03.DFHGCD",
        delete=False)

    assert len(result_exececutions) == 1
    assert result_exececutions[0].to_dict() == {
        "name": "IDCAMS - Create Catalog - Run 1",
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr,
    }


def test_run_idcams_create_exists():

    rc = 12
    stdout = (
        "1IDCAMS  SYSTEM SERVICES                                           TIME: 10:04:51  "
        "      06/29/23     PAGE      1\n"
        "0        \n"
        "    DEFINE CLUSTER -\n"
        "        (NAME(TWYDELL.CICS.IYTWYD01.DFHGCD) -\n"
        "        INDEXED                      -\n"
        "        MEGABYTES(5 1)             -\n"
        "        SHR(2)              -\n"
        "        FREESPACE(10 10)              -\n"
        "        RECORDSIZE(4089 32760)       -\n"
        "        REUSE)              -\n"
        "        DATA                           -\n"
        "        (NAME(TWYDELL.CICS.IYTWYD01.DFHGCD.DATA)  -\n"
        "        CONTROLINTERVALSIZE(32768)    -\n"
        "        KEYS(52 0))  -\n"
        "        INDEX                          -\n"
        "        (NAME(TWYDELL.CICS.IYTWYD01.DFHGCD.INDEX))\n"
        "0IGD17101I DATA SET TWYDELL.CICS.IYTWYD01.DFHGCD\n"
        "NOT DEFINED BECAUSE DUPLICATE NAME EXISTS IN CATALOG\n"
        "RETURN CODE IS 8 REASON CODE IS 38 IGG0CLEH\n"
        "IGD17219I UNABLE TO CONTINUE DEFINE OF DATA SET\n"
        "TWYDELL.CICS.IYTWYD01.DFHGCD\n"
        "0IDC3013I DUPLICATE DATA SET NAME\n"
        "IDC3009I ** VSAM CATALOG RETURN CODE IS 8 - REASON CODE IS IGG0CLEH-38\n"
        "0IDC3003I FUNCTION TERMINATED. CONDITION CODE IS 12\n"
        "0        \n"
        "\n"
        "0IDC0002I IDCAMS PROCESSING COMPLETE. MAXIMUM CONDITION CODE WAS 12")
    stderr = ""
    idcams.idcams = MagicMock(return_value=[rc, stdout, stderr])

    cmd = '''
    DEFINE CLUSTER -
        (NAME(TWYDELL.CICS.IYTWYD01.DFHGCD) -
        INDEXED                      -
        MEGABYTES(5 1)             -
        SHR(2)              -
        FREESPACE(10 10)              -
        RECORDSIZE(4089 32760)       -
        REUSE)              -
        DATA                           -
        (NAME(TWYDELL.CICS.IYTWYD01.DFHGCD.DATA)  -
        CONTROLINTERVALSIZE(32768)    -
        KEYS(52 0))  -
        INDEX                          -
        (NAME(TWYDELL.CICS.IYTWYD01.DFHGCD.INDEX))
    '''

    result_exececutions = idcams.run_idcams(
        cmd=cmd,
        name="Create Catalog",
        location="TWYDELL.CICS.IYTWYD01.DFHGCD",
        delete=False)

    assert len(result_exececutions) == 1
    assert result_exececutions[0].to_dict() == {
        "name": "IDCAMS - Create Catalog - Run 1",
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr,
    }


def test_run_idcams_delete():

    rc = 0
    stdout = (
        "1IDCAMS  SYSTEM SERVICES                                           TIME: 10:15:27"
        "        06/29/23     PAGE      1\n"
        "0        \n"
        "        DELETE TWYDELL.CICS.IYTWYD03.DFHGCD\n"
        "0IDC0550I ENTRY (D) TWYDELL.CICS.IYTWYD03.DFHGCD.DATA DELETED\n"
        "0IDC0550I ENTRY (I) TWYDELL.CICS.IYTWYD03.DFHGCD.INDEX DELETED\n"
        "0IDC0550I ENTRY (C) TWYDELL.CICS.IYTWYD03.DFHGCD DELETED\n"
        "0IDC0001I FUNCTION COMPLETED, HIGHEST CONDITION CODE WAS 0\n"
        "0        \n"
        "\n"
        "0IDC0002I IDCAMS PROCESSING COMPLETE. MAXIMUM CONDITION CODE WAS 0")
    stderr = ""
    idcams.idcams = MagicMock(return_value=[rc, stdout, stderr])

    cmd = '''
        DELETE TWYDELL.CICS.IYTWYD03.DFHGCD
    '''

    result_exececutions = idcams.run_idcams(
        cmd=cmd,
        name="Remove Catalog",
        location="TWYDELL.CICS.IYTWYD03.DFHGCD",
        delete=True)

    assert len(result_exececutions) == 1
    assert result_exececutions[0].to_dict() == {
        "name": "IDCAMS - Remove Catalog - Run 1",
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr,
    }


def test_run_idcams_delete_no_exist():

    rc = 8
    stdout = (
        "1IDCAMS  SYSTEM SERVICES                                           TIME: 10:15:24"
        "        06/29/23     PAGE      1\n"
        "0        \n"
        "        DELETE TWYDELL.CICS.IYTWYD02.DFHGCD\n"
        "0IDC3012I ENTRY TWYDELL.CICS.IYTWYD02.DFHGCD NOT FOUND\n"
        "IDC3009I ** VSAM CATALOG RETURN CODE IS 8 - REASON CODE IS IGG0CLEG-42\n"
        "IDC0551I ** ENTRY TWYDELL.CICS.IYTWYD02.DFHGCD NOT DELETED\n"
        "0IDC0001I FUNCTION COMPLETED, HIGHEST CONDITION CODE WAS 8\n"
        "0        \n"
        "    \n"
        "0IDC0002I IDCAMS PROCESSING COMPLETE. MAXIMUM CONDITION CODE WAS 8")
    stderr = ""
    idcams.idcams = MagicMock(return_value=[rc, stdout, stderr])

    cmd = '''
        DELETE TWYDELL.CICS.IYTWYD02.DFHGCD
    '''

    result_exececutions = idcams.run_idcams(
        cmd=cmd,
        name="Remove Catalog",
        location="TWYDELL.CICS.IYTWYD02.DFHGCD",
        delete=True)

    assert len(result_exececutions) == 1
    assert result_exececutions[0].to_dict() == {
        "name": "IDCAMS - Remove Catalog - Run 1",
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr,
    }
