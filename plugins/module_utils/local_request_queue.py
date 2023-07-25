# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


def _local_request_queue(size, name, state, exists, vsam):
    return {
        'size': size,
        'name': name,
        'state': state,
        'exists': exists,
        'vsam': vsam,
    }
