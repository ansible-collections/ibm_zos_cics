# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023,2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

# FOR INTERNAL USE IN THE COLLECTION ONLY.

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
import subprocess


def _execution(name, rc, stdout, stderr):  # type: (str, int, str, str) -> dict
    return {
        "name": name,
        "rc": rc,
        "stdout": stdout,
        "stderr": stderr,
    }


class MVSExecutionException(Exception):
    def __init__(self, message, executions):   # type: (str, list[dict]) -> None
        self.message = message
        self.executions = executions


class MVSCmdResponse:
    """Holds the result of an MVS program execution."""
    def __init__(self, rc, stdout, stderr):  # type: (int, str, str) -> None
        self.rc = rc
        self.stdout = stdout
        self.stderr = stderr


def _execute_subprocess(command):
    # type: (str) -> tuple
    """Execute a shell command and return (rc, stdout, stderr)."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=60,
            check=False
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 1, "", "Command timed out after 60 seconds"
    except Exception as e:
        return 1, "", "Command execution failed: {0}".format(str(e))


def _cleanup_temp_items(temp_items):
    # type: (list) -> None
    """Clean up temporary items: Unix paths via os.unlink, MVS datasets via drm."""
    for item in temp_items:
        if item.startswith('/'):
            try:
                os.unlink(item)
            except Exception:
                pass
        else:
            subprocess.run(
                "drm -f '{0}'".format(item),
                shell=True,
                capture_output=True,
                timeout=30,
                check=False
            )
