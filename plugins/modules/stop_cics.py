#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: stop_cics
short_description: Query CICS and CICSPlex SM resources and definitions
description:
  - Stop a CICS Region using CEMT PERFORM SHUTDOWN. The shutdown-assist transaction will be used if SDTRAN is specified
    in the CICS Region system initialisation parameters. The task will run until the region has successfully shutdown or
    the shutdown has failed.
version_added: 1.1.0-beta.4
author:
  - Kiera Bennett (@KieraBennett)
options:
  job_name:
    description:
      - Identifies the name of the job that the region was started with. Job names are 1-8 characters.
      - If a job name was not specified in the start-up playbook, the C(applid) can be provided instead.
    type: str
    required: true
  mode:
    description:
      - Specify the type of shutdown to be executed on the CICS Region.
    type: str
    required: false
    default: normal
    choices:
      - normal
      - immediate
      - cancel
'''


EXAMPLES = r'''
- name: "Stop CICS"
  ibm.ibm_zos_cics.stop_cics:
    job_name: ABC9ABC1

- name: "Stop CICS immediately"
  ibm.ibm_zos_cics.stop_cics:
    job_name: STARTJOB
    mode: immediate
'''

RETURN = r'''
  changed:
    description: True if the shutdown command was executed.
    returned: always
    type: bool
  failed:
    description: True if the module failed, otherwise False.
    returned: always
    type: bool
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
        returned: On shutdown execution
      return:
        description: The standard output returned by the program execution.
        type: str
        returned: always
'''

from ansible.module_utils.basic import AnsibleModule

CANCEL = 'cancel'
IMMEDIATE = 'immediate'
JOB_NAME = 'job_name'
MODE = 'mode'
NORMAL = 'normal'


class AnsibleStopCICSModule(object):

    def __init__(self):
        self._module = AnsibleModule(
            argument_spec=self.init_argument_spec()
        )

    def main(self):
        self._module.exit_json()

    def init_argument_spec(self):
        return {
            JOB_NAME: {
                'type': 'str',
                'required': True,
            },
            MODE: {
                'type': 'str',
                'required': False,
                'default': NORMAL,
                'choices': [NORMAL, IMMEDIATE, CANCEL]
            },
        }


def main():
    if __name__ == '__main__':
        AnsibleStopCICSModule().main()


if __name__ == '__main__':
    main()
