#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
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
  - Use the O(state) option to specify the intended state for the local
    catalog. For example, O(state=initial) will create and initialize a local
    catalog data set if it doesn't yet exist, or it will take an existing
    local catalog and empty it of all records.
author: Enam Khan (@enam-khan)
version_added: 1.1.0-beta.2
seealso:
  - module: global_catalog
options:
  space_primary:
    description:
      - The size of the primary space allocated to the local catalog data set.
        Note that this is just the value; the unit is specified with O(space_type).
      - This option takes effect only when the local catalog is being created.
        If the local catalog already exists, the option has no effect.
    type: int
    required: false
    default: 200
  space_secondary:
    description:
      - The size of the secondary space allocated to the local catalog data set.
        Note that this is just the value; the unit is specified with O(space_type).
      - This option takes effect only when the local catalog is being created.
        If the local catalog already exists, the option has no effect.
    type: int
    required: false
    default: 5
  space_type:
    description:
      - The unit portion of the local catalog data set size. Note that this is
        just the unit; the value is specified with O(space_primary).
      - This option takes effect only when the local catalog is being created.
        If the local catalog already exists, the option has no effect.
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
  region_data_sets:
    description:
      - The location of the region data sets to be created using a template, for example,
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
          - The location of the  C(SDFHLOAD) library to override the template.
        type: str
        required: false
  state:
    description:
      - The intended state for the local catalog, which the module will aim to
        achieve.
      - V(absent) will remove the local catalog data set entirely, if it
        already exists.
      - V(initial) will create the local catalog data set if it does not
        already exist, and empty it of all existing records.
      - V(warm) will retain an existing local catalog in its current state.
    choices:
      - "initial"
      - "absent"
      - "warm"
    required: true
    type: str
'''


EXAMPLES = r"""
- name: Initialize a local catalog
  ibm.ibm_zos_cics.local_catalog:
    region_data_sets:
      template: "REGIONS.ABCD0001.<< data_set_name >>"
    cics_data_sets:
      template: "CICSTS61.CICS.<< lib_name >>"
    state: "initial"

- name: Initialize a large catalog
  ibm.ibm_zos_cics.local_catalog:
    region_data_sets:
      template: "REGIONS.ABCD0001.<< data_set_name >>"
    cics_data_sets:
      template: "CICSTS61.CICS.<< lib_name >>"
    space_primary: 500
    space_type: "REC"
    state: "initial"

- name: Delete local catalog
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
  description: True if the query job failed, otherwise False.
  returned: always
  type: bool
start_state:
  description:
    - The state of the local catalog before the Ansible task runs.
  returned: always
  type: dict
  contains:
    data_set_organization:
      description: The organization of the data set at the start of the Ansible task.
      returned: always
      type: str
      sample: "VSAM"
    exists:
      description: True if the local catalog data set exists.
      type: bool
      returned: always
end_state:
  description: The state of the local catalog at the end of the Ansible task.
  returned: always
  type: dict
  contains:
    data_set_organization:
      description: The organization of the data set at the end of the Ansible task.
      returned: always
      type: str
      sample: "VSAM"
    exists:
      description: True if the local catalog data set exists.
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
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.data_set_utils import (
    _build_idcams_define_cmd
)
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.data_set import (
    CICS_DATA_SETS,
    RECORDS,
    REGION_DATA_SETS,
    SPACE_PRIMARY,
    SPACE_SECONDARY,
    SPACE_TYPE,
    DataSet
)
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.local_catalog import (
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
