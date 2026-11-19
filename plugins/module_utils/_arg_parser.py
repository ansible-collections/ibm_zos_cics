# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

# FOR INTERNAL USE IN THE COLLECTION ONLY.

"""
Internal argument parser with z/OS-specific validation.

Provides BetterArgParser for validating z/OS-specific argument types including
dataset names, volume serials, and members.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re
from typing import Any, Dict, List


class BetterArgParser:
    """
    Argument parser with z/OS-specific validation.

    Validates z/OS-specific types including dataset names, volume serials,
    and member names using standard MVS naming convention regex patterns:
    - Dataset: ^(?:(?:[A-Z$#@]{1}[A-Z0-9$#@-]{0,7})(?:[.]{1})){1,21}[A-Z$#@]{1}[A-Z0-9$#@-]{0,7}$
    - Volume: ^[A-Z0-9@#$]{1,6}$
    - Member: ^[A-Z$#@]{1}[A-Z0-9$#@]{0,7}$
    """

    # MVS naming convention regex patterns
    DATASET_PATTERN = r"^(?:(?:[A-Z$#@]{1}[A-Z0-9$#@-]{0,7})(?:[.]{1})){1,21}[A-Z$#@]{1}[A-Z0-9$#@-]{0,7}$"
    VOLUME_PATTERN = r"^[A-Z0-9@#$]{1,6}$"
    MEMBER_PATTERN = r"^[A-Z$#@]{1}[A-Z0-9$#@]{0,7}$"

    def __init__(self, arg_defs):
        # type: (Dict[str, Any]) -> None
        """
        Initialize the argument parser with argument definitions.

        Args:
            arg_defs: Dictionary of argument definitions with validation rules
        """
        self.arg_defs = arg_defs
        self._dataset_regex = re.compile(self.DATASET_PATTERN)
        self._volume_regex = re.compile(self.VOLUME_PATTERN)
        self._member_regex = re.compile(self.MEMBER_PATTERN)

    def parse_args(self, params):
        # type: (Dict[str, Any]) -> Dict[str, Any]
        """
        Parse and validate arguments according to the argument definitions.

        Args:
            params: Dictionary of parameters to validate

        Returns:
            Validated parameters dictionary

        Raises:
            ValueError: If validation fails
        """
        validated = {}

        for arg_name, arg_def in self.arg_defs.items():
            value = params.get(arg_name)

            # Handle required arguments
            if arg_def.get("required", False) and value is None:
                raise ValueError(f"Missing required argument: {arg_name}")

            # Skip validation if value is None and not required
            if value is None:
                validated[arg_name] = value
                continue

            # Handle nested options (dict type with options)
            if arg_def.get("type") == "dict" and "options" in arg_def:
                validated[arg_name] = self._validate_dict_options(
                    arg_name, value, arg_def["options"]
                )
            # Handle custom arg_type validation
            elif "arg_type" in arg_def:
                validated[arg_name] = self._validate_arg_type(
                    arg_name, value, arg_def
                )
            # Handle standard type validation
            elif "type" in arg_def:
                validated[arg_name] = self._validate_type(
                    arg_name, value, arg_def
                )
            else:
                validated[arg_name] = value

        return validated

    def _validate_dict_options(self, arg_name, value, options):
        # type: (str, Dict[str, Any], Dict[str, Any]) -> Dict[str, Any]
        """Validate dictionary with nested options."""
        if not isinstance(value, dict):
            raise ValueError(f"Argument '{arg_name}' must be a dictionary")

        validated = {}
        for opt_name, opt_def in options.items():
            opt_value = value.get(opt_name)

            # Handle required nested options
            if opt_def.get("required", False) and opt_value is None:
                raise ValueError(
                    f"Missing required option '{opt_name}' in argument '{arg_name}'"
                )

            # Skip if None and not required
            if opt_value is None:
                validated[opt_name] = opt_value
                continue

            # Validate nested option
            if "arg_type" in opt_def:
                validated[opt_name] = self._validate_arg_type(
                    f"{arg_name}.{opt_name}", opt_value, opt_def
                )
            elif "type" in opt_def:
                validated[opt_name] = self._validate_type(
                    f"{arg_name}.{opt_name}", opt_value, opt_def
                )
            else:
                validated[opt_name] = opt_value

        # Include any extra keys not in options
        for key in value:
            if key not in validated:
                validated[key] = value[key]

        return validated

    def _validate_arg_type(self, arg_name, value, arg_def):
        # type: (str, Any, Dict[str, Any]) -> Any
        """Validate custom arg_type (z/OS-specific types)."""
        arg_type = arg_def["arg_type"]

        if arg_type == "data_set_base":
            return self._validate_dataset_base(arg_name, value)
        elif arg_type == "data_set_member":
            return self._validate_dataset_member(arg_name, value)
        elif arg_type == "volume":
            return self._validate_volume(arg_name, value)
        elif arg_type == "dd":
            return self._validate_dd(arg_name, value)
        elif arg_type == "list":
            return self._validate_list(arg_name, value, arg_def)
        elif arg_type == "dict":
            return self._validate_dict(arg_name, value)
        elif arg_type == "str":
            return self._validate_string(arg_name, value)
        elif arg_type == "int":
            return self._validate_int(arg_name, value)
        elif arg_type == "qualifier":
            return self._validate_qualifier(arg_name, value)
        elif arg_type == "bool":
            return self._validate_bool(arg_name, value)
        else:
            raise ValueError(f"Unknown arg_type '{arg_type}' for argument '{arg_name}'")

    def _validate_type(self, arg_name, value, arg_def):
        # type: (str, Any, Dict[str, Any]) -> Any
        """Validate standard type."""
        arg_type = arg_def["type"]

        if arg_type == "str":
            return self._validate_string(arg_name, value)
        elif arg_type == "int":
            return self._validate_int(arg_name, value)
        elif arg_type == "bool":
            return self._validate_bool(arg_name, value)
        elif arg_type == "list":
            return self._validate_list(arg_name, value, arg_def)
        elif arg_type == "dict":
            if "options" in arg_def:
                return self._validate_dict_options(arg_name, value, arg_def["options"])
            return self._validate_dict(arg_name, value)
        elif arg_type == "raw":
            # raw type accepts anything
            return value
        else:
            raise ValueError(f"Unknown type '{arg_type}' for argument '{arg_name}'")

    def _validate_dataset_base(self, arg_name, value):
        # type: (str, str) -> str
        """
        Validate dataset name without member.

        Uses MVS naming convention regex pattern.
        """
        if not isinstance(value, str):
            raise ValueError(f"Argument '{arg_name}' must be a string")

        # Convert to uppercase for validation
        value_upper = value.upper()

        # Check for member syntax (should not be present for data_set_base)
        if "(" in value_upper:
            raise ValueError(
                'Invalid argument "{0}" for type "data_set_base".'.format(value)
            )

        # Validate against dataset pattern
        if not self._dataset_regex.match(value_upper):
            raise ValueError(
                'Invalid argument "{0}" for type "data_set_base".'.format(value)
            )

        return value_upper

    def _validate_dataset_member(self, arg_name, value):
        # type: (str, str) -> str
        """
        Validate dataset name with optional member.

        Uses MVS naming convention regex pattern.
        """
        if not isinstance(value, str):
            raise ValueError(f"Argument '{arg_name}' must be a string")

        value_upper = value.upper()

        # Check if member syntax is present
        if "(" in value_upper:
            if not value_upper.endswith(")"):
                raise ValueError(
                    f"Argument '{arg_name}' has invalid member syntax: {value}. "
                    f"Member must be enclosed in parentheses: DATASET.NAME(MEMBER)"
                )

            # Split dataset and member
            parts = value_upper.split("(")
            if len(parts) != 2:
                raise ValueError(
                    f"Argument '{arg_name}' has invalid member syntax: {value}"
                )

            dataset = parts[0]
            member = parts[1].rstrip(")")

            # Validate dataset part
            if not self._dataset_regex.match(dataset):
                raise ValueError(
                    f"Argument '{arg_name}' has invalid dataset name: {dataset}"
                )

            # Validate member part
            if not self._member_regex.match(member):
                raise ValueError(
                    f"Argument '{arg_name}' has invalid member name: {member}. "
                    f"Member names must be 1-8 characters starting with A-Z, $, #, or @, "
                    f"followed by A-Z, 0-9, $, #, or @"
                )
        else:
            # No member, just validate dataset
            if not self._dataset_regex.match(value_upper):
                raise ValueError(
                    f"Argument '{arg_name}' is not a valid dataset name: {value}"
                )

        return value_upper

    def _validate_volume(self, arg_name, value):
        # type: (str, str) -> str
        """
        Validate volume serial.

        Uses MVS naming convention regex pattern.
        """
        if not isinstance(value, str):
            raise ValueError(f"Argument '{arg_name}' must be a string")

        value_upper = value.upper()

        if not self._volume_regex.match(value_upper):
            raise ValueError(
                f"Argument '{arg_name}' is not a valid volume serial: {value}. "
                f"Volume serials must be 1-6 characters containing A-Z, 0-9, @, #, or $"
            )

        return value_upper

    def _validate_qualifier(self, arg_name, value):
        # type: (str, str) -> str
        """
        Validate a JES job name qualifier (single segment, 1-8 chars).

        Must start with A-Z, $, #, or @, followed by A-Z, 0-9, $, #, @.
        """
        if not isinstance(value, str):
            raise ValueError(f"Argument '{arg_name}' must be a string")

        if not re.fullmatch(r"^[A-Z$#@][A-Z0-9@#$]{0,7}$", value, re.IGNORECASE):
            raise ValueError(
                'Invalid argument "{0}" for type "qualifier".'.format(value)
            )

        return value.upper()

    def _validate_dd(self, arg_name, value):
        # type: (str, str) -> str
        """
        Validate a DD name.

        1-8 characters, starting with A-Z, $, #, or @,
        followed by A-Z, 0-9, @, #, or $. Case-insensitive.
        """
        if not isinstance(value, str):
            raise ValueError(f"Argument '{arg_name}' must be a string")

        if not re.fullmatch(r"^[A-Z$#@][A-Z0-9@#$]{0,7}$", value, re.IGNORECASE):
            raise ValueError(
                'Invalid argument "{0}" for type "dd".'.format(value)
            )

        return value.upper()

    def _validate_list(self, arg_name, value, arg_def):
        # type: (str, Any, Dict[str, Any]) -> List[Any]
        """Validate list type with optional element validation."""
        if not isinstance(value, list):
            raise ValueError(f"Argument '{arg_name}' must be a list")

        # Validate elements if element type is specified
        if "elements" in arg_def:
            element_type = arg_def["elements"]
            validated_list = []

            for i, element in enumerate(value):
                if element_type == "volume":
                    validated_list.append(
                        self._validate_volume(f"{arg_name}[{i}]", element)
                    )
                elif element_type == "data_set_base":
                    validated_list.append(
                        self._validate_dataset_base(f"{arg_name}[{i}]", element)
                    )
                elif element_type == "data_set_member":
                    validated_list.append(
                        self._validate_dataset_member(f"{arg_name}[{i}]", element)
                    )
                elif element_type == "str":
                    validated_list.append(
                        self._validate_string(f"{arg_name}[{i}]", element)
                    )
                elif element_type == "int":
                    validated_list.append(
                        self._validate_int(f"{arg_name}[{i}]", element)
                    )
                else:
                    validated_list.append(element)

            return validated_list

        return value

    def _validate_dict(self, arg_name, value):
        # type: (str, Any) -> Dict[str, Any]
        """Validate dictionary type."""
        if not isinstance(value, dict):
            raise ValueError(f"Argument '{arg_name}' must be a dictionary")
        return value

    def _validate_string(self, arg_name, value):
        # type: (str, Any) -> str
        """Validate string type."""
        if not isinstance(value, str):
            raise ValueError(f"Argument '{arg_name}' must be a string")
        return value

    def _validate_int(self, arg_name, value):
        # type: (str, Any) -> int
        """Validate integer type."""
        if not isinstance(value, int):
            try:
                return int(value)
            except (ValueError, TypeError):
                raise ValueError(f"Argument '{arg_name}' must be an integer")
        return value

    def _validate_bool(self, arg_name, value):
        # type: (str, Any) -> bool
        """Validate boolean type."""
        if not isinstance(value, bool):
            # Try to convert string to bool
            if isinstance(value, str):
                if value.lower() in ("true", "yes", "1"):
                    return True
                elif value.lower() in ("false", "no", "0"):
                    return False
            raise ValueError(f"Argument '{arg_name}' must be a boolean")
        return value

# Made with Bob
