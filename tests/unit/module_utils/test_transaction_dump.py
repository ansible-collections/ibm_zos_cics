# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
import pytest
import sys
from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.data_set_helper import PYTHON_LANGUAGE_FEATURES_MESSAGE
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.data_set import MEGABYTES
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.dd_statement import DatasetDefinition
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.transaction_dump import _build_seq_data_set_definition_transaction_dump
from ansible_collections.ibm.ibm_zos_cics.plugins.modules.transaction_dump import SPACE_PRIMARY_DEFAULT, SPACE_SECONDARY_DEFAULT


@pytest.mark.skipif(sys.version_info.major < 3,
                    reason=PYTHON_LANGUAGE_FEATURES_MESSAGE)
def test_transaction_dump_definition_megabytes():
    data_set = dict(
        name="ANSI.M.DFHDMPA",
        state="initial",
        exists=False,
        data_set_organization="NONE",
        unit=MEGABYTES,
        primary=SPACE_PRIMARY_DEFAULT,
        secondary=SPACE_SECONDARY_DEFAULT
    )

    definition = _build_seq_data_set_definition_transaction_dump(data_set)
    test_definition = DatasetDefinition(
        dataset_name="ANSI.M.DFHDMPA",
        block_size=4096,
        record_length=4092,
        record_format="VB",
        disposition="NEW",
        normal_disposition="CATALOG",
        conditional_disposition="DELETE",
        primary=20,
        primary_unit="M",
        type="SEQ"
    )

    assert definition.__dict__ == test_definition.__dict__
