# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
import pytest

from mock import MagicMock
from ansible_collections.ibm.ibm_zos_cics.plugins.modules import (
    stop_region
)

from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.data_set_helper import (
    set_module_args
)

DEFAULT_JOB_ID = "ANS12345"
DEFAULT_MODE = "normal"
class AnsibleExitJson(Exception):
    def __init__(self, args, kwargs) -> None:
        self.args = args
        self.kwargs = kwargs

class AnsibleFailJson(Exception):
    def __init__(self, args, kwargs) -> None:
        self.args = args
        self.kwargs = kwargs

def exit_json(*args, **kwargs):
    if 'changed' not in kwargs:
        kwargs['changed'] = False
    raise AnsibleExitJson(args, kwargs)

def fail_json(*args, **kwargs):
    if 'changed' not in kwargs:
        kwargs['changed'] = False
    raise AnsibleFailJson(args, kwargs)


def initialise_module(monkeypatch, **kwargs):
    initial_args = {
        "job_id": DEFAULT_JOB_ID,
        "mode": DEFAULT_MODE
    }
    initial_args.update(kwargs)
    set_module_args(initial_args)

    stop_module = stop_region.AnsibleStopCICSModule()

    # Monkeypatch module exits, so we can assert the correct one
    monkeypatch.setattr(stop_module._module, "fail_json", fail_json)
    monkeypatch.setattr(stop_module._module, "exit_json", exit_json)
    return stop_module


def test_get_job_name_from_query(monkeypatch):
    job_name = "JOBNAM"

    stop_module = initialise_module(monkeypatch)
    
    stop_region.get_jobs_wrapper = MagicMock(
        return_value=[{
            "job_name": job_name,
            "job_id": DEFAULT_JOB_ID,
            "ret_code": {
                "msg": "AC"
            }
        }]
    )

    with pytest.raises(AnsibleExitJson) as exit:
        stop_module.main()

    e = exit.value
    assert(e.kwargs["job_name"] == job_name)
    assert(e.kwargs["job_status"] == "EXECUTING")

    stop_region.get_jobs_wrapper.assert_called_once_with(DEFAULT_JOB_ID)
    

def test_get_job_name_from_query_not_executing(monkeypatch):
    job_name = "JOBNAM"

    stop_module = initialise_module(monkeypatch)
    
    stop_region.get_jobs_wrapper = MagicMock(
        return_value=[{
            "job_name": job_name,
            "job_id": DEFAULT_JOB_ID,
            "ret_code": {
                "msg": "CC"
            }
        }]
    )

    with pytest.raises(AnsibleExitJson) as exit:
        stop_module.main()

    e = exit.value
    assert(e.kwargs["job_name"] == job_name)
    assert(e.kwargs["job_status"] == "NOT_EXECUTING")

    stop_region.get_jobs_wrapper.assert_called_once_with(DEFAULT_JOB_ID)


def test_get_job_name_from_query_missing(monkeypatch):
    stop_module = initialise_module(monkeypatch)
    
    stop_region.get_jobs_wrapper = MagicMock(
        return_value=[]
    )

    with pytest.raises(AnsibleFailJson) as exit:
        stop_module.main()
    
    e = exit.value
    assert(e.args[0] == f"No jobs found with id {DEFAULT_JOB_ID}")

    stop_region.get_jobs_wrapper.assert_called_once_with(DEFAULT_JOB_ID)


def test_get_job_name_from_query_no_ret_code(monkeypatch):
    job_name = "JOBNAM"

    stop_module = initialise_module(monkeypatch)
    
    stop_region.get_jobs_wrapper = MagicMock(
        return_value=[{
            "job_name": job_name,
            "job_id": DEFAULT_JOB_ID
        }]
    )

    with pytest.raises(AnsibleFailJson) as exit:
        stop_module.main()
    
    e = exit.value
    assert(e.args[0] == f"Couldn't determine status for job ID {DEFAULT_JOB_ID} with name JOBNAM")
    
    stop_region.get_jobs_wrapper.assert_called_once_with(DEFAULT_JOB_ID)


