# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
import traceback

ZOS_CORE_IMP_ERR = None
try:
    from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.dd_statement import StdoutDefinition, DatasetDefinition, DDStatement
    from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.zos_mvs_raw import MVSCmd
except ImportError:
    ZOS_CORE_IMP_ERR = traceback.format_exc()

ZOS_CICS_IMP_ERR = None
try:
    from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.response import (
        _execution)
except ImportError:
    ZOS_CICS_IMP_ERR = traceback.format_exc()


def _local_catalog(size, name, sdfhload, state, exists, vsam):
    return {
        'size': size,
        'name': name,
        'sdfhload': sdfhload,
        'state': state,
        'exists': exists,
        'vsam': vsam,
    }


def _get_ccmutl_dds(catalog):
    return [
        DDStatement('steplib', DatasetDefinition(catalog.sdfhload)),
        DDStatement('sysprint', StdoutDefinition()),
        DDStatement('sysudump', StdoutDefinition()),
        DDStatement(
            'dfhlcd',
            DatasetDefinition(
                dataset_name=catalog.name,
                disposition="SHR")),
    ]


def _run_dfhccutl(starting_catalog, cmd):
    executions = []
    dfhccutl_response = MVSCmd.execute(
        pgm="DFHCCUTL",
        dds=_get_ccmutl_dds(catalog=starting_catalog, cmd=cmd),
        verbose=True,
        debug=False)

    if dfhccutl_response.rc != 0:
        raise Exception(
            "DFHCCUTL failed with RC {0}".format(
                dfhccutl_response.rc
            )
        )
    executions.append(_execution(
        name="DFHCCUTL - Initialise Local Catalog",
        rc=dfhccutl_response.rc,
        stdout=dfhccutl_response.stdout,
        stderr=dfhccutl_response.stderr))

    return executions
