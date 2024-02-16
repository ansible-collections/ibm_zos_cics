# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.data_set import CYLINDERS, MEGABYTES

from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.data_set_helper import PYTHON_LANGUAGE_FEATURES_MESSAGE
__metaclass__ = type
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import local_request_queue
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import dataset_utils
from ansible_collections.ibm.ibm_zos_cics.plugins.modules.local_request_queue import SPACE_PRIMARY_DEFAULT, SPACE_SECONDARY_DEFAULT
import pytest
import sys


@pytest.mark.skipif(sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE)
def test_get_idcams_cmd_megabytes():
    dataset = dict(
        name="ANSI.CYLS.DFHLRQ",
        state="initial",
        exists=False,
        data_set_organization="NONE",
        unit=MEGABYTES,
        primary=SPACE_PRIMARY_DEFAULT,
        secondary=SPACE_SECONDARY_DEFAULT
    )
    idcams_cmd_lrq = dataset_utils._build_idcams_define_cmd(local_request_queue._get_idcams_cmd_lrq(dataset))
    assert idcams_cmd_lrq == '''
    DEFINE CLUSTER (NAME(ANSI.CYLS.DFHLRQ) -
    MEGABYTES(4 1) -
    RECORDSIZE(2232 2400) -
    INDEXED -
    KEYS(40 0) -
    FREESPACE(0 10) -
    SHAREOPTIONS(2 3) -
    REUSE -
    LOG(UNDO)) -
    DATA (NAME(ANSI.CYLS.DFHLRQ.DATA) -
    CONTROLINTERVALSIZE(2560)) -
    INDEX (NAME(ANSI.CYLS.DFHLRQ.INDEX))
    '''


@pytest.mark.skipif(sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE)
def test_get_idcams_cmd_cylinders():
    dataset = dict(
        name="ANSI.CYLS.DFHLRQ",
        state="initial",
        exists=False,
        data_set_organization="NONE",
        unit=CYLINDERS,
        primary=SPACE_PRIMARY_DEFAULT,
        secondary=SPACE_SECONDARY_DEFAULT
    )
    idcams_cmd_lrq = dataset_utils._build_idcams_define_cmd(local_request_queue._get_idcams_cmd_lrq(dataset))
    assert idcams_cmd_lrq == '''
    DEFINE CLUSTER (NAME(ANSI.CYLS.DFHLRQ) -
    CYLINDERS(4 1) -
    RECORDSIZE(2232 2400) -
    INDEXED -
    KEYS(40 0) -
    FREESPACE(0 10) -
    SHAREOPTIONS(2 3) -
    REUSE -
    LOG(UNDO)) -
    DATA (NAME(ANSI.CYLS.DFHLRQ.DATA) -
    CONTROLINTERVALSIZE(2560)) -
    INDEX (NAME(ANSI.CYLS.DFHLRQ.INDEX))
    '''
