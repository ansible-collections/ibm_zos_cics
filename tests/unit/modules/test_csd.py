# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import absolute_import, division, print_function
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import dataset_utils
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import csd as csd_utils
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import icetool
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.response import _execution
from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.data_set_helper import (
    PYTHON_LANGUAGE_FEATURES_MESSAGE,
    CSDUP_name,
    CSDUP_stderr,
    CSDUP_stdout,
    ICETOOL_name,
    ICETOOL_stderr,
    ICETOOL_stdout,
    IDCAMS_delete_run_name,
    IDCAMS_delete_vsam,
    IDCAMS_create_run_name,
    LISTDS_data_set_doesnt_exist,
    LISTDS_data_set,
    LISTDS_run_name,
    set_module_args
)
from ansible_collections.ibm.ibm_zos_cics.plugins.modules import csd
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.zos_mvs_raw import MVSCmdResponse
import pytest
import sys


try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock


__metaclass__ = type


NAME = "TEST.REGIONS.CSD"

default_arg_parms = {
    "space_primary": 5,
    "space_type": "M",
    "region_data_sets": {
        "dfhcsd": {
            "dsn": NAME
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


@pytest.mark.skipif(
    sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE
)
def test_create_an_intial_csd():
    csd_module = initialise_module()

    dataset_utils.idcams = MagicMock(
        return_value=(0, NAME, "")
    )
    dataset_utils.ikjeft01 = MagicMock(
        side_effect=[
            (8, LISTDS_data_set_doesnt_exist(NAME), ""),
            (0, LISTDS_data_set(NAME, "VSAM"), ""),
        ]
    )
    csd_utils._execute_dfhcsdup = MagicMock(
        return_value=MVSCmdResponse(rc=0, stdout=CSDUP_stdout(NAME), stderr=CSDUP_stderr(NAME))
    )

    csd_module.main()
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
                stdout=NAME,
                stderr="",
            ),
            _execution(
                name=CSDUP_name(),
                rc=0,
                stdout=CSDUP_stdout(NAME),
                stderr=CSDUP_stderr(NAME)
            ),
            _execution(
                name=LISTDS_run_name(1),
                rc=0,
                stdout=LISTDS_data_set(NAME, "VSAM"),
                stderr="",
            )
        ],
        start_state=dict(
            exists=False,
            data_set_organization="NONE"
        ),
        end_state=dict(
            exists=True,
            data_set_organization="VSAM"
        ),
        changed=True,
        failed=False
    )
    assert csd_module.get_result() == expected_result


@pytest.mark.skipif(
    sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE
)
def test_delete_an_existing_csd():
    csd_module = initialise_module(state="absent")

    dataset_utils.idcams = MagicMock(
        return_value=(0, IDCAMS_delete_vsam(NAME), "")
    )
    dataset_utils.ikjeft01 = MagicMock(
        side_effect=[
            (0, LISTDS_data_set(NAME, "VSAM"), ""),
            (8, LISTDS_data_set_doesnt_exist(NAME), ""),
        ]
    )

    csd_module.main()
    expected_result = dict(
        executions=[
            _execution(
                name=LISTDS_run_name(1),
                rc=0,
                stdout=LISTDS_data_set(NAME, "VSAM"),
                stderr="",
            ),
            _execution(
                name=IDCAMS_delete_run_name(1, NAME),
                rc=0,
                stdout=IDCAMS_delete_vsam(NAME),
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
            data_set_organization="VSAM"
        ),
        end_state=dict(
            exists=False,
            data_set_organization="NONE"
        ),
        changed=True,
        failed=False
    )
    assert csd_module.get_result() == expected_result


@pytest.mark.skipif(
    sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE
)
def test_do_nothing_to_an_existing_csd():
    csd_module = initialise_module()

    dataset_utils.ikjeft01 = MagicMock(side_effect=[(0, LISTDS_data_set(NAME, "VSAM"), ""), (0, LISTDS_data_set(NAME, "VSAM"), "")])
    icetool._execute_icetool = MagicMock(
        return_value=MVSCmdResponse(
            rc=0,
            stdout=ICETOOL_stdout(0),
            stderr=ICETOOL_stderr()
        )
    )
    csd_utils._execute_dfhcsdup = MagicMock(
        return_value=MVSCmdResponse(rc=0, stdout=CSDUP_stdout(NAME), stderr=CSDUP_stderr(NAME))
    )

    csd_module.main()
    expected_result = dict(
        executions=[
            _execution(
                name=LISTDS_run_name(1),
                rc=0,
                stdout=LISTDS_data_set(NAME, "VSAM"),
                stderr="",
            ),
            _execution(
                name=ICETOOL_name(1),
                rc=0,
                stdout=ICETOOL_stdout(0),
                stderr=ICETOOL_stderr()
            ),
            _execution(
                name=CSDUP_name(),
                rc=0,
                stdout=CSDUP_stdout(NAME),
                stderr=CSDUP_stderr(NAME)
            ),
            _execution(
                name=LISTDS_run_name(1),
                rc=0,
                stdout=LISTDS_data_set(NAME, "VSAM"),
                stderr="",
            ),
        ],
        start_state=dict(
            exists=True,
            data_set_organization="VSAM"
        ),
        end_state=dict(
            exists=True,
            data_set_organization="VSAM"
        ),
        changed=False,
        failed=False
    )
    assert csd_module.get_result() == expected_result


@pytest.mark.skipif(
    sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE
)
def test_remove_non_existent_csd():
    csd_module = initialise_module(state="absent")

    dataset_utils.ikjeft01 = MagicMock(
        return_value=(8, LISTDS_data_set_doesnt_exist(NAME), "")
    )

    csd_module.main()
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
            data_set_organization="NONE"
        ),
        end_state=dict(
            exists=False,
            data_set_organization="NONE"
        ),
        changed=False,
        failed=False
    )
    assert csd_module.get_result() == expected_result


