# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

import time
import re
import logging
from ansible.plugins.action import ActionBase
from ansible_collections.ibm.ibm_zos_cics.plugins.modules.stop_cics import (
    JOB_ID, MODE, IMMEDIATE, CANCEL, SDTRAN, NO_SDTRAN)
from ansible.errors import AnsibleActionFail

ACTIVE_AND_WAITING = 'CICS is still active... waiting for successful shutdown.'
CANCEL_REGION = 'CANCEL {0}'
CICS_NOT_ACTIVE = 'CICS region is not active.'
CHECK_CICS_STATUS = 'z/OS Job Query - Checking status of job {0}'
EXECUTIONS = 'executions'
DEFAULT_SHUTDOWN = 'MODIFY {0},CEMT PERFORM SHUTDOWN'
FAILED = 'failed'
IMMEDIATE_SHUTDOWN = 'MODIFY {0},CEMT PERFORM SHUTDOWN IMMEDIATE'
JOB_NAME = 'job_name'
JOB_QUERY_FAILED = 'Job query failed.'
MODULE_NAME = 'ibm.ibm_zos_cics.stop_cics'
NAME = 'name'
RC = 'rc'
RETURN = 'return'
RUNNING_ATTEMPTING_TO_STOP = 'CICS is running, attempting to stop CICS.'
SHUTDOWN_FAILED = 'Shutdown Failed'
SHUTDOWN_REGION = 'Shutdown CICS'
SHUTDOWN_SUCCESS = 'CICS has been shutdown.'
SDTRAN_COMMAND = '{0} SDTRAN({1})'
NO_SDTRAN_COMMAND = '{0} NOSDTRAN'


class ActionModule(ActionBase):

    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        self.module_args = self._task.args.copy()

        self.result = {
            "failed": False,
            "changed": False,
            "msg": "",
            "executions": [],
        }

        self.result.update(
            self._execute_module(
                module_name=MODULE_NAME,
                module_args=self.module_args,
                task_vars=task_vars,
                tmp=tmp,
            )
        )
        if self.result.get(FAILED):
            return self.result

        self._configure(task_vars)

        try:
            self.shutdown_cics_region()
        except (AnsibleActionFail, KeyError) as e:
            self.result.update({"failed": True, "msg": e.args[0]})
        return self.result

    def _configure(self, task_vars):
        self.task_vars = task_vars
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.DEBUG)
        self.result = dict(changed=False, failed=False, executions=[])

    def shutdown_cics_region(self):  # type: () -> None
        region_running = self.is_job_running()
        self.result[EXECUTIONS].append({NAME: CHECK_CICS_STATUS.format(self.module_args[JOB_ID]), RETURN: self.jobs})
        if region_running:
            self.logger.debug(RUNNING_ATTEMPTING_TO_STOP)
            shutdown_result = self.run_shutdown_command(self.get_shutdown_command())
            self.result[EXECUTIONS].append({NAME: SHUTDOWN_REGION, RC: shutdown_result.pop(RC), RETURN: shutdown_result})

            self.get_console_errors(shutdown_result)
            self.result["changed"] = True

            self.wait_for_successful_shutdown()
        else:
            self.logger.debug(CICS_NOT_ACTIVE)

    def get_console_errors(self, shutdown_result):
        shutdown_stdout = "".join(shutdown_result.get("content", [])).replace(
            " ", "").replace("\n", "").upper()
        fail_pattern = r'CICSAUTOINSTALLFORCONSOLE[A-Z]{4}\d{4}HASFAILED'
        ignore_pattern = r'CONSOLE[A-Z]{4}\d{4}HASNOTBEENDEFINEDTOCICS.INPUTISIGNORED'

        if re.search(fail_pattern, shutdown_stdout):
            raise AnsibleActionFail(
                "Shutdown command failed because the auto-install of the console was unsuccessful. See executions for full command output.")
        if re.search(ignore_pattern, shutdown_stdout):
            raise AnsibleActionFail(
                "Shutdown command failed because the console used was not defined. See executions for full command output.")

    def wait_for_successful_shutdown(self):  # type: () -> None
        region_running = self.is_job_running()
        while region_running:
            self.logger.debug(ACTIVE_AND_WAITING)
            time.sleep(15)
            region_running = self.is_job_running()
        self.logger.debug(SHUTDOWN_SUCCESS)
        self.result[EXECUTIONS].append({NAME: CHECK_CICS_STATUS.format(self.module_args[JOB_ID]), RETURN: self.jobs})

    def is_job_running(self):  # type: () -> bool
        self.jobs = self._get_job_query_result()
        if self.jobs.get(FAILED):
            self.result[FAILED] = True
            raise AnsibleActionFail(JOB_QUERY_FAILED)

        # Get list of running jobs, if it's equal to 1, region is active, so return true
        return len([job for job in self.jobs["jobs"] if job["ret_code"] is None]) == 1

    def _get_job_query_result(self):  # type: () -> dict
        return self._execute_module(module_name="ibm.ibm_zos_core.zos_job_query",
                                    module_args={JOB_ID: self.module_args[JOB_ID]},
                                    task_vars=self.task_vars)

    def get_shutdown_command(self):  # type: () -> str
        job_name = self.jobs['jobs'][0][JOB_NAME]

        if self.module_args.get(MODE) == CANCEL:
            return CANCEL_REGION.format(job_name)

        shutdown_command = DEFAULT_SHUTDOWN.format(job_name)
        if self.module_args.get(MODE) == IMMEDIATE:
            shutdown_command = IMMEDIATE_SHUTDOWN.format(job_name)
        return self._get_shutdown_assistant_command(shutdown_command)

    def _get_shutdown_assistant_command(self, base_command):  # type: (str) -> str
        if self.module_args.get(SDTRAN):
            program = self.module_args[SDTRAN]
            return SDTRAN_COMMAND.format(base_command, program.upper())
        if self.module_args.get(NO_SDTRAN):
            return NO_SDTRAN_COMMAND.format(base_command)
        return base_command

    def run_shutdown_command(self, cmd):  # type: (str) -> dict
        shutdown_result = self._execute_module(
            module_name="ibm.ibm_zos_core.zos_operator",
            module_args={"cmd": cmd},
            task_vars=self.task_vars
        )
        if shutdown_result.get(FAILED):
            self.result[FAILED] = True
            raise AnsibleActionFail(SHUTDOWN_FAILED)
        return shutdown_result
