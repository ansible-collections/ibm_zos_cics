#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: transaction_dump
short_description: Allocate transaction dump data sets
description:
  - Allocates the two L(transaction dump ,https://www.ibm.com/docs/en/cics-ts/6.1?topic=sets-defining-transaction-dump-data)
    data sets used by a CICS® region.
author: Thomas Foyle (@tom-foyle)
version_added: 1.1.0-beta.4
options:
  space_primary:
    description:
      - The size of the primary space allocated to the transaction dump data set.
        Note that this is just the value; the unit is specified with O(space_type).
      - This option takes effect only when the transaction dump data set is being created.
        If the data set already exists, the option has no effect.
      - The size value of the secondary space allocation for the transaction dump data set is 10; the unit is specified with O(space_type).
    type: int
    required: false
    default: 20
  space_type:
    description:
      - The unit portion of the transaction dump data set size. Note that this is
        just the unit; the value is specified with O(space_primary).
      - This option takes effect only when the transaction dump data set is being created.
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
    type: dict
    required: true
    suboptions:
      template:
        description:
          - The base location of the region data sets with a template.
        required: false
        type: str
      dfhdmpa:
        description:
          - Overrides the templated location for the DFHDMPA data set.
        required: false
        type: dict
        suboptions:
          dsn:
            description:
              - The data set name of DFHDMPA to override the template.
            type: str
            required: false
      dfhdmpb:
        description:
          - Overrides the templated location for the DFHDMPB data set.
        required: false
        type: dict
        suboptions:
          dsn:
            description:
              - The data set name of DFHDMPB to override the template.
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
      - The transaction dump data set to create. If the value is left blank, A is implied, but you can specify A or B.
      - V(A) will create or delete the A transaction dump data set.
      - V(B) will create or delete the B transaction dump data set. This MUST be set for the creation of the B data set.
    choices:
      - "A"
      - "B"
    type: str
    required: false
    default: "A"
  state:
    description:
      - The intended state for the transaction dump data set, which the module will aim to
        achieve.
      - V(absent) will remove the transaction dump data set data set entirely, if it already exists.
      - V(initial) will create the transaction dump data set if it does not already exist.
      - V(warm) will retain an existing transaction dump data set in its current state.
    choices:
      - "initial"
      - "absent"
      - "warm"
    required: true
    type: str
'''


EXAMPLES = r"""
- name: Allocate transaction dump data set A (implicit)
  ibm.ibm_zos_cics.transaction_dump:
    state: initial

- name: Allocate transaction dump data set A
  ibm.ibm_zos_cics.transaction_dump:
    state: initial
    destination: A

- name: Allocate transaction dump data set B
  ibm.ibm_zos_cics.transaction_dump:
    state: initial
    destination: B

- name: Delete transaction dump data set A (implicit)
  ibm.ibm_zos_cics.transaction_dump:
    state: absent

- name: Delete transaction dump data set B
  ibm.ibm_zos_cics.transaction_dump:
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
    REGION_DATA_SETS,
    SPACE_PRIMARY,
    SPACE_TYPE,
    STATE,
    DataSet
)
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.transaction_dump import (
    DESTINATION_OPTIONS,
    DESTINATION_DEFAULT_VALUE,
    SPACE_PRIMARY_DEFAULT,
    SPACE_TYPE_DEFAULT,
    STATE_OPTIONS,
    _build_seq_data_set_definition_transaction_dump
)


class AnsibleTransactionDumpModule(DataSet):

    ds_destination = ""

    def __init__(self):  # type: () -> None
        super(AnsibleTransactionDumpModule, self).__init__()

    def _get_arg_spec(self):  # type: () -> dict
        arg_spec = super(AnsibleTransactionDumpModule, self)._get_arg_spec()

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
            "dfhdmpa": {
                "type": "dict",
                "required": False,
                "options": {
                    "dsn": {
                        "type": "str",
                        "required": False,
                    },
                },
            },
            "dfhdmpb": {
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
        defs[REGION_DATA_SETS]["options"]["dfhdmpa"]["options"]["dsn"].update({
            "arg_type": "data_set_base"
        })
        defs[REGION_DATA_SETS]["options"]["dfhdmpb"]["options"]["dsn"].update({
            "arg_type": "data_set_base"
        })
        defs[REGION_DATA_SETS]["options"]["dfhdmpa"]["options"]["dsn"].pop("type")
        defs[REGION_DATA_SETS]["options"]["dfhdmpb"]["options"]["dsn"].pop("type")
        return defs

    def validate_parameters(self):  # type: () -> None
        super().validate_parameters()
        if self.destination == "A":
            self.ds_destination = "dfhdmpa"
        elif self.destination == "B":
            self.ds_destination = "dfhdmpb"
        self.name = self.region_param.get(self.ds_destination).get("dsn").upper()
        self.expected_data_set_organization = "Sequential"

    def create_data_set(self):  # type: () -> None
        definition = _build_seq_data_set_definition_transaction_dump(self.get_data_set())
        super().build_seq_data_set(self.ds_destination, definition)


def main():
    AnsibleTransactionDumpModule().main()


if __name__ == '__main__':
    main()
