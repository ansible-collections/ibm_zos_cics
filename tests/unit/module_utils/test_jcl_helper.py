# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.jcl_helper import (
    JCLHelper, JCL_PREFIX, JOB_CARD, EXECS
)
import pytest
import sys


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_render_jcl():
    jcl_helper = JCLHelper()
    jcl_helper.job_data = {
        JOB_CARD: {"job_name": "TESTJOB"},
        EXECS: [{"name": "CICS", "pgm": "TESTPRG", "parm": "SI",
                 "dds": [{"COUT": [{"disp": "SHR", "dsn": "DATA.SET.NAME"}]}]}]
    }
    expected_jcl = ['//TESTJOB  JOB',
                    '//CICS     EXEC PGM=TESTPRG,PARM=SI',
                    '//COUT     DD DISP=SHR,DSN=DATA.SET.NAME',
                    '//']

    assert jcl_helper.render_jcl() == expected_jcl


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_write_job_statement():
    jcl_helper = JCLHelper()
    job_name = "TESTJOB"
    job_parameters = {"job_name": job_name,
                      "class": "A",
                      "user": "BOBSMITH",
                      "region": "0M"}

    expected_jcl = JCL_PREFIX + job_name + \
        "  JOB CLASS=A,USER=BOBSMITH,REGION=0M"
    jcl_helper._write_job_statement(job_parameters)
    assert jcl_helper.jcl == [expected_jcl]
    assert len(jcl_helper.jcl) == 1


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_write_long_job_statement():
    jcl_helper = JCLHelper()
    job_name = "TESTJOB"
    job_parameters = {"job_name": job_name,
                      "class": "A",
                      "user": "KIERA",
                      "region": "0M",
                      "msgclass": "A",
                      "memlimit": "10G",
                      "additional_parameter": "TESTONE",
                      "additional_parameter1": "TESTTWO"}

    expected_jcl = [JCL_PREFIX + job_name + "  JOB CLASS=A,USER=KIERA,REGION=0M,MSGCLASS=A,MEMLIMIT=10G,",
                    '//         ADDITIONAL_PARAMETER=TESTONE,ADDITIONAL_PARAMETER1=TESTTWO']
    jcl_helper._write_job_statement(job_parameters)
    assert jcl_helper.jcl == expected_jcl
    assert len(jcl_helper.jcl) == 2


def test_write_dds():
    jcl_helper = JCLHelper()
    dds = [{"COUT": [{"disp": "SHR", "dsn": "DATA.SET.NAME"}]}]
    jcl_helper._write_dds(dds)
    assert jcl_helper.jcl == [
        "//COUT     DD DISP=SHR,DSN=DATA.SET.NAME"]


def test_write_dds_with_instream():
    jcl_helper = JCLHelper()
    dds = [{"COUT": [{"disp": "SHR", "dsn": "DATA.SET.NAME"}]},
           {"INPUT": {"content": ['INSTREAM DATA']}}]
    jcl_helper._write_dds(dds)
    assert jcl_helper.jcl == ["//COUT     DD DISP=SHR,DSN=DATA.SET.NAME",
                              "//INPUT    DD *",
                              "INSTREAM DATA",
                              "/*"]


def test_write_dds_with_concatenation():
    jcl_helper = JCLHelper()
    dds = [{"COUT": [{"disp": "SHR", "dsn": "DATA.SET.NAME"}]},
           {"CONCAT": [{"disp": "OLD", "dsn": "DATA.SET.NAME1"},
                       {"disp": "SHR", "dsn": "DATA.SET.NAME2"}]}]
    jcl_helper._write_dds(dds)
    assert jcl_helper.jcl == ["//COUT     DD DISP=SHR,DSN=DATA.SET.NAME",
                              "//CONCAT   DD DISP=OLD,DSN=DATA.SET.NAME1",
                              "//         DD DISP=SHR,DSN=DATA.SET.NAME2"]


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_write_exec_statement():
    jcl_helper = JCLHelper()
    expected_jcl = [
        "//CICS     EXEC PGM=DFHSIP,PARM=SI,REGION=0M,TIME=1440"]
    jcl_helper._write_exec_statements([{"name": "CICS", "pgm": "DFHSIP", "parm": "SI", "region": "0M",
                                        "time": 1440, "dds": {}}])
    assert jcl_helper.jcl == expected_jcl


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_write_exec_statement_with_dds():
    jcl_helper = JCLHelper()
    expected_jcl = ["//CICS     EXEC PGM=DFHSIP,PARM=SI,REGION=0M,TIME=1440",
                    "//COUT     DD DISP=SHR,DSN=DATA.SET.NAME"]
    jcl_helper._write_exec_statements([{"name": "CICS", "pgm": "DFHSIP", "parm": "SI", "region": "0M", "time": 1440,
                                        "dds": [{"COUT": [{"disp": "SHR", "dsn": "DATA.SET.NAME"}]}]}])
    assert jcl_helper.jcl == expected_jcl


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_build_exec_statement_string():
    expected_jcl = "//CICS     EXEC PGM=DFHSIP,PARM=SI,REGION=0M,TIME=1440"
    exec_dict = {"name": "CICS", "pgm": "DFHSIP", "parm": "SI", "region": "0M", "time": 1440}
    assert JCLHelper._build_exec_statement_string(
        exec_dict) == expected_jcl


