# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023,2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function
import pytest
import sys
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils._data_set import MEGABYTES
from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.data_set_helper import PYTHON_LANGUAGE_FEATURES_MESSAGE
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.dd_statement import DatasetDefinition
__metaclass__ = type
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils._aux_trace import _build_seq_data_set_definition_aux_trace
from ansible_collections.ibm.ibm_zos_cics.plugins.modules.aux_trace import SPACE_PRIMARY_DEFAULT, SPACE_SECONDARY_DEFAULT


@pytest.mark.skipif(sys.version_info.major < 3,
                    reason=PYTHON_LANGUAGE_FEATURES_MESSAGE)
def test_aux_trace_definition_megabytes():
    data_set = dict(
        name="ANSI.M.DFHAUXT",
        state="initial",
        exists=False,
        data_set_organization="NONE",
        unit=MEGABYTES,
        primary=SPACE_PRIMARY_DEFAULT,
        secondary=SPACE_SECONDARY_DEFAULT
    )

    definition = _build_seq_data_set_definition_aux_trace(data_set)
    test_definition = DatasetDefinition(
        dataset_name="ANSI.M.DFHAUXT",
        block_size=4096,
        record_length=4096,
        record_format="FB",
        disposition="NEW",
        normal_disposition="CATALOG",
        conditional_disposition="DELETE",
        primary=SPACE_PRIMARY_DEFAULT,
        secondary=SPACE_SECONDARY_DEFAULT,
        primary_unit="m",
        secondary_unit="m",
        type="SEQ"
    )

    assert definition.__dict__ == test_definition.__dict__


@pytest.mark.skipif(sys.version_info.major < 3,
                    reason=PYTHON_LANGUAGE_FEATURES_MESSAGE)
def test_aux_trace_definition_volumes():
    data_set = dict(
        name="ANSI.M.DFHAUXT",
        state="initial",
        exists=False,
        data_set_organization="NONE",
        unit=MEGABYTES,
        primary=SPACE_PRIMARY_DEFAULT,
        secondary=SPACE_SECONDARY_DEFAULT,
        volumes=["vserv1"]
    )

    definition = _build_seq_data_set_definition_aux_trace(data_set)
    test_definition = DatasetDefinition(
        dataset_name="ANSI.M.DFHAUXT",
        block_size=4096,
        record_length=4096,
        record_format="FB",
        disposition="NEW",
        normal_disposition="CATALOG",
        conditional_disposition="DELETE",
        primary=SPACE_PRIMARY_DEFAULT,
        secondary=SPACE_SECONDARY_DEFAULT,
        primary_unit="m",
        secondary_unit="m",
        type="SEQ",
        volumes=["vserv1"]
    )

    assert definition.__dict__ == test_definition.__dict__
