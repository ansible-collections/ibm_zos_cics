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
    index_statement = (""" -
    INDEX({0})""".format(_build_idcams_define_index_parms(dataset))
                       if dataset.get("INDEX", None)
                       else ""
                       )

    return """
    DEFINE CLUSTER ({0}) -
    DATA ({1}){2}
    """.format(_build_idcams_define_cluster_parms(dataset),
               _build_idcams_define_data_parms(dataset),
               index_statement)


def _build_idcams_define_cluster_parms(dataset):  # type: (dict) -> str

    clusterStr = "NAME({0}) -\n    {1}({2} {3})".format(
        dataset["name"],
        _get_dataset_size_unit(
            dataset["size"]["unit"]),
        dataset["size"]["primary"],
        dataset["size"]["secondary"])
    if isinstance(dataset["CLUSTER"], dict):
        clusterStr += " -\n    "
        for key, value in dataset["CLUSTER"].items():
            if value is not None:
                clusterStr += "{0}({1})".format(key, value)
                if key != list(dataset["CLUSTER"].keys())[-1]:
                    clusterStr += " -\n    "
            elif key is not None:
                clusterStr += "{0}".format(key)
                if key != list(dataset["CLUSTER"].keys())[-1]:
                    clusterStr += " -\n    "

    return clusterStr


def _build_idcams_define_data_parms(dataset):  # type: (dict) -> str
    dataStr = "NAME({0}.DATA)".format(dataset["name"])
    if isinstance(dataset["DATA"], dict):
        dataStr += " -\n    "
        for key, value in dataset["DATA"].items():
            if value is not None:
                dataStr += "{0}({1})".format(key, value)
                if key != list(dataset["DATA"].keys())[-1]:
                    dataStr += " -\n    "
            elif key is not None:
                dataStr += "{0}".format(key)
                if key != list(dataset["DATA"].keys())[-1]:
                    dataStr += " -\n    "

    return dataStr


def _build_idcams_define_index_parms(dataset):  # type: (dict) -> str
    indexStr = "NAME({0}.INDEX)".format(dataset["name"])
    if isinstance(dataset["INDEX"], dict):
        indexStr += " -\n    "
        for key, value in dataset["INDEX"].items():
            if value is not None:
                indexStr += "{0}({1})".format(key, value)
                if key != list(dataset["INDEX"].keys())[-1]:
                    indexStr += " -\n    "
            elif key is not None:
                indexStr += "{0}".format(key)
                if key != list(dataset["INDEX"].keys())[-1]:
                    indexStr += " -\n    "

    return indexStr


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