def test_build_exec_statement_string_with_no_parameters():
    expected_jcl = "//CICS     EXEC"
    exec_dict = {"name": "CICS"}
    assert JCLHelper._build_exec_statement_string(
        exec_dict) == expected_jcl


def test_write_list_of_strings():
    jcl_helper = JCLHelper()
    expected_jcl = ["//TEST     DD DISP=SHR,PARAM=TEST",
                    "//TEST2    DD DISP=SHR,PARAM=TEST2"]
    jcl_helper._write_list_of_strings(expected_jcl)
    assert jcl_helper.jcl == expected_jcl


def test_write_list_of_strings_pass_a_string():
    jcl_helper = JCLHelper()
    expected_jcl = "//TEST     DD DISP=SHR,PARAM=TEST"
    jcl_helper._write_list_of_strings(expected_jcl)
    assert jcl_helper.jcl == [expected_jcl]


def test_write_instream_data():
    jcl_helper = JCLHelper()
    jcl_helper._write_instream_data("COUT", {"content": ["FIRST=ONE", "SECOND=TWO"]})
    expected_statement = ["//COUT     DD *", "FIRST=ONE", "SECOND=TWO", "/*"]
    assert jcl_helper.jcl == expected_statement


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_write_instream_data_with_additional_parameters():
    jcl_helper = JCLHelper()
    jcl_helper._write_instream_data(
        "COUT", {"content": ["FIRST=ONE", "SECOND=TWO"], "DLM": "@@", "PARAM2": "TWO"})
    expected_statement = [
        "//COUT     DD *,DLM=@@,PARAM2=TWO", "FIRST=ONE", "SECOND=TWO", "/*"]
    assert jcl_helper.jcl == expected_statement


def test_write_dd_statement():
    jcl_helper = JCLHelper()
    jcl_helper._write_dd_statement(
        "COUT", {"disp": "SHR", "dsn": "DATA.SET.NAME"})
    expected_statement = ["//COUT     DD DISP=SHR,DSN=DATA.SET.NAME"]
    assert jcl_helper.jcl == expected_statement


def test_write_dd_concatenation():
    jcl_helper = JCLHelper()
    jcl_helper._write_dd_concatenation("SYSIN", [{"disp": "SHR", "dsn": "DATA.ONE"},
                                                 {"disp": "SHR", "dsn": "DATA.TWO"},
                                                 {"disp": "SHR", "dsn": "DATA.THREE"}])
    expected_statement = ["//SYSIN    DD DISP=SHR,DSN=DATA.ONE",
                          "//         DD DISP=SHR,DSN=DATA.TWO",
                          "//         DD DISP=SHR,DSN=DATA.THREE"]

    assert jcl_helper.jcl == expected_statement


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_write_dd_concatenation_with_long_line():
    jcl_helper = JCLHelper()
    jcl_helper._write_dd_concatenation("SYSIN", [{"disp": "SHR", "dsn": "DATA.ONE", "ONE": "FIRSTVAL",
                                                  "TWO": "SECONDVAL", "THIRD": "THIRDVAL", "FOUR": "FOURTHVAL"},
                                                 {"disp": "SHR", "dsn": "DATA.TWO"},
                                                 {"disp": "SHR", "dsn": "DATA.THREE"}])
    expected_statement = ["//SYSIN    DD DISP=SHR,DSN=DATA.ONE,ONE=FIRSTVAL,TWO=SECONDVAL,",
                          "//         THIRD=THIRDVAL,FOUR=FOURTHVAL",
                          "//         DD DISP=SHR,DSN=DATA.TWO",
                          "//         DD DISP=SHR,DSN=DATA.THREE"]

    assert jcl_helper.jcl == expected_statement


