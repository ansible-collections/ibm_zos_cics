# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
import traceback
from typing import List

ZOS_CORE_IMP_ERR = None

try:
    from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.zos_mvs_raw import MVSCmd
    from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.dd_statement import StdoutDefinition, DatasetDefinition, DDStatement, InputDefinition

except ImportError:
    ZOS_CORE_IMP_ERR = traceback.format_exc()

ZOS_CICS_IMP_ERR = None
try:
    from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.response import (
        _execution)
except ImportError:
    ZOS_CICS_IMP_ERR = traceback.format_exc()


def _get_value_from_line(line):
    val = None
    if len(line) == 1:
        val = line[0].split(":")[1]
    return val


def _get_filtered_list(elements, target):
    return list(filter(lambda x: target in x, elements))


def _get_rmutl_dds(
        location,
        sdfhload,
        cmd):  # type: (str, str, str) -> List[DDStatement]
    return [
        DDStatement('steplib', DatasetDefinition(sdfhload)),
        DDStatement('dfhgcd', DatasetDefinition(location)),
        DDStatement('sysin', InputDefinition(content=cmd)),
        DDStatement('sysprint', StdoutDefinition()),
    ]


def _get_reason_code(filtered):
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


def _get_catalog_records(stdout):
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


def _run_dfhrmutl(location, sdfhload, cmd=""):

    executions = []

    for x in range(10):
        dfhrmutl_response = MVSCmd.execute(
            pgm="DFHRMUTL",
            dds=_get_rmutl_dds(location=location, sdfhload=sdfhload, cmd=cmd),
            verbose=True,
            debug=False)
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
                    "DFHRMUTL failed with RC 16 - {0}".format(filtered[0]))
        else:
            raise Exception(
                "DFHRMUTL failed with RC {0}".format(
                    dfhrmutl_response.rc))

    if cmd != "":
        return executions

    return executions, _get_catalog_records(dfhrmutl_response.stdout)


def _global_catalog(
        size,
        name,
        sdfhload,
        state,
        autostart_override,
        nextstart,
        exists,
        vsam):
    return {
        'size': size,
        'name': name,
        'sdfhload': sdfhload,
        'state': state,
        'autostart_override': autostart_override,
        'nextstart': nextstart,
        'exists': exists,
        'vsam': vsam,
    }
