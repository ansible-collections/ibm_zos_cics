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


# Simple test initialise LCD
def test_cics_dfhccutl_initialise_LCD(ansible_zos_module):
    hosts = ansible_zos_module
    results = hosts.all.cics_dfhccutl(steplib='CTS550.CICS720.SDFHLOAD', dfhlcd='BJMAXY.CICS.IYK3ZMX7.DFHLCD')
    for result in results.contacted.values():
        assert result.get('rc') == 0
        assert result.get('changed') is True


# Failure test
def test_cics_dfhccutl_failure_no_existing_LCD(ansible_zos_module):
    hosts = ansible_zos_module
    results = hosts.all.cics_dfhccutl(steplib='CTS550.CICS720.SDFHLOAD', dfhlcd='BJMAXY.CICS.IYK3ZMX0.DFHLCD')
    for result in results.contacted.values():
        assert result.get('rc') != 0
        assert result.get('changed') is False
