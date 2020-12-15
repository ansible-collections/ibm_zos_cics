# -*- coding: utf-8 -*-

# Copyright (c) IBM Corporation 2019, 2020
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.cmci import (
    AnsibleCMCIModule, RESOURCE, PARAMETERS, ATTRIBUTES, append_parameters, append_attributes,
    append_attributes_parameters_arguments, append_criteria_parameter_arguments
)
from typing import Optional, Dict

DOCUMENTATION = r'''
---
module: cmci_update
short_description: Get CICS and CICSplex SM resources
description:
  - The cmci_update module can be used to make changes to CICS and CICSPlex® SM resources in CICS regions
    using the CMCI API.  The CMCI API is provided by CICSplex SM, or in SMSS regions.  For information about the CMCI
    API see
    U(https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/cmci/clientapi_overview.html).
    For information about how to compose PUT requests, see
    U(https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/cmci/clientapi_put.html).
author: "IBM"
extends_documentation_fragment:
  - ibm.ibm_zos_cics.cmci.COMMON
  - ibm.ibm_zos_cics.cmci.RESOURCE
  - ibm.ibm_zos_cics.cmci.ATTRIBUTES
  - ibm.ibm_zos_cics.cmci.PARAMETERS
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
url:
    description: The cmci url that been composed
    returned: always
    type: str
api_response:
    description: Indicate if the cmci request been issued successfully or not
    returned: always
    type: str
response:
    description: The response of cmci request
    returned: success
    type: dict
    sample:
        {   "records": {
                "cicsdefinitionlibrary": {
                    "_keydata": "D7D6D5C74040404000D1E5D4C7D9D74040",
                    "changeagent": "CSDAPI",
                    "changeagrel": "0710",
                    "changetime": "2020-06-16T10:40:50.000000+00:00",
                    "changeusrid": "CICSUSER",
                    "createtime": "2020-06-16T10:40:50.000000+00:00",
                    "critical": "NO",
                    "csdgroup": "JVMGRP",
                    "defver": "0",
                    "desccodepage": "0",
                    "description": "",
                    "dsname01": "XIAOPIN.PONG.LOADLIB",
                    "dsname02": "",
                    "dsname03": "",
                    "dsname04": "",
                    "dsname05": "",
                    "dsname06": "",
                    "dsname07": "",
                    "dsname08": "",
                    "dsname09": "",
                    "dsname10": "",
                    "dsname11": "",
                    "dsname12": "",
                    "dsname13": "",
                    "dsname14": "",
                    "dsname15": "",
                    "dsname16": "",
                    "name": "PONG",
                    "ranking": "50",
                    "status": "ENABLED",
                    "userdata1": "",
                    "userdata2": "",
                    "userdata3": ""
                }
            },
          "resultsummary": {
                "api_response1": "1024",
                "api_response1_alt": "OK",
                "api_response2": "0",
                "api_response2_alt": "",
                "displayed_recordcount": "1",
                "recordcount": "1"
            }
      }

"""


class AnsibleCMCIUpdateModule(AnsibleCMCIModule):
    def __init__(self):
        super(AnsibleCMCIUpdateModule, self).__init__('PUT')

    def init_argument_spec(self):  # type: () -> Dict
        argument_spec = super(AnsibleCMCIUpdateModule, self).init_argument_spec()
        append_attributes_parameters_arguments(argument_spec)
        append_criteria_parameter_arguments(argument_spec)
        return argument_spec

    def init_body(self):  # type: () -> Optional[Dict]
        resource = self._p.get(RESOURCE)

        update = {}
        append_parameters(update, resource.get(PARAMETERS))
        append_attributes(update, resource.get(ATTRIBUTES))

        return {
            'request': {
                'update': update
            }
        }

    def init_request_params(self):  # type: () -> Optional[Dict[str, str]]
        return self.get_criteria_parameter_request_params()


def main():
    AnsibleCMCIUpdateModule().main()


if __name__ == '__main__':
    main()
