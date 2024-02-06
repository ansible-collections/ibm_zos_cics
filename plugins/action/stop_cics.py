# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

import time
import logging
from ansible.plugins.action import ActionBase
from ansible_collections.ibm.ibm_zos_cics.plugins.modules.stop_cics import (
    JOB_NAME, IMMEDIATE)
from ansible.errors import AnsibleActionFail

ACTIVE_AND_WAITING = 'CICS is still active... waiting for successful shutdown.'
CHECK_CICS_STATUS = 'Check CICS status'
EXECUTIONS = 'executions'
FAILED = 'failed'
IMMEDIATE = 'immediate'
JOB_NAME = 'job_name'
RUNNING_ATTEMPTING_TO_STOP = 'CICS is running, attempting to stop CICS.'
SHUTDOWN_REGION = 'Shutdown CICS'
CICS_NOT_ACTIVE = 'CICS region is not active.'
SHUTDOWN_SUCCESS = 'CICS has been shutdown.'
MODULE_NAME = 'ibm.ibm_zos_cics.stop_cics'
DEFAULT_SHUTDOWN = 'MODIFY {},CEMT PERFORM SHUTDOWN'
IMMEDIATE_SHUTDOWN = 'MODIFY {},CEMT PERFORM SHUTDOWN IMMEDIATE'
SHUTDOWN_FAILED = 'Shutdown Failed'


class ActionModule(ActionBase):

    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        self.module_args = self._task.args.copy()
        module_return = self._execute_module(module_name=MODULE_NAME, module_args=self.module_args, task_vars=task_vars,
                                             tmp=tmp)
        if module_return.get(FAILED):
            return module_return

        self._configure(task_vars)
        self.shutdown_cics_region()
        return self.result

    def _configure(self, task_vars):
        self.task_vars = task_vars
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.DEBUG)
        self.result = dict(changed=False, failed=False, executions=[])

    def shutdown_cics_region(self):  # type: () -> None
        region_running, result = self.is_job_running()
        self.result[EXECUTIONS].append({CHECK_CICS_STATUS: result})
        if region_running:
            self.logger.debug(RUNNING_ATTEMPTING_TO_STOP)
            self.result[EXECUTIONS].append({SHUTDOWN_REGION : self.run_shutdown_command(self.get_shutdown_command())})
            self.wait_for_successful_shutdown()
        else:
            self.logger.debug(CICS_NOT_ACTIVE)

    def wait_for_successful_shutdown(self):  # type: () -> None
        region_running, result = self.is_job_running()
        while region_running:
            self.logger.debug(ACTIVE_AND_WAITING)
            region_running, result = self.is_job_running()
            time.sleep(15)
        self.logger.debug(SHUTDOWN_SUCCESS)
        self.result[EXECUTIONS].append({CHECK_CICS_STATUS: result})

    def is_job_running(self):  # type: () -> tuple[bool, dict]
        result = self._get_job_query_result()
        if result.get(FAILED) is True:
            self.result[FAILED] = True
            raise AnsibleActionFail("Job Query Failed")

        # Get list of running jobs, if it's equal to 1, region is active (as cant have more than 1 running job), so
        # return true and also return query result to append to executions where needed.
        return len([job for job in result["jobs"] if job["ret_code"] is None]) == 1, result

    def _get_job_query_result(self):  # type: () -> dict
        return self._execute_module(module_name="ibm.ibm_zos_core.zos_job_query",
                                    module_args=dict(job_name=self.module_args[JOB_NAME]),
                                    task_vars=self.task_vars)

    def get_shutdown_command(self):  # type: () -> str
        job_name = self.module_args[JOB_NAME]

        if self.module_args.get(IMMEDIATE) is True:
            return DEFAULT_SHUTDOWN.format(job_name)
        else:
            return IMMEDIATE_SHUTDOWN.format(job_name)

    def run_shutdown_command(self, cmd):  # type: (str) -> dict
        shutdown_result = self._execute_module(
            module_name="ibm.ibm_zos_core.zos_operator",
            module_args=dict(cmd=cmd),
            task_vars=self.task_vars
        )
        if shutdown_result.get(FAILED) is True:
            self.result[FAILED] = True
            raise AnsibleActionFail(SHUTDOWN_FAILED)
        return shutdown_result
