# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 10:38:34 2020

@author: haglers
"""

#
def amend():
    return '(amended|amendment)'

#
def article():
    article_list = [ 'an?', 'that', 'the', 'these', 'this', 'those' ]
    return regex_from_list(article_list)
    
#
def be():
    return '(am|are|be|been|being|is|was|were)'

#
def block_label():
    return '([A-Z]*[0-9]*|[0-9]*[A-Z]*)'

#
def case_number():
    return '[A-Z0-9-]*'

#
def class_label():
    return '[A-Z0-9]{1}'

#
def clinician():
    base = '(attend(ant|ing)|assist(ant|ing)|author|nurse|physician|practitioner|provider|reviewer|surgeon)' + s()
    modifier0 = '(attending|authorizing|consulting|discharging|enrolling|referring|requesting)'
    modifier1 = 'nephrology'
    return '(' + modifier0 + '(/' + modifier0 + ')? )?' + '(' + modifier1 + ' )?' + base

#
def clinician_reviewed():
    return '(confirmed|dictated|reviewed|seen|staffed)'

#
def colon():
    return ' ?: ?'

#
def comma():
    return ' ?, ?'

#
def conjunction():
    conjunction_list = [ 'and', 'or' ]
    return regex_from_list(conjunction_list)

#
def datetime(mode_flg='full'):
    base = 'date(/time)?'
    modifier = modifier = '(admission|consultation|discharge|notification|onset|referral|service|visit)'
    if mode_flg == 'full':
        return '(' + modifier + '(/' + modifier + ')? )?' + base
    elif mode_flg == 'modifier':
        return modifier

#
def diagnosis():
    base = '(diagnos(e|i)s|dx)'
    modifier0 = '(additional|encounter|final|postoperative|preoperative|primary|principal|referral|secondary)'
    modifier1 = 'nutritional'
    return '(' + modifier0 + '(/' + modifier0 + ')? )?' + '(' + modifier1 + ' )?' + base

#
def history():
    base = '((history|hx)|((history|hx) of present illness|hpi)|(history|hx) of presenting problem)'
    modifier = '(clinical|immunization|interim|interval|medical|oncologic|social|surgical|treatment)'
    return '(' + modifier + ' )?' + base

#
def left_parenthesis():
    return '\( ?'

#
def medication():
    base = '(medication|prescription|supplement)' + s()
    modifier = '(dietary|hospital|outpatient)'
    return '(' + modifier + ' )?' + base

#
def minus_sign():
    return ' ?- ?'

#
def nonword():
    return '[^A-Za-z0-9 ]+'

#
def note_label():
    return '[A-Z0-9]{1}'

#
def part_label():
    return '[A-Z0-9]{1}'

#
def patient():
    return '(learner|patient|subject)'

#
def preposition():
    preposition_list = [ 'after', 'at', 'for', 'in', 'of', 'on', 'to', 'with' ]
    return regex_from_list(preposition_list)

#
def regex_from_list(text_list):
    regex = '('
    for i in range(len(text_list)):
        regex += text_list[i]
        regex += '|'
    regex = regex[:-1] + ')'
    return regex

#
def review_item():
    return '(case|diagnosis|report)'

#
def right_parenthesis():
    return ' ?\)'

#
def s():
    return '(es|s| ?\( ?es ?\)| ?\( ?s ?\))?'

#
def slash():
    return ' ?/ ?'

#
def slice_label():
    return '[0-9]+'

#
def slide_label():
    return '([A-Z]*[0-9]*|[0-9]*[A-Z]*)'
    
#
def specimen_label():
    return '[A-Z0-9]{1}'

#
def test_label():
    return '[a-z0-9\-]+'

#
def space():
    return ' +'
        
#
def word():
    return '[A-Za-z0-9]+([\-/][A-Za-z0-9]+)?'