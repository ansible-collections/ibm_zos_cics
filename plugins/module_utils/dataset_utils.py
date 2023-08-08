# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.module_utils.basic import AnsibleModule
import traceback
from typing import Dict, List

ZOS_CORE_IMP_ERR = None

try:
    from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.mvs_cmd import idcams, ikjeft01
    from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.better_arg_parser import BetterArgParser
except ImportError:
    ZOS_CORE_IMP_ERR = traceback.format_exc()

ZOS_CICS_IMP_ERR = None
try:
    from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.response import (
        _execution, _response, _state)
except ImportError:
    ZOS_CICS_IMP_ERR = traceback.format_exc()


def _dataset_size(unit, primary, secondary):  # type: (str,int,int) -> Dict
    return {
        "unit": unit,
        "primary": primary,
        "secondary": secondary
    }


def _run_idcams(cmd, name, location, delete=False):  # type: (str, str, str, bool) -> List
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
        "M": "MEGABYTES",
        "K": "KILOBYTES",
        "CYL": "CYLINDERS",
        "REC": "RECORDS",
        "TRK": "TRACKS"
    }.get(unit_symbol, "MEGABYTES")


def _build_idcams_define_cmd(dataset):  # type: (Dict) -> str
    return '''
    DEFINE CLUSTER ({0}) -
    DATA ({1}) -
    INDEX({2})
    '''.format(_build_idcams_define_cluster_parms(dataset),
               _build_idcams_define_data_parms(dataset),
               _build_idcams_define_index_parms(dataset))


def _build_idcams_define_cluster_parms(dataset):  # type: (Dict) -> str

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


def _build_idcams_define_data_parms(dataset):  # type: (Dict) -> str
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


def _build_idcams_define_index_parms(dataset):  # type: (Dict) -> str
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


def _run_listds(location):  # type: (str) -> [List, _state]
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
        return executions, _state(exists=False, vsam=False)

    # Exists

    if rc != 0:
        raise Exception("RC {0} running LISTDS Command".format(rc))

    # Exists, RC 0

    elements = ["{0}".format(element.replace(" ", "").upper())
                for element in stdout.split("\n")]
    filtered = list(filter(lambda x: "VSAM" in x, elements))

    if len(filtered) == 0:
        return executions, _state(exists=True, vsam=False)
    else:
        return executions, _state(exists=True, vsam=True)


_dataset_constants = {
    "DATASET_LOCATION_ALIAS": "location",
    "SDFHLOAD_ALIAS": "sdfhload",
    "TARGET_STATE_ALIAS": "state",
    "PRIMARY_SPACE_VALUE_ALIAS": "space_primary",
    "PRIMARY_SPACE_UNIT_ALIAS": "space_type",
    "SPACE_UNIT_OPTIONS": ["K", "M", "REC", "CYL", "TRK"],
    "TARGET_STATE_ABSENT": "absent",
    "TARGET_STATE_INITIAL": "initial",
    "TARGET_STATE_WARM": "warm",
    "TARGET_STATE_COLD": "cold",
    "CICS_DATA_SETS_ALIAS": "cics_data_sets",
    "REGION_DATA_SETS_ALIAS": "region_data_sets",
}


def _data_set(size, name, state, exists, vsam, **kwargs):  # type: (_dataset_size, str, str, bool, bool, Dict) -> Dict
    data_set = {
        "size": size,
        "name": name,
        "state": state,
        "exists": exists,
        "vsam": vsam,
    }
    data_set.update(kwargs)
    return data_set


