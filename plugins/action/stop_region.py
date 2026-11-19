# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

import time
import re
import logging
from ansible.plugins.action import ActionBase
from ansible_collections.ibm.ibm_zos_cics.plugins.modules.stop_region import (
    JOB_ID,
    MODE,
    IMMEDIATE,
    CANCEL,
    SDTRAN,
    NO_SDTRAN,
    JOB_NAME,
    TIMEOUT,
    TIMEOUT_DEFAULT,
    _parse_jls_response,
)
from ansible.errors import AnsibleActionFail
from datetime import datetime, timedelta

logging.basicConfig(level=logging.DEBUG)

ACTIVE_AND_WAITING = "CICS is still active... waiting for successful shutdown."
CANCEL_REGION = "CANCEL {0}"
CHECK_CICS_STATUS = "Checking status of job {0}"
EXECUTIONS = "executions"
DEFAULT_SHUTDOWN = "MODIFY {0},CEMT PERFORM SHUTDOWN"
FAILED = "failed"
CHANGED = "changed"
MSG = "msg"
EXECUTING = "EXECUTING"
STATUS = "status"
IMMEDIATE_SHUTDOWN = "MODIFY {0},CEMT PERFORM SHUTDOWN IMMEDIATE"
STOP_MODULE_NAME = "ibm.ibm_zos_cics.stop_region"
NAME = "name"
RC = "rc"
RETURN = "return"
RUNNING_ATTEMPTING_TO_STOP = "CICS is running, attempting to stop CICS."
SHUTDOWN_SUCCESS = "CICS has been shutdown."
SDTRAN_COMMAND = "{0} SDTRAN({1})"
NO_SDTRAN_COMMAND = "{0} NOSDTRAN"
JLS_NAME_COMMAND = "jls -j '/*/{0}'"
JLS_ID_COMMAND = "jls -j '{0}'"


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        self._setup(tmp, task_vars)

        self.job_name, self.job_id, self.stop_mode, self.sdtran, self.no_sdtran, self.timeout = validate_module_params(
            self.module_args.get(JOB_NAME),
            self.module_args.get(JOB_ID),
            self.module_args.get(MODE),
            self.module_args.get(SDTRAN),
            self.module_args.get(NO_SDTRAN),
            self.module_args.get(TIMEOUT, TIMEOUT_DEFAULT)
        )

        self.job_status = EXECUTING

        try:
            self._get_job_data()
        except AnsibleActionFail as e:
            self.failed = True
            return self.get_result(e.args[0])

        if not self.job_id or not self.job_name or self.job_status != EXECUTING:
            return self.get_result()

        self.logger.debug(RUNNING_ATTEMPTING_TO_STOP)
        try:
            if self.stop_mode == CANCEL:
                self._cancel_region()
            else:
                self._perform_shutdown()
        except AnsibleActionFail as e:
            self.failed = True
            return self.get_result(e.args[0])

        try:
            self.wait_for_shutdown()
            self.changed = True
        except TimeoutError as e:
            self.failed = True
            self.msg = e.args[0]

        return self.get_result()

    def _cancel_region(self):
        run_command_result = self.execute_cancel_shell_cmd(
            self.job_name, self.job_id)
        if run_command_result.get(RC) != 0:
            raise AnsibleActionFail("Error running job cancel command")

    def _perform_shutdown(self):
        shutdown_command = format_shutdown_command(
            self.job_name, self.stop_mode, self.sdtran, self.no_sdtran
        )
        shutdown_output = self.execute_zos_operator_cmd(shutdown_command)
        get_console_errors(shutdown_output)

    def _setup(self, tmp, task_vars):
        super(ActionModule, self).run(tmp, task_vars)
        self.task_vars = task_vars
        self.tmp = tmp
        self.module_args = self._task.args.copy()
        self.logger = logging.getLogger(__name__)

        self.failed = False
        self.changed = False
        self.msg = ""
        self.executions = []

    def get_result(self, msg=None):
        return {
            FAILED: self.failed,
            CHANGED: self.changed,
            MSG: msg if msg else self.msg,
            EXECUTIONS: self.executions,
        }

    def _get_job_data(self):
        if self.job_id and self.job_name:
            self.job_status = self._get_job_status_by_name_and_id()
        elif self.job_name:
            self.job_id, self.job_status = self._get_job_id_and_status_by_name()
        elif self.job_id:
            self.job_name, self.job_status = self._get_job_name_and_status_by_id()
        else:
            raise Exception("Neither job_name nor job_id was set.  This shouldn't happen according to the argument spec")

    def _get_job_status_by_name_and_id(self):  # type: () -> str
        jls_response = self.execute_jls_cmd(job_name=self.job_name)
        self._add_status_execution("{0}({1})".format(
            self.job_name, self.job_id), jls_response)
        return _get_job_status_name_id(
            jls_response, self.job_name, self.job_id
        )

    def _get_job_id_and_status_by_name(self):  # type: () -> (str, str)
        # If we have a name but no ID, we use a TSO command to get the job ID
        running_jobs = self._get_running_jobs()

        if len(running_jobs) == 0:
            return (None, "MISSING")

        if len(running_jobs) > 1:
            raise AnsibleActionFail(
                "Cannot disambiguate between multiple running jobs with the same name ({0}). Use `job_id` as a parameter to specify the correct job.".format(
                    self.job_name))

        return (running_jobs[0][JOB_ID], running_jobs[0][STATUS])

    def _get_job_name_and_status_by_id(self):  # type: () -> (str, str)
        # We're going to execute this via the stop_region module, to massage the response format into something sensible
        stop_module_output = self._execute_module(
            module_name=STOP_MODULE_NAME,
            module_args={JOB_ID: self.job_id},
            task_vars=self.task_vars,
        )

        self.executions.append({
            NAME: "Get job name and status for job ID {0}".format(self.job_id),
            RC: 1 if stop_module_output.get("failed") else 0,
            RETURN: stop_module_output,
        })

        if stop_module_output.get("failed"):
            raise AnsibleActionFail(
                message=stop_module_output.get("msg", "Failure getting job name and status from ID")
            )

        return (stop_module_output["job_name"], stop_module_output["job_status"])

    def _get_running_jobs(self):
        jls_response = self.execute_jls_cmd(job_name=self.job_name)
        self._add_status_execution(self.job_name, jls_response)
        jobs = _get_job_info_from_status(jls_response, self.job_name)
        if len(jobs) == 0:
            raise AnsibleActionFail(
                "Job with name {0} not found".format(self.job_name))

        running = []
        for job in jobs:
            if job[STATUS] == EXECUTING:
                running.append(job)
        return running

    def _add_status_execution(self, job, result):
        self.executions.append({
            NAME: CHECK_CICS_STATUS.format(job),
            RC: result.get("rc"),
            RETURN: result,
        })

    def wait_for_shutdown(self):
        end_time = calculate_end_time(
            self.timeout) if self.timeout > 0 else None

        status = EXECUTING
        while status == EXECUTING and (
            get_datetime_now() < end_time if end_time else True
        ):
            self.logger.debug(ACTIVE_AND_WAITING)
            time.sleep(15)

            jls_response = self.execute_jls_cmd(job_name=self.job_name)

            self._add_status_execution(self.job_id, jls_response)

            status = _get_job_status_name_id(
                jls_response, self.job_name, self.job_id
            )

        if status == EXECUTING:
            raise TimeoutError(
                "Timeout reached before region successfully stopped")
        self.logger.debug(SHUTDOWN_SUCCESS)

    def _execute_remote_cmd(self, command):
        """Run a shell command on the remote z/OS host via the command action plugin."""
        saved_args = self._task.args
        try:
            self._task.args = {
                "_uses_shell": True,
                "_raw_params": command,
            }
            command_action = self._shared_loader_obj.action_loader.get(
                "ansible.legacy.command",
                task=self._task,
                connection=self._connection,
                play_context=self._play_context,
                loader=self._loader,
                templar=self._templar,
                shared_loader_obj=self._shared_loader_obj,
            )
            return command_action.run(task_vars=self.task_vars)
        finally:
            self._task.args = saved_args

    def execute_jls_cmd(self, job_name=None, job_id=None):
        """Query job status using jls -j on the remote z/OS host."""
        if job_name:
            jls_cmd = JLS_NAME_COMMAND.format(job_name)
        else:
            jls_cmd = JLS_ID_COMMAND.format(job_id)
        return self._execute_remote_cmd(jls_cmd)

    def execute_zos_operator_cmd(self, command):
        """Execute operator command using opercmd -j."""
        result = self._execute_remote_cmd("opercmd -j \"{0}\"".format(command))
        self.executions.append({
            NAME: "Operator Command - {0}".format(command),
            RC: result.get("rc"),
            RETURN: result,
        })
        return result

    def execute_cancel_shell_cmd(self, job_name, job_id):
        cancel_response = self._execute_remote_cmd(
            "jcan C {0} {1}".format(job_name, job_id)
        )
        self.executions.append({
            NAME: "Cancel command - {0}({1})".format(job_name, job_id),
            RC: cancel_response.get("rc"),
            RETURN: cancel_response,
        })
        return cancel_response


