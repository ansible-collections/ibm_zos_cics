# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
import json

from _pytest.monkeypatch import MonkeyPatch
from ansible.module_utils.common.text.converters import to_bytes
from ansible.module_utils import basic
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import _data_set_utils
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils._response import _execution
from ansible_collections.ibm.ibm_zos_cics.plugins.modules.region_jcl import (
    AnsibleRegionJCLModule as StartCICSModule, DFHSIP, PGM, DISP, DSN, SHR
)
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils._jcl_helper import (
    NAME, DDS
)
from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.data_set_helper import (
    IDCAMS_delete,
    IDCAMS_delete_run_name,
    IEFBR14_create_stderr,
    LISTDS_data_set,
    LISTDS_data_set_doesnt_exist,
    LISTDS_run_name,
    get_sample_generated_JCL,
    get_sample_generated_JCL_args
)
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.zos_mvs_raw import MVSCmdResponse
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.data_set import DataSet
import pytest
import sys

try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock


DS_NAME = "TEST.DATA.START"

default_arg_parms = {
    "state": "initial",
    "applid": "APPLID",
    "cics_data_sets": {},
    "le_data_sets": {},
    "output_data_sets": {},
    "region_data_sets": {
        "dfhstart": {
            "dsn": DS_NAME
        }
    }
}


def set_module_args(args):
    """prepare arguments so that they will be picked up during module creation"""
    args = json.dumps({'ANSIBLE_MODULE_ARGS': args})
    basic._ANSIBLE_ARGS = to_bytes(args)


def setup_and_update_parms(args):
    parms = default_arg_parms
    parms.update(args)
    set_module_args(parms)
    dfhsip = StartCICSModule()
    dfhsip._remove_none_values_from_dict(dfhsip._module.params)
    return dfhsip


def prepare_for_fail():
    monkey_patch = MonkeyPatch()
    monkey_patch.setattr(basic.AnsibleModule, "fail_json", fail_json)


def prepare_for_exit():
    monkey_patch = MonkeyPatch()
    monkey_patch.setattr(basic.AnsibleModule, "exit_json", exit_json)


def fail_json(*args, **kwargs):
    """function to patch over fail_json; package return data into an exception"""
    kwargs['failed'] = True
    raise AnsibleFailJson(kwargs)


def exit_json(*args, **kwargs):
    """function to patch over exit_json; package return data into an exception"""
    kwargs['failed'] = False


class AnsibleFailJson(Exception):
    """Exception class to be raised by module.fail_json and caught by the test case"""
    pass


def test_populate_job_card_dict_with_job_name():
    module = setup_and_update_parms({
        "job_parameters": {"job_name": "STRTCICS"}})
    module._populate_job_card_dict()
    assert module.jcl_helper.job_data['job_card'] == {"job_name": "STRTCICS"}


def test_populate_job_card_dict_without_job_name():
    module = setup_and_update_parms({})
    module._populate_job_card_dict()
    assert module.jcl_helper.job_data['job_card'] == {"job_name": "APPLID"}


def test_populate_job_card_dict_without_job_name_but_with_region():
    module = setup_and_update_parms({
        "job_parameters": {"region": "0M"}})
    module._populate_job_card_dict()
    assert module.jcl_helper.job_data['job_card'] == {"job_name": "APPLID", "region": "0M"}


def test_add_exec_parameters():
    module = setup_and_update_parms({})
    module._add_exec_parameters({NAME: "", PGM: DFHSIP, DDS: {}})
    print(module.jcl_helper.job_data['execs'])
    assert module.jcl_helper.job_data['execs'] == [{'name': '', 'pgm': DFHSIP, 'dds': {}}]


def test_add_exec_parameters_with_sit_parameters():
    module = setup_and_update_parms({"sit_parameters": {"start": "COLD"}})
    module._add_exec_parameters({NAME: "", PGM: DFHSIP, DDS: {}})
    print(module.jcl_helper.job_data['execs'])
    assert module.jcl_helper.job_data['execs'] == [{'name': '', 'pgm': DFHSIP, 'dds': {}, 'PARM': 'SI'}]


def test_add_block_of_libraries_empty_libraries():
    module = setup_and_update_parms({"steplib": {"top_data_sets": [], "data_sets": []}})
    module._add_block_of_libraries("steplib")
    assert module.dds == []


def test_add_block_of_libraries_empty_top_data_sets():
    module = setup_and_update_parms({"steplib": {"top_data_sets": [], "data_sets": ["LIB.ONE"]}})
    module._add_block_of_libraries("steplib")
    assert module.dds == [{"steplib": [{DISP: SHR, DSN: "LIB.ONE"}]}]


def test_add_block_of_libraries_dict_is_none():
    set_module_args(default_arg_parms)
    dfhsip = StartCICSModule()
    dfhsip._module.params.pop("steplib")
    dfhsip._add_block_of_libraries("steplib")
    assert dfhsip.dds == []


def test_get_delimiter_when_dlm_not_needed():
    set_module_args(default_arg_parms)
    dfhsip = StartCICSModule()
    dlm = dfhsip._get_delimiter(["value1=one", "value2=two", "value3=three"])
    assert dlm is None


def test_get_delimiter():
    set_module_args(default_arg_parms)
    dfhsip = StartCICSModule()
    dlm = dfhsip._get_delimiter(["value1=one", "value2=two/*", "value3=three"])
    assert dlm == "@@"


def test_find_unused_character():
    content = [
        "Hello"
        "instream_content",
    ]
    dlm = StartCICSModule._find_unused_character(content)
    assert dlm == "@@"


def test_find_unused_character_with_some_preferred_chars_used():
    content = [
        "Hello",
        "instream_content",
        "@@$$##"
    ]
    dlm = StartCICSModule._find_unused_character(content)
    assert dlm == "@$"


def test_find_unused_character_with_all_preferred_chars_used():
    content = [
        "Hello",
        "instream_content",
        "@@$$##@#$@"
    ]
    dlm = StartCICSModule._find_unused_character(content)
    assert dlm == "@$"


def test_find_unused_character_with_preferred_chars_and_first_combinations_used():
    content = [
        "Hello",
        "AAABBBCC"
        "instream_content",
        "@@$$##@#$@"
    ]
    dlm = StartCICSModule._find_unused_character(content)
    assert dlm == "@$"