def test_write_null_statement():
    jcl_helper = JCLHelper()
    jcl_helper._write_null_statement()
    expected_statement = ["//"]
    assert jcl_helper.jcl == expected_statement


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_build_job_statement():
    job_parameters = {"job_name": "JOB123",
                      "class": "A",
                      "user": "BOBSMITH",
                      "region": "0M"}
    expected_statement = JCL_PREFIX + "JOB123   JOB CLASS=A,USER=BOBSMITH,REGION=0M"
    assert JCLHelper._build_job_statement(
        job_parameters) == expected_statement


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_build_job_statement_with_accounting_info():
    job_parameters = {"job_name": "JOB123",
                      "accounting_information": {"pano": "ABCD"},
                      "class": "A",
                      "user": "BOBSMITH",
                      "region": "0M"}
    expected_statement = JCL_PREFIX + "JOB123   JOB ABCD,CLASS=A,USER=BOBSMITH,REGION=0M"
    assert JCLHelper._build_job_statement(
        job_parameters) == expected_statement


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_build_job_statement_with_programmer_name():
    job_parameters = {"job_name": "JOB123",
                      "programmer_name": "USER",
                      "class": "A",
                      "user": "BOBSMITH",
                      "region": "0M"}
    expected_statement = JCL_PREFIX + "JOB123   JOB ,'USER',CLASS=A,USER=BOBSMITH,REGION=0M"
    assert JCLHelper._build_job_statement(
        job_parameters) == expected_statement


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_build_job_statement_with_programmer_name_and_account_info():
    job_parameters = {"job_name": "JOB123",
                      "accounting_information": {"pano": "ABCD"},
                      "programmer_name": "USER",
                      "class": "A",
                      "user": "BOBSMITH",
                      "region": "0M"}
    expected_statement = JCL_PREFIX + "JOB123   JOB ABCD,'USER',CLASS=A,USER=BOBSMITH,REGION=0M"
    assert JCLHelper._build_job_statement(
        job_parameters) == expected_statement


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_build_job_statement_with_msglevel_parameter_statements():
    job_parameters = {"job_name": "JOB123",
                      "programmer_name": "USER",
                      "class": "A",
                      "msglevel": {"statements": 0},
                      "user": "BOBSMITH",
                      "region": "0M"}
    expected_statement = JCL_PREFIX + "JOB123   JOB ,'USER',CLASS=A,MSGLEVEL=0,USER=BOBSMITH,REGION=0M"
    assert JCLHelper._build_job_statement(
        job_parameters) == expected_statement


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_build_job_statement_with_msglevel_parameter_messages():
    job_parameters = {"job_name": "JOB123",
                      "programmer_name": "USER",
                      "class": "A",
                      "msglevel": {"messages": 1},
                      "user": "BOBSMITH",
                      "region": "0M"}
    expected_statement = JCL_PREFIX + "JOB123   JOB ,'USER',CLASS=A,MSGLEVEL=(,1),USER=BOBSMITH,REGION=0M"
    assert JCLHelper._build_job_statement(
        job_parameters) == expected_statement


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_build_job_statement_with_msglevel_parameter():
    job_parameters = {"job_name": "JOB123",
                      "programmer_name": "USER",
                      "class": "A",
                      "msglevel": {"statements": 1, "messages": 1},
                      "user": "BOBSMITH",
                      "region": "0M"}
    expected_statement = JCL_PREFIX + "JOB123   JOB ,'USER',CLASS=A,MSGLEVEL=(1,1),USER=BOBSMITH,REGION=0M"
    assert JCLHelper._build_job_statement(
        job_parameters) == expected_statement


def test_format_job_positional_parameters_two_accounting_infomation_values():
    jcl_helper = JCLHelper()
    job_parameters = {"accounting_information": {"pano": "ABCD", "times": 12}, "programmer_name": "USER"}
    expected_statement = "(ABCD,,12),USER"
    assert jcl_helper._format_job_positional_parameters(job_parameters) == expected_statement


def test_format_job_positional_parameters_accounting_information_only():
    jcl_helper = JCLHelper()
    job_parameters = {"accounting_information": {"pano": "ABCD"}}
    expected_statement = "ABCD"
    assert jcl_helper._format_job_positional_parameters(job_parameters) == expected_statement


def test_format_job_positional_parameters_two_accounting_infomation_values():
    jcl_helper = JCLHelper()
    job_parameters = {"accounting_information": {"pano": "ABCD", "times": 12}}
    expected_statement = "(ABCD,,12)"
    assert jcl_helper._format_job_positional_parameters(job_parameters) == expected_statement


def test_format_job_positional_parameters_only_programmer_name():
    jcl_helper = JCLHelper()
    job_parameters = {"programmer_name": "USER"}
    expected_statement = ",'USER'"
    assert jcl_helper._format_job_positional_parameters(job_parameters) == expected_statement