def test_get_job_name_from_query_wrong_job_id(monkeypatch):
    job_name = "JOBNAM"

    stop_module = initialise_module(monkeypatch)
    
    stop_region.get_jobs_wrapper = MagicMock(
        return_value=[{
            "job_name": job_name,
            "job_id": "ASDF",
            "ret_code": {
                "msg": "CC"
            }
        }]
    )

    with pytest.raises(AnsibleFailJson) as exit:
        stop_module.main()
    
    e = exit.value
    assert(e.args[0] == f"Couldn't determine job name for job ID {DEFAULT_JOB_ID}")
    
    stop_region.get_jobs_wrapper.assert_called_once_with(DEFAULT_JOB_ID)


def test_get_job_name_from_query_wrong_no_job_name(monkeypatch):
    job_name = "JOBNAM"

    stop_module = initialise_module(monkeypatch)
    
    stop_region.get_jobs_wrapper = MagicMock(
        return_value=[{
            "job_id": DEFAULT_JOB_ID,
            "ret_code": {
                "msg": "CC"
            }
        }]
    )

    with pytest.raises(AnsibleFailJson) as exit:
        stop_module.main()
    
    e = exit.value
    assert(e.args[0] == f"Couldn't determine job name for job ID {DEFAULT_JOB_ID}")
    
    stop_region.get_jobs_wrapper.assert_called_once_with(DEFAULT_JOB_ID)


def test_get_job_name_from_query_wrong_no_msg(monkeypatch):
    job_name = "JOBNAM"

    stop_module = initialise_module(monkeypatch)
    
    stop_region.get_jobs_wrapper = MagicMock(
        return_value=[{
            "job_name": job_name,
            "job_id": DEFAULT_JOB_ID,
            "ret_code": {}
        }]
    )

    with pytest.raises(AnsibleFailJson) as exit:
        stop_module.main()
    
    e = exit.value
    assert(e.args[0] == f"Couldn't determine status for job ID {DEFAULT_JOB_ID} with name JOBNAM")
    
    stop_region.get_jobs_wrapper.assert_called_once_with(DEFAULT_JOB_ID)


# def test_get_job_name_from_query_failed():
#     job_name = "JOBNAM"
#     job_id = "JOB12345"
#     job_query_response = get_job_query_result(jobname=job_name, failed=True)

#     with pytest.raises(AnsibleActionFail) as action_err:
#         _get_job_name_from_query(job_query_response, job_id)
#     assert "Job query failed - (No failure message provided by zos_job_query)" in str(
#         action_err
#     )


# def test_get_job_name_from_query_failed_msg():
#     job_name = "JOBNAM"
#     job_id = "JOB12345"
#     job_query_response = get_job_query_result(
#         jobname=job_name, failed=True, message="MEANINGFUL MSG FROM CORE"
#     )

#     with pytest.raises(AnsibleActionFail) as action_err:
#         _get_job_name_from_query(job_query_response, job_id)
#     assert "Job query failed - MEANINGFUL MSG FROM CORE" in str(action_err)


# def test_get_job_name_from_query_0_jobs():
#     job_name = "JOBNAM"
#     job_id = "JOB12345"
#     job_query_response = get_job_query_result(jobname=job_name, jobs=0)

#     with pytest.raises(AnsibleActionFail) as action_err:
#         _get_job_name_from_query(job_query_response, job_id)
#     assert "No jobs found with id {0}".format(job_id) in str(action_err)


# def test_get_job_name_from_query_missing_jobs():
#     job_name = "JOBNAM"
#     job_id = "JOB12345"
#     job_query_response = get_job_query_result(
#         jobname=job_name, no_jobs_found=True)

#     with pytest.raises(AnsibleActionFail) as action_err:
#         _get_job_name_from_query(job_query_response, job_id)
#     assert "No jobs found with id {0}".format(job_id) in str(action_err)


# def test_get_job_name_from_query_multiple_jobs():
#     job_name = "JOBNAM"
#     job_id = "JOB12345"
#     job_query_response = get_job_query_result(jobname=job_name, jobs=2)

#     with pytest.raises(AnsibleActionFail) as action_err:
#         _get_job_name_from_query(job_query_response, job_id)
#     assert "Multiple jobs found with ID {0}".format(job_id) in str(action_err)
