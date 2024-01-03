# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.mvs_cmd import idcams, ikjeft01
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.response import _execution, _state


def _dataset_size(unit, primary, secondary):  # type: (str,int,int) -> dict
    return {
        "unit": unit,
        "primary": primary,
        "secondary": secondary
    }


def _run_idcams(cmd, name, location, delete=False):  # type: (str, str, str, bool) -> list
    executions = []

    for x in range(10):
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
        if rc == 8 and "ENTRY{0}NOTFOUND".format(
            location.upper()) in stdout.upper().replace(
            " ",
            "").replace(
            "\n",
                ""):
            return executions
        if rc != 0 or "ENTRY(C){0}DELETED".format(
            location.upper()) not in stdout.upper().replace(
            " ",
            "").replace(
            "\n",
                ""):
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
        _get_dataset_size_unit(dataset["size"]["unit"]),
        dataset["size"]["primary"],
        dataset["size"]["secondary"],
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


def _run_listds(location):  # type: (str) -> [list, _state]
    cmd = " LISTDS '{0}'".format(location)
    executions = []

    for x in range(10):
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
        return executions, _state(exists=False, vsam=False)

    # Exists

    if rc != 0:
        raise Exception("RC {0} running LISTDS Command".format(rc), executions)

    # Exists, RC 0

    elements = ["{0}".format(element.replace(" ", "").upper())
                for element in stdout.split("\n")]
    filtered = list(filter(lambda x: "VSAM" in x, elements))

    if len(filtered) == 0:
        return executions, _state(exists=True, vsam=False)
    else:
        return executions, _state(exists=True, vsam=True)


def _data_set(size, name, state, exists, vsam, **kwargs):  # type: (_dataset_size, str, str, bool, bool, dict) -> dict
    data_set = {
        "size": size,
        "name": name,
        "state": state,
        "exists": exists,
        "vsam": vsam,
    }
    data_set.update(kwargs)
    return data_set
