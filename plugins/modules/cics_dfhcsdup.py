#!/usr/bin/python
# -*- coding: utf-8 -*-​
# Copyright (c) IBM Corporation 2019, 2020

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r"""
module: cics_dfhcsdup
author:
    - "Zhao Lu (@zlbjlu)"
short_description: CICS system definition utility program(DFHCSDUP)
description:
    - Run CICS system definition utility program DFHCSDUP to read from and write to a CICS system definition (CSD) file.
    - Manage CICS resource definitions using commands supplied as part of DFHCSDUP.
    - ALL the commands supplied by DFHCSDUP can be invoked through this module, such as ADD, ALTER, COPY, DEFINE, DELETE, EXTRACT, etc.
      Refer to CICS Resource Definition Guide for command usage.
version_added: "2.9"
options:
    parms:
        description: The PARM parameter used by DFHCSDUP, e.g., -a='UPPERCASE'.
        required: false
        type: dict
        suboptions:
            uppercase:
                description:
                    - Specifies that you want all output from DFHCSDUP to be in uppercase.
                type: bool
                required: false
                default: false
            access_mode:
                description:
                    - Specifies whether you want read and write access or read-only access to the CSD.
                type: str
                required: false
                default: 'rw'
                choices: [ 'rw', 'ro' ]
            compat:
                description:
                    - Specifies whether the DFHCSDUP utility program is to run in compatibility mode.
                type: bool
                required: false
                default: false
            page_size:
                description:
                    - Specifies the number of lines per page on output listings.
                    - Values range from 4 to 9999.
                type: int
                required: false
                default: 60
    steplib:
        description: Specifies the library in which the utility is stored in.
        required: false
        type: str
    dfhcsd:
        description: Specifies the CSD file which you read from or write to.
        required: true
        type: str
    seccsd:
        description:
            - Specifies the CSD file which you read from or write to.
            - Required if you specify the FROMCSD parameter on an APPEND, COPY, or SERVICE command.
        required: false
        type: str
    userprog_lib:
        description:
            - Specifies the library in which the utility is stored in.
            - Required if you specify the EXTRACT command and need to do some customized operations.
        required: false
        type: str
    userprog_dd:
        description:
            - Specifies the dd names used by the user program.
            - Required if you specify the EXTRACT command and need to do some customized operations.
        required: false
        type: str
    userprog_ds:
        description:
            - Specifies the input data set that is used by the user program.
            - Required if you specify the EXTRACT command and need to do some customized operations.
        type: str
        required: false
    cmd_dsn:
        description: Specify the file used in which the command statements are stored.
        type: str
        required: false
    cmd_str:
        description: Specify the file used in which the command statements are stored.
        type: list
        required: false
    cmd_stmt:
        description:
            - Specify the command statements which would be invoked through the utility.
        type: list
        required: false
        default: null
        elements: dict
        suboptions:
            add:
                description: Add a group to a list.
                required: false
                type: str
                suboptions:
                    list_name:
                        description: Specify the name of the list.
                        required: true
                        type: str
                    group_name:
                        description: Specify the name of the group.
                        required: true
                        type: str
                    after:
                        description: Specify AFTER to place the new group name after the existing group name.
                        required: false
                        type: str
                    before:
                        description: Specify BEFORE to place the new group name before the existing group name.
                        required: false
                        type: str
            remove:
                description: Remove a group name from a list.
                required: false
                type: dict
                suboptions:
                    list_name:
                        description: Specify the name of the list.
                        required: true
                        type: str
                    group_name:
                        description: Specify the name of the group.
                        required: true
                        type: str
            list:
                description: Produce listings of the current status of the CSD file.
                required: false
                type: dict
                suboptions:
                    list_name:
                        description: Specify the name of the list.
                        required: false
                        type: str
                    group_name:
                        description: Specify the name of the group.
                        required: false
                        type: str
                    objects:
                        description: Specify the level of detail required for each resource definition.
                        required: false
                        type: bool
                    sigsumm:
                        description: Show the definition signature for each of the resource definitions displayed.
                        required: false
                        type: bool
                    all:
                        description: Print summaries of all the definitions of lists and groups that are on the CSD file.
                        required: false
                        type: bool
            extract:
                description: Extract a resource definition, group, or list from the CSD file.
                required: false
                type: dict
                suboptions:
                    list_name:
                        description: Specify the name of the list.
                        required: false
                        type: str
                    group_name:
                        description: Specify the name of the group.
                        required: false
                        type: str
                    userprogram:
                        description:
                            - Specify the name of the user-written program that is to process the data retrieved
                              by the EXTRACT command.
                        required: true
                        type: str
                    objects:
                        description: Specify the level of detail required for each resource definition.
                        required: false
                        type: bool
            initialize:
                description: Prepare a newly defined data set for use as a CSD file.
                required: false
                type: str
            verify:
                description: Remove internal locks on groups and lists.
                required: false
                type: str
            process:
                description: Apply maintenance to the CSD file for a specific APAR.
                required: false
                type: dict
                suboptions:
                    apar_num:
                        description: The number of the APAR providing the maintenance.
                        required: false
                        type: str
            upgrade:
                description: Apply maintenance to the CSD file for a specific APAR.
                required: false
                type: dict
                suboptions:
                    using:
                        description: Install IBM features onto CICS.
                        required: false
                        type: str
                    replace:
                        description: Specify the REPLACE option when you need to rerun the UPGRADE command.
                        required: false
                        type: bool
            define:
                description: Create new resource definitions.
                required: false
                type: dict
                suboptions:
                    list_name:
                        description: Specify the name of the list.
                        required: false
                        type: str
                    group_name:
                        description: Specify the name of the group.
                        required: true
                        type: str
                    resource_type:
                        description: Specify the type of the resource.
                        required: true
                        type: str
                    resource_name:
                        description: Specify the name of the resource.
                        required: true
                        type: str
                    attr_list:
                        description:
                            - The resource attributes.
                            - Refer to CICS Resource Definition Guide for the supported attributes.
                        required: false
                        type: dict
            userdefine:
                description: Create new resource definitions using your own default values instead of the default values supplied by CICS.
                required: false
                type: dict
                suboptions:
                    group_name:
                        description: Specify the name of the group.
                        required: true
                        type: str
                    resource_type:
                        description: Specify the type of the resource.
                        required: true
                        type: str
                    resource_name:
                        description: Specify the name of the resource.
                        required: true
                        type: str
                    alias:
                        description: Specify the alias name of the resource type to be searched for in the user-defined groups.
                        required: false
                        type: str
                    attr_list:
                        description:
                            - The resource attributes.
                            - Refer to CICS Resource Definition Guide for the supported attributes.
                        required: false
                        type: dict
            scan:
                description: SCAN all the IBM®-supplied groups and user-defined groups for a specified resource.
                required: false
                type: dict
                suboptions:
                    resource_type:
                        description: Specify the type of the resource.
                        required: true
                        type: str
                    resource_name:
                        description: Specify the name of the resource.
                        required: true
                        type: str
                    alias:
                        description: Specify the alias name of the resource type to be searched for in the user-defined groups.
                        required: false
                        type: str
            alter:
                description: Change some or all of the attributes of an existing resource definition.
                required: false
                type: dict
                suboptions:
                    group_name:
                        description: Specify the name of the group.
                        required: true
                        type: str
                    resource_type:
                        description: Specify the type of the resource.
                        required: true
                        type: str
                    resource_name:
                        description: Specify the name of the resource.
                        required: true
                        type: str
                    attr_list:
                        description:
                            - The resource attributes.
                            - Refer to CICS Resource Definition Guide for the supported attributes.
                        required: false
                        type: dict
            delete:
                description: Delete a single resource definition in a group.
                required: false
                type: dict
                suboptions:
                    list_name:
                        description: Specify the name of the list.
                        required: false
                        type: str
                    group_name:
                        description: Specify the name of the group.
                        required: false
                        type: str
                    resource_type:
                        description: Specify the type of the resource.
                        required: false
                        type: str
                    resource_name:
                        description: Specify the name of the resource.
                        required: false
                        type: str
                    remove:
                        description:
                            - The group will be removed from all lists that contained it unless UPGRADE commands are running.
                        required: false
                        type: bool
                    all:
                        description: Delete all the definitions.
                        required: false
                        type: bool
            copy:
                description: Copy resource definitions from one group to another group.
                required: false
                type: dict
                suboptions:
                    from_csd:
                        description: Specify the ddname of the secondary CSD file.
                        required: true
                        type: str
                    group_name:
                        description: Specify the name of the group.
                        required: true
                        type: str
                    resource_type:
                        description: Specify the type of the resource.
                        required: false
                        type: str
                    resource_name:
                        description: Specify the name of the resource.
                        required: false
                        type: str
                    to:
                        description: Specify the target name of the list or group.
                        required: true
                        type: str
                    replace:
                        description: Replace the definitions in groupname2.
                        required: false
                        type: bool
                    merge:
                        description: Preserve the definitions in groupname2.
                        required: false
                        type: bool
            append:
                description: Add the groups in one list to the end of another list.
                required: false
                type: dict
                suboptions:
                    from_csd:
                        description: Specify the ddname of the secondary CSD file.
                        required: true
                        type: str
                    list_name:
                        description: Specify the name of the list.
                        required: true
                        type: str
                    to:
                        description: Specify the target name of the list.
                        required: true
                        type: str
            service:
                description: Copy resource definitions from one group to another group.
                required: false
                type: dict
                suboptions:
                    from_csd:
                        description: Specify the ddname of the secondary CSD file.
                        required: true
                        type: str
                    level:
                        description: Specify the the service level.
                        required: false
                        type: int
"""

