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

from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.data_set import (
    DESTINATION,
    REGION_DATA_SETS,
    SPACE_PRIMARY,
    SPACE_TYPE,
    STATE,
    DataSet
)
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.trace import (
    DESTINATION_OPTIONS,
    DESTINATION_DEFAULT_VALUE,
    SPACE_PRIMARY_DEFAULT,
    SPACE_TYPE_DEFAULT,
    STATE_OPTIONS,
    _build_seq_data_set_definition_trace
)


class AnsibleAuxiliaryTraceModule(DataSet):

    ds_destination: str = ""

    def __init__(self) -> None:
        super(AnsibleAuxiliaryTraceModule, self).__init__()

    def _get_arg_spec(self) -> dict:
        arg_spec = super(AnsibleAuxiliaryTraceModule, self)._get_arg_spec()

        arg_spec.update({
            DESTINATION: {
                "type": "str",
                "choices": DESTINATION_OPTIONS,
                "default": DESTINATION_DEFAULT_VALUE
            }
        })

        arg_spec[SPACE_PRIMARY].update({
            "default": SPACE_PRIMARY_DEFAULT
        })
        arg_spec[SPACE_TYPE].update({
            "default": SPACE_TYPE_DEFAULT
        })
        arg_spec[STATE].update({
            "choices": STATE_OPTIONS
        })
        arg_spec[REGION_DATA_SETS]["options"].update({
            "dfhauxt": {
                "type": "dict",
                "required": False,
                "options": {
                    "dsn": {
                        "type": "str",
                        "required": False,
                    },
                },
            },
            "dfhbuxt": {
                "type": "dict",
                "required": False,
                "options": {
                    "dsn": {
                        "type": "str",
                        "required": False,
                    },
                },
            },
        })

        return arg_spec

    def get_arg_defs(self) -> dict:
        defs = super().get_arg_defs()
        defs[REGION_DATA_SETS]["options"]["dfhauxt"]["options"]["dsn"].update({
            "arg_type": "data_set_base"
        })
        defs[REGION_DATA_SETS]["options"]["dfhbuxt"]["options"]["dsn"].update({
            "arg_type": "data_set_base"
        })
        defs[REGION_DATA_SETS]["options"]["dfhauxt"]["options"]["dsn"].pop("type")
        defs[REGION_DATA_SETS]["options"]["dfhbuxt"]["options"]["dsn"].pop("type")
        return defs

    def validate_parameters(self) -> None:
        super().validate_parameters()
        if self.destination == "A":
            self.ds_destination = "dfhauxt"
        elif self.destination == "B":
            self.ds_destination = "dfhbuxt"
        self.name = self.region_param.get(self.ds_destination).get("dsn").upper()
        self.expected_data_set_organization = "Sequential"

    def create_data_set(self) -> None:
        definition = _build_seq_data_set_definition_trace(self.get_data_set())
        super().build_seq_data_set(self.ds_destination, definition)


def main():
    AnsibleAuxiliaryTraceModule().main()


if __name__ == '__main__':
    main()
