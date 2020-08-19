# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import os
import sys
import warnings

import ansible.constants
import ansible.errors
import ansible.utils
import pytest

__metaclass__ = type


# Simple test examine set_auto_start.
def test_cics_dfhrmutl_examine_set_auto_start(ansible_zos_module):
    hosts = ansible_zos_module
    results = hosts.all.cics_dfhrmutl(steplib='CTS550.CICS720.SDFHLOAD', dfhgcd='BJMAXY.CICS.IYK3ZMX7.DFHGCD', set_auto_start=None)
    for result in results.contacted.values():
        assert result.get('rc') is 0
        assert result.get('changed') is True


# set_auto_start AUTOINIT
def test_cics_dfhrmutl_set_auto_start_AUTOINIT(ansible_zos_module):
    hosts = ansible_zos_module
    results = hosts.all.cics_dfhrmutl(steplib='CTS550.CICS720.SDFHLOAD', dfhgcd='BJMAXY.CICS.IYK3ZMX7.DFHGCD', set_auto_start='AUTOINIT')
    for result in results.contacted.values():
        assert result.get('rc') is 0
        assert result.get('changed') is True


# set_auto_start AUTODIAG
def test_cics_dfhrmutl_set_auto_start_AUTODIAG(ansible_zos_module):
    hosts = ansible_zos_module
    results = hosts.all.cics_dfhrmutl(steplib='CTS550.CICS720.SDFHLOAD', dfhgcd='BJMAXY.CICS.IYK3ZMX7.DFHGCD', set_auto_start='AUTODIAG')
    for result in results.contacted.values():
        assert result.get('rc') is 0
        assert result.get('changed') is True


# set_auto_start AUTOASIS
def test_cics_dfhrmutl_set_auto_start_AUTOASIS(ansible_zos_module):
    hosts = ansible_zos_module
    results = hosts.all.cics_dfhrmutl(steplib='CTS550.CICS720.SDFHLOAD', dfhgcd='BJMAXY.CICS.IYK3ZMX7.DFHGCD', set_auto_start='AUTOASIS')
    for result in results.contacted.values():
        assert result.get('rc') is 0
        assert result.get('changed') is True


# set_auto_start AUTOCOLD, and cold_copy to a new gcd.
def test_cics_dfhrmutl_set_auto_start_AUTOCOLD(ansible_zos_module):
    hosts = ansible_zos_module
    cold_copy_list = [{'newgcd': 'BJMAXY.CICS.IYK3ZMX7.NEWGCD'}]
    results = hosts.all.cics_dfhrmutl(steplib='CTS550.CICS720.SDFHLOAD', dfhgcd='BJMAXY.CICS.IYK3ZMX7.DFHGCD', set_auto_start='AUTOCOLD',
                                      cold_copy=cold_copy_list)
    for result in results.contacted.values():
        assert result.get('rc') is 0
        assert result.get('changed') is True


# Failure test set auto start to XXXXXXXX
def test_cics_dfhrmutl_failure_set_auto_start_XXXXXXXX(ansible_zos_module):
    hosts = ansible_zos_module
    results = hosts.all.cics_dfhrmutl(steplib='CTS550.CICS720.SDFHLOAD', dfhgcd='BJMAXY.CICS.IYK3ZMX7.DFHGCD', set_auto_start='XXXXXXXX')
    for result in results.contacted.values():
        assert result.get('changed') is False


# Failure test:"COLD_COPY is incompatible with the AUTOASIS and AUTODIAG options of SET_AUTO_START.
def test_cics_dfhrmutl_failure_set_auto_start_AUTOASIS_with_coldcopy(ansible_zos_module):
    hosts = ansible_zos_module
    cold_copy_list = [{'newgcd': 'BJMAXY.CICS.IYK3ZMX7.NEWGCD'}]
    results = hosts.all.cics_dfhrmutl(steplib='CTS550.CICS720.SDFHLOAD', dfhgcd='BJMAXY.CICS.IYK3ZMX7.DFHGCD', set_auto_start='AUTOASIS',
                                      cold_copy=cold_copy_list)
    for result in results.contacted.values():
        assert result.get('changed') is False