def test_format_job_positional_parameters_positional_info_not_set():
    jcl_helper = JCLHelper()
    job_parameters = {"job_name": "JOB123"}
    expected_statement = None
    assert jcl_helper._format_job_positional_parameters(job_parameters) == expected_statement


def test_format_job_positional_parameters_job_parameters_none():
    jcl_helper = JCLHelper()
    expected_statement = None
    assert jcl_helper._format_job_positional_parameters(None) == expected_statement


def test_format_accounting_information():
    accounting_information = {"pano": "AB12", "room": "ROOM", "times": "TIME", "lines": 23}
    formatted_information = JCLHelper._format_accounting_information(accounting_information)
    assert formatted_information == "(AB12,ROOM,TIME,23)"


def test_format_accounting_information_with_missing_values():
    accounting_information = {"pano": "AB12", "times": "TIME", "lines": 23}
    formatted_information = JCLHelper._format_accounting_information(accounting_information)
    assert formatted_information == "(AB12,,TIME,23)"


def test_format_accounting_information_with_missing_value_2():
    accounting_information = {"room": "ABC", "times": "TIME", "lines": 23}
    formatted_information = JCLHelper._format_accounting_information(accounting_information)
    assert formatted_information == "(,ABC,TIME,23)"


def test_format_accounting_information_with_missing_values_3():
    accounting_information = {"pano": "EDFG", "lines": 23, "cards": "CARD"}
    formatted_information = JCLHelper._format_accounting_information(accounting_information)
    assert formatted_information == "(EDFG,,,23,CARD)"


def test_format_accounting_information_with_one_value():
    accounting_information = {"pano": "EDFG"}
    formatted_information = JCLHelper._format_accounting_information(accounting_information)
    assert formatted_information == "EDFG"


def test_format_programmer_name_no_apostrophes():
    name = "USER"
    formatted = JCLHelper._format_programmer_name(name)
    assert formatted == "'USER'"


def test_format_programmer_name_with_apostrophes():
    name = "USER'NAME"
    formatted = JCLHelper._format_programmer_name(name)
    assert formatted == "'USER''NAME'"


def test_format_msglevel_parameter_both_parameters():
    msglevel_dict = {"statements": 1, "messages": 0}
    msglevel_dict_formatted = JCLHelper._format_msglevel_parameter(msglevel_dict)
    assert msglevel_dict_formatted == "(1,0)"


def test_format_msglevel_parameter_statements_only():
    msglevel_dict = {"statements": 1}
    msglevel_dict_formatted = JCLHelper._format_msglevel_parameter(msglevel_dict)
    assert msglevel_dict_formatted == 1


def test_format_msglevel_parameter_messages_only():
    msglevel_dict = {"messages": 1}
    msglevel_dict_formatted = JCLHelper._format_msglevel_parameter(msglevel_dict)
    assert msglevel_dict_formatted == "(,1)"


def test_build_dd_statement():
    jcl_helper = JCLHelper()
    expected_statement = "//COUT     DD DISP=SHR,DSN=DATA.SET.NAME"
    parameters = {"disp": "SHR", "dsn": "DATA.SET.NAME"}
    assert jcl_helper._build_dd_statement("COUT", parameters) == expected_statement


def test_build_dd_statement_with_no_dd_name():
    jcl_helper = JCLHelper()
    expected_statement = None
    parameters = {"disp": "SHR", "dsn": "DATA.SET.NAME"}
    assert jcl_helper._build_dd_statement(None, parameters) == expected_statement


def test_build_dd_concatenation_list():
    jcl_helper = JCLHelper()
    job_name = "DFHTEST"
    list_of_dicts = [{'disp': 'SHR', 'dsn': 'TEST.CICS.PRINT'},
                     {'disp': 'OLD', 'dsn': 'TEST.CICS.PRINT2'}]

    expected = ['//DFHTEST  DD DISP=SHR,DSN=TEST.CICS.PRINT',
                '//         DD DISP=OLD,DSN=TEST.CICS.PRINT2']
    assert jcl_helper._build_dd_concatenation_list(
        job_name, list_of_dicts) == expected


def test_build_dd_concatenation_list_length_one():
    jcl_helper = JCLHelper()
    job_name = "DFHTEST"
    list_of_dicts = [{'disp': 'SHR', 'dsn': 'TEST.CICS.PRINT'}]

    expected = ['//DFHTEST  DD DISP=SHR,DSN=TEST.CICS.PRINT']
    assert jcl_helper._build_dd_concatenation_list(
        job_name, list_of_dicts) == expected


