# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2020,2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.ibm.ibm_zos_cics.plugins.modules import cmci_get
from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.cmci_helper import (
    HOST, PORT, CONTEXT, SCOPE, CMCITestHelper, cmci_module, encode_html_parameter
)

import sys
from collections import OrderedDict

expected_type = 'class'
if sys.version_info.major <= 2:
    expected_type = 'type'


def test_query_criteria(cmci_module):  # type: (cmci_module) -> None
    records = [{'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'}]
    cmci_module.stub_records('GET', 'cicslocalfile', records, scope=SCOPE, parameters='?CRITERIA=%28FOO%3D%27BAR%27%29')

    cmci_module.expect(result(
        'https://example.com:12345/CICSSystemManagement/'
        'cicslocalfile/CICSEX56/IYCWEMW2?CRITERIA=%28FOO%3D%27BAR%27%29',
        records=records
    ))

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'filter': {
                'FOO': 'BAR'
            }
        }
    })


def test_filter_multi(cmci_module):  # type: (CMCITestHelper) -> None
    records = [{'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'}]
    filters = OrderedDict({})
    filters['GOO'] = 'LAR'
    filters['FOO'] = 'BAR'

    cmci_module.stub_records('GET', 'cicslocalfile', records, scope=SCOPE,
                             parameters='?CRITERIA=%28GOO%3D%27LAR%27%29%20AND%20%28FOO%3D%27BAR%27%29')

    cmci_module.expect(result(
        'https://example.com:12345/CICSSystemManagement/'
        'cicslocalfile/CICSEX56/IYCWEMW2?CRITERIA=%28GOO%3D%27LAR%27%29%20AND%20%28FOO%3D%27BAR%27%29',
        records=records
    ))

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'filter': filters
        }
    })


def test_complex_filter_and(cmci_module):  # type: (CMCITestHelper) -> None
    records = [{'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'}]
    cmci_module.stub_records('GET', 'cicslocalfile', records, scope=SCOPE,
                             parameters='?CRITERIA=%28FOO%3D%27BAR%27%29%20AND%20%28GOO%3D%27LAR%27%29')

    cmci_module.expect(result(
        'https://example.com:12345/CICSSystemManagement/'
        'cicslocalfile/CICSEX56/IYCWEMW2?CRITERIA=%28FOO%3D%27BAR%27%29%20AND%20%28GOO%3D%27LAR%27%29',
        records=records
    ))

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'and': [{
                    'attribute': 'FOO',
                    'operator': '=',
                    'value': 'BAR'
                }, {
                    'attribute': 'GOO',
                    'operator': '=',
                    'value': 'LAR'
                }]
            }
        }
    })


def test_complex_filter_or(cmci_module):  # type: (CMCITestHelper) -> None
    records = [{'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'}]
    cmci_module.stub_records('GET', 'cicslocalfile', records, scope=SCOPE,
                             parameters='?CRITERIA=%28FOO%3D%27BAR%27%29%20OR%20%28GOO%3D%27LAR%27%29')

    cmci_module.expect(result(
        'https://example.com:12345/CICSSystemManagement/'
        'cicslocalfile/CICSEX56/IYCWEMW2?CRITERIA=%28FOO%3D%27BAR%27%29%20OR%20%28GOO%3D%27LAR%27%29',
        records=records
    ))

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'or': [{
                    'attribute': 'FOO',
                    'operator': '=',
                    'value': 'BAR'
                }, {
                    'attribute': 'GOO',
                    'operator': '=',
                    'value': 'LAR'
                }]
            }
        }
    })


def test_complex_filter_operator(cmci_module):  # type: (CMCITestHelper) -> None
    records = [{'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'}]
    cmci_module.stub_records('GET', 'cicslocalfile', records, scope=SCOPE,
                             parameters='?CRITERIA=NOT%28FOO%3D%3D%27BAR%27%29')

    cmci_module.expect(result(
        'https://example.com:12345/CICSSystemManagement/'
        'cicslocalfile/CICSEX56/IYCWEMW2?CRITERIA=NOT%28FOO%3D%3D%27BAR%27%29',
        records=records
    ))

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'attribute': 'FOO',
                'operator': '!=',
                'value': 'BAR'
            }
        }
    })


