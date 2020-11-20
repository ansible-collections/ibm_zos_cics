# -*- coding: utf-8 -*-​
# Copyright (c) IBM Corporation 2019, 2020

from __future__ import absolute_import, division, print_function
from pprint import pprint

__metaclass__ = type
STEPLIB = "CTS540.CICS710.SDFHLOAD"
DFHCSD = "ZLBJLU.DTEST.DFHCSD"
SECCSD = "ZLBJLU.ATEST.DFHCSD"


def test01_dfhcsdup_command_initialize(ansible_zos_module):
    hosts = ansible_zos_module
    results = hosts.all.cics_dfhcsdup(
        steplib=STEPLIB,
        dfhcsd=DFHCSD,
        cmd_str=["initialize"],
    )
    pprint(vars(results))
    for result in results.contacted.values():
        assert result.get('parms') is not None
        assert result.get('ret_code') == 0
        assert result.get('content') is not None
        assert result.get('changed') is True


def test02_dfhcsdup_command_verify(ansible_zos_module):
    hosts = ansible_zos_module
    results = hosts.all.cics_dfhcsdup(
        steplib=STEPLIB,
        dfhcsd=DFHCSD,
        cmd_stmt=[{"verify": ""}]
    )
    pprint(vars(results))
    for result in results.contacted.values():
        assert result.get('ret_code') == 0
        assert result.get('content') is not None
        assert result.get('changed') is True


def test03_dfhcsdup_commands_verify_upgrade(ansible_zos_module):
    hosts = ansible_zos_module
    results = hosts.all.cics_dfhcsdup(
        steplib=STEPLIB,
        dfhcsd=DFHCSD,
        cmd_stmt=[{"verify": ""}, {"upgrade": ""}]
    )
    pprint(vars(results))
    for result in results.contacted.values():
        assert result.get('ret_code') == 0
        assert result.get('content') is not None
        assert result.get('changed') is True


def test04_dfhcsdup_commands_list(ansible_zos_module):
    hosts = ansible_zos_module
    results = hosts.all.cics_dfhcsdup(
        steplib=STEPLIB,
        dfhcsd=DFHCSD,
        cmd_stmt=[{"list": {"group_name": "dfh$acct", "objects": ""}}]
    )
    pprint(vars(results))
    for result in results.contacted.values():
        assert result.get('ret_code') == 0
        assert result.get('content') is not None
        assert result.get('changed') is True


def test05_dfhcsdup__commands_scan(ansible_zos_module):
    hosts = ansible_zos_module
    results = hosts.all.cics_dfhcsdup(
        steplib=STEPLIB,
        dfhcsd=DFHCSD,
        cmd_stmt=[{"scan":
                  {"resource_type": "transaction", "resource_name": "ceda"}}]
    )
    pprint(vars(results))
    for result in results.contacted.values():
        assert result.get('ret_code') == 0
        assert result.get('content') is not None
        assert result.get('changed') is True


# def test06_dfhcsdup__commands_define(ansible_zos_module):
#     hosts = ansible_zos_module
#     results = hosts.all.cics_dfhcsdup(
#         steplib=STEPLIB,
#         dfhcsd=DFHCSD,
#         cmd_stmt=[{"define":
#                  {"group_name": "grp01", "list_name": "lst01",
#                      "resource_type": "terminal", "resource_name": "test",
#                      "attr_list": {"consname": "consjcl",
#                                    "typeterm": "dfhcons",
#                                    "description":
#                                    "MVS CONSOLE FOR ISSUING JCL COMMANDS"}}}]
#     )
#     pprint(vars(results))
#     for result in results.contacted.values():
#         assert result.get('ret_code') <= 4
#         assert result.get('content') is not None
#         assert result.get('changed') is True


def test06_dfhcsdup__commands_define(ansible_zos_module):
    hosts = ansible_zos_module
    results = hosts.all.cics_dfhcsdup(
        steplib=STEPLIB,
        dfhcsd=DFHCSD,
        cmd_stmt=[{"define":
                  {"group_name": "grp01", "list_name": "lst01",
                      "resource_type": "program", "resource_name": "test",
                      "attr_list": {"resident": "yes"}}}]
    )
    pprint(vars(results))
    for result in results.contacted.values():
        assert result.get('ret_code') <= 4
        assert result.get('content') is not None
        assert result.get('changed') is True


def test07_dfhcsdup__commands_add(ansible_zos_module):
    hosts = ansible_zos_module
    results = hosts.all.cics_dfhcsdup(
        steplib=STEPLIB,
        dfhcsd=DFHCSD,
        cmd_stmt=[{"add":
                  {"group_name": "grp02", "list_name": "lst01"}}]
    )
    pprint(vars(results))
    for result in results.contacted.values():
        assert result.get('ret_code') <= 4
        assert result.get('content') is not None
        assert result.get('changed') is True


def test08_dfhcsdup__commands_remove(ansible_zos_module):
    hosts = ansible_zos_module
    results = hosts.all.cics_dfhcsdup(
        steplib=STEPLIB,
        dfhcsd=DFHCSD,
        cmd_stmt=[{"remove":
                  {"group_name": "grp02", "list_name": "lst01"}}]
    )
    pprint(vars(results))
    for result in results.contacted.values():
        assert result.get('ret_code') <= 4
        assert result.get('content') is not None
        assert result.get('changed') is True


