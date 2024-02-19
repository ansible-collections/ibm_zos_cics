# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import sys
import pytest
from ansible_collections.ibm.ibm_zos_cics.plugins.action.start_cics import ActionHelper
from ansible_collections.ibm.ibm_zos_cics.plugins.modules.start_cics import DSN
from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar


def setup_and_update_task_vars(key, value):
    loader = DataLoader()
    templar = Templar(loader=loader, variables={key: value})
    return ActionHelper({key: value}, {}, templar)


def setup():
    loader = DataLoader()
    templar = Templar(loader=loader, variables={})
    return ActionHelper({}, {}, templar)


def test_add_per_region_data_sets_with_only_template():
    helper = setup_and_update_task_vars(
        "region_data_sets", {"template": "TEST.CICSPY1.RDEV.<< data_set_name >>"})
    helper.add_per_region_data_sets()
    assert helper.module_args == {"region_data_sets": {'dfhauxt': {DSN: "TEST.CICSPY1.RDEV.DFHAUXT"},
                                                       'dfhbuxt': {DSN: "TEST.CICSPY1.RDEV.DFHBUXT"},
                                                       'dfhcsd': {DSN: "TEST.CICSPY1.RDEV.DFHCSD"},
                                                       'dfhgcd': {DSN: "TEST.CICSPY1.RDEV.DFHGCD"},
                                                       'dfhintra': {DSN: "TEST.CICSPY1.RDEV.DFHINTRA"},
                                                       'dfhlcd': {DSN: "TEST.CICSPY1.RDEV.DFHLCD"},
                                                       'dfhlrq': {DSN: "TEST.CICSPY1.RDEV.DFHLRQ"},
                                                       'dfhtemp': {DSN: "TEST.CICSPY1.RDEV.DFHTEMP"},
                                                       'dfhdmpa': {DSN: "TEST.CICSPY1.RDEV.DFHDMPA"},
                                                       'dfhdmpb': {DSN: "TEST.CICSPY1.RDEV.DFHDMPB"}}}
    assert helper.result['failed'] is False


def test_add_per_region_data_sets_with_default_disp():
    helper = setup_and_update_task_vars("region_data_sets", {"template": "TEST.CICSPY1.RDEV.<< data_set_name >>"})
    helper.add_per_region_data_sets()
    assert helper.module_args == {"region_data_sets": {'dfhauxt': {DSN: "TEST.CICSPY1.RDEV.DFHAUXT"},
                                                       'dfhbuxt': {DSN: "TEST.CICSPY1.RDEV.DFHBUXT"},
                                                       'dfhcsd': {DSN: "TEST.CICSPY1.RDEV.DFHCSD"},
                                                       'dfhgcd': {DSN: "TEST.CICSPY1.RDEV.DFHGCD"},
                                                       'dfhintra': {DSN: "TEST.CICSPY1.RDEV.DFHINTRA"},
                                                       'dfhlcd': {DSN: "TEST.CICSPY1.RDEV.DFHLCD"},
                                                       'dfhlrq': {DSN: "TEST.CICSPY1.RDEV.DFHLRQ"},
                                                       'dfhtemp': {DSN: "TEST.CICSPY1.RDEV.DFHTEMP"},
                                                       'dfhdmpa': {DSN: "TEST.CICSPY1.RDEV.DFHDMPA"},
                                                       'dfhdmpb': {DSN: "TEST.CICSPY1.RDEV.DFHDMPB"}}}


def test_add_per_region_data_sets_with_override():
    helper = setup_and_update_task_vars("region_data_sets", {"template": "TEST.CICSPY1.RDEV.<< data_set_name >>",
                                                             "dfhbuxt": {DSN: "TEST.OVERRIDE.BUXT"}})
    helper.add_per_region_data_sets()
    assert helper.module_args == {"region_data_sets": {'dfhauxt': {DSN: "TEST.CICSPY1.RDEV.DFHAUXT"},
                                                       'dfhbuxt': {DSN: "TEST.OVERRIDE.BUXT"},
                                                       'dfhcsd': {DSN: "TEST.CICSPY1.RDEV.DFHCSD"},
                                                       'dfhgcd': {DSN: "TEST.CICSPY1.RDEV.DFHGCD"},
                                                       'dfhintra': {DSN: "TEST.CICSPY1.RDEV.DFHINTRA"},
                                                       'dfhlcd': {DSN: "TEST.CICSPY1.RDEV.DFHLCD"},
                                                       'dfhlrq': {DSN: "TEST.CICSPY1.RDEV.DFHLRQ"},
                                                       'dfhtemp': {DSN: "TEST.CICSPY1.RDEV.DFHTEMP"},
                                                       'dfhdmpa': {DSN: "TEST.CICSPY1.RDEV.DFHDMPA"},
                                                       'dfhdmpb': {DSN: "TEST.CICSPY1.RDEV.DFHDMPB"}}}
    assert helper.result['failed'] is False


