# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
import traceback

ZOS_CICS_IMP_ERR = None
try:
    from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.dataset_utils import (
        _build_idcams_define_cmd)
except ImportError:
    ZOS_CICS_IMP_ERR = traceback.format_exc()


def _get_idcams_cmd_lrq(dataset):
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
    return _build_idcams_define_cmd(defaults)


def _local_request_queue(size, name, state, exists, vsam):
    return {
        'size': size,
        'name': name,
        'state': state,
        'exists': exists,
        'vsam': vsam,
    }
