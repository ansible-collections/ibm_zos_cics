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
  - Create, remove, and manage the L(csd,https://www.ibm.com/docs/en/cics-ts/6.1?topic=configuring-setting-up-shared-data-sets-csd-sysin)
    data set used by a CICS® region.
  - Useful when provisioning or de-provisioning a CICS region, or when managing
    the state of the CSD during upgrades or restarts.
  - Use the O(state) option to specify the intended state for the CSD.
    For example, O(state=initial) will create and initialize a CSD
    data set if it doesn't yet exist, or it will take an existing
    CSD and empty it of all records.
author: Thomas Latham (@Thomas-Latham3)
version_added: 1.1.0-beta.2
seealso:
  - module: global_catalog
  - module: local_catalog
options:
  space_primary:
    description:
      - The size of the CSD data set's primary space allocation.
        Note, this is just the value; the unit is specified with O(space_type).
      - This option only takes effect when the CSD is being created.
        If it already exists, it has no effect.
      - The CSD data set's secondary space allocation is set to 1.
    type: int
    required: false
    default: 4
  space_type:
    description:
      - The unit portion of the CSD data set size. Note, this is
        just the unit; the value is specified with O(space_primary).
      - This option only takes effect when the CSD is being created.
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
      dfhcsd:
        description:
          - Overrides the templated location for the CSD data set.
        required: false
        type: dict
        suboptions:
          dsn:
            description:
              - Data set name of the CSD to override the template.
            type: str
            required: false
  cics_data_sets:
    description:
      - The name of the C(SDFHLOAD) data set, e.g. C(CICSTS61.CICS.SDFHLOAD).
      - This module uses the C(DFHCCUTL) utility internally, which is found in
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
      - The desired state for the CSD, which the module will aim to
        achieve.
      - V(absent) will remove the CSD data set entirely, if it
        already exists.
      - V(initial) will create the CSD data set if it does not
        already exist, and empty it of all existing records.
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

- name: Initialize a large catalog
  ibm.ibm_zos_cics.csd:
    region_data_sets:
      template: "REGIONS.ABCD0001.<< data_set_name >>"
    cics_data_sets:
      template: "CICSTS61.CICS.<< lib_name >>"
    space_primary: 500
    space_type: "REC"
    state: "initial"

- name: Delete CSD
  ibm.ibm_zos_cics.csd:
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
    - The state of the CSD before the task runs.
  returned: always
  type: dict
  contains:
    vsam:
      description: True if the data set is a VSAM data set.
      returned: always
      type: bool
    exists:
      description: True if the CSD data set exists.
      type: bool
      returned: always
end_state:
  description: The state of the CSD at the end of the task.
  returned: always
  type: dict
  contains:
    vsam:
      description: True if the data set is a VSAM data set.
      returned: always
      type: bool
    exists:
      description: True if the CSD data set exists.
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


from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.better_arg_parser import BetterArgParser
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.dataset_utils import (
    _dataset_size, _data_set, _build_idcams_define_cmd)
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.data_set import DataSet
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.csd import (
    _run_dfhccutl, _get_idcams_cmd_csd)
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.icetool import (_run_icetool)
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.csd import _csd_constants as csd_constants
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.data_set import _dataset_constants as ds_constants


class AnsibleCSDModule(DataSet):
    def __init__(self):
        super(AnsibleCSDModule, self).__init__()

    def init_argument_spec(self):  # type: () -> dict
        arg_spec = super(AnsibleCSDModule, self).init_argument_spec()

        arg_spec[ds_constants["PRIMARY_SPACE_VALUE_ALIAS"]].update({
            "default": csd_constants["PRIMARY_SPACE_VALUE_DEFAULT"]
        })
        arg_spec[ds_constants["PRIMARY_SPACE_UNIT_ALIAS"]].update({
            "default": csd_constants["SPACE_UNIT_DEFAULT"]
        })
        arg_spec[ds_constants["TARGET_STATE_ALIAS"]].update({
            "choices": csd_constants["TARGET_STATE_OPTIONS"]
        })
        arg_spec.update({
            ds_constants["REGION_DATA_SETS_ALIAS"]: {
                "type": "dict",
                "required": True,
                "options": {
                    "template": {
                        "type": "str",
                        "required": False,
                    },
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
                },
            },
            ds_constants["CICS_DATA_SETS_ALIAS"]: {
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
            },
        })
        return arg_spec

    def _get_arg_defs(self):  # type: () -> dict
        arg_def = super(AnsibleCSDModule, self)._get_arg_defs()

        arg_def[ds_constants["PRIMARY_SPACE_VALUE_ALIAS"]].update({
            "default": csd_constants["PRIMARY_SPACE_VALUE_DEFAULT"]
        })
        arg_def[ds_constants["PRIMARY_SPACE_UNIT_ALIAS"]].update({
            "default": csd_constants["SPACE_UNIT_DEFAULT"]
        })
        arg_def[ds_constants["TARGET_STATE_ALIAS"]].update({
            "choices": csd_constants["TARGET_STATE_OPTIONS"],
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
                    "dfhcsd": {
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

    def _get_data_set_object(self, size, result):  # type: (_dataset_size, dict) -> _data_set
        return _data_set(
            size=size,
            name=result.get(ds_constants["REGION_DATA_SETS_ALIAS"]).get("dfhcsd").get("dsn").upper(),
            sdfhload=result.get(ds_constants["CICS_DATA_SETS_ALIAS"]).get("sdfhload").upper(),
            state=result.get(ds_constants["TARGET_STATE_ALIAS"]),
            exists=False,
            vsam=False)

    def _get_data_set_size(self, result):  # type: (dict) -> _dataset_size
        return _dataset_size(
            unit=result.get(ds_constants["PRIMARY_SPACE_UNIT_ALIAS"]),
            primary=result.get(ds_constants["PRIMARY_SPACE_VALUE_ALIAS"]),
            secondary=csd_constants["SECONDARY_SPACE_VALUE_DEFAULT"])

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

    def create_data_set(self):  # type: () -> None
        create_cmd = _build_idcams_define_cmd(_get_idcams_cmd_csd(self.data_set))

        super().build_vsam_data_set(create_cmd, "Create CSD data set")

    def delete_data_set(self):  # type: () -> None
        if not self.data_set["exists"]:
            self.result["end_state"] = {
                "exists": self.data_set["exists"],
                "vsam": self.data_set["vsam"]
            }
            self._exit()

        super().delete_data_set("Removing CSD data set")

    def warm_data_set(self):  # type: () -> None
        super().warm_data_set()

        try:
            icetool_executions, record_count = _run_icetool(self.data_set["name"])
            if record_count["record_count"] <= 0:
                self._fail("Unused catalog. The catalog must be used by CICS before doing a warm start.")

            self.result["executions"] = self.result["executions"] + icetool_executions
            self.result["changed"] = False
        except Exception as e:
            self.result["executions"] = self.result["executions"] + e.args[1]
            self._fail(e.args[0])

    def init_data_set(self):  # type: () -> None
        if self.data_set["exists"]:
            self.result["end_state"] = {
                "exists": self.data_set["exists"],
                "vsam": self.data_set["vsam"]
            }
            self._exit()

        if not self.data_set["exists"]:
            self.create_data_set()

        try:
            ccutl_executions = _run_dfhccutl(self.data_set)
            self.result["executions"] = self.result["executions"] + ccutl_executions
        except Exception as e:
            self.result["executions"] = self.result["executions"] + e.args[1]
            self._fail(e.args[0])


def main():
    AnsibleCSDModule().main()


if __name__ == '__main__':
    main()
