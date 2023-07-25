# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
import traceback

ZOS_CORE_IMP_ERR = None

try:
    from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.mvs_cmd import idcams, ikjeft01
except ImportError:
    ZOS_CORE_IMP_ERR = traceback.format_exc()

ZOS_CICS_IMP_ERR = None
try:
    from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.response import (
        _execution)
except ImportError:
    ZOS_CICS_IMP_ERR = traceback.format_exc()


def _dataset_size(unit, primary, secondary, record_count,
                  record_size, control_interval_size):
    return {
        'unit': unit,
        'primary': primary,
        'secondary': secondary,
        'record_count': record_count,
        'record_size': record_size,
        'control_interval_size': control_interval_size,
    }


def _run_idcams(cmd, name, location, delete=False):
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
        raise Exception("IDCAMS Command output not recognised")

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
            raise Exception("RC {0} when deleting data set".format(rc))
    else:
        if rc == 12 and "NOTDEFINEDBECAUSEDUPLICATENAMEEXISTSINCATALOG" in stdout.upper(
        ).replace(" ", "").replace("\n", ""):
            return executions
        if rc != 0:
            raise Exception("RC {0} when creating data set".format(rc))

    return executions


def _get_dataset_size_unit(unit_symbol):  # type: (str) -> str
    return {
        'M': "MEGABYTES",
        'K': "KILOBYTES",
        'CYL': "CYLINDERS",
        'REC': "RECORDS",
        'TRK': "TRACKS"
    }.get(unit_symbol, "MEGABYTES")


def _get_idcams_create_cmd(dataset):
    return '''
    DEFINE CLUSTER -
        (NAME({0}) -
        INDEXED                      -
        {1}({2} {3})             -
        SHR(2)              -
        FREESPACE(10 10)              -
        RECORDSIZE({4} {5})       -
        REUSE)              -
        DATA                           -
        (NAME({0}.DATA)  -
        CONTROLINTERVALSIZE({6})    -
        KEYS(52 0))  -
        INDEX                          -
        (NAME({0}.INDEX))
    '''.format(dataset["name"],
               _get_dataset_size_unit(dataset["size"]["unit"]),
               dataset["size"]["primary"],
               dataset["size"]["secondary"],
               dataset["size"]["record_count"],
               dataset["size"]["record_size"],
               dataset["size"]["control_interval_size"])


def _get_idcams_create_cmd2(dataset):
    return '''
    DEFINE CLUSTER -
        (NAME({0}) -
        LOG(UNDO)-
        INDEXED                      -
        {1}({2} {3})             -
        SHR(2)              -
        FREESPACE(0 10)              -
        RECORDSIZE({4} {5})       -
        )              -
        DATA                           -
        (NAME({0}.DATA)  -
        CONTROLINTERVALSIZE({6})    -
        KEYS(40 0))  -
        INDEX                          -
        (NAME({0}.INDEX))
    '''.format(dataset["name"],
               _get_dataset_size_unit(dataset["size"]["unit"]),
               dataset["size"]["primary"],
               dataset["size"]["secondary"],
               dataset["size"]["record_count"],
               dataset["size"]["record_size"],
               dataset["size"]["control_interval_size"])


def _run_listds(location):
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
        raise Exception("LISTDS Command output not recognised")

    # DS Name in output, good output

    if rc == 8 and "NOT IN CATALOG" in stdout:
        return executions, {
            "exists": False,
            "vsam": False,
        }

    # Exists

    if rc != 0:
        raise Exception("RC {0} running LISTDS Command".format(rc))

    # Exists, RC 0

    elements = ["{0}".format(element.replace(" ", "").upper())
                for element in stdout.split("\n")]
    filtered = list(filter(lambda x: "VSAM" in x, elements))

    if len(filtered) == 0:
        return executions, {
            "exists": True,
            "vsam": False,
        }
    else:
        return executions, {
            "exists": True,
            "vsam": True,
        }
