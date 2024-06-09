# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function
from datetime import datetime, timedelta

__metaclass__ = type

from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.stop_action_helper import (
    get_operator_shutdown_response,
    get_tso_status_response,
    get_job_query_result,
    CONSOLE_AUTOINSTALL_FAIL,
    CONSOLE_UNDEFINED,
)

# Required for mocking of datetime import in this file
import ansible_collections.ibm.ibm_zos_cics.plugins.action.stop_region as stop_region_action
from ansible_collections.ibm.ibm_zos_cics.plugins.action.stop_region import (
    get_console_errors,
    calculate_end_time,
    format_cancel_command,
    format_shutdown_command,
    _get_job_info_from_status,
    _get_job_name_from_query,
    _get_job_status_name_id,
)
from ansible.errors import AnsibleActionFail

try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock
import pytest


def test_calculate_end_time():
    now = datetime.now()
    timeout_seconds = 10
    stop_region_action.get_datetime_now = MagicMock(return_value=now)

    assert calculate_end_time(timeout_seconds) == now + \
        timedelta(0, timeout_seconds)


def test_format_cancel_command():
    job_name = "LINKJOB"
    job_id = "JOB12345"

    cmd = format_cancel_command(job_name, job_id)
    assert cmd == "jcan C LINKJOB JOB12345"


def test_format_shutdown_command_immediate():
    job_name = "LINKJOB"
    mode = "immediate"

    cmd = format_shutdown_command(job_name, mode)
    assert cmd == "MODIFY LINKJOB,CEMT PERFORM SHUTDOWN IMMEDIATE"


def test_format_shutdown_command_normal():
    job_name = "LINKJOB"
    mode = "normal"

    cmd = format_shutdown_command(job_name, mode)
    assert cmd == "MODIFY LINKJOB,CEMT PERFORM SHUTDOWN"


def test_format_shutdown_command_sd():
    job_name = "LINKJOB"
    mode = "normal"

    cmd = format_shutdown_command(job_name, mode, sdtran="DEFG")
    assert cmd == "MODIFY LINKJOB,CEMT PERFORM SHUTDOWN SDTRAN(DEFG)"


def test_format_shutdown_command_nosd():
    job_name = "LINKJOB"
    mode = "normal"

    cmd = format_shutdown_command(job_name, mode, no_sdtran=True)
    assert cmd == "MODIFY LINKJOB,CEMT PERFORM SHUTDOWN NOSDTRAN"


def test_console_error_valid():
    shutdown_result = get_operator_shutdown_response()
    try:
        # Assert void method does not error
        get_console_errors(shutdown_result)
        assert True
    except Exception as e:
        assert False, "'get_console_errors' raised exception {0}".format(
            str(e))


def test_console_error_undefined():
    shutdown_result = get_operator_shutdown_response(console=CONSOLE_UNDEFINED)

    with pytest.raises(AnsibleActionFail) as action_err:
        get_console_errors(shutdown_result)
    assert "Shutdown command failed because the console used was not defined" in str(
        action_err
    )


def test_console_error_install():
    shutdown_result = get_operator_shutdown_response(
        console=CONSOLE_AUTOINSTALL_FAIL)

    with pytest.raises(AnsibleActionFail) as action_err:
        get_console_errors(shutdown_result)
    assert (
        "Shutdown command failed because the auto-install of the console was unsuccessful"
        in str(action_err)
    )


def test_get_job_info_from_status_1_running():
    job_name = "JOBNAM"
    job_id = "JOB12345"
    tso_query_response = get_tso_status_response(
        jobname=job_name, running_job_id=job_id, stopped=0
    )

    assert _get_job_info_from_status(tso_query_response, job_name) == [
        {
            "job_name": job_name,
            "job_id": job_id,
            "status": "EXECUTING",
        }
    ]


def test_get_job_info_from_status_0_running():
    job_name = "JOBNAM"
    tso_query_response = get_tso_status_response(
        jobname=job_name, stopped=0, running=0)
    assert _get_job_info_from_status(tso_query_response, job_name) == []


def test_get_job_info_from_status_2_running():
    job_name = "JOBNAM"
    job_id = "JOB12345"
    tso_query_response = get_tso_status_response(
        jobname=job_name, running_job_id=job_id, stopped=0, running=2
    )

    assert _get_job_info_from_status(tso_query_response, job_name) == [
        {
            "job_name": job_name,
            "job_id": job_id,
            "status": "EXECUTING",
        },
        {
            "job_name": job_name,
            "job_id": job_id,
            "status": "EXECUTING",
        },
    ]


def test_get_job_info_from_status_0_running_1_stopped():
    job_name = "JOBNAM"
    job_id = "JOB12345"
    tso_query_response = get_tso_status_response(
        jobname=job_name, stopped_job_id=job_id, running=0
    )

    assert _get_job_info_from_status(tso_query_response, job_name) == [
        {
            "job_name": job_name,
            "job_id": job_id,
            "status": "ON OUTPUT QUEUE",
        },
    ]


