# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
import re

from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.mvs_cmd import idcams, ikjeft01
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.response import _execution
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.zos_mvs_raw import MVSCmd
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.dd_statement import DDStatement

MVS_CMD_RETRY_ATTEMPTS = 10


def _run_idcams(cmd: str, name: str, location: str, delete: bool = False) -> list[_execution]:
    executions = []

    for x in range(MVS_CMD_RETRY_ATTEMPTS):
        rc, stdout, stderr = idcams(cmd=cmd, authorized=True)
        executions.append(
            _execution(
                name="IDCAMS - {0} - Run {1}".format(
                    name,
                    x + 1),
                rc=rc,
                stdout=stdout,
                stderr=stderr))
        if location.upper() in stdout.upper():
            break

    if location.upper() not in stdout.upper():
        raise Exception("IDCAMS Command output not recognised", executions)

    if delete:
        pattern = r"^.+ENTRY\(A|C|D|I\){0}DELETED+$".format(location.upper())
        if rc == 8 and "ENTRY{0}NOTFOUND".format(
            location.upper()) in stdout.upper().replace(
            " ",
            "").replace(
            "\n",
                ""):
            return executions
        elif rc != 0 or not bool(re.search(pattern, stdout.upper().replace(
            " ",
            "").replace(
            "\n",
                ""))):
            raise Exception("RC {0} when deleting data set".format(rc), executions)
    else:
        if rc == 12 and "NOTDEFINEDBECAUSEDUPLICATENAMEEXISTSINCATALOG" in stdout.upper(
        ).replace(" ", "").replace("\n", ""):
            return executions
        if rc != 0:
            raise Exception("RC {0} when creating data set".format(rc), executions)

    return executions


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


def _build_idcams_define_parms(dataset, parm):  # type: (Dict, str) -> str
    parmsStr = ""
    if isinstance(dataset[parm], dict):
        for key, value in dataset[parm].items():
            if value is not None:
                parmsStr += " -\n    {0}({1})".format(key, value)
            elif key is not None:
                parmsStr += " -\n    {0}".format(key)
    return parmsStr


def _run_listds(location):
    cmd = " LISTDS '{0}'".format(location)
    executions = []

    for x in range(MVS_CMD_RETRY_ATTEMPTS):
        rc, stdout, stderr = ikjeft01(cmd=cmd, authorized=True)
        executions.append(
            _execution(
                name="IKJEFT01 - Get Data Set Status - Run {0}".format(
                    x + 1),
                rc=rc,
                stdout=stdout,
                stderr=stderr))
        if location.upper() in stdout.upper():
            break

    if location.upper() not in stdout.upper():
        raise Exception("LISTDS Command output not recognised", executions)

    # DS Name in output, good output

    if rc == 8 and "NOT IN CATALOG" in stdout:
        return executions, dict(exists=False, data_set_organization="NONE")

    # Exists

    if rc != 0:
        raise Exception("RC {0} running LISTDS Command".format(rc), executions)

    # Exists, RC 0

    matches = re.findall(r"\s+(PS|PO|IS|DA|VSAM|\?\?)\s+", stdout.upper())
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

    return executions, dict(exists=True, data_set_organization=data_set_organization)


def _run_iefbr14(ddname, definition):  # type (str, DatasetDefinition) -> List[Dict]

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
            raise Exception(
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
