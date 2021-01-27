#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) IBM Corporation 2020
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: cmci_action
short_description: Install CICS and CICSPlex SM definitions
description:
  - Perform actions on CICS® or CICSPlex® SM definitions and resources, by initiating PUT requests via the CMCI REST API.
    The CMCI REST API can be configured in CICSPlex SM or stand-alone regions (SMSS). For information about the API,
    see L(CMCI REST API,
    https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/cmci/clientapi_overview.html).
    For information about how to compose PUT requests, see L(CMCI PUT requests,
    https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/cmci/clientapi_put.html).
author:
  - Stewart Francis (@stewartfrancis)
  - Tom Latham (@Tom-Latham)
  - Sophie Green (@sophiegreen)
extends_documentation_fragment:
  - ibm.ibm_zos_cics.cmci.COMMON
  - ibm.ibm_zos_cics.cmci.RESOURCES
options:
  action_name:
    description: >
      The name of the target action. To find the name of the appropriate action, consult the CICSPlex SM resource
      tables for the target resource type. For example, the L(PROGRAM resource table reference,
      https://www.ibm.com/support/knowledgecenter/en/SSGMCP_5.6.0/reference-cpsm-restables/cpsm-restables/PROGRAMtab.html)
      lists the eligible actions for CICS programs.
    type: str
    required: true
  action_parameters:
    description: >
      A list of one or more parameters that control the I(action) operation. Eligible actions and 
      corresponding parameters for the target operation can be found in the resource table reference 
      for the target resource type, as listed in the PERFORM SET operation section of the "Valid CPSM operations" table.
      For example, the valid parameters for a PROGDEF CSDCOPY action are AS_RESOURCE, DUPACTION and
      TO_CSDGROUP, as found in the L(PROGDEF resource table reference,
      https://www.ibm.com/support/knowledgecenter/en/SSGMCP_5.6.0/reference-cpsm-restables/cpsm-restables/PROGDEFtab.html).
    type: list
    elements: dict
    suboptions:
      name:
        description: Parameter name for the PERFORM SET operation.
        required: true
        type: str
      value:
        description: > 
          Parameter value if any. Can be omitted if the parameter requires no value to be supplied, as shown
          in the resource table reference. For example, the OVERRIDE parameter for the PROGDEF INSTALL action 
          doesn't require a value.
        required: false
        type: str
    required: false
'''


EXAMPLES = r"""
- name: Newcopy a program
  cmci_action:
    cmci_host: 'winmvs2c.hursley.ibm.com'
    cmci_port: '10080'
    context: 'iyk3z0r9'
    type: 'CICSProgram'
    action_name: NEWCOPY
    resource:
      filter:
        name: 'PONGALT'
      parameters:
        - name: 'csdgroup'
          value: 'JVMGRP'

- name: install a bundle in a CICS region
  cmci_action:
    cmci_host: 'winmvs2c.hursley.ibm.com'
    cmci_port: '10080'
    context: 'iyk3z0r9'
    type: CICSBundle
    action_name: install
    resource:
      filter:
        name: 'PONGALT'
    parameters:
      - name: 'usage'
        value: 'local'
"""


RETURN = r"""
changed:
  description: True if the state was changed, otherwise False.
  returned: always
  type: bool
failed:
  description: True if the query job failed, otherwise False.
  returned: always
  type: bool
connect_version:
  description: Version of the CMCI REST API.
  returned: success
  type: str
cpsm_reason:
  description:
    - The character value of the REASON code returned by each CICSPlex SM API command.
      For a list of REASON character values, see
      https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/commands-cpsm/eyup2ky.html.
  returned: success
  type: str
cpsm_reason_code:
  description:
    - The numeric value of the REASON code returned by each CICSPlex SM API command.
      For a list of REASON numeric values, see
      https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/commands-cpsm/eyup2kw.html.
  returned: success
  type: int
cpsm_response:
  description:
    - The character value of the RESPONSE code returned by each CICSPlex SM API command.
      For a list of RESPONSE character values, see
      https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/commands-cpsm/eyup2kx.html.
  returned: success
  type: str
cpsm_response_code:
  description:
    - The numeric value of the RESPONSE code returned by each CICSPlex SM API command.
      For a list of RESPONSE numeric values, see
      https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/commands-cpsm/eyup2kv.html.
  returned: success
  type: str
http_status:
  description:
    - The message associated with HTTP status code that is returned by CMCI.
  returned: success
  type: str
http_status_code:
  description:
    - The HTTP status code returned by CMCI.
  returned: success
  type: int
record_count:
  description:
    - The number of records returned.
  returned: success
  type: int
records:
  description:
    - A list of the returned records.
  returned: success
  type: list
  elements: dict
  sample:
    - _keydata: "C1D5E2C9E3C5E2E3"
      aloadtime: "00:00:00.000000"
      apist: "CICSAPI"
      application: ""
      applmajorver: "-1"
      applmicrover: "-1"
      applminorver: "-1"
      basdefinever: "0"
      cedfstatus: "CEDF"
      changeagent: "CSDAPI"
      changeagrel: "0730"
      changetime: "2020-12-15T02:34:31.000000+00:00"
      changeusrid: "YQCHEN"
      coboltype: "NOTAPPLIC"
      concurrency: "QUASIRENT"
      copy: "NOTREQUIRED"
      currentloc: "NOCOPY"
      datalocation: "ANY"
      definesource: "ANSITEST"
      definetime: "2020-12-15T02:34:29.000000+00:00"
      dynamstatus: "NOTDYNAMIC"
      entrypoint: "FF000000"
      execkey: "USEREXECKEY"
      executionset: "FULLAPI"
      eyu_cicsname: "IYCWEMW2"
      eyu_cicsrel: "E730"
      eyu_reserved: "0"
      fetchcnt: "0"
      fetchtime: "00:00:00.000000"
      holdstatus: "NOTAPPLIC"
      installagent: "CSDAPI"
      installtime: "2020-12-15T02:34:33.000000+00:00"
      installusrid: "YQCHEN"
      jvmclass: ""
      jvmserver: ""
      language: "NOTDEFINED"
      length: "0"
      library: ""
      librarydsn: ""
      loadpoint: "FF000000"
      lpastat: "NOTAPPLIC"
      newcopycnt: "0"
      operation: ""
      pgrjusecount: "0"
      platform: ""
      program: "ANSITEST"
      progtype: "PROGRAM"
      remotename: ""
      remotesystem: ""
      removecnt: "0"
      rescount: "0"
      residency: "NONRESIDENT"
      rloading: "0.000"
      rplid: "0"
      rremoval: "0.000"
      runtime: "UNKNOWN"
      ruse: "0.000"
      sharestatus: "PRIVATE"
      status: "DISABLED"
      transid: ""
      useagelstat: "0"
      usecount: "0"
      usefetch: "0.000"
success_count:
    description: The number of resources for which the action completed successfully.
    returned: success
    type: int
request:
  description: Information about the request that was made to CMCI.
  returned: success
  type: dict
  contains:
    body:
      description: The XML body sent with the request, if any.
      returned: success
      type: str
    method:
      description: The HTTP method used for the request.
      returned: success
      type: str
    url:
      description: The URL used for the request.
      returned: success
      type: str
"""


from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.cmci import (
    AnsibleCMCIModule, RESOURCES_ARGUMENT, parameters_argument
)

from typing import Dict, Optional
from collections import OrderedDict


ACTION_NAME = 'action_name'
ACTION_PARAMETERS = 'action_parameters'


class AnsibleCMCIInstallModule(AnsibleCMCIModule):
    def __init__(self):
        # pylint: disable=super-with-arguments
        super(AnsibleCMCIInstallModule, self).__init__('PUT')

    def init_argument_spec(self):  # type: () -> Dict
        # pylint: disable=super-with-arguments
        argument_spec = super(AnsibleCMCIInstallModule, self).init_argument_spec()
        argument_spec.update({
            'action_name': {
                'type': 'str',
                'required': True
            }
        })
        argument_spec.update(RESOURCES_ARGUMENT)
        argument_spec.update(parameters_argument(ACTION_PARAMETERS))
        return argument_spec

    def init_body(self):  # type: () -> Optional[Dict]

        action = OrderedDict({'@name': self._p.get(ACTION_NAME)})
        self.append_parameters(ACTION_PARAMETERS, action)
        return {
            'request': {
                'action': action
            }
        }

    def init_request_params(self):  # type: () -> Optional[Dict[str, str]]
        return self.get_resources_request_params()


def main():
    AnsibleCMCIInstallModule().main()


if __name__ == '__main__':
    main()
