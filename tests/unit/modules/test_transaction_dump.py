# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import absolute_import, division, print_function
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import dataset_utils
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.response import _execution, _response, _state
from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.data_set_helper import set_module_args
from ansible_collections.ibm.ibm_zos_cics.plugins.modules import transaction_dump
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import icetool
import pytest
import sys

from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.zos_mvs_raw import MVSCmdResponse

try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock


__metaclass__ = type

default_arg_parms = {
    "space_primary": 20,
    "space_type": "M",
    "region_data_sets": {
        "dfhdmpa": {
            "dsn": "TEST.REGIONS.DFHDMPA"
        },
        "dfhdmpb": {
            "dsn": "TEST.REGIONS.DFHDMPB"
        }
    },
    "cics_data_sets": {
        "sdfhload": "TEST.CICS.INSTALL.SDFHLOAD"
    },
    "state": "initial",
    "destination": "A"
}


def initialise_module(**kwargs):
    initial_args = default_arg_parms
    initial_args.update(kwargs)
    set_module_args(initial_args)
    transaction_dump_module = transaction_dump.AnsibleTransactionDumpModule()
    transaction_dump_module._module.fail_json = MagicMock(return_value=None)
    transaction_dump_module._module.exit_json = MagicMock(return_value=None)
    return transaction_dump_module


@pytest.mark.skipif(sys.version_info.major < 3,
                    reason="Requires python 3 language features")
def test_create_an_intial_transaction_dump():
    transaction_dump_module = initialise_module()

    dataset_utils.ikjeft01 = MagicMock(
        side_effect=[
            (8,
             "TEST.REGIONS.DFHDMPA NOT IN CATALOG",
             "stderr"),
            (0,
             "TEST.REGIONS.DFHDMPA PS",
             "stderr")])
    dataset_utils.MVSCmd.execute = MagicMock(
        return_value=MVSCmdResponse(
            rc=0, stdout="TEST.REGIONS.DFHDMPA", stderr=""))

    transaction_dump_module.main()
    expected_result = _response(
        executions=[
            _execution(
                name="IKJEFT01 - Get Data Set Status - Run 1",
                rc=8,
                stdout="TEST.REGIONS.DFHDMPA NOT IN CATALOG",
                stderr="stderr"),
            _execution(
                name="IEFBR14 - dfhdmpa - Run 1",
                rc=0,
                stdout="TEST.REGIONS.DFHDMPA",
                stderr=""),
            _execution(
                name="IKJEFT01 - Get Data Set Status - Run 1",
                rc=0,
                stdout="TEST.REGIONS.DFHDMPA PS",
                stderr="stderr")],
        start_state=_state(
            exists=False),
        end_state=_state(
            exists=True))
    expected_result.update({"changed": True})
    assert transaction_dump_module.result == expected_result


@pytest.mark.skipif(sys.version_info.major < 3,
                    reason="Requires python 3 language features")
def test_delete_an_existing_transaction_dump():
    transaction_dump_module = initialise_module(state="absent")

    dataset_utils.idcams = MagicMock(
        return_value=(
            0,
            "ENTRY (A) TEST.REGIONS.DFHDMPA DELETED\n",
            "stderr"))
    dataset_utils.ikjeft01 = MagicMock(
        side_effect=[
            (0,
             "TEST.REGIONS.DFHDMPA PS",
             "stderr"),
            (8,
             "TEST.REGIONS.DFHDMPA NOT IN CATALOG",
             "stderr")])

    transaction_dump_module.main()
    expected_result = _response(
        executions=[
            _execution(
                name="IKJEFT01 - Get Data Set Status - Run 1",
                rc=0,
                stdout="TEST.REGIONS.DFHDMPA PS",
                stderr="stderr"),
            _execution(
                name="IDCAMS - Deleting transaction dump data set - Run 1",
                rc=0,
                stdout="ENTRY (A) TEST.REGIONS.DFHDMPA DELETED\n",
                stderr="stderr"),
            _execution(
                name="IKJEFT01 - Get Data Set Status - Run 1",
                rc=8,
                stdout="TEST.REGIONS.DFHDMPA NOT IN CATALOG",
                stderr="stderr")],
        start_state=_state(
            exists=True),
        end_state=_state(
            exists=False))
    expected_result.update({"changed": True})
    assert transaction_dump_module.result == expected_result


@pytest.mark.skipif(sys.version_info.major < 3,
                    reason="Requires python 3 language features")
def test_remove_non_existent_transaction_dump():
    transaction_dump_module = initialise_module(state="absent")

    dataset_utils.ikjeft01 = MagicMock(return_value=(
        8, "TEST.REGIONS.DFHDMPA NOT IN CATALOG", "stderr"))

    transaction_dump_module.main()
    expected_result = _response(
        executions=[
            _execution(
                name="IKJEFT01 - Get Data Set Status - Run 1",
                rc=8,
                stdout="TEST.REGIONS.DFHDMPA NOT IN CATALOG",
                stderr="stderr"),
            _execution(
                name="IKJEFT01 - Get Data Set Status - Run 1",
                rc=8,
                stdout="TEST.REGIONS.DFHDMPA NOT IN CATALOG",
                stderr="stderr")],
        start_state=_state(
            exists=False),
        end_state=_state(
            exists=False))
    expected_result.update({"changed": False})
    assert transaction_dump_module.result == expected_result