def test_complex_filter_and_or(cmci_module):  # type: (CMCITestHelper) -> None
    records = [{'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'}]
    cmci_module.stub_records('GET', 'cicslocalfile', records, scope=SCOPE,
                             parameters='?CRITERIA=%28FOO%3D%27BAR%27%29%20AND%20%28BAT%3D%27BAZ%27%29%20AND%20%28'
                                        '%28BING%3D%271%27%29%20OR%20%28BING%3D%272%27%29%29')

    cmci_module.expect(result(
        'https://example.com:12345/CICSSystemManagement/'
        'cicslocalfile/CICSEX56/IYCWEMW2?CRITERIA=%28FOO%3D%27BAR%27%29%20AND%20%28BAT%3D%27BAZ%27%29%20AND%20%28'
        '%28BING%3D%271%27%29%20OR%20%28BING%3D%272%27%29%29',
        records=records
    ))

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'and': [{
                    'attribute': 'FOO',
                    'value': 'BAR'
                }, {
                    'attribute': 'BAT',
                    'value': 'BAZ'
                }, {
                    'or': [{
                        'attribute': 'BING',
                        'operator': '=',
                        'value': '1'
                    }, {
                        'attribute': 'BING',
                        'value': '2'
                    }]
                }]
            }
        }
    })


def test_complex_filter_and_and(cmci_module):  # type: (CMCITestHelper) -> None
    records = [{'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'}]
    cmci_module.stub_records('GET', 'cicslocalfile', records, scope=SCOPE,
                             parameters='?CRITERIA=%28FOO%3D%27BAR%27%29%20AND%20%28BAT%3D%3D%27BAZ%27%29%20AND%20%28'
                                        '%28BING%3D%271%27%29%20AND%20%28BING%3D%272%27%29%29')

    cmci_module.expect(result(
        'https://example.com:12345/CICSSystemManagement/'
        'cicslocalfile/CICSEX56/IYCWEMW2?CRITERIA=%28FOO%3D%27BAR%27%29%20AND%20%28BAT%3D%3D%27BAZ%27%29%20AND%20%28'
        '%28BING%3D%271%27%29%20AND%20%28BING%3D%272%27%29%29',
        records=records
    ))

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'and': [{
                    'attribute': 'FOO',
                    'value': 'BAR'
                }, {
                    'attribute': 'BAT',
                    'operator': '==',
                    'value': 'BAZ'
                }, {
                    'and': [{
                        'attribute': 'BING',
                        'value': '1'
                    }, {
                        'attribute': 'BING',
                        'value': '2'
                    }]
                }]
            }
        }
    })


def test_complex_filter_or_or(cmci_module):  # type: (CMCITestHelper) -> None
    records = [{'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'}]
    cmci_module.stub_records('GET', 'cicslocalfile', records, scope=SCOPE,
                             parameters='?CRITERIA=%28FOO%3E%3D%27BAR%27%29%20OR%20%28%28BING%3D%3D%271%27%29%20OR%20'
                                        '%28BING%3D%272%27%29%29')

    cmci_module.expect(result(
        'https://example.com:12345/CICSSystemManagement/'
        'cicslocalfile/CICSEX56/IYCWEMW2?CRITERIA=%28FOO%3E%3D%27BAR%27%29%20OR%20%28%28BING%3D%3D%271%27%29%20OR%20'
        '%28BING%3D%272%27%29%29',
        records=records
    ))

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'or': [{
                    'attribute': 'FOO',
                    'operator': '>=',
                    'value': 'BAR'
                }, {
                    'or': [{
                        'attribute': 'BING',
                        'operator': 'IS',
                        'value': '1'
                    }, {
                        'attribute': 'BING',
                        'operator': 'EQ',
                        'value': '2'
                    }]
                }]
            }
        }
    })


