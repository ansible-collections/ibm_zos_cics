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
  size_value:
    description: Specifies the size of the local catalog dataset. Note, this is just the value; the unit is specified with space_type.
    type: int
    required: false
    default: 200
  size_unit:
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
    size_value: 500
    size_unit: "REC"
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
is_zos:
  description: True if the target environment is z/OS
  returned: always
  type: bool
result:
  description: The result of the CICS programs run during the module execution.
  type: dict
  returned: success
  contains:
    msg:
      description: The string message returned by the CICS program.
      type: str
      returned: always
    rc:
      description: The return code of the CICS program.
      type: int
      returned: always
    success:
      description: True if the CICS program was successful
      type: bool
      returned: always
"""


from typing import Dict
from ansible.module_utils.basic import AnsibleModule
import traceback

ZOS_CORE_IMP_ERR = None
try:
    from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.dd_statement import StdoutDefinition, DatasetDefinition, DDStatement
    from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.zos_mvs_raw import MVSCmd
    from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.better_arg_parser import BetterArgParser
    from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.system import is_zos
    from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.mvs_cmd import idcams
except ImportError:
    ZOS_CORE_IMP_ERR = traceback.format_exc()

ZOS_CICS_IMP_ERR = None
try:
    from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.dataset_utils import (
        LocalCatalog, CatalogResponse, CatalogSize, update_catalog_props, get_idcams_create_cmd)
except ImportError:
    ZOS_CICS_IMP_ERR = traceback.format_exc()


LOCAL_CATALOG_DATASET_ATTRIBUTE = "location"
CATALOG_SDFHLOAD_ATTRIBUTE = "sdfhload"
CATALOG_TARGET_STATE_ATTRIBUTE = "state"

CATALOG_PRIMARY_SPACE_ATTRIBUTE = "size_value"
CATALOG_PRIMARY_SPACE_VALUE_DEFAULT = "200"

CATALOG_SPACE_UNIT_ATTRIBUTE = "size_unit"
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
        self.validate_parameters()

    def _fail(self, msg):  # type: (str) -> None
        self.result['failed'] = True
        self._module.fail_json(msg=msg, **self.result)

    def _exit(self):
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
            size_value=dict(
                arg_type='int',
                default=CATALOG_PRIMARY_SPACE_VALUE_DEFAULT,
            ),
            size_unit=dict(
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

        size = CatalogSize(unit=result.get(CATALOG_SPACE_UNIT_ATTRIBUTE),
                           primary=result.get(CATALOG_PRIMARY_SPACE_ATTRIBUTE),
                           secondary=CATALOG_SECONDARY_SPACE_VALUE_DEFAULT,
                           record_count=CATALOG_RECORD_COUNT_DEFAULT,
                           record_size=CATALOG_RECORD_SIZE_DEFAULT,
                           control_interval_size=CATALOG_CONTROL_INTERVAL_SIZE_DEFAULT)

        self.starting_catalog = LocalCatalog(size=size,
                                             name=result.get(LOCAL_CATALOG_DATASET_ATTRIBUTE),
                                             sdfhload=result.get(CATALOG_SDFHLOAD_ATTRIBUTE),
                                             state=result.get(CATALOG_TARGET_STATE_ATTRIBUTE),
                                             exists=False,
                                             vsam=False)

    def create_local_catalog_dataset(self):
        create_cmd = get_idcams_create_cmd(self.starting_catalog)
        rc, stdout, stderr = idcams(cmd=create_cmd, authorized=True)
        if rc != 0:
            return CatalogResponse(success=False, rc=rc, msg=stdout)

        self.result['changed'] = True
        self.end_catalog = self.starting_catalog
        self.end_catalog = update_catalog_props(self.end_catalog)

    def run_dfhccutl(self, cmd):  # type: (str) -> CatalogResponse
        self.end_catalog = self.starting_catalog
        response = MVSCmd.execute(
            pgm="DFHCCUTL",
            dds=self.get_ccmutl_dds(catalog=self.end_catalog, cmd=cmd),
            verbose=True,
            debug=False)

        if response.rc != 0:
            self.result['DFHCCUTL_error'] = {
                'rc': response.rc,
                'stdout': response.stdout,
                'stderr': response.stderr,
            }
            self._fail("Error running DFHCCUTL")

        self.end_catalog = update_catalog_props(self.end_catalog)
        return CatalogResponse(success=True, rc=response.rc, msg=response.stdout)

    def delete_local_catalog(self):  # type: () -> CatalogResponse
        if not self.starting_catalog.exists:
            self._exit()

        delete_cmd = '''
        DELETE {0}
        '''.format(self.starting_catalog.name)

        rc, stdout, stderr = idcams(cmd=delete_cmd, authorized=True)

        if rc == 0:
            self.result['changed'] = True

        self.end_catalog = self.starting_catalog
        self.end_catalog = update_catalog_props(self.end_catalog)

        return CatalogResponse(success=(rc == 0), rc=rc, msg=stdout)

    def init_local_catalog(self):  # type: () -> CatalogResponse
        if self.starting_catalog.exists:
            self._exit()

        if not self.starting_catalog.exists:
            return self.create_local_catalog_dataset()

        return self.run_dfhccutl(cmd="*")

    def invalid_state(self):  # type: () -> None
        self.result['state_error'] = "{0} is not a valid state".format(self.local_catalog.state)
        self._module.fail_json(**self.result)

    def get_target_method(self, target):
        return {
            CATALOG_TARGET_STATE_ABSENT: self.delete_local_catalog,
            CATALOG_TARGET_STATE_INITIAL: self.init_local_catalog
        }.get(target, self.invalid_state)

    def get_ccmutl_dds(self, catalog, cmd):  # type: (LocalCatalog, str) -> list[DDStatement]
        return [
            DDStatement('steplib', DatasetDefinition(catalog.sdfhload)),
            DDStatement('sysprint', StdoutDefinition()),
            DDStatement('sysudump', StdoutDefinition()),
            DDStatement('dfhlcd', DatasetDefinition(dataset_name=catalog.name, disposition="SHR")),
        ]

    def main(self):
        self.result['is_zos'] = is_zos()

        self.starting_catalog = update_catalog_props(self.starting_catalog)

        if self.starting_catalog.exists and not self.starting_catalog.vsam:
            self._fail("Dataset {0} does not appear to be a KSDS".format(self.starting_catalog.name))

        if self.starting_catalog.exists and self.starting_catalog.state == CATALOG_TARGET_STATE_INITIAL:
            self._fail("Dataset {0} already exists".format(self.starting_catalog.name))

        if not self.starting_catalog.exists and self.starting_catalog.state == CATALOG_TARGET_STATE_ABSENT:
            self._fail("Dataset {0} not present".format(self.starting_catalog.name))

        result = self.get_target_method(self.starting_catalog.state)()
        self._exit()


def main():
    AnsibleLocalCatalogModule().main()


if __name__ == '__main__':
    main()
