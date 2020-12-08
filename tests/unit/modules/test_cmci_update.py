# -*- coding: utf-8 -*-

# Copyright (c) IBM Corporation 2019, 2020
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.ibm.ibm_zos_cics.plugins.modules import cmci_update
from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.cmci_helper import (
    HOST, PORT, CONTEXT, SCOPE, od, create_records_response, body_matcher, cmci_module
)


def test_update(cmci_module):
    cmci_module.stub_update_record(
        'cicsdefinitionprogram',
        dict(
            changeagent='CSDAPI',
            changeagrel='0730',
            csdgroup='DUMMY',
            description='new description',
            name='DUMMY'
        ),
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

    cmci_module.expect({
        'changed': True,
        'request': {
            'body':
                '<request><update>'
                '<parameter name="CSD"></parameter>'
                '<attributes description="new description"></attributes>'
                '</update></request>',
            'method': 'PUT',
            'url': 'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/cicsdefinitionprogram/CICSEX56/IYCWEMW2',
            'params': {
                'PARAMETER': 'CSDGROUP(DUMMY)',
                'CRITERIA': 'NAME=DUMMY'
            }
        },
        'response': {
            'body': create_records_response(
                'cicsdefinitionprogram',
                [
                    od(
                        ('@changeagent', 'CSDAPI'),
                        ('@changeagrel', '0730'),
                        ('@csdgroup', 'DUMMY'),
                        ('@description', 'new description'),
                        ('@name', 'DUMMY')
                    )
                ]
            ),
            'reason': 'OK',
            'status_code': 200}
    })

    cmci_module.run(cmci_update, dict(
        cmci_host=HOST,
        cmci_port=PORT,
        context=CONTEXT,
        scope=SCOPE,
        security_type='none',
        resource=dict(
            type='cicsdefinitionprogram',
            parameters=[dict(
                name='CSD'
            )],
            attributes=dict(
                description='new description'
            )
        ),
        criteria='NAME=DUMMY',
        parameter='CSDGROUP(DUMMY)'
    ))