EXAMPLES = r"""
  - name: Test case for cics_dfhcsdup
    cics_dfhcsdup:
      steplib: CTS540.CICS710.SDFHLOAD
      dfhcsd: XXXXXX.ATEST.DFHCSD
      cmd_stmt:
        - add:
            list_name: LST01
            group_name: GRP01
"""

RETURN = r"""
ret_code:
    description: The return code.
    returned : always
    type: int
    sample: 0
csd:
    description: The CSD data set used.
    returned : always
    type: str
    sample: "XXXXXXX.TEST.DFHCSD"
content:
    description:
        - Holds additional information related to resource
          definition that may be useful to the user.
        - Return the message if error occurs, return the temporary
          data set used for message if no error.
    type: str
    returned: always
    sample: "XXXXXX.TEST.MSGPS"
changed:
    description: Indicates if any changes were made during module operation.
    returned : always
    type: bool
"""

try:
    from zoautil_py import Datasets
except Exception:
    Datasets = ""
from ansible.module_utils.basic import AnsibleModule
import re


DEFAULT_RECLEN = 80
DEFAULT_SIZE = "10M"
SUPPORTED_COMMANDS = ['ADD', 'ALTER', 'APPEND', 'COPY', 'DEFINE', 'DELETE',
                      'EXTRACT', 'INITIALIZE', 'LIST', 'PROCESS', 'REMOVE',
                      'SCAN', 'SERVICE', 'UPGRADE', 'USERDEFINE', 'VERIFY']
