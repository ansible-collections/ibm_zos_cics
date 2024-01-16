# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.dd_statement import StdoutDefinition, DatasetDefinition, DDStatement
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.zos_mvs_raw import MVSCmd
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.dataset_utils import _data_set
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.response import _execution
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.data_set import _dataset_constants as ds_constants


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


def _run_dfhccutl(starting_catalog):  # type: (_data_set) -> [_execution]
    executions = []
    dfhccutl_response = _execute_dfhccutl(starting_catalog)

    executions.append(_execution(
        name="DFHCCUTL - Initialise CSD",
        rc=dfhccutl_response.rc,
        stdout=dfhccutl_response.stdout,
        stderr=dfhccutl_response.stderr))

    if dfhccutl_response.rc != 0:
        raise Exception(
            "DFHCCUTL failed with RC {0}".format(
                dfhccutl_response.rc
            ), executions
        )
    return executions


def _execute_dfhccutl(starting_catalog):
    return MVSCmd.execute(
        pgm="DFHCCUTL",
        dds=_get_ccmutl_dds(catalog=starting_catalog),
        verbose=True,
        debug=False)


def _get_idcams_cmd_csd(dataset):  # type: (dict) -> dict
    defaults = {
        "CLUSTER": {
            "RECORDSIZE": "{0} {1}".format(_csd_constants["RECORD_COUNT_DEFAULT"], _csd_constants["RECORD_SIZE_DEFAULT"]),
            "INDEXED": None,
            "KEYS": "{0} {1}".format(_csd_constants["KEY_LENGTH"], _csd_constants["KEY_OFFSET"]),
            "FREESPACE": "{0} {1}".format(_csd_constants["CI_PERCENT"], _csd_constants["CA_PERCENT"]),
            "SHAREOPTIONS": "{0}".format(_csd_constants["SHARE_CROSSREGION"]),
            "REUSE": None
        },
        "DATA": {
            "CONTROLINTERVALSIZE": "{0}".format(_csd_constants["CONTROL_INTERVAL_SIZE_DEFAULT"])
        },
        "INDEX": {
            None
        }
    }
    defaults.update(dataset)
    return defaults


_csd_constants = {
    "PRIMARY_SPACE_VALUE_DEFAULT": 4,
    "SECONDARY_SPACE_VALUE_DEFAULT": 1,
    "SPACE_UNIT_DEFAULT": "M",
    "TARGET_STATE_OPTIONS": [
        ds_constants["TARGET_STATE_ABSENT"],
        ds_constants["TARGET_STATE_INITIAL"],
        ds_constants["TARGET_STATE_WARM"]
    ],
    "RECORD_COUNT_DEFAULT": 200,
    "RECORD_SIZE_DEFAULT": 2000,
    "CONTROL_INTERVAL_SIZE_DEFAULT": 8192,
    "KEY_LENGTH": 22,
    "KEY_OFFSET": 0,
    "CI_PERCENT": 10,
    "CA_PERCENT": 10,
    "SHARE_CROSSREGION": 2
}
