#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: global_catalog
short_description: Create, remove, and manage the CICS global catalog
description:
  - Create, remove, and manage the L(global catalog,https://www.ibm.com/docs/en/cics-ts/latest?topic=catalogs-global-catalog)
    data set used by a CICS® region.
  - Useful when provisioning or de-provisioning a CICS region, or when managing
    the state of the global catalog during upgrades or restarts.
  - Use the O(state) option to specify the intended state for the global
    catalog. For example, O(state=initial) will create and initialize a global
    catalog data set if it doesn't yet exist, or it will take an existing
    global catalog and set its autostart override record to C(AUTOINIT). In
    either case, a CICS region using this global catalog and the
    C(START=AUTO) system initialization parameter will perform an initial start.
author: Andrew Twydell (@AndrewTwydell)
version_added: 1.1.0-beta.1
seealso:
  - module: local_catalog
options:
  space_primary:
    description:
      - The size of the global catalog data set's primary space allocation.
        Note, this is just the value; the unit is specified with O(space_type).
      - This option only takes effect when the global catalog is being created.
        If it already exists, it has no effect.
      - The global catalog data set's secondary space allocation is set to 1.
    type: int
    required: false
    default: 5
  space_type:
    description:
      - The unit portion of the global catalog data set size. Note, this is
        just the unit; the value is specified with O(space_primary).
      - This option only takes effect when the global catalog is being created.
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
    default: M
  region_data_sets:
    description:
      - The location of the region's data sets using a template, e.g.
        C(REGIONS.ABCD0001.<< data_set_name >>).
      - If it already exists, this data set must be cataloged.
    type: dict
    required: true
    suboptions:
      template:
        description:
          - The base location of the region's data sets with a template.
        required: false
        type: str
      dfhgcd:
        description:
          - Overrides the templated location for the global catalog data set.
        required: false
        type: dict
        suboptions:
          dsn:
            description:
              - Data set name of the global catalog to override the template.
            type: str
            required: false
  cics_data_sets:
    description:
      - The name of the C(SDFHLOAD) data set, e.g. C(CICSTS61.CICS.SDFHLOAD).
      - This module uses the C(DFHRMUTL) utility internally, which is found in
        the C(SDFHLOAD) data set in the CICS installation.
    type: dict
    required: true
    suboptions:
      template:
        description:
          - Templated location of the cics install data sets.
        required: false
        type: str
      sdfhload:
        description:
          - Location of the sdfhload data set.
          - Overrides the templated location for sdfhload.
        type: str
        required: false
  state:
    description:
      - The desired state for the global catalog, which the module will aim to
        achieve.
      - V(absent) will remove the global catalog data set entirely, if it
        already exists.
      - V(initial) will set the autostart override record to C(AUTOINIT),
        creating the global catalog data set if it does not already exist.
      - V(cold) will set an existing global catalog's autostart override record
        to C(AUTOCOLD).
      - V(warm) will set an existing global catalog's autostart override record
        to C(AUTOASIS), undoing any previous setting of C(AUTOINIT) or
        C(AUTOCOLD).
    choices:
      - "absent"
      - "initial"
      - "cold"
      - "warm"
    required: true
    type: str
'''


EXAMPLES = r"""
- name: Initialize a global catalog
  ibm.ibm_zos_cics.global_catalog:
    region_data_sets:
      template: "REGIONS.ABCD0001.<< data_set_name >>"
    cics_data_sets:
      template: "CICSTS61.CICS.<< lib_name >>"
    state: "initial"

- name: Initialize a large catalog
  ibm.ibm_zos_cics.global_catalog:
    region_data_sets:
      template: "REGIONS.ABCD0001.<< data_set_name >>"
    cics_data_sets:
      template: "CICSTS61.CICS.<< lib_name >>"
    space_primary: 100
    space_type: "M"
    state: "initial"

- name: Set autostart override record to AUTOASIS
  ibm.ibm_zos_cics.global_catalog:
    region_data_sets:
      template: "REGIONS.ABCD0001.<< data_set_name >>"
    cics_data_sets:
      template: "CICSTS61.CICS.<< lib_name >>"
    state: "warm"

- name: Set autostart override record to AUTOCOLD
  ibm.ibm_zos_cics.global_catalog:
    region_data_sets:
      template: "REGIONS.ABCD0001.<< data_set_name >>"
    cics_data_sets:
      template: "CICSTS61.CICS.<< lib_name >>"
    state: "cold"

- name: Delete global catalog
  ibm.ibm_zos_cics.global_catalog:
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
    - The state of the global catalog before the task runs.
  returned: always
  type: dict
  contains:
    autostart_override:
      description: The current autostart override record.
      returned: always
      type: str
    next_start:
      description: The next start type listed in the global catalog.
      returned: always
      type: str
    exists:
      description: True if the global catalog data set exists.
      type: bool
      returned: always
end_state:
  description: The state of the global catalog at the end of the task.
  returned: always
  type: dict
  contains:
    autostart_override:
      description: The current autostart override record.
      returned: always
      type: str
    next_start:
      description: The next start type listed in the global catalog
      returned: always
      type: str
    exists:
      description: True if the global catalog data set exists.
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

DDStatement = None
ZOS_CORE_IMP_ERR = None
try:
    from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.better_arg_parser import BetterArgParser
except ImportError:
    ZOS_CORE_IMP_ERR = traceback.format_exc()

ZOS_CICS_IMP_ERR = None
try:
    from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.dataset_utils import (
        _dataset_size, _run_listds, _run_idcams, _data_set)
    from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.global_catalog import (
        _run_dfhrmutl, _get_idcams_cmd_gcd)
    from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.global_catalog import _global_catalog_constants as gc_constants
    from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.dataset_utils import _dataset_constants as ds_constants
except ImportError:
    ZOS_CICS_IMP_ERR = traceback.format_exc()


class AnsibleGlobalCatalogModule(object):

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

    def _exit(self):  # type: () -> None
        self.result['executions'] = self.executions
        self._module.exit_json(**self.result)

    def init_argument_spec(self):  # type: () -> Dict
        return {
            ds_constants["REGION_DATA_SETS_ALIAS"]: {
                'type': 'dict',
                'required': True,
                'options': {
                    'template': {
                        'type': 'str',
                        'required': False,
                    },
                    'dfhgcd': {
                        'type': 'dict',
                        'required': False,
                        'options': {
                            'dsn': {
                                'type': 'str',
                                'required': False,
                            },
                        },
                    },
                },
            },
            ds_constants["CICS_DATA_SETS_ALIAS"]: {
                'type': 'dict',
                'required': True,
                'options': {
                    'template': {
                        'type': 'str',
                        'required': False,
                    },
                    'sdfhload': {
                        'type': 'str',
                        'required': False,
                    },
                },
            },
            ds_constants["PRIMARY_SPACE_VALUE_ALIAS"]: {
                'required': False,
                'type': 'int',
                'default': gc_constants["PRIMARY_SPACE_VALUE_DEFAULT"],
            },
            ds_constants["PRIMARY_SPACE_UNIT_ALIAS"]: {
                'required': False,
                'type': 'str',
                'choices': ds_constants["SPACE_UNIT_OPTIONS"],
                'default': gc_constants["SPACE_UNIT_DEFAULT"],
            },
            ds_constants["TARGET_STATE_ALIAS"]: {
                'required': True,
                'type': 'str',
                'choices': gc_constants["TARGET_STATE_OPTIONS"],
            },
        }

    def validate_parameters(self):  # type: () -> None
        arg_defs = {
            ds_constants["REGION_DATA_SETS_ALIAS"]: {
                "arg_type": "dict",
                "required": True,
                "options": {
                    "template": {
                        "arg_type": "str",
                        "required": False,
                    },
                    "dfhgcd": {
                        "arg_type": "dict",
                        "required": False,
                        "options": {
                            "dsn": {
                                "arg_type": "data_set_base",
                                "required": False,
                            },
                        },
                    },
                },
            },
            ds_constants["CICS_DATA_SETS_ALIAS"]: {
                "arg_type": "dict",
                "required": True,
                "options": {
                    "template": {
                        "arg_type": "str",
                        "required": False,
                    },
                    "sdfhload": {
                        "arg_type": "data_set_base",
                        "required": False,
                    },
                },
            },
            ds_constants["PRIMARY_SPACE_VALUE_ALIAS"]: {
                "arg_type": 'int',
                "default": gc_constants["PRIMARY_SPACE_VALUE_DEFAULT"],
            },
            ds_constants["PRIMARY_SPACE_UNIT_ALIAS"]: {
                "arg_type": 'str',
                "choices": ds_constants["SPACE_UNIT_OPTIONS"],
                "default": gc_constants["SPACE_UNIT_DEFAULT"],
            },
            ds_constants["TARGET_STATE_ALIAS"]: {
                "arg_type": 'str',
                "choices": gc_constants["TARGET_STATE_OPTIONS"],
                "required": True,
            },
        }
        result = BetterArgParser(arg_defs).parse_args({
            ds_constants["REGION_DATA_SETS_ALIAS"]: self._module.params.get(ds_constants["REGION_DATA_SETS_ALIAS"]),
            ds_constants["CICS_DATA_SETS_ALIAS"]: self._module.params.get(ds_constants["CICS_DATA_SETS_ALIAS"]),
            ds_constants["PRIMARY_SPACE_VALUE_ALIAS"]: self._module.params.get(ds_constants["PRIMARY_SPACE_VALUE_ALIAS"]),
            ds_constants["PRIMARY_SPACE_UNIT_ALIAS"]: self._module.params.get(ds_constants["PRIMARY_SPACE_UNIT_ALIAS"]),
            ds_constants["TARGET_STATE_ALIAS"]: self._module.params.get(ds_constants["TARGET_STATE_ALIAS"])
        })
        self.starting_catalog = _data_set(
            size=_dataset_size(
                result.get(ds_constants["PRIMARY_SPACE_UNIT_ALIAS"]),
                result.get(ds_constants["PRIMARY_SPACE_VALUE_ALIAS"]),
                gc_constants["SECONDARY_SPACE_VALUE_DEFAULT"]),
            name=result.get(ds_constants["REGION_DATA_SETS_ALIAS"]).get('dfhgcd').get('dsn').upper(),
            sdfhload=result.get(ds_constants["CICS_DATA_SETS_ALIAS"]).get('sdfhload').upper(),
            state=result.get(ds_constants["TARGET_STATE_ALIAS"]),
            autostart_override="",
            nextstart="",
            exists=False,
            vsam=False)
        self.end_state = self.starting_catalog

    def create_global_catalog_dataset(self):
        create_cmd = _get_idcams_cmd_gcd(self.starting_catalog)

        idcams_executions = _run_idcams(
            cmd=create_cmd,
            name="Create global catalog data set",
            location=self.starting_catalog["name"],
            delete=False)
        self.executions = self.executions + idcams_executions

        self.result['changed'] = True

    def delete_global_catalog(self):
        if not self.starting_catalog["exists"]:
            self.result['end_state'] = {
                "exists": self.starting_catalog["exists"],
                "autostart_override": self.starting_catalog["autostart_override"],
                "next_start": self.starting_catalog["nextstart"],
            }
            self._exit()

        delete_cmd = '''
        DELETE {0}
        '''.format(self.starting_catalog["name"])

        idcams_executions = _run_idcams(
            cmd=delete_cmd,
            name="Removing global catalog data set",
            location=self.starting_catalog["name"],
            delete=True)
        self.executions = self.executions + idcams_executions
        self.result['changed'] = True

    def init_global_catalog(self):
        if self.starting_catalog["exists"] and self.starting_catalog["autostart_override"] == gc_constants["AUTO_START_INIT"]:
            self.result['end_state'] = {
                "exists": self.starting_catalog["exists"],
                "autostart_override": self.starting_catalog["autostart_override"],
                "next_start": self.starting_catalog["nextstart"],
            }
            self._exit()

        if not self.starting_catalog["exists"]:
            self.create_global_catalog_dataset()

        dfhrmutl_executions = _run_dfhrmutl(
            self.starting_catalog["name"],
            self.starting_catalog[ds_constants["SDFHLOAD_ALIAS"]],
            cmd="SET_AUTO_START=AUTOINIT")
        self.result['changed'] = True
        self.executions = self.executions + dfhrmutl_executions

    def warm_global_catalog(self):
        if not self.starting_catalog["exists"]:
            self._fail(
                "Data set {0} does not exist.".format(
                    self.starting_catalog["name"]))

        if self.starting_catalog["autostart_override"] == gc_constants["AUTO_START_WARM"]:
            self.result['end_state'] = {
                "exists": self.starting_catalog["exists"],
                "autostart_override": self.starting_catalog["autostart_override"],
                "next_start": self.starting_catalog["nextstart"],
            }
            self._exit()

        if (
            self.starting_catalog["autostart_override"] == gc_constants["AUTO_START_INIT"] and
            self.starting_catalog["nextstart"] == gc_constants["NEXT_START_UNKNOWN"]
        ):
            self._fail(
                "Unused catalog. The catalog must be used by CICS before doing a warm start.")

        dfhrmutl_executions = _run_dfhrmutl(
            self.starting_catalog["name"],
            self.starting_catalog[ds_constants["SDFHLOAD_ALIAS"]],
            cmd="SET_AUTO_START=AUTOASIS")
        self.result['changed'] = True
        self.executions = self.executions + dfhrmutl_executions

    def cold_global_catalog(self):
        if not self.starting_catalog["exists"]:
            self._fail(
                "Data set {0} does not exist.".format(
                    self.starting_catalog["name"]))

        if self.starting_catalog["autostart_override"] == gc_constants["AUTO_START_COLD"]:
            self.result['end_state'] = {
                "exists": self.starting_catalog["exists"],
                "autostart_override": self.starting_catalog["autostart_override"],
                "next_start": self.starting_catalog["nextstart"],
            }
            self._exit()

        if (
            self.starting_catalog["autostart_override"] == gc_constants["AUTO_START_INIT"] and
            self.starting_catalog["nextstart"] == gc_constants["NEXT_START_UNKNOWN"]
        ):
            self._fail(
                "Unused catalog. The catalog must be used by CICS before doing a cold start.")

        dfhrmutl_executions = _run_dfhrmutl(
            self.starting_catalog["name"],
            self.starting_catalog[ds_constants["SDFHLOAD_ALIAS"]],
            cmd="SET_AUTO_START=AUTOCOLD")
        self.result['changed'] = True
        self.executions = self.executions + dfhrmutl_executions

    def invalid_target_state(self):  # type: () -> None
        self._fail("{0} is not a valid target state.".format(
            self.global_catalog["state"]))

    def get_target_method(self, target):
        return {
            ds_constants["TARGET_STATE_ABSENT"]: self.delete_global_catalog,
            ds_constants["TARGET_STATE_INITIAL"]: self.init_global_catalog,
            ds_constants["TARGET_STATE_COLD"]: self.cold_global_catalog,
            ds_constants["TARGET_STATE_WARM"]: self.warm_global_catalog,
        }.get(target, self.invalid_target_state)

    def update_catalog(self, catalog):
        listds_executions, ds_status = _run_listds(catalog["name"])

        catalog["exists"] = ds_status['exists']
        catalog["vsam"] = ds_status['vsam']

        self.executions = self.executions + listds_executions

        if catalog["exists"] and catalog["vsam"]:
            dfhrmutl_executions, catalog_status = _run_dfhrmutl(
                catalog["name"], catalog[ds_constants["SDFHLOAD_ALIAS"]])

            catalog["autostart_override"] = catalog_status['autostart_override']
            catalog["nextstart"] = catalog_status['next_start']

            self.executions = self.executions + dfhrmutl_executions
        else:
            catalog["autostart_override"] = ""
            catalog["nextstart"] = ""
        return catalog

    def main(self):
        self.starting_catalog = self.update_catalog(self.starting_catalog)

        self.result['start_state'] = {
            "exists": self.starting_catalog["exists"],
            "autostart_override": self.starting_catalog["autostart_override"],
            "next_start": self.starting_catalog["nextstart"],
        }

        if self.starting_catalog["nextstart"] and self.starting_catalog["nextstart"].upper(
        ) == gc_constants["NEXT_START_EMERGENCY"]:
            self._fail(
                "Next start type is {0}. Potential data loss prevented.".format(
                    gc_constants["NEXT_START_EMERGENCY"]))

        self.get_target_method(
            self.starting_catalog["state"])()

        self.end_state = self.update_catalog(self.end_state)

        self.result['end_state'] = {
            "exists": self.end_state["exists"],
            "autostart_override": self.end_state["autostart_override"],
            "next_start": self.end_state["nextstart"],
        }
        self._exit()


def main():
    AnsibleGlobalCatalogModule().main()


if __name__ == '__main__':
    main()