def validate_module_params(job_name, job_id, stop_mode, sdtran, no_sdtran, timeout):
    if not job_id and not job_name:
        raise AnsibleActionFail("At least one of {0} or {1} must be specified".format(
            JOB_ID, JOB_NAME))

    if sdtran and len(sdtran) > 4:
        raise AnsibleActionFail(
            "Value: {0}, is invalid. SDTRAN value must be  1-4 characters.".format(sdtran)
        )

    return (job_name, job_id, stop_mode, sdtran, no_sdtran, timeout)


def get_datetime_now():
    return datetime.now()


def calculate_end_time(timeout_seconds: int) -> datetime:
    now = get_datetime_now()
    offset = timedelta(0, timeout_seconds)
    return now + offset


def format_cancel_command(job_name, job_id):
    return "jcan C {0} {1}".format(job_name, job_id)


def format_shutdown_command(job_name, stop_mode, sdtran=None, no_sdtran=None):
    shutdown_command = DEFAULT_SHUTDOWN.format(job_name)
    if stop_mode == IMMEDIATE:
        shutdown_command = IMMEDIATE_SHUTDOWN.format(job_name)

    if sdtran:
        return SDTRAN_COMMAND.format(shutdown_command, sdtran.upper())
    if no_sdtran:
        return NO_SDTRAN_COMMAND.format(shutdown_command)

    return shutdown_command