def test_find_unused_character_with_preferred_chars_used():
    content = [
        "Hello",
        "instream_content",
        "@@",
        "$$",
        "##",
        "@#",
        "$@",
        "#@",
        "@$",
        "$#",
        "#$"]
    dlm = StartCICSModule._find_unused_character(content)
    assert dlm == "@A"


def test_validate_content():
    prepare_for_exit()
    set_module_args(default_arg_parms)
    module = StartCICSModule()
    content = ["LISTCAT ENTRIES('SOME.data_set.*')",
               "LISTCAT ENTRIES('SOME.OTHER.DS.*')"]
    module._validate_content(content)
    module._exit()
    assert module.result["failed"] is False


def test_validate_content_with_passing_jcl():
    prepare_for_exit()
    set_module_args(default_arg_parms)
    module = StartCICSModule()
    content = ["//TEST DD DISP=SHR,DSN=TEST.DATA"]
    module._validate_content(content)
    module._exit()
    assert module.result["failed"] is False


def test_validate_content_with_invalid_content_dd_data():
    prepare_for_fail()
    set_module_args(default_arg_parms)
    module = StartCICSModule()
    content = ["//TEST DD DISP=SHR,DSN=TEST.DATA", "//TEST2 DD DATA"]
    with pytest.raises(AnsibleFailJson) as exec_info:
        module._validate_content(content)
    expected = "Invalid content for an in-stream: DD DATA"
    assert exec_info.value.args[0]['msg'] == expected
    assert module.result["failed"] is True


def test_validate_content_with_invalid_content_DD_instream():
    prepare_for_fail()
    set_module_args(default_arg_parms)
    module = StartCICSModule()
    content = ["//TEST DD DISP=SHR,DSN=TEST.DATA", "//TEST2 DD *"]
    with pytest.raises(AnsibleFailJson) as exec_info:
        module._validate_content(content)
    expected = "Invalid content for an in-stream: DD *"
    assert exec_info.value.args[0]['msg'] == expected
    assert module.result["failed"] is True


def test_check_for_existing_dlm_within_content_true():
    set_module_args(default_arg_parms)
    module = StartCICSModule()
    content = ["RUN PROGRAM", "/* RUNNING */"]
    end_stream_present = module._check_for_existing_dlm_within_content(
        content)
    assert end_stream_present is True


def test_check_for_existing_dlm_within_content_falce():
    set_module_args(default_arg_parms)
    module = StartCICSModule()
    content = ["RUN PROGRAM", "HELLO WORLD"]
    end_stream_present = module._check_for_existing_dlm_within_content(
        content)
    assert end_stream_present is False


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_add_output_data_sets_with_global_default():
    module = setup_and_update_parms({
        "output_data_sets": {"default_sysout_class": "A"}})
    module._add_output_data_sets()
    assert module.dds == [{"ceemsg": [{"sysout": "A"}]}, {"ceeout": [{"sysout": "A"}]}, {"msgusr": [{"sysout": "A"}]},
                          {"sysprint": [{"sysout": "A"}]}, {"sysudump": [{"sysout": "A"}]},
                          {"sysabend": [{"sysout": "A"}]}, {"sysout": [{"sysout": "A"}]},
                          {"dfhcxrf": [{"sysout": "A"}]}, {"logusr": [{"sysout": "A"}]}]


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_add_output_data_sets_without_global_default():
    module = setup_and_update_parms({})
    module._add_output_data_sets()
    assert module.dds == [{"ceemsg": [{"sysout": "*"}]}, {"ceeout": [{"sysout": "*"}]}, {"msgusr": [{"sysout": "*"}]},
                          {"sysprint": [{"sysout": "*"}]}, {"sysudump": [{"sysout": "*"}]},
                          {"sysabend": [{"sysout": "*"}]}, {"sysout": [{"sysout": "*"}]},
                          {"dfhcxrf": [{"sysout": "*"}]}, {"logusr": [{"sysout": "*"}]}]


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_add_output_data_sets_with_overrides_and_global_default():
    module = setup_and_update_parms({"output_data_sets": {
        "default_sysout_class": "A", "ceemsg": {"sysout": "B"},
        "logusr": {"sysout": "*"}
    }})
    module._add_output_data_sets()
    assert module.dds == [{"ceemsg": [{"sysout": "B"}]}, {"logusr": [{"sysout": "*"}]}, {"ceeout": [{"sysout": "A"}]},
                          {"msgusr": [{"sysout": "A"}]}, {"sysprint": [{"sysout": "A"}]},
                          {"sysudump": [{"sysout": "A"}]}, {"sysabend": [{"sysout": "A"}]},
                          {"sysout": [{"sysout": "A"}]}, {"dfhcxrf": [{"sysout": "A"}]}]


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_add_output_data_sets_with_overrides_and_omit():
    module = setup_and_update_parms({"output_data_sets": {
        "default_sysout_class": "A", "ceemsg": {"sysout": "B"},
        "logusr": {"omit": True}
    }})
    module._add_output_data_sets()
    assert module.dds == [{"ceemsg": [{"sysout": "B"}]}, {"ceeout": [{"sysout": "A"}]},
                          {"msgusr": [{"sysout": "A"}]}, {"sysprint": [{"sysout": "A"}]},
                          {"sysudump": [{"sysout": "A"}]}, {"sysabend": [{"sysout": "A"}]},
                          {"sysout": [{"sysout": "A"}]}, {"dfhcxrf": [{"sysout": "A"}]}]


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_add_output_data_sets_without_global_default_and_with_override():
    module = setup_and_update_parms({"output_data_sets": {"ceemsg": {"sysout": "B"}, "logusr": {"omit": True}}})
    module._add_output_data_sets()
    assert module.dds == [{"ceemsg": [{"sysout": "B"}]}, {"ceeout": [{"sysout": "*"}]}, {"msgusr": [{"sysout": "*"}]},
                          {"sysprint": [{"sysout": "*"}]}, {"sysudump": [{"sysout": "*"}]},
                          {"sysabend": [{"sysout": "*"}]}, {"sysout": [{"sysout": "*"}]},
                          {"dfhcxrf": [{"sysout": "*"}]}]