def test_complex_filter_invalid_and_or_combo(cmci_module):  # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': 'parameters are mutually exclusive: attribute|and|or found in resources -> complex_filter',
        'failed': True
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'and': [{
                    'attribute': 'FOO',
                    'operator': '=',
                    'value': 'BAR'
                }, {
                    'attribute': 'GOO',
                    'operator': '=',
                    'value': 'LAR'
                }],
                'or': [{
                    'attribute': 'FOO',
                    'operator': '=',
                    'value': 'BAR'
                }, {
                    'attribute': 'GOO',
                    'operator': '=',
                    'value': 'LAR'
                }]
            }
        }
    })


def test_query_criteria_complex_filter_root_no_value(cmci_module):
    cmci_module.expect({
        'msg': 'parameters are required together: attribute, value found in '
               'resources -> complex_filter',
        'failed': True
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'attribute': 'FOO'
            }
        }
    })


def test_query_criteria_complex_filter_or_no_value(cmci_module):
    cmci_module.expect({
        'msg': 'parameters are required together: attribute, value found in resources -> complex_filter -> or',
        'failed': True,
        'changed': False
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'or': [{
                    'attribute': 'FOO'
                }, {
                    'attribute': 'BAR',
                    'value': 'BOO'
                }]
            }
        }
    })


def test_query_criteria_complex_filter_and_no_value(cmci_module):
    cmci_module.expect({
        'msg': 'parameters are required together: attribute, value found in resources -> complex_filter -> and',
        'failed': True,
        'changed': False
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'and': [{
                    'attribute': 'FOO'
                }, {
                    'attribute': 'BAR',
                    'value': 'BOO'
                }]
            }
        }
    })


def test_complex_filter_operator_letters(cmci_module):  # type: (CMCITestHelper) -> None
    records = [{'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'}]
    cmci_module.stub_records('GET', 'cicslocalfile', records, scope=SCOPE, parameters='?CRITERIA=FOO%3E%27BAR%27')

    cmci_module.expect(result(
        'https://example.com:12345/CICSSystemManagement/'
        'cicslocalfile/CICSEX56/IYCWEMW2?CRITERIA=FOO%3E%27BAR%27',
        records=records
    ))

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'attribute': 'FOO',
                'operator': 'GT',
                'value': 'BAR'
            }
        }
    })


def test_complex_filter_invalid_and_attribute_root(cmci_module):  # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': 'parameters are mutually exclusive: attribute|and|or found in resources -> complex_filter',
        'failed': True
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'and': [{
                    'attribute': 'FOO',
                    'value': 'BAR'
                }, {
                    'attribute': 'BAT',
                    'operator': '==',
                    'value': 'BAZ'
                }],
                'attribute': 'FOO2',
                'value': 'BAR2'
            }
        }
    })


def test_complex_filter_invalid_and_attribute_and(cmci_module):  # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': 'parameters are mutually exclusive: attribute|and|or found in resources -> complex_filter -> and',
        'failed': True,
        'changed': False
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'and': [{
                    'attribute': 'FOO',
                    'value': 'BAR'
                }, {
                    'attribute': 'BAT',
                    'operator': '==',
                    'value': 'BAZ',
                    'and': [{
                        'attribute': 'FOO2',
                        'value': 'BAR2'
                    }]
                }]
            }
        }
    })


def test_complex_filter_invalid_and_attribute_or(cmci_module):  # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': 'parameters are mutually exclusive: attribute|and|or found in resources -> complex_filter',
        'failed': True
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'and': [{
                    'attribute': 'FOO',
                    'value': 'BAR'
                }, {
                    'attribute': 'BAT',
                    'operator': '==',
                    'value': 'BAZ'
                }],
                'attribute': 'FOO2',
                'value': 'BAR2'
            }
        }
    })