def test_get_job_info_from_status_0_running_2_stopped():
    job_name = "JOBNAM"
    job_id = "JOB12345"
    tso_query_response = get_tso_status_response(
        jobname=job_name, stopped_job_id=job_id, running=0, stopped=2
    )

    assert _get_job_info_from_status(tso_query_response, job_name) == [
        {
            "job_name": job_name,
            "job_id": job_id,
            "status": "ON OUTPUT QUEUE",
        },
        {
            "job_name": job_name,
            "job_id": job_id,
            "status": "ON OUTPUT QUEUE",
        },
    ]


def test_get_job_info_from_status_1_running_2_stopped():
    job_name = "JOBNAM"
    job_id = "JOB12345"
    stopped_id = "JOB98765"
    tso_query_response = get_tso_status_response(
        jobname=job_name, running_job_id=job_id, stopped_job_id=stopped_id, stopped=2
    )

    assert _get_job_info_from_status(tso_query_response, job_name) == [
        {
            "job_name": job_name,
            "job_id": job_id,
            "status": "EXECUTING",
        },
        {
            "job_name": job_name,
            "job_id": stopped_id,
            "status": "ON OUTPUT QUEUE",
        },
        {
            "job_name": job_name,
            "job_id": stopped_id,
            "status": "ON OUTPUT QUEUE",
        },
    ]


def test_get_job_name_from_query():
    job_name = "JOBNAM"
    job_id = "JOB12345"
    job_query_response = get_job_query_result(jobname=job_name)

    assert _get_job_name_from_query(job_query_response, job_id) == job_name


def test_get_job_name_from_query_failed():
    job_name = "JOBNAM"
    job_id = "JOB12345"
    job_query_response = get_job_query_result(jobname=job_name, failed=True)

    with pytest.raises(AnsibleActionFail) as action_err:
        _get_job_name_from_query(job_query_response, job_id)
    assert "Job query failed - (No failure message provided by zos_job_query)" in str(
        action_err
    )


def test_get_job_name_from_query_failed_msg():
    job_name = "JOBNAM"
    job_id = "JOB12345"
    job_query_response = get_job_query_result(
        jobname=job_name, failed=True, message="MEANINGFUL MSG FROM CORE"
    )

    with pytest.raises(AnsibleActionFail) as action_err:
        _get_job_name_from_query(job_query_response, job_id)
    assert "Job query failed - MEANINGFUL MSG FROM CORE" in str(action_err)


def test_get_job_name_from_query_0_jobs():
    job_name = "JOBNAM"
    job_id = "JOB12345"
    job_query_response = get_job_query_result(jobname=job_name, jobs=0)

    with pytest.raises(AnsibleActionFail) as action_err:
        _get_job_name_from_query(job_query_response, job_id)
    assert "No jobs found with id {0}".format(job_id) in str(action_err)


def test_get_job_name_from_query_missing_jobs():
    job_name = "JOBNAM"
    job_id = "JOB12345"
    job_query_response = get_job_query_result(
        jobname=job_name, no_jobs_found=True)

    with pytest.raises(AnsibleActionFail) as action_err:
        _get_job_name_from_query(job_query_response, job_id)
    assert "No jobs found with id {0}".format(job_id) in str(action_err)


def test_get_job_name_from_query_multiple_jobs():
    job_name = "JOBNAM"
    job_id = "JOB12345"
    job_query_response = get_job_query_result(jobname=job_name, jobs=2)

    with pytest.raises(AnsibleActionFail) as action_err:
        _get_job_name_from_query(job_query_response, job_id)
    assert "Multiple jobs found with ID {0}".format(job_id) in str(action_err)


def test_get_job_status_name_id():
    job_name = "JOBNAM"
    job_id = "JOB12345"
    stopped_id = "JOB98765"
    tso_query_response = get_tso_status_response(
        jobname=job_name, running_job_id=job_id, stopped_job_id=stopped_id
    )
    assert _get_job_status_name_id(
        tso_query_response, job_name, job_id) == "EXECUTING"


def test_get_job_status_name_id_no_output():
    job_name = "JOBNAM"
    job_id = "JOB12345"
    with pytest.raises(AnsibleActionFail) as action_err:
        _get_job_status_name_id({}, job_name, job_id)
    assert "Output not received for TSO STATUS command" in str(action_err)


def test_get_job_status_name_id_0_jobs():
    job_name = "JOBNAM"
    job_id = "JOB12345"
    tso_query_response = get_tso_status_response(
        jobname=job_name, running=0, stopped=0)
    with pytest.raises(AnsibleActionFail) as action_err:
        _get_job_status_name_id(tso_query_response, job_name, job_id)
    assert "No jobs found with name {0} and ID {1}".format(job_name, job_id) in str(
        action_err
    )


def test_get_job_status_name_id_2_jobs():
    job_name = "JOBNAM"
    job_id = "JOB12345"
    tso_query_response = get_tso_status_response(
        jobname=job_name, running=2, stopped=0)
    with pytest.raises(AnsibleActionFail) as action_err:
        _get_job_status_name_id(tso_query_response, job_name, job_id)
    assert "Multiple jobs with name and ID found" in str(action_err)
