# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023,2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

# FOR INTERNAL USE IN THE COLLECTION ONLY.

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type
import re
import tempfile
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.ansible_module import AnsibleModuleHelper
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils._response import _execution, MVSExecutionException
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.zos_mvs_raw import MVSCmd
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.dd_statement import DDStatement, StdoutDefinition, StdinDefinition
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.job import job_output

MVS_CMD_RETRY_ATTEMPTS = 10


DSORG = {
    "PS": "Sequential",
    "PO": "Partitioned",
    "IS": "Indexed Sequential",
    "DA": "Direct Access",
    "VSAM": "VSAM",
    "??": "Other"
}


def _run_idcams(cmd, name, location, delete=False):  # type: (str, str, str, bool) -> list[dict[str, str| int]]
    executions = []

    for x in range(MVS_CMD_RETRY_ATTEMPTS):
        idcams_response = _execute_idcams(cmd=cmd)
        executions.append(
            _execution(
                name="IDCAMS - {0} - Run {1}".format(
                    name,
                    x + 1),
                rc=idcams_response.rc,
                stdout=idcams_response.stdout,
                stderr=idcams_response.stderr))
        if location.upper() in idcams_response.stdout.upper():
            break

    if location.upper() not in idcams_response.stdout.upper():
        raise MVSExecutionException("IDCAMS Command output not recognised", executions)

    if delete:
        pattern = r"^.+ENTRY\(A|C|D|I\){0}DELETED+$".format(location.upper())
        if idcams_response.rc == 8 and "ENTRY{0}NOTFOUND".format(
            location.upper()) in idcams_response.stdout.upper().replace(
            " ",
            "").replace(
            "\n",
                ""):
            return executions
        elif idcams_response.rc != 0 or not bool(re.search(pattern, idcams_response.stdout.upper().replace(
            " ",
            "").replace(
            "\n",
                ""))):
            raise MVSExecutionException("RC {0} when deleting data set".format(idcams_response.rc), executions)
    else:
        if idcams_response.rc == 12 and "NOTDEFINEDBECAUSEDUPLICATENAMEEXISTSINCATALOG" in idcams_response.stdout.upper(
        ).replace(" ", "").replace("\n", ""):
            return executions
        if idcams_response.rc != 0:
            raise MVSExecutionException("RC {0} when creating data set".format(idcams_response.rc), executions)

    return executions


def _get_idcams_dds(cmd):
    return [
        DDStatement('sysin', StdinDefinition(content=cmd)),
        DDStatement('sysprint', StdoutDefinition()),
    ]


def _execute_idcams(cmd):
    return MVSCmd.execute_authorized(
        pgm="IDCAMS",
        dds=_get_idcams_dds(cmd),
        verbose=True,
        debug=False
    )


def _get_listds_dds(cmd):
    return [
        DDStatement('systsin', StdinDefinition(content=cmd)),
        DDStatement('systsprt', StdoutDefinition()),
    ]


def _execute_listds(cmd):
    return MVSCmd.execute_authorized(
        pgm="IKJEFT01",
        dds=_get_listds_dds(cmd),
        verbose=True,
        debug=False
    )


def _get_dataset_size_unit(unit_symbol):  # type: (str) -> str
    return {
        "M": "MEGABYTES",
        "K": "KILOBYTES",
        "CYL": "CYLINDERS",
        "REC": "RECORDS",
        "TRK": "TRACKS"
    }.get(unit_symbol, "MEGABYTES")


def _build_idcams_define_cmd(dataset):  # type: (dict) -> str
    defineStr = "\n    DEFINE{0}{1}{2}\n    ".format(
        _build_idcams_define_cluster_parms(dataset),
        _build_idcams_define_data_parms(dataset),
        _build_idcams_define_index_parms(dataset))
    return defineStr


def _build_idcams_define_cluster_parms(dataset):  # type: (dict) -> str
    if dataset.get("volumes"):
        volumes_cmd = _build_idcams_volumes(dataset["volumes"])
    else:
        volumes_cmd = ""

    clusterStr = " CLUSTER (NAME({0}) -\n    {1}({2} {3}){4}{5})".format(
        dataset["name"],
        _get_dataset_size_unit(dataset["unit"]),
        dataset["primary"],
        dataset["secondary"],
        _build_idcams_define_parms(dataset, "CLUSTER"),
        volumes_cmd)
    return clusterStr