@pytest.mark.skipif(sys.version_info.major < 3,
                    reason="Requires python 3 language features")
def test_create_an_intial_destination_b_transaction_dump():
    transaction_dump_module = initialise_module(destination="B")

    dataset_utils.ikjeft01 = MagicMock(
        side_effect=[
            (8,
             "TEST.REGIONS.DFHDMPB NOT IN CATALOG",
             "stderr"),
            (0,
             "TEST.REGIONS.DFHDMPB PS",
             "stderr")])
    dataset_utils.MVSCmd.execute = MagicMock(
        return_value=MVSCmdResponse(
            rc=0, stdout="TEST.REGIONS.DFHDMPB", stderr=""))

    transaction_dump_module.main()
    expected_result = _response(
        executions=[
            _execution(
                name="IKJEFT01 - Get Data Set Status - Run 1",
                rc=8,
                stdout="TEST.REGIONS.DFHDMPB NOT IN CATALOG",
                stderr="stderr"),
            _execution(
                name="IEFBR14 - dfhdmpb - Run 1",
                rc=0,
                stdout="TEST.REGIONS.DFHDMPB",
                stderr=""),
            _execution(
                name="IKJEFT01 - Get Data Set Status - Run 1",
                rc=0,
                stdout="TEST.REGIONS.DFHDMPB PS",
                stderr="stderr")],
        start_state=_state(
            exists=False),
        end_state=_state(
            exists=True))
    expected_result.update({"changed": True})
    assert transaction_dump_module.result == expected_result


@pytest.mark.skipif(sys.version_info.major < 3,
                    reason="Requires python 3 language features")
def test_warm_on_non_existent():
    transaction_dump_module = initialise_module(state="warm")

    dataset_utils.ikjeft01 = MagicMock(return_value=(
        8, "TEST.REGIONS.DFHDMPA NOT IN CATALOG", "stderr"))

    transaction_dump_module.main()
    expected_result = _response(
        executions=[
            _execution(
                name="IKJEFT01 - Get Data Set Status - Run 1",
                rc=8,
                stdout="TEST.REGIONS.DFHDMPA NOT IN CATALOG",
                stderr="stderr"),
            _execution(
                name="IKJEFT01 - Get Data Set Status - Run 1",
                rc=8,
                stdout="TEST.REGIONS.DFHDMPA NOT IN CATALOG",
                stderr="stderr"),
        ],
        start_state=_state(
            exists=False),
        end_state=_state(
            exists=False))
    expected_result.update({"changed": False})
    expected_result.update({"failed": True})
    assert transaction_dump_module.result == expected_result


@pytest.mark.skipif(sys.version_info.major < 3,
                    reason="Requires python 3 language features")
def test_warm_on_empty():
    transaction_dump_module = initialise_module(state="warm")

    dataset_utils.ikjeft01 = MagicMock(
        return_value=(0, "TEST.REGIONS.DFHDMPA PS", "stderr"))
    icetool._execute_icetool = MagicMock(return_value=MVSCmdResponse(
        rc=0, stdout="RECORD COUNT:  000000000000000", stderr="stderr"))

    transaction_dump_module.main()
    expected_result = _response(
        executions=[
            _execution(
                name="IKJEFT01 - Get Data Set Status - Run 1",
                rc=0,
                stdout="TEST.REGIONS.DFHDMPA PS",
                stderr="stderr"),
            _execution(
                name="ICETOOL - Get record count",
                rc=0,
                stdout="RECORD COUNT:  000000000000000",
                stderr="stderr"),
            _execution(
                name="IKJEFT01 - Get Data Set Status - Run 1",
                rc=0,
                stdout="TEST.REGIONS.DFHDMPA PS",
                stderr="stderr"),
        ],
        start_state=_state(
            exists=True),
        end_state=_state(
            exists=True))
    expected_result.update({"changed": False})
    expected_result.update({"failed": True})
    assert transaction_dump_module.result == expected_result


@pytest.mark.skipif(sys.version_info.major < 3,
                    reason="Requires python 3 language features")
def test_warm_success():
    transaction_dump_module = initialise_module(state="warm")

    dataset_utils.ikjeft01 = MagicMock(
        return_value=(0, "TEST.REGIONS.DFHDMPA PS", "stderr"))
    icetool._execute_icetool = MagicMock(return_value=MVSCmdResponse(
        rc=0, stdout="RECORD COUNT:  000000000000052", stderr="stderr"))

    transaction_dump_module.main()
    expected_result = _response(
        executions=[
            _execution(
                name="IKJEFT01 - Get Data Set Status - Run 1",
                rc=0,
                stdout="TEST.REGIONS.DFHDMPA PS",
                stderr="stderr"),
            _execution(
                name="ICETOOL - Get record count",
                rc=0,
                stdout="RECORD COUNT:  000000000000052",
                stderr="stderr"),
            _execution(
                name="IKJEFT01 - Get Data Set Status - Run 1",
                rc=0,
                stdout="TEST.REGIONS.DFHDMPA PS",
                stderr="stderr"),
        ],
        start_state=_state(
            exists=True),
        end_state=_state(
            exists=True))
    expected_result.update({"changed": False})
    expected_result.update({"failed": False})
    assert transaction_dump_module.result == expected_result
