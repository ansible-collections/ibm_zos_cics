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
    data set used by a CICS® region. The global catalog is used to store start type information, location of the CICS system log,
    installed resource definitions, terminal control information and profiles. It contains information that CICS requires on a restart.
  - You can use this module when provisioning or de-provisioning a CICS region, or when managing
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
      - The size of the primary space allocated to the global catalog data set.
        Note that this is just the value; the unit is specified with O(space_type).
      - This option takes effect only when the global catalog is being created.
        If the global catalog already exists, the option has no effect.
    type: int
    required: false
    default: 5
  space_secondary:
    description:
      - The size of the secondary space allocated to the global catalog data set.
        Note that this is just the value; the unit is specified with O(space_type).
      - This option takes effect only when the global catalog is being created.
        If the global catalog already exists, the option has no effect.
    type: int
    required: false
    default: 1
  space_type:
    description:
      - The unit portion of the global catalog data set size. Note that this is
        just the unit; the value is specified with O(space_primary).
      - This option takes effect only when the global catalog is being created.
        If the global catalog already exists, the option has no effect.
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
      - If you want to use a data set that already exists, ensure that the data set is a global catalog data set.
    type: dict
    required: true
    suboptions:
      template:
        description:
          - The base location of the region data sets with a template.
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
              - The data set name of the global catalog to override the template.
            type: str
            required: false
  cics_data_sets:
    description:
      - The name of the C(SDFHLOAD) library of the CICS installation, for example, C(CICSTS61.CICS.SDFHLOAD).
      - This module uses the C(DFHRMUTL) utility internally, which is found in the C(SDFHLOAD) library.
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
          - The location of the C(SDFHLOAD) library to override the template.
        type: str
        required: false
  state:
    description:
      - The intended state for the global catalog, which the module will aim to
        achieve.
      - V(absent) will remove the global catalog data set entirely, if it
        already exists.
      - V(initial) will set the autostart override record to C(AUTOINIT). The module will
        create the global catalog data set if it does not already exist.
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
    - The state of the global catalog before the Ansible task runs.
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
    data_set_organization:
      description: The organization of the data set at the start of the Ansible task.
      returned: always
      type: str
      sample: "VSAM"
end_state:
  description: The state of the global catalog at the end of the Ansible task.
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
    data_set_organization:
      description: The organization of the data set at the end of the Ansible task.
      returned: always
      type: str
      sample: "VSAM"
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
    MEGABYTES,
    REGION_DATA_SETS,
    SPACE_PRIMARY,
    SPACE_SECONDARY,
    SPACE_TYPE,
    STATE,
    ABSENT,
    INITIAL,
    WARM,
    DataSet
)
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.global_catalog import (
    _get_idcams_cmd_gcd,
    _run_dfhrmutl
)

COLD = "cold"
STATE_OPTIONS = [ABSENT, INITIAL, WARM, COLD]
DSN = "dfhgcd"
AUTO_START_WARM = "AUTOASIS"
AUTO_START_COLD = "AUTOCOLD"
AUTO_START_INIT = "AUTOINIT"
NEXT_START_EMERGENCY = "EMERGENCY"
NEXT_START_WARM = "WARM"
NEXT_START_COLD = "COLD"
NEXT_START_UNKNOWN = "UNKNOWN"
SPACE_PRIMARY_DEFAULT = 5
SPACE_SECONDARY_DEFAULT = 1


