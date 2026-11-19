# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

# FOR INTERNAL USE IN THE COLLECTION ONLY.

"""
Internal DD statement classes for MVS program execution.

Provides DatasetDefinition, StdinDefinition, StdoutDefinition, InputDefinition,
OutputDefinition, DDStatement and DataDefinition for use with mvscmd/mvscmdauth.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from typing import Any, List, Optional, Union


class DatasetDefinition:
    """
    Represents a dataset allocation for use with mvscmd/mvscmdauth DD statements.
    """

    def __init__(
        self,
        dataset_name=None,  # type: Optional[str]
        disposition=None,  # type: Optional[str]
        primary=None,  # type: Optional[int]
        secondary=None,  # type: Optional[int]
        primary_unit=None,  # type: Optional[str]
        secondary_unit=None,  # type: Optional[str]
        record_format=None,  # type: Optional[str]
        record_length=None,  # type: Optional[int]
        block_size=None,  # type: Optional[int]
        directory_blocks=None,  # type: Optional[int]
        type=None,  # type: Optional[str]
        volumes=None,  # type: Optional[Union[str, List[str]]]
        storage_class=None,  # type: Optional[str]
        data_class=None,  # type: Optional[str]
        management_class=None,  # type: Optional[str]
        normal_disposition=None,  # type: Optional[str]
        conditional_disposition=None,  # type: Optional[str]
        **kwargs  # type: Any
    ):
        # type: (...) -> None
        """
        Initialize a dataset definition.

        Args:
            dataset_name: Dataset name (e.g., 'MY.DATASET.NAME')
            disposition: Dataset disposition (NEW, OLD, SHR, MOD)
            primary: Primary space allocation
            secondary: Secondary space allocation
            primary_unit: Primary space unit (TRK, CYL, K, M, G, REC)
            secondary_unit: Secondary space unit (TRK, CYL, K, M, G, REC)
            record_format: Record format (FB, VB, U, FBA, VBA, FBS, VBS)
            record_length: Logical record length in bytes
            block_size: Block size in bytes
            directory_blocks: Number of directory blocks for PDS/PDSE
            type: Dataset type (SEQ, PDS, PDSE, LIBRARY, ESDS, KSDS, LDS, LARGE)
            volumes: Volume serial(s) - string or list of strings
            storage_class: SMS storage class
            data_class: SMS data class
            management_class: SMS management class
            normal_disposition: Normal disposition (CATALOG, DELETE, KEEP, UNCATALOG)
            conditional_disposition: Conditional disposition (CATALOG, DELETE, KEEP, UNCATALOG)
            **kwargs: Additional parameters for forward compatibility
        """
        self.dataset_name = dataset_name
        self.disposition = disposition
        self.primary = primary
        self.secondary = secondary
        self.primary_unit = primary_unit
        self.secondary_unit = secondary_unit
        self.record_format = record_format
        self.record_length = record_length
        self.block_size = block_size
        self.directory_blocks = directory_blocks
        self.type = type

        # Handle volumes as string or list
        if isinstance(volumes, str):
            self.volumes = [volumes]
        else:
            self.volumes = volumes

        self.storage_class = storage_class
        self.data_class = data_class
        self.management_class = management_class
        self.normal_disposition = normal_disposition
        self.conditional_disposition = conditional_disposition

        # Store any additional kwargs for forward compatibility
        self._extra_params = kwargs

    def __repr__(self):
        # type: () -> str
        """String representation for debugging."""
        return (
            f"DatasetDefinition(dataset_name={self.dataset_name!r}, "
            f"disposition={self.disposition!r}, "
            f"type={self.type!r})"
        )


class StdinDefinition:
    """
    Represents inline content for SYSIN DD statement.

    Represents inline content for a SYSIN DD statement.
    """

    def __init__(self, content=None):
        # type: (Optional[str]) -> None
        """
        Initialize a SYSIN definition with inline content.

        Args:
            content: String content to pass as input to the program
        """
        self.content = content if content is not None else ""

    def __repr__(self):
        # type: () -> str
        """String representation for debugging."""
        content_preview = self.content[:50] + "..." if len(self.content) > 50 else self.content
        return f"StdinDefinition(content={content_preview!r})"


class StdoutDefinition:
    """
    Represents output capture for a SYSPRINT DD statement.
    """

    def __init__(self, return_content=True):
        # type: (bool) -> None
        """
        Initialize a SYSPRINT definition for output capture.

        Args:
            return_content: Whether to capture and return the output (default: True)
        """
        self.return_content = return_content

    def __repr__(self):
        # type: () -> str
        """String representation for debugging."""
        return f"StdoutDefinition(return_content={self.return_content!r})"


class InputDefinition:
    """
    Represents input content with an optional dataset reference.
    """

    def __init__(self, content=None, dataset=None):
        # type: (Optional[str], Optional[str]) -> None
        """
        Initialize an input definition.

        Args:
            content: Input content string
            dataset: Optional dataset reference
        """
        self.content = content if content is not None else ""
        self.dataset = dataset

    def __repr__(self):
        # type: () -> str
        """String representation for debugging."""
        content_preview = self.content[:50] + "..." if len(self.content) > 50 else self.content
        return f"InputDefinition(content={content_preview!r}, dataset={self.dataset!r})"


class OutputDefinition:
    """
    Represents output with dataset attributes.
    """

    def __init__(
        self,
        dataset=None,  # type: Optional[str]
        disposition=None,  # type: Optional[str]
        record_format=None,  # type: Optional[str]
        record_length=None,  # type: Optional[int]
        block_size=None,  # type: Optional[int]
        **kwargs  # type: Any
    ):
        # type: (...) -> None
        """
        Initialize an output definition.

        Args:
            dataset: Dataset name
            disposition: Dataset disposition (NEW, OLD, SHR, MOD)
            record_format: Record format (FB, VB, U, etc.)
            record_length: Logical record length
            block_size: Block size
            **kwargs: Additional parameters for forward compatibility
        """
        self.dataset = dataset
        self.disposition = disposition
        self.record_format = record_format
        self.record_length = record_length
        self.block_size = block_size
        self._extra_params = kwargs

    def __repr__(self):
        # type: () -> str
        """String representation for debugging."""
        return (
            f"OutputDefinition(dataset={self.dataset!r}, "
            f"disposition={self.disposition!r})"
        )


class DDStatement:
    """
    Associates a DD name with its definition for use with mvscmd/mvscmdauth.
    """

    def __init__(self, name, definition):
        # type: (str, Union[DatasetDefinition, StdinDefinition, StdoutDefinition, InputDefinition, OutputDefinition]) -> None
        """
        Initialize a DD statement.

        Args:
            name: DD name (e.g., 'SYSIN', 'SYSPRINT', 'STEPLIB', 'DFHCSD')
            definition: One of the definition types (DatasetDefinition, StdinDefinition, etc.)
        """
        self.name = name.upper()  # DD names are always uppercase
        self.definition = definition

    def __repr__(self):
        # type: () -> str
        """String representation for debugging."""
        return f"DDStatement(name={self.name!r}, definition={self.definition!r})"

    @property
    def is_input(self):
        # type: () -> bool
        """Check if this is an input DD (SYSIN, SYSTSIN, etc.)."""
        return isinstance(self.definition, (StdinDefinition, InputDefinition))

    @property
    def is_output(self):
        # type: () -> bool
        """Check if this is an output DD (SYSPRINT, SYSTSPRT, etc.)."""
        return isinstance(self.definition, (StdoutDefinition, OutputDefinition))

    @property
    def is_dataset(self):
        # type: () -> bool
        """Check if this is a dataset DD."""
        return isinstance(self.definition, DatasetDefinition)


class DataDefinition:
    """
    Generic data definition for use with mvscmd/mvscmdauth.
    """

    def __init__(self, content=None, **kwargs):
        # type: (Optional[str], Any) -> None
        """
        Initialize a data definition.

        Args:
            content: Optional content string
            **kwargs: Additional parameters for forward compatibility
        """
        self.content = content if content is not None else ""
        self._extra_params = kwargs

    def __repr__(self):
        # type: () -> str
        """String representation for debugging."""
        return f"DataDefinition(content={self.content[:50]!r}...)"

# Made with Bob