def test_remove_omited_data_set():
    module = setup_and_update_parms({})
    data_set = "ceeout"
    user_data_sets = {data_set: {"omit": True}}
    module._remove_omitted_data_set(data_set, user_data_sets)
    assert user_data_sets == {}


def test_remove_omited_data_set_with_omit_false():
    module = setup_and_update_parms({})
    data_set = "ceeout"
    user_data_sets = {data_set: {"omit": False}}
    module._remove_omitted_data_set(data_set, user_data_sets)
    assert user_data_sets == {"ceeout": {"omit": False}}


def test_remove_omited_data_set_not_present():
    data_set = "ceemsg"
    module = setup_and_update_parms({})
    user_data_sets = {"ceeout": {"omit": True}}
    module._remove_omitted_data_set(data_set, user_data_sets)
    assert user_data_sets == {"ceeout": {"omit": True}}


def test_set_sysout_class_for_data_set_no_override():
    module = setup_and_update_parms({})
    data_set = "ceemsg"
    default_class = "A"
    user_data_sets = {'ceeout': {'sysout': 'B'}}
    module._set_sysout_class_for_data_set(
        data_set, default_class, user_data_sets)
    assert user_data_sets == {"ceeout": {
        "sysout": "B"}, data_set: {"sysout": default_class}}


def test_set_sysout_class_for_data_set_with_override():
    module = setup_and_update_parms({})
    data_set = "ceemsg"
    default_class = "A"
    user_data_sets = {"ceemsg": {"sysout": "B"}}
    module._set_sysout_class_for_data_set(
        data_set, default_class, user_data_sets)
    assert user_data_sets == {"ceemsg": {"sysout": "B"}}


def test_add_per_region_data_sets():
    module = setup_and_update_parms({"region_data_sets": {"dfhcsd": {"dsn": "TEST.DATA.DFHCSD"},
                                    "dfhtemp": {"dsn": "TEST.DATA.DFHTEMP"},
                                    "dfhstart": {"dsn": DS_NAME}}})
    module._add_per_region_data_sets()
    assert module.dds == [{"dfhcsd": [{"dsn": "TEST.DATA.DFHCSD", "disp": "SHR"}]},
                          {"dfhtemp": [{"dsn": "TEST.DATA.DFHTEMP", "disp": "SHR"}]}]


def test_add_libraries():
    module = setup_and_update_parms({})
    dsn_dict = module._add_libraries(["LIB.ONE", "LIB.TWO", "LIB.THREE"])
    assert dsn_dict == [{"dsn": "LIB.ONE", "disp": "SHR"},
                        {"dsn": "LIB.TWO", "disp": "SHR"},
                        {"dsn": "LIB.THREE", "disp": "SHR"}]


def test_add_libraries_with_none_value():
    module = setup_and_update_parms({})
    dsn_dict = module._add_libraries(["LIB.ONE", None, "LIB.THREE"])
    assert dsn_dict == [{"dsn": "LIB.ONE", "disp": "SHR"},
                        {"dsn": "LIB.THREE", "disp": "SHR"}]


def test_add_libraries_with_none_passed():
    module = setup_and_update_parms({})
    dsn_dict = module._add_libraries([])
    assert dsn_dict == []


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_add_sit_parameters():
    module = setup_and_update_parms({"sit_parameters": {}})
    # All sit parms have been added automatically and set as None.
    module._module.params["sit_parameters"]["AICONS"] = "AUTO"
    module._add_sit_parameters()
    assert module.dds == [{"sysin": {"content": ["AICONS=AUTO", "APPLID=APPLID"]}}]


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_add_sit_parameters_with_dictionaries_in_sit_parms():
    module = setup_and_update_parms({"sit_parameters": {}})
    # All sit parms have been added automatically and set as None.
    module._module.params["sit_parameters"]["AICONS"] = "AUTO"
    module._module.params["sit_parameters"]["strnxx"] = {
        "ap": "VAL1", "aq": "VAL2"}

    module._add_sit_parameters()
    print(module.dds)
    assert module.dds == [
        {"sysin": {"content": ["AICONS=AUTO", "APPLID=APPLID", "STRNAP=VAL1", "STRNAQ=VAL2"]}}]


def test_add_sit_parameters_when_none():
    module = setup_and_update_parms({"sit_parameters": None})
    # All sit parms have been added automatically and set as None.
    module.dds = []
    module._add_sit_parameters()
    assert module.dds == []


def test_manage_dictionaries_in_sit_parameters():
    dictionary_of_values = {"Param1": "value1",
                            "paramxxx": {"VAL": "TRUE", "NUM": "TWO"}}
    module = setup_and_update_parms({})
    module._manage_dictionaries_in_sit_parameters(dictionary_of_values)
    assert dictionary_of_values == {
        "Param1": "value1", "paramVAL": "TRUE", "paramNUM": "TWO"}


def test_validate_dictionary_value_within_sit_parms():
    prepare_for_exit()
    string_with_trailing_x = "paramxx"
    value = "ap"
    module = setup_and_update_parms({})
    module._validate_dictionary_value_within_sit_parms(
        string_with_trailing_x, value)
    module._exit()
    assert module.result["failed"] is False


def test_validate_dictionary_value_within_sit_parms_skr_4_letters():
    prepare_for_exit()
    string_with_trailing_x = "SKRXXXX"
    value = "PA24"
    module = setup_and_update_parms({})
    module._validate_dictionary_value_within_sit_parms(
        string_with_trailing_x, value)
    module._exit()
    assert module.result["failed"] is False


def test_validate_dictionary_value_within_sit_parms_skr_3_letters():
    prepare_for_exit()
    string_with_trailing_x = "SKRXXXX"
    value = "PA1"
    module = setup_and_update_parms({})
    module._validate_dictionary_value_within_sit_parms(
        string_with_trailing_x, value)
    module._exit()
    assert module.result["failed"] is False


