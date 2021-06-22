# -*- coding: utf-8 -*-
"""
Created on Tue May 12 17:04:28 2020

@author: haglers
"""

#
import re

#
from nlp_lib.py.document_preprocessing_lib.base_class_lib.preprocessor_base_class import Preprocessor_base
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
    def amendment_section_header(self, mode_flg):
        section_header = 'AMENDMENT COMMENT'
        regex_list = self.section_header_dict[section_header]
        self._pull_out_section_header_to_bottom_of_report(regex_list, self._tagged_section_header('AMENDMENT COMMENT'), True)
        self._general_command(self._tagged_section_header('AMENDMENT COMMENT'), {None : self._tagged_section_header('AMENDMENT_COMMENT')})
        section_header = 'AMENDMENT'
        regex_list = self.section_header_dict[section_header]
        self._pull_out_section_header_to_bottom_of_report(regex_list, self._tagged_section_header('AMENDMENT'), True)
        self._general_command(self._tagged_section_header('AMENDMENT_COMMENT'), {None : self._tagged_section_header('AMENDMENT COMMENT')})
            
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
            
    #
    def general_command(self, section_header_list, mode_flg):
        for section_header in section_header_list:
            regex_list = self.section_header_dict[section_header]
            self._general_command(regex_list,
                                  self._tagged_section_header(section_header),
                                  True)
        
    #
    def normalize_section_header(self, section_header_list, mode_flg):
        for section_header in section_header_list:
            if mode_flg == 'formatted':
                no_punctuation_flg = False
            elif mode_flg == 'unformatted':
                no_punctuation_flg = True
            regex_list = self.section_header_dict[section_header]
            self._normalize_section_header(mode_flg, regex_list,
                                           section_header,
                                           no_punctuation_flg=no_punctuation_flg)
            
    #
    def pull_dynamic_data_manager(self):
        return self.dynamic_data_manager
        
    #
    def push_dynamic_data_manager(self, dynamic_data_manager):
        self.dynamic_data_manager = dynamic_data_manager