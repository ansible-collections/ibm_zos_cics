# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function

__metaclass__ = type
from ansible_collections.ibm.ibm_zos_cics.plugins.modules import intrapartition
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import dataset_utils
import pytest
import sys


@pytest.mark.skipif(
    sys.version_info.major < 3, reason="Requires python 3 language features"
)
def test_get_idcams_cmd_megabytes():
    dataset_size = dataset_utils._dataset_size(unit="M", primary=10, secondary=1)
    dataset = dataset_utils._data_set(
        size=dataset_size,
        name="ANSI.CYLS.DFHINTRA",
        state="initial",
        exists=False,
        vsam=False,
    )
    idcams_cmd_intra = dataset_utils._build_idcams_define_cmd(
        intrapartition._get_idcams_cmd_intra(dataset)
    )
    assert (
        idcams_cmd_intra
        == """
    DEFINE CLUSTER (NAME(ANSI.CYLS.DFHINTRA) -
    MEGABYTES(10 1) -
    RECORDSIZE(1529 1529) -
    NONINDEXED -
    CONTROLINTERVALSIZE(1536)) -
    DATA (NAME(ANSI.CYLS.DFHINTRA.DATA))
    """
    )


@pytest.mark.skipif(
    sys.version_info.major < 3, reason="Requires python 3 language features"
)
def test_get_idcams_cmd_cylinders():
    dataset_size = dataset_utils._dataset_size(unit="CYL", primary=3, secondary=1)
    dataset = dataset_utils._data_set(
        size=dataset_size,
        name="ANSI.CYLS.DFHINTRA",
        state="initial",
        exists=False,
        vsam=False,
    )
    idcams_cmd_intra = dataset_utils._build_idcams_define_cmd(
        intrapartition._get_idcams_cmd_intra(dataset)
    )
    assert (
        idcams_cmd_intra
        == """
    DEFINE CLUSTER (NAME(ANSI.CYLS.DFHINTRA) -
    CYLINDERS(3 1) -
    RECORDSIZE(1529 1529) -
    NONINDEXED -
    CONTROLINTERVALSIZE(1536)) -
    DATA (NAME(ANSI.CYLS.DFHINTRA.DATA))
    """
    )
