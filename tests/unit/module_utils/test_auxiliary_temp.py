# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function

__metaclass__ = type
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import auxiliary_temp
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import dataset_utils
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.data_set import CYLINDERS, MEGABYTES
from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.data_set_helper import PYTHON_LANGUAGE_FEATURES_MESSAGE
import pytest
import sys


@pytest.mark.skipif(
    sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE
)
def test_get_idcams_cmd_megabytes():
    dataset = dict(
        name="ANSI.CYLS.DFHTEMP",
        state="initial",
        exists=False,
        data_set_organization="NONE",
        unit=MEGABYTES,
        primary=auxiliary_temp.SPACE_PRIMARY_DEFAULT,
        secondary=auxiliary_temp.SPACE_SECONDARY_DEFAULT
    )
    idcams_cmd_intra = dataset_utils._build_idcams_define_cmd(
        auxiliary_temp._get_idcams_cmd_temp(dataset)
    )
    assert (
        idcams_cmd_intra
        == """
    DEFINE CLUSTER (NAME(ANSI.CYLS.DFHTEMP) -
    MEGABYTES(200 10) -
    RECORDSIZE(4089 4089) -
    NONINDEXED -
    CONTROLINTERVALSIZE(4096) -
    SHAREOPTIONS(2 3)) -
    DATA (NAME(ANSI.CYLS.DFHTEMP.DATA) -
    UNIQUE)
    """
    )


@pytest.mark.skipif(
    sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE
)
def test_get_idcams_cmd_cylinders():
    dataset = dict(
        name="ANSI.CYLS.DFHTEMP",
        state="initial",
        exists=False,
        data_set_organization="NONE",
        unit=CYLINDERS,
        primary=auxiliary_temp.SPACE_PRIMARY_DEFAULT,
        secondary=auxiliary_temp.SPACE_SECONDARY_DEFAULT
    )
    idcams_cmd_intra = dataset_utils._build_idcams_define_cmd(
        auxiliary_temp._get_idcams_cmd_temp(dataset)
    )
    assert (
        idcams_cmd_intra
        == """
    DEFINE CLUSTER (NAME(ANSI.CYLS.DFHTEMP) -
    CYLINDERS(200 10) -
    RECORDSIZE(4089 4089) -
    NONINDEXED -
    CONTROLINTERVALSIZE(4096) -
    SHAREOPTIONS(2 3)) -
    DATA (NAME(ANSI.CYLS.DFHTEMP.DATA) -
    UNIQUE)
    """
    )