COMMAND_TYPE_01 = ["INITIALIZE", "VERIFY", "UPGRADE", "PROCESS",
                   "LIST", "SCAN"]
COMMAND_TYPE_02 = ["ADD", "REMOVE", "ALTER", "DEFINE", "DELETE",
                   "USERDEFINE"]
COMMAND_TYPE_SUB_02 = ["DEFINE", "USERDEFINE", "ALTER", "DELETE"]
COMMAND_TYPE_03 = ["APPEND", "COPY", "SERVICE"]


class ValidationError(Exception):
    def __init__(self, key, value):
        self.msg = (
            "Input value: {0} for the parameter: {1} "
            "is not valid.".format(key, value)
        )
        super().__init__(self.msg)


class CmdRunError(Exception):
    def __init__(self, cmds, out, err):
        self.msg = (
            "Failed during execution of cics command: {0}; "
            "stdout: {1}; stderr: {2}".format(cmds, out, err)
        )
        super().__init__(self.msg)


def run_dfhcsdup(mvscmd_args, steplib, dfhcsd, seccsd, cmds,
                 userprog_lib, userprog_dd, userprog_ds, cmd_dsn, sysin_ds):
    ''' Call zOAU API to invoke CICS utility DFHCSDUP '''
    out = None
    err = None
    prog_ds = ""
    prog_ds_size = "5M"
    prog_ds_reclen = 80
    dfhcsdup_cmd_base = "mvscmd --pgm=dfhcsdup --args='{0}' --sysprint=stdout \
                        --dfhcsd='{1}'".format(
                        mvscmd_args, dfhcsd)
    if cmds:
        dfhcsdup_cmd = "{0} --sysin='{1}' --steplib='{2}'".format(
                       dfhcsdup_cmd_base, sysin_ds, steplib)
        if cmd_dsn:
            sysin_ds = sysin_ds + ':' + cmd_dsn
            dfhcsdup_cmd = "{0} --sysin='{1}' --steplib='{2}'".format(
                           dfhcsdup_cmd_base, sysin_ds, steplib)
        if seccsd:
            rc, err_msg = check_ds(seccsd, module)
            if err_msg:
                module.fail_json(msg=err_msg)
            dfhcsdup_cmd = "{0} --seccsd='{1}'".format(dfhcsdup_cmd, seccsd)

        if "EXTRACT" in cmds:
            if userprog_dd:
                if userprog_lib:
                    rc, err_msg = check_ds(userprog_lib, module)
                    steplib = steplib + ':' + userprog_lib
                    if err_msg:
                        module.fail_json(msg=err_msg)
                    dfhcsdup_cmd = "{0} --sysin='{1}' --steplib='{2}'".format(
                        dfhcsdup_cmd_base, sysin_ds, steplib)
                if userprog_ds:
                    rc, err_msg = check_ds(userprog_ds, module)
                    if err_msg:
                        module.fail_json(msg=err_msg)
                else:
                    prog_ds = alloc_ds(prog_ds_size, prog_ds_reclen)
                    userprog_ds = prog_ds
            else:
                module.fail_json(
                    msg="USERPROG_DD is required for command EXTRACT.")
            dfhcsdup_cmd = "{0} --{1}='{2}'".format(
                dfhcsdup_cmd, userprog_dd, userprog_ds)
    else:
        dfhcsdup_cmd = "mvscmd --pgm=dfhcsdup --args='{0}' --sysprint=stdout \
                        --steplib='{1}' --sysin='{2}' --dfhcsd='{3}'".format(
                       mvscmd_args, steplib, cmd_dsn, dfhcsd)
    try:
        rc, out, err = module.run_command(dfhcsdup_cmd)
        if rc <= 4 and userprog_ds:
            out = Datasets.read("{0}".format(userprog_ds))
    except Exception:
        raise CmdRunError(cmds, out, err)
    finally:
        # if prog_ds:
        #     Datasets.delete(prog_ds)
        if sysin_ds:
            Datasets.delete(sysin_ds)
    return rc, out, err, userprog_ds


