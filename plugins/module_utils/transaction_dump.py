# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import (absolute_import, division, print_function)

from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.dd_statement import DatasetDefinition
__metaclass__ = type


def _build_seq_data_set_definition_transaction_dump(data_set):  # type (Dict) -> DatasetDefinition
    definition = DatasetDefinition(
        dataset_name=data_set["name"],
        primary=data_set["size"]["primary"],
        primary_unit=data_set["size"]["unit"],
        block_size=_transaction_dump_data_set_constants["BLOCK_SIZE_DEFAULT"],
        record_length=_transaction_dump_data_set_constants["RECORD_LENGTH_DEFAULT"],
        record_format=_transaction_dump_data_set_constants["RECORD_FORMAT"],
        disposition=_transaction_dump_data_set_constants["DISPOSITION"],
        normal_disposition=_transaction_dump_data_set_constants["NORMAL_DISP"],
        conditional_disposition=_transaction_dump_data_set_constants["CONDITION_DISP"],
        type=_transaction_dump_data_set_constants["TYPE"]
    )
    return definition


_transaction_dump_data_set_constants = {
    "TARGET_STATE_OPTIONS": ["absent", "initial", "warm"],
    "PRIMARY_SPACE_VALUE_DEFAULT": 20,
    "PRIMARY_SPACE_UNIT_DEFAULT": "M",
    "SECONDARY_SPACE_VALUE_DEFAULT": 4,
    "BLOCK_SIZE_DEFAULT": 4096,
    "RECORD_LENGTH_DEFAULT": 4092,
    "RECORD_FORMAT": "VB",
    "TYPE": "SEQ",
    "DISPOSITION": "NEW",
    "NORMAL_DISP": "CATALOG",
    "CONDITION_DISP": "DELETE",
    "TRANSACTION_DUMP_DESTINATION_OPTIONS": ["A", "B"],
    "TRANSACTION_DUMP_DESTINATION_DEFAULT_VALUE": "A"
}