def test_format_dd_name():
    assert JCLHelper._format_dd_name("TEST") == "TEST     "


def test_exceeds_line_length_short():
    dd_statement = "// This is a short statement"
    assert JCLHelper._exceeds_line_length(dd_statement) is False


def test_exceeds_line_length_long():
    dd_statement = "// This is a longer test comment which is over the current specified max limit"
    assert JCLHelper._exceeds_line_length(dd_statement) is True


def test_split_too_long_dd_statement_list():
    long_dd_statement = ["//TOOLONG  DD DISP=SHR,DSN=TOOLONGNAME,PARM1=ONE,PARM2=TWO,PARM3=THREE,PARM4=FOUR",
                         "//THIS DD ONE=SHORT"]
    split_statement = JCLHelper._split_long_dd_statement_list(long_dd_statement)
    assert split_statement == ["//TOOLONG  DD DISP=SHR,DSN=TOOLONGNAME,PARM1=ONE,PARM2=TWO,PARM3=THREE,",
                               "//         PARM4=FOUR",
                               "//THIS DD ONE=SHORT"]


def test_split_too_long_dd_statement_list_not_a_list():
    long_dd_statement = "//TOOLONG  DD DISP=SHR,DSN=TOOLONGNAME,PARM1=ONE,PARM2=TWO,PARM3=THREE,PARM4=FOUR"
    split_statement = JCLHelper._split_long_dd_statement_list(long_dd_statement)
    assert split_statement == ["//TOOLONG  DD DISP=SHR,DSN=TOOLONGNAME,PARM1=ONE,PARM2=TWO,PARM3=THREE,",
                               "//         PARM4=FOUR"]


def test_split_too_long_dd_statement_list_but_not_long():
    dd_statement_list = ["//NOTLONG  DD DISP=SHR,DSN=TOOLONGNAME,PARM1=ONE",
                         "//THIS DD ONE=SHORT"]
    split_statement = JCLHelper._split_long_dd_statement_list(dd_statement_list)
    assert split_statement == ["//NOTLONG  DD DISP=SHR,DSN=TOOLONGNAME,PARM1=ONE",
                               "//THIS DD ONE=SHORT"]


def test_split_too_long_dd_statement():
    long_dd_statement = "//TOOLONG  DD DISP=SHR,DSN=TOOLONGNAME,PARM1=ONE,PARM2=TWO,PARM3=THREE,PARM4=FOUR"
    split_statement = JCLHelper._split_long_dd_statement(long_dd_statement)
    assert split_statement == ["//TOOLONG  DD DISP=SHR,DSN=TOOLONGNAME,PARM1=ONE,PARM2=TWO,PARM3=THREE,",
                               "//         PARM4=FOUR"]


def test_add_parameters_onto_existing_dd_statement():
    existing_dd_statement = "//TEST     DD NEED SOME PARAMETERS"
    parameter_list = ["PARAM1=ONE", "PARAM2=TWO"]
    expected = "//TEST     DD NEED SOME PARAMETERS,PARAM1=ONE,PARAM2=TWO"
    assert JCLHelper._add_parameters_onto_dd_statement(
        existing_dd_statement, parameter_list, True) == expected


def test_build_parameter_string():
    parameter_list = ["TEST1=PARM1", "TEST2=PARM2", "TEST3=PARM3"]
    assert JCLHelper._build_parameter_string(
        parameter_list) == "TEST1=PARM1,TEST2=PARM2,TEST3=PARM3"


def test_build_parameter_string_when_none():
    parameter_list = None
    assert JCLHelper._build_parameter_string(parameter_list) == ""


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_concatenate_key_value_pairs_into_list():
    dictionary = {"Val1": "One", "Val2": "Two", "Val3": "Three", "Val4": "Four"}
    dictionary_unpacked = JCLHelper._concatenate_key_value_pairs_into_list(
        dictionary)
    assert dictionary_unpacked == ["VAL1=One", "VAL2=Two", "VAL3=Three", "VAL4=Four"]


def test_add_single_quotes_to_text():
    assert JCLHelper._add_single_quotes_to_text("'hello'") == "'hello'"
    assert JCLHelper._add_single_quotes_to_text("hello") == "'hello'"
    assert JCLHelper._add_single_quotes_to_text("\"'hello'\"") == "\"'hello'\""
    assert JCLHelper._add_single_quotes_to_text("\"hel'lo\"") == "'hel''lo'"
    assert JCLHelper._add_single_quotes_to_text("hel'lo") == "'hel''lo'"
    assert JCLHelper._add_single_quotes_to_text("h'e'l'l'o") == "'h''e''l''l''o'"
