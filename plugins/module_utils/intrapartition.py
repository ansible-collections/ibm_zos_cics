# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


def _get_idcams_cmd_intra(data_set):   # type: (dict) -> dict
    defaults = {
        "CLUSTER": {
            "RECORDSIZE": "{0} {1}".format(
                RECORD_COUNT_DEFAULT,
                RECORD_SIZE_DEFAULT,
            ),
            "NONINDEXED": None,
            "CONTROLINTERVALSIZE": "{0}".format(
                CONTROL_INTERVAL_SIZE_DEFAULT
            ),
        },
        "DATA": {None},
    }
    defaults.update(data_set)
    return defaults


SPACE_PRIMARY_DEFAULT = 100
SPACE_SECONDARY_DEFAULT = 10
SPACE_TYPE_DEFAULT = "REC"
STATE_OPTIONS = ["absent", "initial", "warm"]
RECORD_COUNT_DEFAULT = 1529
RECORD_SIZE_DEFAULT = 1529
CONTROL_INTERVAL_SIZE_DEFAULT = 1536