def test_validate_dictionary_value_within_sit_parms_skr_5_letters():
    string_with_trailing_x = "SKRXXXX"
    value = "PA015"
    prepare_for_fail()
    module = setup_and_update_parms({})
    with pytest.raises(AnsibleFailJson) as exec_info:
        module._validate_dictionary_value_within_sit_parms(
            string_with_trailing_x, value)
    expected = "Invalid key: PA015. Key must be a length of 3 or 4."
    assert exec_info.value.args[0]['msg'] == expected
    assert module.result["failed"] is True


def test_validate_dictionary_value_within_sit_parms_value_length_doesnt_match_trailing_x():
    string_with_trailing_x = "STRNRXXX"
    value = "VAL2"
    prepare_for_fail()
    module = setup_and_update_parms({})
    with pytest.raises(AnsibleFailJson) as exec_info:
        module._validate_dictionary_value_within_sit_parms(
            string_with_trailing_x, value)
    expected = "Invalid key: VAL2. Key must be the same length as the x's within STRNRXXX."
    assert exec_info.value.args[0]['msg'] == expected
    assert module.result["failed"] is True


def test_remove_none_values_from_dict():
    module = setup_and_update_parms({})
    # All sit parms have been added automatically and set as None.
    # Assert they've been added.
    arg_spec = {"sit_parameters": {"one": 1, "two": 2},
                "data_sets": {"auxt": {"disp": "SHR", "omit": None}, "buxt": None}}
    module._remove_none_values_from_dict(arg_spec)
    assert arg_spec == {"sit_parameters": {"one": 1, "two": 2},
                        "data_sets": {"auxt": {"disp": "SHR"}}}


def test_check_parameter_is_provided():
    module = setup_and_update_parms({})
    assert module._check_parameter_is_provided("applid") is True


def test_check_parameter_is_provided_when_its_absent():
    dfhsip = setup_and_update_parms({})
    assert dfhsip._check_parameter_is_provided("dfhcsd") is False


def test_fail():
    prepare_for_fail()
    module = setup_and_update_parms({})
    expected_message = "Module failed for test"
    with pytest.raises(AnsibleFailJson) as message:
        module._fail(expected_message)
    assert message.value.args[0]['msg'] == expected_message
    assert module.result["failed"]


def test_concat_libraries_both_provided():
    prepare_for_exit()
    data_sets = ["FIRST.LIB", "SECOND.LIB"]
    top_data_sets = ["FIRST.TOP.LIB", "SECOND.TOP.LIB"]
    module = setup_and_update_parms({
        "steplib": {"data_sets": data_sets, "top_data_sets": top_data_sets}})
    concat_libs = module._concat_libraries("steplib")
    assert concat_libs == top_data_sets + data_sets


def test_concat_libraries_only_first_provided():
    prepare_for_exit()
    top_data_sets = ["FIRST.TOP.LIB", "SECOND.TOP.LIB"]
    module = setup_and_update_parms({
        "steplib": {"data_sets": None, "top_data_sets": top_data_sets}})
    concat_libs = module._concat_libraries("steplib")
    assert concat_libs == top_data_sets


def test_concat_libraries_only_second_provided():
    prepare_for_exit()
    data_sets = ["FIRST.LIB", "SECOND.LIB"]
    module = setup_and_update_parms({
        "steplib": {"data_sets": data_sets, "top_data_sets": None}})
    concat_libs = module._concat_libraries("steplib")
    assert concat_libs == data_sets


