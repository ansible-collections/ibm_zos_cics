#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) IBM Corporation 2020
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

DOCUMENTATION = r'''
---
module: cmci_create
short_description: Create CICS and CICSplex definitions in CSD and BAS repositories
description:
  - The cmci_create module can be used to create definitional CICS and CICSPlex® SM resources in CICS
    regions, using the CMCI API.  The CMCI API is provided by CICSplex SM, or in SMSS regions.  For information about
    the CMCI API see
    U(https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/cmci/clientapi_overview.html).
    For information about how to compose POST requests, see
    U(https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/cmci/clientapi_post.html).
author: "IBM"
extends_documentation_fragment:
  - ibm.ibm_zos_cics.cmci.COMMON
  - ibm.ibm_zos_cics.cmci.ATTRIBUTES
  - ibm.ibm_zos_cics.cmci.PARAMETERS
'''


EXAMPLES = r"""
- name: define a BUNDLE in a CSD
  cmci_create:
      cmci_host: 'winmvs2c.hursley.ibm.com'
      cmci_port: '10080'
      context: 'iyk3z0r9'
      resource_name: 'CICSDefinitionBundle'
      attributes:
        name: PONGALT
        BUNDLEDIR: /u/ibmuser/bundle/pong/pongbundle_1.0.0
        csdgroup: JVMGRP
      parameters:
        csd: null
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
    AnsibleCMCIModule, PARAMETERS, ATTRIBUTES, append_attributes, append_parameters,
    append_attributes_parameters_arguments
)
from typing import Optional, Dict


class AnsibleCMCICreateModule(AnsibleCMCIModule):
    def __init__(self):
        super(AnsibleCMCICreateModule, self).__init__('POST')

    def init_argument_spec(self):  # type: () -> Dict
        argument_spec = super(AnsibleCMCICreateModule, self).init_argument_spec()
        append_attributes_parameters_arguments(argument_spec)
        return argument_spec

    def init_body(self):  # type: () -> Optional[Dict]
        create = {}
        append_parameters(create, self._p.get(PARAMETERS))
        append_attributes(create, self._p.get(ATTRIBUTES))

        return {
            'request': {
                'create': create
            }
        }


def main():
    AnsibleCMCICreateModule().main()


if __name__ == '__main__':
    main()
