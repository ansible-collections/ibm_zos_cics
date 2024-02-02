#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: auxiliary_temp
short_description: Create and remove the CICS auxiliary temporary storage data set
description:
  - Create and remove the L(auxiliary temporary storage,https://www.ibm.com/docs/en/cics-ts/latest?topic=sets-defining-auxiliary-temporary-storage-data-set)
    data set used by a CICS® region.
  - You can use this module when provisioning or de-provisioning a CICS region.
  - Use the O(state) option to specify the intended state for the auxiliary
    temporary storage data set. For example, O(state=initial) will create a auxiliary temporary storage
    data set if it doesn't exist.
author: Andrew Twydell (@andrewtwydell)
version_added: 1.1.0-beta.4
options:
  space_primary:
    description:
      - The size of the primary space allocated to the auxiliary temporary storage data set.
        Note that this is just the value; the unit is specified with O(space_type).
      - This option takes effect only when the auxiliary temporary storage data set is being created.
        If the data set already exists, the option has no effect.
      - The size value of the secondary space allocation for the auxiliary temporary storage data set is 10; the unit is specified with O(space_type).
    type: int
    required: false
    default: 200
  space_type:
    description:
      - The unit portion of the auxiliary temporary storage data set size. Note that this is
        just the unit; the value is specified with O(space_primary).
      - This option takes effect only when the auxiliary temporary storage data set is being created.
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
    default: REC
  region_data_sets:
    description:
      - The location of the region data sets to be created using a template, for example,
        C(REGIONS.ABCD0001.<< data_set_name >>).
      - If you want to use a data set that already exists, ensure that the data set is a auxiliary temporary storage data set.
    type: dict
    required: true
    suboptions:
      template:
        description:
          - The base location of the region data sets with a template.
        required: false
        type: str
      dfhtemp:
        description:
          - Overrides the templated location for the auxiliary temporary storage data set.
        required: false
        type: dict
        suboptions:
          dsn:
            description:
              - The data set name of the auxiliary temporary storage to override the template.
            type: str
            required: false
  cics_data_sets:
    description:
      - The name of the C(SDFHLOAD) library of the CICS installation, for example, C(CICSTS61.CICS.SDFHLOAD).
    type: dict
    required: false
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
      - The intended state for the auxiliary temporary storage data set, which the module will aim to
        achieve.
      - V(absent) will remove the auxiliary temporary storage data set entirely, if it
        already exists.
      - V(initial) will create the auxiliary temporary storage data set if it does not
        already exist.
      - V(warm) will retain an existing auxiliary temporary storage data set in its current state.
    choices:
      - "initial"
      - "absent"
      - "warm"
    required: true
    type: str
"""


EXAMPLES = r"""
- name: Initialize an auxiliary temporary storage data set
  ibm.ibm_zos_cics.auxiliary_temp:
    region_data_sets:
      template: "REGIONS.ABCD0001.<< data_set_name >>"
    state: "initial"

- name: Initialize a large auxiliary temporary storage data set
  ibm.ibm_zos_cics.auxiliary_temp:
    region_data_sets:
      template: "REGIONS.ABCD0001.<< data_set_name >>"
    space_primary: 50
    space_type: "M"
    state: "initial"

- name: Delete an existing auxiliary temporary storage data set
  ibm.ibm_zos_cics.auxiliary_temp:
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
    - The state of the auxiliary temporary storage before the Ansible task runs.
  returned: always
  type: dict
  contains:
    vsam:
      description: True if the data set is a VSAM data set.
      returned: always
      type: bool
    exists:
      description: True if the auxiliary temporary storage data set exists.
      type: bool
      returned: always
end_state:
  description: The state of the auxiliary temporary storage at the end of the Ansible task.
  returned: always
  type: dict
  contains:
    vsam:
      description: True if the data set is a VSAM data set.
      returned: always
      type: bool
    exists:
      description: True if the auxiliary temporary storage data set exists.
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


from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.better_arg_parser import (
    BetterArgParser,
)
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.dataset_utils import (
    _build_idcams_define_cmd,
    _dataset_size,
    _data_set,
)
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.data_set import (
    DataSet,
)
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.response import (
    _state,
)
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.auxiliary_temp import (
    _auxiliary_temp_constants as temp_constants,
    _get_idcams_cmd_temp,
)
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.data_set import (
    _dataset_constants as ds_constants,
)


class AnsibleAuxiliaryTempModule(DataSet):
    def __init__(self):
        super(AnsibleAuxiliaryTempModule, self).__init__()

    def init_argument_spec(self):  # type: () -> dict
        arg_spec = super(AnsibleAuxiliaryTempModule, self).init_argument_spec()

        arg_spec[ds_constants["PRIMARY_SPACE_VALUE_ALIAS"]].update({
            "default": temp_constants["PRIMARY_SPACE_VALUE_DEFAULT"],
        })
        arg_spec[ds_constants["PRIMARY_SPACE_UNIT_ALIAS"]].update({
            "default": temp_constants["SPACE_UNIT_DEFAULT"],
        })
        arg_spec[ds_constants["TARGET_STATE_ALIAS"]].update({
            "choices": temp_constants["TARGET_STATE_OPTIONS"],
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
                    "dfhtemp": {
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
                "required": False,
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
        arg_def = super(AnsibleAuxiliaryTempModule, self)._get_arg_defs()

        arg_def[ds_constants["PRIMARY_SPACE_VALUE_ALIAS"]].update({
            "default": temp_constants["PRIMARY_SPACE_VALUE_DEFAULT"]
        })
        arg_def[ds_constants["PRIMARY_SPACE_UNIT_ALIAS"]].update({
            "default": temp_constants["SPACE_UNIT_DEFAULT"]
        })
        arg_def[ds_constants["TARGET_STATE_ALIAS"]].update({
            "choices": temp_constants["TARGET_STATE_OPTIONS"]
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
                    "dfhtemp": {
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
                "required": False,
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

    def _get_data_set_object(self, size, result):
        return _data_set(
            size=size,
            name=result.get(ds_constants["REGION_DATA_SETS_ALIAS"])
            .get("dfhtemp")
            .get("dsn")
            .upper(),
            state=result.get(ds_constants["TARGET_STATE_ALIAS"]),
            exists=False,
            vsam=False,
        )

    def _get_data_set_size(self, result):
        return _dataset_size(
            unit=result.get(ds_constants["PRIMARY_SPACE_UNIT_ALIAS"]),
            primary=result.get(ds_constants["PRIMARY_SPACE_VALUE_ALIAS"]),
            secondary=temp_constants["SECONDARY_SPACE_VALUE_DEFAULT"],
        )

    def validate_parameters(self):  # type: () -> None
        arg_defs = self._get_arg_defs()

        result = BetterArgParser(arg_defs).parse_args({
            ds_constants["REGION_DATA_SETS_ALIAS"]: self._module.params.get(
                ds_constants["REGION_DATA_SETS_ALIAS"]
            ),
            ds_constants["CICS_DATA_SETS_ALIAS"]: self._module.params.get(
                ds_constants["CICS_DATA_SETS_ALIAS"]
            ),
            ds_constants["PRIMARY_SPACE_VALUE_ALIAS"]: self._module.params.get(
                ds_constants["PRIMARY_SPACE_VALUE_ALIAS"]
            ),
            ds_constants["PRIMARY_SPACE_UNIT_ALIAS"]: self._module.params.get(
                ds_constants["PRIMARY_SPACE_UNIT_ALIAS"]
            ),
            ds_constants["DATASET_LOCATION_ALIAS"]: self._module.params.get(
                ds_constants["DATASET_LOCATION_ALIAS"]
            ),
            ds_constants["TARGET_STATE_ALIAS"]: self._module.params.get(
                ds_constants["TARGET_STATE_ALIAS"]
            ),
        })

        size = self._get_data_set_size(result)
        self.data_set = self._get_data_set_object(size, result)

    def create_data_set(self):  # type: () -> None
        create_cmd = _build_idcams_define_cmd(_get_idcams_cmd_temp(self.data_set))

        super().build_vsam_data_set(create_cmd, "Create auxiliary temp data set")

    def delete_data_set(self):  # type: () -> None
        if not self.data_set["exists"]:
            self.result["end_state"] = _state(
                exists=self.data_set["exists"], vsam=self.data_set["vsam"]
            )
            self._exit()

        super().delete_data_set("Removing auxiliary temp data set")


def main():
    AnsibleAuxiliaryTempModule().main()


if __name__ == "__main__":
    main()
