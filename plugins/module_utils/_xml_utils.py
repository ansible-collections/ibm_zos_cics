# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2025
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import xml.etree.ElementTree as ET
from collections import OrderedDict
from typing import Any, Iterable, Optional


def parse_xml(xml_string, strip_namespaces=None, force_list=None):
    # type: (str, Optional[Iterable[str]], Optional[Iterable[str]]) -> dict[str, Any]
    """
    Parse an XML string into an OrderedDict structure, using the same layout
    as xmltodict: attributes are prefixed with @, text alongside attributes is
    stored under #text, and repeated children become lists.

    strip_namespaces: namespace URIs whose prefix is removed from tag and
        attribute names.
    force_list: tag names that always produce a list, even for a single child.

    Raises xml.etree.ElementTree.ParseError if the document is empty or is not
    valid XML.
    """
    # An XML declaration is only valid at the very start of the document
    root = ET.fromstring(xml_string.strip())

    return _element_to_dict(
        root,
        set(strip_namespaces) if strip_namespaces else set(),
        set(force_list) if force_list else set()
    )


def unparse_xml(data_dict):
    # type: (dict[str, Any]) -> str
    """
    Convert a dict structure in the layout produced by parse_xml into an XML
    string, without an XML declaration (CMCI rejects one).
    """
    if not data_dict:
        return ''

    root_name = list(data_dict.keys())[0]
    root = _dict_to_element(root_name, data_dict[root_name])

    # CMCI expects explicit end tags rather than self-closing elements
    return ET.tostring(root, encoding='unicode', method='xml', short_empty_elements=False)


def _strip_namespace(tag, ns_uris):
    # type: (str, set) -> str
    """Remove the namespace from a tag or attribute name if it is in ns_uris."""
    if tag.startswith('{'):
        namespace, local_name = tag[1:].split('}', 1)
        if namespace in ns_uris:
            return local_name

    return tag


def _element_to_dict(element, ns_uris, force_list_set):
    # type: (ET.Element, set, set) -> OrderedDict
    result = OrderedDict()
    tag = _strip_namespace(element.tag, ns_uris)

    for key, value in element.attrib.items():
        result['@' + _strip_namespace(key, ns_uris)] = value

    children = list(element)

    if not children:
        text = element.text.strip() if element.text else None
        if result:
            if text:
                result['#text'] = text
            return OrderedDict([(tag, result)])
        return OrderedDict([(tag, text or None)])

    child_dict = OrderedDict()  # type: OrderedDict[str, list[OrderedDict]]
    for child in children:
        child_tag = _strip_namespace(child.tag, ns_uris)
        child_content = _element_to_dict(child, ns_uris, force_list_set)[child_tag]
        child_dict.setdefault(child_tag, []).append(child_content)

    for child_tag, child_list in child_dict.items():
        result[child_tag] = child_list if (len(child_list) > 1 or child_tag in force_list_set) else child_list[0]

    return OrderedDict([(tag, result)])


def _dict_to_element(tag, data):
    # type: (str, Any) -> ET.Element
    element = ET.Element(tag)

    if data is None:
        return element

    if isinstance(data, dict):
        for key, value in data.items():
            if key == '@xmlns' and isinstance(value, dict):
                # Namespace declarations, keyed by prefix ('' for the default namespace)
                for ns_prefix, ns_uri in value.items():
                    element.set('xmlns:' + ns_prefix if ns_prefix else 'xmlns', str(ns_uri))
            elif key.startswith('@'):
                element.set(key[1:], str(value))
            elif key == '#text':
                element.text = str(value)
            else:
                for item in (value if isinstance(value, list) else [value]):
                    element.append(_dict_to_element(key, item))
    else:
        element.text = str(data)

    return element
