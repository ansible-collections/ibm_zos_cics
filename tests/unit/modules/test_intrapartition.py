# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import absolute_import, division, print_function
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import dataset_utils
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.response import (
    _execution,
    _response,
    _state,
)
from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.data_set_helper import (
    set_data_set,
    set_module_args,
)
from ansible_collections.ibm.ibm_zos_cics.plugins.modules import intrapartition
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
    "region_data_sets": {"dfhintra": {"dsn": "TEST.REGIONS.INTRA"}},
    "cics_data_sets": {"sdfhload": "TEST.CICS.INSTALL.SDFHLOAD"},
    "state": "initial",
}


def initialise_module(**kwargs):
    initial_args = default_arg_parms
    initial_args.update(kwargs)
    set_module_args(initial_args)
    intra_module = intrapartition.AnsibleIntrapartitionModule()
    return intra_module


@pytest.mark.skipif(
    sys.version_info.major < 3, reason="Requires python 3 language features"
)
def test_create_an_intial_intrapartition_ds():
    intra_module = initialise_module()

    dataset_utils.idcams = MagicMock(return_value=(0, "TEST.REGIONS.INTRA", "stderr"))
    dataset_utils.ikjeft01 = MagicMock(
        side_effect=[
            (8, "TEST.REGIONS.INTRA NOT IN CATALOG", "stderr"),
            (0, "TEST.REGIONS.INTRA VSAM", "stderr"),
        ]
    )
    intrapartition.AnsibleIntrapartitionModule._exit = MagicMock(return_value=None)

    intra_module.main()
    expected_result = _response(
        executions=[
            _execution(
                name="IKJEFT01 - Get Data Set Status - Run 1",
                rc=8,
                stdout="TEST.REGIONS.INTRA NOT IN CATALOG",
                stderr="stderr",
            ),
            _execution(
                name="IDCAMS - Create intrapartition data set - Run 1",
                rc=0,
                stdout="TEST.REGIONS.INTRA",
                stderr="stderr",
            ),
            _execution(
                name="IKJEFT01 - Get Data Set Status - Run 1",
                rc=0,
                stdout="TEST.REGIONS.INTRA VSAM",
                stderr="stderr",
            ),
        ],
        start_state=_state(exists=False, vsam=False),
        end_state=_state(exists=True, vsam=True),
    )
    expected_result.update({"changed": True})
    assert intra_module.result == expected_result


@pytest.mark.skipif(
    sys.version_info.major < 3, reason="Requires python 3 language features"
)
def test_delete_an_existing_intrapartition_ds():
    intra_module = initialise_module(state="absent")

    dataset_utils.idcams = MagicMock(
        return_value=(0, "ENTRY (C) TEST.REGIONS.INTRA DELETED\n", "stderr")
    )
    dataset_utils.ikjeft01 = MagicMock(
        side_effect=[
            (0, "TEST.REGIONS.INTRA VSAM", "stderr"),
            (8, "TEST.REGIONS.INTRA NOT IN CATALOG", "stderr"),
        ]
    )
    intrapartition.AnsibleIntrapartitionModule._exit = MagicMock(return_value=None)

    intra_module.main()
    expected_result = _response(
        executions=[
            _execution(
                name="IKJEFT01 - Get Data Set Status - Run 1",
                rc=0,
                stdout="TEST.REGIONS.INTRA VSAM",
                stderr="stderr",
            ),
            _execution(
                name="IDCAMS - Removing intrapartition data set - Run 1",
                rc=0,
                stdout="ENTRY (C) TEST.REGIONS.INTRA DELETED\n",
                stderr="stderr",
            ),
            _execution(
                name="IKJEFT01 - Get Data Set Status - Run 1",
                rc=8,
                stdout="TEST.REGIONS.INTRA NOT IN CATALOG",
                stderr="stderr",
            ),
        ],
        start_state=_state(exists=True, vsam=True),
        end_state=_state(exists=False, vsam=False),
    )
    expected_result.update({"changed": True})
    assert intra_module.result == expected_result


@pytest.mark.skipif(
    sys.version_info.major < 3, reason="Requires python 3 language features"
)
def test_do_nothing_to_an_existing_intra():
    intra_module = initialise_module()
    data_set = set_data_set(exists=True, name="TEST.REGIONS.INTRA", vsam=True)
    intra_module.data_set = data_set

    dataset_utils.ikjeft01 = MagicMock(
        side_effect=[
            (0, "TEST.REGIONS.INTRA VSAM", "stderr"),
            (0, "TEST.REGIONS.INTRA VSAM", "stderr"),
        ]
    )
    intrapartition.AnsibleIntrapartitionModule._exit = MagicMock(return_value=None)

    intra_module.main()
    expected_result = _response(
        executions=[
            _execution(
                name="IKJEFT01 - Get Data Set Status - Run 1",
                rc=0,
                stdout="TEST.REGIONS.INTRA VSAM",
                stderr="stderr",
            ),
            _execution(
                name="IKJEFT01 - Get Data Set Status - Run 1",
                rc=0,
                stdout="TEST.REGIONS.INTRA VSAM",
                stderr="stderr",
            ),
        ],
        start_state=_state(exists=True, vsam=True),
        end_state=_state(exists=True, vsam=True),
    )
    assert intra_module.result == expected_result


@pytest.mark.skipif(
    sys.version_info.major < 3, reason="Requires python 3 language features"
)
def test_remove_non_existent_intra():
    intra_module = initialise_module(state="absent")

    dataset_utils.idcams = MagicMock(
        return_value=(8, "ENTRY TEST.REGIONS.INTRA NOTFOUND", "stderr")
    )
    dataset_utils.ikjeft01 = MagicMock(
        return_value=(8, "TEST.REGIONS.INTRA NOT IN CATALOG", "stderr")
    )
    intrapartition.AnsibleIntrapartitionModule._exit = MagicMock(return_value=None)

    intra_module.main()
    expected_result = _response(
        executions=[
            _execution(
                name="IKJEFT01 - Get Data Set Status - Run 1",
                rc=8,
                stdout="TEST.REGIONS.INTRA NOT IN CATALOG",
                stderr="stderr",
            ),
            _execution(
                name="IDCAMS - Removing intrapartition data set - Run 1",
                rc=8,
                stdout="ENTRY TEST.REGIONS.INTRA NOTFOUND",
                stderr="stderr",
            ),
            _execution(
                name="IKJEFT01 - Get Data Set Status - Run 1",
                rc=8,
                stdout="TEST.REGIONS.INTRA NOT IN CATALOG",
                stderr="stderr",
            ),
        ],
        start_state=_state(exists=False, vsam=False),
        end_state=_state(exists=False, vsam=False),
    )
    expected_result.update({"changed": True})
    assert intra_module.result == expected_result
