#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: csd
short_description: Create, remove, and manage the CICS CSD
description:
  - Create, remove, and manage the
    L(CICS system definition data set,https://www.ibm.com/docs/en/cics-ts/6.1?topic=configuring-setting-up-shared-data-sets-csd-sysin) (CSD) used by a CICS®
    region.
  - You can use this module when provisioning or de-provisioning a CICS region, or when managing
    the state of the CSD during upgrades or restarts.
  - Use the O(state) option to specify the intended state for the CSD.
    For example, O(state=initial) will create and initialize a CSD
    if it doesn't exist, or it will take an existing
    CSD and empty it of all records.
author: Thomas Latham (@Thomas-Latham3)
version_added: 1.1.0-beta.4
options:
  space_primary:
    description:
      - The size of the primary space allocated to the CSD.
        Note that this is just the value; the unit is specified with O(space_type).
      - This option takes effect only when the CSD is being created.
        If the CSD already exists, the option has no effect.
    type: int
    required: false
    default: 4
  space_secondary:
    description:
      - The size of the secondary space allocated to the CSD.
        Note that this is just the value; the unit is specified with O(space_type).
      - This option takes effect only when the CSD is being created.
        If the CSD already exists, the option has no effect.
    type: int
    required: false
    default: 1
  space_type:
    description:
      - The unit portion of the CSD size. Note that this is
        just the unit; the value is specified with O(space_primary).
      - This option takes effect only when the CSD is being created.
        If the CSD already exists, the option has no effect.
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
      dfhcsd:
        description:
          - Overrides the templated location for the CSD.
        required: false
        type: dict
        suboptions:
          dsn:
            description:
              - The data set name of the CSD to override the template.
            type: str
            required: false
  cics_data_sets:
    description:
      - The name of the C(SDFHLOAD) library of the CICS installation, for example, C(CICSTS61.CICS.SDFHLOAD).
    type: dict
    required: true
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
  state:
    description:
      - The intended state for the CSD, which the module will aim to
        achieve.
      - V(absent) will remove the CSD entirely, if it already exists.
      - V(initial) will create the CSD if it does not
        already exist, and initialize it by using DFHCSDUP.
      - V(warm) will retain an existing CSD in its current state.
      - V(script) will run a DFHCSDUP script to update an existing CSD.
    choices:
      - "initial"
      - "absent"
      - "warm"
      - "script"
    required: true
    type: str
  script_location:
    description:
      - The type of location to load the DFHCSDUP script from.
      - V(DATA_SET) will load from a data set a PDS, PDSE, or sequential data set.
      - V(USS) will load from a file on UNIX System Services (USS).
      - V(LOCAL) will load from a file local to the ansible control node. NOT SUPPORTED IN THIS BETA.
    choices:
      - "DATA_SET"
      - "USS"
      - "LOCAL"
    type: str
    required: false
    default: "DATA_SET"
  script_src:
    description:
      - The path to the source file containing the DFHCSDUP script to submit.
      - It could be a data set.(e.g "MY.HLQ.SOME.DEFS","MY.HLQ.SOME(DEFS)").
      - Or a USS file (e.g "/u/tester/demo/sample.csdup").
      - Or a LOCAL file (e.g "/User/tester/ansible-playbook/script.csdup"). NOT SUPPORTED IN THIS BETA.
    type: str
    required: false
'''


EXAMPLES = r"""
- name: Initialize a CSD
  ibm.ibm_zos_cics.csd:
    region_data_sets:
      template: "REGIONS.ABCD0001.<< data_set_name >>"
    cics_data_sets:
      template: "CICSTS61.CICS.<< lib_name >>"
    state: "initial"

- name: Initialize a large CSD data set
  ibm.ibm_zos_cics.csd:
    region_data_sets:
      template: "REGIONS.ABCD0001.<< data_set_name >>"
    cics_data_sets:
      template: "CICSTS61.CICS.<< lib_name >>"
    space_primary: 10
    space_type: "M"
    state: "initial"

- name: Delete CSD
  ibm.ibm_zos_cics.csd:
    region_data_sets:
      template: "REGIONS.ABCD0001.<< data_set_name >>"
    cics_data_sets:
      template: "CICSTS61.CICS.<< lib_name >>"
    state: "absent"

- name: Retain existing state of CSD
  ibm.ibm_zos_cics.csd:
    region_data_sets:
      template: "REGIONS.ABCD0001.<< data_set_name >>"
    cics_data_sets:
      template: "CICSTS61.CICS.<< lib_name >>"
    state: "warm"

- name: Run a DFHCSDUP script from a data set
  ibm.ibm_zos_cics.csd:
    region_data_sets:
      template: "REGIONS.ABCD0001.<< data_set_name >>"
    cics_data_sets:
      template: "CICSTS61.CICS.<< lib_name >>"
    state: "script"
    script_src: "MY.HLQ.SOME.DEFS"

- name: Run a DFHCSDUP script from a USS file
  ibm.ibm_zos_cics.csd:
    region_data_sets:
      template: "REGIONS.ABCD0001.<< data_set_name >>"
    cics_data_sets:
      template: "CICSTS61.CICS.<< lib_name >>"
    script_src: "/path/to/my/defs.csdup"
    script_location: "USS"
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
    - The state of the CSD before the Ansible task runs.
  returned: always
  type: dict
  contains:
    data_set_organization:
      description: The organization of the data set at the start of the Ansible task.
      returned: always
      type: str
      sample: "VSAM"
    exists:
      description: True if the CSD exists.
      type: bool
      returned: always
end_state:
  description: The state of the CSD at the end of the Ansible task.
  returned: always
  type: dict
  contains:
    data_set_organization:
      description: The organization of the data set at the end of the Ansible task.
      returned: always
      type: str
      sample: "VSAM"
    exists:
      description: True if the CSD exists.
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


from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.response import MVSExecutionException
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.dd_statement import DatasetDefinition, StdinDefinition
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.data_set_utils import (
    _build_idcams_define_cmd
)
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.data_set import (
    CICS_DATA_SETS,
    MEGABYTES,
    REGION_DATA_SETS,
    SPACE_PRIMARY,
    SPACE_SECONDARY,
    SPACE_TYPE,
    STATE,
    ABSENT,
    INITIAL,
    WARM,
    DataSet
)
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.csd import (
    _get_csdup_initilize_cmd,
    _get_idcams_cmd_csd,
    _run_dfhcsdup
)

DSN = "dfhcsd"
SPACE_PRIMARY_DEFAULT = 4
SPACE_SECONDARY_DEFAULT = 1
SCRIPT = "script"
STATE_OPTIONS = [ABSENT, INITIAL, WARM, SCRIPT]
SCRIPT_SOURCE = "script_src"
SCRIPT_LOCATION = "script_location"
DATA_SET = "DATA_SET"
USS = "USS"
LOCAL = "LOCAL"
SCRIPT_LOCATION_OPTIONS = [DATA_SET, USS, LOCAL]
SCRIPT_LOCATION_DEFAULT = DATA_SET


class AnsibleCSDModule(DataSet):
    def __init__(self):
        self.script_src = ""
        self.script_location = ""
        super(AnsibleCSDModule, self).__init__(SPACE_PRIMARY_DEFAULT, SPACE_SECONDARY_DEFAULT)
        self.name = self.region_param[DSN]["dsn"].upper()
        self.expected_data_set_organization = "VSAM"

    def _get_arg_spec(self):  # type: () -> dict
        arg_spec = super(AnsibleCSDModule, self)._get_arg_spec()

        arg_spec[SPACE_PRIMARY].update({
            "default": SPACE_PRIMARY_DEFAULT
        })
        arg_spec[SPACE_SECONDARY].update({
            "default": SPACE_SECONDARY_DEFAULT
        })
        arg_spec[SPACE_TYPE].update({
            "default": MEGABYTES
        })
        arg_spec[STATE].update({
            "choices": STATE_OPTIONS
        })
        arg_spec[REGION_DATA_SETS]["options"].update({
            DSN: {
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
        arg_spec[CICS_DATA_SETS] = {
            "type": "dict",
            "required": True,
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
        }
        arg_spec.update({
            SCRIPT_SOURCE: {
                "type": "str"
            },
            SCRIPT_LOCATION: {
                "type": "str",
                "choices": SCRIPT_LOCATION_OPTIONS,
                "default": DATA_SET
            },
        })

        return arg_spec

    def get_arg_defs(self):  # type: () -> dict
        defs = super().get_arg_defs()
        defs[REGION_DATA_SETS]["options"][DSN]["options"]["dsn"].update({
            "arg_type": "data_set_base"
        })
        defs[REGION_DATA_SETS]["options"][DSN]["options"]["dsn"].pop("type")
        if SCRIPT_LOCATION == DATA_SET:
            defs[SCRIPT_SOURCE].update({
                "arg_type": "data_set_base"
            })
            defs[SCRIPT_SOURCE].pop("type")
        return defs

    def assign_parameters(self, params):  # type: (dict) -> None
        super().assign_parameters(params)
        if params.get(SCRIPT_SOURCE):
            self.script_src = params[SCRIPT_SOURCE]
        if params.get(SCRIPT_LOCATION):
            self.script_location = params[SCRIPT_LOCATION]

    def execute_target_state(self):   # type: () -> None
        if self.target_state == ABSENT:
            self.delete_data_set()
        elif self.target_state == INITIAL:
            self.init_data_set()
        elif self.target_state == WARM:
            self.warm_data_set()
        elif self.target_state == SCRIPT:
            self.csdup_script()
        else:
            self.invalid_target_state()

    def create_data_set(self):  # type: () -> None
        create_cmd = _build_idcams_define_cmd(_get_idcams_cmd_csd(self.get_data_set()))
        super().build_vsam_data_set(create_cmd)

    def init_data_set(self):  # type: () -> None
        super().init_data_set()
        try:
            csdup_initialize_executions = _run_dfhcsdup(self.get_data_set(), _get_csdup_initilize_cmd())
            self.executions.extend(csdup_initialize_executions)
        except MVSExecutionException as e:
            self.executions.extend(e.executions)
            self._fail(e.message)

    def csdup_script(self):

        if not self.script_location:
            self._fail("script_location required")

        if not self.script_src:
            self._fail("script_src required")

        try:
            csdup_script_executions = []
            if self.script_location == DATA_SET:
                csdup_script_executions.extend(_run_dfhcsdup(self.get_data_set(), DatasetDefinition(self.script_src)))
            elif self.script_location == USS:
                file = open(self.script_src)
                file_content = file.read()
                csdup_script_executions.append(_run_dfhcsdup(self.get_data_set(), StdinDefinition(content=file_content)))
            elif self.script_location == LOCAL:
                self._fail("script_location: LOCAL not supported in this beta.")
            else:
                self._fail("script_location: {0} not recognised.".format(self.script_location))

            self.executions.extend(csdup_script_executions)

            self.changed = True
        except MVSExecutionException as e:
            self.executions.extend(e.executions)
            self._fail(e.message)


def main():
    AnsibleCSDModule().main()


if __name__ == '__main__':
    main()