def test_complex_filter_default_operator_root(cmci_module):
    # type: (CMCITestHelper) -> None
    records = [{'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'}]
    cmci_module.stub_records('GET', 'cicslocalfile', records, scope=SCOPE,
                             parameters='?CRITERIA=FOO%3D%27BAR%27')

    cmci_module.expect(result(
        'https://example.com:12345/CICSSystemManagement/'
        'cicslocalfile/CICSEX56/IYCWEMW2?CRITERIA=FOO%3D%27BAR%27',
        records=records
    ))

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'attribute': 'FOO',
                'value': 'BAR'
            }
        }
    })


def test_required_by_root(cmci_module):
    # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': "missing parameter(s) required by 'operator': attribute found in resources -> complex_filter",
        'failed': True
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'and': [{
                    'attribute': 'FOO',
                    'value': 'BAR'
                }, {
                    'attribute': 'BAT',
                    'operator': '==',
                    'value': 'BAZ'
                }],
                'operator': '=='
            }
        }
    })


def test_required_by_and(cmci_module):
    # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': "missing parameter(s) required by 'operator': attribute",
        'changed': False,
        'failed': True
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'and': [{
                    'and': [{
                        'attribute': 'FOO',
                        'value': 'BAR'
                    }, {
                        'attribute': 'BAT',
                        'operator': '==',
                        'value': 'BAZ'
                    }],
                    'operator': '=='
                }]
            }
        }
    })


def test_required_by_or(cmci_module):
    # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': "missing parameter(s) required by 'operator': attribute",
        'changed': False,
        'failed': True
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'or': [{
                    'and': [{
                        'attribute': 'FOO',
                        'value': 'BAR'
                    }, {
                        'attribute': 'BAT',
                        'operator': '==',
                        'value': 'BAZ'
                    }],
                    'operator': '=='
                }]
            }
        }
    })


def test_extra_attributes_root(cmci_module):
    # type: (CMCITestHelper) -> None
    extension = "py"
    if sys.version_info.major <= 2:
        extension = "pyc"

    # Order that Ansible returns supported parameters is not consistent everytime
    # expect_list ensures expected and actual output are compared after sorting the
    # list first. This means passing tests if all expected attributes are listed, but not caring about
    # the order.
    before_list = "Unsupported parameters for (basic.%s) module: resources.complex_filter.orange. Supported parameters include: " % extension
    sorted_list_older_ansible = [
        "cmci_cert", "cmci_host", "cmci_key", "cmci_password",
        "cmci_port", "cmci_user", "context", "fail_on_nodata", "insecure",
        "record_count", "resources", "scheme", "scope", "timeout", "type"]
    sorted_list_newer_ansible = ["and", "attribute", "operator", "or", "value"]
    after_list = "."

    cmci_module.expect_list(
        chars_before_list=len(before_list),
        chars_after_list=len(after_list),
        string_containing_list='msg',
        expected_output_options=[{
            'msg': before_list + ", ".join(sorted_list_older_ansible) + after_list,
            'failed': True
        }, {
            'msg': before_list + ", ".join(sorted_list_newer_ansible) + after_list,
            'failed': True
        }]
    )
    cmci_module.expect({
        'failed': True
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'attribute': 'FOO',
                'value': 'BAR',
                'orange': 'red'
            }
        }
    })


def test_extra_attributes_and(cmci_module):
    # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': "Unsupported parameters for (basic.py) module: orange found in "
               "resources -> complex_filter -> and. Supported parameters "
               "include: and, attribute, operator, or, value",
        'failed': True,
        'changed': False
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'and': [{
                    "attribute": "foo",
                    "value": "bar",
                    "orange": "red"
                }]
            }
        }
    })


def test_extra_attributes_or(cmci_module):
    # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': "Unsupported parameters for (basic.py) module: orange found in "
               "resources -> complex_filter -> or. Supported parameters "
               "include: and, attribute, operator, or, value",
        'failed': True,
        'changed': False
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'or': [{
                    "attribute": "foo",
                    "value": "bar",
                    "orange": "red"
                }]
            }
        }
    })