@pytest.mark.skipif(
    sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE
)
def test_warm_start_a_existing_csd():
    csd_module = initialise_module(state="warm")

    dataset_utils.ikjeft01 = MagicMock(
        return_value=(
            0,
            LISTDS_data_set(NAME, "VSAM"),
            ""
        )
    )
    icetool._execute_icetool = MagicMock(
        return_value=MVSCmdResponse(
            rc=0,
            stdout=ICETOOL_stdout(52),
            stderr=ICETOOL_stderr()
        )
    )

    csd_module.main()
    expected_result = dict(
        executions=[
            _execution(
                name=LISTDS_run_name(1),
                rc=0,
                stdout=LISTDS_data_set(NAME, "VSAM"),
                stderr=""),
            _execution(
                name=ICETOOL_name(1),
                rc=0,
                stdout=ICETOOL_stdout(52),
                stderr=ICETOOL_stderr(),
            ),
            _execution(
                name=LISTDS_run_name(1),
                rc=0,
                stdout=LISTDS_data_set(NAME, "VSAM"),
                stderr=""),
        ],
        start_state=dict(
            exists=True,
            data_set_organization="VSAM"
        ),
        end_state=dict(
            exists=True,
            data_set_organization="VSAM"
        ),
        changed=False,
        failed=False
    )
    assert csd_module.get_result() == expected_result


@pytest.mark.skipif(
    sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE
)
def test_error_warm_start_a_unused_csd():
    csd_module = initialise_module(state="warm")

    dataset_utils.ikjeft01 = MagicMock(
        return_value=(
            0,
            LISTDS_data_set(NAME, "VSAM"),
            ""
        )
    )
    icetool._execute_icetool = MagicMock(
        return_value=MVSCmdResponse(
            rc=0,
            stdout=ICETOOL_stdout(0),
            stderr=ICETOOL_stderr()
        )
    )
    csd_module.main()

    expected_result = dict(
        executions=[
            _execution(
                name=LISTDS_run_name(1),
                rc=0,
                stdout=LISTDS_data_set(NAME, "VSAM"),
                stderr=""),
            _execution(
                name=ICETOOL_name(1),
                rc=0,
                stdout=ICETOOL_stdout(0),
                stderr=ICETOOL_stderr()),
            _execution(
                name=LISTDS_run_name(1),
                rc=0,
                stdout=LISTDS_data_set(NAME, "VSAM"),
                stderr=""),
        ],
        start_state=dict(
            exists=True,
            data_set_organization="VSAM"
        ),
        end_state=dict(
            exists=True,
            data_set_organization="VSAM"
        ),
        changed=False,
        failed=True
    )
    assert csd_module.get_result() == expected_result


@pytest.mark.skipif(sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE)
def test_error_warm_start_a_non_existent_csd():
    csd_module = initialise_module(state="warm")

    dataset_utils.ikjeft01 = MagicMock(return_value=(
        8, LISTDS_data_set_doesnt_exist(NAME), ""))

    csd_module.main()
    expected_result = dict(
        executions=[
            _execution(
                name=LISTDS_run_name(1),
                rc=8,
                stdout=LISTDS_data_set_doesnt_exist(NAME),
                stderr=""),
            _execution(
                name=LISTDS_run_name(1),
                rc=8,
                stdout=LISTDS_data_set_doesnt_exist(NAME),
                stderr=""),
        ],
        start_state=dict(
            exists=False,
            data_set_organization="NONE"
        ),
        end_state=dict(
            exists=False,
            data_set_organization="NONE"
        ),
        failed=True,
        changed=False
    )
    assert csd_module.get_result() == expected_result


@pytest.mark.skipif(sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE)
def test_bad_response_from_csdup():
    csd_module = initialise_module()

    dataset_utils.idcams = MagicMock(
        return_value=(0, NAME, "")
    )
    dataset_utils.ikjeft01 = MagicMock(
        side_effect=[
            (8, LISTDS_data_set_doesnt_exist(NAME), ""),
            (0, LISTDS_data_set(NAME, "VSAM"), ""),
        ]
    )
    csd_utils._execute_dfhcsdup = MagicMock(
        return_value=MVSCmdResponse(rc=99, stdout=CSDUP_stdout(NAME), stderr=CSDUP_stderr(NAME))
    )

    csd_module.main()
    expected_result = dict(
        executions=[
            _execution(
                name=LISTDS_run_name(1),
                rc=8,
                stdout=LISTDS_data_set_doesnt_exist(NAME),
                stderr=""
            ),
            _execution(
                name=IDCAMS_create_run_name(1, NAME),
                rc=0,
                stdout=NAME,
                stderr="",
            ),
            _execution(
                name=CSDUP_name(),
                rc=99,
                stdout=CSDUP_stdout(NAME),
                stderr=CSDUP_stderr(NAME)
            ),
            _execution(
                name=LISTDS_run_name(1),
                rc=0,
                stdout=LISTDS_data_set(NAME, "VSAM"),
                stderr="",
            ),
        ],
        start_state=dict(
            exists=False,
            data_set_organization="NONE"
        ),
        end_state=dict(
            exists=True,
            data_set_organization="VSAM"
        ),
        changed=True,
        failed=True
    )
    assert csd_module.get_result() == expected_result
