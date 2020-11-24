# -*- coding: utf-8 -*-
"""
Created on Mon May 20 12:25:32 2019

@author: haglers
"""

#
import re

#
from nlp_lib.py.base_class_lib.general_base_class import General_base
from nlp_lib.py.tool_lib.processing_tools_lib.text_processing_tools \
    import make_ascii, make_xml_compatible, substitution

#
class Preprocessor_base(General_base):
    
    #
    def __init__(self, project_data):
        General_base.__init__(self, project_data)
        self.command_list = []
        self.section_header_post_tag = '>>>'
        self.section_header_pre_tag = '<<<'
        self.text = ''
        
    #
    def _append_keywords_text(self, keyword, index_flg=1):
        keyword = re.sub(self.section_header_pre_tag, '', keyword)
        keyword = re.sub(self.section_header_post_tag, '', keyword)
        self.linguamatics_i2e_writer._append_keywords_text(keyword, index_flg)
        
    #
    def _clear_command_list(self):
        self.command_list = []
        
    #
    def _clear_section_header_tags(self):
        self.text = re.sub(' > > >', self.section_header_post_tag, self.text)
        self.text = re.sub('< < < ', self.section_header_pre_tag, self.text)
        self.text = re.sub(self.section_header_pre_tag, '', self.text)
        self.text = re.sub(self.section_header_post_tag, '', self.text) 
        
    #
    def _extract_section_to_bottom_of_report(self, match_strs, item_label):
        item_label = item_label
        footer = ''
        for match_str in match_strs:
            m_str0 = re.compile(match_str + '[^\n]+\n')
            m_str1 = re.compile(match_str)
            match = 0
            while match is not None:
                match = m_str0.search(self.text)
                if match is not None:
                    self.text = self.text[:match.start()] + '\n\n' + \
                                self.text[match.end():]
                    match1 = m_str1.search(match.group(0))
                    footer += '\n\n' + item_label  + ' N\n\n' + \
                              match.group(0)[match1.end():]
        self.text += footer
        self.text, num = self._number_section(item_label, self.text)
        
    #
    def _general_command(self, command0, command1, keyword_flg=False):
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
    def _make_text_ascii(self):
        self.text = make_ascii(self.text)
                            
    #
    def _make_text_xml_compatible(self):
        self.text = make_xml_compatible(self.text)
        
    #
    def _normalize_regular_initialism(self, text, initialism):
        self._general_command('(?i)' + text + '( \( ' + initialism + ' \))?', {None : initialism})
        
    #
    def _normalize_section_headers(self, match_lists, match_strs, section_lbl):
        for match_list in match_lists:
            self.text = substitution(match_list[0], 
                                           {match_list[1]: '\n\n' + section_lbl + ' N\n\n'}, 
                                           self.text)
        for match_str in match_strs:
            self.text = re.sub(match_str, '\n\n' + section_lbl + ' N\n\n', self.text)
        self.text = re.sub(section_lbl + ' N(\n+' + section_lbl + ' N\n+)+',
                           section_lbl + ' N\n\n', self.text)
        self.text, num = self._number_section(section_lbl, self.text)
        return num
    
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
    def _number_section(self, section_str, text):
        count_str = section_str + ' N\n'
        num = text.count(count_str)
        for n in range(num):
            match_str = section_str + ' N\n'
            sub_str = section_str + ' ' + str(n+1) + '\n'
            text = re.sub(match_str, sub_str, text, 1)
        return text, num
    
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
    def _pull_out_section_header(self, command):
        self._clear_command_list()
        self.command_list.append([ 1, command ])
        self._process_command_list()
        
    #
    def _pull_out_section_header_to_bottom_of_report(self, command0, command1, keyword_flg=False):
        self._clear_command_list()
        self.command_list.append([ 0, command0, command1 ])
        if keyword_flg:
            self._append_keywords_text(command1)
        self._process_command_list()
            
    #
    def _pull_out_table_entry(self, command):
        self._clear_command_list()
        self.command_list.append([ 2, command ])
        self._process_command_list()
        
    #
    def _push_down_body_header(self, match_str):
        match = re.search(match_str, self.text)
        if match is not None:
            self.text = self.text[:match.end()] + '\n' + self.body_header + \
                                  '\n\n' + self.text[match.end():]
            self.text = re.sub('^' + self.body_header + '[\n\s]*', '', self.text)
    
    #
    def _substitution_endings_list(self, search_str):
        self._general_command(search_str + '\n', {None : '\n'})
        self._general_command(search_str + '\t', {None : '\t'})
        self._general_command(search_str + ' ', {None : ' '})
        self._general_command(search_str + ',', {None : ','})
        self._general_command(search_str + '\.', {None : '.'})
        self._general_command(search_str + ';', {None : ';'})
        self._general_command(search_str + '( )?-', {None : '-'})
    
    #
    def _tagged_section_header(self, untagged_text):
         tagged_text = self.section_header_pre_tag + untagged_text + self.section_header_post_tag
         return tagged_text
     
    #
    def pull_linguamatics_i2e_writer(self):
        return self.linguamatics_i2e_writer
     
    #
    def pull_text(self):
        return self.text
    
    #
    def push_linguamatics_i2e_writer(self, linguamatics_i2e_writer):
        self.linguamatics_i2e_writer = linguamatics_i2e_writer
     
    #
    def push_text(self, text):
        self.text = text