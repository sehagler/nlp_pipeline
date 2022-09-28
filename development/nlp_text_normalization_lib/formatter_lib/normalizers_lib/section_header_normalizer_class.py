# -*- coding: utf-8 -*-
"""
Created on Tue May 12 17:04:28 2020

@author: haglers
"""

#
import re

#
from lambda_lib.lambda_manager_class import Lambda_manager
from regex_lib.regex_tools \
    import amend, clinician, clinician_reviewed, history, patient, review_item, s
from tool_lib.py.structure_tools_lib.section_header_structure_tools \
    import Section_header_structure_tools

#
class Section_header_normalizer(object):
    
    #
    def __init__(self, static_data):
        self.static_data = static_data
        self.lambda_manager = Lambda_manager()
        self.section_header = Section_header_structure_tools()
        self.section_header_post_tag = '>>>'
        self.section_header_pre_tag = '<<<'
    
    #
    def _append_keywords_text(self, keyword, index_flg=1):
        keyword = re.sub(self.section_header_pre_tag, '', keyword)
        keyword = re.sub(self.section_header_post_tag, '', keyword)
        self.dynamic_data_manager.append_keywords_text(keyword, index_flg)
    
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
    def _normalize_section_header(self, mode_flg, text_list, label):
        if mode_flg == 'formatted' or mode_flg == 'unformatted':
            self._normalize_section_headers(text_list, label)
        elif mode_flg == 'pull_out_section_header_to_bottom_of_report':
            self._extract_section_to_bottom_of_report(text_list,
                                                      self._tagged_section_header(label))
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
                    self.lambda_manager.lambda_conversion(match_str,
                                                          self.text,
                                                          '\n\n' + section_lbl + ' N\n\n')
            self.text = \
                self.lambda_manager.lambda_conversion(section_lbl + ' N(\n+' + section_lbl + ' N\n+)+',
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
        return('(:|\.|\n)([\n\s]*|$)')
        
    #
    def _pre_punct(self):
        return('(?i)(^|\n)')
    
    #
    def _remove_from_keywords_text(self, keyword, index_flg=1):
        self.dynamic_data_manager.remove_from_keywords_text(keyword, index_flg)
        
    #
    def _tagged_section_header(self, untagged_text):
        tagged_text = \
            self.section_header_pre_tag + untagged_text + self.section_header_post_tag
        return tagged_text

    #
    def amendment_section_header(self, mode_flg, text):
        self.text = text
        self.text = \
            self.lambda_manager.lambda_conversion(self._tagged_section_header('AMENDMENT COMMENT'),
                                                  self.text,
                                                  self._tagged_section_header('AMENDMENT_COMMENT'))
        section_header = 'AMENDMENT'
        text_list = \
            self.section_header.get_amendment_text_list(section_header)
        self._extract_section_to_bottom_of_report(text_list,
                                                  self._tagged_section_header('AMENDMENT'))
        self._append_keywords_text(self._tagged_section_header('AMENDMENT'))
        self.text = \
            self.lambda_manager.lambda_conversion(self._tagged_section_header('AMENDMENT_COMMENT'),
                                                  self.text,
                                                  self._tagged_section_header('AMENDMENT COMMENT'))
        return self.text
        
    #
    def clear_section_header_tags(self, text):
        self.text = text
        self.text = \
            self.lambda_manager.lambda_conversion(' > > >', self.text, self.section_header_post_tag)
        self.text = \
            self.lambda_manager.lambda_conversion('< < < ', self.text, self.section_header_pre_tag)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion(self.section_header_pre_tag, self.text)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion(self.section_header_post_tag, self.text)
        return self.text
    
    #
    def comment_section_header(self, mode_flg, text):
        self.text = text
        regex_list = []
        if mode_flg == 'pull_out_section_header_to_bottom_of_report':
            regex_list.append(self._pre_punct() + 'comment' + s() + ' (\([^\)]*\))?' + self._post_punct())
            regex_list.append(self._pre_punct() + 'comment' + s() + ' (for specimen )?[A-Z]' + self._post_punct())
            regex_list.append(self._pre_punct() + 'comment' + s() + self._post_punct())
            regex_list.append(self._pre_punct() + '(\()?comment' + s() + '[\n\s]*:')
            regex_list.append(self._pre_punct() + 'note' + self._post_punct())
            regex_list.append(self._pre_punct() + 'note\s+\([^\)]*\)' + self._post_punct())
            regex_list.append(self._pre_punct() + 'note (\([^\)]*\))?' + self._post_punct())
            regex_list.append(self._pre_punct() + 'note( [A-Z])?' + self._post_punct())
        elif mode_flg == 'unformatted':
            regex_list = []
            regex_list.append('comment' + s())
            regex_list.append('miscellaneous')
            regex_list.append('(?<!labs to\n\n)note')
            regex_list.append(patient() + ' ?/ ?family baseline understanding')
            regex_list.append(patient() + ' ?/ ?family readiness to learn')
            regex_list.append(patient() + ' ?/ ?family responses to teaching')
            regex_list.append('regarding')
            regex_list.append('teaching provided')
            regex_list.append('visit type')
            
        if mode_flg == 'formatted':
            no_punctuation_flg = False
        elif mode_flg == 'unformatted':
            no_punctuation_flg = True
        else:
            no_punctuation_flg = False
        if mode_flg == 'formatted':
            text_list = self._add_punctuation_formatted(regex_list)
        elif mode_flg == 'unformatted':
            text_list = self._add_punctuation_unformatted(regex_list,
                                                          no_punctuation_flg)
        else:
            text_list = regex_list
        self._normalize_section_header(mode_flg, text_list, 'COMMENT')
        return self.text
        
    #
    def fix_section_headers(self, text):
        self.text = text
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?i)(?<=\nperipheral blood,)\n\n\nflow cytometric analysis \d+',
                                                           self.text)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?i)(?<=\nperipheral blood, smear and)\n\n\nflow cytometric analysis \d+',
                                                           self.text)
        return self.text
    
    #
    def history_section_header(self, mode_flg):
        section_header = 'FAMILY HISTORY'
        text_list, no_punctuation_flg = \
            self.section_header.get_text_list(section_header, mode_flg)
        section_header = 'FAMILY HSTRY'
        self._normalize_section_header(mode_flg, text_list, section_header)
        regex_list = []
        if mode_flg == 'formatted':
            regex_list.append('(PMH|PSH)')
        elif mode_flg == 'unformated':
            regex_list.append('(PMH|PSH) :')
        regex_list.append('(brief|past) ' + history())
        regex_list.append(patient() + ' ' + history())
        regex_list.append('(?!<family )' + history())
        regex_list.append('(?<!' + patient() + ') id( |/hpi)')
        
        if mode_flg == 'formatted':
            no_punctuation_flg = False
        elif mode_flg == 'unformatted':
            no_punctuation_flg = True
        else:
            no_punctuation_flg = False
        if mode_flg == 'formatted':
            text_list = self._add_punctuation_formatted(regex_list)
        elif mode_flg == 'unformatted':
            text_list = self._add_punctuation_unformatted(regex_list,
                                                          no_punctuation_flg)
        else:
            text_list = regex_list  
        
        self._normalize_section_header(mode_flg, text_list, 'HISTORY')
        self.text = \
            self.lambda_manager.lambda_conversion('FAMILY HSTRY', self.text, 'FAMILY HISTORY')
        self._append_keywords_text('FAMILY HISTORY')
        self._remove_from_keywords_text('FAMILY HSTRY')
        
    #
    def normalize_section_header(self, mode_flg, text):
        self.text = text
        section_header_list = self.section_header.get_section_header_list()
        for section_header in section_header_list:
            text_list, no_punctuation_flg = \
                self.section_header.get_text_list(section_header, mode_flg)
            self._normalize_section_header(mode_flg, text_list, section_header)
        return self.text
            
    #
    def pull_dynamic_data_manager(self):
        return self.dynamic_data_manager
        
    #
    def push_dynamic_data_manager(self, dynamic_data_manager):
        self.dynamic_data_manager = dynamic_data_manager