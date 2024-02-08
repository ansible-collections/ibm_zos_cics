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
      - The size value of the secondary space allocation for the CSD is 1; the unit is specified with O(space_type).
    type: int
    required: false
    default: 4
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
    choices:
      - "initial"
      - "absent"
      - "warm"
    required: true
    type: str
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


from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.dataset_utils import (
    _build_idcams_define_cmd
)
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.data_set import (
    CICS_DATA_SETS,
    REGION_DATA_SETS,
    SPACE_PRIMARY,
    SPACE_TYPE,
    STATE,
    DataSet
)
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.csd import (
    SPACE_PRIMARY_DEFAULT,
    SPACE_TYPE_DEFAULT,
    STATE_OPTIONS,
    _get_idcams_cmd_csd,
    _run_dfhcsdup
)


class AnsibleCSDModule(DataSet):
    def __init__(self):
        super(AnsibleCSDModule, self).__init__()

    def _get_arg_spec(self):  # type: () -> dict
        arg_spec = super(AnsibleCSDModule, self)._get_arg_spec()

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
            "dfhcsd": {
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
        arg_spec[CICS_DATA_SETS].update({
            "required": True
        })

        return arg_spec

    def get_arg_defs(self) -> dict:
        defs = super().get_arg_defs()
        defs[REGION_DATA_SETS]["options"]["dfhcsd"]["options"]["dsn"].update({
            "arg_type": "data_set_base"
        })
        defs[REGION_DATA_SETS]["options"]["dfhcsd"]["options"]["dsn"].pop("type")
        return defs

    def validate_parameters(self) -> None:
        super().validate_parameters()
        self.name = self.region_param.get("dfhcsd").get("dsn").upper()
        self.expected_data_set_organization = "VSAM"

    def create_data_set(self) -> None:
        create_cmd = _build_idcams_define_cmd(_get_idcams_cmd_csd(self.get_data_set()))
        super().build_vsam_data_set(create_cmd)

    def init_data_set(self) -> None:
        super().init_data_set()
        try:
            csdup_executions = _run_dfhcsdup(self.get_data_set())
            self.executions.extend(csdup_executions)
        except Exception as e:
            self.executions.extend(e.args[1])
            self._fail(e.args[0])


def main():
    AnsibleCSDModule().main()


if __name__ == '__main__':
    main()
