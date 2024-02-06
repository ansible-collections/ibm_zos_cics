#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: trace
short_description: Allocate auxiliary trace data sets
description:
  - Allocates the two L(auxiliary trace ,https://www.ibm.com/docs/en/cics-ts/6.1?topic=sets-setting-up-auxiliary-trace-data)
    data sets used by a CICS® region. When CICS auxiliary trace is activated, trace entries produced by CICS are written to the auxiliary trace data sets.
    These data sets can hold large amounts of trace data.
author: Kye Maloy (@KyeMaloy97)
version_added: 1.1.0-beta.4
options:
  space_primary:
    description:
      - The size of the primary space allocated to the auxiliary trace data set.
        Note that this is just the value; the unit is specified with O(space_type).
      - This option takes effect only when the auxiliary trace data set is being created.
        If the data set already exists, the option has no effect.
      - The size value of the secondary space allocation for the auxiliary trace data set is 10; the unit is specified with O(space_type).
    type: int
    required: false
    default: 20
  space_type:
    description:
      - The unit portion of the auxiliary trace data set size. Note that this is
        just the unit; the value is specified with O(space_primary).
      - This option takes effect only when the auxiliary trace data set is being created.
        If the data set already exists, the option has no effect.
      - The size can be specified in megabytes (V(M)), kilobytes (V(K)),
        records (V(REC)), cylinders (V(CYL)), or tracks (V(TRK)).
    required: false
    type: str
    choices:
      - M
      - K
      - REC
      - CYL
      - TRK
    default: M
  region_data_sets:
    description:
      - The location of the region data sets to be created using a template, for example,
        C(REGIONS.ABCD0001.<< data_set_name >>).
      - If you want to use a data set that already exists, ensure that the data set is an auxiliary trace data set.
    type: dict
    required: true
    suboptions:
      template:
        description:
          - The base location of the region data sets with a template.
        required: false
        type: str
      dfhauxt:
        description:
          - Overrides the templated location for the DFHAUXT data set.
        required: false
        type: dict
        suboptions:
          dsn:
            description:
              - The data set name of DFHAUXT to override the template.
            type: str
            required: false
      dfhbuxt:
        description:
          - Overrides the templated location for the DFHBUXT data set.
        required: false
        type: dict
        suboptions:
          dsn:
            description:
              - The data set name of DFHBUXT to override the template.
            type: str
            required: false
  cics_data_sets:
    description:
      - The name of the C(SDFHLOAD) library of the CICS installation, for example, C(CICSTS61.CICS.SDFHLOAD).
    type: dict
    required: false
    suboptions:
      template:
        description:
          - The templated location of the C(SDFHLOAD) library.
        required: false
        type: str
      sdfhload:
        description:
          - The location of the C(SDFHLOAD) library to override the template.
        type: str
        required: false
  destination:
    description:
      - The auxiliary trace data set to create. If the value is left blank, A is implied, but you can specify A or B.
      - V(A) will create or delete the A auxiliary trace data set.
      - V(B) will create or delete the B auxiliary trace data set. This MUST be set for the creation of B data set.
    choices:
      - "A"
      - "B"
    type: str
    required: false
    default: "A"
  state:
    description:
      - The intended state for the auxiliary trace data set, which the module will aim to
        achieve.
      - V(absent) will remove the auxiliary trace data set data set entirely, if it
        already exists.
      - V(initial) will create the auxiliary trace data set if it does not
        already exist.
      - V(warm) will retain an existing auxiliary trace data set in its current state.
    choices:
      - "initial"
      - "absent"
      - "warm"
    required: true
    type: str
'''


EXAMPLES = r"""
- name: Allocate auxiliary trace data set A (implicit)
  ibm.ibm_zos_cics.trace:
    state: initial

- name: Allocate auxiliary trace data set A
  ibm.ibm_zos_cics.trace:
    state: initial
    destination: A

- name: Allocate auxiliary trace data set B
  ibm.ibm_zos_cics.trace:
    state: initial
    destination: B

- name: Delete auxiliary trace data set A (implicit)
  ibm.ibm_zos_cics.trace:
    state: absent

- name: Delete auxiliary trace data set B
  ibm.ibm_zos_cics.trace:
    state: absent
    destination: B
"""


RETURN = r"""
changed:
  description: True if the state was changed, otherwise False.
  returned: always
  type: bool
failed:
  description: True if the query job failed, otherwise False.
  returned: always
  type: bool
executions:
  description: A list of program executions performed during the Ansible task.
  returned: always
  type: list
  elements: dict
  contains:
    name:
      description: A human-readable name for the program execution.
      type: str
      returned: always
    rc:
      description: The return code for the program execution.
      type: int
      returned: always
    stdout:
      description: The standard out stream returned by the program execution.
      type: str
      returned: always
    stderr:
      description: The standard error stream returned from the program execution.
      type: str
      returned: always
"""

from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.response import _state
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.trace import _build_seq_data_set_definition_trace
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.trace import _trace_data_set_constants as trace_constants
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.data_set import DataSet
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.data_set import _dataset_constants as ds_constants
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.dataset_utils import (
    _run_listds, _dataset_size, _data_set)
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.better_arg_parser import BetterArgParser


class AnsibleAuxiliaryTraceModule(DataSet):

    ddname_destination = ""

    def __init__(self):
        super(AnsibleAuxiliaryTraceModule, self).__init__()

    def init_argument_spec(self):  # type: () -> dict
        arg_spec = super(
            AnsibleAuxiliaryTraceModule,
            self).init_argument_spec()

        arg_spec.update(
            {
                ds_constants["DESTINATION_ALIAS"]: {
                    "type": "str",
                    "required": False,
                    "choices": trace_constants["TRACE_DESTINATION_OPTIONS"],
                    "default": trace_constants["TRACE_DESTINATION_DEFAULT_VALUE"]
                }
            }
        )

        arg_spec[ds_constants["PRIMARY_SPACE_VALUE_ALIAS"]].update({
            "default": trace_constants["PRIMARY_SPACE_VALUE_DEFAULT"],
        })
        arg_spec[ds_constants["PRIMARY_SPACE_UNIT_ALIAS"]].update({
            "default": trace_constants["PRIMARY_SPACE_UNIT_DEFAULT"],
        })
        arg_spec[ds_constants["TARGET_STATE_ALIAS"]].update({
            "choices": trace_constants["TARGET_STATE_OPTIONS"],
        })
        arg_spec.update({
            ds_constants["REGION_DATA_SETS_ALIAS"]: {
                "type": "dict",
                "required": True,
                "options": {
                    "template": {
                        "type": "str",
                        "required": False,
                    },
                    "dfhauxt": {
                        "type": "dict",
                        "required": False,
                        "options": {
                            "dsn": {
                                "type": "str",
                                "required": False
                            }
                        }
                    },
                    "dfhbuxt": {
                        "type": "dict",
                        "required": False,
                        "options": {
                            "dsn": {
                                "type": "str",
                                "required": False
                            }
                        }
                    }
                },
            },
            ds_constants["CICS_DATA_SETS_ALIAS"]: {
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
        })

        return arg_spec

    def _get_arg_defs(self):  # type () -> dict
        arg_def = super(AnsibleAuxiliaryTraceModule, self)._get_arg_defs()

        arg_def.update(
            {
                ds_constants["DESTINATION_ALIAS"]: {
                    "arg_type": "str",
                    "choices": trace_constants["TRACE_DESTINATION_OPTIONS"],
                    "default": trace_constants["TRACE_DESTINATION_DEFAULT_VALUE"]
                }
            }
        )

        arg_def[ds_constants["PRIMARY_SPACE_VALUE_ALIAS"]].update({
            "default": trace_constants["PRIMARY_SPACE_VALUE_DEFAULT"]
        })
        arg_def[ds_constants["PRIMARY_SPACE_UNIT_ALIAS"]].update({
            "default": trace_constants["PRIMARY_SPACE_UNIT_DEFAULT"]
        })
        arg_def[ds_constants["TARGET_STATE_ALIAS"]].update({
            "choices": trace_constants["TARGET_STATE_OPTIONS"]
        })
        arg_def.update({
            ds_constants["REGION_DATA_SETS_ALIAS"]: {
                "arg_type": "dict",
                "required": True,
                "options": {
                    "template": {
                        "arg_type": "str",
                        "required": False,
                    },
                    "dfhauxt": {
                        "arg_type": "dict",
                        "required": False,
                        "options": {
                            "dsn": {
                                "arg_type": "data_set_base",
                                "required": False,
                            },
                        },
                    },
                    "dfhbuxt": {
                        "arg_type": "dict",
                        "required": False,
                        "options": {
                            "dsn": {
                                "arg_type": "data_set_base",
                                "required": False,
                            },
                        },
                    },
                },
            },
            ds_constants["CICS_DATA_SETS_ALIAS"]: {
                "arg_type": "dict",
                "required": False,
                "options": {
                    "template": {
                        "arg_type": "str",
                        "required": False,
                    },
                    "sdfhload": {
                        "arg_type": "data_set_base",
                        "required": False,
                    },
                },
            },
        })

        return arg_def

    def _get_data_set_object(self, size, result):
        ds_destination = ""
        if result[ds_constants["DESTINATION_ALIAS"]] == "A":
            ds_destination = "dfhauxt"
        elif result[ds_constants["DESTINATION_ALIAS"]] == "B":
            ds_destination = "dfhbuxt"

        self.ddname_destination = ds_destination

        return _data_set(
            size=size,
            name=result.get(ds_constants["REGION_DATA_SETS_ALIAS"]).get(
                ds_destination).get("dsn").upper(),
            state=result.get(ds_constants["TARGET_STATE_ALIAS"]),
            exists=False,
            vsam=False)

    def _get_data_set_size(self, result):
        return _dataset_size(
            unit=result.get(ds_constants["PRIMARY_SPACE_UNIT_ALIAS"]),
            primary=result.get(ds_constants["PRIMARY_SPACE_VALUE_ALIAS"]),
            secondary=ds_constants["SECONDARY_SPACE_VALUE_DEFAULT"]
        )

    def get_data_set_state(self, data_set):
        try:
            listds_executions, ds_status = _run_listds(data_set["name"])

            data_set["exists"] = ds_status["exists"]

            self.result["executions"] = self.result["executions"] + \
                listds_executions
        except Exception as e:
            self.result["executions"] = self.result["executions"] + e.args[1]
            self._fail(e.args[0])

        return data_set

    def validate_parameters(self):
        arg_defs = self._get_arg_defs()

        result = BetterArgParser(arg_defs).parse_args({
            ds_constants["REGION_DATA_SETS_ALIAS"]: self._module.params.get(ds_constants["REGION_DATA_SETS_ALIAS"]),
            ds_constants["CICS_DATA_SETS_ALIAS"]: self._module.params.get(ds_constants["CICS_DATA_SETS_ALIAS"]),
            ds_constants["PRIMARY_SPACE_VALUE_ALIAS"]: self._module.params.get(ds_constants["PRIMARY_SPACE_VALUE_ALIAS"]),
            ds_constants["PRIMARY_SPACE_UNIT_ALIAS"]: self._module.params.get(ds_constants["PRIMARY_SPACE_UNIT_ALIAS"]),
            ds_constants["DATASET_LOCATION_ALIAS"]: self._module.params.get(ds_constants["DATASET_LOCATION_ALIAS"]),
            ds_constants["TARGET_STATE_ALIAS"]: self._module.params.get(ds_constants["TARGET_STATE_ALIAS"]),
            ds_constants["DESTINATION_ALIAS"]: self._module.params.get(
                ds_constants["DESTINATION_ALIAS"])
        })

        size = self._get_data_set_size(result)
        self.data_set = self._get_data_set_object(size, result)

    def create_data_set(self):  # type () -> None

        definition = _build_seq_data_set_definition_trace(self.data_set)
        super().build_seq_data_set(self.ddname_destination, definition)

    def delete_aux_trace_datasets(self):
        if (self.data_set["exists"]):
            super().delete_data_set("Deleting auxiliary trace data set")

    def init_trace(self):
        if (self.data_set["exists"]):
            self.result["end_state"] = _state(
                exists=self.data_set["exists"]
            )

        if not (self.data_set["exists"]):
            self.create_data_set()

    def invalid_state(self):  # type: () -> None
        self._fail("{0} is not a valid target state.".format(
            self.data_set["state"]))

    def get_target_method(self, target):
        return {
            ds_constants["TARGET_STATE_ABSENT"]: self.delete_aux_trace_datasets,
            ds_constants["TARGET_STATE_INITIAL"]: self.init_trace,
            ds_constants["TARGET_STATE_WARM"]: super().warm_data_set
        }.get(target, self.invalid_state)

    def main(self):

        self.data_set = self.get_data_set_state(self.data_set)

        self.result["start_state"] = _state(exists=self.data_set["exists"])

        self.get_target_method(self.data_set["state"])()

        self.end_state = self.get_data_set_state(self.data_set)

        self.result["end_state"] = _state(exists=self.end_state["exists"])

        self._exit()


def main():
    AnsibleAuxiliaryTraceModule().main()


if __name__ == '__main__':
    main()
