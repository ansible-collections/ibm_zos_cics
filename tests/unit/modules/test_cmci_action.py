# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2020,2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from collections import OrderedDict

from ansible_collections.ibm.ibm_zos_cics.plugins.modules import cmci_action
from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.cmci_helper import (
    HOST, PORT, CONTEXT, SCOPE, od, body_matcher, cmci_module, CMCITestHelper
)


def test_csd_install(cmci_module):  # type: (cmci_module) -> None
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

    cmci_module.expect(ok_result(
        'https://example.com:12345/CICSSystemManagement/'
        'cicsdefinitionbundle/CICSEX56/IYCWEMW2?PARAMETER=CSDGROUP%28%2A%29',
        record,
        '<request><action name="CSDINSTALL"></action></request>'
    ))

    cmci_module.run(cmci_action, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicsdefinitionbundle',
        'action_name': 'CSDINSTALL',
        'resources': {
            'get_parameters': [{'name': 'CSDGROUP', 'value': '*'}]
        }
    })


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

    cmci_module.expect(ok_result(
        'https://example.com:12345/CICSSystemManagement/cicsdefinitionbundle/CICSEX56/',
        record,
        '<request><action name="INSTALL"></action></request>'
    ))

    cmci_module.run(cmci_action, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'type': 'cicsdefinitionbundle',
        'action_name': 'INSTALL'
    })


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
        parameters='?CRITERIA=%28NAME%3D%27DUMMY%27%29%20AND%20%28DEFVER%3D%270%27%29%20AND'
                   '%20%28CSDGROUP%3D%27DUMMY%27%29&PARAMETER=CSDGROUP%28DUMMY%29',

        additional_matcher=body_matcher(od(
            ('request', od(
                ('action', od(
                    ('@name', 'CSDINSTALL')
                ))
            ))
        ))
    )

    cmci_module.expect(ok_result(
        'https://example.com:12345/CICSSystemManagement/cicsdefinitionprogram/'
        'CICSEX56/IYCWEMW2?CRITERIA=%28NAME%3D%27DUMMY%27%29%20AND%20%28DEFVER%3D%270%27%29%20AND'
        '%20%28CSDGROUP%3D%27DUMMY%27%29&PARAMETER=CSDGROUP%28DUMMY%29',
        record,
        '<request><action name="CSDINSTALL"></action></request>'
    ))
    cmci_module.run(cmci_action, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': SCOPE,
        'type': 'cicsdefinitionprogram',
        'action_name': 'CSDINSTALL',
        'resources': {
            'complex_filter': {
                'and': [
                    {
                        'attribute': 'NAME',
                        'value': 'DUMMY'
                    }, {
                        'attribute': 'DEFVER',
                        'value': '0'
                    }, {
                        'attribute': 'CSDGROUP',
                        'value': 'DUMMY'
                    }
                ]
            },
            'get_parameters': [{'name': 'CSDGROUP', 'value': 'DUMMY'}]
        }
    })


def test_bas_install_params(cmci_module):  # type: (CMCITestHelper) -> None
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
                    ('@name', 'INSTALL'),
                    ('parameter', [
                        od(
                            ('@name', 'FORCEINS'),
                            ('@value', 'NO')
                        ),
                        od(
                            ('@name', 'USAGE'),
                            ('@value', 'LOCAL')
                        )
                    ])
                ))
            ))
        ))
    )

    cmci_module.expect(ok_result(
        'https://example.com:12345/CICSSystemManagement/cicsdefinitionbundle/CICSEX56/',
        record,
        '<request><action name="INSTALL">'
        '<parameter name="FORCEINS" value="NO"></parameter>'
        '<parameter name="USAGE" value="LOCAL"></parameter>'
        '</action></request>'
    ))

    cmci_module.run(cmci_action, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'type': 'cicsdefinitionbundle',
        'action_name': 'INSTALL',
        'action_parameters': [
            {'name': 'FORCEINS', 'value': 'NO'},
            {'name': 'USAGE', 'value': 'LOCAL'}
        ]
    })


def test_bas_install_error_detailed_feedback(cmci_module):
    feedback = [
        {
            'action': 'INSTALL',
            'installerror': [od(
                ('eibfn', '3042'),
                ('eibfn_alt', 'CREATE ATOMSERVICE'),
                ('eyu_cicsname', 'IYCWEMI1'),
                ('resp', '16'),
                ('resp_alt', 'INVREQ'),
                ('resp2', '627'),
                ('errorcode', '4'),
                ('resourcename', 'ASD2')
            ), od(
                ('eibfn', '3042'),
                ('eibfn_alt', 'CREATE ATOMSERVICE'),
                ('eyu_cicsname', 'IYCWEMJ1'),
                ('resp', '16'),
                ('resp_alt', 'INVREQ'),
                ('resp2', '627'),
                ('errorcode', '4'),
                ('resourcename', 'ASD2')
            )]
        },
        {'keydata': 'C2C1E2C9C3C2F140', 'errorcode': '29', 'attribute1': 'RESDESC'},
    ]

    cmci_module.stub_non_ok_records(
        'PUT',
        'cicsresourcedescription',
        feedback,
        scope=SCOPE,
        parameters="?CRITERIA=%28RESDESC%3D%27BASICB1%27%29",
        additional_matcher=body_matcher(od(
            ('request', od(
                ('action', od(
                    ('@name', 'INSTALL')
                ))
            ))
        ))
    )

    cmci_module.expect(fail_result(
        'https://example.com:12345/CICSSystemManagement/cicsresourcedescription/'
        'CICSEX56/IYCWEMW2?CRITERIA=%28RESDESC%3D%27BASICB1%27%29',
        '<request><action name="INSTALL">'
        '</action></request>',
        feedback,
        'TABLEERROR',
        1038,
        'DATAERROR',
        1361,
        'CMCI request failed with response "TABLEERROR" reason "DATAERROR"'
    ))

    cmci_module.run(cmci_action, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': SCOPE,
        'type': 'cicsresourcedescription',
        'action_name': 'INSTALL',
        'resources': {
            'filter': {
                'RESDESC': 'BASICB1'
            }
        }
    })


