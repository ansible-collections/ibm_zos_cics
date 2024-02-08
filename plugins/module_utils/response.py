# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


def _execution(name, rc, stdout, stderr) -> dict:
    return {
        "name": name,
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr,
    }
