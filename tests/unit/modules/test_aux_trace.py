# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import absolute_import, division, print_function
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import _data_set_utils as data_set_utils
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils._response import _execution
from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.data_set_helper import (
    PYTHON_LANGUAGE_FEATURES_MESSAGE,
    IDCAMS_delete_run_name,
    IDCAMS_delete,
    IEFBR14_create_stderr,
    LISTDS_data_set_doesnt_exist,
    LISTDS_data_set,
    LISTDS_run_name,
    set_module_args
)
from ansible_collections.ibm.ibm_zos_cics.plugins.modules import aux_trace
import pytest
import sys

from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.zos_mvs_raw import MVSCmdResponse

try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock


__metaclass__ = type

NAMEA = "TEST.REGIONS.DFHAUXT"
NAMEB = "TEST.REGIONS.DFHBUXT"

default_arg_parms = {
    "space_primary": 20,
    "space_secondary": 3,
    "space_type": "M",
    "region_data_sets": {
        "dfhauxt": {
            "dsn": NAMEA
        },
        "dfhbuxt": {
            "dsn": NAMEB
        }
    },
    "state": "initial",
    "destination": "A"
}


def initialise_module(**kwargs):
    initial_args = default_arg_parms
    initial_args.update(kwargs)
    set_module_args(initial_args)
    trace_module = aux_trace.AnsibleAuxiliaryTraceModule()
    trace_module._module.fail_json = MagicMock(return_value=None)
    trace_module._module.exit_json = MagicMock(return_value=None)
    return trace_module


@pytest.mark.skipif(
    sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE
)
def test_create_an_intial_aux_trace():
    trace_module = initialise_module()

    data_set_utils._execute_listds = MagicMock(
        side_effect=[
            MVSCmdResponse(8, LISTDS_data_set_doesnt_exist(NAMEA), ""),
            MVSCmdResponse(0, LISTDS_data_set(NAMEA, "PS"), ""),
        ]
    )
    data_set_utils._execute_iefbr14 = MagicMock(
        return_value=MVSCmdResponse(
            rc=0, stdout="", stderr=IEFBR14_create_stderr(NAMEA, "DFHAUXT")
        )
    )

    trace_module.main()
    expected_result = dict(
        executions=[
            _execution(
                name=LISTDS_run_name(1),
                rc=8,
                stdout=LISTDS_data_set_doesnt_exist(NAMEA),
                stderr="",
            ),
            _execution(
                name="IEFBR14 - dfhauxt - Run 1",
                rc=0,
                stdout="",
                stderr=IEFBR14_create_stderr(NAMEA, "DFHAUXT")
            ),
            _execution(
                name=LISTDS_run_name(1),
                rc=0,
                stdout=LISTDS_data_set(NAMEA, "PS"),
                stderr="",
            ),
        ],
        start_state=dict(
            exists=False,
            data_set_organization="NONE"
        ),
        end_state=dict(
            exists=True,
            data_set_organization="Sequential"
        ),
        changed=True,
        failed=False,
        msg="",
    )
    assert trace_module.get_result() == expected_result


@pytest.mark.skipif(
    sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE
)
def test_delete_an_existing_aux_trace():
    trace_module = initialise_module(state="absent")

    data_set_utils._execute_idcams = MagicMock(
        return_value=MVSCmdResponse(0, IDCAMS_delete(NAMEA), "")
    )
    data_set_utils._execute_listds = MagicMock(
        side_effect=[
            MVSCmdResponse(0, LISTDS_data_set(NAMEA, "PS"), ""),
            MVSCmdResponse(8, LISTDS_data_set_doesnt_exist(NAMEA), ""),
        ]
    )

    trace_module.main()
    expected_result = dict(
        executions=[
            _execution(
                name=LISTDS_run_name(1),
                rc=0,
                stdout=LISTDS_data_set(NAMEA, "PS"),
                stderr="",
            ),
            _execution(
                name=IDCAMS_delete_run_name(1, NAMEA),
                rc=0,
                stdout=IDCAMS_delete(NAMEA),
                stderr=""
            ),
            _execution(
                name=LISTDS_run_name(1),
                rc=8,
                stdout=LISTDS_data_set_doesnt_exist(NAMEA),
                stderr="",
            ),
        ],
        start_state=dict(
            exists=True,
            data_set_organization="Sequential"
        ),
        end_state=dict(
            exists=False,
            data_set_organization="NONE"
        ),
        changed=True,
        failed=False,
        msg="",
    )
    assert trace_module.get_result() == expected_result


