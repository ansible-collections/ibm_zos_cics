# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023,2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function

__metaclass__ = type
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import _auxiliary_temp as auxiliary_temp
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import _data_set_utils as data_set_utils
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils._data_set import CYLINDERS, MEGABYTES
from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.data_set_helper import PYTHON_LANGUAGE_FEATURES_MESSAGE
from ansible_collections.ibm.ibm_zos_cics.plugins.modules.auxiliary_temp import SPACE_PRIMARY_DEFAULT, SPACE_SECONDARY_DEFAULT
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
        primary=SPACE_PRIMARY_DEFAULT,
        secondary=SPACE_SECONDARY_DEFAULT
    )
    idcams_cmd_intra = data_set_utils._build_idcams_define_cmd(
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
        primary=SPACE_PRIMARY_DEFAULT,
        secondary=SPACE_SECONDARY_DEFAULT
    )
    idcams_cmd_intra = data_set_utils._build_idcams_define_cmd(
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


@pytest.mark.skipif(
    sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE
)
def test_get_idcams_cmd_volumes():
    dataset = dict(
        name="ANSI.CYLS.DFHTEMP",
        state="initial",
        exists=False,
        data_set_organization="NONE",
        unit=CYLINDERS,
        primary=SPACE_PRIMARY_DEFAULT,
        secondary=SPACE_SECONDARY_DEFAULT,
        volumes=["vserv1"]
    )
    idcams_cmd_intra = data_set_utils._build_idcams_define_cmd(
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
    SHAREOPTIONS(2 3) -
    VOLUMES(vserv1)) -
    DATA (NAME(ANSI.CYLS.DFHTEMP.DATA) -
    UNIQUE)
    """
    )


@pytest.mark.skipif(
    sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE
)
def test_get_idcams_cmd_multiple_volumes():
    dataset = dict(
        name="ANSI.CYLS.DFHTEMP",
        state="initial",
        exists=False,
        data_set_organization="NONE",
        unit=CYLINDERS,
        primary=SPACE_PRIMARY_DEFAULT,
        secondary=SPACE_SECONDARY_DEFAULT,
        volumes=["vserv1", "vserv2"]
    )
    idcams_cmd_intra = data_set_utils._build_idcams_define_cmd(
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
    SHAREOPTIONS(2 3) -
    VOLUMES(vserv1 vserv2)) -
    DATA (NAME(ANSI.CYLS.DFHTEMP.DATA) -
    UNIQUE)
    """
    )
