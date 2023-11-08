# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from typing import Dict


def _get_idcams_cmd_lrq(dataset):  # type: (Dict) -> Dict
    defaults = {
        "CLUSTER": {
            "RECORDSIZE": "2232 2400",
            "INDEXED": None,
            "KEYS": "40 0",
            "FREESPACE": "0 10",
            "SHAREOPTIONS": "2 3",
            "REUSE": None,
            "LOG": "UNDO"
        },
        "DATA": {
            "CONTROLINTERVALSIZE": "2560"
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
    "CONTROL_INTERVAL_SIZE_DEFAULT": 2560
}
