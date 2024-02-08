# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.dataset_utils import (
    _build_idcams_define_cmd,
    _run_idcams,
    _run_listds,
    _run_iefbr14
)
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.icetool import _run_icetool
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.better_arg_parser import BetterArgParser
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.dd_statement import DatasetDefinition

LOCATION = "location"
SDFHLOAD = "sdfhload"
STATE = "state"
SPACE_PRIMARY = "space_primary"
SPACE_TYPE = "space_type"
SECONDARY_SPACE_DEFAULT = 0
SPACE_OPTIONS = ["K", "M", "REC", "CYL", "TRK"]
ABSENT = "absent"
INITIAL = "initial"
WARM = "warm"
COLD = "cold"
CICS_DATA_SETS = "cics_data_sets"
REGION_DATA_SETS = "region_data_sets"
DESTINATION = "destination"


class DataSet():
    def __init__(self):
        self.name = ""
        self.target_state = ""
        self.exists = False
        self.data_set_organization = ""
        self.expected_data_set_organization = ""
        self.unit = ""
        self.primary = 0
        self.secondary = SECONDARY_SPACE_DEFAULT
        self.sdfhload = ""
        self.destination = ""

        self.changed = False
        self.failed = False
        self.start_state = dict(exists=False, data_set_organization=self.data_set_organization)
        self.end_state = dict(exists=False, data_set_organization=self.data_set_organization)
        self.executions = list()
        self.region_param = dict()

        self._module = AnsibleModule(
            argument_spec=self._get_arg_spec(),
        )
        self.validate_parameters()

    def get_result(self):  # type: () -> dict
        return {
            "changed": self.changed,
            "failed": self.failed,
            "executions": self.executions,
            "start_state": self.start_state,
            "end_state": self.end_state,
        }

    def get_data_set(self):  # type: () -> dict
        return {
            "name": self.name,
            "state": self.target_state,
            "exists": self.exists,
            "data_set_organization": self.data_set_organization,
            "unit": self.unit,
            "primary": self.primary,
            "secondary": self.secondary,
            "sdfhload": self.sdfhload,
        }

    def set_start_state(self):   # type: () -> None
        self.start_state = dict(
            exists=self.exists,
            data_set_organization=self.data_set_organization
        )

    def set_end_state(self):  # type: () -> None
        self.end_state = dict(
            exists=self.exists,
            data_set_organization=self.data_set_organization
        )

    def _fail(self, msg):  # type: (str) -> None
        self.failed = True
        self.set_end_state()
        self.result = self.get_result()
        self._module.fail_json(msg=msg, **self.result)

    def _exit(self):  # type: () -> None
        self.set_end_state()
        self.result = self.get_result()
        self._module.exit_json(**self.result)

    def _get_arg_spec(self):  # type: () -> dict
        return {
            SPACE_PRIMARY: {
                "type": "int",
            },
            SPACE_TYPE: {
                "type": "str",
                "choices": SPACE_OPTIONS,
            },
            STATE: {
                "type": "str",
                "required": True,
            },
            CICS_DATA_SETS: {
                "type": "dict",
                "required": False,
                "options": {
                    "template": {
                        "type": "str",
                        "required": False,
                    },
                    "sdfhload": {
                        "type": "str",
                        "required": False,
                    },
                },
            },
            REGION_DATA_SETS: {
                "type": "dict",
                "required": True,
                "options": {
                    "template": {
                        "type": "str",
                        "required": False,
                    }
                },
            }
        }

    def get_arg_defs(self):  # type: () -> dict
        defs = self._get_arg_spec()
        defs[CICS_DATA_SETS]["options"]["sdfhload"].update({
            "arg_type": "data_set_base"
        })
        defs[CICS_DATA_SETS]["options"]["sdfhload"].pop("type")
        return defs

    def validate_parameters(self):  # type: () -> None
        params = BetterArgParser(self.get_arg_defs()).parse_args(self._module.params)
        self.target_state = params.get(STATE)
        self.primary = params.get(SPACE_PRIMARY)
        self.region_param = params.get(REGION_DATA_SETS)

        # Optional parameters
        if params.get(SPACE_TYPE):
            self.unit = params.get(SPACE_TYPE)
        if params.get(CICS_DATA_SETS):
            self.sdfhload = params.get(CICS_DATA_SETS).get("sdfhload").upper()
        if params.get(DESTINATION):
            self.destination = params.get(DESTINATION)

    def create_data_set(self):  # type: () -> None
        create_cmd = _build_idcams_define_cmd({})

    def build_vsam_data_set(self, create_cmd):  # type: (str) -> None
        try:
            message = "Creating {0} data set".format(self.name)
            idcams_executions = _run_idcams(
                cmd=create_cmd,
                name=message,
                location=self.name,
                delete=False)
            self.executions.extend(idcams_executions)

            self.changed = True
        except Exception as e:
            self.executions.extend(e.args[1])
            self._fail(e.args[0])

    def build_seq_data_set(self, ddname, definition):  # type: (str, DatasetDefinition) -> None
        try:
            iefbr14_executions = _run_iefbr14(ddname, definition)
            self.executions.extend(iefbr14_executions)

            self.changed = True
        except Exception as e:
            self.executions.extend(e.args[1])
            self._fail(e.args[0])

    def delete_data_set(self):  # type: () -> None
        if self.exists:
            delete_cmd = '''
            DELETE {0}
            '''.format(self.name)

            try:
                idcams_executions = _run_idcams(
                    cmd=delete_cmd,
                    name=self.name,
                    location=self.name,
                    delete=True)
                self.executions.extend(idcams_executions)
                self.changed = True
            except Exception as e:
                self.executions.extend(e.args[1])
                self._fail(e.args[0])

    def init_data_set(self):   # type: () -> None
        if self.exists:
            icetool_executions, record_count = _run_icetool(self.name)
            self.executions.extend(icetool_executions)
            if record_count > 0:
                self.delete_data_set()
                self.get_data_set_state()
                self.create_data_set()

        else:
            self.create_data_set()

    def warm_data_set(self):  # type: () -> None
        if self.exists:
            try:
                icetool_executions, record_count = _run_icetool(self.name)
                self.executions.extend(icetool_executions)
                if record_count <= 0:
                    self._fail("Data set {0} is empty.".format(self.name))
            except Exception as e:
                self.executions.extend(e.args[1])
                self._fail(e.args[0])
        else:
            self._fail("Data set {0} does not exist.".format(self.name))

    def invalid_target_state(self):   # type: () -> None
        self._fail("{0} is not a valid target state.".format(
            self.target_state))

    def get_target_method(self):   # type: () -> None
        return {
            ABSENT: self.delete_data_set,
            INITIAL: self.init_data_set,
            WARM: self.warm_data_set,
        }.get(self.target_state, self.invalid_target_state)

    def get_data_set_state(self):   # type: () -> None
        try:
            listds_executions, ds_status = _run_listds(self.name)

            self.exists = ds_status["exists"]
            self.data_set_organization = ds_status["data_set_organization"]

            self.executions.extend(listds_executions)
        except Exception as e:
            self.executions.extend(e.args[1])
            self._fail(e.args[0])

    def main(self):  # type: () -> None
        self.get_data_set_state()
        self.set_start_state()

        if self.exists and (self.data_set_organization != self.expected_data_set_organization):
            self._fail(
                "Data set {0} is not in expected format {1}.".format(
                    self.name, self.expected_data_set_organization))

        self.get_target_method()()

        self.get_data_set_state()

        self._exit()
