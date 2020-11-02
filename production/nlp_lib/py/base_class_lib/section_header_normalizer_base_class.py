# -*- coding: utf-8 -*-
"""
Created on Tue May 12 17:04:28 2020

@author: haglers
"""

#
import re

#
from nlp_lib.py.base_class_lib.preprocessor_base_class import Preprocessor_base
from nlp_lib.py.tool_lib.processing_tools_lib.text_processing_tools import s

#
class Section_header_normalizer_base(Preprocessor_base):
    
    #
    def _amend(self):
        return('(amended|amendment)')
        
    #
    def _case(self):
        return('(case|diagnosis|report)')
        
    #
    def _confirmed(self):
        return('(confirmed|dictated|reviewed|seen|staffed)')
    
    #
    def _datetime(self, mode_flg='full'):
        base = 'date(/time)?'
        modifier = modifier = '(admission|consultation|discharge|notification|onset|referral|service|visit)'
        if mode_flg == 'full':
            return('(' + modifier + '(/' + modifier + ')? )?' + base)
        elif mode_flg == 'modifier':
            return(modifier)
    
    #
    def _diagnosis(self):
        base = '(diagnos(e|i)s|dx)'
        modifier0 = '(additional|encounter|final|postoperative|preoperative|primary|principal|referral|secondary)'
        modifier1 = 'nutritional'
        return('(' + modifier0 + '(/' + modifier0 + ')? )?' + '(' + modifier1 + ' )?' + base)
    
    #
    def _history(self):
        base = '((history|hx)|((history|hx) of present illness|hpi)|(history|hx) of presenting problem)'
        modifier = '(clinical|immunization|interim|interval|medical|oncologic|social|surgical|treatment)'
        return('(' + modifier + ' )?' + base)
    
    #
    def _medication(self):
        base = '(medication|prescription|supplement)' + s()
        modifier = '(dietary|hospital|outpatient)'
        return('(' + modifier + ' )?' + base)
    
    #
    def _patient(self):
        return('(learner|patient|subject)')
    
    #
    def _physician(self):
        base = '(attend(ant|ing)|assist(ant|ing)|author|nurse|physician|practitioner|provider|reviewer|surgeon)' + s()
        modifier0 = '(attending|authorizing|consulting|discharging|enrolling|referring|requesting)'
        modifier1 = 'nephrology'
        return('(' + modifier0 + '(/' + modifier0 + ')? )?' + '(' + modifier1 + ' )?' + base)

    #
    def _normalize_formatted_section_header(self, text_in, label, keyword_flg=True):
        text = []
        if isinstance(text_in, list):
            for i in range(len(text_in)):
                text.append('(?i)(^|\n)' + text_in[i] + '(:|\.|\n)([\n\s]*|$)')
        else:
            text.append('(?i)(^|\n)' + text_in + '(:|\.|\n)([\n\s]*|$)')
        self._clear_command_list()
        self._general_command(text, self._tagged_section_header(label), keyword_flg)
        self._process_command_list()
        
    #
    def _normalize_unformatted_section_header(self, text_in, label, no_punctuation_flg, keyword_flg=True):
        text = []
        if isinstance(text_in, list):
            for i in range(len(text_in)):
                text.append('(?i)( |\n)' + text_in[i] + '(( updated)? \d+/\d+/\d+)?( )?(:|;)')
        else:
            text.append('(?i)( |\n)' + text_in + '(( updated)? \d+/\d+/\d+)?( )?(:|;)')
        if no_punctuation_flg:
            if isinstance(text_in, list):
                for i in range(len(text_in)):
                    text.append('(?<!<<<)' + text_in[i].upper())
            else:
                text.append('(?<!<<<)' + text_in.upper())
        self._clear_command_list()
        self._general_command(text, self._tagged_section_header(label), keyword_flg)
        self._process_command_list()
        
    #
    def _normalize_section_header(self, mode_flg, text_in, label, no_punctuation_flg=False, keyword_flg=True):
        if mode_flg == 'formatted':
            self._normalize_formatted_section_header(text_in, label, keyword_flg)
        elif mode_flg == 'unformatted':
            self._normalize_unformatted_section_header(text_in, label, no_punctuation_flg, keyword_flg)
        elif mode_flg == 'pull_out_section_header_to_bottom_of_report':
            self._clear_command_list()
            self._pull_out_section_header_to_bottom_of_report(text_in, self._tagged_section_header(label), keyword_flg)
            self._process_command_list()
        else:
            print('unknown mode: ' + mode_flg)
            
    #
    def _post_punct(self):
        return('(:|\.|\n)([\n\s]*|$)')
        
    #
    def _pre_punct(self):
        return('(?i)(^|\n)')
            
    #
    def comment(self, mode_flg):
        text_list = []
        if mode_flg == 'pull_out_section_header_to_bottom_of_report':
            text_list.append(self._pre_punct() + 'comment' + s() + ' (\([^\)]*\))?' + self._post_punct())
            text_list.append(self._pre_punct() + 'comment' + s() + ' (for specimen )?[A-Z]' + self._post_punct())
            text_list.append(self._pre_punct() + 'comment' + s() + self._post_punct())
            text_list.append(self._pre_punct() + '(\()?comment' + s() + '[\n\s]*:')
            text_list.append(self._pre_punct() + 'note' + self._post_punct())
            text_list.append(self._pre_punct() + 'note\s+\([^\)]*\)' + self._post_punct())
            text_list.append(self._pre_punct() + 'note (\([^\)]*\))?' + self._post_punct())
            text_list.append(self._pre_punct() + 'note( [A-Z])?' + self._post_punct())
            self._normalize_section_header(mode_flg, text_list, 'COMMENT')
        elif mode_flg == 'unformatted':
            text_list = []
            text_list.append('comment' + s())
            text_list.append('miscellaneous')
            text_list.append('(?<!labs to\n\n)note')
            text_list.append(self._patient() + ' ?/ ?family baseline understanding')
            text_list.append(self._patient() + ' ?/ ?family readiness to learn')
            text_list.append(self._patient() + ' ?/ ?family responses to teaching')
            text_list.append('regarding')
            text_list.append('teaching provided')
            text_list.append('visit type')
            self._normalize_section_header(mode_flg, text_list, 'COMMENT')
        else:
            print('unknown mode: ' + mode_flg)
            
    #
    def history(self, mode_flg):
        text_list = []
        text_list.append('((brief|past) )?' + '(family history|FH)')
        if mode_flg == 'formatted':
            self._normalize_section_header(mode_flg, text_list, 'FAMILY HSTRY', keyword_flg=False)
        elif mode_flg == 'unformatted':
            self._normalize_section_header(mode_flg, text_list, 'FAMILY HSTRY', no_punctuation_flg=True, keyword_flg=False)
        else:
            print('unknown mode: ' + mode_flg)
        text_list = []
        if mode_flg == 'formatted':
            text_list.append('(PMH|PSH)')
        elif mode_flg == 'unformated':
            text_list.append('(PMH|PSH) :')
        text_list.append('(brief|past) ' + self._history())
        text_list.append(self._patient() + ' ' + self._history())
        text_list.append('(?!<family )' + self._history())
        text_list.append('(?<!' + self._patient() + ') id( |/hpi)')
        if mode_flg == 'formatted':
            self._normalize_section_header(mode_flg, text_list, 'HISTORY')
        elif mode_flg == 'unformatted':
            self._normalize_section_header(mode_flg, text_list, 'HISTORY', no_punctuation_flg=True)
        else:
            print('unknown mode: ' + mode_flg)
        self.text = re.sub('FAMILY HSTRY', 'FAMILY HISTORY', self.text)
        self._append_keywords_text('FAMILY HISTORY')
        
    #
    def impression_and_recommendation(self, mode_flg):
        text_list = []
        text_list.append('discharge recommendation' + s())
        text_list.append('impression' + s() + ' and recommendation' + s())
        if mode_flg == 'formatted':
            self._normalize_section_header(mode_flg, text_list, 'IMPRESSION AND RECOMMENDATION')
        elif mode_flg == 'unformatted':
            self._normalize_section_header(mode_flg, text_list, 'IMPRESSION AND RECOMMENDATION', no_punctuation_flg=True)
        else:
            print('unknown mode: ' + mode_flg)
            
    #
    def person(self, mode_flg):
        text_list = []
        if mode_flg == 'formatted':
            text_list.append('discussed with[^ \d]')
            text_list.append(self._case() + ' (' + self._amend() + '|' + self._confirmed() + ') by')
            text_list.append(self._amend() + ' ' + self._confirmed() + ' by')
            text_list.append('(frozen section diagnosis|intraoperative consult(ation)? diagnosis) ' + \
                             self._confirmed() + ' by')
            text_list.append(self._confirmed() + ' by[^ \d]?')
            self._normalize_section_header(mode_flg, text_list, 'PERSON')
        elif mode_flg == 'unformatted':
            text_list.append(self._patient())
            text_list.append('name of ' + self._physician() + '/clinical support person notified')
            text_list.append(self._patient() + ' (identification|name)')
            text_list.append('(addended|performed|referred|requested) by')
            text_list.append(self._physician())
            text_list.append('(primary care ' + self._physician() + '|pcp)')
            self._normalize_section_header(mode_flg, text_list, 'PERSON')
        else:
            print('unknown mode: ' + mode_flg)