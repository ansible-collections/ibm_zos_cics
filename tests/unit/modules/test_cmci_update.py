# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2020,2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.ibm.ibm_zos_cics.plugins.modules import cmci_update
from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.cmci_helper import (
    HOST, PORT, CONTEXT, SCOPE, od, body_matcher, cmci_module, CMCITestHelper
)


def test_csd_update(cmci_module):  # type: (cmci_module) -> None
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
        parameters='?CRITERIA=%28NAME%3D%27DUMMY%27%29&PARAMETER=CSDGROUP%28DUMMY%29',
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
        'https://example.com:12345/CICSSystemManagement/cicsdefinitionprogram'
        '/CICSEX56/IYCWEMW2?CRITERIA=%28NAME%3D%27DUMMY%27%29&PARAMETER=CSDGROUP%28DUMMY%29',
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
        'type': 'cicsdefinitionprogram',
        'update_parameters': [{
            'name': 'CSD'
        }],
        'attributes': {
            'description': 'new description'
        },
        'resources': {
            'filter': {
                'NAME': 'DUMMY'
            },
            'get_parameters': [{'name': 'CSDGROUP', 'value': 'DUMMY'}]
        }
    })


def test_bas_update(cmci_module):  # type: (CMCITestHelper) -> None
    record = dict(
        changeagent='CSDAPI',
        changeagrel='0730',
        description='new description',
        resdesc='BASICB1'
    )
    cmci_module.stub_records(
        'PUT',
        'cicsresourcedefinition',
        [record],
        scope=SCOPE,
        parameters='?CRITERIA=%28RESDESC%3D%27BASICB1%27%29',
        additional_matcher=body_matcher(od(
            ('request', od(
                ('update', od(
                    ('attributes', od(
                        ('@description', 'new description')
                    ))
                ))
            ))
        ))
    )

    cmci_module.expect(result(
        'https://example.com:12345/CICSSystemManagement/cicsresourcedefinition'
        '/CICSEX56/IYCWEMW2?CRITERIA=%28RESDESC%3D%27BASICB1%27%29',
        record,
        '<request><update>'
        '<attributes description="new description"></attributes>'
        '</update></request>'
    ))

    cmci_module.run(cmci_update, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': SCOPE,
        'type': 'cicsresourcedefinition',
        'attributes': {
            'description': 'new description'
        },
        'resources': {
            'filter': {
                'RESDESC': 'BASICB1'
            }
        }
    })


def test_resource_update(cmci_module):  # type: (CMCITestHelper) -> None
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
        parameters='?CRITERIA=%28NAME%3D%27DUMMY%27%29%20AND%20%28DEFVER%3D%271%27%29',
        additional_matcher=body_matcher(od(
            ('request', od(
                ('update', od(
                    ('attributes', od(
                        ('@description', 'new description')
                    ))
                ))
            ))
        ))
    )

    cmci_module.expect(result(
        'https://example.com:12345/CICSSystemManagement/cicsdefinitionprogram'
        '/CICSEX56/IYCWEMW2?CRITERIA=%28NAME%3D%27DUMMY%27%29%20AND%20%28DEFVER%3D%271%27%29',
        record,
        '<request><update>'
        '<attributes description="new description"></attributes>'
        '</update></request>'
    ))

    cmci_module.run(cmci_update, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': SCOPE,
        'type': 'cicsdefinitionprogram',
        'attributes': {
            'description': 'new description'
        },
        'resources': {
            'filter': {
                'NAME': 'DUMMY',
                'DEFVER': '1'
            },
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
