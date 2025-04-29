#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: stop_region
short_description: Stop a CICS region
description:
  - Stop a CICS region by issuing a CEMT PERFORM SHUTDOWN command, or by canceling the job through the C(jobs.cancel) utility provided by
    Z Open Automation Utilities (ZOAU). You can choose the shutdown mode from NORMAL, IMMEDIATE, or CANCEL.
  - The O(job_id), O(job_name), or both can be used to shut down a CICS region. If mulitple jobs are running with the same name, the O(job_id) is required.
  - During a NORMAL or IMMEDIATE shutdown, a shutdown assist transaction should run to enable CICS to shut down in a controlled manner.
    By default, the CICS-supplied shutdown assist transaction, CESD is used. You can specify a custom shutdown assist transaction in the
    SDTRAN system initialization parameter. The task runs until the region has successfully shut down, or until the shutdown fails.
  - You must have a console installed in the CICS region so that the stop_region module can communicate with CICS. To define a console,
    you must install a terminal with the CONSNAME attribute set to your TSO user ID. For detailed instructions, see
    L(Defining TSO users as console devices,https://www.ibm.com/docs/en/cics-ts/latest?topic=cics-defining-tso-users-as-console-devices).
    Add your console definition into one of the resource lists defined on the GRPLIST system initialization parameter so that it gets
    installed into the CICS region.
    Alternatively, you can use a DFHCSDUP script to update an existing CSD. This function is provided by the csd module.
  - You can specify a timeout, in seconds, for CICS shutdown processing. After a request to stop CICS is issued, if CICS shutdown processing is not
    completed when this timeout is reached, the module completes in a failed state. By default, the stop_region module does not use a timeout, that is,
    the O(timeout) parameter assumes a value of -1.
version_added: 2.1.0
author:
  - Kiera Bennett (@KieraBennett)
options:
  job_id:
    description:
      - Identifies the job ID belonging to the running CICS region.
      - The stop_region module uses this job ID to identify the state of the CICS region and shut it down.
    type: str
    required: false
  job_name:
    description:
      - Identifies the job name belonging to the running CICS region.
      - The stop_region module uses this job name to identify the state of the CICS region and shut it down.
      - The O(job_name) must be unique; if multiple jobs with the same name are running, use O(job_id).
    type: str
    required: false
  mode:
    description:
      - Specify the type of shutdown to be executed on the CICS region.
      - Specify C(normal) to perform a normal shutdown. This instructs the stop_region module to issue a CEMT PERFORM SHUTDOWN command.
      - Specify C(immediate) to perform an immediate shutdown. This instructs the stop_region module to issue a CEMT PERFORM SHUTDOWN IMMEDIATE command.
      - Specify C(cancel) to cancel the CICS region. This instructs the stop_region module to use ZOAU's C(jobs.cancel) utility to process the request.
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
  timeout:
    description:
      - The maximum time, in seconds, to wait for CICS shutdown processing to complete.
      - Specify -1 to exclude a timeout.
    type: int
    default: -1
    required: false
'''


EXAMPLES = r'''
- name: "Stop CICS region using job ID"
  ibm.ibm_zos_cics.stop_region:
    job_id: JOB12345

- name: "Stop CICS region immediately using job ID"
  ibm.ibm_zos_cics.stop_region:
    job_id: JOB12354
    mode: immediate

- name: "Stop CICS region using job name and job ID"
  ibm.ibm_zos_cics.stop_region:
    job_id: JOB12354
    job_name: MYREG01

- name: "Stop CICS region using job name"
  ibm.ibm_zos_cics.stop_region:
    job_name: ANS1234
    mode: normal

- name: "Cancel CICS region using job name"
  ibm.ibm_zos_cics.stop_region:
    job_name: ANS1234
    mode: cancel
'''

RETURN = r'''
changed:
  description: True if the PERFORM SHUTDOWN or CANCEL command was executed.
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
      returned: always
    return:
      description: The standard output returned by the program execution.
      type: dict
      returned: always
      contains:
        changed:
          description: True if the state was changed, otherwise False.
          returned: always
          type: bool
        failed:
          description: True if the module failed, otherwise False.
          returned: always
          type: bool
        jobs:
          description: The output information for a list of jobs matching the specified criteria.
          type: list
          returned: on zos_job_query module execution
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
          returned: on zos_job_query module execution
          type: str
        content:
          description: The resulting text from the command submitted.
          returned: on zos_operator module execution
          type: list
        cmd:
          description: The operator command that has been executed
          returned: on zos_operator module execution
          type: str
        rc:
          description: The return code from the operator command
          returned: on zos_operator module execution
          type: int
        max_rc:
          description: The maximum return code from the TSO status command
          returned: on zos_tso_command module execution
          type: int
        output:
          description: The output from the TSO command.
          returned: on zos_tso_command module execution
          type: list
          elements: dict
          contains:
            command:
              description: The executed TSO command.
              returned: always
              type: str
            rc:
              description: The return code from the executed TSO command.
              returned: always
              type: int
            content:
              description: The response resulting from the execution of the TSO command.
              returned: always
              type: list
            lines:
              description: The line number of the content.
              returned: always
              type: int

msg:
  description: A string containing an error message if applicable.
  returned: always
  type: str
'''

import traceback

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.job import job_status

from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.import_handler import (
    ZOAUImportError
)

try:
    from zoautil_py.exceptions import JobFetchException
except Exception:
    # Use ibm_zos_core's approach to handling zoautil_py imports so sanity tests pass
    datasets = ZOAUImportError(traceback.format_exc())


CANCEL = 'cancel'
IMMEDIATE = 'immediate'
JOB_ID = 'job_id'
JOB_NAME = 'job_name'
MODE = 'mode'
NORMAL = 'normal'
NO_SDTRAN = 'no_sdtran'
SDTRAN = 'sdtran'
TIMEOUT = 'timeout'
TIMEOUT_DEFAULT = -1


class AnsibleStopCICSModule(object):

    def __init__(self):
        self._module = AnsibleModule(
            argument_spec=self.init_argument_spec(),
            mutually_exclusive=[(SDTRAN, NO_SDTRAN)],
            required_one_of=[(JOB_ID, JOB_NAME)],
        )
        self.failed = False
        self.msg = ""

    def main(self):
        # At this point, this module only gets executed with JOB_ID
        # This is as a wrapper to jls via ibm_zos_core job to clean-up the output
        # if there is no job found with that ID (ZOAU throws an exception)
        job_id = self._module.params.get(JOB_ID)

        jobs_raw: list[dict] = get_jobs_wrapper(job_id)

        if not jobs_raw:
            self._module.fail_json("No jobs found with id {0}".format(job_id))

        if len(jobs_raw) > 1:
            self._module.fail_json("Multiple jobs found with ID {0}".format(job_id))

        job = jobs_raw[0]

        no_name_msg = "Couldn't determine job name for job ID {0}".format(job_id)
        if not job.get("job_id") == job_id:
            self._module.fail_json(no_name_msg)

        job_name = job.get("job_name")
        if not job_name:
            self._module.fail_json(no_name_msg)

        no_status_msg = "Couldn't determine status for job ID {0} with name {1}".format(job_id, job_name)
        ret_code = job.get("ret_code")
        if not ret_code:
            self._module.fail_json(no_status_msg)

        status = ret_code.get("msg")
        if not status:
            self._module.fail_json(no_status_msg)

        self._module.exit_json(
            changed=False,
            failed=False,
            job_name=job["job_name"],
            job_status="EXECUTING" if "AC" in status else "NOT_EXECUTING"
        )

    def init_argument_spec(self):
        return {
            JOB_ID: {
                'type': 'str',
                'required': False,
            },
            JOB_NAME: {
                'type': 'str',
                'required': False,
            },
            MODE: {
                'type': 'str',
                'required': False,
                'default': NORMAL,
                'choices': [NORMAL, IMMEDIATE, CANCEL],
            },
            SDTRAN: {
                'type': 'str',
                'required': False,
            },
            NO_SDTRAN: {
                'type': 'bool',
                'required': False,
                'default': False,
            },
            TIMEOUT: {
                'type': 'int',
                'required': False,
                'default': TIMEOUT_DEFAULT,
            }
        }


def get_jobs_wrapper(job_id):  # type: (str) -> list[dict]
    try:
        return job_status(job_id=job_id)
    except JobFetchException as e:
        response = e.response

        # ZOAU 1.3 returns an error with this message if there's no job with the expected ID
        if "BGYSC3503E Failed to retrieve job list." in response.stderr_response:
            # In this case, we'll clean up the error, so the user gets a clearer response
            return []
        else:
            # Otherwise something unexpected happened
            raise e


def main():
    if __name__ == '__main__':
        AnsibleStopCICSModule().main()


if __name__ == '__main__':
    main()
