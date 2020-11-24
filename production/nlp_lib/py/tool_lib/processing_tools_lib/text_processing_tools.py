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
def amend():
    return('(amended|amendment)')

#
def article():
    return('(a|an|that|the|these|this|those)')
    
#
def be():
    return('(am|are|be|been|being|is|was|were)')

#
def block_label():
    return('([A-Z]*[0-9]*|[0-9]*[A-Z]*)')

#
def case_number():
    return('[A-Z0-9-]*')

#
def class_label():
    return('[A-Z0-9]{1}')

#
def clinician():
    base = '(attend(ant|ing)|assist(ant|ing)|author|nurse|physician|practitioner|provider|reviewer|surgeon)' + s()
    modifier0 = '(attending|authorizing|consulting|discharging|enrolling|referring|requesting)'
    modifier1 = 'nephrology'
    return('(' + modifier0 + '(/' + modifier0 + ')? )?' + '(' + modifier1 + ' )?' + base)

#
def clinician_reviewed():
    return('(confirmed|dictated|reviewed|seen|staffed)')

#
def datetime(mode_flg='full'):
    base = 'date(/time)?'
    modifier = modifier = '(admission|consultation|discharge|notification|onset|referral|service|visit)'
    if mode_flg == 'full':
        return('(' + modifier + '(/' + modifier + ')? )?' + base)
    elif mode_flg == 'modifier':
        return(modifier)

#
def diagnosis():
    base = '(diagnos(e|i)s|dx)'
    modifier0 = '(additional|encounter|final|postoperative|preoperative|primary|principal|referral|secondary)'
    modifier1 = 'nutritional'
    return('(' + modifier0 + '(/' + modifier0 + ')? )?' + '(' + modifier1 + ' )?' + base)

#
def history():
    base = '((history|hx)|((history|hx) of present illness|hpi)|(history|hx) of presenting problem)'
    modifier = '(clinical|immunization|interim|interval|medical|oncologic|social|surgical|treatment)'
    return('(' + modifier + ' )?' + base)

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
def medication():
    base = '(medication|prescription|supplement)' + s()
    modifier = '(dietary|hospital|outpatient)'
    return('(' + modifier + ' )?' + base)

#
def note_label():
    return('[A-Z0-9]{1}')

#
def part_label():
    return('[A-Z0-9]{1}')

#
def patient():
    return('(learner|patient|subject)')

#
def remove_repeated_substrings(text):
    ctr = 0
    while True:
        ctr += 1
        stop_flg = True
        for i in range(int(len(text)/2)):
            if text[:i+1] == text[i+1:2*(i+1)]:
                text = text[i+1:]
                stop_flg = False
                break
        if stop_flg or ctr > 100:
            break
    return text

#
def review_item():
    return('(case|diagnosis|report)')

#
def s():
    return('(es|s| ?\( ?es ?\)| ?\( ?s ?\))?')

#
def slice_label():
    return('[0-9]+')

#
def slide_label():
    return('([A-Z]*[0-9]*|[0-9]*[A-Z]*)')
    
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

#
def test_label():
    return('[a-z0-9\-]+')