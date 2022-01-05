# -*- coding: utf-8 -*-
"""
Created on Fri Feb 01 13:28:54 2019

@author: haglers
"""

#
import re

#
from nlp_lib.py.base_lib.postprocessor_base_class \
    import Postprocessor_base
from nlp_lib.py.base_lib.preprocessor_base_class \
    import Preprocessor_base

#
class Postprocessor(Postprocessor_base):
 
    #
    def _extract_data_value(self, text_list):
        text_list = text_list[0]
        if len(text_list) > 0:
            text_list = text_list[0]
        entry_text = text_list[0]
        entry_text = re.sub('\( ', '(', entry_text)
        entry_text = re.sub(' (?=(:|,|\)))', '', entry_text)
        entry_text = re.sub('(?i)preliminary (report|results).*', '', entry_text)
        entry_text = re.sub('(?i)(\*\*)?amended (for|to).*', '', entry_text)
        entry_text = re.sub(':[ \n\t]*$', '', entry_text)
        value_list = []
        value_list.append(entry_text)
        value_dict_list = []
        for value in value_list:
            value_dict = {}
            value_dict['FISH_ANALYSIS_SUMMARY'] = value
            value_dict_list.append(value_dict)
        return value_dict_list
    
    #
    def run_postprocessor(self):
        Postprocessor_base.run_postprocessor(self,
                                             query_name='FISH_ANALYSIS_SUMMARY',
                                             section_name='FISH ANALYSIS SUMMARY \d')
    
#
class Summarization(Preprocessor_base):
    
    #
    def run_preprocessor(self):
        self._clear_command_list()
        self._general_command('(?i)[\n\s]+by FISH', {None : ''})
        self._process_command_list()