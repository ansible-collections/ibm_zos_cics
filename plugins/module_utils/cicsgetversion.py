# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
try:
    import zoautil_py.datasets as Datasets
    import zoautil_py.exceptions as ZOAUExceptions
except ImportError as imp_exc:
    ZOAUTIL_IMPORT_ERROR = imp_exc
else:
    ZOAUTIL_IMPORT_ERROR = None


def get_dataset_member_version_record(dataset):  # type: (str) -> str
    try:
        result = Datasets.read("%s.SDFHSAMP(DFH0SINX)" % dataset).split("STATUS = ", 1)[1].split(" ")[0]
        if not result or result == "":
            raise Exception("CICS version was blank")
        elif len(result) >= 10:
            raise Exception("CICS version was too long")
        else:
            return result
    except ZOAUExceptions.ZOAUException:
        raise Exception("Error reading dataset for calculating CICS version.")