def check_ds(ds_name, module):
    err_msg = None
    check_rc = False
    check_ds_cmd = "mvscmdauth --pgm=ikjeft01 --systsin=stdin \
        --systsprt=stdout"
    tso_cmd = " LISTDS '{0}'".format(ds_name)
    rc, out, err = module.run_command(check_ds_cmd, data=tso_cmd)
    if re.findall(r"NOT IN CATALOG", out):
        err_msg = "Data set {0} does not exist.".format(ds_name)
    elif rc <= 4:
        check_rc = True
    else:
        err_msg = "Failed when checking the data set {0}".format(ds_name)
    return check_rc, err_msg


def alloc_ds(size, reclen):
    if not reclen:
        reclen = DEFAULT_RECLEN
    if not size:
        size = DEFAULT_SIZE
    temp_name = Datasets.temp_name(Datasets.hlq())
    rc = Datasets.create(temp_name, 'SEQ', size, 'FB', '', reclen)
    if rc >= 4:
        module.fail_json(msg="Can not allocate temporary data set!")
    return temp_name


def dollar_sign_to_literal(text):
    if r'$' in text:
        text = text.replace("$", r"\$")
    return text


def parse_dict(dict):
    attr_list = []
    attr = ""
    for k, v in dict.items():
        if isinstance(v, bool):
            b2s_map = {True: "YES", False: "NO"}
            v = b2s_map[v]
        attr = k.upper() + "(" + str(v).upper() + ")"
        attr_list.append(attr)
    return "{0}".format(" ".join(attr_list))


