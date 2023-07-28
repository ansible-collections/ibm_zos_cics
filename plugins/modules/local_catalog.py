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
    data set used by a CICS® region.
  - Useful when provisioning or de-provisioning a CICS region, or when managing
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
      - The size of the local catalog data set's primary space allocation.
        Note, this is just the value; the unit is specified with O(space_type).
      - This option only takes effect when the local catalog is being created.
        If it already exists, it has no effect.
      - The local catalog data set's secondary space allocation is set to 1.
    type: int
    required: false
    default: 200
  space_type:
    description:
      - The unit portion of the local catalog data set size. Note, this is
        just the unit; the value is specified with O(space_primary).
      - This option only takes effect when the local catalog is being created.
        If it already exists, it has no effect.
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
  location:
    description:
      - The name of the local catalog data set, e.g.
        C(REGIONS.ABCD0001.DFHLCD).
      - If it already exists, this data set must be cataloged.
    type: str
    required: true
  sdfhload:
    description:
      - The name of the C(SDFHLOAD) data set, e.g. C(CICSTS61.CICS.SDFHLOAD).
      - This module uses the C(DFHCCUTL) utility internally, which is found in
        the C(SDFHLOAD) data set in the CICS installation.
    type: str
    required: true
  state:
    description:
      - The desired state for the local catalog, which the module will aim to
        achieve.
      - V(absent) will remove the local catalog data set entirely, if it
        already exists.
      - V(initial) will create the local catalog data set if it does not
        already exist, and empty it of all existing records.
      - V(warm) will retain an existing local catalog in its current state.
    choices:
      - "initial"
      - "absent"
    required: true
    type: str
