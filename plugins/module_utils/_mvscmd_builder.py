# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

# FOR INTERNAL USE IN THE COLLECTION ONLY.

"""
MVS command builder for ZOAU mvscmd/mvscmdauth utilities.

Builds command-line invocations of mvscmd and mvscmdauth from DD statement
definitions, and handles temp dataset allocation and cleanup.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
import subprocess
from typing import List, Optional, Tuple

from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils._dd_statement import (
    DatasetDefinition, DDStatement, InputDefinition, OutputDefinition,
    StdinDefinition, StdoutDefinition)


def build_mvscmd_command(
    program,  # type: str
    dd_statements,  # type: List[DDStatement]
    authorized=False,  # type: bool
    verbose=False,  # type: bool
    debug=False  # type: bool
):
    # type: (...) -> Tuple[str, List[str]]
    """
    Build mvscmd or mvscmdauth command from DD statements.

    Args:
        program: Program name (IDCAMS, IKJEFT01, DFHRMUTL, etc.)
        dd_statements: List of DDStatement objects
        authorized: Use mvscmdauth if True, mvscmd if False
        verbose: Add -v flag for verbose output
        debug: Add -d flag for debug mode (retains temp datasets)

    Returns:
        Tuple of (command_string, list_of_temp_items_to_cleanup)

    Note:
        Temp items can be either dataset names (strings starting with uppercase)
        or Unix file paths (strings starting with '/')

    Example:
        >>> cmd, temps = build_mvscmd_command(
        ...     "IDCAMS",
        ...     [DDStatement('sysin', StdinDefinition("DELETE MY.DATASET")),
        ...      DDStatement('sysprint', StdoutDefinition())],
        ...     authorized=True
        ... )
        >>> # cmd = 'mvscmdauth --pgm=IDCAMS --sysin="DELETE MY.DATASET" --sysprint=* -j'
    """
    # Choose command based on authorization
    cmd_name = "mvscmdauth" if authorized else "mvscmd"

    # Start building command
    cmd_parts = [cmd_name, f"--pgm={program}"]

    # Track temporary datasets for cleanup
    temp_datasets = []

    # Process each DD statement
    for dd_stmt in dd_statements:
        dd_param, temp_ds = build_dd_parameter(dd_stmt)
        cmd_parts.append(dd_param)
        if temp_ds:
            temp_datasets.append(temp_ds)

    # Note: -j (JSON) flag removed due to ZOAU bug in JSON parsing
    # that causes memory errors with certain programs (DFHCSDUP, etc.)
    # Output will be parsed as text instead

    # Add optional flags
    if verbose:
        cmd_parts.append("-v")
    if debug:
        cmd_parts.append("-d")

    # Join into single command string
    command = " ".join(cmd_parts)

    return command, temp_datasets


def build_dd_parameter(dd_stmt):
    # type: (DDStatement) -> Tuple[str, Optional[str]]
    """
    Convert DDStatement to --ddname=value,options format.

    Args:
        dd_stmt: DDStatement object

    Returns:
        Tuple of (parameter_string, temp_dataset_name_or_none)

    Examples:
        SYSIN with content → --sysin="content"
        SYSPRINT capture → --sysprint=*
        Dataset allocation → --ddname=DATASET.NAME,SHR
        New dataset → --ddname=DATASET.NAME,new,lrecl=80,recfm=fb,blksize=3200
    """
    dd_name = dd_stmt.name.lower()
    definition = dd_stmt.definition
    temp_dataset = None

    # Handle StdinDefinition (inline content)
    # Mirrors zos_core: DataSet.create_temp() + DataSet.write() → temp MVS dataset
    if isinstance(definition, StdinDefinition):
        temp_dataset = create_temp_dataset_name()
        _write_to_dataset(temp_dataset, definition.content)
        return f'--{dd_name}={temp_dataset}', temp_dataset

    # Handle InputDefinition (inline content with optional dataset)
    elif isinstance(definition, InputDefinition):
        if definition.dataset:
            # Reference existing dataset
            return f'--{dd_name}={definition.dataset},SHR', None
        else:
            # Mirrors zos_core: DataSet.create_temp() + DataSet.write()
            temp_dataset = create_temp_dataset_name()
            _write_to_dataset(temp_dataset, definition.content)
            return f'--{dd_name}={temp_dataset}', temp_dataset

    # Handle StdoutDefinition (capture output)
    elif isinstance(definition, StdoutDefinition):
        if definition.return_content:
            # Use * to capture to stdout
            return f'--{dd_name}=*', None
        else:
            # Create temp dataset for output
            temp_dataset = create_temp_dataset_name()
            return f'--{dd_name}={temp_dataset},new', temp_dataset

    # Handle OutputDefinition (output with attributes)
    elif isinstance(definition, OutputDefinition):
        if definition.dataset:
            # Use specified dataset
            options = [definition.dataset]
            if definition.disposition:
                options.append(map_disposition(definition.disposition))
            if definition.record_length:
                options.append(f"lrecl={definition.record_length}")
            if definition.record_format:
                options.append(f"recfm={map_record_format(definition.record_format)}")
            if definition.block_size:
                options.append(f"blksize={definition.block_size}")
            return f'--{dd_name}={",".join(options)}', None
        else:
            # Create temp dataset
            temp_dataset = create_temp_dataset_name()
            options = [temp_dataset, "new"]
            if definition.record_length:
                options.append(f"lrecl={definition.record_length}")
            if definition.record_format:
                options.append(f"recfm={map_record_format(definition.record_format)}")
            if definition.block_size:
                options.append(f"blksize={definition.block_size}")
            return f'--{dd_name}={",".join(options)}', temp_dataset

    # Handle DatasetDefinition (dataset allocation)
    elif isinstance(definition, DatasetDefinition):
        if definition.dataset_name:
            # Reference existing dataset or allocate new one
            options = [definition.dataset_name]

            # Add disposition
            if definition.disposition:
                options.append(map_disposition(definition.disposition))
            else:
                # Default to SHR for existing datasets
                options.append("shr")

            # If NEW disposition, add allocation parameters
            if definition.disposition and definition.disposition.upper() == "NEW":
                if definition.record_length:
                    options.append(f"lrecl={definition.record_length}")
                if definition.record_format:
                    options.append(f"recfm={map_record_format(definition.record_format)}")
                if definition.block_size:
                    options.append(f"blksize={definition.block_size}")
                if definition.primary:
                    unit = map_space_unit(definition.primary_unit) if definition.primary_unit else "trk"
                    options.append(f"primary={definition.primary}{unit}")
                if definition.secondary:
                    unit = map_space_unit(definition.secondary_unit) if definition.secondary_unit else "trk"
                    options.append(f"secondary={definition.secondary}{unit}")
                if definition.directory_blocks:
                    options.append(f"dirblk={definition.directory_blocks}")
                if definition.volumes:
                    vol_list = ",".join(definition.volumes) if isinstance(definition.volumes, list) else definition.volumes
                    options.append(f"vol={vol_list}")
                if definition.storage_class:
                    options.append(f"storclas={definition.storage_class}")
                if definition.data_class:
                    options.append(f"dataclas={definition.data_class}")
                if definition.management_class:
                    options.append(f"mgmtclas={definition.management_class}")

            return f'--{dd_name}={",".join(options)}', None
        else:
            # No dataset name - use positional dataset reference
            # This is for cases like STEPLIB where only the dataset name is provided
            # as a positional argument to DatasetDefinition
            # Check if first positional arg was passed (common pattern in codebase)
            return f'--{dd_name}=*', None

    # Fallback - should not reach here
    return f'--{dd_name}=*', None


def create_temp_dataset_name():
    # type: () -> str
    """
    Create temporary dataset name using ZOAU mvstmp command.

    Returns:
        Temporary dataset name

    Note:
        Falls back to a simple pattern if mvstmp is not available.
    """
    try:
        result = subprocess.run(
            ["mvstmp"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    # Fallback: use USER environment variable for HLQ
    import random
    import string

    # Get USER from environment, fallback to 'ZOAU' if not set
    user = os.environ.get('USER', 'ZOAU').upper()[:8]  # Max 8 chars for HLQ

    # Generate random suffix
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    return f"{user}.TEMP.D{suffix}"


def map_disposition(disposition):
    # type: (str) -> str
    """
    Map zos_core disposition to mvscmd format.

    Args:
        disposition: Disposition string (NEW, OLD, SHR, MOD)

    Returns:
        Lowercase disposition for mvscmd
    """
    disp_map = {
        "NEW": "new",
        "OLD": "old",
        "SHR": "shr",
        "MOD": "mod",
        "EXCL": "excl"
    }
    return disp_map.get(disposition.upper(), disposition.lower())


def map_record_format(record_format):
    # type: (str) -> str
    """
    Map zos_core record format to mvscmd format.

    Args:
        record_format: Record format (FB, VB, U, FBA, VBA, FBS, VBS)

    Returns:
        Lowercase record format for mvscmd
    """
    # mvscmd accepts lowercase record formats
    return record_format.lower()


def map_space_unit(unit):
    # type: (str) -> str
    """
    Map zos_core space unit to mvscmd format.

    Args:
        unit: Space unit (TRK, CYL, K, M, G, REC)

    Returns:
        Lowercase unit suffix for mvscmd

    Note:
        mvscmd uses suffixes: k/kb, m/mb, g/gb, c/cyl, t/trk
        Avoid BLK suffix (only in ZOAU 1.4.0.0+)
    """
    unit_map = {
        "TRK": "trk",
        "CYL": "cyl",
        "K": "k",
        "KB": "k",
        "M": "m",
        "MB": "m",
        "G": "g",
        "GB": "g",
        "REC": "rec"
    }
    return unit_map.get(unit.upper(), unit.lower())


def _write_to_dataset(dataset_name, content):
    # type: (str, str) -> None
    """
    Allocate a temporary MVS dataset and write content into it.

    Mirrors zos_core's StdinDefinition approach:
      DataSet.create_temp(record_format="FB", record_length=80, space_primary=5, space_type="M")
      DataSet.write(name, content)

    Uses dtouch to allocate (FB, lrecl=80, 5 cylinders) then decho to write content.
    The dataset name must already be generated (e.g. via create_temp_dataset_name()).

    Args:
        dataset_name: MVS dataset name to allocate and write to
        content: String content to write

    Raises:
        Exception: If allocation or write fails
    """
    # Allocate the temp dataset using dtouch defaults: FB, lrecl=80, 100 tracks primary
    alloc_result = subprocess.run(
        ["dtouch", "-tseq", dataset_name],
        capture_output=True,
        text=True,
        timeout=30,
        check=False
    )
    if alloc_result.returncode != 0:
        raise Exception(
            "Failed to allocate temp dataset {0}: {1}".format(dataset_name, alloc_result.stderr)
        )

    # Only write content if non-empty. An empty dataset (zero records) is valid and
    # matches ZOAU DataSet.write(name, "") behaviour — programs like DFHRMUTL expect
    # SYSIN to be present but treat a zero-record dataset as having no commands.
    if content:
        escaped = content.replace("'", "'\\''")
        write_result = subprocess.run(
            "decho '{0}' '{1}'".format(escaped, dataset_name),
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
            check=False
        )
        if write_result.returncode != 0:
            # Clean up the allocated dataset before raising
            subprocess.run(
                ["drm", "-f", dataset_name],
                capture_output=True,
                timeout=10,
                check=False
            )
            raise Exception(
                "Failed to write to dataset {0}: {1}".format(dataset_name, write_result.stderr)
            )

# Made with Bob