def split_str(cmd):
    LINE_LIMIT = 71
    cmd = " ".join(cmd.split())
    cmd = cmd + " "
    re_pat = r"\s+(?=[^()]*(?:\(|$))"
    pos_list = []
    if len(cmd) > LINE_LIMIT:
        for space in re.finditer(re_pat, cmd):
            pos_list.append(space.start())
            for ix, pos in enumerate(pos_list):
                if pos >= LINE_LIMIT:
                    cmd = cmd[:pos_list[ix - 1]] + "\n" + \
                        split_str(cmd[(pos_list[ix - 1] + 1):])
    return cmd


def parse_args(parms):
    ''' Parse the parms(dict) to generate the args used by zOAU API '''
    args = ""
    args_list = []
    csd_dict = dict(
        rw="CSD(READWRITE)",
        ro="CSD(READONLY)",
    )
    for pi in parms:
        arg = ""
        pv = parms.get(pi)
        if pi == "access_mode":
            arg = csd_dict.get(pv)
        if pi == "page_size":
            arg = "PAGESIZE({0})".format(str(pv))
        if pi == "compat":
            if pv:
                arg = "COMPAT"
            else:
                arg = "NOCOMPAT"
        if pi == "uppercase" and pv:
            arg = "UPPERCASE"
        if arg:
            args_list.append(arg)
    args = "{0}".format(",".join(args_list))
    return args


