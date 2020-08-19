#!/usr/bin/python
# -*- coding: utf-8 -*-​
# Copyright (c) IBM Corporation 2019, 2020

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r"""
module: cics_dfhrmutl
author:
    - "Xiao Yuan Ma (@bjmaxy)"
short_description: CICS Recovery manager utility program
description:
    - You can use the recovery manager utility program to do the following work.
    - Examine the setting of the autostart override record on the global catalog.
    - Set or reset the recovery manager autostart override record on the global catalog.
    - Copy that part of the catalog needed for a cold start to a new global catalog.If a new catalog is built using DFHRMUTL,
      CICS is able to perform only a cold start or an initial start with the new catalog. The performance of these starts will,
      however, be better than that of a cold or initial start with a full catalog.
version_added: "2.9"
options:
    steplib:
        description: Defines a partioned data set containing DFHRMUTL.
        required: false
        type: str
    dfhgcd:
        description:
            - Specify the input global catalog data set.
            - If cold_copy option is specified, it is only read.
            - In other cases, it may be updated.
        required: true
        type: str
    set_auto_start:
        description:
            - The type of the next startup.
            - If set_auto_start is not specified, the module will examine the value of current dfhgcd set_auto_start.
            - AUTOASIS is perform the default startup, either warm or emergency.
            - AUTOCOLD is perform a cold start.
            - AUTODIAG is perform a diagnostic run.
            - AUTOINIT is perform an initial start.
        type: str
        choices:
            - AUTOASIS
            - AUTOCOLD
            - AUTODIAG
            - AUTOINIT
            - None
    cold_copy:
        description:
            - Specify whether make a reduced copy of DFHGCD in NEWGCD.
            - Create in NEWGCD a copy of only those records from DFHGCD that CICS needs to perform a cold start,
              and update NEWGCD with the autostart override record specified by the SET_AUTO_START parameter.
            - All changes caused by SET_AUTO_START are made to the NEWGCD data set, and DFHGCD is not changed.
            - COLD_COPY is incompatible with the AUTOASIS and AUTODIAG options of SET_AUTO_START.
              If you specify COLD_COPY and either of these values of SET_AUTO_START, it is an error.
        type: list
        suboptions:
            newgcd:
                description:
                    - Defines the output global catalog data set.
                    - This option is not required unless the cold_copy option is specified.
                    - If COLD_COPY is specified the NEWGCD data set is first cleared and then has DFHGCD records and an
                      override record added to it. It must have been defined with the VSAM REUSE attribute.
                type: str
"""

RETURN = r"""
msg:
    description: The execution result message.
    returned : always
    type: str
    sample: "The DFHRMUTL program executed successfully."
rc:
    description: The return code.
    returned : always
    type: str
content:
    description: the output data set for results, information and error messages.
    returned: always
    type: str
changed:
    description: Indicates if any changes were made during module operation.
    returned: always
    type: bool
"""

EXAMPLES = r"""
  - name: Examining the override record
    cics_dfhrmutl:
      steplib: CTS550.CICS720.SDFHLOAD
      dfhgcd: BJMAXY.CICS.IYK3ZMX7.DFHGCD

  - name: set auto start to autoinit to the dfhgcd. Setting an initial start without operator intervention
    cics_dfhrmutl:
      steplib: CTS550.CICS720.SDFHLOAD
      dfhgcd: BJMAXY.CICS.IYK3ZMX7.DFHGCD
      set_auto_start: AUTOINIT

  - name: setting the global catalog for a cold start. COLD_COPY is used to improve performance.
    cics_dfhrmutl:
      steplib: CTS550.CICS720.SDFHLOAD
      dfhgcd: BJMAXY.CICS.IYK3ZMX7.DFHGCD
      set_auto_start: AUTOCOLD
      cold_copy:
        - newgcd: BJMAXY.CICS.IYK3ZMX7.NEWGCD
"""

import re
from traceback import format_exc
from ansible.module_utils.basic import AnsibleModule, env_fallback, AnsibleFallbackNotFound


MVSCMD = "mvscmd"
CICS_UTILITY = "dfhrmutl"


def run_cics_program(steplib, dfhgcd, set_auto_start, cold_copy, module):
    set_auto_start_string = ""
    mvscmd_suffix_script = ' --pgm=' + CICS_UTILITY + ' --steplib=' + steplib + ' --dfhgcd=' + dfhgcd + \
                           ' --sysin=stdin --sysprint=stdout -v'

    if set_auto_start != "" and set_auto_start is not None:
        set_auto_start_string = "SET_AUTO_START=" + set_auto_start
        if cold_copy is not None:
            set_auto_start_string = set_auto_start_string + ",COLD_COPY"
    elif cold_copy is not None:
        set_auto_start_string = "COLD_COPY"

    if cold_copy is not None:
        newgcd = cold_copy[0].get("newgcd")
        mvscmd_suffix_script = mvscmd_suffix_script + ' --newgcd=' + newgcd

    mvscmd_command = MVSCMD + mvscmd_suffix_script
    rc, stdout, stderr = module.run_command(mvscmd_command, data=set_auto_start_string, use_unsafe_shell=True)

    return rc, stdout, stderr


