# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.dd_statement import StdinDefinition, DatasetDefinition, DDStatement, StdoutDefinition
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.zos_mvs_raw import MVSCmd, MVSCmdResponse
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.response import _execution


def _get_csdup_dds(data_set, cmd):  # type: (dict, str) -> list[DDStatement]
    return [
        DDStatement('steplib', DatasetDefinition(data_set["sdfhload"], disposition="SHR")),
        DDStatement(
            'dfhcsd',
            DatasetDefinition(
                dataset_name=data_set["name"],
                disposition="SHR")),
        DDStatement('sysprint', StdoutDefinition()),
        DDStatement('sysudump', StdoutDefinition()),
        DDStatement('sysin', StdinDefinition(content=cmd)),
    ]


def _run_dfhcsdup(data_set, cmd):  # type: (dict, str) -> list[_execution]
    executions = []
    dfhcsdup_response = _execute_dfhcsdup(data_set, cmd)

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


def _execute_dfhcsdup(data_set, cmd):  # type: (dict, str) -> MVSCmdResponse
    return MVSCmd.execute(
        pgm="DFHCSDUP",
        dds=_get_csdup_dds(data_set, cmd),
        verbose=True,
        debug=False)


def _get_csdup_initilize_cmd():  # type: () -> str
    return "INITIALIZE"


def _get_add_dfhtermc_to_group_cmd():  # type: () -> str
    return "ADD GROUP(DFHTERMC) LIST(DFHLIST1)"


def _get_idcams_cmd_csd(dataset):  # type: (dict) -> dict
    defaults = {
        "CLUSTER": {
            "RECORDSIZE": "{0} {1}".format(RECORD_COUNT_DEFAULT, RECORD_SIZE_DEFAULT),
            "INDEXED": None,
            "KEYS": "{0} {1}".format(KEY_LENGTH, KEY_OFFSET),
            "FREESPACE": "{0} {1}".format(CI_PERCENT, CA_PERCENT),
            "SHAREOPTIONS": str(SHARE_CROSSREGION),
            "REUSE": None
        },
        "DATA": {
            "CONTROLINTERVALSIZE": str(CONTROL_INTERVAL_SIZE_DEFAULT)
        },
        "INDEX": {
            None
        }
    }
    defaults.update(dataset)
    return defaults


RECORD_COUNT_DEFAULT = 200
RECORD_SIZE_DEFAULT = 2000
CONTROL_INTERVAL_SIZE_DEFAULT = 8192
KEY_LENGTH = 22
KEY_OFFSET = 0
CI_PERCENT = 10
CA_PERCENT = 10
SHARE_CROSSREGION = 2
