# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import absolute_import, division, print_function
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import dataset_utils
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.response import _execution
from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.data_set_helper import (
    PYTHON_LANGUAGE_FEATURES_MESSAGE,
    ICETOOL_name,
    ICETOOL_stderr,
    ICETOOL_stdout,
    IDCAMS_delete_run_name,
    IDCAMS_delete_vsam,
    IEFBR14_create_stderr,
    LISTDS_data_set_doesnt_exist,
    LISTDS_data_set,
    LISTDS_run_name,
    set_module_args
)
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

NAMEA = "TEST.REGIONS.DFHDMPA"
NAMEB = "TEST.REGIONS.DFHDMPB"

default_arg_parms = {
    "space_primary": 20,
    "space_type": "M",
    "region_data_sets": {
        "dfhdmpa": {
            "dsn": NAMEA
        },
        "dfhdmpb": {
            "dsn": NAMEB
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


@pytest.mark.skipif(
    sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE
)
def test_create_an_intial_transaction_dump():
    transaction_dump_module = initialise_module()

    dataset_utils.ikjeft01 = MagicMock(
        side_effect=[
            (8, LISTDS_data_set_doesnt_exist(NAMEA), ""),
            (0, LISTDS_data_set(NAMEA, "PS"), ""),
        ]
    )
    dataset_utils._execute_iefbr14 = MagicMock(
        return_value=MVSCmdResponse(
            rc=0, stdout="", stderr=IEFBR14_create_stderr(NAMEA, "DFHDMPA")
        )
    )

    transaction_dump_module.main()
    expected_result = dict(
        executions=[
            _execution(
                name=LISTDS_run_name(1),
                rc=8,
                stdout=LISTDS_data_set_doesnt_exist(NAMEA),
                stderr="",
            ),
            _execution(
                name="IEFBR14 - dfhdmpa - Run 1",
                rc=0,
                stdout="",
                stderr=IEFBR14_create_stderr(NAMEA, "DFHDMPA")
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
        failed=False
    )
    assert transaction_dump_module.get_result() == expected_result


@pytest.mark.skipif(
    sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE
)
def test_delete_an_existing_transaction_dump():
    transaction_dump_module = initialise_module(state="absent")

    dataset_utils.idcams = MagicMock(
        return_value=(0, IDCAMS_delete_vsam(NAMEA), "")
    )
    dataset_utils.ikjeft01 = MagicMock(
        side_effect=[
            (0, LISTDS_data_set(NAMEA, "PS"), ""),
            (8, LISTDS_data_set_doesnt_exist(NAMEA), ""),
        ]
    )

    transaction_dump_module.main()
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
                stdout=IDCAMS_delete_vsam(NAMEA),
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
        failed=False
    )
    assert transaction_dump_module.get_result() == expected_result


@pytest.mark.skipif(
    sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE
)
def test_remove_non_existent_transaction_dump():
    transaction_dump_module = initialise_module(state="absent")

    dataset_utils.ikjeft01 = MagicMock(
        return_value=(8, LISTDS_data_set_doesnt_exist(NAMEA), "")
    )

    transaction_dump_module.main()
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
        failed=False
    )
    assert transaction_dump_module.get_result() == expected_result


@pytest.mark.skipif(
    sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE
)
def test_create_an_intial_destination_b_transaction_dump():
    transaction_dump_module = initialise_module(destination="B")

    dataset_utils.ikjeft01 = MagicMock(
        side_effect=[
            (8, LISTDS_data_set_doesnt_exist(NAMEB), ""),
            (0, LISTDS_data_set(NAMEB, "PS"), ""),
        ]
    )
    dataset_utils._execute_iefbr14 = MagicMock(
        return_value=MVSCmdResponse(
            rc=0, stdout="", stderr=IEFBR14_create_stderr(NAMEB, "DFHDMPB")
        )
    )

    transaction_dump_module.main()
    expected_result = dict(
        executions=[
            _execution(
                name=LISTDS_run_name(1),
                rc=8,
                stdout=LISTDS_data_set_doesnt_exist(NAMEB),
                stderr="",
            ),
            _execution(
                name="IEFBR14 - dfhdmpb - Run 1",
                rc=0,
                stdout="",
                stderr=IEFBR14_create_stderr(NAMEB, "DFHDMPB")),
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
        failed=False
    )
    assert transaction_dump_module.get_result() == expected_result


@pytest.mark.skipif(
    sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE
)
def test_warm_on_non_existent():
    transaction_dump_module = initialise_module(state="warm")

    dataset_utils.ikjeft01 = MagicMock(
        return_value=(8, LISTDS_data_set_doesnt_exist(NAMEA), "")
    )

    transaction_dump_module.main()
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
        changed=False
    )
    assert transaction_dump_module.get_result() == expected_result


@pytest.mark.skipif(
    sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE
)
def test_warm_on_empty():
    transaction_dump_module = initialise_module(state="warm")

    dataset_utils.ikjeft01 = MagicMock(
        return_value=(0, LISTDS_data_set(NAMEA, "PS"), "")
    )
    icetool._execute_icetool = MagicMock(
        return_value=(
            MVSCmdResponse(
                rc=0,
                stdout=ICETOOL_stdout(0),
                stderr=ICETOOL_stderr()
            )
        )
    )

    transaction_dump_module.main()
    expected_result = dict(
        executions=[
            _execution(
                name=LISTDS_run_name(1),
                rc=0,
                stdout=LISTDS_data_set(NAMEA, "PS"),
                stderr="",
            ),
            _execution(
                name=ICETOOL_name(1),
                rc=0,
                stdout=ICETOOL_stdout(0),
                stderr=ICETOOL_stderr()
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
        failed=True,
        changed=False
    )
    assert transaction_dump_module.get_result() == expected_result


@pytest.mark.skipif(
    sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE
)
def test_warm_success():
    transaction_dump_module = initialise_module(state="warm")

    dataset_utils.ikjeft01 = MagicMock(
        return_value=(0, LISTDS_data_set(NAMEA, "PS"), "")
    )
    icetool._execute_icetool = MagicMock(
        return_value=(
            MVSCmdResponse(
                rc=0,
                stdout=ICETOOL_stdout(52),
                stderr=ICETOOL_stderr()
            )
        )
    )

    transaction_dump_module.main()
    expected_result = dict(
        executions=[
            _execution(
                name=LISTDS_run_name(1),
                rc=0,
                stdout=LISTDS_data_set(NAMEA, "PS"),
                stderr="",
            ),
            _execution(
                name=ICETOOL_name(1),
                rc=0,
                stdout=ICETOOL_stdout(52),
                stderr=ICETOOL_stderr()
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
        changed=False
    )
    assert transaction_dump_module.get_result() == expected_result
