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


from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.data_set import _dataset_constants as ds_constants
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.global_catalog import _global_catalog_constants as gc_constants
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.response import _state
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.global_catalog import (
    _run_dfhrmutl, _get_idcams_cmd_gcd)
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.data_set import DataSet
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.dataset_utils import (
    _dataset_size, _run_listds, _data_set, _build_idcams_define_cmd)
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.better_arg_parser import BetterArgParser
from typing import Dict


class AnsibleGlobalCatalogModule(DataSet):
    def __init__(self):
        super(AnsibleGlobalCatalogModule, self).__init__()

    def init_argument_spec(self):  # type: () -> Dict
        arg_spec = super(AnsibleGlobalCatalogModule, self).init_argument_spec()

        arg_spec[ds_constants["PRIMARY_SPACE_VALUE_ALIAS"]].update({
            "default": gc_constants["PRIMARY_SPACE_VALUE_DEFAULT"]
        })
        arg_spec[ds_constants["PRIMARY_SPACE_UNIT_ALIAS"]].update({
            "default": gc_constants["SPACE_UNIT_DEFAULT"]
        })
        arg_spec[ds_constants["TARGET_STATE_ALIAS"]].update({
            "choices": gc_constants["TARGET_STATE_OPTIONS"]
        })
        arg_spec.update({
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
        })

        return arg_spec

    def _get_arg_defs(self):  # type: () -> Dict
        arg_def = super(AnsibleGlobalCatalogModule, self)._get_arg_defs()

        arg_def[ds_constants["PRIMARY_SPACE_VALUE_ALIAS"]].update({
            "default": gc_constants["PRIMARY_SPACE_VALUE_DEFAULT"]
        })
        arg_def[ds_constants["PRIMARY_SPACE_UNIT_ALIAS"]].update({
            "default": gc_constants["SPACE_UNIT_DEFAULT"]
        })
        arg_def[ds_constants["TARGET_STATE_ALIAS"]].update({
            "choices": gc_constants["TARGET_STATE_OPTIONS"],
        })
        arg_def.update({
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
        })

        return arg_def

    def _get_data_set_object(self, size, result):  # type: (_dataset_size, Dict) -> _data_set
        return _data_set(
            size=size,
            name=result.get(ds_constants["REGION_DATA_SETS_ALIAS"]).get('dfhgcd').get('dsn').upper(),
            sdfhload=result.get(ds_constants["CICS_DATA_SETS_ALIAS"]).get('sdfhload').upper(),
            state=result.get(ds_constants["TARGET_STATE_ALIAS"]),
            autostart_override="",
            nextstart="",
            exists=False,
            vsam=False)

    def _get_data_set_size(self, result):
        return _dataset_size(
            unit=result.get(ds_constants["PRIMARY_SPACE_UNIT_ALIAS"]),
            primary=result.get(ds_constants["PRIMARY_SPACE_VALUE_ALIAS"]),
            secondary=gc_constants["SECONDARY_SPACE_VALUE_DEFAULT"])

    def validate_parameters(self):  # type: () -> None
        arg_defs = self._get_arg_defs()

        result = BetterArgParser(arg_defs).parse_args({
            ds_constants["REGION_DATA_SETS_ALIAS"]: self._module.params.get(ds_constants["REGION_DATA_SETS_ALIAS"]),
            ds_constants["CICS_DATA_SETS_ALIAS"]: self._module.params.get(ds_constants["CICS_DATA_SETS_ALIAS"]),
            ds_constants["PRIMARY_SPACE_VALUE_ALIAS"]: self._module.params.get(ds_constants["PRIMARY_SPACE_VALUE_ALIAS"]),
            ds_constants["PRIMARY_SPACE_UNIT_ALIAS"]: self._module.params.get(ds_constants["PRIMARY_SPACE_UNIT_ALIAS"]),
            ds_constants["TARGET_STATE_ALIAS"]: self._module.params.get(ds_constants["TARGET_STATE_ALIAS"])
        })

        size = self._get_data_set_size(result)
        self.data_set = self._get_data_set_object(size, result)
        self.end_state = self.data_set

    def create_data_set(self):
        create_cmd = _build_idcams_define_cmd(_get_idcams_cmd_gcd(self.data_set))

        super().build_vsam_data_set(create_cmd, "Create global catalog data set")

    def delete_data_set(self):
        if not self.data_set["exists"]:
            self.result["end_state"] = {
                "exists": self.data_set["exists"],
                "autostart_override": self.data_set["autostart_override"],
                "next_start": self.data_set["nextstart"],
            }
            self._exit()

        super().delete_data_set("Removing global catalog data set")

    def init_data_set(self):
        if self.data_set["exists"] and self.data_set["autostart_override"] == gc_constants["AUTO_START_INIT"]:
            self.result["end_state"] = _state(
                exists=self.data_set["exists"],
                autostart_override=self.data_set["autostart_override"],
                next_start=self.data_set["nextstart"],
            )
            self._exit()

        if not self.data_set["exists"]:
            self.create_data_set()

        dfhrmutl_executions = _run_dfhrmutl(
            self.data_set["name"],
            self.data_set[ds_constants["SDFHLOAD_ALIAS"]],
            cmd="SET_AUTO_START=AUTOINIT")
        self.result["changed"] = True
        self.result["executions"] = self.result["executions"] + dfhrmutl_executions

    def warm_data_set(self):
        if not self.data_set["exists"]:
            self._fail(
                "Data set {0} does not exist.".format(
                    self.data_set["name"]))

        if self.data_set["autostart_override"] == gc_constants["AUTO_START_WARM"]:
            self.result["end_state"] = _state(
                exists=self.data_set["exists"],
                autostart_override=self.data_set["autostart_override"],
                next_start=self.data_set["nextstart"],
            )
            self._exit()

        if (
            self.data_set["autostart_override"] == gc_constants["AUTO_START_INIT"] and
            self.data_set["nextstart"] == gc_constants["NEXT_START_UNKNOWN"]
        ):
            self._fail(
                "Unused catalog. The catalog must be used by CICS before doing a warm start.")

        dfhrmutl_executions = _run_dfhrmutl(
            self.data_set["name"],
            self.data_set[ds_constants["SDFHLOAD_ALIAS"]],
            cmd="SET_AUTO_START=AUTOASIS")
        self.result["changed"] = True
        self.result["executions"] = self.result["executions"] + dfhrmutl_executions

    def cold_data_set(self):
        if not self.data_set["exists"]:
            self._fail(
                "Data set {0} does not exist.".format(
                    self.data_set["name"]))

        if self.data_set["autostart_override"] == gc_constants["AUTO_START_COLD"]:
            self.result["end_state"] = {
                "exists": self.data_set["exists"],
                "autostart_override": self.data_set["autostart_override"],
                "next_start": self.data_set["nextstart"],
            }
            self._exit()

        if (
            self.data_set["autostart_override"] == gc_constants["AUTO_START_INIT"] and
            self.data_set["nextstart"] == gc_constants["NEXT_START_UNKNOWN"]
        ):
            self._fail(
                "Unused catalog. The catalog must be used by CICS before doing a cold start.")

        dfhrmutl_executions = _run_dfhrmutl(
            self.data_set["name"],
            self.data_set[ds_constants["SDFHLOAD_ALIAS"]],
            cmd="SET_AUTO_START=AUTOCOLD")
        self.result["changed"] = True
        self.result["executions"] = self.result["executions"] + dfhrmutl_executions

    def get_target_method(self, target):
        return {
            ds_constants["TARGET_STATE_ABSENT"]: self.delete_data_set,
            ds_constants["TARGET_STATE_INITIAL"]: self.init_data_set,
            ds_constants["TARGET_STATE_COLD"]: self.cold_data_set,
            ds_constants["TARGET_STATE_WARM"]: self.warm_data_set,
        }.get(target, self.invalid_target_state)

    def get_data_set_state(self, data_set):
        listds_executions, ds_status = _run_listds(data_set["name"])

        data_set["exists"] = ds_status['exists']
        data_set["vsam"] = ds_status['vsam']

        self.result["executions"] = self.result["executions"] + listds_executions

        if data_set["exists"] and data_set["vsam"]:
            dfhrmutl_executions, catalog_status = _run_dfhrmutl(
                data_set["name"], data_set[ds_constants["SDFHLOAD_ALIAS"]])

            data_set["autostart_override"] = catalog_status['autostart_override']
            data_set["nextstart"] = catalog_status['next_start']

            self.result["executions"] = self.result["executions"] + dfhrmutl_executions
        else:
            data_set["autostart_override"] = ""
            data_set["nextstart"] = ""
        return data_set

    def main(self):
        self.data_set = self.get_data_set_state(self.data_set)

        self.result["start_state"] = _state(
            exists=self.data_set["exists"],
            autostart_override=self.data_set["autostart_override"],
            next_start=self.data_set["nextstart"],
            vsam=self.data_set["vsam"])

        if self.data_set["nextstart"] and self.data_set["nextstart"].upper(
        ) == gc_constants["NEXT_START_EMERGENCY"]:
            self._fail(
                "Next start type is {0}. Potential data loss prevented.".format(
                    gc_constants["NEXT_START_EMERGENCY"]))

        self.get_target_method(self.data_set["state"])()

        self.end_state = self.get_data_set_state(self.data_set)

        self.result["end_state"] = _state(
            exists=self.end_state["exists"],
            autostart_override=self.end_state["autostart_override"],
            next_start=self.end_state["nextstart"],
            vsam=self.end_state["vsam"])

        self._exit()


def main():
    AnsibleGlobalCatalogModule().main()


if __name__ == '__main__':
    main()
