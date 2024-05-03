#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023,2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: local_catalog
short_description: Create, remove, and manage the CICS local catalog
description:
  - Create, remove, and manage the L(local catalog,https://www.ibm.com/docs/en/cics-ts/latest?topic=catalogs-local-catalog)
    data set used by a CICS® region. CICS domains use the local catalog to save some of their information between CICS runs and
    to preserve this information across a cold start.
  - You can use this module when provisioning or de-provisioning a CICS region, or when managing
    the state of the local catalog during upgrades or restarts.
  - Use the O(state) option to specify the intended state for the local catalog.
    For example, use O(state=initial) to create and initialize a local catalog data set if it doesn't exist,
    or empty an existing local catalog of all records.
author: Enam Khan (@enam-khan)
version_added: 1.1.0-beta.2
seealso:
  - module: global_catalog
options:
  space_primary:
    description:
      - The size of the primary space allocated to the local catalog data set.
        Note that this is just the value; the unit is specified with O(space_type).
      - This option takes effect only when the local catalog data set is being created.
        If the local catalog data set already exists, the option has no effect.
    type: int
    required: false
    default: 200
  space_secondary:
    description:
      - The size of the secondary space allocated to the local catalog data set.
        Note that this is just the value; the unit is specified with O(space_type).
      - This option takes effect only when the local catalog data set is being created.
        If the local catalog data set already exists, the option has no effect.
    type: int
    required: false
    default: 5
  space_type:
    description:
      - The unit portion of the local catalog data set size. Note that this is
        just the unit; the value for the primary space is specified with O(space_primary) and
        the value for the secondary space is specified with O(space_secondary).
      - This option takes effect only when the local catalog data set is being created.
        If the local catalog data set already exists, the option has no effect.
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
      - If you want to use a data set that already exists, ensure that the data set is a local catalog data set.
    type: dict
    required: true
    suboptions:
      template:
        description:
          - The base location of the region data sets with a template.
        required: false
        type: str
      dfhlcd:
        description:
          - Overrides the templated location for the local catalog data set.
        required: false
        type: dict
        suboptions:
          dsn:
            description:
              - The data set name of the local catalog to override the template.
            type: str
            required: false
  cics_data_sets:
    description:
      - The name of the C(SDFHLOAD) library of the CICS installation, for example, C(CICSTS61.CICS.SDFHLOAD).
      - This module uses the C(DFHCCUTL) utility internally, which is found in the C(SDFHLOAD) library.
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
      - The intended state for the local catalog, which the module aims to achieve.
      - Specify V(absent) to remove the local catalog data set entirely, if it already exists.
      - Specify V(initial) to create the local catalog data set if it does not exist,
        or empty this existing local catalog of all records.
      - Specify V(warm) to retain an existing local catalog in its current state.
        The module verifies whether the specified data set exists and whether it contains any records.
        If both conditions are met, the module leaves the data set as is.
        If the data set does not exist or if it is empty, the operation fails.
    choices:
      - "initial"
      - "absent"
      - "warm"
    required: true
    type: str
'''


EXAMPLES = r"""
- name: Initialize a local catalog data set
  ibm.ibm_zos_cics.local_catalog:
    region_data_sets:
      template: "REGIONS.ABCD0001.<< data_set_name >>"
    cics_data_sets:
      template: "CICSTS61.CICS.<< lib_name >>"
    state: "initial"

- name: Initialize a large catalog data set
  ibm.ibm_zos_cics.local_catalog:
    region_data_sets:
      template: "REGIONS.ABCD0001.<< data_set_name >>"
    cics_data_sets:
      template: "CICSTS61.CICS.<< lib_name >>"
    space_primary: 500
    space_type: "REC"
    state: "initial"

- name: Delete a local catalog data set
  ibm.ibm_zos_cics.local_catalog:
    region_data_sets:
      template: "REGIONS.ABCD0001.<< data_set_name >>"
    cics_data_sets:
      template: "CICSTS61.CICS.<< lib_name >>"
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
    - The state of the local catalog data set before the Ansible task runs.
  returned: always
  type: dict
  contains:
    data_set_organization:
      description: The organization of the data set at the start of the Ansible task.
      returned: always
      type: str
      sample: "VSAM"
    exists:
      description: True if the specified local catalog data set exists.
      type: bool
      returned: always
end_state:
  description: The state of the local catalog data set at the end of the Ansible task.
  returned: always
  type: dict
  contains:
    data_set_organization:
      description: The organization of the data set at the end of the Ansible task.
      returned: always
      type: str
      sample: "VSAM"
    exists:
      description: True if the specified local catalog data set exists.
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

from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils._response import MVSExecutionException
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils._data_set_utils import (
    _build_idcams_define_cmd
)
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils._data_set import (
    CICS_DATA_SETS,
    RECORDS,
    REGION_DATA_SETS,
    SPACE_PRIMARY,
    SPACE_SECONDARY,
    SPACE_TYPE,
    ABSENT,
    INITIAL,
    WARM,
    DataSet
)
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils._local_catalog import (
    _get_idcams_cmd_lcd,
    _run_dfhccutl
)


DSN = "dfhlcd"
SPACE_PRIMARY_DEFAULT = 200
SPACE_SECONDARY_DEFAULT = 5


class AnsibleLocalCatalogModule(DataSet):
    def __init__(self):
        super(AnsibleLocalCatalogModule, self).__init__(SPACE_PRIMARY_DEFAULT, SPACE_SECONDARY_DEFAULT)
        self.name = self.region_param[DSN]["dsn"].upper()
        self.expected_data_set_organization = "VSAM"

    def _get_arg_spec(self):  # type: () -> dict
        arg_spec = super(AnsibleLocalCatalogModule, self)._get_arg_spec()

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

        return arg_spec

    def get_arg_defs(self):  # type: () -> dict
        defs = super().get_arg_defs()
        defs[REGION_DATA_SETS]["options"][DSN]["options"]["dsn"].update({
            "arg_type": "data_set_base"
        })
        defs[REGION_DATA_SETS]["options"][DSN]["options"]["dsn"].pop("type")
        return defs

    def execute_target_state(self):   # type: () -> None
        if self.target_state == ABSENT:
            self.delete_data_set()
        elif self.target_state == INITIAL:
            self.init_data_set()
        elif self.target_state == WARM:
            self.warm_with_records()
        else:
            self.invalid_target_state()

    def create_data_set(self):  # type: () -> None
        create_cmd = _build_idcams_define_cmd(_get_idcams_cmd_lcd(self.get_data_set()))
        super().build_vsam_data_set(create_cmd)

    def init_data_set(self):  # type: () -> None
        super().init_data_set()
        try:
            ccutl_executions = _run_dfhccutl(self.get_data_set())
            self.executions.extend(ccutl_executions)
        except MVSExecutionException as e:
            self.executions.extend(e.executions)
            self._fail(e.message)


def main():
    AnsibleLocalCatalogModule().main()


if __name__ == '__main__':
    main()
