#!/usr/bin/python
# -*- coding: utf-8 -*-​
# Copyright (c) IBM Corporation 2019, 2020

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r"""
module: cics_dfhccutl
author:
    - "Xiao Yuan Ma (@bjmaxy)"
short_description: Initialize CICS local catalog
description:
    - Initialize the CICS local catalog by invoking the DFHCCUTL program.

version_added: "2.9"
options:
    steplib:
        description:
            - Specify a partioned data set containing DFHCCUTL.
        required: false
        type: str
    dfhlcd:
        description:
            - Specify the input local catalog data set
        required: true
        type: str
"""

RETURN = r"""
msg:
    description: The execution result message.
    returned : always
    type: str
    sample: "The DFHCCUTL program executed successfully."
rc:
    description: The return code.
    returned : always
    type: str
content:
    description: The output data set for results, information and error/dump messages.
    returned: always
    type: str
changed:
    description: Indicates if any changes were made during module operation.
    returned: always
    type: bool
"""

EXAMPLES = r"""
  - name: Initialize the LCD
    cics_local_catalog_initialization:
      steplib: CTS550.CICS720.SDFHLOAD
      dfhlcd: BJMAXY.CICS.IYK3ZMX7.DFHLCD
"""

import re
from traceback import format_exc
from ansible.module_utils.basic import AnsibleModule, env_fallback, AnsibleFallbackNotFound

MVSCMD = "mvscmd"
CICS_UTILITY = "dfhccutl"


def run_cics_program(steplib, dfhlcd, module):
    try:
        mvscmd_suffix_script = ' --pgm=' + CICS_UTILITY + ' --steplib=' + steplib + ' --dfhlcd=' + dfhlcd + \
                               ' --sysprint=stdout --sysudump=stdout'

        mvscmd_command = MVSCMD + mvscmd_suffix_script
        rc, stdout, stderr = module.run_command(mvscmd_command, use_unsafe_shell=True)
    except Error as e:
        raise cics_local_catalog_initialization_Error(e)
    return (rc, stdout, stderr)


def validate_module_params(params):
    regex_dataset = "^(([A-Z]{1}[A-Z0-9]{0,7})([.]{1})){1,21}[A-Z]{1}[A-Z0-9]{0,7}$"
    pattern = re.compile(regex_dataset)
    steplib = params.get("steplib")
    dfhlcd = params.get("dfhlcd")
    if pattern.fullmatch(steplib):
        pass
    else:
        raise cics_local_catalog_initialization_Error("The dataset name format of option steplib "
                                                      + steplib + " is not supported.")
    if pattern.fullmatch(dfhlcd):
        pass
    else:
        raise cics_local_catalog_initialization_Error("The dataset name format of option dfhlcd "
                                                      + dfhlcd + " is not supported.")


def run_module():
    module_args = dict(
        steplib=dict(type='str', required=False),
        dfhlcd=dict(type='str', required=True),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
    result = dict(
        changed=False,
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
        dfhlcd = module.params.get("dfhlcd")
        rc, stdout, stderr = run_cics_program(steplib, dfhlcd, module)

        result['content'] = stdout
        result['rc'] = rc
        if rc == 0:
            result['msg'] = "CICS DFHCCUTL program executed successfully."
            result['changed'] = True
            module.exit_json(**result)
        else:
            module.fail_json(msg="CICS DFHCCUTL program execution failed.", **result)
    except cics_local_catalog_initialization_Error as e:
        trace = format_exc()
        module.fail_json(
            msg="An unexpected error occurred: {0}".format(trace), **result)
    except Error as e:
        module.fail_json(msg=e.msg, **result)


class Error(Exception):
    pass


class cics_local_catalog_initialization_Error(Error):
    def __init__(self, error):
        self.msg = 'An error occurred during execution of CICS DFCCMUTL module --- "{0}"'.format(error)


def main():
    run_module()


if __name__ == '__main__':
    main()