def _build_idcams_define_data_parms(dataset):  # type: (dict) -> str
    dataStr = " -\n    DATA (NAME({0}.DATA){1})".format(
        dataset["name"],
        _build_idcams_define_parms(dataset, "DATA"))
    return dataStr


def _build_idcams_define_index_parms(dataset):  # type: (dict) -> str
    if dataset.get("INDEX", None):
        indexStr = " -\n    INDEX (NAME({0}.INDEX){1})".format(
            dataset["name"],
            _build_idcams_define_parms(dataset, "INDEX"))
    else:
        indexStr = ""
    return indexStr


def _build_idcams_define_parms(dataset, parm):  # type: (dict, str) -> str
    parmsStr = ""
    if isinstance(dataset[parm], dict):
        for key, value in dataset[parm].items():
            if value is not None:
                parmsStr += " -\n    {0}({1})".format(key, value)
            elif key is not None:
                parmsStr += " -\n    {0}".format(key)
    return parmsStr


def _build_idcams_volumes(volumes):  # type: (list[str]) -> str
    volumes_cmd = ""
    if len(volumes) > 1:
        for vol in volumes:
            volumes_cmd += (vol + " ")
    else:
        volumes_cmd = volumes[0]
    return " -\n    VOLUMES({0})".format(volumes_cmd.rstrip())


def _get_data_set_type(listds_stdout):
    data_set_type = ""
    matches = re.findall(r"\s+(PS|PO|IS|DA|VSAM|\?\?)\s+", listds_stdout)

    if (len(matches) != 0):
        try:
            data_set_type = DSORG[matches[0]]
        except KeyError:
            data_set_type = "Unspecified"
    else:
        data_set_type = "Unspecified"
    return data_set_type


def _run_listds(location):  # type: (str) -> tuple[list[_execution], bool, str]
    cmd = " LISTDS '{0}'".format(location)
    executions = []

    for x in range(MVS_CMD_RETRY_ATTEMPTS):
        listds_response = _execute_listds(cmd=cmd)
        executions.append(
            _execution(
                name="IKJEFT01 - Get Data Set Status - Run {0}".format(
                    x + 1),
                rc=listds_response.rc,
                stdout=listds_response.stdout,
                stderr=listds_response.stderr))
        if location.upper() in listds_response.stdout.upper():
            break

    if location.upper() not in listds_response.stdout.upper():
        raise MVSExecutionException("LISTDS Command output not recognised", executions)

    # DS Name in output, good output

    if listds_response.rc == 8 and "NOT IN CATALOG" in listds_response.stdout:
        return executions, False, "NONE"

    if listds_response.rc == 4 and "MEMBER NAME NOT FOUND" in listds_response.stdout:
        return executions, False, "NONE"

    # Exists

    if listds_response.rc != 0:
        raise MVSExecutionException("RC {0} running LISTDS Command".format(listds_response.rc), executions)

    # Exists, RC 0
    data_set_organization = _get_data_set_type(listds_response.stdout)

    return executions, True, data_set_organization


def _run_iefbr14(ddname, definition):  # type: (str, DatasetDefinition) -> list[dict[str, str| int]]

    executions = []

    for x in range(MVS_CMD_RETRY_ATTEMPTS):
        iefbr14_response = _execute_iefbr14(ddname, definition)
        executions.append(
            _execution(
                name="IEFBR14 - {0} - Run {1}".format(
                    ddname,
                    x + 1),
                rc=iefbr14_response.rc,
                stdout=iefbr14_response.stdout,
                stderr=iefbr14_response.stderr))
        if iefbr14_response.stdout != "" or iefbr14_response.stderr != "":
            break

    if iefbr14_response.stdout == "" and iefbr14_response.stderr == "":
        raise MVSExecutionException("IEFBR14 Command output not recognised", executions)

    if iefbr14_response.rc != 0:
        raise MVSExecutionException(
            "RC {0} when creating sequential data set".format(
                iefbr14_response.rc), executions)

    return executions


