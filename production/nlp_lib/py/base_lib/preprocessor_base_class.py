# -*- coding: utf-8 -*-
"""
Created on Mon May 20 12:25:32 2019

@author: haglers
"""

#
import re

#
from tool_lib.py.processing_tools_lib.text_processing_tools \
    import substitution

#
class Preprocessor_base(object):
    
    #
    def __init__(self, static_data):
        self.static_data = static_data
        self.command_list = []
        self.text = ''
        
    #
    def _append_keywords_text(self, keyword, index_flg=1):
        keyword = re.sub(self.section_header_pre_tag, '', keyword)
        keyword = re.sub(self.section_header_post_tag, '', keyword)
        self.dynamic_data_manager._append_keywords_text(keyword, index_flg)
        
    #
    def _clear_command_list(self):
        self.command_list = []
        
    #
    def _general_command(self, command0, command1, keyword_flg=False):
        if isinstance(command0, list):
            command0_tmp = command0
            command0 = []
            for command in command0_tmp:
                command = \
                    re.sub('(?<=[A-Za-z]) (?=[A-Za-z])', '(\n| )', command)
                command0.append(command)
        else:
            command0 = \
                re.sub('(?<=[A-Za-z]) (?=[A-Za-z])', '(\n| )', command0)
        self._clear_command_list()
        self.command_list.append([ 3, command0, command1 ])
        if keyword_flg:
            self._append_keywords_text(command1)
        self._process_command_list()
        
    #
    def _insert_whitespace(self, match_str, whitespace):
        match = 0
        m_str = re.compile(match_str)
        while match is not None:
            match = m_str.search(self.text, re.IGNORECASE)
            if match is not None:
                self.text = self.text[:match.start()] + whitespace + \
                            self.text[match.start()+1:]
        
    #
    def _normalize_regular_initialism(self, text, initialism):
        self._general_command('(?i)' + text + '( \( ' + initialism + ' \))?',
                              {None : initialism})
    
    #
    def _normalize_whitespace(self):
        self._general_command('\n\t', {None : '\n'})
        self._general_command('\r\n', {None : '\n'})
        self._general_command('\n*\n\n', {None : '\n\n'})
        self._general_command('[\n\s]*\n\s*\n', {None : '\n\n'})
        self._general_command('\n *', {None : '\n'})
        self._general_command(' *\n', {None : '\n'})
        self._general_command('\n-', {None : '\n\t-'})
        self._general_command('\t+', {None : '\t'})
        self._general_command(' ?\t ?', {None : '\t'})
        self.text = re.sub('^[\n\s]*', '', self.text)
        self.text = re.sub('[\n\s]*$', '', self.text)
        self._general_command('^ +[-]', {' ' : ''})
        self._general_command(' +', {None : ' '})
        self._general_command(' \n', {None : '\n'})
        self.text = re.sub(' \n', '\n', self.text)
    
    #
    def _process_command_list(self):
        for command in self.command_list:
            if command[0] == 0:
                self._extract_section_to_bottom_of_report(command[1], command[2])
            elif command[0] == 1:
                self._insert_whitespace(command[1], '\n\n')
            elif command[0] == 2:
                self._insert_whitespace(command[1], '\n')
            elif command[0] == 3:
                if type(command[1]) == str:
                    if None in command[2].keys():
                        self.text = re.sub(command[1], command[2][None], self.text)
                    else:
                        self.text = substitution(command[1], command[2], self.text)
                elif type(command[1]) == list:
                    if isinstance(command[2], str):
                        self._normalize_section_headers([], command[1], command[2])
                    else:
                        for comm in command[1]:
                            self.text = re.sub(comm, command[2][None], self.text)
            else:
                print('error')    
     
    #
    def pull_dynamic_data_manager(self):
        return self.dynamic_data_manager
     
    #
    def pull_text(self):
        return self.text
    
    #
    def push_dynamic_data_manager(self, dynamic_data_manager):
        self.dynamic_data_manager = dynamic_data_manager
     
    #
    def push_text(self, text):
        self.text = text