def test_concat_libraries_none_provided():
    module = setup_and_update_parms({
        "steplib": {"data_sets": None, "top_data_sets": None}})
    concat_libs = module._concat_libraries("steplib")
    assert concat_libs == []


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_copy_libraries_to_steplib_and_dfhrpl():
    module = setup_and_update_parms({
        "region_data_sets": {
            'dfhauxt': {DSN: "TEST.CICSPY1.RDEV.DFHAUXT"},
            'dfhbuxt': {DSN: "TEST.CICSPY1.RDEV.DFHBUXT"},
            'dfhcsd': {DSN: "TEST.CICSPY1.RDEV.DFHCSD"},
            'dfhgcd': {DSN: "TEST.CICSPY1.RDEV.DFHGCD"},
            'dfhintra': {DSN: "TEST.CICSPY1.RDEV.DFHINTRA"},
            'dfhlcd': {DSN: "TEST.CICSPY1.RDEV.DFHLCD"},
            'dfhlrq': {DSN: "TEST.CICSPY1.RDEV.DFHLRQ"},
            'dfhtemp': {DSN: "TEST.CICSPY1.RDEV.DFHTEMP"},
            'dfhdmpa': {DSN: "TEST.CICSPY1.RDEV.DFHDMPA"},
            'dfhdmpb': {DSN: "TEST.CICSPY1.RDEV.DFHDMPB"},
            "dfhstart": {DSN: DS_NAME}
        },
        "cics_data_sets": {
            "sdfhload": "TEST.CICS.SDFHLOAD",
            "sdfhauth": "TEST.CICS.SDFHAUTH",
            "sdfhlic": "TEST.CICS.SDFHLIC",
            "template": "TEST.CICS.<< lib_name >>"
        },
        "le_data_sets": {
            "sceecics": "TEST.LE.SCEECICS",
            "sceerun": "TEST.LE.SCEERUN",
            "sceerun2": "TEST.LE.SCEERUN2",
            "template": "TEST.LE.<< lib_name >>"
        },
        "cpsm_data_sets": {
            "seyuauth": "TEST.CPSM.SEYUAUTH",
            "seyuload": "TEST.CPSM.SEYULOAD",
            "template": "TEST.CPSM.<< lib_name >>"
        },
        "steplib": {
            "top_data_sets": []
        },
        "dfhrpl": {
            "top_data_sets": []
        }
    })
    module._copy_libraries_to_steplib_and_dfhrpl()

    assert module._module.params["steplib"] == {
        "top_data_sets": [
            "TEST.CICS.SDFHAUTH",
            "TEST.CICS.SDFHLIC",
            "TEST.CPSM.SEYUAUTH",
            "TEST.LE.SCEERUN",
            "TEST.LE.SCEERUN2"
        ]
    }
    assert module._module.params["dfhrpl"] == {
        "top_data_sets": [
            "TEST.CICS.SDFHLOAD",
            "TEST.CPSM.SEYULOAD",
            "TEST.LE.SCEECICS",
            "TEST.LE.SCEERUN",
            "TEST.LE.SCEERUN2"
        ]
    }


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test__populate_dds():
    module = setup_and_update_parms({
        "region_data_sets": {
            'dfhauxt': {DSN: "test.dfhauxt"},
            'dfhbuxt': {DSN: "test.dfhbuxt"},
            'dfhcsd': {DSN: "test.dfhcsd"},
            'dfhgcd': {DSN: "test.dfhgcd"},
            'dfhintra': {DSN: "test.dfhintra"},
            'dfhlcd': {DSN: "test.dfhlcd"},
            'dfhlrq': {DSN: "test.dfhlrq"},
            'dfhtemp': {DSN: "test.dfhtemp"},
            'dfhdmpa': {DSN: "test.dfhdmpa"},
            'dfhdmpb': {DSN: "test.dfhdmpb"},
            "dfhstart": {DSN: DS_NAME}
        },
        "cics_data_sets": {
            "sdfhload": "test.sdfhload",
            "sdfhauth": "test.sdfhauth",
            "sdfhlic": "test.sdfhlic",
        },
        "le_data_sets": {
            "sceecics": "test.sceecics",
            "sceerun": "test.sceerun",
            "sceerun2": "test.sceerun2",
        },
        "cpsm_data_sets": {
            "seyuauth": "test.seyuauth",
            "seyuload": "test.seyuload",
        },
        "steplib": {
            "top_data_sets": ["some.top.lib"]
        },
        "dfhrpl": {
            "top_data_sets": ["another.top.lib"]
        }
    })
    dds = module._populate_dds()

    expected_dds = [
        {
            "steplib": [
                {"disp": "SHR", "dsn": "SOME.TOP.LIB"},
                {"disp": "SHR", "dsn": "TEST.SDFHAUTH"},
                {"disp": "SHR", "dsn": "TEST.SDFHLIC"},
                {"disp": "SHR", "dsn": "TEST.SEYUAUTH"},
                {"disp": "SHR", "dsn": "TEST.SCEERUN"},
                {"disp": "SHR", "dsn": "TEST.SCEERUN2"},
            ]
        },
        {
            "dfhrpl": [
                {"disp": "SHR", "dsn": "ANOTHER.TOP.LIB"},
                {"disp": "SHR", "dsn": "TEST.SDFHLOAD"},
                {"disp": "SHR", "dsn": "TEST.SEYULOAD"},
                {"disp": "SHR", "dsn": "TEST.SCEECICS"},
                {"disp": "SHR", "dsn": "TEST.SCEERUN"},
                {"disp": "SHR", "dsn": "TEST.SCEERUN2"},
            ]
        },
        {"dfhauxt": [{"disp": "SHR", "dsn": "TEST.DFHAUXT"}]},
        {"dfhbuxt": [{"disp": "SHR", "dsn": "TEST.DFHBUXT"}]},
        {"dfhcsd": [{"disp": "SHR", "dsn": "TEST.DFHCSD"}]},
        {"dfhgcd": [{"disp": "SHR", "dsn": "TEST.DFHGCD"}]},
        {"dfhintra": [{"disp": "SHR", "dsn": "TEST.DFHINTRA"}]},
        {"dfhlcd": [{"disp": "SHR", "dsn": "TEST.DFHLCD"}]},
        {"dfhlrq": [{"disp": "SHR", "dsn": "TEST.DFHLRQ"}]},
        {"dfhtemp": [{"disp": "SHR", "dsn": "TEST.DFHTEMP"}]},
        {"dfhdmpa": [{"disp": "SHR", "dsn": "TEST.DFHDMPA"}]},
        {"dfhdmpb": [{"disp": "SHR", "dsn": "TEST.DFHDMPB"}]},
        {"ceemsg": [{"sysout": "*"}]},
        {"ceeout": [{"sysout": "*"}]},
        {"msgusr": [{"sysout": "*"}]},
        {"sysprint": [{"sysout": "*"}]},
        {"sysudump": [{"sysout": "*"}]},
        {"sysabend": [{"sysout": "*"}]},
        {"sysout": [{"sysout": "*"}]},
        {"dfhcxrf": [{"sysout": "*"}]},
        {"logusr": [{"sysout": "*"}]},
    ]

    assert dds == expected_dds


def test_validate_parameters_job_name_too_long():
    prepare_for_fail()
    job_name = "TOOOOLONGGGJOB"
    with pytest.raises(AnsibleFailJson) as exec_info:
        module = setup_and_update_parms({"job_parameters": {"job_name": job_name}})
        assert module.result["failed"]
    assert exec_info.value.args[0]['msg'] == 'Invalid argument "{0}" for type "qualifier".'.format(job_name)


def test_validate_parameters_job_name():
    prepare_for_exit()
    job_name = "STRTJOB"
    module = setup_and_update_parms({"job_parameters": {"job_name": job_name}})
    module.validate_parameters()
    module._exit()
    assert not module.result["failed"]


def test_validate_parameters_ds_too_long():
    prepare_for_fail()
    data_set_name = "TOOOOLONGG.DATA"
    with pytest.raises(AnsibleFailJson) as exec_info:
        module = setup_and_update_parms({"cics_data_sets": {"sdfhauth": data_set_name}})
        assert module.result["failed"]
    assert exec_info.value.args[0]['msg'] == 'Invalid argument "{0}" for type "data_set_base".'.format(data_set_name)


def test_validate_parameters_ds():
    prepare_for_exit()
    data_set_name = "DATASET.DATA"
    module = setup_and_update_parms({"cics_data_sets": {"sdfhauth": data_set_name}})
    module.validate_parameters()
    module._exit()
    assert not module.result["failed"]


def test_validate_parameters_applid_too_long():
    prepare_for_fail()
    applid = "APPLIDTOOLONG"
    with pytest.raises(AnsibleFailJson) as exec_info:
        module = setup_and_update_parms({"applid": applid})
        assert module.result["failed"]
    assert exec_info.value.args[0]['msg'] == 'Invalid argument "{0}" for type "qualifier".'.format(applid)


