# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function

__metaclass__ = type
from typing import Dict


def _get_idcams_cmd_temp(dataset):  # type: (Dict) -> Dict
    defaults = {
        "CLUSTER": {
            "RECORDSIZE": "{0} {1}".format(
                _auxiliary_temp_constants["RECORD_COUNT_DEFAULT"],
                _auxiliary_temp_constants["RECORD_SIZE_DEFAULT"],
            ),
            "NONINDEXED": None,
            "CONTROLINTERVALSIZE": "{0}".format(
                _auxiliary_temp_constants["CONTROL_INTERVAL_SIZE_DEFAULT"]
            ),
            "SHAREOPTIONS": "{0} {1}".format(
                _auxiliary_temp_constants["SHARE_CROSSREGION"],
                _auxiliary_temp_constants["SHARE_CROSSSYSTEM"],
            ),
        },
        "DATA": {"UNIQUE": None},
    }
    defaults.update(dataset)
    return defaults


_auxiliary_temp_constants = {
    "PRIMARY_SPACE_VALUE_DEFAULT": 200,
    "SECONDARY_SPACE_VALUE_DEFAULT": 10,
    "SPACE_UNIT_DEFAULT": "REC",
    "TARGET_STATE_OPTIONS": ["absent", "initial"],
    "RECORD_COUNT_DEFAULT": 4089,
    "RECORD_SIZE_DEFAULT": 4089,
    "CONTROL_INTERVAL_SIZE_DEFAULT": 4096,
    "SHARE_CROSSREGION": 2,
    "SHARE_CROSSSYSTEM": 3,
}
