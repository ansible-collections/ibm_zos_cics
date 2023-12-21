# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import dataset_utils
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.response import _response, _state


class DataSet(object):
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

    def init_argument_spec(self):  # type: () -> dict
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

    def _get_arg_defs(self):  # type: () -> dict
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

    def _get_data_set_object(self, size, result):  # type: (dataset_utils._dataset_size, dict) -> dataset_utils._data_set
        return dataset_utils._data_set(
            size=size,
            name=result.get(_dataset_constants["DATASET_LOCATION_ALIAS"]).upper(),
            state=result.get(_dataset_constants["TARGET_STATE_ALIAS"]),
            exists=False,
            vsam=False)

    def _get_data_set_size(self, result):
        return dataset_utils._dataset_size(
            unit=result.get(_dataset_constants["PRIMARY_SPACE_UNIT_ALIAS"]),
            primary=result.get(_dataset_constants["PRIMARY_SPACE_VALUE_ALIAS"]),
            secondary=_dataset_constants["SECONDARY_SPACE_VALUE_DEFAULT"])

    def validate_parameters(self):  # type: () -> None
        arg_defs = self._get_arg_defs()

        result = dataset_utils.BetterArgParser(arg_defs).parse_args({
            _dataset_constants["PRIMARY_SPACE_VALUE_ALIAS"]:
                self._module.params.get(_dataset_constants["PRIMARY_SPACE_VALUE_ALIAS"]),
            _dataset_constants["PRIMARY_SPACE_UNIT_ALIAS"]:
                self._module.params.get(_dataset_constants["PRIMARY_SPACE_UNIT_ALIAS"]),
            _dataset_constants["DATASET_LOCATION_ALIAS"]:
                self._module.params.get(_dataset_constants["DATASET_LOCATION_ALIAS"]),
            _dataset_constants["TARGET_STATE_ALIAS"]:
                self._module.params.get(_dataset_constants["TARGET_STATE_ALIAS"])
        })

        size = self._get_data_set_size(result)
        self.data_set = self._get_data_set_object(size, result)

    def create_data_set(self):
        create_cmd = dataset_utils._build_idcams_define_cmd({})

    def build_vsam_data_set(self, create_cmd, message):  # type: (str, str) -> None
        idcams_executions = dataset_utils._run_idcams(
            cmd=create_cmd,
            name=message,
            location=self.data_set["name"],
            delete=False)
        self.result["executions"] = self.result["executions"] + idcams_executions

        self.result["changed"] = True

    def delete_data_set(self, message):  # type: (str) -> None
        delete_cmd = '''
        DELETE {0}
        '''.format(self.data_set["name"])

        idcams_executions = dataset_utils._run_idcams(
            cmd=delete_cmd,
            name=message,
            location=self.data_set["name"],
            delete=True)
        self.result["executions"] = self.result["executions"] + idcams_executions
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

    def get_data_set_state(self, data_set):  # type: (dict) -> dict
        try:
            listds_executions, ds_status = dataset_utils._run_listds(data_set["name"])

            data_set["exists"] = ds_status["exists"]
            data_set["vsam"] = ds_status["vsam"]

            self.result["executions"] = self.result["executions"] + listds_executions
        except Exception as e:
            self.result["executions"] = self.result["executions"] + e.args[1]
            self._fail(e.args[0])

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


_dataset_constants = {
    "DATASET_LOCATION_ALIAS": "location",
    "SDFHLOAD_ALIAS": "sdfhload",
    "TARGET_STATE_ALIAS": "state",
    "PRIMARY_SPACE_VALUE_ALIAS": "space_primary",
    "PRIMARY_SPACE_UNIT_ALIAS": "space_type",
    "SECONDARY_SPACE_VALUE_DEFAULT": 0,
    "SPACE_UNIT_OPTIONS": ["K", "M", "REC", "CYL", "TRK"],
    "TARGET_STATE_ABSENT": "absent",
    "TARGET_STATE_INITIAL": "initial",
    "TARGET_STATE_WARM": "warm",
    "TARGET_STATE_COLD": "cold",
    "CICS_DATA_SETS_ALIAS": "cics_data_sets",
    "REGION_DATA_SETS_ALIAS": "region_data_sets",
}
