# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.ibm.ibm_zos_cics.plugins.modules import local_request_queue
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import dataset_utils
import pytest
import sys


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_get_idcams_cmd_cyl():
    dataset_size = dataset_utils._dataset_size(
        unit="CYL", primary=3, secondary=1)
    dataset = local_request_queue._local_request_queue(
        size=dataset_size,
        name="ANSI.CYLS.DFHLRQ",
        state="initial",
        exists=False,
        vsam=False)
    idcams_cmd_lcd = local_request_queue._get_idcams_cmd_lrq(dataset)
    assert idcams_cmd_lcd == '''
    DEFINE CLUSTER (NAME(ANSI.CYLS.DFHLRQ) -
    CYLINDERS(3 1) -
    RECORDSIZE(2232 2400) -
    INDEXED -
    KEYS(40 0) -
    FREESPACE(0 10) -
    SHAREOPTIONS(2 3) -
    REUSE -
    LOG(UNDO)) -
    DATA (NAME(ANSI.CYLS.DFHLRQ.DATA) -
    CONTROLINTERVALSIZE(2560)) -
    INDEX(NAME(ANSI.CYLS.DFHLRQ.INDEX))
    '''
