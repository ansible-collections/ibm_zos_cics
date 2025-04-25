CONSOLE_UNDEFINED = "UNDEFINED"
CONSOLE_AUTOINSTALL_FAIL = "AUTOINSTALL"


def get_operator_shutdown_response(console=None):
    content_msg = "MV2C       2024128  16:01:05.00             "
    if console == CONSOLE_UNDEFINED:
        content_msg += "+DFHAC2015  AN1234   Console ANSI0000 has not been defined to CICS. Input is ignored."
    elif console == CONSOLE_AUTOINSTALL_FAIL:
        content_msg += (
            "+DFHAC2032  AN1234   CICS autoinstall for console ANSI0000 has failed."
        )

    return {
        "changed": True,
        "cmd": "MODIFY AN1234,CEMT PERFORM SHUTDOWN",
        "content": [
            "MV2C       2024128  16:01:05.00             ISF031I CONSOLE ANSI0000 ACTIVATED",
            "MV2C       2024128  16:01:05.00            -MODIFY AN1234,CEMT PERFORM SHUTDOWN ",
            content_msg,
        ],
        "elapsed": 1.1,
        "invocation": {
            "module_args": {
                "cmd": "MODIFY AN1234,CEMT PERFORM SHUTDOWN",
                "verbose": False,
                "wait_time_s": 1,
            }
        },
        "wait_time_s": 1,
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
    content = []
    if status_line:
        content.append("STATUS {0}".format(jobname))
    for i in range(running):
        content.append(
            "IKJ56211I JOB {0}({1}) EXECUTING".format(jobname, running_job_id)
        )
    for i in range(stopped):
        content.append(
            "IKJ56192I JOB {0}({1}) ON OUTPUT QUEUE".format(jobname, stopped_job_id)
        )

    full = {"output": []}
    for i in range(command_responses):
        full["output"].append(
            {
                "command": "STATUS LINKJOB",
                "content": content,
                "rc": 0,
                "max_rc": 0,
                "lines": 4,
                "failed": False,
            }
        )

    return full if full_response else content
