#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: stop_cics
short_description: Stop a CICS region
description:
  - Stop a CICS region by using CEMT PERFORM SHUTDOWN. You can choose to perform a NORMAL or IMMEDIATE shutdown.
  - During a NORMAL or IMMEDIATE shutdown, a shutdown assist program should run to enable CICS to shut down in a controlled manner.
    By default, the CICS-supplied shutdown assist transaction, CESD is used. You can specify a custom shutdown assist program in the
    SDTRAN system initialization parameter. The task runs until the region has successfully shut down, or until the shutdown fails.
  - You must have a console installed in the CICS region so that the stop_cics module can communicate with CICS. To define a console,
    you must install a terminal with the CONSNAME attribute set to your TSO user ID. For detailed instructions, see
    L(Defining TSO users as console devices,https://www.ibm.com/docs/en/cics-ts/6.1?topic=cics-defining-tso-users-as-console-devices).
    Add your console definition into one of the resource lists defined on the GRPLIST system initialization parameter so that it gets
    installed into the CICS region.
    Alternatively, you can use a DFHCSDUP script to update an existing CSD. This function is provided by the csd module.
version_added: 1.1.0-beta.5
author:
  - Kiera Bennett (@KieraBennett)
options:
  job_id:
    description:
      - Identifies the job ID belonging to the running CICS region.
      - The stop_cics module uses this job ID to identify the state of the CICS region and shut it down.
    type: str
    required: true
  mode:
    description:
      - Specify the type of shutdown to be executed on the CICS region.
    type: str
    required: false
    default: normal
    choices:
      - normal
      - immediate
      - cancel
  sdtran:
    description:
      - The 4-character identifier of the shutdown assist transaction.
      - The default shutdown transaction, if neither SDTRAN nor NOSDTRAN is specified, is CESD.
    type: str
    required: false
  no_sdtran:
    description:
      - No shutdown assist transaction is to be run at CICS shutdown.
    type: bool
    default: false
    required: false
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
  description: True if the PERFORM SHUTDOWN command was executed.
  returned: always
  type: bool
failed:
  description: True if the Ansible task failed, otherwise False.
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
                Return code output collected from the job log.
              type: dict
              contains:
                msg:
                  description:
                    Return code or abend resulting from the job submission.
                  type: str
                msg_code:
                  description:
                    Return code extracted from the `msg` so that it can be evaluated.
                    For example, ABEND(S0C4) yields "S0C4".
                  type: str
                msg_txt:
                  description:
                    Returns additional information related to the job.
                  type: str
                code:
                  description:
                    Return code converted to an integer value (when possible).
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
          returned: on success of PERFORM SHUTDOWN command submission.
          type: list
msg:
  description: A string containing an error message if applicable
  returned: always
  type: str
'''

from ansible.module_utils.basic import AnsibleModule

CANCEL = 'cancel'
IMMEDIATE = 'immediate'
JOB_ID = 'job_id'
MODE = 'mode'
NORMAL = 'normal'
NO_SDTRAN = 'no_sdtran'
SDTRAN = 'sdtran'


class AnsibleStopCICSModule(object):

    def __init__(self):
        self._module = AnsibleModule(
            argument_spec=self.init_argument_spec(), mutually_exclusive=[('sdtran', 'no_sdtran')],
        )
        self.changed = False
        self.failed = False
        self.executions = []

    def main(self):
        if self._module.params.get(SDTRAN):
            self._validate_sdtran(self._module.params[SDTRAN])
        self._module.exit_json()

    def _validate_sdtran(self, program):  # type: (str) -> None
        if len(program) > 4:
            self._fail("Value: {0}, is invalid. SDTRAN value must be  1-4 characters.".format(program))

    def _fail(self, msg):  # type: (str) -> None
        self.failed = True
        self.msg = msg
        self.result = self.get_result()
        self._module.fail_json(**self.result)

    def get_result(self):  # type: () -> dict
        return {
            "changed": self.changed,
            "failed": self.failed,
            "executions": self.executions,
            "msg": self.msg
        }

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
            SDTRAN: {
                'type': 'str',
                'required': False
            },
            NO_SDTRAN: {
                'type': 'bool',
                'required': False,
                'default': False,
            }
        }


def main():
    if __name__ == '__main__':
        AnsibleStopCICSModule().main()


if __name__ == '__main__':
    main()
