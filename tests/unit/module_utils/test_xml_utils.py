# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2025
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from collections import OrderedDict
from xml.etree.ElementTree import ParseError

import pytest
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils._xml_utils import (
    parse_xml, unparse_xml)


def get_test_xml_data():
    return '''<response xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://www.ibm.com/xmlns/prod/CICS/smw2int http://example.com/CICSSystemManagement/schema/CICSSystemManagement.xsd"
version="3.0" connect_version="0610">
<resultsummary api_response1="1024" api_response2="0" api_response1_alt="OK" api_response2_alt="" recordcount="2" displayed_recordcount="2"/>
<records>
<cicslocalfile _keydata="BLAH" accessmethod="VSAM" add="ADDABLE" addcnt="0" basdefinever="0" basedsname="DFHCSD" blockformat="BLOCKED"
blockkeyln="N/A" blocksize="N/A" browse="BROWSABLE" browsecnt="4321" browupdcnt="0" changeagent="SYSTEM" changeagrel="0740"
changetime="2025-12-31T00:00:00.000000+00:00" changeusrid="CICSUSER" datasettype="K" definesource="SYSTEM" definetime="2025-12-15T02:10:58.000000+00:00"
delete="DELETABLE" dexcpcnt="0" disposition="SHARE" dsname="DFHCSD" emptystatus="NOEMPTYREQ" enablestatus="UNENABLED" exclusive="NOTAPPLIC"
eyu_cicsname="APPL1" eyu_cicsrel="E740" eyu_reserved="0" file="DFHCSD" fwdrecstatus="NOTFWDRCVBLE" getcnt="221" getupdcnt="0"
gmtfilecls="0000-00-00T00:00:00.000000+00:00" gmtfileopn="0000-00-00T00:00:00.000000+00:00" iexcpcnt="0" installagent="SYSTEM"
installtime="2025-12-15T02:10:58.000000+00:00" installusrid="CICSUSER" journalnum="0" keylength="0" keyposition="0" locdelcnt="0" lsrpoolid="1"
numactstring="0" numdatbuff="0" numindexbuff="0" numstringwt="0" object="BASE" openstatus="CLOSED" rbatype="NOTAPPLIC" read="READABLE" readinteg="NOTAPPLIC"
recordformat="VARIABLE" recordsize="0" recovstatus="NOTRECOVABLE" reltype="NOTAPPLIC" rlsaccess="NOTRLS" rlsreqwtto="0" strings="6" timeclose="00:00:00.0"
timeopen="00:00:00.0" update="UPDATABLE" updatecnt="0" vsamtype="NOTAPPLIC" wstrccurcnt="0" wstrcnt="0"/>
<cicslocalfile _keydata="BLAH2" accessmethod="VSAM" dsname="DFHLCD" eyu_cicsname="APPL1" file="DFHLCD" openstatus="OPEN"/>
</records>
</response>'''.strip()


def get_test_namespaces():
    return (
        'http://www.ibm.com/xmlns/prod/CICS/smw2int',
        'http://www.w3.org/2001/XMLSchema-instance'
    )


def parse_test_xml():
    return parse_xml(xml_string=get_test_xml_data(), strip_namespaces=get_test_namespaces())


def test_parse_xml_response_element():
    result = parse_test_xml()

    assert 'response' in result, "Root 'response' element should exist"
    response = result['response']

    assert response['@version'] == '3.0'
    assert response['@connect_version'] == '0610'


def test_parse_xml_namespace_stripping():
    result = parse_test_xml()
    response = result['response']

    assert '@schemaLocation' in response, "Namespace should be stripped from xsi:schemaLocation"
    assert '@xsi:schemaLocation' not in response, "Original namespaced attribute should not exist"
    assert '@xmlns:xsi' not in response, "Namespace declarations should not be included as attributes"


def test_parse_xml_resultsummary():
    result = parse_test_xml()
    response = result['response']

    assert 'resultsummary' in response
    resultsummary = response['resultsummary']

    assert resultsummary['@api_response1'] == '1024'
    assert resultsummary['@api_response2'] == '0'
    assert resultsummary['@recordcount'] == '2'


def test_parse_xml_records():
    result = parse_test_xml()
    response = result['response']

    assert 'records' in response
    assert 'cicslocalfile' in response['records']

    cicslocalfile = response['records']['cicslocalfile']

    assert isinstance(cicslocalfile, list)
    assert len(cicslocalfile) == 2
    assert cicslocalfile[0]['@file'] == 'DFHCSD'
    assert cicslocalfile[0]['@dsname'] == 'DFHCSD'
    assert cicslocalfile[0]['@accessmethod'] == 'VSAM'
    assert cicslocalfile[1]['@file'] == 'DFHLCD'
    assert cicslocalfile[1]['@openstatus'] == 'OPEN'


def test_parse_xml_force_list_single_record():
    xml = '<response><records><cicslocalfile file="A"/></records></response>'

    result = parse_xml(xml, force_list=('cicslocalfile',))

    assert result['response']['records']['cicslocalfile'] == [{'@file': 'A'}]


