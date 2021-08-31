# -*- coding: utf-8 -*-
"""
Created on Tue May 12 17:04:28 2020

@author: haglers
"""

#
import re

#
from nlp_lib.py.document_preprocessing_lib.base_class_lib.preprocessor_base_class\
    import Preprocessor_base
from tool_lib.py.processing_tools_lib.text_processing_tools \
    import amend, clinician, clinician_reviewed, history, patient, review_item, s
from tool_lib.py.structure_tools_lib.section_header_structure_tools \
    import Section_header_structure_tools

#
class Section_header_normalizer(Preprocessor_base):
    
    #
    def __init__(self, static_data):
        Preprocessor_base.__init__(self, static_data)
        section_header = Section_header_structure_tools()
        self.section_header_dict = section_header._section_header_dict()
        self.section_header_post_tag = '>>>'
        self.section_header_pre_tag = '<<<'
        
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
    def _normalize_formatted_section_header(self, regex_dict, label, keyword_flg=True):
        if isinstance(regex_dict, dict):
            for key in regex_dict.keys():
                text = []
                text_in = regex_dict[key]
                if 'PRE_PUNCT' in key and 'POST_PUNCT' in key:
                    if isinstance(text_in, list):
                        for i in range(len(text_in)):
                            text.append('(?i)(^|\n)' + text_in[i] + '(:|\.|\n)([\n\s]*|$)')
                    else:
                        text.append('(?i)(^|\n)' + text_in + '(:|\.|\n)([\n\s]*|$)')
                elif 'PRE_PUNCT' in key:
                    if isinstance(text_in, list):
                        for i in range(len(text_in)):
                            text.append('(?i)(^|\n)' + text_in[i])
                    else:
                        text.append('(?i)(^|\n)' + text_in)
                else:
                    if isinstance(text_in, list):
                        for i in range(len(text_in)):
                            text.append(text_in[i])
                    else:
                        text.append(text_in)
                self._clear_command_list()
                self._general_command(text, self._tagged_section_header(label), keyword_flg)
                self._process_command_list()
        else:
            text_in = regex_dict
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
    def _normalize_unformatted_section_header(self, regex_dict, label, no_punctuation_flg, keyword_flg=True):
        if isinstance(regex_dict, dict):
            for key in regex_dict.keys():
                text = []
                text_in = regex_dict[key]
                if isinstance(text_in, list):
                    for i in range(len(text_in)):
                            text.append('(?i)( |\n)' + text_in[i] + '(( updated)? \d+/\d+/\d+)?( )?(:|;)')
                else:
                    text.append('(?i)( |\n)' + text_in + '(( updated)? \d+/\d+/\d+)?( )?(:|;)')
                if no_punctuation_flg:
                    if isinstance(text_in, list):
                        for i in range(len(text_in)):
                            text_in_upper = text_in[i].upper()
                            text_in_upper = re.sub('\(\?I\)', '(?i)', text_in_upper)
                            text.append('(?<!<<<)' + text_in_upper)
                    else:
                        text_in_upper = text_in.upper()
                        text_in_upper = re.sub('\(\?I\)', '(?i)', text_in_upper)
                        text.append('(?<!<<<)' + text_in_upper)
                self._clear_command_list()
                self._general_command(text, self._tagged_section_header(label), keyword_flg)
                self._process_command_list()
        else:
            text_in = regex_dict
            text = []
            if isinstance(text_in, list):
                for i in range(len(text_in)):
                    text.append('(?i)( |\n)' + text_in[i] + '(( updated)? \d+/\d+/\d+)?( )?(:|;)')
            else:
                text.append('(?i)( |\n)' + text_in + '(( updated)? \d+/\d+/\d+)?( )?(:|;)')
            if no_punctuation_flg:
                if isinstance(text_in, list):
                    for i in range(len(text_in)):
                        text_in_upper = text_in[i].upper()
                        text_in_upper = re.sub('\(\?I\)', '(?i)', text_in_upper)
                        text.append('(?<!<<<)' + text_in_upper)
                else:
                    text_in_upper = text_in.upper()
                    text_in_upper = re.sub('\(\?I\)', '(?i)', text_in_upper)
                    text.append('(?<!<<<)' + text_in_upper)
            self._clear_command_list()
            self._general_command(text, self._tagged_section_header(label), keyword_flg)
            self._process_command_list()
        
    #
    def _normalize_section_header(self, mode_flg, text_in, label, no_punctuation_flg=False, keyword_flg=True):
        if mode_flg == 'formatted':
            self._normalize_formatted_section_header(text_in, label, keyword_flg)
        elif mode_flg == 'unformatted':
            self._normalize_unformatted_section_header(text_in, label,
                                                       no_punctuation_flg,
                                                       keyword_flg)
        elif mode_flg == 'pull_out_section_header_to_bottom_of_report':
            self._clear_command_list()
            self._pull_out_section_header_to_bottom_of_report(text_in,
                                                              self._tagged_section_header(label),
                                                              keyword_flg)
            self._process_command_list()
        else:
            print('unknown mode: ' + mode_flg)
            
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
    def _pull_out_section_header_to_bottom_of_report(self, command0, command1, keyword_flg=False):
        self._clear_command_list()
        self.command_list.append([ 0, command0, command1 ])
        if keyword_flg:
            self._append_keywords_text(command1)
        self._process_command_list()
        
    #
    def _tagged_section_header(self, untagged_text):
        tagged_text = \
            self.section_header_pre_tag + untagged_text + self.section_header_post_tag
        return tagged_text
    
    #
    def amendment_section_header(self, mode_flg):
        section_header = 'AMENDMENT COMMENT'
        regex_list = self.section_header_dict[section_header]
        self._pull_out_section_header_to_bottom_of_report(regex_list,
                                                          self._tagged_section_header('AMENDMENT COMMENT'),
                                                          True)
        self._general_command(self._tagged_section_header('AMENDMENT COMMENT'),
                              {None : self._tagged_section_header('AMENDMENT_COMMENT')})
        section_header = 'AMENDMENT'
        regex_list = self.section_header_dict[section_header]
        self._pull_out_section_header_to_bottom_of_report(regex_list,
                                                          self._tagged_section_header('AMENDMENT'),
                                                          True)
        self._general_command(self._tagged_section_header('AMENDMENT_COMMENT'),
                              {None : self._tagged_section_header('AMENDMENT COMMENT')})
            
    #
    def biomarkers_tests_section_header(self, mode_flg):
        regex_list = []
        regex_list.append('er, pr and her-2/neu immunohistochemical stains by computer assisted quantitative image analysis')
        regex_list.append('er, pr and her-2/neu tests')
        regex_list.append('er and pr tests')
        self._normalize_section_header(mode_flg, regex_list, 'BIOMARKERS TESTS')
        
    #
    def clear_section_header_tags(self):
        self.text = re.sub(' > > >', self.section_header_post_tag, self.text)
        self.text = re.sub('< < < ', self.section_header_pre_tag, self.text)
        self.text = re.sub(self.section_header_pre_tag, '', self.text)
        self.text = re.sub(self.section_header_post_tag, '', self.text)
    
    #
    def comment_section_header(self, mode_flg):
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
        self._normalize_section_header(mode_flg, regex_list, 'COMMENT')
        
    #
    def fix_section_headers(self):
        self.text = \
            re.sub('(?i)(?<=\nperipheral blood,)\n\n\nflow cytometric analysis \d+', '', self.text)
        self.text = \
            re.sub('(?i)(?<=\nperipheral blood, smear and)\n\n\nflow cytometric analysis \d+', '', self.text)
        
        
    #
    def general_command(self, section_header_list, mode_flg):
        for section_header in section_header_list:
            regex_list = self.section_header_dict[section_header]
            self._general_command(regex_list,
                                  self._tagged_section_header(section_header),
                                  True)
            
    #
    def history_section_header(self, mode_flg):
        section_header = 'FAMILY HISTORY'
        regex_list = self.section_header_dict[section_header]
        section_header = 'FAMILY HSTRY'
        if mode_flg == 'formatted':
            no_punctuation_flg = False
        elif mode_flg == 'unformatted':
            no_punctuation_flg = True
        self._normalize_section_header(mode_flg, regex_list,
                                       section_header,
                                       no_punctuation_flg=no_punctuation_flg,
                                       keyword_flg=False)
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
        self._normalize_section_header(mode_flg, regex_list, 'HISTORY',
                                       no_punctuation_flg=no_punctuation_flg)
        self.text = re.sub('FAMILY HSTRY', 'FAMILY HISTORY', self.text)
        self._append_keywords_text('FAMILY HISTORY')
        
    #
    def normalize_section_header(self, mode_flg):
        section_header_list = list(self.section_header_dict.keys())
        section_header_list.sort(key=len, reverse=True)
        for section_header in section_header_list:
            if mode_flg == 'formatted':
                no_punctuation_flg = False
            elif mode_flg == 'unformatted':
                no_punctuation_flg = True
            regex_list = self.section_header_dict[section_header]
            self._normalize_section_header(mode_flg, regex_list,
                                           section_header,
                                           no_punctuation_flg=no_punctuation_flg)
            
    '''
    #
    def person_section_header(self, mode_flg):
        regex_list = []
        if mode_flg == 'formatted':
            regex_list.append('discussed with[^ \d]')
            regex_list.append(review_item() + ' (' + amend() + '|' + clinician_reviewed() + ') by')
            regex_list.append(amend() + ' ' + clinician_reviewed() + ' by')
            regex_list.append('(frozen section diagnosis|intraoperative consult(ation)? diagnosis) ' + \
                             clinician_reviewed() + ' by')
            regex_list.append(clinician_reviewed() + ' by[^ \d]?')
        elif mode_flg == 'unformatted':
            regex_list.append(patient())
            regex_list.append('name of ' + clinician() + '/clinical support person notified')
            regex_list.append(patient() + ' (identification|name)')
            regex_list.append('(addended|performed|referred|requested) by')
            regex_list.append(clinician())
            regex_list.append('(primary care ' + clinician() + '|pcp)')
        self._normalize_section_header(mode_flg, regex_list, 'PERSON')
    '''
            
    #
    def pull_dynamic_data_manager(self):
        return self.dynamic_data_manager
        
    #
    def push_dynamic_data_manager(self, dynamic_data_manager):
        self.dynamic_data_manager = dynamic_data_manager