# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2025
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

import re
import subprocess

CURRENT_MINIMUM_LEVEL = "1.3.0.0"

IMPORT_ERROR_MESSAGE = "Incompatible ZOAU version found. Minimum supported version is v{0}.".format(CURRENT_MINIMUM_LEVEL)


def _get_zoau_version():
    # type: () -> str | None
    """Return the raw output of zoaversion, or None if the command is unavailable."""
    try:
        result = subprocess.run(
            ["zoaversion"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return None


def _check_zoau_version():
    raw = _get_zoau_version()
    if not raw:
        raise ImportError(IMPORT_ERROR_MESSAGE)
    try:
        _check_zoau_version_str(raw)
    except RuntimeError:
        raise ImportError(IMPORT_ERROR_MESSAGE)


def _check_zoau_version_str(zoau_version):
    # type: (str) -> None
    zoau_version_parsed = re.search(r'\d+(?:\.\d+)+', zoau_version)
    if zoau_version_parsed is not None:
        zoau_version = zoau_version_parsed.group()

    zoau_version_split = [int(x) for x in zoau_version.split('.')]
    min_zoau_version_split = [int(x) for x in CURRENT_MINIMUM_LEVEL.split('.')]

    if zoau_version_split < min_zoau_version_split:
        raise RuntimeError(
            "ZOAU version {0} does not meet the minimum requirement. "
            "Please upgrade to {1} or newer.".format(zoau_version, CURRENT_MINIMUM_LEVEL)
        )
