# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2020,2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import absolute_import, division, print_function
from collections import OrderedDict

__metaclass__ = type

from ansible_collections.ibm.ibm_zos_cics.plugins.modules import cmci_create
from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.cmci_helper import (
    HOST, PORT, CONTEXT, od, body_matcher, cmci_module, CMCITestHelper
)


def test_csd_create(cmci_module):  # type: (cmci_module) -> None
    record = OrderedDict({})
    record['csdgroup'] = 'bat'
    record['name'] = 'bar'
    record['bundledir'] = '/u/bundles/bloop'

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
                        ('@csdgroup', 'bat'),
                        ('@name', 'bar'),
                        ('@bundledir', '/u/bundles/bloop')
                    ))
                ))
            ))
        ))
    )

    cmci_module.expect(
        result(
            'https://example.com:12345/CICSSystemManagement/'
            'cicsdefinitionbundle/CICSEX56/IYCWEMW2',
            record,
            '<request><create>'
            '<parameter name="CSD"></parameter>'
            '<attributes csdgroup="bat" name="bar" bundledir="/u/bundles/bloop"></attributes>'
            '</create></request>'
        )
    )

    cmci_module.run(cmci_create, dict(
        cmci_host=HOST,
        cmci_port=PORT,
        context=CONTEXT,
        scope='IYCWEMW2',
        type='cicsdefinitionbundle',
        create_parameters=[dict(
            name='CSD'
        )],
        attributes=record
    ))


def test_bas_create(cmci_module):  # type: (CMCITestHelper) -> None
    record = OrderedDict({})
    record['AUTOINST'] = 'NO'
    record['RGSCOPE'] = 'BAS1'
    record['RESDESC'] = 'BASICB11'

    cmci_module.stub_records(
        'POST',
        'cicsdefinitionbundle',
        [record],
        scope='IYCWEMW2',
        additional_matcher=body_matcher(od(
            ('request', od(
                ('create', od(
                    ('parameter', od(
                        ('@name', 'BAS')
                    )),
                    ('attributes', od(
                        ('@AUTOINST', 'NO'),
                        ('@RGSCOPE', 'BAS1'),
                        ('@RESDESC', 'BASICB11')
                    ))
                ))
            ))
        ))
    )

    cmci_module.expect(
        result(
            'https://example.com:12345/CICSSystemManagement/'
            'cicsdefinitionbundle/CICSEX56/IYCWEMW2',
            record,
            '<request><create>'
            '<parameter name="BAS"></parameter>'
            '<attributes AUTOINST="NO" RGSCOPE="BAS1" RESDESC="BASICB11"></attributes>'
            '</create></request>'
        )
    )

    cmci_module.run(cmci_create, dict(
        cmci_host=HOST,
        cmci_port=PORT,
        context=CONTEXT,
        scope='IYCWEMW2',
        type='cicsdefinitionbundle',
        create_parameters=[dict(
            name='BAS'
        )],
        attributes=record
    ))


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
        'record_count': 1,
        'records': [record],
        'request': {
            'url': url,
            'method': 'POST',
            'body': body
        },
    }
