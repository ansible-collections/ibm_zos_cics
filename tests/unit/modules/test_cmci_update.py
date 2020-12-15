# -*- coding: utf-8 -*-

# Copyright (c) IBM Corporation 2019, 2020
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.ibm.ibm_zos_cics.plugins.modules import cmci_update
from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.cmci_helper import (
    HOST, PORT, CONTEXT, SCOPE, od, body_matcher, cmci_module, CMCITestHelper
)


def test_update(cmci_module):  # type: (CMCITestHelper) -> None
    record = dict(
        changeagent='CSDAPI',
        changeagrel='0730',
        csdgroup='DUMMY',
        description='new description',
        name='DUMMY'
    )
    cmci_module.stub_records(
        'PUT',
        'cicsdefinitionprogram',
        [record],
        scope=SCOPE,
        parameters='?CRITERIA=NAME%3DDUMMY&PARAMETER=CSDGROUP%28DUMMY%29',
        additional_matcher=body_matcher(od(
            ('request', od(
                ('update', od(
                    ('parameter', od(
                        ('@name', 'CSD')
                    )),
                    ('attributes', od(
                        ('@description', 'new description')
                    ))
                ))
            ))
        ))
    )

    cmci_module.expect(result(
        'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/cicsdefinitionprogram'
        '/CICSEX56/IYCWEMW2?CRITERIA=NAME%3DDUMMY&PARAMETER=CSDGROUP%28DUMMY%29',
        record,
        '<request><update>'
        '<parameter name="CSD"></parameter>'
        '<attributes description="new description"></attributes>'
        '</update></request>'
    ))

    cmci_module.run(cmci_update, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': SCOPE,
        'security_type': 'none',
        'type': 'cicsdefinitionprogram',
        'parameters': [{
            'name': 'CSD'
        }],
        'attributes': {
            'description': 'new description'
        },
        'resources': {
            'criteria': 'NAME=DUMMY',
            'parameter': 'CSDGROUP(DUMMY)'
        }
    })


def result(url, record, body):
    return {
        'changed': True,
        'connect_version': '0560',
        'cpsm_reason': '',
        'cpsm_reason_code': 0,
        'cpsm_response': 'OK',
        'cpsm_response_code': 1024,
        'http_status': 'OK',
        'http_status_code': 200,
        'request': {
            'url': url,
            'method': 'PUT',
            'body': body
        },
        'records': [record],
        'record_count': 1
    }
