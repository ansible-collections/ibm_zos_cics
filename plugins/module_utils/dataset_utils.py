# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.module_utils.basic import AnsibleModule
import traceback

ZOS_CORE_IMP_ERR = None

try:
    from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.mvs_cmd import idcams, ikjeft01
    from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.better_arg_parser import BetterArgParser
except ImportError:
    ZOS_CORE_IMP_ERR = traceback.format_exc()

ZOS_CICS_IMP_ERR = None
try:
    from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.response import (
        _execution)
except ImportError:
    ZOS_CICS_IMP_ERR = traceback.format_exc()


def _dataset_size(unit, primary, secondary):
    return {
        'unit': unit,
        'primary': primary,
        'secondary': secondary
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


def _build_idcams_define_cmd(dataset):
    return '''
    DEFINE CLUSTER ({0}) -
    DATA ({1}) -
    INDEX({2})
    '''.format(_build_idcams_define_cluster_parms(dataset),
               _build_idcams_define_data_parms(dataset),
               _build_idcams_define_index_parms(dataset))


def _build_idcams_define_cluster_parms(dataset):
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


def _build_idcams_define_data_parms(dataset):
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


def _build_idcams_define_index_parms(dataset):
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


def _data_set(size, name, state, exists, vsam):
    return {
        "size": size,
        "name": name,
        "state": state,
        "exists": exists,
        "vsam": vsam,
    }


class AnsibleDataSetModule(object):
    def __init__(self):
        self._module = AnsibleModule(
            argument_spec=self.init_argument_spec(),
        )
        self.result = {}
        self.result["changed"] = False
        self.result["failed"] = False
        self.result["executions"] = []
        self.executions = []
        self.validate_parameters()

    def _fail(self, msg):  # type: (str) -> None
        self.result["failed"] = True
        self.result["executions"] = self.executions
        self._module.fail_json(msg=msg, **self.result)

    def _exit(self):
        self.result["executions"] = self.executions
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
            _dataset_constants["DATASET_LOCATION_ALIAS"]: {
                "required": True,
                "type": "str",
            },
            _dataset_constants["TARGET_STATE_ALIAS"]: {
                "required": True,
                "type": "str",
            }
        }

    def _get_arg_defs(self):
        return {
            _dataset_constants["PRIMARY_SPACE_VALUE_ALIAS"]: {
                "arg_type": "int",
            },
            _dataset_constants["PRIMARY_SPACE_UNIT_ALIAS"]: {
                "arg_type": "str",
                "choices": _dataset_constants["SPACE_UNIT_OPTIONS"],
            },
            _dataset_constants["DATASET_LOCATION_ALIAS"]: {
                "arg_type": "data_set_base",
                "required": True,
            },
            _dataset_constants["TARGET_STATE_ALIAS"]: {
                "arg_type": "str",
                "required": True,
            },
        }

    def _get_data_set_object(self, size, result):
        return _data_set(
            size=size,
            name=result.get(_dataset_constants["DATASET_LOCATION_ALIAS"]).upper(),
            state=result.get(_dataset_constants["TARGET_STATE_ALIAS"]),
            exists=False,
            vsam=False)

    def validate_parameters(self):
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

        self.data_set_definition = self._get_data_set_object(size, result)

    def create_dataset(self):
        self.result["changed"] = True

    def delete_data_set(self):
        self.result["changed"] = True

    def init_data_set(self):
        if self.data_set_definition["exists"]:
            self.result["end_state"] = {
                "exists": self.data_set_definition["exists"],
                "vsam": self.data_set_definition["vsam"]
            }
            self._exit()

        if not self.data_set_definition["exists"]:
            self.create_dataset()

    def invalid_state(self):  # type: () -> None
        self._fail("{0} is not a valid target state.".format(
            self.data_set_definition["state"]))

    def get_target_method(self, target):
        return {
            _dataset_constants["TARGET_STATE_ABSENT"]: self.delete_data_set,
            _dataset_constants["TARGET_STATE_INITIAL"]: self.init_data_set
        }.get(target, self.invalid_state)

    def get_dataset_state(self, dataset):
        listds_executions, ds_status = _run_listds(dataset["name"])

        dataset["exists"] = ds_status["exists"]
        dataset["vsam"] = ds_status["vsam"]

        self.executions = self.executions + listds_executions

        return dataset

    def main(self):
        self.data_set_definition = self.get_dataset_state(self.data_set_definition)

        self.result["start_state"] = {
            "exists": self.data_set_definition["exists"],
            "vsam": self.data_set_definition["vsam"]
        }

        if self.data_set_definition["exists"] and not self.data_set_definition["vsam"]:
            self._fail(
                "Data set {0} does not appear to be a KSDS.".format(
                    self.data_set_definition["name"]))

        self.get_target_method(self.data_set_definition["state"])()

        self.end_state = self.get_dataset_state(self.data_set_definition)

        self.result["end_state"] = {
            "exists": self.end_state["exists"],
            "vsam": self.end_state["vsam"]
        }

        self._exit()