def test_validate_parameters_steplib_library_too_long():
    prepare_for_fail()
    steplib = "LIB.TOOO.LONGQUALIFIER"
    with pytest.raises(AnsibleFailJson) as exec_info:
        module = setup_and_update_parms({"steplib": {"top_data_sets": [steplib]}})
        assert module.result["failed"]
    assert exec_info.value.args[0]['msg'] == 'Invalid argument "{0}" for type "data_set_base".'.format(steplib)


def test_validate_parameters_region_ds_too_long():
    prepare_for_fail()
    region_ds = "LIB.TOOO.LONGQUALIFIER"
    with pytest.raises(AnsibleFailJson) as exec_info:
        module = setup_and_update_parms({"region_data_sets": {"dfhcsd": {"dsn": region_ds}}})
        assert module.result["failed"]
    assert exec_info.value.args[0]['msg'] == 'Invalid argument "{0}" for type "data_set_base".'.format(region_ds)


def test_wrap_sit_parameters_no_wrapping():
    content = ["USSHOME=HOMEDIR", "START=INITIAL", "APPLID=ABC123"]
    wrapped_content = StartCICSModule._wrap_sit_parameters(content)
    assert wrapped_content == content


def test_wrap_sit_parameters_no_equals():
    content = ["USSHOME=HOMEDIR", "HELLO", "APPLID=ABC123"]
    wrapped_content = StartCICSModule._wrap_sit_parameters(content)
    assert wrapped_content == content


def test_wrap_sit_parameters_wrapping_two_parms():
    content = ["USSHOME=LONGHOMEDIRECTORYLONGERTHAN80CHARACTERSNEEDSTOBEWRAPPEDBYTHEWRAPPINGMETHOD",
               "START=INITIAL",
               "GMTEXT='GOOD MORNING USER, WELCOME TO YOUR CICS REGION. THIS IS A LONG MESSAGE FOR TEST.'",
               "APPLID=ABC123"]
    wrapped_content = StartCICSModule._wrap_sit_parameters(content)

    assert wrapped_content == ["USSHOME=LONGHOMEDIRECTORYLONGERTHAN80CHARACTERSNEEDSTOBEWRAPPEDBYTHEWRAPPINGMETH",
                               "OD",
                               "START=INITIAL",
                               "GMTEXT='GOOD MORNING USER, WELCOME TO YOUR CICS REGION. THIS IS A LONG MESSAGE F",
                               "OR TEST.'",
                               "APPLID=ABC123"]


def test_wrap_sit_parameters_wrapping_one_parm():
    content = ["USSHOME=LONGHOMEDIRECTORYLONGERTHAN80CHARACTERSNEEDSTOBEWRAPPEDBYTHEWRAPPINGMETHOD",
               "START=INITIAL",
               "APPLID=ABC123"]
    wrapped_content = StartCICSModule._wrap_sit_parameters(content)

    assert wrapped_content == ["USSHOME=LONGHOMEDIRECTORYLONGERTHAN80CHARACTERSNEEDSTOBEWRAPPEDBYTHEWRAPPINGMETH",
                               "OD",
                               "START=INITIAL",
                               "APPLID=ABC123"]


def test_find_sit_parm_key():
    sit_parm = "GMTEXT='HELLO"
    key = StartCICSModule._find_sit_parm_key(sit_parm)
    assert key == "GMTEXT"


def test_find_sit_parm_key_two_equals():
    sit_parm = "GMTEXT='HELLO=HOWAREYOU'"
    key = StartCICSModule._find_sit_parm_key(sit_parm)
    assert key == "GMTEXT"


def test_find_sit_parm_key_not_present():
    sit_parm = "HELLO"
    key = StartCICSModule._find_sit_parm_key(sit_parm)
    assert key is None


def test_calculate_size_parameters_with_overrides():
    module = setup_and_update_parms({
        "space_primary": 10,
        "space_secondary": 5,
        "space_type": "CYL"
    })

    assert module.unit == "CYL"
    assert module.primary == 10
    assert module.primary_unit == ""
    assert module.secondary == 5
    assert module.secondary_unit == ""

    module.generate_jcl()
    module.calculate_size_parameters()

    assert module.unit == "CYL"
    assert module.primary_unit == "CYL"
    assert module.primary == 10
    assert module.secondary_unit == "CYL"
    assert module.secondary == 5


def test_calculate_size_parameters_no_overrides():
    module = setup_and_update_parms({})

    assert module.unit == "M"
    assert module.primary == 1
    assert module.primary_unit == ""
    assert module.secondary == 1
    assert module.secondary_unit == ""

    module.generate_jcl()
    module.calculate_size_parameters()

    assert module.unit == "M"
    assert module.primary_unit == "K"
    assert module.primary == 2
    assert module.secondary_unit == "K"
    assert module.secondary == 1


def test_calculate_size_parameters_primary_override_only():
    module = setup_and_update_parms({"space_primary": 10})

    assert module.unit == "M"
    assert module.primary == 10
    assert module.primary_unit == ""
    assert module.secondary == 1
    assert module.secondary_unit == ""

    module.generate_jcl()
    module.calculate_size_parameters()

    assert module.unit == "M"
    assert module.primary_unit == "M"
    assert module.primary == 10
    assert module.secondary_unit == "K"
    assert module.secondary == 1


def test_calculate_size_parameters_secondary_override_only():
    module = setup_and_update_parms({"space_secondary": 10})

    assert module.unit == "M"
    assert module.primary == 1
    assert module.primary_unit == ""
    assert module.secondary == 10
    assert module.secondary_unit == ""

    module.generate_jcl()
    module.calculate_size_parameters()

    assert module.unit == "M"
    assert module.primary_unit == "K"
    assert module.primary == 2
    assert module.secondary_unit == "M"
    assert module.secondary == 10


def test_calculate_size_parameters_primary_override_and_units_only():
    module = setup_and_update_parms({
        "space_primary": 10,
        "space_type": "CYL"
    })

    assert module.unit == "CYL"
    assert module.primary == 10
    assert module.primary_unit == ""
    assert module.secondary == 1
    assert module.secondary_unit == ""

    module.generate_jcl()
    module.calculate_size_parameters()

    assert module.unit == "CYL"
    assert module.primary_unit == "CYL"
    assert module.primary == 10
    assert module.secondary_unit == "K"
    assert module.secondary == 1


