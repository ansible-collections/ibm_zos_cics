# -*- coding: utf-8 -*-

# Copyright (c) IBM Corporation 2019, 2020
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.ibm.ibm_zos_cics.plugins.modules import cmci_install
from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.cmci_helper import (
    HOST, PORT, CONTEXT, SCOPE, od, create_records_response, body_matcher, cmci_module, CMCITestHelper
)


def test_csd_install(cmci_module):  # type: (CMCITestHelper) -> None
    record = dict(
        name='bar',
        bundledir='/u/bundles/bloop',
        csdgroup='bat'
    )
    cmci_module.stub_records(
        'PUT',
        'cicsdefinitionbundle',
        records=[record],
        scope='IYCWEMW2',
        parameters='?PARAMETER=CSDGROUP%28%2A%29',
        additional_matcher=body_matcher(od(
            ('request', od(
                ('action', od(
                    ('@name', 'CSDINSTALL')
                ))
            ))
        ))
    )

    cmci_module.expect(result(
        'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/'
        'cicsdefinitionbundle/CICSEX56/IYCWEMW2?PARAMETER=CSDGROUP%28%2A%29',
        record,
        '<request><action name="CSDINSTALL"></action></request>'
    ))

    cmci_module.run(cmci_install, dict(
        cmci_host=HOST,
        cmci_port=PORT,
        context=CONTEXT,
        scope='IYCWEMW2',
        type='cicsdefinitionbundle',
        location='CSD',
        parameter='CSDGROUP(*)'
    ))


def test_bas_install(cmci_module):  # type: (CMCITestHelper) -> None
    record = dict(
        name='bar',
        bundledir='/u/bundles/bloop',
        csdgroup='bat'
    )
    cmci_module.stub_records(
        'PUT',
        'cicsdefinitionbundle',
        [record],
        additional_matcher=body_matcher(od(
            ('request', od(
                ('action', od(
                    ('@name', 'INSTALL')
                ))
            ))
        ))
    )

    cmci_module.expect(result(
        'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/cicsdefinitionbundle/CICSEX56/',
        record,
        '<request><action name="INSTALL"></action></request>'
    ))

    cmci_module.run(cmci_install, dict(
        cmci_host=HOST,
        cmci_port=PORT,
        context=CONTEXT,
        type='cicsdefinitionbundle',
        location='BAS'
    ))


def test_install_csd_criteria_parameter(cmci_module):  # type: (CMCITestHelper) -> None
    record = dict(
        changeagent='CSDAPI',
        changeagrel='0730',
        csdgroup='DUMMY',
        name='DUMMY'
    )
    cmci_module.stub_records(
        'PUT',
        'cicsdefinitionprogram',
        [record],
        scope=SCOPE,
        parameters='?CRITERIA=%28%28NAME%3DDUMMY%29+AND+%28DEFVER%3D0%29+AND+'
                   '%28CSDGROUP%3DDUMMY%29%29&PARAMETER=CSDGROUP%28DUMMY%29',
        additional_matcher=body_matcher(od(
            ('request', od(
                ('action', od(
                    ('@name', 'CSDINSTALL')
                ))
            ))
        ))
    )

    cmci_module.expect(result(
        'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/cicsdefinitionprogram/'
        'CICSEX56/IYCWEMW2?CRITERIA=%28%28NAME%3DDUMMY%29%20AND%20%28DEFVER%3D0%29%20AND'
        '%20%28CSDGROUP%3DDUMMY%29%29&PARAMETER=CSDGROUP%28DUMMY%29',
        record,
        '<request><action name="CSDINSTALL"></action></request>'
    ))

    cmci_module.run(cmci_install, dict(
        cmci_host=HOST,
        cmci_port=PORT,
        context=CONTEXT,
        scope=SCOPE,
        security_type='none',
        type='cicsdefinitionprogram',
        location='CSD',
        criteria="((NAME=DUMMY) AND (DEFVER=0) AND (CSDGROUP=DUMMY))",
        parameter='CSDGROUP(DUMMY)'
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
        'request': {
            'url': url,
            'method': 'PUT',
            'body': body
        },
        'records': [record],
        'record_count': 1
    }
