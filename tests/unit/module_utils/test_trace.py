# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function
import pytest
import sys
from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.data_set_helper import PYTHON_LANGUAGE_FEATURES_MESSAGE
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.dd_statement import DatasetDefinition
__metaclass__ = type
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.trace import _build_seq_data_set_definition_trace


@pytest.mark.skipif(sys.version_info.major < 3,
                    reason=PYTHON_LANGUAGE_FEATURES_MESSAGE)
def test_trace_definition_megabytes():
    data_set = dict(
        name="ANSI.M.DFHAUXT",
        state="initial",
        exists=False,
        vsam=False,
        unit="M",
        primary=20,
        secondary=1
    )

    definition = _build_seq_data_set_definition_trace(data_set)
    test_definition = DatasetDefinition(
        dataset_name="ANSI.M.DFHAUXT",
        block_size=4096,
        record_length=4096,
        record_format="FB",
        disposition="NEW",
        normal_disposition="CATALOG",
        conditional_disposition="DELETE",
        primary=20,
        primary_unit="M",
        type="SEQ"
    )

    assert definition.__dict__ == test_definition.__dict__
