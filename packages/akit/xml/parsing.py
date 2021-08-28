
from typing import List, Union

from collections import defaultdict

import yaml

from xml.etree.ElementTree import fromstring as xml_from_string

def etree_to_dict(cursor) -> dict:
    """
       Converts an ElementTree node and its descendant children to a dictionary
       object.

       :param cursor: The root element tree node to convert to a dictionary 
    """

    info = {cursor.tag: {} if cursor.attrib else None}

    children = list(cursor)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        info = {cursor.tag: {k: v[0] if len(v) == 1 else v
                     for k, v in dd.items()}}

    if cursor.attrib:
        info[cursor.tag].update(('@' + k, v)
                        for k, v in cursor.attrib.items())

    if cursor.text:
        text = cursor.text.strip()
        if children or cursor.attrib:
            if text:
                info[cursor.tag]['#text'] = text
        else:
            info[cursor.tag] = text

    return info

def parse_xml_to_dict(xml_content) -> dict:
    """
        Processes xml content and returns a dictionary based on the xml content.

        :param xml_content: The xml document content to process and convert.
    """
    rtn_info = None
    troot = xml_from_string(xml_content)
    rtn_info = etree_to_dict(troot)

    return rtn_info

def format_xml_as_yaml(xml_content: str, split_lines: bool = False) -> Union[str, List[str]]:
    """
        Processes xml content and converts it to YAML

        :param xml_content: The xml document content to process and convert.
        :param split_lines: A boolean indicating that the yaml content should be
                            returned as a multi-line list of strings.
    """

    dict_info = parse_xml_to_dict(xml_content)

    content = yaml.dump(dict_info)

    if split_lines:
        content = content.splitlines(False)

    return content
