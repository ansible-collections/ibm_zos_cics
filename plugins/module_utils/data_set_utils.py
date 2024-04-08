# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
import re

from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.response import _execution, MVSExecutionException
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.zos_mvs_raw import MVSCmd
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.dd_statement import DDStatement, StdoutDefinition, DatasetDefinition, StdinDefinition

MVS_CMD_RETRY_ATTEMPTS = 10


def _run_idcams(cmd, name, location, delete=False):  # type: (str, str, str, bool) -> list[dict[str, str| int]]
    executions = []

    for x in range(MVS_CMD_RETRY_ATTEMPTS):
        idcams_response = _execute_idcams(cmd=cmd)
        executions.append(
            _execution(
                name="IDCAMS - {0} - Run {1}".format(
                    name,
                    x + 1),
                rc=idcams_response.rc,
                stdout=idcams_response.stdout,
                stderr=idcams_response.stderr))
        if location.upper() in idcams_response.stdout.upper():
            break

    if location.upper() not in idcams_response.stdout.upper():
        raise MVSExecutionException("IDCAMS Command output not recognised", executions)

    if delete:
        pattern = r"^.+ENTRY\(A|C|D|I\){0}DELETED+$".format(location.upper())
        if idcams_response.rc == 8 and "ENTRY{0}NOTFOUND".format(
            location.upper()) in idcams_response.stdout.upper().replace(
            " ",
            "").replace(
            "\n",
                ""):
            return executions
        elif idcams_response.rc != 0 or not bool(re.search(pattern, idcams_response.stdout.upper().replace(
            " ",
            "").replace(
            "\n",
                ""))):
            raise MVSExecutionException("RC {0} when deleting data set".format(idcams_response.rc), executions)
    else:
        if idcams_response.rc == 12 and "NOTDEFINEDBECAUSEDUPLICATENAMEEXISTSINCATALOG" in idcams_response.stdout.upper(
        ).replace(" ", "").replace("\n", ""):
            return executions
        if idcams_response.rc != 0:
            raise MVSExecutionException("RC {0} when creating data set".format(idcams_response.rc), executions)

    return executions


def _get_idcams_dds(cmd):
    return [
        DDStatement('sysin', StdinDefinition(content=cmd)),
        DDStatement('sysprint', StdoutDefinition()),
    ]


def _execute_idcams(cmd):
    return MVSCmd.execute_authorized(
        pgm="IDCAMS",
        dds=_get_idcams_dds(cmd),
        verbose=True,
        debug=False
    )


def _get_listds_dds(cmd):
    return [
        DDStatement('systsin', StdinDefinition(content=cmd)),
        DDStatement('systsprt', StdoutDefinition()),
    ]


def _execute_listds(cmd):
    return MVSCmd.execute_authorized(
        pgm="IKJEFT01",
        dds=_get_listds_dds(cmd),
        verbose=True,
        debug=False
    )


def _get_dataset_size_unit(unit_symbol):  # type: (str) -> str
    return {
        "M": "MEGABYTES",
        "K": "KILOBYTES",
        "CYL": "CYLINDERS",
        "REC": "RECORDS",
        "TRK": "TRACKS"
    }.get(unit_symbol, "MEGABYTES")


def _build_idcams_define_cmd(dataset):  # type: (dict) -> str
    defineStr = "\n    DEFINE{0}{1}{2}\n    ".format(
        _build_idcams_define_cluster_parms(dataset),
        _build_idcams_define_data_parms(dataset),
        _build_idcams_define_index_parms(dataset))
    return defineStr


def _build_idcams_define_cluster_parms(dataset):  # type: (dict) -> str
    clusterStr = " CLUSTER (NAME({0}) -\n    {1}({2} {3}){4})".format(
        dataset["name"],
        _get_dataset_size_unit(dataset["unit"]),
        dataset["primary"],
        dataset["secondary"],
        _build_idcams_define_parms(dataset, "CLUSTER"))
    return clusterStr


