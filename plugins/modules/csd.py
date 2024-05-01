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
    For example, use O(state=initial) to create and initialize a CSD
    if it doesn't exist, or empty an existing CSD of all records.
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
        just the unit; the value for the primary space is specified with O(space_primary)
        and the value for the secondary space is specified with O(space_secondary).
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
  volumes:
    description:
      - The volume(s) where the data set is created. Use a string to define a singular volume or a list of strings for multiple volumes.
    type: raw
    required: false
  region_data_sets:
    description:
      - The location of the region data sets to be created by using a template, for example,
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
          - The location of the C(SDFHLOAD) library. If O(cics_data_sets.template) is provided, this value overrides the template.
        type: str
        required: false
  state:
    description:
      - The intended state for the CSD, which the module aims to achieve.
      - Specify V(absent) to remove the CSD entirely, if it already exists.
      - Specify V(initial) to create the CSD if it does not already exist, and initialize it by using DFHCSDUP.
      - Specify V(warm) to retain an existing CSD in its current state.
        The module verifies whether the specified data set exists and whether it contains any records.
        If both conditions are met, the module leaves the data set as is.
        If the data set does not exist or if it is empty, the operation fails.
      - Specify V(script) to run a DFHCSDUP script to update an existing CSD.
    choices:
      - "initial"
      - "absent"
      - "warm"
      - "script"
    required: true
    type: str
  script_location:
    description:
      - The type of location from which to load the DFHCSDUP script.
      - Specify V(DATA_SET) to load from a PDS, PDSE, or sequential data set.
      - Specify V(USS) to load from a file on UNIX System Services (USS).
      - Specify V(LOCAL) to load from a file local to the Ansible control node.
      - Specify V(INLINE) to allow a script to be passed directly through the O(script_content) parameter.
    choices:
      - "DATA_SET"
      - "USS"
      - "LOCAL"
      - "INLINE"
    type: str
    required: false
    default: "DATA_SET"
  script_src:
    description:
      - The path to the source file that contains the DFHCSDUP script to submit.
      - 'It can be a data set. For example: "TESTER.DEFS.SCRIPT" or "TESTER.DEFS(SCRIPT)"'
      - 'It can be a USS file. For example: "/u/tester/defs/script.csdup"'
      - 'It can be a local file. For example: "/User/tester/defs/script.csdup"'
    type: str
    required: false
  script_content:
    description:
      - The content of the DFHCSDUP script to submit, if you are using the O(script_location=INLINE) option.
    type: str
    required: false
  log:
    description:
      - Specify the recovery attribute for the CSD, overriding the CSD system initialization parameters.
      - Specify NONE for a nonrecoverable CSD.
      - Specify UNDO for a CSD that is limited to file backout only.
      - Specify ALL for a CSD for which you want both forward recovery and file backout. If you specify O(log=ALL), you
        must also specify LOGSTREAMID to identify the 26-character name of the z/OS™ log stream to be used as the
        forward recovery log. The CICS collection does not support defining forward recovery log streams; you
        must follow the instructions in L(Defining forward recovery log streams,
        https://www.ibm.com/docs/en/cics-ts/latest?topic=journaling-defining-forward-recovery-log-streams).
    choices:
      - "NONE"
      - "UNDO"
      - "ALL"
    required: false
    type: str
  logstreamid:
    description:
      - The 26-character name of the z/OS™ log stream to be used as the forward recovery log.
      - This is required when you use O(log=ALL).
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

- name: Initialize a large CSD
  ibm.ibm_zos_cics.csd:
    region_data_sets:
      template: "REGIONS.ABCD0001.<< data_set_name >>"
    cics_data_sets:
      template: "CICSTS61.CICS.<< lib_name >>"
    space_primary: 10
    space_type: "M"
    state: "initial"

- name: Delete a CSD
  ibm.ibm_zos_cics.csd:
    region_data_sets:
      template: "REGIONS.ABCD0001.<< data_set_name >>"
    cics_data_sets:
      template: "CICSTS61.CICS.<< lib_name >>"
    state: "absent"

- name: Retain the existing state of a CSD
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
    script_location: "DATA_SET"
    script_src: "TESTER.DEFS.SCRIPT"

- name: Run a DFHCSDUP script from a USS file
  ibm.ibm_zos_cics.csd:
    region_data_sets:
      template: "REGIONS.ABCD0001.<< data_set_name >>"
    cics_data_sets:
      template: "CICSTS61.CICS.<< lib_name >>"
    script_location: "USS"
    script_src: "/u/tester/defs/script.csdup"

- name: Run a DFHCSDUP script from a local file
  ibm.ibm_zos_cics.csd:
    region_data_sets:
      template: "REGIONS.ABCD0001.<< data_set_name >>"
    cics_data_sets:
      template: "CICSTS61.CICS.<< lib_name >>"
    script_location: "LOCAL"
    script_src: "/User/tester/defs/script.csdup"

- name: Run a DFHCSDUP script inline
  ibm.ibm_zos_cics.csd:
    region_data_sets:
      template: "REGIONS.ABCD0001.<< data_set_name >>"
    cics_data_sets:
      template: "CICSTS61.CICS.<< lib_name >>"
    script_location: "INLINE"
    script_content: |
      DEFINE PROGRAM(TESTPRG1) GROUP(TESTGRP1)
      DEFINE PROGRAM(TESTPRG2) GROUP(TESTGRP2)
"""


RETURN = r"""
changed:
  description: True if the state was changed, otherwise False.
  returned: always
  type: bool
failed:
  description: True if the Ansible task failed, otherwise False.
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
      description: The standard output stream returned from the program execution.
      type: str
      returned: always
    stderr:
      description: The standard error stream returned from the program execution.
      type: str
      returned: always
msg:
  description: A string containing an error message if applicable
  returned: always
  type: str
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
SCRIPT_CONTENT = "script_content"
DATA_SET = "DATA_SET"
USS = "USS"
LOCAL = "LOCAL"
INLINE = "INLINE"
SCRIPT_LOCATION_OPTIONS = [DATA_SET, USS, LOCAL, INLINE]
SCRIPT_LOCATION_DEFAULT = DATA_SET
LOG = "log"
LOG_OPTIONS = ["NONE", "UNDO", "ALL"]
LOGSTREAMID = "logstreamid"


class AnsibleCSDModule(DataSet):
    def __init__(self):
        self.script_src = ""
        self.script_location = ""
        super(AnsibleCSDModule, self).__init__(SPACE_PRIMARY_DEFAULT, SPACE_SECONDARY_DEFAULT)
        self._validate_log_args()
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
            SCRIPT_CONTENT: {
                "type": "str"
            },
        })
        arg_spec.update({
            LOG: {
                "type": "str",
                "choices": LOG_OPTIONS,
                "required": False
            },
        })
        arg_spec.update({
            LOGSTREAMID: {
                "type": "str",
                "required": False
            },
        })
        return arg_spec

    def _validate_log_args(self):
        if self._module.params.get(LOG, "") == "ALL" and self._module.params.get(LOGSTREAMID) is None:
            self._fail("LOGSTREAMID must be provided when LOG is set to ALL.")

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
        if params.get(SCRIPT_CONTENT):
            self.script_content = params[SCRIPT_CONTENT]

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

    def get_data_set(self):
        data_set = super().get_data_set()
        data_set.update({
            LOG: self._module.params.get(LOG),
            LOGSTREAMID: self._module.params.get(LOGSTREAMID)
        })
        return data_set

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

        if self.script_location == INLINE:
            if not self.script_content:
                self._fail("script_content required when script_location={0}".format(self.script_location))
        else:
            if not self.script_src:
                self._fail("script_src required when script_location={0}".format(self.script_location))

        try:
            csdup_script_executions = []
            if self.script_location == DATA_SET:
                csdup_script_executions.extend(_run_dfhcsdup(self.get_data_set(), DatasetDefinition(self.script_src)))
            elif self.script_location == USS:
                file = open(self.script_src)
                file_content = file.read()
                csdup_script_executions.extend(_run_dfhcsdup(self.get_data_set(), StdinDefinition(content=file_content)))
            elif self.script_location in [LOCAL, INLINE]:
                csdup_script_executions.extend(_run_dfhcsdup(self.get_data_set(), StdinDefinition(content=self.script_content)))
            else:
                self._fail("script_location: {0} not recognised.".format(self.script_location))

            self.executions.extend(csdup_script_executions)

            self.changed = True
        except MVSExecutionException as e:
            self.executions.extend(e.executions)
            self._fail(e.message)
        except (OSError, ValueError) as e:
            # Handles the 'open' method failures
            self.executions.extend(csdup_script_executions)
            self._fail("{0} - {1}".format(type(e).__name__, str(e)))


def main():
    AnsibleCSDModule().main()


if __name__ == '__main__':
    main()