def get_console_errors(shutdown_result):
    shutdown_stdout = (
        shutdown_result.get("stdout", "")
        .replace(" ", "")
        .replace("\n", "")
        .upper()
    )
    fail_pattern = r"CICSAUTOINSTALLFORCONSOLE[A-Z]{4}\d{4}HASFAILED"
    ignore_pattern = r"CONSOLE[A-Z]{4}\d{4}HASNOTBEENDEFINEDTOCICS.INPUTISIGNORED"

    if re.search(fail_pattern, shutdown_stdout):
        raise AnsibleActionFail(
            "Shutdown command failed because the auto-install of the console was unsuccessful. See executions for full command output."
        )
    if re.search(ignore_pattern, shutdown_stdout):
        raise AnsibleActionFail(
            "Shutdown command failed because the console used was not defined. See executions for full command output."
        )


def _get_job_info_from_status(jls_response, job_name):
    """Parse jls response for jobs matching job_name. Returns list of {job_name, job_id, status}."""
    jobs = _parse_jls_response(jls_response)
    result = []
    for job in jobs:
        if job.get("name", "").upper() == job_name.upper():
            status = "EXECUTING" if job.get("status") == "AC" else job.get("status", "")
            result.append({
                JOB_NAME: job.get("name"),
                JOB_ID: job.get("id"),
                STATUS: status,
            })
    return result


def _get_job_status_name_id(jls_response, job_name, job_id):
    """Parse jls response for a specific job_name + job_id. Returns status string."""
    if not jls_response:
        raise AnsibleActionFail("Output not received for job status command")
    jobs = _parse_jls_response(jls_response)
    matches = [
        j for j in jobs
        if j.get("name", "").upper() == job_name.upper()
        and j.get("id", "").upper() == job_id.upper()
    ]
    if len(matches) == 0:
        raise AnsibleActionFail(
            "No jobs found with name {0} and ID {1}".format(job_name, job_id))
    if len(matches) > 1:
        raise AnsibleActionFail("Multiple jobs with name and ID found")
    job = matches[0]
    return "EXECUTING" if job.get("status") == "AC" else job.get("status", "")
