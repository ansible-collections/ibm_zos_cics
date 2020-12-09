# -*- coding: utf-8 -*-

# Copyright (c) IBM Corporation 2019, 2020
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.ibm.ibm_zos_cics.plugins.modules import cmci_create
from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.cmci_helper import (
    HOST, PORT, CONTEXT, od, create_records_response, body_matcher, cmci_module, CMCITestHelper
)


def test_csd_create(cmci_module):  # type: (CMCITestHelper) -> None
    record = dict(
        name='bar',
        bundledir='/u/bundles/bloop',
        csdgroup='bat'
    )
    cmci_module.stub_records(
        'POST',
        'cicsdefinitionbundle',
        [record],
        scope='IYCWEMW2',
        additional_matcher=body_matcher(od(
            ('request', od(
                ('create', od(
                    ('parameter', od(
                        ('@name', 'CSD')
                    )),
                    ('attributes', od(
                        ('@name', 'bar'),
                        ('@bundledir', '/u/bundles/bloop'),
                        ('@csdgroup', 'bat')
                    ))
                ))
            ))
        ))
    )

    cmci_module.expect({
        'changed': True,
        'request': {
            'url': 'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/'
                   'cicsdefinitionbundle/CICSEX56/IYCWEMW2',
            'method': 'POST',
            'body': '<request><create>'
                    '<parameter name="CSD"></parameter>'
                    '<attributes name="bar" bundledir="/u/bundles/bloop" csdgroup="bat"></attributes>'
                    '</create></request>'
        },
        'response': {
            'body': create_records_response(
                'cicsdefinitionbundle', [record]
            ),
            'reason': 'OK',
            'status_code': 200,
        }
    })

    cmci_module.run(cmci_create, dict(
        cmci_host=HOST,
        cmci_port=PORT,
        context=CONTEXT,
        scope='IYCWEMW2',
        resource=dict(
            type='cicsdefinitionbundle',
            parameters=[dict(
                name='CSD'
            )],
            attributes=record
        )
    ))
