#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2020,2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: local_request_queue
short_description: Create and remove the CICS local request queue
description:
  - Create and remove the L(local request queue,https://www.ibm.com/docs/en/cics-ts/latest?topic=sets-local-request-queue-data-set)
    data set used by a CICS® region.
  - Useful when provisioning or de-provisioning a CICS region.
  - Use the O(state) option to specify the intended state for the local
    request queue. For example, O(state=initial) will create a local
    request queue data set if it doesn't yet exist, or it will take an existing
    local request queue and empty it of all records.
author: Drew Hughes (@andrewhughes101)
version_added: 1.1.0-beta.2
options:
  space_primary:
    description:
      - The size of the local request queue data set's primary space allocation.
        Note, this is just the value; the unit is specified with O(space_type).
      - This option only takes effect when the local request queue is being created.
        If it already exists, it has no effect.
      - The local request queue data set's secondary space allocation is set to 1.
    type: int
    required: false
    default: 4
  space_type:
    description:
      - The unit portion of the local request queue data set size. Note, this is
        just the unit; the value is specified with O(space_primary).
      - This option only takes effect when the local request queue is being created.
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
  location:
    description:
      - The name of the local request queue data set, e.g.
        C(REGIONS.ABCD0001.DFHLCD).
    type: str
    required: true
  state:
    description:
      - The desired state for the local request queue, which the module will aim to
        achieve.
      - V(absent) will remove the local request queue data set entirely, if it
        already exists.
      - V(initial) will create the local request queue data set if it does not
        already exist, and empty it of all existing records.
    choices:
      - "initial"
      - "absent"
    required: true
    type: str
'''


EXAMPLES = r"""
- name: Initialize a local request queue
  ibm.ibm_zos_cics.local_request_queue:
    location: "REGIONS.ABCD0001.DFHLRQ"
    state: "initial"

- name: Initialize a large request queue
  ibm.ibm_zos_cics.local_request_queue:
    location: "REGIONS.ABCD0001.DFHLRQ"
    space_primary: 50
    space_type: "M"
    state: "initial"

- name: Delete local request queue
  ibm.ibm_zos_cics.local_request_queue:
    location: "REGIONS.ABCD0001.DFHLRQ"
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
    - The state of the local request queue before the task runs.
  returned: always
  type: dict
  contains:
    vsam:
      description: True if the data set is a VSAM data set.
      returned: always
      type: bool
    exists:
      description: True if the local request queue data set exists.
      type: bool
      returned: always
end_state:
  description: The state of the local request queue at the end of the task.
  returned: always
  type: dict
  contains:
    vsam:
      description: True if the data set is a VSAM data set.
      returned: always
      type: bool
    exists:
      description: True if the local request queue data set exists.
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
        _dataset_size, _run_idcams, _run_listds)
    from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import catalog_constants as constants
    from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.local_request_queue import (
        _local_request_queue, _get_idcams_cmd_lrq)
except ImportError:
    ZOS_CICS_IMP_ERR = traceback.format_exc()


class AnsibleLocalRequestQueueModule(object):
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
                'default': 4,
            },
            constants.CATALOG_PRIMARY_SPACE_UNIT_ALIAS: {
                'required': False,
                'type': 'str',
                'choices': constants.CATALOG_SPACE_UNIT_OPTIONS,
                'default': "M",
            },
            constants.CATALOG_DATASET_ALIAS: {
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
                default=4,
            ),
            space_type=dict(
                arg_type='str',
                choices=constants.CATALOG_SPACE_UNIT_OPTIONS,
                default="M",
            ),
            location=dict(
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
            constants.CATALOG_TARGET_STATE_ALIAS: self._module.params.get(constants.CATALOG_TARGET_STATE_ALIAS)
        })

        size = _dataset_size(
            unit=result.get(constants.CATALOG_PRIMARY_SPACE_UNIT_ALIAS),
            primary=result.get(constants.CATALOG_PRIMARY_SPACE_VALUE_ALIAS),
            secondary=1,
            record_count=2232,
            record_size=2400,
            control_interval_size=2560)

        self.queue_definition = _local_request_queue(
            size=size,
            name=result.get(constants.CATALOG_DATASET_ALIAS).upper(),
            state=result.get(constants.CATALOG_TARGET_STATE_ALIAS),
            exists=False,
            vsam=False)

    def create_local_request_queue_dataset(self):
        create_cmd = _get_idcams_cmd_lrq(self.queue_definition)

        idcams_executions = _run_idcams(
            cmd=create_cmd,
            name="Create local request queue data set",
            location=self.queue_definition["name"],
            delete=False)
        self.executions = self.executions + idcams_executions

        self.result['changed'] = True

    def delete_local_request_queue_dataset(self):
        if not self.queue_definition["exists"]:
            self.result['end_state'] = {
                "exists": self.queue_definition["exists"],
                "vsam": self.queue_definition["vsam"]
            }
            self._exit()

        delete_cmd = '''
        DELETE {0}
        '''.format(self.queue_definition["name"])

        idcams_executions = _run_idcams(
            cmd=delete_cmd,
            name="Removing local request queue data set",
            location=self.queue_definition["name"],
            delete=True)
        self.executions = self.executions + idcams_executions
        self.result['changed'] = True

    def init_local_request_queue(self):
        if self.queue_definition["exists"]:
            self.result['end_state'] = {
                "exists": self.queue_definition["exists"],
                "vsam": self.queue_definition["vsam"]
            }
            self._exit()

        if not self.queue_definition["exists"]:
            self.create_local_request_queue_dataset()

    def invalid_state(self):  # type: () -> None
        self._fail("{0} is not a valid target state.".format(
            self.local_request_queue["state"]))

    def get_target_method(self, target):
        return {
            constants.LOCAL_CATALOG_TARGET_STATE_ABSENT: self.delete_local_request_queue_dataset,
            constants.LOCAL_CATALOG_TARGET_STATE_INITIAL: self.init_local_request_queue
        }.get(target, self.invalid_state)

    def get_dataset_state(self, dataset):
        listds_executions, ds_status = _run_listds(dataset["name"])

        dataset["exists"] = ds_status['exists']
        dataset["vsam"] = ds_status['vsam']

        self.executions = self.executions + listds_executions

        return dataset

    def main(self):
        self.queue_definition = self.get_dataset_state(self.queue_definition)

        self.result['start_state'] = {
            "exists": self.queue_definition["exists"],
            "vsam": self.queue_definition["vsam"]
        }

        if self.queue_definition["exists"] and not self.queue_definition["vsam"]:
            self._fail(
                "Data set {0} does not appear to be a KSDS.".format(
                    self.queue_definition["name"]))

        self.get_target_method(self.queue_definition["state"])()

        self.end_state = self.get_dataset_state(self.queue_definition)

        self.result['end_state'] = {
            "exists": self.end_state["exists"],
            "vsam": self.end_state["vsam"]
        }

        self._exit()


def main():
    AnsibleLocalRequestQueueModule().main()


if __name__ == '__main__':
    main()