'''


EXAMPLES = r"""
- name: Initialize a local catalog
  ibm.ibm_zos_cics.local_catalog:
    location: "REGIONS.ABCD0001.DFHLCD"
    sdfhload: "CICSTS61.CICS.SDFHLOAD"
    state: "initial"

- name: Initialize a large catalog
  ibm.ibm_zos_cics.local_catalog:
    location: "REGIONS.ABCD0001.DFHLCD"
    sdfhload: "CICSTS61.CICS.SDFHLOAD"
    space_primary: 500
    space_type: "REC"
    state: "initial"

- name: Delete local catalog
  ibm.ibm_zos_cics.local_catalog:
    location: "REGIONS.ABCD0001.DFHLCD"
    sdfhload: "CICSTS61.CICS.SDFHLOAD"
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
    - The state of the local catalog before the task runs.
  returned: always
  type: dict
  contains:
    vsam:
      description: True if the data set is a VSAM data set.
      returned: always
      type: bool
    exists:
      description: True if the local catalog data set exists.
      type: bool
      returned: always
end_state:
  description: The state of the local catalog at the end of the task.
  returned: always
  type: dict
  contains:
    vsam:
      description: True if the data set is a VSAM data set.
      returned: always
      type: bool
    exists:
      description: True if the local catalog data set exists.
      type: bool
      returned: always
executions:
  description: A list of program executions performed during the task.
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
        _dataset_size, _run_idcams, _run_listds)
    from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.local_catalog import (
        _local_catalog, _run_dfhccutl, _get_idcams_cmd_lcd)
    from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import catalog_constants as constants
except ImportError:
    ZOS_CICS_IMP_ERR = traceback.format_exc()


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
            constants.CATALOG_PRIMARY_SPACE_VALUE_ALIAS: {
                'required': False,
                'type': 'int',
                'default': constants.LOCAL_CATALOG_PRIMARY_SPACE_VALUE_DEFAULT,
            },
            constants.CATALOG_PRIMARY_SPACE_UNIT_ALIAS: {
                'required': False,
                'type': 'str',
                'choices': constants.CATALOG_SPACE_UNIT_OPTIONS,
                'default': constants.LOCAL_CATALOG_SPACE_UNIT_DEFAULT,
            },
            constants.CATALOG_DATASET_ALIAS: {
                'required': True,
                'type': 'str',
            },
            constants.CATALOG_SDFHLOAD_ALIAS: {
                'required': True,
                'type': 'str',
            },
            constants.CATALOG_TARGET_STATE_ALIAS: {
                'required': True,
                'type': 'str',
                'choices': constants.LOCAL_CATALOG_TARGET_STATE_OPTIONS,
            }
        }

    def validate_parameters(self):
        arg_defs = dict(
            space_primary=dict(
                arg_type='int',
                default=constants.LOCAL_CATALOG_PRIMARY_SPACE_VALUE_DEFAULT,
            ),
            space_type=dict(
                arg_type='str',
                choices=constants.CATALOG_SPACE_UNIT_OPTIONS,
                default=constants.LOCAL_CATALOG_SPACE_UNIT_DEFAULT,
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
                choices=constants.LOCAL_CATALOG_TARGET_STATE_OPTIONS,
                required=True,
            ),
        )
        parser = BetterArgParser(arg_defs)

        result = parser.parse_args({
            constants.CATALOG_PRIMARY_SPACE_VALUE_ALIAS: self._module.params.get(constants.CATALOG_PRIMARY_SPACE_VALUE_ALIAS),
            constants.CATALOG_PRIMARY_SPACE_UNIT_ALIAS: self._module.params.get(constants.CATALOG_PRIMARY_SPACE_UNIT_ALIAS),
            constants.CATALOG_DATASET_ALIAS: self._module.params.get(constants.CATALOG_DATASET_ALIAS),
            constants.CATALOG_SDFHLOAD_ALIAS: self._module.params.get(constants.CATALOG_SDFHLOAD_ALIAS),
            constants.CATALOG_TARGET_STATE_ALIAS: self._module.params.get(constants.CATALOG_TARGET_STATE_ALIAS)
        })

        size = _dataset_size(
            unit=result.get(constants.CATALOG_PRIMARY_SPACE_UNIT_ALIAS),
            primary=result.get(constants.CATALOG_PRIMARY_SPACE_VALUE_ALIAS),
            secondary=constants.LOCAL_CATALOG_SECONDARY_SPACE_VALUE_DEFAULT,
            record_count=constants.LOCAL_CATALOG_RECORD_COUNT_DEFAULT,
            record_size=constants.LOCAL_CATALOG_RECORD_SIZE_DEFAULT,
            control_interval_size=constants.LOCAL_CATALOG_CONTROL_INTERVAL_SIZE_DEFAULT)

        self.starting_catalog = _local_catalog(
            size=size,
            name=result.get(constants.CATALOG_DATASET_ALIAS).upper(),
            sdfhload=result.get(constants.CATALOG_SDFHLOAD_ALIAS),
            state=result.get(constants.CATALOG_TARGET_STATE_ALIAS),
            exists=False,
            vsam=False)

    def create_local_catalog_dataset(self):
        create_cmd = _get_idcams_cmd_lcd(self.starting_catalog)

        idcams_executions = _run_idcams(
            cmd=create_cmd,
            name="Create local catalog data set",
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
            name="Removing local catalog data set",
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
            self.create_local_catalog_dataset()

        ccutl_executions = _run_dfhccutl(self.starting_catalog)
        self.executions = self.executions + ccutl_executions

    def invalid_state(self):  # type: () -> None
        self._fail("{0} is not a valid target state.".format(
            self.local_catalog["state"]))

    def get_target_method(self, target):
        return {
            constants.LOCAL_CATALOG_TARGET_STATE_ABSENT: self.delete_local_catalog,
            constants.LOCAL_CATALOG_TARGET_STATE_INITIAL: self.init_local_catalog
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
                "Data set {0} does not appear to be a KSDS.".format(
                    self.starting_catalog["name"]))

        self.get_target_method(self.starting_catalog["state"])()

        self.end_state = self.get_catalog_state(self.starting_catalog)

        self.result['end_state'] = {
            "exists": self.end_state["exists"],
            "vsam": self.end_state["vsam"]
        }

        self._exit()


def main():
    AnsibleLocalCatalogModule().main()


if __name__ == '__main__':
    main()