def test_add_per_region_data_sets_with_no_template_only_some_overrides_some_missing():
    helper = setup_and_update_task_vars("region_data_sets", {"dfhauxt": {DSN: "TEST.OVERRIDE.AUXT"},
                                                             "dfhbuxt": {DSN: "TEST.OVERRIDE.BUXT"},
                                                             "dfhcsd": {DSN: "OVERRIDE.TEST.DCSD"}})
    helper.add_per_region_data_sets()
    assert helper.module_args == {"region_data_sets": {'dfhauxt': {DSN: "TEST.OVERRIDE.AUXT"},
                                                       'dfhbuxt': {DSN: "TEST.OVERRIDE.BUXT"},
                                                       'dfhcsd': {DSN: "OVERRIDE.TEST.DCSD"}}}
    assert helper.result['failed'] is True
    assert helper.result['err'] == "Must provide either a template or data set name for data set: DFHGCD"


def test_add_per_region_data_sets_with_no_template_some_missing():
    helper = setup_and_update_task_vars("region_data_sets", {"dfhauxt": {DSN: "TEST.OVERRIDE.AUXT"},
                                                             "dfhbuxt": {DSN: "TEST.OVERRIDE.BUXT"}})

    helper.add_per_region_data_sets()
    assert helper.module_args == {"region_data_sets": {'dfhauxt': {DSN: "TEST.OVERRIDE.AUXT"},
                                                       'dfhbuxt': {DSN: "TEST.OVERRIDE.BUXT"}}}
    assert helper.result['failed'] is True
    assert helper.result['err'] == "Must provide either a template or data set name for data set: DFHCSD"


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_add_steplib_libraries_with_cics_data_sets():
    libraries = ["LIBONE", "LIBTWO"]
    top_libraries = ["TOPLIBONE", "TOPLIBTWO"]
    helper = setup_and_update_task_vars(
        "steplib", {"libraries": libraries, "top_libraries": top_libraries})
    helper.module_args["cics_data_sets"] = {
        "template": "TEST.ANTZ.CICS.<< lib_name >>"}
    helper.module_args["le_data_sets"] = {"template": "CEE.<< lib_name >>"}

    helper.add_steplib_libraries()
    assert helper.module_args["steplib"] == {"top_libraries": ["TOPLIBONE", "TOPLIBTWO", "TEST.ANTZ.CICS.SDFHAUTH",
                                             "TEST.ANTZ.CICS.SDFHLIC", "CEE.SCEERUN", "CEE.SCEERUN2"],
                                             "libraries": ["LIBONE", "LIBTWO"]}


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_add_steplib_libraries_with_template_and_override():
    libraries = ["LIBONE", "LIBTWO"]
    top_libraries = ["TOPLIBONE", "TOPLIBTWO"]
    helper = setup_and_update_task_vars(
        "steplib", {"libraries": libraries, "top_libraries": top_libraries})
    helper.module_args["cics_data_sets"] = {
        "template": "TEST.ANTZ.CICS.<< lib_name >>", "sdfhauth": "OVERRIDE.TEST"}
    helper.module_args["le_data_sets"] = {"template": "CEE.<< lib_name >>"}

    helper.add_steplib_libraries()
    assert helper.module_args["steplib"] == {"top_libraries": ["TOPLIBONE", "TOPLIBTWO", "OVERRIDE.TEST",
                                                               "TEST.ANTZ.CICS.SDFHLIC", "CEE.SCEERUN", "CEE.SCEERUN2"],
                                             "libraries": ["LIBONE", "LIBTWO"]}


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_add_steplib_libraries_with_overrides():
    libraries = ["LIBONE", "LIBTWO"]
    top_libraries = ["TOPLIBONE", "TOPLIBTWO"]
    helper = setup_and_update_task_vars(
        "steplib", {"libraries": libraries, "top_libraries": top_libraries})
    helper.module_args["cics_data_sets"] = {"template": "TEST.ANTZ.CICS.<< lib_name >>", "sdfhauth": "TEST.SDFH.AUTH"}
    helper.module_args["le_data_sets"] = {"template": "CEE.<< lib_name >>"}

    helper.add_steplib_libraries()
    assert helper.module_args["steplib"] == {"top_libraries": ["TOPLIBONE", "TOPLIBTWO", "TEST.SDFH.AUTH",
                                                               "TEST.ANTZ.CICS.SDFHLIC", "CEE.SCEERUN", "CEE.SCEERUN2"],
                                             "libraries": ["LIBONE", "LIBTWO"]}


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_add_steplib_libraries_with_missing_template():
    helper = setup_and_update_task_vars(
        "cics_data_sets", {"template": "TEST.ANTZ.CICS.<< lib_name >>"})
    helper.module_args["le_data_sets"] = {"sceerun": "TEST.SCEERUN"}
    helper.add_steplib_libraries()
    assert helper.module_args["steplib"] == {"top_libraries": ["TEST.ANTZ.CICS.SDFHAUTH", "TEST.ANTZ.CICS.SDFHLIC",
                                                               "TEST.SCEERUN"]}
    assert helper.result["failed"] is True
    assert helper.result["err"] == 'No template or data set name provided for: SCEERUN2'


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_add_dfhrpl_libraries():
    libraries = ["LIBONE", "LIBTWO"]
    top_libraries = ["TOPLIBONE", "TOPLIBTWO"]
    helper = setup_and_update_task_vars(
        "dfhrpl", {"libraries": libraries, "top_libraries": top_libraries})
    helper.module_args["cics_data_sets"] = {
        "template": "TEST.ANTZ.CICS.<< lib_name >>"}
    helper.module_args["le_data_sets"] = {"template": "CEE.<< lib_name >>"}

    helper.add_dfhrpl_libraries()
    assert helper.module_args["dfhrpl"] == {"top_libraries": ["TOPLIBONE", "TOPLIBTWO", "TEST.ANTZ.CICS.SDFHLOAD",
                                                              "CEE.SCEECICS", "CEE.SCEERUN",
                                                              "CEE.SCEERUN2"],
                                            "libraries": ["LIBONE", "LIBTWO"]}


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_add_dfhrpl_libraries_with_overrides():
    libraries = ["LIBONE", "LIBTWO"]
    top_libraries = ["TOPLIBONE", "TOPLIBTWO"]
    helper = setup_and_update_task_vars(
        "dfhrpl", {"libraries": libraries, "top_libraries": top_libraries})
    helper.module_args["cics_data_sets"] = {
        "template": "TEST.ANTZ.CICS.<< lib_name >>", "sdfhload": "TEST.SDFH.LOAD"}
    helper.module_args["le_data_sets"] = {"template": "CEE.<< lib_name >>"}
    helper.add_dfhrpl_libraries()
    assert helper.module_args["dfhrpl"] == {"top_libraries": ["TOPLIBONE", "TOPLIBTWO", "TEST.SDFH.LOAD",
                                                              "CEE.SCEECICS", "CEE.SCEERUN",
                                                              "CEE.SCEERUN2"],
                                            "libraries": ["LIBONE", "LIBTWO"]}


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_add_dfhrpl_libraries_with_missing_template():
    helper = setup_and_update_task_vars(
        "cics_data_sets", {"template": "TEST.ANTZ.CICS.<< lib_name >>"})
    helper.module_args["le_data_sets"] = {"sceerun": "TEST.SCEERUN"}

    helper.add_dfhrpl_libraries()
    assert helper.module_args["dfhrpl"] == {"top_libraries": ["TEST.ANTZ.CICS.SDFHLOAD", "TEST.SCEERUN"]}
    assert helper.result["failed"] is True
    assert helper.result["err"] == 'No template or data set name provided for: SCEECICS'


def test_get_dsn_no_template():
    helper = setup()
    datasets = {"dfhauxt": {DSN: "test.auxt"}}
    assert helper.get_dsn(datasets, "dfhauxt", None) == "TEST.AUXT"


def test_get_dsn_no_template_no_dsn():
    helper = setup()
    datasets = {"dfhauxt": {DSN: None}}
    assert helper.get_dsn(datasets, "dfhauxt", None) is None


def test_get_dsn_template_and_dsn_provided():
    helper = setup()
    datasets = {"dfhauxt": {DSN: "test.auxt"}}
    result = helper.get_dsn(datasets, "dfhauxt",
                            "TEST.DATA.<< dataset_name >>")
    assert result == "TEST.AUXT"


def test_get_dsn_template_and_no_dsn_provided():
    helper = setup()
    datasets = {"dfhauxt": {DSN: None}}
    assert helper.get_dsn(datasets, "dfhauxt", "TEST.DATA.<< data_set_name >>") == "TEST.DATA.DFHAUXT"


def test_fail():
    module = setup()
    assert module.result["failed"] is False
    expected_message = "Module failed for test"
    module._fail(expected_message)
    assert module.result["err"] == expected_message
    assert module.result["failed"]