class AnsibleDataSetModule(object):
    def __init__(self):
        self._module = AnsibleModule(
            argument_spec=self.init_argument_spec(),
        )
        self.result = _response(executions=[], start_state=_state(exists=False), end_state=_state(exists=False))
        self.validate_parameters()

    def _fail(self, msg):  # type: (str) -> None
        self.result["failed"] = True
        self._module.fail_json(msg=msg, **self.result)

    def _exit(self):  # type: () -> None
        self._module.exit_json(**self.result)

    def init_argument_spec(self):  # type: () -> Dict
        return {
            _dataset_constants["PRIMARY_SPACE_VALUE_ALIAS"]: {
                "required": False,
                "type": "int",
            },
            _dataset_constants["PRIMARY_SPACE_UNIT_ALIAS"]: {
                "required": False,
                "type": "str",
                "choices": _dataset_constants["SPACE_UNIT_OPTIONS"],
            },
            _dataset_constants["TARGET_STATE_ALIAS"]: {
                "required": True,
                "type": "str",
            }
        }

    def _get_arg_defs(self):  # type: () -> Dict
        return {
            _dataset_constants["PRIMARY_SPACE_VALUE_ALIAS"]: {
                "arg_type": "int",
            },
            _dataset_constants["PRIMARY_SPACE_UNIT_ALIAS"]: {
                "arg_type": "str",
                "choices": _dataset_constants["SPACE_UNIT_OPTIONS"],
            },
            _dataset_constants["TARGET_STATE_ALIAS"]: {
                "arg_type": "str",
                "required": True,
            },
        }

    def _get_data_set_object(self, size, result):  # type: (_dataset_size, Dict) -> _data_set
        return _data_set(
            size=size,
            name=result.get(_dataset_constants["DATASET_LOCATION_ALIAS"]).upper(),
            state=result.get(_dataset_constants["TARGET_STATE_ALIAS"]),
            exists=False,
            vsam=False)

    def validate_parameters(self):  # type: () -> None
        arg_defs = self._get_arg_defs()

        result = BetterArgParser(arg_defs).parse_args({
            _dataset_constants["PRIMARY_SPACE_VALUE_ALIAS"]: self._module.params.get(_dataset_constants["PRIMARY_SPACE_VALUE_ALIAS"]),
            _dataset_constants["PRIMARY_SPACE_UNIT_ALIAS"]: self._module.params.get(_dataset_constants["PRIMARY_SPACE_UNIT_ALIAS"]),
            _dataset_constants["DATASET_LOCATION_ALIAS"]: self._module.params.get(_dataset_constants["DATASET_LOCATION_ALIAS"]),
            _dataset_constants["TARGET_STATE_ALIAS"]: self._module.params.get(_dataset_constants["TARGET_STATE_ALIAS"])
        })

        size = _dataset_size(
            unit=result.get(_dataset_constants["PRIMARY_SPACE_UNIT_ALIAS"]),
            primary=result.get(_dataset_constants["PRIMARY_SPACE_VALUE_ALIAS"]),
            secondary=1)

        self.data_set = self._get_data_set_object(size, result)

    def create_data_set(self):  # type: () -> None
        self.result["changed"] = True

    def delete_data_set(self):  # type: () -> None
        self.result["changed"] = True

    def init_data_set(self):  # type: () -> None
        if self.data_set["exists"]:
            self.result["end_state"] = _state(exists=self.data_set["exists"], vsam=self.data_set["vsam"])
            self._exit()

        if not self.data_set["exists"]:
            self.create_data_set()

    def warm_data_set(self):  # type: () -> None
        if not self.data_set["exists"]:
            self._fail(
                "Data set {0} does not exist.".format(
                    self.data_set["name"]))

    def invalid_target_state(self):  # type: () -> None
        self._fail("{0} is not a valid target state.".format(
            self.data_set["state"]))

    def get_target_method(self, target):  # type: (str) -> [str | invalid_target_state]
        return {
            _dataset_constants["TARGET_STATE_ABSENT"]: self.delete_data_set,
            _dataset_constants["TARGET_STATE_INITIAL"]: self.init_data_set,
            _dataset_constants["TARGET_STATE_WARM"]: self.warm_data_set,
        }.get(target, self.invalid_target_state)

    def get_data_set_state(self, data_set):  # type: (Dict) -> Dict
        listds_executions, ds_status = _run_listds(data_set["name"])

        data_set["exists"] = ds_status["exists"]
        data_set["vsam"] = ds_status["vsam"]

        self.result["executions"] = self.result["executions"] + listds_executions

        return data_set

    def main(self):
        self.data_set = self.get_data_set_state(self.data_set)

        self.result["start_state"] = _state(exists=self.data_set["exists"], vsam=self.data_set["vsam"])

        # Change below to account for non vsams
        if self.data_set["exists"] and not self.data_set["vsam"]:
            self._fail(
                "Data set {0} does not appear to be a KSDS.".format(
                    self.data_set["name"]))

        self.get_target_method(self.data_set["state"])()

        self.end_state = self.get_data_set_state(self.data_set)

        self.result["end_state"] = _state(exists=self.end_state["exists"], vsam=self.end_state["vsam"])

        self._exit()