def parse_cmds(cmd_stmt):
    err_msg = None
    cmd = ""
    sep = " "
    grp = "GROUP_NAME"
    lst = "LIST_NAME"
    res_type = "RESOURCE_TYPE"
    res_name = "RESOURCE_NAME"
    cmd_list = []
    for cmd_dict in cmd_stmt:
        cmd_key = list(cmd_dict.keys())[0]
        cmd_value = cmd_dict[cmd_key]
        cmd_upper = cmd_key.upper()
        if cmd_upper not in SUPPORTED_COMMANDS:
            err_msg = "Input command '{0}' is not supported by \
                      DFHCSDUP".format(cmd_key)
            module.fail_json(msg=err_msg)
        else:
            if cmd_upper in COMMAND_TYPE_01:
                cmd = cmd_key
                if cmd_upper == "UPGRADE":
                    if cmd_value:
                        for ci in cmd_value:
                            cv = ""
                            if ci.upper() == "REPLACE" and cmd_value[ci]:
                                cv = "R"
                            if ci.upper() == "USING" and cmd_value[ci]:
                                cv = "US({0})".format(cmd_value[ci].upper())
                            if cv:
                                cmd = "UP {0}".format(cv)
                if cmd_upper == "PROCESS":
                    apar = "APAR"
                    flag = 1
                    if cmd_value:
                        for k, v in cmd_value.items():
                            if k.upper() == apar and v:
                                cmd = "PROCESS A({0})".format(v.upper())
                                flag = 0
                    if flag:
                        err_msg = "Missing APAR number from the command \
                                  '{0}'.".format(cmd_upper)
                        module.fail_json(msg=err_msg)
                if cmd_upper == "SCAN":
                    alias = ""
                    res_type_value = ""
                    res_name_value = ""
                    resource = ""
                    if cmd_value:
                        for k, v in cmd_value.items():
                            if k.upper() == res_type and v:
                                res_type_value = v.upper()
                            if k.upper() == res_name and v:
                                res_name_value = v.upper()
                            if res_name_value and res_type_value:
                                resource = "{0}({1})".format(
                                    res_type_value, res_name_value)
                            if k.upper() == "ALIAS" and v:
                                alias = "ALIAS({0})".format(v.upper())
                        if resource:
                            cmd = "SCAN {0} {1}".format(resource, alias)
                if cmd_upper == "LIST":
                    if cmd_value:
                        option_list = []
                        flag1 = 1
                        flag2 = 1
                        for k, v in cmd_value.items():
                            option = ""
                            if flag1:
                                if k.upper() == "ALL":
                                    option = "ALL"
                                elif k.upper() == "GROUP_NAME":
                                    option = "G({0})".format(v.upper())
                                elif k.upper() == "LIST_NAME":
                                    option = "LI({0})".format(v.upper())
                                if option:
                                    flag1 = 0
                            if flag2:
                                if (k.upper() == "OBJECTS" or
                                   k.upper() == "SIGSUMM"):
                                    option = k.upper()
                                    flag2 = 0
                            option_list.append(option)
                        cmd = "{0} {1}".format(
                            cmd.upper(), sep.join(option_list))
            if cmd_upper in COMMAND_TYPE_02:
                if cmd_value and grp.lower() in cmd_value.keys():
                    flag = 1
                    option_list = []
                    if (cmd_upper in ("ADD", "REMOVE") and
                            lst.lower() not in cmd_value.keys()):
                        err_msg = "Missing necessary command parameters: '{0}' \
                             for the command {1}.".format(lst, cmd_upper)
                        module.fail_json(msg=err_msg)
                    if (cmd_upper in COMMAND_TYPE_SUB_02 and
                            res_type.lower() not in cmd_value.keys()):
                        err_msg = "Missing necessary command parameters: '{0}' \
                        for the command {1}.".format(res_type, cmd_upper)
                        module.fail_json(msg=err_msg)
                    else:
                        resource = ""
                        attr_list = ""
                        group_name = ""
                        list_name = ""
                        res_type_value = ""
                        res_name_value = ""
                        for k, v in cmd_value.items():
                            option = ""
                            if cmd_upper == "ADD" and flag:
                                if k.upper() == "AFTER_GRP" and v:
                                    option = "A({0})".format(v.upper())
                                if k.upper() == "BEFORE_GRP" and v:
                                    option = "B({0})".format(v.upper())
                                if option:
                                    flag = 0
                            if k.upper() == grp and v:
                                group_name = "G({0})".format(v.upper())
                            if k.upper() == lst and v:
                                list_name = "LI({0})".format(v.upper())
                            if k.upper() == res_type and v:
                                res_type_value = v.upper()
                            if k.upper() == res_name and v:
                                res_name_value = v.upper()
                            if k.upper() == "ATTR_LIST" and v:
                                attr_list = parse_dict(v)
                            if cmd_upper == "DELETE" and k.upper() == "REMOVE":
                                option = "REMOVE"
                            if cmd_upper == "DELETE" and k.upper() == "ALL":
                                resource = "ALL"
                            if res_name_value and res_type_value:
                                resource = "{0}({1})".format(
                                    res_type_value, res_name_value)
                            option_list.append(option)
                        if cmd_upper in COMMAND_TYPE_SUB_02:
                            if resource:
                                cmd = "{0} {1} {2} {3} {4}".format(
                                    cmd_upper, resource, group_name,
                                    sep.join(option_list), attr_list)
                            else:
                                # err_msg
                                pass
                        else:
                            cmd = "{0} {1} {2} {3}".format(
                                cmd_upper, group_name, list_name,
                                sep.join(option_list))
                else:
                    err_msg = "Missing necessary command parameters: '{0}' \
                              for the command {1}.".format(grp, cmd_upper)
                    module.fail_json(msg=err_msg)
            if cmd_upper in COMMAND_TYPE_03:
                if cmd_value:
                    flag = 1
                    to = ""
                    list_group = ""
                    option = ""
                    resource_name = ""
                    resource_type = ""
                    resource = ""
                    if cmd_upper == "SERVICE":
                        fromcsd = "FROMCSD(DFHCSD)"
                    else:
                        fromcsd = "FROMCSD(SECCSD)"
                    for k, v in cmd_value.items():
                        if k.upper() == "FROMCSD" and v:
                            fromcsd = "FROMCSD({0})".format(v.upper())
                        if k.upper() == "TO" and v:
                            to = "TO({0})".format(v.upper())
                        if k.upper() == "LEVEL" and str(v):
                            option = "LEVEL({0})".format(str(v).zfill(3))
                        if k.upper() == "GROUP_NAME" and v:
                            list_group = "GROUP({0})".format(v.upper())
                        if k.upper() == "LIST_NAME" and v:
                            list_group = "LIST({0})".format(v.upper())
                        if k.upper() == "MERGE" and v and flag:
                            option = "MERGE"
                            flag = 0
                        if k.upper() == "REPLACE" and v and flag:
                            option = "REPLACE"
                            flag = 0
                        if k.upper() == "RESOURCE_TYPE" and v:
                            resource_type = v.upper()
                        if k.upper() == "RESOURCE_NAME" and v:
                            resource_name = "({0})".format(v.upper())
                        resource = "{0}{1}".format(
                            resource_type, resource_name)
                    cmd = "{0} {1} {2} {3} {4} {5}".format(
                        cmd_upper, fromcsd, list_group, to, resource, option)
            if cmd_upper == "EXTRACT":
                flag = 1
                option = ""
                option_list = []
                if cmd_value:
                    for k, v in cmd_value.items():
                        if flag and k.upper() == "GROUP_NAME" and v:
                            option = "GROUP({0})".format(v.upper())
                            flag = 0
                        if flag and k.upper() == "LIST_NAME" and v:
                            option = "LIST({0})".format(v.upper())
                            flag = 0
                        if k.upper() == "USER_PROGRAM" and v:
                            option = "USERPROGRAM({0})".format(v.upper())
                        if k.upper() == "OBJECTS" and v:
                            option = "OBJECTS"
                        option_list.append(option)
                if not flag:
                    cmd = "{0} {1}".format(cmd_upper, sep.join(option_list))
        cmd_list.append(split_str(cmd))
    cmds = "\n".join(cmd_list)
    return cmds