def test09_dfhcsdup__commands_alter(ansible_zos_module):
    hosts = ansible_zos_module
    results = hosts.all.cics_dfhcsdup(
        steplib=STEPLIB,
        dfhcsd=DFHCSD,
        cmd_stmt=[{"alter":
                  {"group_name": "grp01", "list_name": "lst01",
                      "resource_type": "program", "resource_name": "test",
                      "attr_list": {"resident": "no"}}}]
    )
    pprint(vars(results))
    for result in results.contacted.values():
        assert result.get('ret_code') <= 4
        assert result.get('content') is not None
        assert result.get('changed') is True


def test10_dfhcsdup__commands_userdefine(ansible_zos_module):
    hosts = ansible_zos_module
    results = hosts.all.cics_dfhcsdup(
        steplib=STEPLIB,
        dfhcsd=DFHCSD,
        cmd_stmt=[{"user_define":
                  {"group_name": "grp01", "list_name": "lst01",
                   "resource_type": "program", "resource_name": "utest"}}]
    )
    pprint(vars(results))
    for result in results.contacted.values():
        assert result.get('ret_code') <= 4
        assert result.get('content') is not None
        assert result.get('changed') is True


def test11_dfhcsdup__commands_delete(ansible_zos_module):
    hosts = ansible_zos_module
    results = hosts.all.cics_dfhcsdup(
        steplib=STEPLIB,
        dfhcsd=DFHCSD,
        cmd_stmt=[{"delete":
                  {"group_name": "grp01",
                      "resource_type": "program", "resource_name": "test"}}]
    )
    pprint(vars(results))
    for result in results.contacted.values():
        assert result.get('ret_code') <= 4
        assert result.get('content') is not None
        assert result.get('changed') is True


def test00_dfhcsdup__commands_pretest(ansible_zos_module):
    hosts = ansible_zos_module
    results = hosts.all.cics_dfhcsdup(
        steplib=STEPLIB,
        dfhcsd=SECCSD,
        cmd_stmt=[{"define":
                  {"group_name": "grp01", "list_name": "lst01",
                   "resource_type": "program", "resource_name": "test1"}}]
    )
    pprint(vars(results))
    for result in results.contacted.values():
        assert result.get('ret_code') <= 4
        assert result.get('content') is not None
        assert result.get('changed') is True


def test12_dfhcsdup__commands_copy(ansible_zos_module):
    hosts = ansible_zos_module
    results = hosts.all.cics_dfhcsdup(
        steplib=STEPLIB,
        dfhcsd=DFHCSD,
        seccsd=SECCSD,
        cmd_stmt=[{"copy":
                  {"group_name": "grp01", "to": "grp01",
                      "replace": "yes", "fromcsd": "seccsd"}}]
    )
    pprint(vars(results))
    for result in results.contacted.values():
        assert result.get('ret_code') <= 4
        assert result.get('content') is not None
        assert result.get('changed') is True


def test13_dfhcsdup__commands_append(ansible_zos_module):
    hosts = ansible_zos_module
    results = hosts.all.cics_dfhcsdup(
        steplib=STEPLIB,
        dfhcsd=DFHCSD,
        seccsd=SECCSD,
        cmd_stmt=[{"append":
                  {"to": "lst01", "list_name": "lst01"}}]
    )
    pprint(vars(results))
    for result in results.contacted.values():
        assert result.get('ret_code') <= 4
        assert result.get('content') is not None
        assert result.get('changed') is True


def test14_dfhcsdup__commands_process(ansible_zos_module):
    hosts = ansible_zos_module
    results = hosts.all.cics_dfhcsdup(
        steplib=STEPLIB,
        dfhcsd=DFHCSD,
        cmd_stmt=[{"process":
                  {"apar": "test"}}]
    )
    pprint(vars(results))
    for result in results.contacted.values():
        assert result.get('ret_code') <= 4
        assert result.get('content') is not None
        assert result.get('changed') is True


def test15_dfhcsdup__commands_service(ansible_zos_module):
    hosts = ansible_zos_module
    results = hosts.all.cics_dfhcsdup(
        steplib=STEPLIB,
        dfhcsd=DFHCSD,
        cmd_stmt=[{"service":
                  {"level": "000"}}]
    )
    pprint(vars(results))
    for result in results.contacted.values():
        assert result.get('ret_code') <= 4
        assert result.get('content') is not None
        assert result.get('changed') is True


# def test16_dfhcsdup__commands_extract(ansible_zos_module):
#     hosts = ansible_zos_module
#     results = hosts.all.cics_dfhcsdup(
        # steplib=STEPLIB,
        # userprog_lib="cts540.cics710.sdfhauth",
        # userprog_dd="cbdout",
        # dfhcsd=DFHCSD,
        # cmd_stmt=[{"extract":
        #             {"group_name": "dfhtype", "userprogram": "dfh0cbdc",
        #                 "objects": "yes"}}]
#     )
#     pprint(vars(results))
#     for result in results.contacted.values():
#         assert result.get('ret_code') <= 4
#         assert result.get('content') is not None
#         assert result.get('changed') is True
