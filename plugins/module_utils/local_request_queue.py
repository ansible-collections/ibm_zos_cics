# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from typing import Dict


def _get_idcams_cmd_lrq(dataset):  # type: (Dict) -> Dict
    defaults = {
        "CLUSTER": {
            "RECORDSIZE": "{0} {1}".format(_local_request_queue_constants["RECORD_COUNT_DEFAULT"], _local_request_queue_constants["RECORD_SIZE_DEFAULT"]),
            "INDEXED": None,
            "KEYS": "{0} {1}".format(_local_request_queue_constants["KEY_LENGTH"], _local_request_queue_constants["KEY_OFFSET"]),
            "FREESPACE": "{0} {1}".format(_local_request_queue_constants["CI_PERCENT"], _local_request_queue_constants["CA_PERCENT"]),
            "SHAREOPTIONS": "{0} {1}".format(_local_request_queue_constants["SHARE_CROSSREGION"], _local_request_queue_constants["SHARE_CROSSSYSTEM"]),
            "REUSE": None,
            "LOG": "{0}".format(_local_request_queue_constants["LOG_OPTION"])
        },
        "DATA": {
            "CONTROLINTERVALSIZE": "{0}".format(_local_request_queue_constants["CONTROL_INTERVAL_SIZE_DEFAULT"])
        },
        "INDEX": {
            None
        }
    }
    defaults.update(dataset)
    return defaults


_local_request_queue_constants = {
    "PRIMARY_SPACE_VALUE_DEFAULT": 4,
    "SECONDARY_SPACE_VALUE_DEFAULT": 1,
    "SPACE_UNIT_DEFAULT": "M",
    "TARGET_STATE_OPTIONS": ["absent", "initial"],
    "RECORD_COUNT_DEFAULT": 2232,
    "RECORD_SIZE_DEFAULT": 2400,
    "CONTROL_INTERVAL_SIZE_DEFAULT": 2560,
    "KEY_LENGTH": 40,
    "KEY_OFFSET": 0,
    "CI_PERCENT": 0,
    "CA_PERCENT": 10,
    "SHARE_CROSSREGION": 2,
    "SHARE_CROSSSYSTEM": 3,
    "LOG_OPTION": "UNDO"
}