def check_parms(params):
    check_flag = False
    end_p = r'$'
    dd_p = r'^[@$#A-Za-z][@$#A-Za-z0-9]{0,7}$'
    dsn_p = r'''
        ^[a-zA-Z#$@][a-zA-Z0-9#$@-]{0,7}
        ([.][a-zA-Z#$@][a-zA-Z0-9#$@-]{0,7}){0,21}'''
    mem_p = r'([(][@$#A-Za-z][@$#A-Za-z0-9]{0,7}[)]){0,1}'
    dsn_p_01 = dsn_p + end_p
    dsn_p_02 = dsn_p + mem_p + end_p
    re_dsn_01 = re.compile(dsn_p_01, re.VERBOSE)
    re_dsn_02 = re.compile(dsn_p_02, re.VERBOSE)
    re_dd = re.compile(dd_p)
    keys = ['parms', 'cmd_stmt', 'cmd_str', 'userprog_dd',
            'userprog_ds', 'userprog_lib', 'steplib',
            'cmd_dsn', 'dfhcsd', 'seccsd']
    for key in keys:
        value = params.get(key)
        if value:
            if key in ('parms', 'cmd_stmt'):
                pass
            elif key == 'cmd_str':
                for cmd in value:
                    if len(cmd) <= 71:
                        pass
                    else:
                        value = cmd
                        check_flag = True
            elif key == 'userprog_dd':
                if re_dd.fullmatch(value):
                    pass
                else:
                    check_flag = True
            elif key in ('userprog_ds', 'cmd_dsn'):
                if ((re_dsn_01.fullmatch(value) and len(value) <= 44) or
                   (re_dsn_02.fullmatch(value) and len(value) <= 54)):
                    pass
                else:
                    check_flag = True
            elif key in ('steplib', 'userprog_lib', 'dfhcsd', 'seccsd'):
                if (len(value) <= 44 and
                   re_dsn_01.fullmatch(value)):
                    pass
                else:
                    check_flag = True

            if check_flag:
                raise ValidationError(str(key), str(value))
        else:
            pass


