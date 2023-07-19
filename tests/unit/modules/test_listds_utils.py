# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import dataset_utils
import pytest
try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock


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
        "name": "IKJEFT01 - Get Dataset Status - Run 1",
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
        "name": "IKJEFT01 - Get Dataset Status - Run 1",
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr,
    }
    assert result_status == {
        "exists": True,
        "vsam": False,
    }


def test__run_listds_bad_rc():

    rc = 16
    stdout = ""
    stderr = ""
    dataset_utils.ikjeft01 = MagicMock(return_value=[rc, stdout, stderr])

    with pytest.raises(Exception) as e_info:
        result_exececutions, result_status = dataset_utils._run_listds(
            "ANSIBIT.CICS.TESTS.A365D7A.DFHGCD")

        assert e_info == "LISTDS Command output not recognised"


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
        "name": "IKJEFT01 - Get Dataset Status - Run 1",
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr,
    }
    assert result_status == {
        "exists": False,
        "vsam": False,
    }
