#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2020,2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: cmci_action
short_description: Perform actions on CICS and CICSPlex SM resources
description:
  - Perform actions on CICS® or CICSPlex® SM definitions and resources, by
    initiating PUT requests via the CMCI REST API. The CMCI REST API can be
    configured in CICSPlex SM or stand-alone regions (SMSS). For information
    about the API, see
    L(CMCI REST API,https://www.ibm.com/docs/en/cics-ts/latest?topic=programming-cmci-rest-api-reference).
    For information about how to compose PUT requests, see
    L(CMCI PUT requests,https://www.ibm.com/docs/en/cics-ts/latest?topic=requests-cmci-put).
version_added: 1.0.0
author:
  - Stewart Francis (@stewartfrancis)
  - Tom Latham (@Tom-Latham)
  - Sophie Green (@sophiegreen)
  - Ya Qing Chen (@vera-chan)
extends_documentation_fragment:
  - ibm.ibm_zos_cics.cmci.COMMON
  - ibm.ibm_zos_cics.cmci.RESOURCES
options:
  action_name:
    description: >
      The name of the target action. To find the name of the appropriate action,
      consult the CICSPlex SM resource tables for the target resource type. For
      example, the
      L(PROGRAM resource table reference,https://www.ibm.com/docs/en/cics-ts/latest?topic=tables-program-resource-table)
      lists the eligible actions for CICS programs.
    type: str
    required: true
  action_parameters:
    description: >
      A list of one or more parameters that control the I(action) operation.
      Eligible actions and corresponding parameters for the target operation can
      be found in the resource table reference for the target resource type, as
      listed in the PERFORM SET operation section of the "Valid CPSM operations"
      table. For example, the valid parameters for a PROGDEF CSDCOPY action are
      C(AS_RESOURCE), C(DUPACTION) and C(TO_CSDGROUP), as found in the
      L(PROGDEF resource table reference,https://www.ibm.com/docs/en/cics-ts/latest?topic=tables-progdef-resource-table).
    type: list
    elements: dict
    suboptions:
      name:
        description: Parameter name for the PERFORM SET operation.
        required: true
        type: str
      value:
        description: >
          Parameter value if any. Can be omitted if the parameter requires no
          value to be supplied, as shown in the resource table reference. For
          example, the OVERRIDE parameter for the PROGDEF INSTALL action doesn't
          require a value.
        required: false
        type: str
    required: false
'''


EXAMPLES = r"""
- name: Newcopy a program
  cmci_action:
    cmci_host: "example.com"
    cmci_port: 12345
    context: ABCDEFGH # context is the name of your CICSplex in a CPSM environment or the applid of your region in an SMSS environment
    type: CICSProgram
    action_name: NEWCOPY
    resources:
      filter:
        name: PONGALT

- name: Install a bundle definition from CSD in a CICS region
  cmci_action:
    cmci_host: "example.com"
    cmci_port: 1234
    context: ABCDEFGH # context is the name of your CICSplex in a CPSM environment or the applid of your region in an SMSS environment
    scope: IJKLMNOP # scope only applies if you're in a CPSM environment and is the name of a CICS system definition (CSYSDEF) or CICS system group (CSYSGRP)
    type: CICSBundle
    action_name: CSDINSTALL
    resources:
      filter:
        name: mybund
      get_parameters:
        - name: csdgroup
          value: mygrp
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
    - The character value of the REASON code returned by each CICSPlex SM API
      command. For a list of REASON character values, see
      https://www.ibm.com/docs/en/cics-ts/latest?topic=values-eyuda-reason-in-alphabetical-order.
  returned: success
  type: str
cpsm_reason_code:
  description:
    - The numeric value of the REASON code returned by each CICSPlex SM API
      command. For a list of REASON numeric values, see
      https://www.ibm.com/docs/en/cics-ts/latest?topic=values-eyuda-reason-in-numerical-order.
  returned: success
  type: int
cpsm_response:
  description:
    - The character value of the RESPONSE code returned by each CICSPlex SM API
      command. For a list of RESPONSE character values, see
      https://www.ibm.com/docs/en/cics-ts/latest?topic=values-eyuda-response-in-alphabetical-order.
  returned: success
  type: str
cpsm_response_code:
  description:
    - The numeric value of the RESPONSE code returned by each CICSPlex SM API
      command. For a list of RESPONSE numeric values, see
      https://www.ibm.com/docs/en/cics-ts/latest?topic=values-eyuda-response-in-numerical-order.
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
  description:
    - The number of resources for which the action completed successfully.
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
feedback:
  description: Diagnostic data from FEEDBACK records associated with the request
  returned: cmci error
  type: list
  elements: dict
  contains:
    action:
      description: The name of the action that has failed.
      returned: cmci error
      type: str
    attribute1:
      description: The name of one of up to six attributes associated with the error.
      returned: cmci error
      type: str
    attribute2:
      description: The name of one of up to six attributes associated with the error.
      returned: cmci error
      type: str
    attribute3:
      description: The name of one of up to six attributes associated with the error.
      returned: cmci error
      type: str
    attribute4:
      description: The name of one of up to six attributes associated with the error.
      returned: cmci error
      type: str
    attribute5:
      description: The name of one of up to six attributes associated with the error.
      returned: cmci error
      type: str
    attribute6:
      description: The name of one of up to six attributes associated with the error.
      returned: cmci error
      type: str
    eibfn:
      description: The function code associated with the request.
      returned: cmci error
      type: str
    eibfn_alt:
      description: The name of the function associated with the request.
      returned: cmci error
      type: str
    errorcode:
      description: The CICSPlex® SM error code associated with the resource.
      returned: cmci error
      type: str
    eyu_cicsname:
      description: The name of the CICS region or CICSplex associated with the error.
      returned: cmci error
      type: str
    keydata:
      description: A string of data that identifies the instance of a resource associated with the error.
      returned: cmci error
      type: str
    resp:
      description: The CICS RESP code or the CICSPlex SM API EYUDA response code as a numeric value.
      returned: cmci error
      type: str
    resp2:
      description: The CICS RESP2 code or the CICSPlex SM API EYUDA reason code as a numeric value.
      returned: cmci error
      type: str
    resp_alt:
      description: >
        The text equivalent for the resp value. For example, the text equivalent of a resp value of 16 is INVREQ.
      returned: cmci error
      type: str
    installerror:
      description: >
        Contains diagnostic data from a BINSTERR record associated with a CICS® management client interface PUT install request.
      returned: cmci error
      type: list
      elements: dict
      contains:
        eibfn:
          description: The function code associated with the request.
          returned: cmci error
          type: str
        eyu_cicsname:
          description: The name of the CICS region or CICSplex associated with the installation error.
          returned: cmci error
          type: str
        cresp1:
          description: The CICS RESP code or the CICSPlex® SM API EYUDA response code as a numeric value.
          returned: cmci error
          type: str
        cresp2:
          description: The CICS RESP2 code or the CICSPlex SM API EYUDA reason code as a numeric value.
          returned: cmci error
          type: str
        errorcode:
          description: The CICSPlex SM error code associated with the resource.
          returned: cmci error
          type: str
        ressname:
          description: The name of the resource associated with the error.
          returned: cmci error
          type: str
        resver:
          description: The version number of the resource associated with the error.
          returned: cmci error
          type: str
    inconsistentscope:
      description: >
        Contains diagnostic data from a BINCONSC record associated with a CICS® management client interface PUT request.
      returned: cmci error
      type: list
      elements: dict
      contains:
        eibfn:
          description: The function code associated with the request.
          returned: cmci error
          type: str
        eyu_cicsname:
          description: The name of the CICS region or CICSplex associated with the installation error.
          returned: cmci error
          type: str
        erroroperation:
          description: A numeric value that identifies the operation being performed when the error occurred.
          returned: cmci error
          type: str
        errorcode:
          description: The CICSPlex® SM error code associated with the resource.
          returned: cmci error
          type: str
        targetassignment:
          description: The assignment for the target scope.
          returned: cmci error
          type: str
        targetdescription:
          description: The resource description for the target scope.
          returned: cmci error
          type: str
        relatedassignment:
          description: The resource assignment for the related scope.
          returned: cmci error
          type: str
        relateddescription:
          description: The resource description for the related scope.
          returned: cmci error
          type: str
        relatedscope:
          description: The name of the related scope.
          returned: cmci error
          type: str
    inconsistentset:
      description: >
        Contains diagnostic data from a BINCONRS record associated with a CICS® management client interface PUT request.
      returned: cmci error
      type: list
      elements: dict
      contains:
        candidatename:
          description: The name of the candidate resource.
          returned: cmci error
          type: str
        candidateversion:
          description: The version number of the candidate resource.
          returned: cmci error
          type: str
        candidategroup:
          description: The resource group of the candidate resource.
          returned: cmci error
          type: str
        candidateassignment:
          description: The assignment of the candidate resource.
          returned: cmci error
          type: str
        candidatedescription:
          description: The description of the candidate resource.
          returned: cmci error
          type: str
        candidateusage:
          description: The assignment usage of the candidate resource.
          returned: cmci error
          type: str
        candidatesystemgroup:
          description: The system group of the candidate resource.
          returned: cmci error
          type: str
        candidatetype:
          description: The system type of the candidate resource.
          returned: cmci error
          type: str
        candidateoverride:
          description: The assignment override of the candidate resource.
          returned: cmci error
          type: str
        eyu_cicsname:
          description: The name of the CICS region associated with the installation error.
          returned: cmci error
          type: str
        erroroperation:
          description: >
            A numeric value that identifies that the operation being performed when the error occurred
          returned: cmci error
          type: str
        existingname:
          description: The name of the existing resource.
          returned: cmci error
          type: str
        existingversion:
          description: The version number of the existing resource.
          returned: cmci error
          type: str
        existinggroup:
          description: The resource group of the existing resource.
          returned: cmci error
          type: str
        existingassignment:
          description: The assignment of the existing resource.
          returned: cmci error
          type: str
        existingdescription:
          description: The description of the existing resource.
          returned: cmci error
          type: str
        existingusage:
          description: The assignment usage of the existing resource.
          returned: cmci error
          type: str
        existingsystemgroup:
          description: The system group of the existing resource.
          returned: cmci error
          type: str
        existingtype:
          description: The system type of the existing resource.
          returned: cmci error
          type: str
        existingoverride:
          description: The assignment override of the existing resource.
          returned: cmci error
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
        super(AnsibleCMCIInstallModule, self).__init__('PUT')

    def init_argument_spec(self):  # type: () -> Dict
        argument_spec = super(AnsibleCMCIInstallModule, self)\
            .init_argument_spec()
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