def run_module():
    global module

    module_args = dict(
        parms=dict(type="dict", required=False,
                   options=dict(
                       uppercase=dict(type="bool", default=False),
                       access_mode=dict(type="str", default="rw",
                                        choices=["rw", "ro"]),
                       page_size=dict(type="int", default=60),
                       compat=dict(type="bool", default=False),
                   )),
        steplib=dict(type="str", required=True),
        dfhcsd=dict(type="str", required=True),
        seccsd=dict(type="str", required=False, default=None),
        cmd_dsn=dict(type="str", required=False, default=None),
        cmd_stmt=dict(type="list", elements="dict", default=None),
        cmd_str=dict(type="list", elements="str", default=None),
        userprog_dd=dict(type="str", required=False),
        userprog_lib=dict(type="str", required=False),
        userprog_ds=dict(type="str", required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args
    )

    changed = False
    mvscmd_commands = ""
    sysin_ds = None
    rc_steplib = False
    rc_dfhcsd = False
    rc_cmd_dsn = False
    content = None
    cmds = None
    err_msg = None

    check_parms(module.params)
    parms = module.params.get("parms")
    steplib = module.params.get("steplib")
    dfhcsd = module.params.get("dfhcsd")
    seccsd = module.params.get("seccsd")
    cmd_stmt = module.params.get("cmd_stmt")
    cmd_str = module.params.get("cmd_str")
    cmd_dsn = module.params.get("cmd_dsn")
    userprog_lib = module.params.get("userprog_lib")
    userprog_dd = module.params.get("userprog_dd")
    userprog_ds = module.params.get("userprog_ds")
    result = dict(
        changed=changed,
        csd=dfhcsd,
        parms=parms,
        cmds=cmds,
        content=content,
    )

    rc_steplib, err_msg = check_ds(steplib, module)
    if err_msg:
        module.fail_json(msg=err_msg)
    rc_dfhcsd, err_msg = check_ds(dfhcsd, module)
    if err_msg:
        module.fail_json(msg=err_msg)

    if parms:
        mvscmd_args = parse_args(parms)
    else:
        parms = "CSD(READWRITE),PAGESIZE(60),NOCOMPAT"
        mvscmd_args = parms

    if all(c is None for c in [cmd_dsn, cmd_stmt, cmd_str]):
        err_msg = "No command to be executed!"
    if err_msg:
        module.fail_json(msg=err_msg)

    if cmd_dsn:
        rc_cmd_dsn, err_msg = check_ds(cmd_dsn, module)
    if cmd_stmt:
        mvscmd_commands = parse_cmds(cmd_stmt)
    if cmd_str:
        mvscmd_commands = "\n".join(cmd_str) + '\n' + mvscmd_commands
    if mvscmd_commands:
        mvscmd_commands = dollar_sign_to_literal(mvscmd_commands)

    if mvscmd_commands:
        sysin_ds = alloc_ds("5M", 80)
        Datasets.write(sysin_ds, mvscmd_commands)

    rc, out, err, userprog_ds = run_dfhcsdup(mvscmd_args, steplib, dfhcsd, seccsd,
                                             mvscmd_commands, userprog_lib, userprog_dd,
                                             userprog_ds, cmd_dsn, sysin_ds)
    if out:
        content = out.split("\n")

    if rc <= 4:
        changed = True
        if userprog_ds:
            content_ds = userprog_ds
        else:
            content_ds = alloc_ds("", 133)
            out = dollar_sign_to_literal(out)
            Datasets.write(content_ds, out)
        result = dict(
            changed=changed,
            csd=dfhcsd,
            parms=parms,
            content=content_ds,
            ret_code=rc,
        )
    else:
        result = dict(
            changed=changed,
            csd=dfhcsd,
            content=content,
            ret_code=rc,
        )
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
