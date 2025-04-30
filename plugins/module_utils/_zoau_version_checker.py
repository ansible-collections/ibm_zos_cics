# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2025
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

import traceback
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.import_handler import ZOAUImportError

try:
    from zoautil_py import ZOAU_API_VERSION
except Exception:
    # Use ibm_zos_core's approach to handling zoautil_py imports so sanity tests pass
    ZOAU_API_VERSION = ZOAUImportError(traceback.format_exc())


CURRENT_MINIMUM_LEVEL = "1.3.0.0"

IMPORT_ERROR_MESSAGE = f"Incompatible ZOAU API version found. Minimum supported version is v{CURRENT_MINIMUM_LEVEL}."


def _check_zoau_version():
    if isinstance(ZOAU_API_VERSION, str):
        zoau_version = list(map(int, ZOAU_API_VERSION.split('.')))
        min_version = list(map(int, CURRENT_MINIMUM_LEVEL.split('.')))
        if not _zoau_version_greater_than_min(zoau_version, min_version):
            raise ImportError(f"{IMPORT_ERROR_MESSAGE} Version found is {ZOAU_API_VERSION}")
    else:
        raise ImportError(IMPORT_ERROR_MESSAGE)


def _zoau_version_greater_than_min(zoau_version, min_version):  # type: (list[int],list[int]) -> bool
    for i in range(4):
        if zoau_version[i] > min_version[i]:
            return True
        elif min_version[i] > zoau_version[i]:
            return False

    # Version is equal to minimum
    return True