def test_calculate_size_parameters_primary_override_and_secondary_only():
    module = setup_and_update_parms({
        "space_primary": 10,
        "space_secondary": "5"
    })

    assert module.unit == "M"
    assert module.primary == 10
    assert module.primary_unit == ""
    assert module.secondary == 5
    assert module.secondary_unit == ""

    module.generate_jcl()
    module.calculate_size_parameters()

    assert module.unit == "M"
    assert module.primary_unit == "M"
    assert module.primary == 10
    assert module.secondary_unit == "M"
    assert module.secondary == 5


def test_calculate_size_parameters_secondary_override_and_units_only():
    module = setup_and_update_parms({
        "space_secondary": 10,
        "space_type": "CYL"
    })

    assert module.unit == "CYL"
    assert module.primary == 1
    assert module.primary_unit == ""
    assert module.secondary == 10
    assert module.secondary_unit == ""

    module.generate_jcl()
    module.calculate_size_parameters()

    assert module.unit == "CYL"
    assert module.primary_unit == "K"
    assert module.primary == 2
    assert module.secondary_unit == "CYL"
    assert module.secondary == 10


def test_calculate_size_parameters_units_override_only():
    module = setup_and_update_parms({
        "space_type": "CYL"
    })

    assert module.unit == "CYL"
    assert module.primary == 1
    assert module.primary_unit == ""
    assert module.secondary == 1
    assert module.secondary_unit == ""

    module.generate_jcl()
    module.calculate_size_parameters()

    assert module.unit == "CYL"
    assert module.primary_unit == "K"
    assert module.primary == 2
    assert module.secondary_unit == "K"
    assert module.secondary == 1


def test_initial_state():
    prepare_for_exit()
    region_jcl_module = setup_and_update_parms(get_sample_generated_JCL_args(DS_NAME, "initial"))

    _data_set_utils._execute_listds = MagicMock(
        side_effect=[
            MVSCmdResponse(8, LISTDS_data_set_doesnt_exist(DS_NAME), ""),
            MVSCmdResponse(0, LISTDS_data_set(DS_NAME, "PS"), ""),
        ]
    )

    _data_set_utils._execute_iefbr14 = MagicMock(
        return_value=MVSCmdResponse(
            rc=0, stdout="", stderr=IEFBR14_create_stderr(DS_NAME, "DFHSTART")
        )
    )

    DataSet.write = MagicMock()

    region_jcl_module.main()
    expected_result = dict(
        executions=[
            _execution(
                name=LISTDS_run_name(1),
                rc=8,
                stdout=LISTDS_data_set_doesnt_exist(DS_NAME),
                stderr="",
            ),
            _execution(
                name="IEFBR14 - dfhstart - Run 1",
                rc=0,
                stdout="",
                stderr=IEFBR14_create_stderr(DS_NAME, "DFHSTART")
            ),
            _execution(
                name="Copy JCL contents to data set",
                rc=0,
                stdout="",
                stderr=""
            ),
            _execution(
                name=LISTDS_run_name(1),
                rc=0,
                stdout=LISTDS_data_set(DS_NAME, "PS"),
                stderr="",
            ),
        ],
        start_state=dict(
            exists=False,
            data_set_organization="NONE"
        ),
        end_state=dict(
            exists=True,
            data_set_organization="Sequential"
        ),
        changed=True,
        failed=False,
        msg="",
        jcl=get_sample_generated_JCL()
    )
    assert region_jcl_module.get_result() == expected_result


def test_initial_state_pre_existing():
    prepare_for_exit()
    region_jcl_module = setup_and_update_parms(get_sample_generated_JCL_args(DS_NAME, "initial"))

    _data_set_utils._execute_listds = MagicMock(
        side_effect=[
            MVSCmdResponse(0, LISTDS_data_set(DS_NAME, "PS"), ""),
            MVSCmdResponse(8, LISTDS_data_set_doesnt_exist(DS_NAME), ""),
            MVSCmdResponse(0, LISTDS_data_set(DS_NAME, "PS"), ""),
        ]
    )
    _data_set_utils._execute_idcams = MagicMock(
        return_value=MVSCmdResponse(0, IDCAMS_delete(DS_NAME), "")
    )
    _data_set_utils._execute_iefbr14 = MagicMock(
        return_value=MVSCmdResponse(
            rc=0, stdout="", stderr=IEFBR14_create_stderr(DS_NAME, "DFHSTART")
        )
    )

    DataSet.write = MagicMock()

    region_jcl_module.main()
    expected_result = dict(
        executions=[
            _execution(
                name=LISTDS_run_name(1),
                rc=0,
                stdout=LISTDS_data_set(DS_NAME, "PS"),
                stderr="",
            ),
            _execution(
                name=IDCAMS_delete_run_name(1, DS_NAME),
                rc=0,
                stdout=IDCAMS_delete(DS_NAME),
                stderr=""
            ),
            _execution(
                name=LISTDS_run_name(1),
                rc=8,
                stdout=LISTDS_data_set_doesnt_exist(DS_NAME),
                stderr="",
            ),
            _execution(
                name="IEFBR14 - dfhstart - Run 1",
                rc=0,
                stdout="",
                stderr=IEFBR14_create_stderr(DS_NAME, "DFHSTART")
            ),
            _execution(
                name="Copy JCL contents to data set",
                rc=0,
                stdout="",
                stderr=""
            ),
            _execution(
                name=LISTDS_run_name(1),
                rc=0,
                stdout=LISTDS_data_set(DS_NAME, "PS"),
                stderr="",
            ),
        ],
        start_state=dict(
            exists=True,
            data_set_organization="Sequential"
        ),
        end_state=dict(
            exists=True,
            data_set_organization="Sequential"
        ),
        changed=True,
        failed=False,
        msg="",
        jcl=get_sample_generated_JCL()
    )
    assert region_jcl_module.get_result() == expected_result


