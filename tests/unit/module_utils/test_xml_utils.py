# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2025
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from typing import OrderedDict

from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils._xml_utils import (
    parse_xml, unparse_xml)


def get_test_xml_data():
    return '''<response xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://www.ibm.com/xmlns/prod/CICS/smw2int http://example.com/CICSSystemManagement/schema/CICSSystemManagement.xsd"
version="3.0" connect_version="0610">
<resultsummary api_response1="1024" api_response2="0" api_response1_alt="OK" api_response2_alt="" recordcount="4" displayed_recordcount="4"/>
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
</records>
</response>'''.strip()


def get_test_namespaces():
    return {
        'http://www.ibm.com/xmlns/prod/CICS/smw2int': None,
        'http://www.w3.org/2001/XMLSchema-instance': None
    }


def parse_test_xml():
    return parse_xml(xml_string=get_test_xml_data(), namespaces=get_test_namespaces())


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
    assert resultsummary['@recordcount'] == '4'


def test_parse_xml_records():
    result = parse_test_xml()
    response = result['response']

    assert 'records' in response
    assert 'cicslocalfile' in response['records']

    cicslocalfile = response['records']['cicslocalfile']

    assert cicslocalfile['@file'] == 'DFHCSD'
    assert cicslocalfile['@dsname'] == 'DFHCSD'
    assert cicslocalfile['@accessmethod'] == 'VSAM'


def test_unparse_xml():
    request_data = OrderedDict([
        ('request', OrderedDict([
            ('action', OrderedDict([
                ('@name', 'DISABLE')
            ]))
        ]))
    ])

    xml_string = unparse_xml(request_data)

    assert '<request>' in xml_string
    assert '<action name="DISABLE"></action>' in xml_string
    assert '</request>' in xml_string

    assert parse_xml(xml_string)['request']['action']['@name'] == 'DISABLE'
