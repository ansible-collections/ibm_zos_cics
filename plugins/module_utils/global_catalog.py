# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.zos_mvs_raw import MVSCmd, MVSCmdResponse
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.dd_statement import StdoutDefinition, DatasetDefinition, DDStatement, InputDefinition
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.response import _execution
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.dataset_utils import MVS_CMD_RETRY_ATTEMPTS


def _get_value_from_line(line):  # type: (str) -> str
    val = None
    if len(line) == 1:
        val = line[0].split(":")[1]
    return val


def _get_filtered_list(elements, target):  # type: (list(str),str) -> list
    return list(filter(lambda x: target in x, elements))


def _get_rmutl_dds(
        location,
        sdfhload,
        cmd):  # type: (str, str, str) -> list[DDStatement]
    return [
        DDStatement('steplib', DatasetDefinition(sdfhload)),
        DDStatement('dfhgcd', DatasetDefinition(location)),
        DDStatement('sysin', InputDefinition(content=cmd)),
        DDStatement('sysprint', StdoutDefinition()),
    ]


def _get_reason_code(filtered):  # type: (list(str)) -> str
    if len(filtered) == 0:
        raise Exception(
            "DFHRMUTL failed with RC 16 but no reason code was found")

    elements2 = list(filtered[0].split(','))
    filtered2 = list(filter(lambda x: "REASON:X" in x, elements2))
    if len(filtered2) == 0:
        raise Exception(
            "DFHRMUTL failed with RC 16 but no reason code was found")

    elements3 = [element.replace("0", "")
                 for element in filtered2[0].split("'")]
    return elements3[1]


def _get_catalog_records(stdout):  # type: (str) -> str
    elements = ['{0}'.format(element.replace(" ", "").upper())
                for element in stdout.split("\n")]

    autostart_filtered = _get_filtered_list(
        elements, "AUTO-STARTOVERRIDE:")
    nextstart_filtered = _get_filtered_list(elements, "NEXTSTARTTYPE:")

    autostart_override = _get_value_from_line(
        autostart_filtered)
    nextstart = _get_value_from_line(nextstart_filtered)

    return {
        "autostart_override": autostart_override,
        "next_start": nextstart
    }


def _run_dfhrmutl(location: str, sdfhload: str, cmd: str = "") -> list():

    executions = []

    for x in range(MVS_CMD_RETRY_ATTEMPTS):
        dfhrmutl_response = _execute_dfhrmutl(location, sdfhload, cmd)
        executions.append(
            _execution(
                name="DFHRMUTL - {0} - Run {1}".format(
                    "Get current catalog" if cmd == "" else "Updating autostart override",
                    x + 1),
                rc=dfhrmutl_response.rc,
                stdout=dfhrmutl_response.stdout,
                stderr=dfhrmutl_response.stderr))

        if dfhrmutl_response.rc == 0:
            break
        if dfhrmutl_response.rc == 16:
            elements = ["{0}".format(element.replace(" ", "").upper())
                        for element in dfhrmutl_response.stdout.split("\n")]
            filtered = list(filter(lambda x: "REASON:X" in x, elements))

            reason_code = _get_reason_code(filtered)
            if reason_code != "A8":
                raise Exception(
                    "DFHRMUTL failed with RC 16 - {0}".format(filtered[0]), executions)
        else:
            raise Exception(
                "DFHRMUTL failed with RC {0}".format(
                    dfhrmutl_response.rc), executions)

    if cmd != "":
        return executions

    return executions, _get_catalog_records(dfhrmutl_response.stdout)


def _execute_dfhrmutl(location: str, sdfhload: str, cmd: str = "") -> MVSCmdResponse:
    return MVSCmd.execute(
        pgm="DFHRMUTL",
        dds=_get_rmutl_dds(location=location, sdfhload=sdfhload, cmd=cmd),
        verbose=True,
        debug=False)


def _get_idcams_cmd_gcd(dataset: dict) -> dict:
    defaults = {
        "CLUSTER": {
            "RECORDSIZE": "{0} {1}".format(RECORD_COUNT_DEFAULT, RECORD_SIZE_DEFAULT),
            "INDEXED": None,
            "KEYS": "{0} {1}".format(KEY_LENGTH, KEY_OFFSET),
            "FREESPACE": "{0} {1}".format(CI_PERCENT, CA_PERCENT),
            "SHAREOPTIONS": "{0}".format(SHARE_CROSSREGION),
            "REUSE": None
        },
        "DATA": {
            "CONTROLINTERVALSIZE": "{0}".format(CONTROL_INTERVAL_SIZE_DEFAULT)
        },
        "INDEX": {
            None
        }
    }
    defaults.update(dataset)
    return defaults


AUTO_START_WARM = "AUTOASIS"
AUTO_START_COLD = "AUTOCOLD"
AUTO_START_INIT = "AUTOINIT"
NEXT_START_EMERGENCY = "EMERGENCY"
NEXT_START_WARM = "WARM"
NEXT_START_COLD = "COLD"
NEXT_START_UNKNOWN = "UNKNOWN"
SPACE_PRIMARY_DEFAULT = 5
SPACE_SECONDARY_DEFAULT = 1
SPACE_TYPE_DEFAULT = "M"
STATE_OPTIONS = ["absent", "initial", "cold", "warm"]
RECORD_COUNT_DEFAULT = 4089
RECORD_SIZE_DEFAULT = 32760
CONTROL_INTERVAL_SIZE_DEFAULT = 32768
KEY_LENGTH = 52
KEY_OFFSET = 0
CI_PERCENT = 10
CA_PERCENT = 10
SHARE_CROSSREGION = 2
