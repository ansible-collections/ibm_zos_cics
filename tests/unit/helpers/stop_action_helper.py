import json

CONSOLE_UNDEFINED = "UNDEFINED"
CONSOLE_AUTOINSTALL_FAIL = "AUTOINSTALL"


def get_operator_shutdown_response(console=None):
    lines = [
        "MV2C       2024128  16:01:05.00             ISF031I CONSOLE ANSI0000 ACTIVATED",
        "MV2C       2024128  16:01:05.00            -MODIFY AN1234,CEMT PERFORM SHUTDOWN ",
    ]
    content_msg = "MV2C       2024128  16:01:05.00             "
    if console == CONSOLE_UNDEFINED:
        content_msg += "+DFHAC2015  AN1234   Console ANSI0000 has not been defined to CICS. Input is ignored."
    elif console == CONSOLE_AUTOINSTALL_FAIL:
        content_msg += (
            "+DFHAC2032  AN1234   CICS autoinstall for console ANSI0000 has failed."
        )
    lines.append(content_msg)

    return {
        "rc": 0,
        "stdout": "\n".join(lines),
        "stderr": "",
        "cmd": "opercmd -j \"MODIFY AN1234,CEMT PERFORM SHUTDOWN\"",
    }


def get_tso_status_response(
    full_response=True,
    jobname="LINKJOB",
    status_line=True,
    running=1,
    stopped=1,
    command_responses=1,
    running_job_id="JOB12345",
    stopped_job_id="JOB98765",
):
    jobs = {}
    for i in range(running):
        key = "{0}_{1}_run_{2}".format(jobname, running_job_id, i)
        jobs[key] = {
            "name": jobname,
            "id": running_job_id,
            "status": "AC",
        }
    for i in range(stopped):
        key = "{0}_{1}_stop_{2}".format(jobname, stopped_job_id, i)
        jobs[key] = {
            "name": jobname,
            "id": stopped_job_id,
            "status": "ON OUTPUT QUEUE",
        }

    jls_stdout = json.dumps({"data": jobs}) if jobs else ""
    return {"rc": 0, "stdout": jls_stdout, "stderr": ""}