class AnsibleGlobalCatalogModule(DataSet):
    def __init__(self):
        self.autostart_override = ""
        self.next_start = ""
        super(AnsibleGlobalCatalogModule, self).__init__(SPACE_PRIMARY_DEFAULT, SPACE_SECONDARY_DEFAULT)
        self.start_state = dict(
            exists=False,
            data_set_organization=self.data_set_organization,
            autostart_override=self.autostart_override,
            next_start=self.next_start
        )
        self.end_state = dict(
            exists=False,
            data_set_organization=self.data_set_organization,
            autostart_override=self.autostart_override,
            next_start=self.next_start
        )
        self.name = self.region_param[DSN]["dsn"].upper()
        self.expected_data_set_organization = "VSAM"

    def get_data_set(self):  # type: () -> dict
        data_set = super().get_data_set()
        data_set.update({
            "autostart_override": self.autostart_override,
            "next_start": self.next_start,
        })
        return data_set

    def set_start_state(self):  # type: () -> None
        self.start_state = dict(
            exists=self.exists,
            data_set_organization=self.data_set_organization,
            autostart_override=self.autostart_override,
            next_start=self.next_start
        )

    def set_end_state(self):  # type: () -> None
        self.end_state = dict(
            exists=self.exists,
            data_set_organization=self.data_set_organization,
            autostart_override=self.autostart_override,
            next_start=self.next_start
        )

    def _get_arg_spec(self):  # type: () -> dict
        arg_spec = super(AnsibleGlobalCatalogModule, self)._get_arg_spec()

        arg_spec[SPACE_PRIMARY].update({
            "default": SPACE_PRIMARY_DEFAULT
        })
        arg_spec[SPACE_SECONDARY].update({
            "default": SPACE_SECONDARY_DEFAULT
        })
        arg_spec[SPACE_TYPE].update({
            "default": MEGABYTES
        })
        arg_spec[STATE].update({
            "choices": STATE_OPTIONS
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
        create_cmd = _build_idcams_define_cmd(_get_idcams_cmd_gcd(self.get_data_set()))
        super().build_vsam_data_set(create_cmd)

    def init_data_set(self):  # type: () -> None
        if self.exists and self.autostart_override == AUTO_START_INIT:
            self._exit()

        if not self.exists:
            self.create_data_set()

        self.check_emergency()
        try:
            dfhrmutl_executions = _run_dfhrmutl(
                self.name,
                self.sdfhload,
                cmd="SET_AUTO_START=AUTOINIT")
            self.changed = True
            self.executions.extend(dfhrmutl_executions)
        except MVSExecutionException as e:
            self.executions.extend(e.executions)
            self._fail(e.message)

    def warm_data_set(self):  # type: () -> None
        super().warm_data_set()

        if self.autostart_override == AUTO_START_WARM:
            self._exit()

        if (
            self.autostart_override == AUTO_START_INIT and
            self.next_start == NEXT_START_UNKNOWN
        ):
            self._fail(
                "Unused catalog. The catalog must be used by CICS before doing a warm start.")
        try:
            dfhrmutl_executions = _run_dfhrmutl(
                self.name,
                self.sdfhload,
                cmd="SET_AUTO_START=AUTOASIS")
            self.changed = True
            self.executions.extend(dfhrmutl_executions)
        except MVSExecutionException as e:
            self.executions.extend(e.executions)
            self._fail(e.message)

    def cold_data_set(self):  # type: () -> None
        if not self.exists:
            self._fail("Data set {0} does not exist.".format(self.name))

        self.check_emergency()
        if self.autostart_override == AUTO_START_COLD:
            self._exit()

        if (
            self.autostart_override == AUTO_START_INIT and
            self.next_start == NEXT_START_UNKNOWN
        ):
            self._fail(
                "Unused catalog. The catalog must be used by CICS before doing a cold start.")
        try:
            dfhrmutl_executions = _run_dfhrmutl(
                self.name,
                self.sdfhload,
                cmd="SET_AUTO_START=AUTOCOLD")
            self.changed = True
            self.executions.extend(dfhrmutl_executions)
        except MVSExecutionException as e:
            self.executions.extend(e.executions)
            self._fail(e.message)

    def execute_target_state(self):   # type: () -> None
        if self.target_state == ABSENT:
            self.delete_data_set()
        elif self.target_state == INITIAL:
            self.init_data_set()
        elif self.target_state == WARM:
            self.warm_data_set()
        elif self.target_state == COLD:
            self.cold_data_set()
        else:
            self.invalid_target_state()

    def update_data_set_state(self):  # type: () -> None
        super().update_data_set_state()

        if self.exists and (self.data_set_organization == self.expected_data_set_organization):
            try:
                dfhrmutl_executions, (self.autostart_override, self.next_start) = _run_dfhrmutl(
                    self.name, self.sdfhload)

                self.executions.extend(dfhrmutl_executions)
            except MVSExecutionException as e:
                self.executions.extend(e.executions)
                self._fail(e.message)
        else:
            self.autostart_override = ""
            self.next_start = ""

    def check_emergency(self):  # type: () -> None
        if self.next_start and self.next_start.upper() == NEXT_START_EMERGENCY:
            self._fail(
                "Next start type is {0}. Potential data loss prevented."
                .format(NEXT_START_EMERGENCY))


def main():
    AnsibleGlobalCatalogModule().main()


if __name__ == '__main__':
    main()
