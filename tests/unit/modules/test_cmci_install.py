# -*- coding: utf-8 -*-

# Copyright (c) IBM Corporation 2019, 2020
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.ibm.ibm_zos_cics.plugins.modules import cmci_install
from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.cmci_helper import (
    HOST, PORT, CONTEXT, od, create_records_response, body_matcher, cmci_module
)


def test_csd_install(cmci_module):
    cmci_module.stub_cmci(
        'PUT',
        'cicsdefinitionbundle',
        records=[dict(
            name='bar',
            bundledir='/u/bundles/bloop',
            csdgroup='bat'
        )],
        scope='IYCWEMW2',
        additional_matcher=body_matcher(od(
            ('request', od(
                ('action', od(
                    ('@name', 'CSDINSTALL')
                ))
            ))
        ))
    )

    cmci_module.expect({
        'changed': True,
        'request': {
            'url': 'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/'
                   'cicsdefinitionbundle/CICSEX56/IYCWEMW2',
            'method': 'PUT',
            'body': '<request><action name="CSDINSTALL"></action></request>'
        },
        'response': {
            # TODO: check install response
            'body': create_records_response(
                'cicsdefinitionbundle',
                [
                    od(
                        ('@name', 'bar'),
                        ('@bundledir', '/u/bundles/bloop'),
                        ('@csdgroup', 'bat')
                    )
                ]
            ),
            'reason': 'OK',
            'status_code': 200,
        }
    })

    cmci_module.run(cmci_install, dict(
        cmci_host=HOST,
        cmci_port=PORT,
        context=CONTEXT,
        scope='IYCWEMW2',
        resource=dict(
            type='cicsdefinitionbundle',
            location='CSD'
        )
    ))


def test_bas_install(cmci_module):
    cmci_module.stub_cmci(
        'PUT',
        'cicsdefinitionbundle',
        records=[dict(
            name='bar',
            bundledir='/u/bundles/bloop',
            csdgroup='bat'
        )],
        additional_matcher=body_matcher(od(
            ('request', od(
                ('action', od(
                    ('@name', 'INSTALL')
                ))
            ))
        ))
    )

    cmci_module.expect({
        'changed': True,
        'request': {
            'url': 'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/'
                   'cicsdefinitionbundle/CICSEX56/',
            'method': 'PUT',
            'body': '<request><action name="INSTALL"></action></request>'
        },
        'response': {
            # TODO: check install response
            'body': create_records_response(
                'cicsdefinitionbundle',
                [
                    od(
                        ('@name', 'bar'),
                        ('@bundledir', '/u/bundles/bloop'),
                        ('@csdgroup', 'bat')
                    )
                ]
            ),
            'reason': 'OK',
            'status_code': 200,
        }
    })

    cmci_module.run(cmci_install, dict(
        cmci_host=HOST,
        cmci_port=PORT,
        context=CONTEXT,
        resource=dict(
            type='cicsdefinitionbundle',
            location='BAS'
        )
    ))
