#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: local_request_queue
short_description: Create and remove the CICS local request queue
description:
  - Create and remove the L(local request queue,https://www.ibm.com/docs/en/cics-ts/latest?topic=sets-local-request-queue-data-set)
    data set used by a CICS® region. The local request queue data set stores pending BTS requests. It ensures that, if CICS fails, no pending requests are lost.
  - You can use this module when provisioning or de-provisioning a CICS region.
  - Use the O(state) option to specify the intended state for the local
    request queue. For example, O(state=initial) will create a local
    request queue data set if it doesn't yet exist, or it will take an existing
    local request queue and empty it of all records.
author: Drew Hughes (@andrewhughes101)
version_added: 1.1.0-beta.3
options:
  space_primary:
    description:
      - The size of the primary space allocated to the local request queue data set.
        Note that this is just the value; the unit is specified with O(space_type).
      - This option takes effect when the local request queue data set is being created.
        If the data set already exists, the option has no effect.
    type: int
    required: false
    default: 4
  space_secondary:
    description:
      - The size of the secondary space allocated to the local request queue data set.
        Note that this is just the value; the unit is specified with O(space_type).
      - This option takes effect when the local request queue data set is being created.
        If the data set already exists, the option has no effect.
    type: int
    required: false
    default: 1
  space_type:
    description:
      - The unit portion of the local request queue data set size. Note that this is
        just the unit; the value is specified with O(space_primary).
      - This option takes effect only when the local request queue data set is being created.
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
      - If you want to use a data set that already exists, ensure that the data set is a local request queue data set.
    type: dict
    required: true
    suboptions:
      template:
        description:
          - The base location of the region data sets with a template.
        required: false
        type: str
      dfhlrq:
        description:
          - Overrides the templated location for the local request queue data set.
        required: false
        type: dict
        suboptions:
          dsn:
            description:
              - The data set name of the local request queue to override the template.
            type: str
            required: false
  state:
    description:
      - The intended state for the local request queue, which the module will aim to
        achieve.
      - V(absent) will remove the local request queue data set entirely, if it
        already exists.
      - V(initial) will create the local request queue data set if it does not
        already exist, and empty it of all existing records.
      - V(warm) will retain an existing local request queue data set in its current state.
    choices:
      - "initial"
      - "absent"
      - "warm"
    required: true
    type: str
'''


EXAMPLES = r"""
- name: Initialize a local request queue
  ibm.ibm_zos_cics.local_request_queue:
    region_data_sets:
      template: "REGIONS.ABCD0001.<< data_set_name >>"
    state: "initial"

- name: Initialize a large request queue
  ibm.ibm_zos_cics.local_request_queue:
    region_data_sets:
      template: "REGIONS.ABCD0001.<< data_set_name >>"
    space_primary: 50
    space_type: "M"
    state: "initial"

- name: Delete local request queue
  ibm.ibm_zos_cics.local_request_queue:
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
      sample: "VSAM"
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
      sample: "VSAM"
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

from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.data_set_utils import (
    _build_idcams_define_cmd
)
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.data_set import (
    MEGABYTES,
    REGION_DATA_SETS,
    SPACE_PRIMARY,
    SPACE_SECONDARY,
    SPACE_TYPE,
    DataSet
)
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.local_request_queue import (
    _get_idcams_cmd_lrq
)


DSN = "dfhlrq"
SPACE_PRIMARY_DEFAULT = 4
SPACE_SECONDARY_DEFAULT = 1


class AnsibleLocalRequestQueueModule(DataSet):
    def __init__(self):
        super(AnsibleLocalRequestQueueModule, self).__init__(SPACE_PRIMARY_DEFAULT, SPACE_SECONDARY_DEFAULT)
        self.name = self.region_param[DSN]["dsn"].upper()
        self.expected_data_set_organization = "VSAM"

    def _get_arg_spec(self):  # type: () -> dict
        arg_spec = super(AnsibleLocalRequestQueueModule, self)._get_arg_spec()

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
        create_cmd = _build_idcams_define_cmd(_get_idcams_cmd_lrq(self.get_data_set()))
        super().build_vsam_data_set(create_cmd)


def main():
    AnsibleLocalRequestQueueModule().main()


if __name__ == '__main__':
    main()
