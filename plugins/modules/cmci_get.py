#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) IBM Corporation 2020
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

DOCUMENTATION = r'''
---
module: cmci_get
short_description: Query CICS and CICSplex SM resources
description:
  - The cmci_get module can be used to get information about installed and definitional
    CICS and CICSPlex® SM resources from CICS regions, using the CMCI API.  The CMCI API is provided by 
    CICSplex SM, or in SMSS regions.  For information about the CMCI API see
    U(https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/cmci/clientapi_overview.html).
    For information about how to compose GET requests, see
    U(https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/cmci/clientapi_get.html).
author: "IBM"
extends_documentation_fragment:
  - ibm.ibm_zos_cics.cmci.COMMON
  - ibm.ibm_zos_cics.cmci.RESOURCE
options:
  record_count:
    description:
      - Identifies a subset of records in a results cache starting from the
        first record in the results cache or from the record specified
        by the index parameter.
      - A negative number indicates a count back from the last record; for
        example, -1 means the last record, -2 the last record but one, and so
        on
      - Count must be an integer, a value of zero is not permitted.
    type: int
    required: false
'''


EXAMPLES = r"""
- name: get 2 LOCFILEs from a CICSplex
  cmci_get:
    cmci_host: 'winmvs2c.hursley.ibm.com'
    cmci_port: '10080'
    cmci_user: 'ibmuser'
    cmci_password: '123456'
    context: 'iyk3z0r9'
    resource_name:  CICSLocalFile
    record_count: 2
    resource:
      filter:
        dsname: 'CTS*'

- name: get a localfile in a CICS region
  cmci_get:
    cmci_host: 'winmvs2c.hursley.ibm.com'
    cmci_port: '10080'
    cmci_cert: './sec/ansible.pem'
    cmci_key: './sec/ansible.key'
    context: 'iyk3z0r9'
    option: 'query'
    resource_name: 'CICSLocalFile' 
    resource:
      filter:
        dsname: 'XIAOPIN*'
        file: 'DFH*'
    record_count: 1
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


from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.cmci import (
    AnsibleCMCIModule, append_resources_argument
)

from typing import Dict, Optional


_RECORD_COUNT = 'record_count'


class AnsibleCMCIGetModule(AnsibleCMCIModule):
    def __init__(self):
        super(AnsibleCMCIGetModule, self).__init__('GET')

    def init_argument_spec(self):  # type: () -> Dict
        argument_spec = super(AnsibleCMCIGetModule, self).init_argument_spec()
        argument_spec.update({
            _RECORD_COUNT: {
                'type': 'int'
            }
        })
        append_resources_argument(argument_spec)
        return argument_spec

    def init_request_params(self):  # type: () -> Optional[Dict[str, str]]
        return self.get_resources_request_params()

    def init_url(self):  # type: () -> str
        url = super(AnsibleCMCIGetModule, self).init_url()

        if self._p.get(_RECORD_COUNT):
            url = url + '//' + str(self._p.get(_RECORD_COUNT))

        return url


def main():
    AnsibleCMCIGetModule().main()


if __name__ == '__main__':
    main()
