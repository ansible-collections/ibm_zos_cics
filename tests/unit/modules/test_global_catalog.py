# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import absolute_import, division, print_function
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import dataset_utils
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import global_catalog as global_catalog_utils
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.response import _execution, _response, _state
from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.data_set_helper import set_data_set, set_module_args
from ansible_collections.ibm.ibm_zos_cics.plugins.modules import global_catalog
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import icetool
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
        "dfhgcd": {
            "dsn": "TEST.REGIONS.GCD"
        }
    },
    "cics_data_sets": {
        "sdfhload": "TEST.CICS.INSTALL.SDFHLOAD"
    },
    "state": "initial"
}


def initialise_module(**kwargs):
    initial_args = default_arg_parms
    initial_args.update(kwargs)
    set_module_args(initial_args)
    gcd_module = global_catalog.AnsibleGlobalCatalogModule()
    # Mock Ansible module fail and exits, this prevents sys.exit being called but retains an accurate results
    gcd_module._module.fail_json = MagicMock(return_value=None)
    gcd_module._module.exit_json = MagicMock(return_value=None)
    return gcd_module


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_create_an_intial_global_catalog():
    gcd_module = initialise_module()

    dataset_utils.idcams = MagicMock(return_value=(0, "TEST.REGIONS.GCD", "stderr"))
    dataset_utils.ikjeft01 = MagicMock(side_effect=[(8, "TEST.REGIONS.GCD NOT IN CATALOG", "stderr"), (0, "TEST.REGIONS.GCD VSAM", "stderr")])
    global_catalog_utils._execute_dfhrmutl = MagicMock(return_value=MVSCmdResponse(rc=0, stdout="stdout", stderr="stderr"))

    gcd_module.main()
    expected_result = _response(executions=[
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=8, stdout="TEST.REGIONS.GCD NOT IN CATALOG", stderr="stderr"),
        _execution(name="IDCAMS - Create global catalog data set - Run 1", rc=0, stdout="TEST.REGIONS.GCD", stderr="stderr"),
        _execution(name="DFHRMUTL - Updating autostart override - Run 1", rc=0, stdout="stdout", stderr="stderr"),
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=0, stdout="TEST.REGIONS.GCD VSAM", stderr="stderr"),
        _execution(name="DFHRMUTL - Get current catalog - Run 1", rc=0, stdout="stdout", stderr="stderr")
    ],
        start_state=_state(exists=False, vsam=False, autostart_override="", next_start=""),
        end_state=_state(exists=True, vsam=True, autostart_override=None, next_start=None)
    )
    expected_result.update({"changed": True})
    assert gcd_module.result == expected_result


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_delete_an_existing_global_catalog():
    gcd_module = initialise_module(state="absent")

    dataset_utils.idcams = MagicMock(return_value=(0, "ENTRY (C) TEST.REGIONS.GCD DELETED\n", "stderr"))
    dataset_utils.ikjeft01 = MagicMock(side_effect=[(0, "TEST.REGIONS.GCD VSAM", "stderr"), (8, "TEST.REGIONS.GCD NOT IN CATALOG", "stderr")])
    global_catalog_utils._execute_dfhrmutl = MagicMock(return_value=MVSCmdResponse(rc=0, stdout="stdout", stderr="stderr"))

    gcd_module.main()
    expected_result = _response(executions=[
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=0, stdout="TEST.REGIONS.GCD VSAM", stderr="stderr"),
        _execution(name="DFHRMUTL - Get current catalog - Run 1", rc=0, stdout="stdout", stderr="stderr"),
        _execution(name="IDCAMS - Removing global catalog data set - Run 1", rc=0, stdout="ENTRY (C) TEST.REGIONS.GCD DELETED\n", stderr="stderr"),
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=8, stdout="TEST.REGIONS.GCD NOT IN CATALOG", stderr="stderr")
    ],
        start_state=_state(exists=True, vsam=True, autostart_override=None, next_start=None),
        end_state=_state(exists=False, vsam=False, autostart_override="", next_start="")
    )
    expected_result.update({"changed": True})
    assert gcd_module.result == expected_result


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_remove_non_existent_global_catalog():
    gcd_module = initialise_module(state="absent")

    dataset_utils.idcams = MagicMock(return_value=(8, "ENTRY TEST.REGIONS.GCD NOTFOUND", "stderr"))
    dataset_utils.ikjeft01 = MagicMock(return_value=(8, "TEST.REGIONS.GCD NOT IN CATALOG", "stderr"))

    gcd_module.main()
    expected_result = _response(executions=[
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=8, stdout="TEST.REGIONS.GCD NOT IN CATALOG", stderr="stderr"),
        _execution(name="IDCAMS - Removing global catalog data set - Run 1", rc=8, stdout="ENTRY TEST.REGIONS.GCD NOTFOUND", stderr="stderr"),
        _execution(name="IKJEFT01 - Get Data Set Status - Run 1", rc=8, stdout="TEST.REGIONS.GCD NOT IN CATALOG", stderr="stderr")
    ],
        start_state=_state(exists=False, vsam=False, autostart_override="", next_start=""),
        end_state=_state(exists=False, vsam=False, autostart_override="", next_start="")
    )
    expected_result.update({"changed": True})
    assert gcd_module.result == expected_result


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_warm_start_a_global_catalog():
    gcd_module = initialise_module(state="warm")
    data_set = set_data_set(exists=True, name="TEST.REGIONS.GCD", vsam=True, sdfhload="TEST.CICS.INSTALL.SDFHLOAD")
    gcd_module.data_set = data_set

    dataset_utils.ikjeft01 = MagicMock(return_value=(0, "TEST.REGIONS.GCD VSAM", "stderr"))
    global_catalog_utils._execute_dfhrmutl = MagicMock(
        return_value=MVSCmdResponse(rc=0, stdout="auto-start override   : AUTOASIS \n next start type       : UNKNOWN", stderr="stderr")
    )

    gcd_module.main()
    expected_result = _response(executions=[
        _execution(
            name="IKJEFT01 - Get Data Set Status - Run 1",
            rc=0,
            stdout="TEST.REGIONS.GCD VSAM",
            stderr="stderr"
        ),
        _execution(
            name="DFHRMUTL - Get current catalog - Run 1",
            rc=0,
            stdout="auto-start override   : AUTOASIS \n next start type       : UNKNOWN",
            stderr="stderr"
        ),
        _execution(
            name="DFHRMUTL - Updating autostart override - Run 1",
            rc=0,
            stdout="auto-start override   : AUTOASIS \n next start type       : UNKNOWN",
            stderr="stderr"
        ),
        _execution(
            name="IKJEFT01 - Get Data Set Status - Run 1",
            rc=0,
            stdout="TEST.REGIONS.GCD VSAM",
            stderr="stderr"
        ),
        _execution(
            name="DFHRMUTL - Get current catalog - Run 1",
            rc=0,
            stdout="auto-start override   : AUTOASIS \n next start type       : UNKNOWN",
            stderr="stderr"
        ),
    ],
        start_state=_state(exists=True, vsam=True, autostart_override="AUTOASIS", next_start="UNKNOWN"),
        end_state=_state(exists=True, vsam=True, autostart_override="AUTOASIS", next_start="UNKNOWN")
    )
    expected_result.update({"changed": True})
    assert gcd_module.result == expected_result


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_error_warm_start_a_unused_global_catalog():
    gcd_module = initialise_module(state="warm")

    dataset_utils.ikjeft01 = MagicMock(return_value=(0, "TEST.REGIONS.GCD VSAM", "stderr"))
    global_catalog_utils._execute_dfhrmutl = MagicMock(
        return_value=MVSCmdResponse(rc=0, stdout="auto-start override   : AUTOINIT \n next start type       : UNKNOWN", stderr="stderr")
    )
    icetool._execute_icetool = MagicMock(return_value=MVSCmdResponse(rc=0, stdout="RECORD COUNT:  000000000000000", stderr="stderr"))

    gcd_module.main()

    expected_result = _response(executions=[
        _execution(
            name="IKJEFT01 - Get Data Set Status - Run 1",
            rc=0,
            stdout="TEST.REGIONS.GCD VSAM",
            stderr="stderr"
        ),
        _execution(
            name="DFHRMUTL - Get current catalog - Run 1",
            rc=0,
            stdout="auto-start override   : AUTOINIT \n next start type       : UNKNOWN",
            stderr="stderr"
        ),
        _execution(name="ICETOOL - Get record count", rc=0, stdout="RECORD COUNT:  000000000000000", stderr="stderr"),
        _execution(
            name="DFHRMUTL - Updating autostart override - Run 1",
            rc=0,
            stdout="auto-start override   : AUTOINIT \n next start type       : UNKNOWN",
            stderr="stderr"
        ),
        _execution(
            name="IKJEFT01 - Get Data Set Status - Run 1",
            rc=0,
            stdout="TEST.REGIONS.GCD VSAM",
            stderr="stderr"
        ),
        _execution(
            name="DFHRMUTL - Get current catalog - Run 1",
            rc=0,
            stdout="auto-start override   : AUTOINIT \n next start type       : UNKNOWN",
            stderr="stderr"
        ),
    ],
        start_state=_state(exists=True, vsam=True, autostart_override="AUTOINIT", next_start="UNKNOWN"),
        end_state=_state(exists=True, vsam=True, autostart_override="AUTOINIT", next_start="UNKNOWN")
    )
    expected_result.update({"changed": True})
    expected_result.update({"failed": True})
    assert gcd_module.result == expected_result


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_error_warm_start_a_non_existent_global_catalog():
    gcd_module = initialise_module(state="warm")

    dataset_utils.ikjeft01 = MagicMock(return_value=(8, "TEST.REGIONS.GCD NOT IN CATALOG", "stderr"))
    global_catalog_utils._execute_dfhrmutl = MagicMock(
        return_value=MVSCmdResponse(rc=0, stdout="auto-start override   : AUTOINIT \n next start type       : UNKNOWN", stderr="stderr")
    )

    gcd_module.main()
    expected_result = _response(executions=[
        _execution(
            name="IKJEFT01 - Get Data Set Status - Run 1",
            rc=8,
            stdout="TEST.REGIONS.GCD NOT IN CATALOG",
            stderr="stderr"
        ),
        _execution(
            name="DFHRMUTL - Updating autostart override - Run 1",
            rc=0,
            stdout="auto-start override   : AUTOINIT \n next start type       : UNKNOWN",
            stderr="stderr"
        ),
        _execution(
            name="IKJEFT01 - Get Data Set Status - Run 1",
            rc=8,
            stdout="TEST.REGIONS.GCD NOT IN CATALOG",
            stderr="stderr"
        ),
    ],
        start_state=_state(exists=False, vsam=False, autostart_override="", next_start=""),
        end_state=_state(exists=False, vsam=False, autostart_override="", next_start="")
    )
    expected_result.update({"changed": True})
    expected_result.update({"failed": True})
    assert gcd_module.result == expected_result


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def tests_cold_start_non_existent_catalog():
    gcd_module = initialise_module(state="cold")

    dataset_utils.ikjeft01 = MagicMock(return_value=(8, "TEST.REGIONS.GCD NOT IN CATALOG", "stderr"))
    global_catalog_utils._execute_dfhrmutl = MagicMock(
        return_value=MVSCmdResponse(rc=0, stdout="auto-start override   : AUTOCOLD \n next start type       : UNKNOWN", stderr="stderr")
    )

    gcd_module.main()
    expected_result = _response(executions=[
        _execution(
            name="IKJEFT01 - Get Data Set Status - Run 1",
            rc=8,
            stdout="TEST.REGIONS.GCD NOT IN CATALOG",
            stderr="stderr"
        ),
        _execution(
            name="DFHRMUTL - Updating autostart override - Run 1",
            rc=0,
            stdout="auto-start override   : AUTOCOLD \n next start type       : UNKNOWN",
            stderr="stderr"
        ),
        _execution(
            name="IKJEFT01 - Get Data Set Status - Run 1",
            rc=8,
            stdout="TEST.REGIONS.GCD NOT IN CATALOG",
            stderr="stderr"
        ),
    ],
        start_state=_state(exists=False, vsam=False, autostart_override="", next_start=""),
        end_state=_state(exists=False, vsam=False, autostart_override="", next_start="")
    )
    expected_result.update({"changed": True})
    expected_result.update({"failed": True})
    assert gcd_module.result == expected_result


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_cold_start_unused_catalog():
    gcd_module = initialise_module(state="cold")

    dataset_utils.ikjeft01 = MagicMock(return_value=(0, "TEST.REGIONS.GCD VSAM", "stderr"))
    global_catalog_utils._execute_dfhrmutl = MagicMock(
        return_value=MVSCmdResponse(rc=0, stdout="auto-start override   : AUTOINIT \n next start type       : UNKNOWN", stderr="stderr")
    )

    gcd_module.main()
    expected_result = _response(executions=[
        _execution(
            name="IKJEFT01 - Get Data Set Status - Run 1",
            rc=0,
            stdout="TEST.REGIONS.GCD VSAM",
            stderr="stderr"
        ),
        _execution(
            name="DFHRMUTL - Get current catalog - Run 1",
            rc=0,
            stdout="auto-start override   : AUTOINIT \n next start type       : UNKNOWN",
            stderr="stderr"
        ),
        _execution(
            name="DFHRMUTL - Updating autostart override - Run 1",
            rc=0,
            stdout="auto-start override   : AUTOINIT \n next start type       : UNKNOWN",
            stderr="stderr"
        ),
        _execution(
            name="IKJEFT01 - Get Data Set Status - Run 1",
            rc=0,
            stdout="TEST.REGIONS.GCD VSAM",
            stderr="stderr"
        ),
        _execution(
            name="DFHRMUTL - Get current catalog - Run 1",
            rc=0,
            stdout="auto-start override   : AUTOINIT \n next start type       : UNKNOWN",
            stderr="stderr"
        ),
    ],
        start_state=_state(exists=True, vsam=True, autostart_override="AUTOINIT", next_start="UNKNOWN"),
        end_state=_state(exists=True, vsam=True, autostart_override="AUTOINIT", next_start="UNKNOWN")
    )
    expected_result.update({"changed": True})
    expected_result.update({"failed": True})
    assert gcd_module.result == expected_result


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_cold_start_global_catalog():
    gcd_module = initialise_module(state="cold")

    dataset_utils.ikjeft01 = MagicMock(return_value=(0, "TEST.REGIONS.GCD VSAM", "stderr"))
    global_catalog_utils._execute_dfhrmutl = MagicMock(
        return_value=MVSCmdResponse(rc=0, stdout="auto-start override   : AUTOCOLD \n next start type       : UNKNOWN", stderr="stderr")
    )

    gcd_module.main()
    expected_result = _response(executions=[
        _execution(
            name="IKJEFT01 - Get Data Set Status - Run 1",
            rc=0,
            stdout="TEST.REGIONS.GCD VSAM",
            stderr="stderr"
        ),
        _execution(
            name="DFHRMUTL - Get current catalog - Run 1",
            rc=0,
            stdout="auto-start override   : AUTOCOLD \n next start type       : UNKNOWN",
            stderr="stderr"
        ),
        _execution(
            name="DFHRMUTL - Updating autostart override - Run 1",
            rc=0,
            stdout="auto-start override   : AUTOCOLD \n next start type       : UNKNOWN",
            stderr="stderr"
        ),
        _execution(
            name="IKJEFT01 - Get Data Set Status - Run 1",
            rc=0,
            stdout="TEST.REGIONS.GCD VSAM",
            stderr="stderr"
        ),
        _execution(
            name="DFHRMUTL - Get current catalog - Run 1",
            rc=0,
            stdout="auto-start override   : AUTOCOLD \n next start type       : UNKNOWN",
            stderr="stderr"
        ),
    ],
        start_state=_state(exists=True, vsam=True, autostart_override="AUTOCOLD", next_start="UNKNOWN"),
        end_state=_state(exists=True, vsam=True, autostart_override="AUTOCOLD", next_start="UNKNOWN")
    )
    expected_result.update({"changed": True})
    assert gcd_module.result == expected_result
