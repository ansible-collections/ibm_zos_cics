# -*- coding: utf-8 -*-

# Copyright (c) IBM Corporation 2019, 2020
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.cmci import (
    AnsibleCMCIModule, RESOURCE, append_criteria_parameter_arguments
)

from typing import Dict, Optional

DOCUMENTATION = r'''
---
module: cmci_install
short_description: Install CICS and CICSplex SM definitions
description:
  - The cmci_install module can be used to install CICS and CICSPlex® SM resources into CICS regions from definitions,
    using the CMCI API.  The CMCI API is provided by CICSplex SM, or in SMSS regions.  For information about the CMCI
    API see
    U(https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/cmci/clientapi_overview.html).
    For information about how to compose PUT requests, see
    U(https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/cmci/clientapi_put.html).
author: "IBM"
extends_documentation_fragment:
  - ibm.ibm_zos_cics.cmci.COMMON
  - ibm.ibm_zos_cics.cmci.RESOURCE
  - ibm.ibm_zos_cics.cmci.PARAMETERS
options:
  location:
    description:
      - The location that resource been installed to.
      - This variable only work with option 'install'.
    type: str
    required: false
    choices:
      - BAS
      - CSD
'''


EXAMPLES = r"""
- name: get a localfile in a CICS region
  cics_cmci:
    cmci_host: 'winmvs2c.hursley.ibm.com'
    cmci_port: '10080'
    cmci_user: 'ibmuser'
    cmci_password: '123456'
    context: 'iyk3z0r9'
    option: 'query'
    resource:
      - type: CICSLocalFile
    record_count: 2
    criteria: 'dsname=XIAOPIN* and file=DFH*'

- name: define a bundle in a CICS region
  cics_cmci:
      cmci_host: 'winmvs2c.hursley.ibm.com'
      cmci_port: '10080'
      context: 'iyk3z0r9'
      option: 'define'
      resource:
        - type: CICSDefinitionBundle
          attributes:
            - name: PONGALT
              BUNDLEDIR: /u/ibmuser/bundle/pong/pongbundle_1.0.0
              csdgroup: JVMGRP
          parameters:
            - name: CSD
      record_count: 1

- name: install a bundle in a CICS region
  cics_cmci:
    cmci_host: 'winmvs2c.hursley.ibm.com'
    cmci_port: '10080'
    context: 'iyk3z0r9'
    option: 'install'
    resource:
      - type: CICSDefinitionBundle
        location: CSD
    criteria: 'NAME=PONGALT'
    parameter: 'CSDGROUP(JVMGRP)'

- name: update a bundle definition in a CICS region
  cics_cmci:
    cmci_host: 'winmvs2c.hursley.ibm.com'
    cmci_port: '10080'
    context: 'iyk3z0r9'
    option: 'update'
    resource:
      - type: CICSDefinitionBundle
        attributes:
          - description: 'forget description'
        parameters:
          - name: CSD
    criteria: 'NAME=PONGALT'
    parameter: 'CSDGROUP(JVMGRP)'

- name: install a bundle in a CICS region
  cics_cmci:
    cmci_host: 'winmvs2c.hursley.ibm.com'
    cmci_port: '10080'
    context: 'iyk3z0r9'
    option: 'update'
    resource:
      - type: CICSBundle
        attributes:
          - Enablestatus: disabled
    criteria: 'NAME=PONGALT'

- name: delete a bundle in a CICS region
  cics_cmci:
    cmci_host: 'winmvs2c.hursley.ibm.com'
    cmci_port: '10080'
    security_type: 'yes'
    context: 'iyk3z0r9'
    option: 'delete'
    resource:
      - type: CICSBundle
    criteria: 'NAME=PONGALT'

- name: delete a bundle definition in a CICS region
  cics_cmci:
    cmci_host: 'winmvs2c.hursley.ibm.com'
    cmci_port: '10080'
    context: 'iyk3z0r9'
    option: 'delete'
    resource:
      - type: CICSDefinitionBundle
    criteria: 'NAME=PONGALT'
    parameter: 'CSDGROUP(JVMGRP)'

- name: get a localfile in a CICS region
  cics_cmci:
    cmci_host: 'winmvs2c.hursley.ibm.com'
    cmci_port: '10080'
    cmci_cert: './sec/ansible.pem'
    cmci_key: './sec/ansible.key'
    connection_type: 'certificate'
    context: 'iyk3z0r9'
    option: 'query'
    resource:
      - type: CICSLocalFile
    record_count: 1
    criteria: 'dsname=XIAOPIN* AND file=DFH*'
"""


RETURN = r"""
changed:
  description: True if the state was changed, otherwise False
  returned: always
  type: bool
failed:
  description: True if query_job failed, othewise False
  returned: always
  type: bool
connect_version:
  description: Version of the CMCI API
  returned: success
  type: str
cpsm_reason:
  description:
    - Character value of the CPSM API reason code returned.  For a list of reason values provided by each API command,
      see
      U(https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/commands-cpsm/eyup2kr.html)
  returned: success
  type: str
cpsm_reason_code:
  description:
    - Numeric value of the CPSM API reason code returned.  For a list of numeric values see
      U(https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/commands-cpsm/eyup2ks.html)
  returned: success
  type: int
cpsm_response:
  description:
    - Character value of the CPSM API response code returned.  For a list of response values provided by each API
      command, see
      U(https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/commands-cpsm/eyup2kr.html)
  returned: success
  type: str
cpsm_response_code:
  description:
    - Numeric value of the CPSM API response code returned.  For a list of numeric values see
      U(https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/commands-cpsm/eyup2ks.html)
  returned: success
  type: str
http_status:
  description:
    - Message associated with HTTP status code returned by CMCI
  returned: success
  type: str
http_status_code:
  description:
    - HTTP status code returned by CMCI
  returned: success
  type: int
record_count:
  description:
    - Number of records returned
  returned: success
  type: int
records:
  description:
    - A list of the returned records
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
    description: Number of resources that the action completed successfully for
    returned: success
    type: int
request:
  description: Information about the request that was made to CMCI
  returned: success
  type: dict
  contains:
    body:
      description: The XML body sent with the request, if any
      returned: success
      type: str
    method:
      description: The HTTP method used for the request
      returned: success
      type: str
    url:
      description: The URL used for the request
      returned: success
      type: str
"""


LOCATION = 'location'


class AnsibleCMCIInstallModule(AnsibleCMCIModule):
    def __init__(self):
        super(AnsibleCMCIInstallModule, self).__init__('PUT')

    def init_argument_spec(self):  # type: () -> Dict
        argument_spec = super(AnsibleCMCIInstallModule, self).init_argument_spec()
        argument_spec[RESOURCE]['options'][LOCATION] = {
            'type': 'str',
            'required': False,
            'choices': ['BAS', 'CSD']
        }
        append_criteria_parameter_arguments(argument_spec)
        return argument_spec

    def init_body(self):  # type: () -> Optional[Dict]
        location = self._p.get(RESOURCE).get(LOCATION)
        return {
            'request': {
                'action': {
                    '@name': 'INSTALL' if location == 'BAS' else 'CSDINSTALL'
                }
            }
        }

    def init_request_params(self):  # type: () -> Optional[Dict[str, str]]
        return self.get_criteria_parameter_request_params()


def main():
    AnsibleCMCIInstallModule().main()


if __name__ == '__main__':
    main()
