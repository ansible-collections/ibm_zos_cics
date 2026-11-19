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
    By default, the shutdown assist transaction specified in the SDTRAN system initialization parameter is used. If this is not set,
    the CICS-supplied shutdown assist transaction, CESD, is used instead. The task runs until the region has successfully shut down,
    or until the shutdown fails.
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
      - Specify C(cancel) to cancel the CICS region. This instructs the stop_region module to use the ZOAU C(jcan) utility to cancel the job.
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
      - If neither SDTRAN nor NOSDTRAN is specified, the value specified in the SDTRAN SIT parameter is used; or if this has not been set, the
        CICS-supplied shutdown assist transaction, CESD, is used instead.
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
      description: The raw output from the shell command execution.
      type: dict
      returned: always
      contains:
        rc:
          description: The return code from the shell command.
          type: int
          returned: always
        stdout:
          description: Standard output from the shell command.
          type: str
          returned: always
        stderr:
          description: Standard error from the shell command.
          type: str
          returned: always
        cmd:
          description: The shell command that was executed.
          type: str
          returned: always
msg:
  description: A string containing an error message if applicable.
  returned: always
  type: str
'''

import json
import subprocess

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils._zoau_version_checker import _check_zoau_version


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
        try:
            _check_zoau_version()
        except ImportError as e:
            self._module.fail_json(e.msg)
        # At this point, this module only gets executed with JOB_ID.
        # It wraps jls -j to normalise the output and surface a clean failure
        # when no job is found (jls exits non-zero with BGYSC3503E in that case).
        job_id = self._module.params.get(JOB_ID)

        jobs_raw: list[dict] = get_jobs_wrapper(job_id)

        if not jobs_raw:
            self._module.fail_json("No jobs found with id {0}".format(job_id))

        if len(jobs_raw) > 1:
            self._module.fail_json("Multiple jobs found with ID {0}".format(job_id))

        job = jobs_raw[0]

        no_name_msg = "Couldn't determine job name for job ID {0}".format(job_id)
        if job.get("id") != job_id:
            self._module.fail_json(no_name_msg)

        job_name = job.get("name")
        if not job_name:
            self._module.fail_json(no_name_msg)

        status = job.get("status", "")
        if not status:
            self._module.fail_json(
                "Couldn't determine status for job ID {0} with name {1}".format(job_id, job_name)
            )

        self._module.exit_json(
            changed=False,
            failed=False,
            job_name=job_name,
            job_status="EXECUTING" if status == "AC" else "NOT_EXECUTING"
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


def _parse_jls_response(jls_response):
    # type: (dict) -> list[dict]
    """Parse jls JSON output dict (must have a 'stdout' key). Returns list of job dicts."""
    stdout = jls_response.get("stdout", "")
    if not stdout.strip():
        return []
    try:
        data = json.loads(stdout)
    except (json.JSONDecodeError, ValueError):
        return []
    return list(data.get("data", {}).values())


def get_jobs_wrapper(job_id):  # type: (str) -> list[dict]
    """Query job status by ID using jls -j. Returns list of job dicts."""
    result = subprocess.run(
        "jls -j '{0}'".format(job_id),
        shell=True,
        capture_output=True,
        text=True,
        timeout=30,
        check=False
    )

    # RC 4 with BGYSC3503E means no job found — treat as empty list
    if result.returncode != 0:
        if "BGYSC3503E" in result.stderr:
            return []
        raise Exception("jls failed (RC {0}): {1}".format(result.returncode, result.stderr))

    try:
        jobs = _parse_jls_response({"stdout": result.stdout})
    except Exception:
        raise Exception("jls returned unexpected output: {0}".format(result.stdout))
    return jobs


def main():
    AnsibleStopCICSModule().main()


if __name__ == '__main__':
    main()