def test_parse_xml_force_list_with_multiple_children():
    xml = '<response><records><cicslocalfile file="A"/><cicslocalfile file="B"/></records></response>'

    result = parse_xml(xml, force_list=('cicslocalfile',))

    assert result['response']['records']['cicslocalfile'] == [{'@file': 'A'}, {'@file': 'B'}]


def test_parse_xml_single_child_not_a_list_by_default():
    result = parse_xml('<response><records><cicslocalfile file="A"/></records></response>')

    assert result['response']['records']['cicslocalfile'] == {'@file': 'A'}


def test_parse_xml_text_only_element():
    result = parse_xml('<response><item>hello</item></response>')

    assert result['response']['item'] == 'hello'


def test_parse_xml_text_with_attributes():
    result = parse_xml('<response><item name="a">hello</item></response>')

    assert result['response']['item'] == {'@name': 'a', '#text': 'hello'}


def test_parse_xml_force_list_text_only_element():
    result = parse_xml('<response><item>hello</item></response>', force_list=('item',))

    assert result['response']['item'] == ['hello']


def test_parse_xml_empty_and_whitespace_elements():
    result = parse_xml('<response><empty/><blank>   </blank><attrs name="a"/></response>')

    assert result['response']['empty'] is None
    assert result['response']['blank'] is None
    assert result['response']['attrs'] == {'@name': 'a'}


def test_parse_xml_with_declaration_and_whitespace():
    result = parse_xml('  \n<?xml version="1.0" encoding="UTF-8" ?>\n<response version="3.0"/>')

    assert result['response']['@version'] == '3.0'


def test_parse_xml_namespace_not_in_strip_list_is_kept():
    result = parse_xml('<response xmlns="urn:other"><item/></response>', strip_namespaces=get_test_namespaces())

    assert '{urn:other}response' in result


def test_parse_xml_invalid_raises_parse_error():
    with pytest.raises(ParseError):
        parse_xml('<response><a></response>')


def test_parse_xml_empty_string_raises_parse_error():
    with pytest.raises(ParseError):
        parse_xml('')


def test_unparse_xml():
    request_data = OrderedDict([
        ('request', OrderedDict([
            ('action', OrderedDict([
                ('@name', 'DISABLE')
            ]))
        ]))
    ])

    xml_string = unparse_xml(request_data)

    assert xml_string == '<request><action name="DISABLE"></action></request>'
    assert parse_xml(xml_string)['request']['action']['@name'] == 'DISABLE'


# The expected strings below are the exact output previously produced by
# xmltodict.unparse(..., full_document=False), which is what CMCI receives.
def test_unparse_xml_create_request():
    request_data = OrderedDict([
        ('request', OrderedDict([
            ('create', OrderedDict([
                ('parameter', [
                    {'@name': 'CSD'},
                    {'@name': 'BAS', '@value': 'x&y'}
                ]),
                ('attributes', OrderedDict([
                    ('@name', 'A&B<>"x\'y'),
                    ('@desc', 'multi word')
                ]))
            ]))
        ]))
    ])

    assert unparse_xml(request_data) == (
        '<request><create>'
        '<parameter name="CSD"></parameter>'
        '<parameter name="BAS" value="x&amp;y"></parameter>'
        '<attributes name="A&amp;B&lt;&gt;&quot;x\'y" desc="multi word"></attributes>'
        '</create></request>'
    )


def test_unparse_xml_action_with_parameters():
    request_data = {
        'request': {
            'action': OrderedDict([
                ('@name', 'DISABLE'),
                ('parameter', [{'@name': 'P', '@value': 'V'}])
            ])
        }
    }

    assert unparse_xml(request_data) == (
        '<request><action name="DISABLE"><parameter name="P" value="V"></parameter></action></request>'
    )


def test_unparse_xml_update_request():
    request_data = {'request': {'update': {'attributes': {'@status': 'ENABLED'}}}}

    assert unparse_xml(request_data) == '<request><update><attributes status="ENABLED"></attributes></update></request>'


def test_unparse_xml_empty_returns_empty_string():
    assert unparse_xml({}) == ''
    assert unparse_xml(None) == ''


def test_unparse_xml_namespace_declarations_round_trip():
    response_data = OrderedDict([
        ('response', OrderedDict([
            ('@xmlns', OrderedDict([
                ('', 'http://www.ibm.com/xmlns/prod/CICS/smw2int'),
                ('xsi', 'http://www.w3.org/2001/XMLSchema-instance')
            ])),
            ('@version', '3.0'),
            ('resultsummary', {'@api_response1': '1024'})
        ]))
    ])

    xml_string = unparse_xml(response_data)

    assert 'xmlns="http://www.ibm.com/xmlns/prod/CICS/smw2int"' in xml_string
    assert 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"' in xml_string

    result = parse_xml(xml_string, strip_namespaces=get_test_namespaces())
    assert result == OrderedDict([
        ('response', OrderedDict([
            ('@version', '3.0'),
            ('resultsummary', OrderedDict([('@api_response1', '1024')]))
        ]))
    ])


def test_unparse_xml_none_leaf_is_empty_element():
    xml_string = unparse_xml({'request': {'item': None}})

    assert xml_string == '<request><item></item></request>'
    assert parse_xml(xml_string) == OrderedDict([('request', OrderedDict([('item', None)]))])
