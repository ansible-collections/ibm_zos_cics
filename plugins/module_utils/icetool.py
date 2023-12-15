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


def _get_icetool_dds(location):  # type: (str) -> List[DDStatement]
    return [
        DDStatement('sysprint', StdoutDefinition()),
        DDStatement('dd1', DatasetDefinition(dataset_name=location, disposition="SHR")),
        DDStatement('toolmsg', StdoutDefinition()),
        DDStatement('dfsmsg', StdoutDefinition()),
        DDStatement('showdef', StdoutDefinition()),
        DDStatement('toolin', InputDefinition(content="COUNT FROM(DD1)")),
    ]


def _get_reason_code(filtered):
    if len(filtered) == 0:
        raise Exception(
            "ICETOOL failed with RC 16 but no reason code was found")

    elements2 = list(filtered[0].split(','))
    filtered2 = list(filter(lambda x: "REASON:X" in x, elements2))
    if len(filtered2) == 0:
        raise Exception(
            "ICETOOL failed with RC 16 but no reason code was found")

    elements3 = [element.replace("0", "")
                 for element in filtered2[0].split("'")]
    return elements3[1]


def _get_record_count(stdout):
    record_count = -1
    elements = ['{0}'.format(element.replace(" ", "").upper())
                for element in stdout.split("\n")]

    lines = list(filter(lambda x: "RECORDCOUNT:" in x, elements))
    if len(lines) > 0:
        record_count = int(lines[0].split(":")[1])

    return {"record_count": record_count}


def _run_icetool(location):
    executions = []

    for x in range(10):
        icetool_response = _execute_icetool(location)

        executions.append(
            _execution(
                name="ICETOOL - Get record count",
                rc=icetool_response.rc,
                stdout=icetool_response.stdout,
                stderr=icetool_response.stderr))

        if icetool_response.rc == 0:
            break
        if icetool_response.rc == 16:
            elements = ["{0}".format(element.replace(" ", "").upper())
                        for element in icetool_response.stdout.split("\n")]
            filtered = list(filter(lambda x: "REASON:X" in x, elements))

            reason_code = _get_reason_code(filtered)
            if reason_code != "A8":
                raise Exception(
                    "ICETOOL failed with RC 16 - {0}".format(filtered[0]))
        else:
            raise Exception(
                "ICETOOL failed with RC {0}".format(
                    icetool_response.rc))

    return executions, _get_record_count(icetool_response.stdout)


def _execute_icetool(location):
    return MVSCmd.execute(
        pgm="ICETOOL",
        dds=_get_icetool_dds(location=location),
        verbose=True,
        debug=False)
