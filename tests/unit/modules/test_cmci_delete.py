# -*- coding: utf-8 -*-

# Copyright (c) IBM Corporation 2020
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.ibm.ibm_zos_cics.plugins.modules import cmci_delete
from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.cmci_helper import (
    HOST, PORT, CONTEXT, cmci_module, CMCITestHelper
)


def test_delete_context(cmci_module):  # type: (CMCITestHelper) -> None
    cmci_module.stub_delete('cicsdefinitionbundle', 1)

    cmci_module.expect(
        result(
            'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/cicsdefinitionbundle/CICSEX56/',
            1
        )
    )

    cmci_module.run(cmci_delete, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'type': 'cicsdefinitionbundle'
    })


def test_delete_context_scope(cmci_module):  # type: (CMCITestHelper) -> None
    cmci_module.stub_delete('cicsdefinitionbundle', 1, scope='IYCWEMW2')

    cmci_module.expect(
        result(
            'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/cicsdefinitionbundle/CICSEX56/IYCWEMW2',
            1
        )
    )

    cmci_module.run(cmci_delete, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicsdefinitionbundle'
    })


def test_delete_criteria(cmci_module):  # type: (CMCITestHelper) -> None
    cmci_module.stub_delete('cicsdefinitionbundle', 1, parameters='?CRITERIA=%28FOO%3D%27BAR%27%29')

    cmci_module.expect(
        result(
            'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/'
            'cicsdefinitionbundle/CICSEX56/?CRITERIA=%28FOO%3D%27BAR%27%29',
            1
        )
    )

    cmci_module.run(cmci_delete, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'type': 'cicsdefinitionbundle',
        'resources': {
            'filter': {
                'FOO': 'BAR'
            }
        }
    })


def test_delete_parameter(cmci_module):  # type: (CMCITestHelper) -> None
    cmci_module.stub_delete('cicsdefinitionbundle', 1, parameters='?PARAMETER=CSDGROUP%28%2A%29')

    cmci_module.expect(
        result(
            'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/'
            'cicsdefinitionbundle/CICSEX56/?PARAMETER=CSDGROUP%28%2A%29',
            1
        )
    )

    cmci_module.run(cmci_delete, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'type': 'cicsdefinitionbundle',
        'resources': {
            'parameters': [{'name': 'CSDGROUP', 'value': '*'}]
        }
    })


def test_delete_criteria_parameter(cmci_module):  # type: (CMCITestHelper) -> None
    cmci_module.stub_delete(
        'cicsdefinitionbundle',
        1,
        parameters='?CRITERIA=%28FOO%3D%27BAR%27%29&PARAMETER=CSDGROUP%28%2A%29'
    )

    cmci_module.expect(
        result(
            'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/'
            'cicsdefinitionbundle/CICSEX56/?CRITERIA=%28FOO%3D%27BAR%27%29&PARAMETER=CSDGROUP%28%2A%29',
            1
        )
    )

    cmci_module.run(cmci_delete, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'type': 'cicsdefinitionbundle',
        'resources': {
            'filter': {
                'FOO': 'BAR'
            },
            'parameters': [{'name': 'CSDGROUP', 'value': '*'}]
        }
    })


def result(url, success_count):
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
        'request': {
            'url': url,
            'method': 'DELETE',
            'body': None
        },
        'success_count': success_count
    }