def test_warm_state_match():
    prepare_for_exit()
    region_jcl_module = setup_and_update_parms(get_sample_generated_JCL_args(DS_NAME, "warm"))

    _data_set_utils._execute_listds = MagicMock(
        return_value=MVSCmdResponse(0, LISTDS_data_set(DS_NAME, "PS"), "")
    )
    _data_set_utils._execute_command = MagicMock(return_value=(0, get_sample_generated_JCL(), ""))

    region_jcl_module.main()
    expected_result = dict(
        executions=[
            _execution(
                name=LISTDS_run_name(1),
                rc=0,
                stdout=LISTDS_data_set(DS_NAME, "PS"),
                stderr="",
            ),
            _execution(
                name="Read data set {0}".format(DS_NAME),
                rc=0,
                stdout=get_sample_generated_JCL(),
                stderr=""
            ),
            _execution(
                name=LISTDS_run_name(1),
                rc=0,
                stdout=LISTDS_data_set(DS_NAME, "PS"),
                stderr="",
            ),
        ],
        start_state=dict(
            exists=True,
            data_set_organization="Sequential"
        ),
        end_state=dict(
            exists=True,
            data_set_organization="Sequential"
        ),
        changed=False,
        failed=False,
        msg="",
        jcl=get_sample_generated_JCL()
    )
    assert region_jcl_module.get_result() == expected_result


def test_warm_state_not_existing():
    prepare_for_fail()
    region_jcl_module = setup_and_update_parms(get_sample_generated_JCL_args(DS_NAME, "warm"))

    _data_set_utils._execute_listds = MagicMock(
        return_value=MVSCmdResponse(8, LISTDS_data_set_doesnt_exist(DS_NAME), ""),
    )

    expected_result = dict(
        executions=[
            _execution(
                name=LISTDS_run_name(1),
                rc=8,
                stdout=LISTDS_data_set_doesnt_exist(DS_NAME),
                stderr="",
            ),
        ],
        start_state=dict(
            exists=False,
            data_set_organization="NONE"
        ),
        end_state=dict(
            exists=False,
            data_set_organization="NONE"
        ),
        changed=False,
        failed=True,
        msg="Data set TEST.DATA.START does not exist.",
        jcl=""
    )
    with pytest.raises(AnsibleFailJson):
        region_jcl_module.main()

    assert region_jcl_module.get_result() == expected_result


def test_warm_state_non_match():
    prepare_for_fail()
    region_jcl_module = setup_and_update_parms(get_sample_generated_JCL_args(DS_NAME, "warm"))

    _data_set_utils._execute_listds = MagicMock(
        return_value=MVSCmdResponse(0, LISTDS_data_set(DS_NAME, "PS"), "")
    )
    _data_set_utils._execute_command = MagicMock(return_value=(0, "NON MATHCING JCL", ""))

    expected_result = dict(
        executions=[
            _execution(
                name=LISTDS_run_name(1),
                rc=0,
                stdout=LISTDS_data_set(DS_NAME, "PS"),
                stderr="",
            ),
            _execution(
                name="Read data set {0}".format(DS_NAME),
                rc=0,
                stdout="NON MATHCING JCL",
                stderr=""
            ),
        ],
        start_state=dict(
            exists=True,
            data_set_organization="Sequential"
        ),
        end_state=dict(
            exists=True,
            data_set_organization="Sequential"
        ),
        changed=False,
        failed=True,
        msg="Data set TEST.DATA.START does not contain the expected Region JCL.",
        jcl=get_sample_generated_JCL()
    )
    with pytest.raises(AnsibleFailJson):
        region_jcl_module.main()

    assert region_jcl_module.get_result() == expected_result


def test_absent_state_pre_existing():
    prepare_for_exit()
    region_jcl_module = setup_and_update_parms(get_sample_generated_JCL_args(DS_NAME, "absent"))

    _data_set_utils._execute_listds = MagicMock(
        side_effect=[
            MVSCmdResponse(0, LISTDS_data_set(DS_NAME, "PS"), ""),
            MVSCmdResponse(8, LISTDS_data_set_doesnt_exist(DS_NAME), ""),
        ]
    )
    _data_set_utils._execute_idcams = MagicMock(
        return_value=MVSCmdResponse(0, IDCAMS_delete(DS_NAME), "")
    )

    region_jcl_module.main()
    expected_result = dict(
        executions=[
            _execution(
                name=LISTDS_run_name(1),
                rc=0,
                stdout=LISTDS_data_set(DS_NAME, "PS"),
                stderr="",
            ),
            _execution(
                name=IDCAMS_delete_run_name(1, DS_NAME),
                rc=0,
                stdout=IDCAMS_delete(DS_NAME),
                stderr=""
            ),
            _execution(
                name=LISTDS_run_name(1),
                rc=8,
                stdout=LISTDS_data_set_doesnt_exist(DS_NAME),
                stderr="",
            ),
        ],
        start_state=dict(
            exists=True,
            data_set_organization="Sequential"
        ),
        end_state=dict(
            exists=False,
            data_set_organization="NONE"
        ),
        changed=True,
        failed=False,
        msg="",
        jcl=""
    )
    assert region_jcl_module.get_result() == expected_result


def test_absent_state_not_existing():
    prepare_for_exit()
    region_jcl_module = setup_and_update_parms(get_sample_generated_JCL_args(DS_NAME, "absent"))

    _data_set_utils._execute_listds = MagicMock(
        return_value=MVSCmdResponse(8, LISTDS_data_set_doesnt_exist(DS_NAME), ""),
    )
    _data_set_utils._execute_idcams = MagicMock(
        return_value=MVSCmdResponse(0, IDCAMS_delete(DS_NAME), "")
    )

    region_jcl_module.main()
    expected_result = dict(
        executions=[
            _execution(
                name=LISTDS_run_name(1),
                rc=8,
                stdout=LISTDS_data_set_doesnt_exist(DS_NAME),
                stderr="",
            ),
            _execution(
                name=LISTDS_run_name(1),
                rc=8,
                stdout=LISTDS_data_set_doesnt_exist(DS_NAME),
                stderr="",
            ),
        ],
        start_state=dict(
            exists=False,
            data_set_organization="NONE"
        ),
        end_state=dict(
            exists=False,
            data_set_organization="NONE"
        ),
        changed=False,
        failed=False,
        msg="",
        jcl=""
    )
    assert region_jcl_module.get_result() == expected_result