def _build_idcams_define_data_parms(dataset):  # type: (dict) -> str
    dataStr = " -\n    DATA (NAME({0}.DATA){1})".format(
        dataset["name"],
        _build_idcams_define_parms(dataset, "DATA"))
    return dataStr


def _build_idcams_define_index_parms(dataset):  # type: (dict) -> str
    if dataset.get("INDEX", None):
        indexStr = " -\n    INDEX (NAME({0}.INDEX){1})".format(
            dataset["name"],
            _build_idcams_define_parms(dataset, "INDEX"))
    else:
        indexStr = ""
    return indexStr


def _build_idcams_define_parms(dataset, parm):  # type: (dict, str) -> str
    parmsStr = ""
    if isinstance(dataset[parm], dict):
        for key, value in dataset[parm].items():
            if value is not None:
                parmsStr += " -\n    {0}({1})".format(key, value)
            elif key is not None:
                parmsStr += " -\n    {0}".format(key)
    return parmsStr


def _run_listds(location):  # type: (str) -> tuple[list[_execution], bool, str]
    cmd = " LISTDS '{0}'".format(location)
    executions = []

    for x in range(MVS_CMD_RETRY_ATTEMPTS):
        listds_response = _execute_listds(cmd=cmd)
        executions.append(
            _execution(
                name="IKJEFT01 - Get Data Set Status - Run {0}".format(
                    x + 1),
                rc=listds_response.rc,
                stdout=listds_response.stdout,
                stderr=listds_response.stderr))
        if location.upper() in listds_response.stdout.upper():
            break

    if location.upper() not in listds_response.stdout.upper():
        raise MVSExecutionException("LISTDS Command output not recognised", executions)

    # DS Name in output, good output

    if listds_response.rc == 8 and "NOT IN CATALOG" in listds_response.stdout:
        return executions, False, "NONE"

    # Exists

    if listds_response.rc != 0:
        raise MVSExecutionException("RC {0} running LISTDS Command".format(listds_response.rc), executions)

    # Exists, RC 0

    matches = re.findall(r"\s+(PS|PO|IS|DA|VSAM|\?\?)\s+", listds_response.stdout.upper())
    if (len(matches) != 0):
        if (matches[0] == "PS"):
            data_set_organization = "Sequential"
        elif (matches[0] == "PO"):
            data_set_organization = "Partitioned"
        elif (matches[0] == "IS"):
            data_set_organization = "Indexed Sequential"
        elif (matches[0] == "DA"):
            data_set_organization = "Direct Access"
        elif (matches[0] == "VSAM"):
            data_set_organization = "VSAM"
        elif (matches[0] == "??"):
            data_set_organization = "Other"
    else:
        data_set_organization = "Unspecified"

    return executions, True, data_set_organization


def _run_iefbr14(ddname, definition):  # type: (str, DatasetDefinition) -> list[dict[str, str| int]]

    executions = []

    for x in range(MVS_CMD_RETRY_ATTEMPTS):
        iefbr14_response = _execute_iefbr14(ddname, definition)
        executions.append(
            _execution(
                name="IEFBR14 - {0} - Run {1}".format(
                    ddname,
                    x + 1),
                rc=iefbr14_response.rc,
                stdout=iefbr14_response.stdout,
                stderr=iefbr14_response.stderr))

        if iefbr14_response.rc == 0:
            break
        else:
            raise MVSExecutionException(
                "RC {0} when creating sequential data set".format(
                    iefbr14_response.rc), executions)

    return executions


def _get_iefbr14_dds(ddname, definition):  # type: (str, DatasetDefinition) -> list[DDStatement]
    return [DDStatement(ddname, definition)]


def _execute_iefbr14(ddname, definition):
    return MVSCmd.execute(
        pgm="IEFBR14",
        dds=_get_iefbr14_dds(ddname, definition),
        verbose=True,
        debug=False
    )
