# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 10:38:34 2020

@author: haglers
"""

#
import re

#
def _valid_xml_char_ordinal(c):
    codepoint = ord(c)
    return (
        0x20 <= codepoint <= 0xD7FF or
        codepoint in (0x9, 0xA, 0xD) or
        0xE000 <= codepoint <= 0xFFFD or
        0x10000 <= codepoint <= 0x10FFFF
        )

#
def article():
    return('(a|an|that|the|these|this|those)')
    
#
def be():
    return('(am|are|be|been|being|is|was|were)')

#
def make_ascii(text):
    text = text.replace('?', '<<QUESTIONMARK>>')
    text = text.encode('ascii', 'replace').decode()
    text = text.replace('?', ' ')
    text = text.replace('<<QUESTIONMARK>>', '?')
    return text
    
#
def make_xml_compatible(text):
    text = ''.join(c for c in text if _valid_xml_char_ordinal(c))
    return text

#
def note_label():
    return('[A-Z0-9]{1}')

#
def part_label():
    return('[A-Z0-9]{1}')

#
def s():
    return('(es|s| ?\( ?es ?\)| ?\( ?s ?\))?')
    
#
def specimen_label():
    return('[A-Z0-9]{1}')

#
def substitution(match_pattern, repl_dict, text_in):
    text_out = text_in
    match = 0
    match_str = match_pattern
    m_str = re.compile(match_str)
    stop_flg = False
    ctr = 0
    while not stop_flg:
        ctr += 1
        stop_flg = True
        for match in m_str.finditer(text_out):
            if match is not None:
                stop_flg = False
                search_str = match.group(0)
                for key in repl_dict.keys():
                    replace_str = re.sub(key, repl_dict[key], search_str)
                    text_out = text_out.replace(search_str, replace_str)
        if ctr == 100:
            stop_flg = True
    return text_out