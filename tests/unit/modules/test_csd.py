# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import absolute_import, division, print_function
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import dataset_utils
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import csd as csd_utils
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import icetool
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.response import _execution, _response, _state
from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.data_set_helper import set_data_set, set_module_args
from ansible_collections.ibm.ibm_zos_cics.plugins.modules import csd
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.zos_mvs_raw import MVSCmdResponse
import pytest
import sys


try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock


__metaclass__ = type

default_arg_parms = {
    "space_primary": 5,
    "space_type": "M",
    "region_data_sets": {
        "dfhcsd": {
            "dsn": "TEST.REGIONS.CSD"
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
    csd_module = csd.AnsibleCSDModule()
    # Mock Ansible module fail and exits, this prevents sys.exit being called but retains an accurate results
    csd_module._module.fail_json = MagicMock(return_value=None)
    csd_module._module.exit_json = MagicMock(return_value=None)
    return csd_module


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_create_an_intial_csd():
    csd_module = initialise_module()

    dataset_utils.idcams = MagicMock(return_value=(0, "TEST.REGIONS.CSD", "stderr"))
    dataset_utils.ikjeft01 = MagicMock(side_effect=[(8, "TEST.REGIONS.CSD NOT IN CATALOG", "stderr"), (0, "TEST.REGIONS.CSD VSAM", "stderr")])
    csd_utils._execute_dfhccutl = MagicMock(return_value=MVSCmdResponse(rc=0, stdout="stdout", stderr="stderr"))

    csd_module.main()
    expected_result = _response(executions=[
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=8, stdout="TEST.REGIONS.CSD NOT IN CATALOG", stderr="stderr"),
        _execution(name="IDCAMS - Create CSD data set - Run 1", rc=0, stdout="TEST.REGIONS.CSD", stderr="stderr"),
        _execution(name="DFHCCUTL - Initialise CSD", rc=0, stdout="stdout", stderr="stderr"),
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=0, stdout="TEST.REGIONS.CSD VSAM", stderr="stderr")
    ],
        start_state=_state(exists=False, vsam=False),
        end_state=_state(exists=True, vsam=True)
    )
    expected_result.update({"changed": True})
    assert csd_module.result == expected_result


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_delete_an_existing_csd():
    csd_module = initialise_module(state="absent")

    dataset_utils.idcams = MagicMock(return_value=(0, "ENTRY (C) TEST.REGIONS.CSD DELETED\n", "stderr"))
    dataset_utils.ikjeft01 = MagicMock(side_effect=[(0, "TEST.REGIONS.CSD VSAM", "stderr"), (8, "TEST.REGIONS.CSD NOT IN CATALOG", "stderr")])

    csd_module.main()
    expected_result = _response(executions=[
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=0, stdout="TEST.REGIONS.CSD VSAM", stderr="stderr"),
        _execution(name="IDCAMS - Removing CSD data set - Run 1", rc=0, stdout="ENTRY (C) TEST.REGIONS.CSD DELETED\n", stderr="stderr"),
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=8, stdout="TEST.REGIONS.CSD NOT IN CATALOG", stderr="stderr")
    ],
        start_state=_state(exists=True, vsam=True),
        end_state=_state(exists=False, vsam=False)
    )
    expected_result.update({"changed": True})
    assert csd_module.result == expected_result


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_do_nothing_to_an_existing_csd():
    csd_module = initialise_module()
    data_set = set_data_set(exists=True, name="TEST.REGIONS.CSD", vsam=True)
    csd_module.data_set = data_set

    dataset_utils.ikjeft01 = MagicMock(side_effect=[(0, "TEST.REGIONS.CSD VSAM", "stderr"), (0, "TEST.REGIONS.CSD VSAM", "stderr")])
    csd_utils._execute_dfhccutl = MagicMock(return_value=MVSCmdResponse(rc=0, stdout="stdout", stderr="stderr"))

    csd_module.main()
    expected_result = _response(executions=[
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=0, stdout="TEST.REGIONS.CSD VSAM", stderr="stderr"),
        _execution(name="DFHCCUTL - Initialise CSD", rc=0, stdout="stdout", stderr="stderr"),
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=0, stdout="TEST.REGIONS.CSD VSAM", stderr="stderr")
    ],
        start_state=_state(exists=True, vsam=True),
        end_state=_state(exists=True, vsam=True)
    )
    assert csd_module.result == expected_result


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_remove_non_existent_csd():
    csd_module = initialise_module(state="absent")

    dataset_utils.idcams = MagicMock(return_value=(8, "ENTRY TEST.REGIONS.CSD NOTFOUND", "stderr"))
    dataset_utils.ikjeft01 = MagicMock(return_value=(8, "TEST.REGIONS.CSD NOT IN CATALOG", "stderr"))

    csd_module.main()
    expected_result = _response(executions=[
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=8, stdout="TEST.REGIONS.CSD NOT IN CATALOG", stderr="stderr"),
        _execution(name="IDCAMS - Removing CSD data set - Run 1", rc=8, stdout="ENTRY TEST.REGIONS.CSD NOTFOUND", stderr="stderr"),
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=8, stdout="TEST.REGIONS.CSD NOT IN CATALOG", stderr="stderr")
    ],
        start_state=_state(exists=False, vsam=False),
        end_state=_state(exists=False, vsam=False)
    )
    expected_result.update({"changed": True})
    assert csd_module.result == expected_result


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_warm_start_a_csd():
    csd_module = initialise_module(state="warm")

    dataset_utils.ikjeft01 = MagicMock(return_value=(0, "TEST.REGIONS.CSD VSAM", "stderr"))
    icetool._execute_icetool = MagicMock(return_value=MVSCmdResponse(rc=0, stdout="RECORD COUNT:  000000000000052", stderr="stderr"))

    csd_module.main()
    expected_result = _response(executions=[
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=0, stdout="TEST.REGIONS.CSD VSAM", stderr="stderr"),
        _execution(name="ICETOOL - Get record count", rc=0, stdout="RECORD COUNT:  000000000000052", stderr="stderr"),
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=0, stdout="TEST.REGIONS.CSD VSAM", stderr="stderr"),
    ],
        start_state=_state(exists=True, vsam=True),
        end_state=_state(exists=True, vsam=True)
    )
    assert csd_module.result == expected_result


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_error_warm_start_a_unused_csd():
    csd_module = initialise_module(state="warm")

    dataset_utils.ikjeft01 = MagicMock(return_value=(0, "TEST.REGIONS.CSD VSAM", "stderr"))
    icetool._execute_icetool = MagicMock(return_value=MVSCmdResponse(rc=0, stdout="RECORD COUNT:  000000000000000", stderr="stderr"))

    csd_module.main()

    expected_result = _response(executions=[
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=0, stdout="TEST.REGIONS.CSD VSAM", stderr="stderr"),
        _execution(name="ICETOOL - Get record count", rc=0, stdout="RECORD COUNT:  000000000000000", stderr="stderr"),
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=0, stdout="TEST.REGIONS.CSD VSAM", stderr="stderr"),
    ],
        start_state=_state(exists=True, vsam=True),
        end_state=_state(exists=True, vsam=True)
    )
    expected_result.update({"failed": True})
    assert csd_module.result == expected_result


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_error_warm_start_a_non_existent_csd():
    csd_module = initialise_module(state="warm")

    dataset_utils.ikjeft01 = MagicMock(return_value=(8, "TEST.REGIONS.CSD NOT IN CATALOG", "stderr"))
    icetool._execute_icetool = MagicMock(return_value=MVSCmdResponse(rc=0, stdout="RECORD COUNT:  000000000000052", stderr="stderr"))

    csd_module.main()
    expected_result = _response(executions=[
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=8, stdout="TEST.REGIONS.CSD NOT IN CATALOG", stderr="stderr"),
        _execution(name="ICETOOL - Get record count", rc=0, stdout="RECORD COUNT:  000000000000052", stderr="stderr"),
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=8, stdout="TEST.REGIONS.CSD NOT IN CATALOG", stderr="stderr"),
    ],
        start_state=_state(exists=False, vsam=False),
        end_state=_state(exists=False, vsam=False)
    )
    expected_result.update({"failed": True})
    assert csd_module.result == expected_result


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_bad_response_from_ccutl():
    csd_module = initialise_module()

    dataset_utils.idcams = MagicMock(return_value=(0, "TEST.REGIONS.CSD", "stderr"))
    dataset_utils.ikjeft01 = MagicMock(side_effect=[(8, "TEST.REGIONS.CSD NOT IN CATALOG", "stderr"), (0, "TEST.REGIONS.CSD VSAM", "stderr")])
    csd_utils._execute_dfhccutl = MagicMock(return_value=MVSCmdResponse(rc=99, stdout="stdout", stderr="stderr"))

    csd_module.main()
    expected_result = _response(executions=[
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=8, stdout="TEST.REGIONS.CSD NOT IN CATALOG", stderr="stderr"),
        _execution(name="IDCAMS - Create CSD data set - Run 1", rc=0, stdout="TEST.REGIONS.CSD", stderr="stderr"),
        _execution(name="DFHCCUTL - Initialise CSD", rc=99, stdout="stdout", stderr="stderr"),
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=0, stdout="TEST.REGIONS.CSD VSAM", stderr="stderr")
    ],
        start_state=_state(exists=False, vsam=False),
        end_state=_state(exists=True, vsam=True)
    )
    expected_result.update({"changed": True})
    expected_result.update({"failed": True})
    assert csd_module.result == expected_result
