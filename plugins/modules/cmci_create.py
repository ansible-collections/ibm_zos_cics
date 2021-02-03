#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) IBM Corporation 2020
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: cmci_create
short_description: Create CICS and CICSPlex SM definitions
description:
  - Create definitional CICS® or CICSPlex® SM resources in CSD and BAS 
    repositories, by initiating POST requests via the CMCI REST API. 
    The CMCI REST API can be configured in CICSPlex SM or stand-alone
    regions (SMSS). For information about the API, see
    L(CMCI REST API,
    https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/cmci/clientapi_overview.html).
    For information about how to compose POST requests, see L(CMCI POST requests,
    https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/cmci/clientapi_post.html).
author: IBM
extends_documentation_fragment:
  - ibm.ibm_zos_cics.cmci.COMMON
  - ibm.ibm_zos_cics.cmci.ATTRIBUTES
options:
  create_parameters:
    description: >
      A list of one or more parameters that control the I(create) operation.
      Eligible parameters for the CREATE operation can be found in the
      resource table reference for the target resource type, as listed in the
      CREATE operation section of the "Valid CPSM operations" table.
      For example, the valid parameters for a PROGDEF CREATE operation
      are CSD and RESGROUP, as found in the L(PROGDEF resource table reference,
      https://www.ibm.com/support/knowledgecenter/en/SSGMCP_5.6.0/reference-cpsm-restables/cpsm-restables/PROGDEFtab.html).
    type: list
    elements: dict
    suboptions:
      name:
        description: Parameter name for the CREATE operation.
        required: true
        type: str
      value:
        description: 
          - Parameter value if any. Can be omitted if the parameter
            requires no value to be supplied, as shown
            in the resource table reference. For example, the CSD parameter 
            for the PROGDEF CREATE operation doesn't require a value.
        required: false
        type: str
    required: false
'''


EXAMPLES = r"""
- name: define a BUNDLE in a CSD
  cmci_create:
      cmci_host: 'winmvs2c.hursley.ibm.com'
      cmci_port: '10080'
      context: 'iyk3z0r9'
      type: 'CICSDefinitionBundle'
      attributes:
        name: PONGALT
        BUNDLEDIR: /u/ibmuser/bundle/pong/pongbundle_1.0.0
        csdgroup: JVMGRP
      parameters:
        - name: 'csd'
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
      https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/commands-cpsm/eyup2ky.html.
  returned: success
  type: str
cpsm_reason_code:
  description:
    - The numeric value of the REASON code returned by each CICSPlex SM API
      command. For a list of REASON numeric values, see
      https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/commands-cpsm/eyup2kw.html.
  returned: success
  type: int
cpsm_response:
  description:
    - The character value of the RESPONSE code returned by each CICSPlex SM API
      command. For a list of RESPONSE character values, see
      https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/commands-cpsm/eyup2kx.html.
  returned: success
  type: str
cpsm_response_code:
  description:
    - The numeric value of the RESPONSE code returned by each CICSPlex SM API
      command. For a list of RESPONSE numeric values, see
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
    AnsibleCMCIModule, parameters_argument, ATTRIBUTES_ARGUMENT
)
from typing import Optional, Dict
from collections import OrderedDict

CREATE_PARAMETERS = 'create_parameters'


class AnsibleCMCICreateModule(AnsibleCMCIModule):
    def __init__(self):
        # pylint: disable=super-with-arguments
        super(AnsibleCMCICreateModule, self).__init__('POST')

    def init_argument_spec(self):  # type: () -> Dict
        # pylint: disable=super-with-arguments
        argument_spec = super(AnsibleCMCICreateModule, self).init_argument_spec()
        argument_spec.update(parameters_argument(CREATE_PARAMETERS))
        argument_spec.update(ATTRIBUTES_ARGUMENT)
        return argument_spec

    def init_body(self):  # type: () -> Optional[OrderedDict]
        create = OrderedDict({})
        self.append_parameters(CREATE_PARAMETERS, create)
        self.append_attributes(create)

        return OrderedDict({
            'request': {
                'create': create
            }
        })


def main():
    AnsibleCMCICreateModule().main()


if __name__ == '__main__':
    main()