@pytest.mark.skipif(
    sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE
)
def test_remove_non_existent_aux_trace():
    trace_module = initialise_module(state="absent")

    data_set_utils._execute_listds = MagicMock(
        return_value=MVSCmdResponse(8, LISTDS_data_set_doesnt_exist(NAMEA), "")
    )

    trace_module.main()
    expected_result = dict(
        executions=[
            _execution(
                name=LISTDS_run_name(1),
                rc=8,
                stdout=LISTDS_data_set_doesnt_exist(NAMEA),
                stderr="",
            ),
            _execution(
                name=LISTDS_run_name(1),
                rc=8,
                stdout=LISTDS_data_set_doesnt_exist(NAMEA),
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
        failed=False,
        msg="",
    )
    assert trace_module.get_result() == expected_result


@pytest.mark.skipif(
    sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE
)
def test_create_an_intial_destination_b_aux_trace():
    trace_module = initialise_module(destination="B")

    data_set_utils._execute_listds = MagicMock(
        side_effect=[
            MVSCmdResponse(8, LISTDS_data_set_doesnt_exist(NAMEB), ""),
            MVSCmdResponse(0, LISTDS_data_set(NAMEB, "PS"), ""),
        ]
    )
    data_set_utils._execute_iefbr14 = MagicMock(
        return_value=MVSCmdResponse(
            rc=0, stdout="", stderr=IEFBR14_create_stderr(NAMEB, "DFHBUXT")
        )
    )

    trace_module.main()
    expected_result = dict(
        executions=[
            _execution(
                name=LISTDS_run_name(1),
                rc=8,
                stdout=LISTDS_data_set_doesnt_exist(NAMEB),
                stderr="",
            ),
            _execution(
                name="IEFBR14 - dfhbuxt - Run 1",
                rc=0,
                stdout="",
                stderr=IEFBR14_create_stderr(NAMEB, "DFHBUXT")),
            _execution(
                name=LISTDS_run_name(1),
                rc=0,
                stdout=LISTDS_data_set(NAMEB, "PS"),
                stderr="",
            ),
        ],
        start_state=dict(
            exists=False,
            data_set_organization="NONE"
        ),
        end_state=dict(
            exists=True,
            data_set_organization="Sequential"
        ),
        changed=True,
        failed=False,
        msg="",
    )
    assert trace_module.get_result() == expected_result


@pytest.mark.skipif(
    sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE
)
def test_warm_on_non_existent_aux():
    aux_module = initialise_module(state="warm")

    data_set_utils._execute_listds = MagicMock(
        return_value=MVSCmdResponse(8, LISTDS_data_set_doesnt_exist(NAMEA), "")
    )

    aux_module.main()
    expected_result = dict(
        executions=[
            _execution(
                name=LISTDS_run_name(1),
                rc=8,
                stdout=LISTDS_data_set_doesnt_exist(NAMEA),
                stderr="",
            ),
            _execution(
                name=LISTDS_run_name(1),
                rc=8,
                stdout=LISTDS_data_set_doesnt_exist(NAMEA),
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
        failed=True,
        changed=False,
        msg="Data set {0} does not exist.".format(NAMEA),
    )
    assert aux_module.get_result() == expected_result


@pytest.mark.skipif(
    sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE
)
def test_warm_success_aux():
    aux_module = initialise_module(state="warm")

    data_set_utils._execute_listds = MagicMock(
        return_value=MVSCmdResponse(0, LISTDS_data_set(NAMEA, "PS"), "")
    )

    aux_module.main()
    expected_result = dict(
        executions=[
            _execution(
                name=LISTDS_run_name(1),
                rc=0,
                stdout=LISTDS_data_set(NAMEA, "PS"),
                stderr="",
            ),
            _execution(
                name=LISTDS_run_name(1),
                rc=0,
                stdout=LISTDS_data_set(NAMEA, "PS"),
                stderr="",
            ),
        ],
        start_state=dict(
            exists=True,
            data_set_organization="Sequential"
        ),
        end_state=dict(
            exists=True,
            data_set_organization="Sequential"
        ),
        failed=False,
        changed=False,
        msg="",
    )
    assert aux_module.get_result() == expected_result