def test_and_string_invalid(cmci_module):
    # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': "Elements value for option 'and' found in 'resources -> "
               "complex_filter' is of type <%s 'str'> and we were unable to "
               "convert to dict: dictionary requested, could not parse JSON or"
               " key=value" % expected_type,
        'failed': True
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'and': 'foo'
            }
        }
    })


def test_and_list_of_strings_invalid(cmci_module):
    # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': "Elements value for option 'and' found in 'resources -> "
               "complex_filter' is of type <%s 'str'> and we were unable to "
               "convert to dict: dictionary requested, could not parse JSON or "
               "key=value" % expected_type,
        'failed': True
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'and': [
                    'bar'
                ]
            }
        }
    })


def test_and_and_string_invalid(cmci_module):
    # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': "nested filters must be a list, was: <%s 'str'> found in "
               "resources -> complex_filter -> and -> and" % expected_type,
        'failed': True,
        'changed': False
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'and': [{
                    "and": "foo"
                }]
            }
        }
    })


def test_and_and_list_of_strings_invalid(cmci_module):
    # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': "nested filter must be of type dict, was: <%s 'str'> found "
               "in resources -> complex_filter -> and -> and" % expected_type,
        'failed': True,
        'changed': False
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'and': [{
                    "and": ["foo", "bar"]
                }]
            }
        }
    })


def test_and_or_string_invalid(cmci_module):
    # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': "nested filters must be a list, was: <%s 'str'> found in "
               "resources -> complex_filter -> and -> or" % expected_type,
        'failed': True,
        'changed': False
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'and': [{
                    "or": "foo"
                }]
            }
        }
    })


def test_and_or_list_of_strings_invalid(cmci_module):
    # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': "nested filter must be of type dict, was: <%s 'str'> found "
               "in resources -> complex_filter -> and -> or" % expected_type,
        'failed': True,
        'changed': False
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'and': [{
                    "or": ["foo", "bar"]
                }]
            }
        }
    })


def test_operator_choice_root(cmci_module):
    # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': 'value of operator must be one of: <, <=, =, >, >=, ¬=, ==, !=, '
               'EQ, NE, LT, LE, GE, GT, IS, got: banana found in resources -> '
               'complex_filter',
        'failed': True
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'attribute': 'FOO',
                'value': 'BAR',
                'operator': 'banana'
            }
        }
    })


def test_operator_choice_and(cmci_module):
    # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': 'value of operator must be one of: <, <=, =, >, >=, ¬=, ==, !=, '
               'EQ, NE, LT, LE, GE, GT, IS, got: banana found in resources -> '
               'complex_filter -> and',
        'failed': True,
        'changed': False
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'and': [{
                    'attribute': 'FOO',
                    'value': 'BAR',
                    'operator': 'banana'
                }]
            }
        }
    })


def test_operator_choice_or(cmci_module):
    # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': 'value of operator must be one of: <, <=, =, >, >=, ¬=, ==, !=, '
               'EQ, NE, LT, LE, GE, GT, IS, got: banana found in resources -> '
               'complex_filter -> or',
        'failed': True,
        'changed': False
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'or': [{
                    'attribute': 'FOO',
                    'value': 'BAR',
                    'operator': 'banana'
                }]
            }
        }
    })


def test_required_one_of_root(cmci_module):
    # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': 'one of the following is required: attribute, and, or found in '
               'resources -> complex_filter',
        'failed': True
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
            }
        }
    })


def test_required_one_of_and(cmci_module):
    # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': 'one of the following is required: attribute, and, or found in '
               'resources -> complex_filter -> and',
        'failed': True,
        'changed': False
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'and': [{}]
            }
        }
    })


def test_required_one_of_or(cmci_module):
    # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': 'one of the following is required: attribute, and, or found in '
               'resources -> complex_filter -> or',
        'failed': True,
        'changed': False
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'or': [{}]
            }
        }
    })


