# -*- coding: utf-8 -*-
"""
Created on Tue May 12 17:04:28 2020

@author: haglers
"""

#
import re

#
import lambda_lib.tool_lib.lambda_tools as lambda_tools
from tools_lib.regex_lib.regex_tools \
    import (
        amend,
        article,
        be,
        colon,
        datetime,
        diagnosis,
        medication,
        period,
        review_item,
        s
    )
from tools_lib.regex_lib.regex_tools \
    import amend, clinician, clinician_reviewed, history, patient, review_item, s

#
class Section_header_normalizer(object):
    
    #
    def __init__(self, section_header_structure):
        self.section_header_structure = section_header_structure
        self.section_header_post_tag = '>>>'
        self.section_header_pre_tag = '<<<'
        
    #
    def _add_punctuation_formatted(self, regex_dict):
        text_list = []
        if isinstance(regex_dict, dict):
            for key in regex_dict.keys():
                text = []
                text_in = regex_dict[key]
                if 'PRE_PUNCT' in key and 'POST_PUNCT' in key:
                    if isinstance(text_in, list):
                        for i in range(len(text_in)):
                            text.append(self._pre_punct() + text_in[i] + self._post_punct())
                    else:
                        text.append(self._pre_punct() + text_in + self._post_punct())
                elif 'PRE_PUNCT' in key:
                    if isinstance(text_in, list):
                        for i in range(len(text_in)):
                            text.append(self._pre_punct() + text_in[i])
                    else:
                        text.append(self._pre_punct() + text_in)
                else:
                    if isinstance(text_in, list):
                        for i in range(len(text_in)):
                            text.append(text_in[i])
                    else:
                        text.append(text_in)
                text_list.append(text)
        else:
            text_in = regex_dict
            text = []
            if isinstance(text_in, list):
                for i in range(len(text_in)):
                    text.append(self._pre_punct() + text_in[i] + self._post_punct())
            else:
                text.append(self._pre_punct() + text_in + self._post_punct())
            text_list.append(text)
        return text_list
    
    #
    def _append_keywords_text(self, keyword, index_flg=1):
        keyword = re.sub(self.section_header_pre_tag, '', keyword)
        keyword = re.sub(self.section_header_post_tag, '', keyword)
        self.dynamic_data_manager.append_keywords_text(keyword, index_flg)
    
    #
    def _get_section_header_list(self, section_header_dict):
        section_header_list = list(section_header_dict.keys())
        section_header_list.sort(key=len, reverse=True)
        return section_header_list
    
    #
    def _insert_whitespace(self, text, match_str, whitespace):
        match = 0
        m_str = re.compile(match_str)
        while match is not None:
            match = m_str.search(text, re.IGNORECASE)
            if match is not None:
                text = text[:match.start()] + whitespace + text[match.start()+1:]
        return text
                
    #
    def _normalize_section_header(self, mode_flg, text_list, label):
        if mode_flg == 'formatted':
            self._normalize_section_headers(text_list, label)
        self._append_keywords_text(self._tagged_section_header(label))
        
    #
    def _normalize_section_headers(self, text_list, label):
        for text in text_list:
            match_strs_tmp = text
            section_lbl = self._tagged_section_header(label)
            match_strs = []
            for match_str in match_strs_tmp:
                match_str = \
                    re.sub('(?<=[A-Za-z]) (?=[A-Za-z])', '(\n| )', match_str)
                match_strs.append(match_str)
            for match_str in match_strs:
                self.text = \
                    lambda_tools.lambda_conversion(match_str,
                                                          self.text,
                                                          '\n\n' + section_lbl + ' N\n\n')
            self.text = \
                lambda_tools.lambda_conversion(section_lbl + ' N(\n+' + section_lbl + ' N\n+)+',
                                                      self.text, section_lbl + ' N\n\n')
            self.text, num = self._number_section(section_lbl, self.text)
        return num
            
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
    def _post_punct(self):
        #return '(' + colon() + '|' + period() + '|\n)([\n\s]*|$)'
        return '(' + colon() + '|' + period() + '|\n)'
        
    #
    def _pre_punct(self):
        return '(^|\n)'
        
    #
    def _pull_out_section_header(self, text, command):
        text = self._insert_whitespace(text, command, '\n\n')
        return text
    
    #
    def _remove_from_keywords_text(self, keyword, index_flg=1):
        self.dynamic_data_manager.remove_from_keywords_text(keyword, index_flg)
        
    #
    def _tagged_section_header(self, untagged_text):
        tagged_text = \
            self.section_header_pre_tag + untagged_text + self.section_header_post_tag
        return tagged_text
        
    #
    def clear_section_header_tags(self, text):
        self.text = text
        self.text = \
            lambda_tools.lambda_conversion(' > > >', self.text, self.section_header_post_tag)
        self.text = \
            lambda_tools.lambda_conversion('< < < ', self.text, self.section_header_pre_tag)
        self.text = \
            lambda_tools.deletion_lambda_conversion(self.section_header_pre_tag, self.text)
        self.text = \
            lambda_tools.deletion_lambda_conversion(self.section_header_post_tag, self.text)
        return self.text
        
    #
    def normalize_section_header(self, text):
        self.text = text
        section_header_dict = \
            self.section_header_structure.get_section_header_dict()
        section_header_list = \
            self._get_section_header_list(section_header_dict)
        for section_header in section_header_dict:
            regex_list = section_header_dict[section_header]
            text_list = self._add_punctuation_formatted(regex_list)
            self._normalize_section_header('formatted', text_list, section_header)
        return self.text
            
    #
    def pull_dynamic_data_manager(self):
        return self.dynamic_data_manager
    
    #
    def pull_out_section_headers(self, text):
        text = self._pull_out_section_header(text, '(?i)\n[ \t]+antibodies tested')
        text = self._pull_out_section_header(text, '(?i)\n[ \t]+bone marrow aspirate smears')
        text = self._pull_out_section_header(text, '(?i)\n[ \t]+bone marrow (biopsy/)?clot section')
        text = self._pull_out_section_header(text, '(?i)\n[ \t]+bone marrow differential')
        text = self._pull_out_section_header(text, '(?i)\n[ \t]+case (reviewed|seen) by:?')
        text = self._pull_out_section_header(text, '(?i)\n[ \t]+cbc')
        text = self._pull_out_section_header(text, '(?i)\n[ \t]+clinical history')
        text = self._pull_out_section_header(text, '(?i)\n[ \t]+comment(s)?( )?(\([a-z0-9 ]*\))?:')
        text = self._pull_out_section_header(text, '(?i)\n[ \t]+component value')
        text = self._pull_out_section_header(text, '(?i)\n[ \t]+cytogenetic and fish studies')
        text = self._pull_out_section_header(text, '(?i)\n[ \t]+flow cytometric analysis')
        text = self._pull_out_section_header(text, '(?i)\n[ \t]+immunohistochemical stains:')
        text = self._pull_out_section_header(text, '(?i)\n[ \t]+immunologic analysis:')
        text = self._pull_out_section_header(text, '(?i)\n[ \t]+molecular studies:')
        text = self._pull_out_section_header(text, '(?i)\n[ \t]+note( )?(\([a-z0-9 ]*\))?:')
        text = self._pull_out_section_header(text, '(?i)\n[ \t]+peripheral blood differential')
        text = self._pull_out_section_header(text, '(?i)\n[ \t]+peripheral blood morphology')
        text = self._pull_out_section_header(text, '(?i)\n[ \t]+resulting agency')
        text = self._pull_out_section_header(text, '(?i)\n[ \t]+special stains')
        return text
        
    #
    def push_dynamic_data_manager(self, dynamic_data_manager):
        self.dynamic_data_manager = dynamic_data_manager