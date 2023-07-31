# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
import traceback

ZOS_CORE_IMP_ERR = None
try:
    from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.dd_statement import StdoutDefinition, DatasetDefinition, DDStatement
    from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.zos_mvs_raw import MVSCmd
except ImportError:
    ZOS_CORE_IMP_ERR = traceback.format_exc()

ZOS_CICS_IMP_ERR = None
try:
    from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.response import (
        _execution)
    from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.dataset_utils import (
        _build_idcams_define_cmd)
    from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.dataset_utils import _dataset_constants as ds_constants
except ImportError:
    ZOS_CICS_IMP_ERR = traceback.format_exc()


def _get_ccmutl_dds(catalog):
    return [
        DDStatement('steplib', DatasetDefinition(catalog["sdfhload"])),
        DDStatement('sysprint', StdoutDefinition()),
        DDStatement('sysudump', StdoutDefinition()),
        DDStatement(
            'dfhlcd',
            DatasetDefinition(
                dataset_name=catalog["name"],
                disposition="SHR")),
    ]


def _run_dfhccutl(starting_catalog):
    executions = []
    dfhccutl_response = MVSCmd.execute(
        pgm="DFHCCUTL",
        dds=_get_ccmutl_dds(catalog=starting_catalog),
        verbose=True,
        debug=False)

    if dfhccutl_response.rc != 0:
        raise Exception(
            "DFHCCUTL failed with RC {0}".format(
                dfhccutl_response.rc
            )
        )
    executions.append(_execution(
        name="DFHCCUTL - Initialise Local Catalog",
        rc=dfhccutl_response.rc,
        stdout=dfhccutl_response.stdout,
        stderr=dfhccutl_response.stderr))

    return executions


def _get_idcams_cmd_lcd(dataset):
    defaults = {
        "CLUSTER": {
            "RECORDSIZE": "70 2041",
            "INDEXED": None,
            "KEYS": "52 0",
            "FREESPACE": "10 10",
            "SHAREOPTIONS": "2",
            "REUSE": None
        },
        "DATA": {
            "CONTROLINTERVALSIZE": "2048"
        },
        "INDEX": {
            None
        }
    }
    defaults.update(dataset)
    return _build_idcams_define_cmd(defaults)


_local_catalog_constants = {
    "PRIMARY_SPACE_VALUE_DEFAULT": 200,
    "SECONDARY_SPACE_VALUE_DEFAULT": 5,
    "SPACE_UNIT_DEFAULT": "REC",
    "TARGET_STATE_OPTIONS": [
        ds_constants["TARGET_STATE_ABSENT"],
        ds_constants["TARGET_STATE_INITIAL"],
        ds_constants["TARGET_STATE_WARM"]
    ],
    "RECORD_COUNT_DEFAULT": 70,
    "RECORD_SIZE_DEFAULT": 2041,
    "CONTROL_INTERVAL_SIZE_DEFAULT": 2048
}


def _local_catalog(size, name, sdfhload, state, exists, vsam):
    return {
        'size': size,
        'name': name,
        'sdfhload': sdfhload,
        'state': state,
        'exists': exists,
        'vsam': vsam,
    }
