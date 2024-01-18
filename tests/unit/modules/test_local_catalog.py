# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import absolute_import, division, print_function
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import dataset_utils
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import local_catalog as local_catalog_utils
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import icetool
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.response import _execution, _response, _state
from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.data_set_helper import set_data_set, set_module_args
from ansible_collections.ibm.ibm_zos_cics.plugins.modules import local_catalog
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
        "dfhlcd": {
            "dsn": "TEST.REGIONS.LCD"
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
    lcd_module = local_catalog.AnsibleLocalCatalogModule()
    # Mock Ansible module fail and exits, this prevents sys.exit being called but retains an accurate results
    lcd_module._module.fail_json = MagicMock(return_value=None)
    lcd_module._module.exit_json = MagicMock(return_value=None)
    return lcd_module


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_create_an_intial_local_catalog():
    lcd_module = initialise_module()

    dataset_utils.idcams = MagicMock(return_value=(0, "TEST.REGIONS.LCD", "stderr"))
    dataset_utils.ikjeft01 = MagicMock(side_effect=[(8, "TEST.REGIONS.LCD NOT IN CATALOG", "stderr"), (0, "TEST.REGIONS.LCD VSAM", "stderr")])
    local_catalog_utils._execute_dfhccutl = MagicMock(return_value=MVSCmdResponse(rc=0, stdout="stdout", stderr="stderr"))

    lcd_module.main()
    expected_result = _response(executions=[
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=8, stdout="TEST.REGIONS.LCD NOT IN CATALOG", stderr="stderr"),
        _execution(name="IDCAMS - Create local catalog data set - Run 1", rc=0, stdout="TEST.REGIONS.LCD", stderr="stderr"),
        _execution(name="DFHCCUTL - Initialise Local Catalog", rc=0, stdout="stdout", stderr="stderr"),
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=0, stdout="TEST.REGIONS.LCD VSAM", stderr="stderr")
    ],
        start_state=_state(exists=False, vsam=False),
        end_state=_state(exists=True, vsam=True)
    )
    expected_result.update({"changed": True})
    assert lcd_module.result == expected_result


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_delete_an_existing_local_catalog():
    lcd_module = initialise_module(state="absent")

    dataset_utils.idcams = MagicMock(return_value=(0, "ENTRY (C) TEST.REGIONS.LCD DELETED\n", "stderr"))
    dataset_utils.ikjeft01 = MagicMock(side_effect=[(0, "TEST.REGIONS.LCD VSAM", "stderr"), (8, "TEST.REGIONS.LCD NOT IN CATALOG", "stderr")])

    lcd_module.main()
    expected_result = _response(executions=[
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=0, stdout="TEST.REGIONS.LCD VSAM", stderr="stderr"),
        _execution(name="IDCAMS - Removing local catalog data set - Run 1", rc=0, stdout="ENTRY (C) TEST.REGIONS.LCD DELETED\n", stderr="stderr"),
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=8, stdout="TEST.REGIONS.LCD NOT IN CATALOG", stderr="stderr")
    ],
        start_state=_state(exists=True, vsam=True),
        end_state=_state(exists=False, vsam=False)
    )
    expected_result.update({"changed": True})
    assert lcd_module.result == expected_result


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_do_nothing_to_an_existing_local_catalog():
    lcd_module = initialise_module()
    data_set = set_data_set(exists=True, name="TEST.REGIONS.LCD", vsam=True)
    lcd_module.data_set = data_set

    dataset_utils.ikjeft01 = MagicMock(side_effect=[(0, "TEST.REGIONS.LCD VSAM", "stderr"), (0, "TEST.REGIONS.LCD VSAM", "stderr")])
    local_catalog_utils._execute_dfhccutl = MagicMock(return_value=MVSCmdResponse(rc=0, stdout="stdout", stderr="stderr"))

    lcd_module.main()
    expected_result = _response(executions=[
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=0, stdout="TEST.REGIONS.LCD VSAM", stderr="stderr"),
        _execution(name="DFHCCUTL - Initialise Local Catalog", rc=0, stdout="stdout", stderr="stderr"),
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=0, stdout="TEST.REGIONS.LCD VSAM", stderr="stderr")
    ],
        start_state=_state(exists=True, vsam=True),
        end_state=_state(exists=True, vsam=True)
    )
    assert lcd_module.result == expected_result


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_remove_non_existent_local_catalog():
    lcd_module = initialise_module(state="absent")

    dataset_utils.idcams = MagicMock(return_value=(8, "ENTRY TEST.REGIONS.LCD NOTFOUND", "stderr"))
    dataset_utils.ikjeft01 = MagicMock(return_value=(8, "TEST.REGIONS.LCD NOT IN CATALOG", "stderr"))

    lcd_module.main()
    expected_result = _response(executions=[
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=8, stdout="TEST.REGIONS.LCD NOT IN CATALOG", stderr="stderr"),
        _execution(name="IDCAMS - Removing local catalog data set - Run 1", rc=8, stdout="ENTRY TEST.REGIONS.LCD NOTFOUND", stderr="stderr"),
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=8, stdout="TEST.REGIONS.LCD NOT IN CATALOG", stderr="stderr")
    ],
        start_state=_state(exists=False, vsam=False),
        end_state=_state(exists=False, vsam=False)
    )
    expected_result.update({"changed": True})
    assert lcd_module.result == expected_result


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_warm_start_a_local_catalog():
    lcd_module = initialise_module(state="warm")

    dataset_utils.ikjeft01 = MagicMock(return_value=(0, "TEST.REGIONS.LCD VSAM", "stderr"))
    icetool._execute_icetool = MagicMock(return_value=MVSCmdResponse(rc=0, stdout="RECORD COUNT:  000000000000052", stderr="stderr"))

    lcd_module.main()
    expected_result = _response(executions=[
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=0, stdout="TEST.REGIONS.LCD VSAM", stderr="stderr"),
        _execution(name="ICETOOL - Get record count", rc=0, stdout="RECORD COUNT:  000000000000052", stderr="stderr"),
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=0, stdout="TEST.REGIONS.LCD VSAM", stderr="stderr"),
    ],
        start_state=_state(exists=True, vsam=True),
        end_state=_state(exists=True, vsam=True)
    )
    assert lcd_module.result == expected_result


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_error_warm_start_a_unused_local_catalog():
    lcd_module = initialise_module(state="warm")

    dataset_utils.ikjeft01 = MagicMock(return_value=(0, "TEST.REGIONS.LCD VSAM", "stderr"))
    icetool._execute_icetool = MagicMock(return_value=MVSCmdResponse(rc=0, stdout="RECORD COUNT:  000000000000000", stderr="stderr"))

    lcd_module.main()

    expected_result = _response(executions=[
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=0, stdout="TEST.REGIONS.LCD VSAM", stderr="stderr"),
        _execution(name="ICETOOL - Get record count", rc=0, stdout="RECORD COUNT:  000000000000000", stderr="stderr"),
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=0, stdout="TEST.REGIONS.LCD VSAM", stderr="stderr"),
    ],
        start_state=_state(exists=True, vsam=True),
        end_state=_state(exists=True, vsam=True)
    )
    expected_result.update({"failed": True})
    assert lcd_module.result == expected_result


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_error_warm_start_a_non_existent_local_catalog():
    lcd_module = initialise_module(state="warm")

    dataset_utils.ikjeft01 = MagicMock(return_value=(8, "TEST.REGIONS.LCD NOT IN CATALOG", "stderr"))
    icetool._execute_icetool = MagicMock(return_value=MVSCmdResponse(rc=0, stdout="RECORD COUNT:  000000000000052", stderr="stderr"))

    lcd_module.main()
    expected_result = _response(executions=[
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=8, stdout="TEST.REGIONS.LCD NOT IN CATALOG", stderr="stderr"),
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=8, stdout="TEST.REGIONS.LCD NOT IN CATALOG", stderr="stderr"),
    ],
        start_state=_state(exists=False, vsam=False),
        end_state=_state(exists=False, vsam=False)
    )
    expected_result.update({"failed": True})
    assert lcd_module.result == expected_result


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_bad_response_from_ccutl():
    lcd_module = initialise_module()

    dataset_utils.idcams = MagicMock(return_value=(0, "TEST.REGIONS.LCD", "stderr"))
    dataset_utils.ikjeft01 = MagicMock(side_effect=[(8, "TEST.REGIONS.LCD NOT IN CATALOG", "stderr"), (0, "TEST.REGIONS.LCD VSAM", "stderr")])
    local_catalog_utils._execute_dfhccutl = MagicMock(return_value=MVSCmdResponse(rc=99, stdout="stdout", stderr="stderr"))

    lcd_module.main()
    expected_result = _response(executions=[
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=8, stdout="TEST.REGIONS.LCD NOT IN CATALOG", stderr="stderr"),
        _execution(name="IDCAMS - Create local catalog data set - Run 1", rc=0, stdout="TEST.REGIONS.LCD", stderr="stderr"),
        _execution(name="DFHCCUTL - Initialise Local Catalog", rc=99, stdout="stdout", stderr="stderr"),
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=0, stdout="TEST.REGIONS.LCD VSAM", stderr="stderr")
    ],
        start_state=_state(exists=False, vsam=False),
        end_state=_state(exists=True, vsam=True)
    )
    expected_result.update({"changed": True})
    expected_result.update({"failed": True})
    assert lcd_module.result == expected_result
