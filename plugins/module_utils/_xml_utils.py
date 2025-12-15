# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2025
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import xml.etree.ElementTree as ET
from collections import OrderedDict
from typing import Any, Optional


def parse_xml(xml_string, namespaces=None, force_list=None):
    # type: (str, Optional[dict[str, Optional[str]]], Optional[tuple]) -> dict[str, Any]
    """
    Parse XML string into an OrderedDict structure similar to xmltodict.
    """
    if not xml_string:
        return OrderedDict()

    # Strip whitespace and remove XML declaration if present
    xml_string = xml_string.strip()
    if xml_string.startswith('<?xml'):
        decl_end = xml_string.find('?>')
        if decl_end != -1:
            xml_string = xml_string[decl_end + 2:].lstrip()

    # Parse the XML
    root = ET.fromstring(xml_string)

    # Build namespace and force_list sets
    ns_map = set(namespaces.keys()) if namespaces else set()
    force_list_set = set(force_list) if force_list else set()

    return _element_to_dict(root, ns_map, force_list_set)


def unparse_xml(data_dict):
    # type: (dict[str, Any]) -> str
    """
    Convert an OrderedDict structure to XML string.
    """
    if not data_dict:
        return ''

    # Get the root element name and data
    root_name = list(data_dict.keys())[0]
    root_data = data_dict[root_name]

    # Create root element
    root = _dict_to_element(root_name, root_data)

    # Convert to string
    xml_string = ET.tostring(root, encoding='unicode', method='xml', short_empty_elements=False)

    return xml_string


def _strip_namespace(tag, ns_map):
    # type: (str, set) -> str
    """Remove namespace from tag."""
    if tag.startswith('{'):
        # Extract namespace and local name
        ns_end = tag.find('}')
        namespace = tag[1:ns_end]
        local_name = tag[ns_end + 1:]

        # Check if we should strip this namespace
        # ns_map is a set of namespace URIs we want to strip
        if namespace in ns_map:
            return local_name

    return tag


def _element_to_dict(element, ns_map, force_list_set):
    # type: (ET.Element, set, set) -> OrderedDict
    """
    Convert an ElementTree element to an OrderedDict.
    Mimics xmltodict behavior with @ prefix for attributes.
    """
    result = OrderedDict()
    tag = _strip_namespace(element.tag, ns_map)

    # Process attributes (prefix with @), skip namespace declarations
    for key, value in element.attrib.items():
        if not (key.startswith('{http://www.w3.org/2000/xmlns/}') or key == 'xmlns'):
            attr_key = _strip_namespace(key, ns_map)
            result['@' + attr_key] = value

    # Process child elements
    children = list(element)

    if not children:
        # Leaf node - handle text content
        text = element.text.strip() if element.text else None
        if text:
            result['#text'] = text if result else None
            return OrderedDict([(tag, result if result else text)])
        return OrderedDict([(tag, result if result else None)])

    # Group children by tag name
    child_dict = OrderedDict()  # type: OrderedDict[str, list[OrderedDict]]
    for child in children:
        child_tag = _strip_namespace(child.tag, ns_map)
        child_data = _element_to_dict(child, ns_map, force_list_set)
        child_content = child_data[child_tag]

        if child_tag not in child_dict:
            child_dict[child_tag] = []
        child_dict[child_tag].append(child_content)

    # Add children to result - use list only for multiple children or forced
    for child_tag, child_list in child_dict.items():
        result[child_tag] = child_list if (len(child_list) > 1 or child_tag in force_list_set) else child_list[0]

    return OrderedDict([(tag, result)])


def _dict_to_element(tag, data):
    # type: (str, Any) -> ET.Element
    """
    Convert a dictionary to an ElementTree element.
    Handles @ prefix for attributes.
    """
    element = ET.Element(tag)

    if data is None:
        return element

    # Handle primitive types
    if isinstance(data, (str, int, float, bool)):
        element.text = str(data) if not isinstance(data, str) else data
        return element

    if isinstance(data, dict):
        for key, value in data.items():
            if key.startswith('@'):
                # Handle attributes
                attr_name = key[1:]
                if attr_name == 'xmlns' and isinstance(value, dict):
                    # Handle namespace declarations
                    for ns_prefix, ns_uri in value.items():
                        ns_attr = 'xmlns' if ns_prefix == '' else 'xmlns:' + ns_prefix
                        element.set(ns_attr, str(ns_uri))
                else:
                    element.set(attr_name, str(value))
            elif key == '#text':
                element.text = str(value)
            else:
                # Handle child elements (single or list)
                children = value if isinstance(value, list) else [value]
                for item in children:
                    element.append(_dict_to_element(key, item))
    return element
