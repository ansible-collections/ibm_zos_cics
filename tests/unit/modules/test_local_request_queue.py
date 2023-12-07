# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2020,2021
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import absolute_import, division, print_function
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import dataset_utils
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.response import _execution, _response, _state
from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.data_set_helper import set_data_set, set_module_args
from ansible_collections.ibm.ibm_zos_cics.plugins.modules import local_request_queue

try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock


__metaclass__ = type

default_arg_parms = {
    "space_primary": 5,
    "space_type": "M",
    "region_data_sets": {
        "dfhlrq": {
            "dsn": "TEST.REGIONS.LRQ"
        }
    },
    "cics_data_sets": {
        "sdfhload": "TEST.CICS.INSTALL.SDFHLOAD"
    },
    "state": "initial",
}


def initialise_module(**kwargs):
    initial_args = default_arg_parms
    initial_args.update(kwargs)
    set_module_args(initial_args)
    lrq_module = local_request_queue.AnsibleLocalRequestQueueModule()
    return lrq_module


def test_create_an_intial_local_request_queue():
    lrq_module = initialise_module()

    dataset_utils.idcams = MagicMock(return_value=(0, "TEST.REGIONS.LRQ", "stderr"))
    dataset_utils.ikjeft01 = MagicMock(side_effect=[(8, "TEST.REGIONS.LRQ NOT IN CATALOG", "stderr"), (0, "TEST.REGIONS.LRQ VSAM", "stderr")])
    local_request_queue.AnsibleLocalRequestQueueModule._exit = MagicMock(return_value=None)

    lrq_module.main()
    expected_result = _response(executions=[
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=8, stdout="TEST.REGIONS.LRQ NOT IN CATALOG", stderr="stderr"),
        _execution(name="IDCAMS - Create local request queue data set - Run 1", rc=0, stdout="TEST.REGIONS.LRQ", stderr="stderr"),
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=0, stdout="TEST.REGIONS.LRQ VSAM", stderr="stderr")
    ],
        start_state=_state(exists=False, vsam=False),
        end_state=_state(exists=True, vsam=True)
    )
    expected_result.update({"changed": True})
    assert lrq_module.result == expected_result


def test_delete_an_existing_local_request_queue():
    lrq_module = initialise_module(state="absent")

    dataset_utils.idcams = MagicMock(return_value=(0, "ENTRY (C) TEST.REGIONS.LRQ DELETED\n", "stderr"))
    dataset_utils.ikjeft01 = MagicMock(side_effect=[(0, "TEST.REGIONS.LRQ VSAM", "stderr"), (8, "TEST.REGIONS.LRQ NOT IN CATALOG", "stderr")])
    local_request_queue.AnsibleLocalRequestQueueModule._exit = MagicMock(return_value=None)

    lrq_module.main()
    expected_result = _response(executions=[
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=0, stdout="TEST.REGIONS.LRQ VSAM", stderr="stderr"),
        _execution(name="IDCAMS - Removing local request queue data set - Run 1", rc=0, stdout="ENTRY (C) TEST.REGIONS.LRQ DELETED\n", stderr="stderr"),
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=8, stdout="TEST.REGIONS.LRQ NOT IN CATALOG", stderr="stderr")
    ],
        start_state=_state(exists=True, vsam=True),
        end_state=_state(exists=False, vsam=False)
    )
    expected_result.update({"changed": True})
    assert lrq_module.result == expected_result


def test_do_nothing_to_an_existing_lrq():
    lrq_module = initialise_module()
    data_set = set_data_set(exists=True, name="TEST.REGIONS.LRQ", vsam=True)
    lrq_module.data_set = data_set

    dataset_utils.ikjeft01 = MagicMock(side_effect=[(0, "TEST.REGIONS.LRQ VSAM", "stderr"), (0, "TEST.REGIONS.LRQ VSAM", "stderr")])
    local_request_queue.AnsibleLocalRequestQueueModule._exit = MagicMock(return_value=None)

    lrq_module.main()
    expected_result = _response(executions=[
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=0, stdout="TEST.REGIONS.LRQ VSAM", stderr="stderr"),
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=0, stdout="TEST.REGIONS.LRQ VSAM", stderr="stderr")
    ],
        start_state=_state(exists=True, vsam=True),
        end_state=_state(exists=True, vsam=True)
    )
    assert lrq_module.result == expected_result
