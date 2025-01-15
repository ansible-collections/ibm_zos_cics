# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023,2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import absolute_import, division, print_function
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import _data_set_utils as data_set_utils
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import _global_catalog as global_catalog_utils
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils._response import _execution
from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.data_set_helper import (
    PYTHON_LANGUAGE_FEATURES_MESSAGE,
    ICETOOL_name,
    ICETOOL_stderr,
    ICETOOL_stdout,
    IDCAMS_create_stdout,
    IDCAMS_delete_run_name,
    IDCAMS_delete,
    IDCAMS_create_run_name,
    LISTDS_data_set_doesnt_exist,
    LISTDS_data_set,
    LISTDS_run_name,
    RMUTL_get_run_name,
    RMUTL_stderr,
    RMUTL_stdout,
    RMUTL_update_run_name,
    set_module_args
)
from ansible_collections.ibm.ibm_zos_cics.plugins.modules import global_catalog
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import _icetool as icetool
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.zos_mvs_raw import MVSCmdResponse
import pytest
import sys


try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock


__metaclass__ = type

NAME = "TEST.REGIONS.GCD"

default_arg_parms = {
    "space_primary": 5,
    "space_secondary": 3,
    "space_type": "M",
    "region_data_sets": {
        "dfhgcd": {
            "dsn": NAME
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


@pytest.mark.skipif(
    sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE
)
def test_create_an_intial_global_catalog():
    gcd_module = initialise_module()

    data_set_utils._execute_idcams = MagicMock(
        return_value=MVSCmdResponse(0, IDCAMS_create_stdout(NAME), "")
    )
    data_set_utils._execute_listds = MagicMock(
        side_effect=[
            MVSCmdResponse(8, LISTDS_data_set_doesnt_exist(NAME), ""),
            MVSCmdResponse(0, LISTDS_data_set(NAME, "VSAM"), ""),
        ]
    )
    global_catalog_utils._execute_dfhrmutl = MagicMock(
        return_value=MVSCmdResponse(rc=0, stdout=RMUTL_stdout("AUTOINIT", "UNKNOWN"), stderr=RMUTL_stderr(NAME))
    )

    gcd_module.main()
    expected_result = dict(
        executions=[
            _execution(
                name=LISTDS_run_name(1),
                rc=8,
                stdout=LISTDS_data_set_doesnt_exist(NAME),
                stderr="",
            ),
            _execution(
                name=IDCAMS_create_run_name(1, NAME),
                rc=0,
                stdout=IDCAMS_create_stdout(NAME),
                stderr="",
            ),
            _execution(
                name=RMUTL_update_run_name(1),
                rc=0,
                stdout=RMUTL_stdout("AUTOINIT", "UNKNOWN"),
                stderr=RMUTL_stderr(NAME)
            ),
            _execution(
                name=LISTDS_run_name(1),
                rc=0,
                stdout=LISTDS_data_set(NAME, "VSAM"),
                stderr="",
            ),
            _execution(
                name=RMUTL_get_run_name(1),
                rc=0,
                stdout=RMUTL_stdout("AUTOINIT", "UNKNOWN"),
                stderr=RMUTL_stderr(NAME)
            ),
        ],
        start_state=dict(
            exists=False,
            data_set_organization="NONE",
            next_start="",
            autostart_override=""
        ),
        end_state=dict(
            exists=True,
            data_set_organization="VSAM",
            next_start="UNKNOWN",
            autostart_override="AUTOINIT"
        ),
        changed=True,
        failed=False,
        msg="",
    )
    assert gcd_module.get_result() == expected_result


@pytest.mark.skipif(
    sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE
)
def test_delete_an_existing_global_catalog():
    gcd_module = initialise_module(state="absent")

    data_set_utils._execute_idcams = MagicMock(
        return_value=MVSCmdResponse(0, IDCAMS_delete(NAME), ""),
    )

    data_set_utils._execute_listds = MagicMock(
        side_effect=[
            MVSCmdResponse(0, LISTDS_data_set(NAME, "VSAM"), ""),
            MVSCmdResponse(8, LISTDS_data_set_doesnt_exist(NAME), ""),
        ]
    )
    icetool._execute_icetool = MagicMock(
        return_value=MVSCmdResponse(
            rc=0,
            stdout=ICETOOL_stdout(0),
            stderr=ICETOOL_stderr()
        )
    )
    global_catalog_utils._execute_dfhrmutl = MagicMock(
        return_value=MVSCmdResponse(rc=0, stdout=RMUTL_stdout("AUTOINIT", "UNKNOWN"), stderr=RMUTL_stderr(NAME))
    )

    gcd_module.main()
    expected_result = dict(
        executions=[
            _execution(
                name=LISTDS_run_name(1),
                rc=0,
                stdout=LISTDS_data_set(NAME, "VSAM"),
                stderr="",
            ),
            _execution(
                name=RMUTL_get_run_name(1),
                rc=0,
                stdout=RMUTL_stdout("AUTOINIT", "UNKNOWN"),
                stderr=RMUTL_stderr(NAME)
            ),
            _execution(
                name=IDCAMS_delete_run_name(1, NAME),
                rc=0,
                stdout=IDCAMS_delete(NAME),
                stderr="",
            ),
            _execution(
                name=LISTDS_run_name(1),
                rc=8,
                stdout=LISTDS_data_set_doesnt_exist(NAME),
                stderr="",
            ),
        ],
        start_state=dict(
            exists=True,
            data_set_organization="VSAM",
            next_start="UNKNOWN",
            autostart_override="AUTOINIT"
        ),
        end_state=dict(
            exists=False,
            data_set_organization="NONE",
            next_start="",
            autostart_override=""
        ),
        changed=True,
        failed=False,
        msg="",
    )
    assert gcd_module.get_result() == expected_result


@pytest.mark.skipif(
    sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE
)
def test_remove_non_existent_global_catalog():
    gcd_module = initialise_module(state="absent")

    data_set_utils._execute_listds = MagicMock(
        return_value=MVSCmdResponse(8, LISTDS_data_set_doesnt_exist(NAME), "")
    )
    gcd_module.main()
    expected_result = dict(
        executions=[
            _execution(
                name=LISTDS_run_name(1),
                rc=8,
                stdout=LISTDS_data_set_doesnt_exist(NAME),
                stderr="",
            ),
            _execution(
                name=LISTDS_run_name(1),
                rc=8,
                stdout=LISTDS_data_set_doesnt_exist(NAME),
                stderr="",
            ),
        ],
        start_state=dict(
            exists=False,
            data_set_organization="NONE",
            next_start="",
            autostart_override=""
        ),
        end_state=dict(
            exists=False,
            data_set_organization="NONE",
            next_start="",
            autostart_override=""
        ),
        changed=False,
        failed=False,
        msg="",
    )
    assert gcd_module.get_result() == expected_result


@pytest.mark.skipif(
    sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE
)
def test_warm_start_a_global_catalog():
    gcd_module = initialise_module(state="warm")

    data_set_utils._execute_listds = MagicMock(
        return_value=MVSCmdResponse(
            0,
            LISTDS_data_set(NAME, "VSAM"),
            ""
        )
    )
    global_catalog_utils._execute_dfhrmutl = MagicMock(
        return_value=MVSCmdResponse(rc=0, stdout=RMUTL_stdout("AUTOASIS", "UNKNOWN"), stderr=RMUTL_stderr(NAME))
    )
    icetool._execute_icetool = MagicMock(
        return_value=MVSCmdResponse(
            rc=0,
            stdout=ICETOOL_stdout(52),
            stderr=ICETOOL_stderr()
        )
    )

    gcd_module.main()
    expected_result = dict(
        executions=[
            _execution(
                name=LISTDS_run_name(1),
                rc=0,
                stdout=LISTDS_data_set(NAME, "VSAM"),
                stderr=""),
            _execution(
                name=RMUTL_get_run_name(1),
                rc=0,
                stdout=RMUTL_stdout("AUTOASIS", "UNKNOWN"),
                stderr=RMUTL_stderr(NAME)
            ),
            _execution(
                name=ICETOOL_name(1),
                rc=0,
                stdout=ICETOOL_stdout(52),
                stderr=ICETOOL_stderr()
            ),
            _execution(
                name=RMUTL_update_run_name(1),
                rc=0,
                stdout=RMUTL_stdout("AUTOASIS", "UNKNOWN"),
                stderr=RMUTL_stderr(NAME)
            ),
            _execution(
                name=LISTDS_run_name(1),
                rc=0,
                stdout=LISTDS_data_set(NAME, "VSAM"),
                stderr=""),
            _execution(
                name=RMUTL_get_run_name(1),
                rc=0,
                stdout=RMUTL_stdout("AUTOASIS", "UNKNOWN"),
                stderr=RMUTL_stderr(NAME)
            ),
        ],
        start_state=dict(
            exists=True,
            data_set_organization="VSAM",
            next_start="UNKNOWN",
            autostart_override="AUTOASIS"
        ),
        end_state=dict(
            exists=True,
            data_set_organization="VSAM",
            next_start="UNKNOWN",
            autostart_override="AUTOASIS"
        ),
        changed=True,
        failed=False,
        msg="",
    )
    assert gcd_module.get_result() == expected_result


@pytest.mark.skipif(
    sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE
)
def test_error_warm_start_a_unused_global_catalog():
    gcd_module = initialise_module(state="warm")

    data_set_utils._execute_listds = MagicMock(
        return_value=MVSCmdResponse(
            0,
            LISTDS_data_set(NAME, "VSAM"),
            ""
        )
    )
    global_catalog_utils._execute_dfhrmutl = MagicMock(
        return_value=MVSCmdResponse(rc=0, stdout=RMUTL_stdout("AUTOINIT", "UNKNOWN"), stderr=RMUTL_stderr(NAME))
    )
    icetool._execute_icetool = MagicMock(
        return_value=MVSCmdResponse(
            rc=0,
            stdout=ICETOOL_stdout(0),
            stderr=ICETOOL_stderr()
        )
    )
    gcd_module.main()

    expected_result = dict(
        executions=[
            _execution(
                name=LISTDS_run_name(1),
                rc=0,
                stdout=LISTDS_data_set(NAME, "VSAM"),
                stderr=""
            ),
            _execution(
                name=RMUTL_get_run_name(1),
                rc=0,
                stdout=RMUTL_stdout("AUTOINIT", "UNKNOWN"),
                stderr=RMUTL_stderr(NAME)
            ),
            _execution(
                name=ICETOOL_name(1),
                rc=0,
                stdout=ICETOOL_stdout(0),
                stderr=ICETOOL_stderr()),
            _execution(
                name=RMUTL_update_run_name(1),
                rc=0,
                stdout=RMUTL_stdout("AUTOINIT", "UNKNOWN"),
                stderr=RMUTL_stderr(NAME)
            ),
            _execution(
                name=LISTDS_run_name(1),
                rc=0,
                stdout=LISTDS_data_set(NAME, "VSAM"),
                stderr=""
            ),
            _execution(
                name=RMUTL_get_run_name(1),
                rc=0,
                stdout=RMUTL_stdout("AUTOINIT", "UNKNOWN"),
                stderr=RMUTL_stderr(NAME)
            ),
        ],
        start_state=dict(
            exists=True,
            data_set_organization="VSAM",
            next_start="UNKNOWN",
            autostart_override="AUTOINIT"
        ),
        end_state=dict(
            exists=True,
            data_set_organization="VSAM",
            next_start="UNKNOWN",
            autostart_override="AUTOINIT"
        ),
        changed=True,
        failed=True,
        msg="Unused catalog. The catalog must be used by CICS before doing a warm start.",
    )
    assert gcd_module.get_result() == expected_result


@pytest.mark.skipif(
    sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE
)
def test_error_warm_start_a_non_existent_global_catalog():
    gcd_module = initialise_module(state="warm")

    data_set_utils._execute_listds = MagicMock(
        return_value=MVSCmdResponse(8, LISTDS_data_set_doesnt_exist(NAME), "")
    )
    global_catalog_utils._execute_dfhrmutl = MagicMock(
        return_value=MVSCmdResponse(rc=0, stdout=RMUTL_stdout("AUTOINIT", "UNKNOWN"), stderr=RMUTL_stderr(NAME))
    )

    gcd_module.main()
    expected_result = dict(
        executions=[
            _execution(
                name=LISTDS_run_name(1),
                rc=8,
                stdout=LISTDS_data_set_doesnt_exist(NAME),
                stderr=""
            ),
            _execution(
                name=RMUTL_update_run_name(1),
                rc=0,
                stdout=RMUTL_stdout("AUTOINIT", "UNKNOWN"),
                stderr=RMUTL_stderr(NAME)
            ),
            _execution(
                name=LISTDS_run_name(1),
                rc=8,
                stdout=LISTDS_data_set_doesnt_exist(NAME),
                stderr=""
            ),
        ],
        start_state=dict(
            exists=False,
            data_set_organization="NONE",
            next_start="",
            autostart_override=""
        ),
        end_state=dict(
            exists=False,
            data_set_organization="NONE",
            next_start="",
            autostart_override=""
        ),
        failed=True,
        changed=True,
        msg="Data set {0} does not exist.".format(NAME),
    )
    assert gcd_module.get_result() == expected_result


@pytest.mark.skipif(
    sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE
)
def tests_cold_start_non_existent_catalog():
    gcd_module = initialise_module(state="cold")

    data_set_utils._execute_listds = MagicMock(
        return_value=MVSCmdResponse(8, LISTDS_data_set_doesnt_exist(NAME), "")
    )
    global_catalog_utils._execute_dfhrmutl = MagicMock(
        return_value=MVSCmdResponse(rc=0, stdout=RMUTL_stdout("AUTOCOLD", "UNKNOWN"), stderr=RMUTL_stderr(NAME))
    )

    gcd_module.main()
    expected_result = dict(
        executions=[
            _execution(
                name=LISTDS_run_name(1),
                rc=8,
                stdout=LISTDS_data_set_doesnt_exist(NAME),
                stderr=""
            ),
            _execution(
                name=RMUTL_update_run_name(1),
                rc=0,
                stdout=RMUTL_stdout("AUTOCOLD", "UNKNOWN"),
                stderr=RMUTL_stderr(NAME)
            ),
            _execution(
                name=LISTDS_run_name(1),
                rc=8,
                stdout=LISTDS_data_set_doesnt_exist(NAME),
                stderr=""
            ),
        ],
        start_state=dict(
            exists=False,
            data_set_organization="NONE",
            next_start="",
            autostart_override=""
        ),
        end_state=dict(
            exists=False,
            data_set_organization="NONE",
            next_start="",
            autostart_override=""
        ),
        failed=True,
        changed=True,
        msg="Data set {0} does not exist.".format(NAME),
    )
    assert gcd_module.get_result() == expected_result


@pytest.mark.skipif(
    sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE
)
def test_cold_start_unused_catalog():
    gcd_module = initialise_module(state="cold")

    data_set_utils._execute_listds = MagicMock(
        return_value=MVSCmdResponse(0, LISTDS_data_set(NAME, "VSAM"), "")
    )
    global_catalog_utils._execute_dfhrmutl = MagicMock(
        return_value=MVSCmdResponse(rc=0, stdout=RMUTL_stdout("AUTOINIT", "UNKNOWN"), stderr=RMUTL_stderr(NAME))
    )

    gcd_module.main()
    expected_result = dict(
        executions=[
            _execution(
                name=LISTDS_run_name(1),
                rc=0,
                stdout=LISTDS_data_set(NAME, "VSAM"),
                stderr="",
            ),
            _execution(
                name=RMUTL_get_run_name(1),
                rc=0,
                stdout=RMUTL_stdout("AUTOINIT", "UNKNOWN"),
                stderr=RMUTL_stderr(NAME)
            ),
            _execution(
                name=RMUTL_update_run_name(1),
                rc=0,
                stdout=RMUTL_stdout("AUTOINIT", "UNKNOWN"),
                stderr=RMUTL_stderr(NAME)
            ),
            _execution(
                name=LISTDS_run_name(1),
                rc=0,
                stdout=LISTDS_data_set(NAME, "VSAM"),
                stderr="",
            ),
            _execution(
                name=RMUTL_get_run_name(1),
                rc=0,
                stdout=RMUTL_stdout("AUTOINIT", "UNKNOWN"),
                stderr=RMUTL_stderr(NAME)
            ),
        ],
        start_state=dict(
            exists=True,
            data_set_organization="VSAM",
            next_start="UNKNOWN",
            autostart_override="AUTOINIT"
        ),
        end_state=dict(
            exists=True,
            data_set_organization="VSAM",
            next_start="UNKNOWN",
            autostart_override="AUTOINIT"
        ),
        changed=True,
        failed=True,
        msg="Unused catalog. The catalog must be used by CICS before doing a cold start.",
    )
    assert gcd_module.get_result() == expected_result


@pytest.mark.skipif(
    sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE
)
def test_cold_start_global_catalog():
    gcd_module = initialise_module(state="cold")

    data_set_utils._execute_listds = MagicMock(
        return_value=MVSCmdResponse(0, LISTDS_data_set(NAME, "VSAM"), "")
    )
    global_catalog_utils._execute_dfhrmutl = MagicMock(
        return_value=MVSCmdResponse(rc=0, stdout=RMUTL_stdout("AUTOCOLD", "UNKNOWN"), stderr=RMUTL_stderr(NAME))
    )

    gcd_module.main()
    expected_result = dict(
        executions=[
            _execution(
                name=LISTDS_run_name(1),
                rc=0,
                stdout=LISTDS_data_set(NAME, "VSAM"),
                stderr=""
            ),
            _execution(
                name=RMUTL_get_run_name(1),
                rc=0,
                stdout=RMUTL_stdout("AUTOCOLD", "UNKNOWN"),
                stderr=RMUTL_stderr(NAME)
            ),
            _execution(
                name=RMUTL_update_run_name(1),
                rc=0,
                stdout=RMUTL_stdout("AUTOCOLD", "UNKNOWN"),
                stderr=RMUTL_stderr(NAME)
            ),
            _execution(
                name=LISTDS_run_name(1),
                rc=0,
                stdout=LISTDS_data_set(NAME, "VSAM"),
                stderr=""
            ),
            _execution(
                name=RMUTL_get_run_name(1),
                rc=0,
                stdout=RMUTL_stdout("AUTOCOLD", "UNKNOWN"),
                stderr=RMUTL_stderr(NAME)
            ),
        ],
        start_state=dict(
            exists=True,
            data_set_organization="VSAM",
            next_start="UNKNOWN",
            autostart_override="AUTOCOLD"
        ),
        end_state=dict(
            exists=True,
            data_set_organization="VSAM",
            next_start="UNKNOWN",
            autostart_override="AUTOCOLD"
        ),
        changed=True,
        failed=False,
        msg="",
    )
    assert gcd_module.get_result() == expected_result