def test_bas_install_non_ok_feedback_all_types(cmci_module):
    # Testing that when each error type is de-serialised it comes out as a list
    feedback = [
        od(
            ('action', 'INSTALL'),
            ('inconsistentscope', [od(
                ('eibfn', '3042'),
                ('eibfn_alt', 'CREATE ATOMSERVICE'),
                ('eyu_cicsname', 'IYCWEMI1'),
                ('resp', '16'),
                ('resp_alt', 'INVREQ'),
                ('resp2', '627'),
                ('errorcode', '4'),
                ('resourcename', 'ASD2')
            )]),
            ('installerror', [od(
                ('eibfn', '3042'),
                ('eibfn_alt', 'CREATE ATOMSERVICE'),
                ('eyu_cicsname', 'IYCWEMI1'),
                ('resp', '16'),
                ('resp_alt', 'INVREQ'),
                ('resp2', '627'),
                ('errorcode', '4'),
                ('resourcename', 'ASD2')
            )]),
            ('inconsistentset', [od(
                ('eibfn', '3042'),
                ('eibfn_alt', 'CREATE ATOMSERVICE'),
                ('eyu_cicsname', 'IYCWEMI1'),
                ('resp', '16'),
                ('resp_alt', 'INVREQ'),
                ('resp2', '627'),
                ('errorcode', '4'),
                ('resourcename', 'ASD2')
            )])
        )
    ]

    cmci_module.stub_non_ok_records(
        'PUT',
        'cicsresourcedescription',
        feedback,
        scope=SCOPE,
        parameters="?CRITERIA=%28RESDESC%3D%27BASICB1%27%29",
        additional_matcher=body_matcher(od(
            ('request', od(
                ('action', od(
                    ('@name', 'INSTALL')
                ))
            ))
        ))
    )

    cmci_module.expect(fail_result(
        'https://example.com:12345/CICSSystemManagement/cicsresourcedescription/'
        'CICSEX56/IYCWEMW2?CRITERIA=%28RESDESC%3D%27BASICB1%27%29',
        '<request><action name="INSTALL">'
        '</action></request>',
        feedback,
        'TABLEERROR',
        1038,
        'DATAERROR',
        1361,
        'CMCI request failed with response "TABLEERROR" reason "DATAERROR"'
    ))

    cmci_module.run(cmci_action, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': SCOPE,
        'type': 'cicsresourcedescription',
        'action_name': 'INSTALL',
        'resources': {
            'filter': {
                'RESDESC': 'BASICB1'
            }
        }
    })


def test_bas_install_error_detailed_feedback(cmci_module):
    feedback = [
        {'keydata': 'C2C1E2C9C3C2F140', 'errorcode': '29', 'attribute1': 'RESDESC'},
    ]

    cmci_module.stub_non_ok_records(
        'PUT',
        'cicsresourcedescription',
        feedback,
        scope=SCOPE,
        parameters="?CRITERIA=%28RESDESC%3D%27BASICB1%27%29",
        additional_matcher=body_matcher(od(
            ('request', od(
                ('action', od(
                    ('@name', 'INSTALL')
                ))
            ))
        ))
    )

    cmci_module.expect(fail_result(
        'https://example.com:12345/CICSSystemManagement/cicsresourcedescription/'
        'CICSEX56/IYCWEMW2?CRITERIA=%28RESDESC%3D%27BASICB1%27%29',
        '<request><action name="INSTALL">'
        '</action></request>',
        feedback,
        'TABLEERROR',
        1038,
        'DATAERROR',
        1361,
        'CMCI request failed with response "TABLEERROR" reason "DATAERROR"'
    ))

    cmci_module.run(cmci_action, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': SCOPE,
        'type': 'cicsresourcedescription',
        'action_name': 'INSTALL',
        'resources': {
            'filter': {
                'RESDESC': 'BASICB1'
            }
        }
    })


def od(*args):
    return OrderedDict(args)


def fail_result(url, body, feedback, cpsm_response, cpsm_response_code, cpsm_reason, cpsm_reason_code, msg):
    return {
        'msg': msg,
        'failed': True,
        'changed': False,
        'connect_version': '0560',
        'cpsm_reason': cpsm_reason,
        'cpsm_reason_code': cpsm_reason_code,
        'cpsm_response': cpsm_response,
        'cpsm_response_code': cpsm_response_code,
        'http_status': 'OK',
        'http_status_code': 200,
        'request': {
            'url': url,
            'method': 'PUT',
            'body': body
        },
        'feedback': feedback,
        'record_count': 1
    }


def ok_result(url, record, body):
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