def test_attribute_type_and(cmci_module):
    # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': "attribute must be of type str, was: <%s 'int'> found in "
               "resources -> complex_filter -> and" % expected_type,
        'failed': True,
        'changed': False
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'and': [{
                    'attribute': 123,
                    'value': '456'
                }]
            }
        }
    })


def test_attribute_type_or(cmci_module):
    # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': "attribute must be of type str, was: <%s 'int'> found in "
               "resources -> complex_filter -> or" % expected_type,
        'failed': True,
        'changed': False
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'or': [{
                    'attribute': 123,
                    'value': '456'
                }]
            }
        }
    })


def test_value_type_and(cmci_module):
    # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': "value must be of type str, was: <%s 'int'> found in "
               "resources -> complex_filter -> and" % expected_type,
        'failed': True,
        'changed': False
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'and': [{
                    'attribute': '123',
                    'value': 456
                }]
            }
        }
    })


def test_value_type_or(cmci_module):
    # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': "value must be of type str, was: <%s 'int'> found in "
               "resources -> complex_filter -> or" % expected_type,
        'failed': True,
        'changed': False
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'or': [{
                    'attribute': '123',
                    'value': 456
                }]
            }
        }
    })


def test_value_no_attribute_root(cmci_module):
    # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': "parameters are required together: attribute, value found in "
               "resources -> complex_filter",
        'failed': True
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'value': '456a',
                'and': [{
                    'attribute': '123',
                    'value': '678a'
                }]
            }
        }
    })


def test_value_no_attribute_and(cmci_module):
    # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': "parameters are required together: attribute, value found in "
               "resources -> complex_filter -> and",
        'failed': True,
        'changed': False
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'and': [{
                    'value': '456',
                    'and': [{
                        'attribute': '123',
                        'value': '678'
                    }]
                }]
            }
        }
    })


def test_value_no_attribute_or(cmci_module):
    # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': "parameters are required together: attribute, value found in "
               "resources -> complex_filter -> or",
        'failed': True,
        'changed': False
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'or': [{
                    'value': '456',
                    'or': [{
                        'attribute': '123',
                        'value': '678'
                    }]
                }]
            }
        }
    })


def test_invalid_complex_filter_attribute(cmci_module):  # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': "Filter attribute with value Broken! was not valid. Valid characters are A-Z a-z 0-9.",
        'failed': True,
        'changed': False
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'and': [{
                    'attribute': 'Broken!',
                    'operator': '=',
                    'value': 'BAR'
                }, {
                    'attribute': 'GOO',
                    'operator': '=',
                    'value': 'LAR'
                }]
            }
        }
    })


def test_sanitise_complex_filter_value(cmci_module):  # type: (CMCITestHelper) -> None
    records = [{'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'}]

    encoded_criteria = encode_html_parameter({"CRITERIA": r"(FOO='++++++W+\') OR (jobname=\'*') AND (GOO='\'\'LAR\'\'')"})

    cmci_module.stub_records('GET', 'cicslocalfile', records, scope=SCOPE,
                             parameters=encoded_criteria)

    cmci_module.expect(result(
        'https://example.com:12345/CICSSystemManagement/'
        'cicslocalfile/CICSEX56/IYCWEMW2' + encoded_criteria,
        records=records
    ))

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'and': [{
                    'attribute': 'FOO',
                    'operator': '=',
                    'value': "++++++W+') OR (jobname='*"
                }, {
                    'attribute': 'GOO',
                    'operator': '=',
                    'value': "''LAR''"
                }]
            }
        }
    })


def result(url, records, http_status='OK', http_status_code=200):
    return {
        'changed': False,
        'connect_version': '0560',
        'cpsm_reason': '',
        'cpsm_reason_code': 0,
        'cpsm_response': 'OK',
        'cpsm_response_code': 1024,
        'http_status': http_status,
        'http_status_code': http_status_code,
        'record_count': len(records),
        'records': records,
        'request': {
            'url': url,
            'method': 'GET',
            'body': None
        }
    }
