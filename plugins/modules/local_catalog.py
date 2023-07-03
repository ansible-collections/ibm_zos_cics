#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: local_catalog
short_description: Create and initialize CICS® local catalog.
description: Create, update, and remove a CICS® local catalog dataset to be used by a CICS® region, achieved by running the IDCAMS and DFHCCUTL programs.
author: Enam Khan (@enam-khan)
version_added: 1.1.0-beta.1
options:
  space_primary:
    description: Specifies the size of the local catalog dataset. Note, this is just the value; the unit is specified with space_type.
    type: int
    required: false
    default: 200
  space_type:
    description: Specifies the unit to be used for the local catalog size. Note, this is just the unit; the value is specified with space_primary.
    required: false
    type: str
    choices:
      - M
      - K
      - REC
      - CYL
      - TRK
    default: REC
  location:
    description: The name of the dataset to be used as the local catalog dataset.
    type: str
    required: true
  sdfhload:
    description: The location of SDFHLOAD for the CICS install to be used to create the local catalog.
    type: str
    required: true
  state:
    description: The state the local catalog will end up in after the task has run.
    choices:
      - "initial"
      - "absent"
    required: true
    type: str
'''


EXAMPLES = r"""
- name: Initialize a local catalog
  ibm.ibm_zos_cics.local_catalog:
    location: "CICS.INSTALL.REG01.DFHLCD"
    sdfhload: "CTS560.CICS730.SDFHLOAD"
    state: "initial"

- name: Initialize a large catalog
  ibm.ibm_zos_cics.local_catalog:
    location: "CICS.INSTALL.REG01.DFHLCD"
    sdfhload: "CTS560.CICS730.SDFHLOAD"
    space_primary: 500
    space_type: "REC"
    state: "initial"

- name: Delete local catalog
  ibm.ibm_zos_cics.local_catalog:
    location: "CICS.INSTALL.REG01.DFHLCD"
    sdfhload: "CTS560.CICS730.SDFHLOAD"
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
    - The state of the local catalog before the task
  returned: always
  type: dict
  contains:
    vsam:
      description: True if the data set is of type vsam
      returned: always
      type: bool
    exists:
      description: True if the local catalog dataset exists
      type: bool
      returned: always
end_state:
  description: The state of the local catalog at the end of the task.
  returned: always
  type: dict
  contains:
    vsam:
      description: True if the data set is of type vsam
      returned: always
      type: bool
    exists:
      description: True if the local catalog dataset exists
      type: bool
      returned: always
executions:
  description: A list of program executions performed during the task
  returned: always
  type: list
  elements: dict
  contains:
    name:
      description: Human readable name for the execution
      type: str
      returned: always
    rc:
      description: The return code for that program execution
      type: int
      returned: always
    stdout:
      description: The stdout returned from the program execution
      type: str
      returned: always
    stderr:
      description: The stderr returned from the program execution
      type: str
      returned: always
"""


from typing import Dict
from ansible.module_utils.basic import AnsibleModule
import traceback

ZOS_CORE_IMP_ERR = None
try:
    from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.better_arg_parser import BetterArgParser
except ImportError:
    ZOS_CORE_IMP_ERR = traceback.format_exc()

ZOS_CICS_IMP_ERR = None
try:
    from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.dataset_utils import (
        _dataset_size, _get_idcams_create_cmd, _run_idcams, _run_listds)
    from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.local_catalog import (
        _local_catalog, _run_dfhccutl)
except ImportError:
    ZOS_CICS_IMP_ERR = traceback.format_exc()


LOCAL_CATALOG_DATASET_ATTRIBUTE = "location"
CATALOG_SDFHLOAD_ATTRIBUTE = "sdfhload"
CATALOG_TARGET_STATE_ATTRIBUTE = "state"

CATALOG_PRIMARY_SPACE_ATTRIBUTE = "space_primary"
CATALOG_PRIMARY_SPACE_VALUE_DEFAULT = "200"

CATALOG_SPACE_UNIT_ATTRIBUTE = "space_type"
CATALOG_SPACE_UNIT_DEFAULT = "REC"
CATALOG_SPACE_UNIT_OPTIONS = ["K", "M", "REC", "CYL", "TRK"]

CATALOG_SECONDARY_SPACE_VALUE_DEFAULT = "5"

CATALOG_TARGET_STATE_ABSENT = 'absent'
CATALOG_TARGET_STATE_INITIAL = 'initial'
CATALOG_TARGET_STATE_OPTIONS = [CATALOG_TARGET_STATE_ABSENT,
                                CATALOG_TARGET_STATE_INITIAL]

CATALOG_RECORD_COUNT_DEFAULT = 70
CATALOG_RECORD_SIZE_DEFAULT = 2041
CATALOG_CONTROL_INTERVAL_SIZE_DEFAULT = 2048


class AnsibleLocalCatalogModule(object):
    def __init__(self):
        self._module = AnsibleModule(
            argument_spec=self.init_argument_spec(),
        )
        self.result = {}
        self.result['changed'] = False
        self.result['failed'] = False
        self.result['executions'] = []
        self.executions = []
        self.validate_parameters()

    def _fail(self, msg):  # type: (str) -> None
        self.result['failed'] = True
        self.result['executions'] = self.executions
        self._module.fail_json(msg=msg, **self.result)

    def _exit(self):
        self.result['executions'] = self.executions
        self._module.exit_json(**self.result)

    def init_argument_spec(self):  # type: () -> Dict
        return {
            CATALOG_PRIMARY_SPACE_ATTRIBUTE: {
                'required': False,
                'type': 'int',
                'default': CATALOG_PRIMARY_SPACE_VALUE_DEFAULT,
            },
            CATALOG_SPACE_UNIT_ATTRIBUTE: {
                'required': False,
                'type': 'str',
                'choices': CATALOG_SPACE_UNIT_OPTIONS,
                'default': CATALOG_SPACE_UNIT_DEFAULT,
            },
            LOCAL_CATALOG_DATASET_ATTRIBUTE: {
                'required': True,
                'type': 'str',
            },
            CATALOG_SDFHLOAD_ATTRIBUTE: {
                'required': True,
                'type': 'str',
            },
            CATALOG_TARGET_STATE_ATTRIBUTE: {
                'required': True,
                'type': 'str',
                'choices': CATALOG_TARGET_STATE_OPTIONS,
            }
        }

    def validate_parameters(self):
        arg_defs = dict(
            space_primary=dict(
                arg_type='int',
                default=CATALOG_PRIMARY_SPACE_VALUE_DEFAULT,
            ),
            space_type=dict(
                arg_type='str',
                choices=CATALOG_SPACE_UNIT_OPTIONS,
                default=CATALOG_SPACE_UNIT_DEFAULT,
            ),
            location=dict(
                arg_type='data_set_base',
                required=True,
            ),
            sdfhload=dict(
                arg_type='data_set_base',
                required=True,
            ),
            state=dict(
                arg_type='str',
                choices=CATALOG_TARGET_STATE_OPTIONS,
                required=True,
            ),
        )
        parser = BetterArgParser(arg_defs)

        result = parser.parse_args({
            CATALOG_PRIMARY_SPACE_ATTRIBUTE: self._module.params.get(CATALOG_PRIMARY_SPACE_ATTRIBUTE),
            CATALOG_SPACE_UNIT_ATTRIBUTE: self._module.params.get(CATALOG_SPACE_UNIT_ATTRIBUTE),
            LOCAL_CATALOG_DATASET_ATTRIBUTE: self._module.params.get(LOCAL_CATALOG_DATASET_ATTRIBUTE),
            CATALOG_SDFHLOAD_ATTRIBUTE: self._module.params.get(CATALOG_SDFHLOAD_ATTRIBUTE),
            CATALOG_TARGET_STATE_ATTRIBUTE: self._module.params.get(CATALOG_TARGET_STATE_ATTRIBUTE)
        })

        size = _dataset_size(
            unit=result.get(CATALOG_SPACE_UNIT_ATTRIBUTE),
            primary=result.get(CATALOG_PRIMARY_SPACE_ATTRIBUTE),
            secondary=CATALOG_SECONDARY_SPACE_VALUE_DEFAULT,
            record_count=CATALOG_RECORD_COUNT_DEFAULT,
            record_size=CATALOG_RECORD_SIZE_DEFAULT,
            control_interval_size=CATALOG_CONTROL_INTERVAL_SIZE_DEFAULT)

        self.starting_catalog = _local_catalog(
            size=size,
            name=result.get(LOCAL_CATALOG_DATASET_ATTRIBUTE).upper(),
            sdfhload=result.get(CATALOG_SDFHLOAD_ATTRIBUTE),
            state=result.get(CATALOG_TARGET_STATE_ATTRIBUTE),
            exists=False,
            vsam=False)

    def create_local_catalog_dataset(self):
        create_cmd = _get_idcams_create_cmd(self.starting_catalog)

        idcams_executions = _run_idcams(
            cmd=create_cmd,
            name="Create local catalog dataset",
            location=self.starting_catalog["name"],
            delete=False)
        self.executions = self.executions + idcams_executions

        self.result['changed'] = True

    def delete_local_catalog(self):
        if not self.starting_catalog["exists"]:
            self.result['end_state'] = {
                "exists": self.starting_catalog["exists"],
                "vsam": self.starting_catalog["vsam"]
            }
            self._exit()

        delete_cmd = '''
        DELETE {0}
        '''.format(self.starting_catalog["name"])

        idcams_executions = _run_idcams(
            cmd=delete_cmd,
            name="Removing local catalog dataset",
            location=self.starting_catalog["name"],
            delete=True)
        self.executions = self.executions + idcams_executions
        self.result['changed'] = True

    def init_local_catalog(self):
        if self.starting_catalog["exists"]:
            self.result['end_state'] = {
                "exists": self.starting_catalog["exists"],
                "vsam": self.starting_catalog["vsam"]
            }
            self._exit()

        if not self.starting_catalog["exists"]:
            return self.create_local_catalog_dataset()

        return _run_dfhccutl(self.starting_catalog, cmd="*")

    def invalid_state(self):  # type: () -> None
        self._fail("{0} is not a valid target state".format(
            self.local_catalog["state"]))

    def get_target_method(self, target):
        return {
            CATALOG_TARGET_STATE_ABSENT: self.delete_local_catalog,
            CATALOG_TARGET_STATE_INITIAL: self.init_local_catalog
        }.get(target, self.invalid_state)

    def get_catalog_state(self, catalog):
        listds_executions, ds_status = _run_listds(catalog["name"])

        catalog["exists"] = ds_status['exists']
        catalog["vsam"] = ds_status['vsam']

        self.executions = self.executions + listds_executions

        return catalog

    def main(self):
        self.starting_catalog = self.get_catalog_state(self.starting_catalog)

        self.result['start_state'] = {
            "exists": self.starting_catalog["exists"],
            "vsam": self.starting_catalog["vsam"]
        }

        if self.starting_catalog["exists"] and not self.starting_catalog["vsam"]:
            self._fail(
                "Dataset {0} does not appear to be a KSDS".format(
                    self.starting_catalog["name"]))

        self.get_target_method(self.starting_catalog["state"])()

        self.end_catalog = self.get_catalog_state(self.starting_catalog)

        self.result['end_state'] = {
            "exists": self.end_catalog["exists"],
            "vsam": self.end_catalog["vsam"]
        }

        self._exit()


def main():
    AnsibleLocalCatalogModule().main()


if __name__ == '__main__':
    main()
