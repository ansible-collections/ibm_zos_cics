#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: stop_cics
short_description: Stop a CICS Region
description:
  - Stop a CICS region by using CEMT PERFORM SHUTDOWN. You can choose to perform a NORMAL or IMMEDIATE shutdown.
    During a NORMAL or IMMEDIATE shutdown, a shutdown assist program should run to enable CICS to shut down in a controlled manner.
    By default, the CICS-supplied shutdown assist transaction, CESD is used. You can specify a custom shutdown assist program in the
    SDTRAN system initialization parameter. The task runs until the region has successfully shut down, or until the shutdown fails.
version_added: 1.1.0-beta.5
author:
  - Kiera Bennett (@KieraBennett)
options:
  job_id:
    description:
      - Identifies the job ID belonging to the running CICS region.
      - The Stop CICS module uses this job ID to identify the state of the CICS region and shut it down.
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
    job_id: JOB12345

- name: "Stop CICS immediately"
  ibm.ibm_zos_cics.stop_cics:
    job_id: JOB12354
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
        returned: on shutdown execution
      return:
        description: The standard output returned by the program execution.
        type: dict
        returned: always
        contains:
          changed:
           description: True if the state was changed, otherwise False.
           returned: always
           type: bool
          jobs:
            description: The output information for a list of jobs matching specified criteria.
            type: list
            returned: success
            elements: dict
            contains:
              job_id:
                description: Unique job identifier assigned to the job by JES.
                type: str
              job_name:
                description: The name of the batch job.
                type: str
              owner:
                description: The owner who ran the job.
                type: str
              ret_code:
                description:
                  Return code output collected from job log.
                type: dict
                contains:
                  msg:
                    description:
                      Return code or abend resulting from the job submission.
                    type: str
                  msg_code:
                    description:
                      Return code extracted from the `msg` so that it can be evaluated.
                      For example, ABEND(S0C4) would yield "S0C4".
                    type: str
                  msg_txt:
                    description:
                      Returns additional information related to the job.
                    type: str
                  code:
                    description:
                      Return code converted to integer value (when possible).
                    type: int
                  steps:
                    description:
                      Series of JCL steps that were executed and their return codes.
                    type: list
                    elements: dict
                    contains:
                      step_name:
                        description:
                          Name of the step shown as "was executed" in the DD section.
                        type: str
                      step_cc:
                        description:
                          The CC returned for this step in the DD section.
                        type: int
          message:
            description: Message returned on failure.
            returned: failure
            type: str
          content:
            description: The resulting text from the command submitted.
            returned: on success of shutdown command submission.
            type: list



'''

from ansible.module_utils.basic import AnsibleModule

CANCEL = 'cancel'
IMMEDIATE = 'immediate'
JOB_ID = 'job_id'
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
            JOB_ID: {
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
