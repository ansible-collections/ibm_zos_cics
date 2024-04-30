#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: intrapartition
short_description: Create and remove the CICS transient data intrapartition data set
description:
  - Create and remove the L(transient data intrapartition,https://www.ibm.com/docs/en/cics-ts/latest?topic=data-defining-intrapartition-set)
    data set used by a CICS® region. This data set holds all the data for intrapartition queues.
  - You can use this module when provisioning or de-provisioning a CICS region.
  - Use the O(state) option to specify the intended state for the transient data
    intrapartition data set. For example, use O(state=initial) to create a transient data
    intrapartition data set if it doesn't exist.
author: Andrew Twydell (@andrewtwydell)
version_added: 1.1.0-beta.4
options:
  space_primary:
    description:
      - The size of the primary space allocated to the transient data intrapartition data set.
        Note that this is just the value; the unit is specified with O(space_type).
      - This option takes effect only when the transient data intrapartition data set is being created.
        If the data set already exists, the option has no effect.
    type: int
    required: false
    default: 100
  space_secondary:
    description:
      - The size of the secondary space allocated to the transient data intrapartition data set.
        Note that this is just the value; the unit is specified with O(space_type).
      - This option takes effect only when the transient data intrapartition data set is being created.
        If the data set already exists, the option has no effect.
    type: int
    required: false
    default: 10
  space_type:
    description:
      - The unit portion of the transient data intrapartition data set size. Note that this is
        just the unit; the value for the primary space is specified with O(space_primary) and the value
        for the secondary space is specified with O(space_secondary).
      - This option takes effect only when the transient data intrapartition data set is being created.
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
    default: REC
  volumes:
    description:
      - The volume(s) where the data set is created. Use a string to define a singular volume or a list of strings for multiple volumes.
    type: raw
    required: false
  region_data_sets:
    description:
      - The location of the region data sets to be created by using a template, for example,
        C(REGIONS.ABCD0001.<< data_set_name >>).
      - If you want to use a data set that already exists, ensure that the data set is a transient data intrapartition data set.
    type: dict
    required: true
    suboptions:
      template:
        description:
          - The base location of the region data sets with a template.
        required: false
        type: str
      dfhintra:
        description:
          - Overrides the templated location for the transient data intrapartition data set.
        required: false
        type: dict
        suboptions:
          dsn:
            description:
              - The data set name of the transient data intrapartition to override the template.
            type: str
            required: false
  state:
    description:
      - The intended state for the transient data intrapartition data set, which the module aims to achieve.
      - Specify V(absent) to remove the transient data intrapartition data set entirely, if it exists.
      - Specify V(initial) to create the transient data intrapartition data set if it does not exist.
        If the specified data set exists but is empty, the module leaves the data set as is.
        If the specified data set exists and has contents, the module deletes the data set and then creates a new, empty one.
      - Specify V(warm) to retain an existing transient data intrapartition data set in its current state.
        The module verifies whether the specified data set exists and whether it contains any records.
        If both conditions are met, the module leaves the data set as is.
        If the data set does not exist or if it is empty, the operation fails.
    choices:
      - "initial"
      - "absent"
      - "warm"
    required: true
    type: str
"""


EXAMPLES = r"""
- name: Initialize a transient data intrapartition data set
  ibm.ibm_zos_cics.intrapartition:
    region_data_sets:
      template: "REGIONS.ABCD0001.<< data_set_name >>"
    state: "initial"

- name: Initialize a large transient data intrapartition data set
  ibm.ibm_zos_cics.intrapartition:
    region_data_sets:
      template: "REGIONS.ABCD0001.<< data_set_name >>"
    space_primary: 50
    space_type: "M"
    state: "initial"

- name: Delete a transient data intrapartition data set
  ibm.ibm_zos_cics.intrapartition:
    region_data_sets:
      template: "REGIONS.ABCD0001.<< data_set_name >>"
    state: "absent"
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
    - The state of the transient data intrapartition data set before the Ansible task runs.
  returned: always
  type: dict
  contains:
    data_set_organization:
      description: The organization of the data set at the start of the Ansible task.
      returned: always
      type: str
      sample: "VSAM"
    exists:
      description: True if the specified transient data intrapartition data set exists.
      type: bool
      returned: always
end_state:
  description: The state of the transient data intrapartition data set at the end of the Ansible task.
  returned: always
  type: dict
  contains:
    data_set_organization:
      description: The organization of the data set at the end of the Ansible task.
      returned: always
      type: str
      sample: "VSAM"
    exists:
      description: True if the specified transient data intrapartition data set exists.
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
"""

from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.data_set_utils import _build_idcams_define_cmd
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.data_set import (
    RECORDS,
    REGION_DATA_SETS,
    SPACE_PRIMARY,
    SPACE_SECONDARY,
    SPACE_TYPE,
    DataSet
)
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.intrapartition import (
    _get_idcams_cmd_intra
)


DSN = "dfhintra"
SPACE_PRIMARY_DEFAULT = 100
SPACE_SECONDARY_DEFAULT = 10


class AnsibleIntrapartitionModule(DataSet):
    def __init__(self):
        super(AnsibleIntrapartitionModule, self).__init__(SPACE_PRIMARY_DEFAULT, SPACE_SECONDARY_DEFAULT)
        self.name = self.region_param[DSN]["dsn"].upper()
        self.expected_data_set_organization = "VSAM"

    def _get_arg_spec(self):  # type: () -> dict
        arg_spec = super(AnsibleIntrapartitionModule, self)._get_arg_spec()

        arg_spec[SPACE_PRIMARY].update({
            "default": SPACE_PRIMARY_DEFAULT
        })
        arg_spec[SPACE_SECONDARY].update({
            "default": SPACE_SECONDARY_DEFAULT
        })
        arg_spec[SPACE_TYPE].update({
            "default": RECORDS
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

        return arg_spec

    def get_arg_defs(self):  # type: () -> dict
        defs = super().get_arg_defs()
        defs[REGION_DATA_SETS]["options"][DSN]["options"]["dsn"].update({
            "arg_type": "data_set_base"
        })
        defs[REGION_DATA_SETS]["options"][DSN]["options"]["dsn"].pop("type")
        return defs

    def create_data_set(self):  # type: () -> None
        create_cmd = _build_idcams_define_cmd(_get_idcams_cmd_intra(self.get_data_set()))
        super().build_vsam_data_set(create_cmd)


def main():
    AnsibleIntrapartitionModule().main()


if __name__ == "__main__":
    main()