def validate_module_params(params):
    regex_dataset = "^(([A-Z]{1}[A-Z0-9]{0,7})([.]{1})){1,21}[A-Z]{1}[A-Z0-9]{0,7}$"
    set_auto_start_supported_value = ["AUTOASIS", "AUTOCOLD", "AUTODIAG", "AUTOINIT", None]
    if params.get("set_auto_start") in set_auto_start_supported_value:
        pass
    else:
        raise CICS_DFHRMUTL_Error("The value of option set_auto_start" + params.get("set_auto_start") + " is not supported."
                                  " The valid supported value is AUTOASIS, AUTOCOLD, AUTODIAG, AUTOINIT.")
    pattern = re.compile(regex_dataset)
    setplib = params.get("steplib")
    dfhgcd = params.get("dfhgcd")
    if pattern.fullmatch(setplib):
        pass
    else:
        raise CICS_DFHRMUTL_Error("The dataset name format of option setplib  " + setplib + " is not supported.")
    if pattern.fullmatch(dfhgcd):
        pass
    else:
        raise CICS_DFHRMUTL_Error("The dataset name format of option dfhgcd  " + dfhgcd + " is not supported.")

    if params.get("cold_copy") is not None:
        newgcd = params.get("cold_copy")[0].get("newgcd")
        if pattern.fullmatch(newgcd):
            pass
        else:
            raise CICS_DFHRMUTL_Error("The dataset name format of option newgcd " + newgcd +
                                      " is not supported.")
        if not check_cold_copy_is_compatible_with_set_auto_start(params.get("set_auto_start")):
            raise CICS_DFHRMUTL_Error(
                "COLD_COPY is incompatible with the AUTOASIS and AUTODIAG options of SET_AUTO_START.")


def check_cold_copy_is_compatible_with_set_auto_start(set_auto_start):
    """
    COLD_COPY is incompatible with the AUTOASIS and AUTODIAG options of SET_AUTO_START.
    :return:
    """
    if set_auto_start is None:
        return True
    elif set_auto_start == "AUTOASIS" or set_auto_start == "AUTODIAG":
        return False
    else:
        return True


def run_module():

    module_args = dict(
        steplib=dict(type='str', required=False),
        set_auto_start=dict(type='str', required=False, choices=['AUTOASIS', 'AUTOCOLD', 'AUTODIAG', 'AUTOINIT', None]),
        cold_copy=dict(type='list', required=False),
        dfhgcd=dict(type='str', required=True),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
    result = dict(
        changed=False,
        ret_code='',
    )

    if not module.params.get("steplib"):
        try:
            module.params['steplib'] = env_fallback('STEPLIB')
        except AnsibleFallbackNotFound as e:
            module.fail_json(msg="The option 'steplib' is not provided. Please specify it in environment "
                                 "variables 'STEPLIB', or in module input option 'steplib'. ", **result)

    try:
        validate_module_params(module.params)
        steplib = module.params.get("steplib")
        dfhgcd = module.params.get("dfhgcd")
        set_auto_start = module.params.get("set_auto_start")
        cold_copy = module.params.get("cold_copy")

        rc, stdout, stderr = run_cics_program(steplib, dfhgcd, set_auto_start, cold_copy, module)

        result['content'] = stdout
        result['rc'] = rc
        if rc == 0:
            result['msg'] = "CICS DFHRMUTL program executed successfully."
            result['changed'] = True
            module.exit_json(**result)
        else:
            result['msg'] = "CICS DFHRMUTL program execution failed."
            module.fail_json(msg="CICS DFHRMUTL program execution failed.", **result)
    except CICS_DFHRMUTL_Error as e:
        trace = format_exc()
        module.fail_json(
            msg="An unexpected error occurred: {0}".format(trace), **result)
    except Error as e:
        module.fail_json(msg=e.msg, **result)


class Error(Exception):
    pass


class CICS_DFHRMUTL_Error(Error):
    def __init__(self, error):
        self.msg = 'An error occurred during execution of CICS DFHRMUTL module --- "{0}"'.format(error)


def main():
    run_module()


if __name__ == '__main__':
    main()
