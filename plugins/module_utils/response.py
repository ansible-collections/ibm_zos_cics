# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from typing import Dict, List


def _execution(name, rc, stdout, stderr):  # type: (str, str, str, str) -> Dict
    return {
        "name": name,
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr,
    }


def _state(exists, **kwargs):  # type: (bool, Dict) -> Dict
    state = {
        "exists": exists
    }
    state.update(kwargs)
    return state


def _response(executions, start_state, end_state):  # type: (List, Dict, Dict) -> Dict
    return {
        "changed": False,
        "failed": False,
        "executions": executions,
        "start_state": start_state,
        "end_state": end_state,
    }