def _get_iefbr14_dds(ddname, definition):  # type: (str, DatasetDefinition) -> list[DDStatement]
    return [DDStatement(ddname, definition)]


def _execute_iefbr14(ddname, definition):
    return MVSCmd.execute(
        pgm="IEFBR14",
        dds=_get_iefbr14_dds(ddname, definition),
        verbose=True,
        debug=False
    )


def _execute_command(command):
    module = AnsibleModuleHelper(argument_spec={})
    return module.run_command(command)

def _submit_jcl(jcl_uss_path, job_name):
    executions =[]
    command = "jsub -f '{0}'".format(jcl_uss_path)

    rc, stdout,stderr = _execute_command(command)
    executions.append(
    _execution(
        name="Submit jcl job {0} for {1}".format(jcl_uss_path, job_name),
        rc=rc,
        stdout=stdout,
        stderr=stderr))
    if rc != 0:
        raise MVSExecutionException(
            "RC {0} when submitting jcl from {1}".format(
                rc, jcl_uss_path), executions)
    return executions


def _get_job_output(job_id, job_name):
    executions = []

    try:
        jobs = job_output(job_id=job_id, job_name=job_name)
        
        #There should only be one job found for the JCL submitted
        if (len(jobs) != 1):
            raise MVSExecutionException(
                "Query for job status for {0} with job id {1} returned more than one result. Jobs returned: {2}".format(
                    job_name,
                    job_id, 
                    jobs), executions)
        
        executions.append(
            _execution(
                name="Get job output for {0}".format(job_id),
                rc=jobs[0].get("ret_code").get("code"),
                stdout=jobs[0].get("ret_code").get("msg", ""),
                stderr=jobs[0].get("ret_code").get("msg_txt", "")))
    except Exception as e:
        raise MVSExecutionException(
            "Query for {0} job submitted under Job ID {1} failed. An exception occured: {2}".format(
            job_name, 
            job_id,
            e), executions)
    
    try:
        # job output fails to get the ddname content in its response. Call direct into zoau to do it
        for i in range(len(jobs[0].get("ddnames"))):
            dd_executions, job_stdout = _get_job_dd(job_id, jobs[0]["ddnames"][i]["ddname"])

            #Put the content back in the job response object
            jobs[0]["ddnames"][i]["content"] = job_stdout
            executions.append(dd_executions)

        return jobs[0], executions
    except Exception as e:
        raise MVSExecutionException(
            "Could not get all job DDs for {0}. An exception occured: {1}".format(
            job_name, 
            e), executions)


def _get_job_dd(job_id, dd_name):
    executions = []
    command = "pjdd {0} {1}".format(job_id, dd_name)

    rc, stdout, stderr = _execute_command(command)
    executions.append(
        _execution(
            name="Get job dd {0} output for {1}".format(dd_name, job_id),
            rc=rc,
            stdout=stdout,
            stderr=stderr))
    if rc != 0:
        raise MVSExecutionException(
            "RC {0} when getting job output for {1} from {2}".format(
                rc, dd_name, job_id), executions)
    return executions, stdout


def _read_data_set_content(data_set_name):
    executions = []
    command = "dcat '{0}'".format(data_set_name)

    rc, stdout, stderr = _execute_command(command)
    executions.append(
        _execution(
            name="Read data set {0}".format(data_set_name),
            rc=rc,
            stdout=stdout,
            stderr=stderr))
    if rc != 0:
        raise MVSExecutionException(
            "RC {0} when reading content from data set {1}".format(
                rc, data_set_name), executions)
    return executions, stdout


def _write_jcl_to_data_set(jcl, data_set_name):
    """Writes generated JCL content to the specified data set
    """
    executions = []

    temp = tempfile.NamedTemporaryFile(delete=True)
    with open(temp.name, "w") as f:
        f.write(jcl)
    rc, stdout, stderr = _execute_command("cp -O u {0} \"//'{1}'\"".format(temp.name, data_set_name))
    executions.append(
        _execution(
            name="Copy JCL contents to data set",
            rc=rc,
            stdout=stdout,
            stderr=stderr))
    if rc != 0:
        raise MVSExecutionException("Failed to copy JCL content to data set", executions)
    return executions
