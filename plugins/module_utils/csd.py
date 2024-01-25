# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.dd_statement import StdinDefinition, DatasetDefinition, DDStatement, StdoutDefinition
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.zos_mvs_raw import MVSCmd, MVSCmdResponse
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.response import _execution
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.data_set import _dataset_constants as ds_constants


def _get_csdup_dds(catalog):  # type: (dict) -> dict
    return [
        DDStatement('steplib', DatasetDefinition(catalog["sdfhload"], disposition="SHR")),
        DDStatement(
            'dfhcsd',
            DatasetDefinition(
                dataset_name=catalog["name"],
                disposition="SHR")),
        DDStatement('sysprint', StdoutDefinition()),
        DDStatement('sysudump', StdoutDefinition()),
        DDStatement('sysin', StdinDefinition(content=_get_csdupcmd())),
    ]


def _run_dfhcsdup(starting_catalog):  # type: (dict) -> [_execution]
    executions = []
    dfhcsdup_response = _execute_dfhcsdup(starting_catalog)

    executions.append(_execution(
        name="DFHCSDUP - Initialise CSD",
        rc=dfhcsdup_response.rc,
        stdout=dfhcsdup_response.stdout,
        stderr=dfhcsdup_response.stderr))

    if dfhcsdup_response.rc != 0:
        raise Exception(
            "DFHCSDUP failed with RC {0}".format(
                dfhcsdup_response.rc
            ), executions
        )
    return executions


def _execute_dfhcsdup(starting_catalog):  # type: (dict) -> MVSCmdResponse
    return MVSCmd.execute(
        pgm="DFHCSDUP",
        dds=_get_csdup_dds(catalog=starting_catalog),
        verbose=True,
        debug=False)


def _get_csdupcmd():  # type () -> dict
    cmd = [
        "INITIALIZE"
    ]
    return cmd


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
