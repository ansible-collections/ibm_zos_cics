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
    type: int
    required: false
    default: 20
  space_secondary:
    description:
      - The size of the secondary space allocated to the auxiliary trace data set.
        Note that this is just the value; the unit is specified with O(space_type).
      - This option takes effect only when the auxiliary trace data set is being created.
        If the data set already exists, the option has no effect.
    type: int
    required: false
    default: 4
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
start_state:
  description:
    - The state of the local request queue before the Ansible task runs.
  returned: always
  type: dict
  contains:
    data_set_organization:
      description: The organization of the data set at the start of the Ansible task.
      returned: always
      type: str
      sample: "Sequential"
    exists:
      description: True if the local request queue data set exists.
      type: bool
      returned: always
end_state:
  description: The state of the local request queue at the end of the Ansible task.
  returned: always
  type: dict
  contains:
    data_set_organization:
      description: The organization of the data set at the end of the Ansible task.
      returned: always
      type: str
      sample: "Sequential"
    exists:
      description: True if the local request queue data set exists.
      type: bool
      returned: always
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
    DESTINATION_OPTIONS,
    DESTINATION_DEFAULT_VALUE,
    MEGABYTES,
    REGION_DATA_SETS,
    SPACE_PRIMARY,
    SPACE_SECONDARY,
    SPACE_TYPE,
    DataSet
)
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.trace import (
    _build_seq_data_set_definition_trace
)


DSN_A = "dfhauxt"
DSN_B = "dfhbuxt"
SPACE_PRIMARY_DEFAULT = 20
SPACE_SECONDARY_DEFAULT = 4


class AnsibleAuxiliaryTraceModule(DataSet):
    def __init__(self):  # type: () -> None
        self.ds_destination = ""
        super(AnsibleAuxiliaryTraceModule, self).__init__(SPACE_PRIMARY_DEFAULT, SPACE_SECONDARY_DEFAULT)
        if self.destination == "A":
            self.ds_destination = DSN_A
        elif self.destination == "B":
            self.ds_destination = DSN_B
        self.name = self.region_param[self.ds_destination]["dsn"].upper()
        self.expected_data_set_organization = "Sequential"

    def _get_arg_spec(self):  # type: () -> dict
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
        arg_spec[SPACE_SECONDARY].update({
            "default": SPACE_SECONDARY_DEFAULT
        })
        arg_spec[SPACE_TYPE].update({
            "default": MEGABYTES
        })
        arg_spec[REGION_DATA_SETS]["options"].update({
            DSN_A: {
                "type": "dict",
                "required": False,
                "options": {
                    "dsn": {
                        "type": "str",
                        "required": False,
                    },
                },
            },
            DSN_B: {
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

    def get_arg_defs(self):  # type: () -> dict
        defs = super().get_arg_defs()
        defs[REGION_DATA_SETS]["options"][DSN_A]["options"]["dsn"].update({
            "arg_type": "data_set_base"
        })
        defs[REGION_DATA_SETS]["options"][DSN_B]["options"]["dsn"].update({
            "arg_type": "data_set_base"
        })
        defs[REGION_DATA_SETS]["options"][DSN_A]["options"]["dsn"].pop("type")
        defs[REGION_DATA_SETS]["options"][DSN_B]["options"]["dsn"].pop("type")
        return defs

    def create_data_set(self):  # type: () -> None
        definition = _build_seq_data_set_definition_trace(self.get_data_set())
        super().build_seq_data_set(self.ds_destination, definition)


def main():
    AnsibleAuxiliaryTraceModule().main()


if __name__ == '__main__':
    main()
