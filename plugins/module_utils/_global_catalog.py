# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023,2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

# FOR INTERNAL USE IN THE COLLECTION ONLY.

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils._response import MVSExecutionException, _execution
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils._data_set_utils import MVS_CMD_RETRY_ATTEMPTS, _submit_jcl, _get_job_output
import tempfile
from time import sleep

def _get_value_from_line(line):  # type: (list[str]) -> str | None
    val = None
    if len(line) == 1:
        val = line[0].split(":")[1]
    return val


def _get_filtered_list(elements, target):  # type: (list[str],str) -> list[str]
    return list(filter(lambda x: target in x, elements))


def _get_reason_code(stdout_lines_arr):  # type: (list[str]) -> str | None
    if len(stdout_lines_arr) == 0:
        return None

    stdout_comma_sep = list(stdout_lines_arr[0].split(","))
    filtered_for_reason_code = list(
        filter(lambda x: "REASON:X" in x, stdout_comma_sep))
    if len(filtered_for_reason_code) == 0:
        return None

    reason_code = [element.replace("0", "")
                   for element in filtered_for_reason_code[0].split("'")]
    return reason_code[1]


def _get_catalog_records(stdout):  # type: (str) -> tuple[str | None, str | None]
    elements = ['{0}'.format(element.replace(" ", "").upper())
                for element in stdout.split("\n")]

    autostart_filtered = _get_filtered_list(
        elements, "AUTO-STARTOVERRIDE:")
    nextstart_filtered = _get_filtered_list(elements, "NEXTSTARTTYPE:")

    autostart_override = _get_value_from_line(
        autostart_filtered)
    nextstart = _get_value_from_line(nextstart_filtered)

    return (autostart_override, nextstart)

def _create_dfhrmutl_jcl(location, sdfhload, cmd=""):
    steplib_line = f"//STEPLIB  DD DSNAME={sdfhload},DISP=SHR"
    dfhgcd_line = f"//DFHGCD   DD DSNAME={location},DISP=OLD"
    # Validate line lengths
    _validate_line_length(steplib_line, sdfhload)
    _validate_line_length(dfhgcd_line, location)
    
    jcl = ""
    if (cmd ==""):
        jcl = f'''
//DFHRMUTL JOB
//RMUTL    EXEC PGM=DFHRMUTL,REGION=1M
{steplib_line}
//SYSPRINT DD SYSOUT=*
{dfhgcd_line}
//SYSIN    DD *
/*
'''
    else:
        jcl = f'''
//DFHRMUTL JOB
//RMUTL    EXEC PGM=DFHRMUTL,REGION=1M
{steplib_line}
//SYSPRINT DD SYSOUT=*
{dfhgcd_line}
//SYSIN    DD *
    {cmd}
/*
'''

    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as fp:
        fp.write(jcl)
        fp.flush()

        # Get the temporary file's name
        qualified_file_path = fp.name
    return qualified_file_path

def _validate_line_length(line, name):
    """
    Validates that the JCL line does not exceed MAX_LINE_LENGTH.
    Raises ValueError if validation fails.
    """
    if len(line) > MAX_LINE_LENGTH:
        raise ValueError(f"{name} line exceeds {MAX_LINE_LENGTH} characters: {len(line)}")

def _validate_name_params(param):
    if any(len(part) > MAX_NAME_LENGTH for part in param.split('.')):
        raise ValueError(f"One or more parts of {param} exceeds MAX_NAME_LENGTH:{MAX_NAME_LENGTH}")
    return True

def _run_dfhrmutl(
        location,  # type: str
        sdfhload,  # type: str
        cmd=""  # type: str
):
   # type: (...) -> tuple[list[dict[str, str| int]], tuple[str | None, str | None]] | list[dict[str, str| int]]
    _validate_name_params(location)
    _validate_name_params(sdfhload)

    qualified_file_path = _create_dfhrmutl_jcl(
        location,
        sdfhload,
        cmd
    )
    #Use job submit to submit the above jcl
    #After execution delete file os.remove(qualified_file_path)
    executions = []

    for x in range(MVS_CMD_RETRY_ATTEMPTS):
        dfhrmutl_response, jcl_executions = _execute_dfhrmutl(qualified_file_path)
        dfhrmutl_rc = dfhrmutl_response.get("ret_code").get("code")

        allContent = []
        for ddname in dfhrmutl_response.get("ddnames"):
                allContent += ddname.get("content")
        stdout_raw = "".join(allContent)

        executions.append(jcl_executions)
        executions.append(
            _execution(
                name="DFHRMUTL - {0} - Run {1}".format(
                    "Get current catalog" if cmd == "" else "Updating autostart override",
                    x + 1),
                rc=dfhrmutl_rc,
                stdout=stdout_raw,
                stderr=dfhrmutl_response.get("ret_code").get("msg_txt", "")))
        
        if dfhrmutl_rc not in (0, 16):
            raise MVSExecutionException(
                "DFHRMUTL failed with RC {0}".format(
                    dfhrmutl_rc), executions)

        if dfhrmutl_rc == 0:
            break
        if dfhrmutl_rc == 16:
            formatted_stdout_lines = [
                "{0}".format(element.replace(" ", "").upper())
                for element in stdout_raw.split("\n")
            ]
            stdout_with_rc = list(filter(lambda x: "REASON:X" in x, formatted_stdout_lines))

            reason_code = _get_reason_code(stdout_with_rc)
            if reason_code and reason_code != "A8":
                raise MVSExecutionException(
                    "DFHRMUTL failed with RC 16 - {0}".format(stdout_with_rc[0]), executions
                )
            elif reason_code is None:
                raise MVSExecutionException(
                    "DFHRMUTL failed with RC 16 but no reason code was found",
                    executions,
                )

    if cmd != "":
        return executions

    return executions, _get_catalog_records(stdout_raw)


def _execute_dfhrmutl(rmutl_jcl_path, job_name="DFHRMUTL"):
    executions = _submit_jcl(rmutl_jcl_path, job_name)
    job_id = executions[0].get("stdout").strip()

    #Give RMUTL a second to run
    sleep(1)

    job, job_executions = _get_job_output(job_id, job_name)
    executions.append(job_executions)

    return job, executions


def _get_idcams_cmd_gcd(dataset):   # type: (dict) -> dict
    defaults = {
        "CLUSTER": {
            "RECORDSIZE": "{0} {1}".format(RECORD_COUNT_DEFAULT, RECORD_SIZE_DEFAULT),
            "INDEXED": None,
            "KEYS": "{0} {1}".format(KEY_LENGTH, KEY_OFFSET),
            "FREESPACE": "{0} {1}".format(CI_PERCENT, CA_PERCENT),
            "SHAREOPTIONS": str(SHARE_CROSSREGION),
            "REUSE": None
        },
        "DATA": {
            "CONTROLINTERVALSIZE": str(CONTROL_INTERVAL_SIZE_DEFAULT)
        },
        "INDEX": {
            None
        }
    }
    defaults.update(dataset)
    return defaults


RECORD_COUNT_DEFAULT = 4089
RECORD_SIZE_DEFAULT = 32760
CONTROL_INTERVAL_SIZE_DEFAULT = 32768
KEY_LENGTH = 52
KEY_OFFSET = 0
CI_PERCENT = 10
CA_PERCENT = 10
SHARE_CROSSREGION = 2
MAX_LINE_LENGTH = 72
MAX_NAME_LENGTH = 8
