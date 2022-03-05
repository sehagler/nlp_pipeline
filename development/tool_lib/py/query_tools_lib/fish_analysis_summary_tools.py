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
        fish_text_list = []
        for item in text_list[0]:
            fish_text_list.append(item[0])
        value_list = []
        for entry_text in fish_text_list:
            entry_text = re.sub('\( ', '(', entry_text)
            entry_text = re.sub(' (?=(:|,|\)))', '', entry_text)
            entry_text = re.sub('(?i)preliminary (report|results).*', '', entry_text)
            entry_text = re.sub('(?i)(\*\*)?amended (for|to).*', '', entry_text)
            entry_text = re.sub(':[ \n\t]*$', '', entry_text)
            value_list.append(entry_text)
        value_dict_list = []
        for value in value_list:
            value_dict = {}
            value_dict['FISH_ANALYSIS_SUMMARY'] = value
            value_dict_list.append(value_dict)
        return value_dict_list
    
#
class Summarization(Preprocessor_base):
    
    #
    def run_preprocessor(self):
        self._clear_command_list()
        self._general_command('(?i)[\n\s]+by FISH', {None : ''})
        self._process_command_list()
        
#
def template():
    template = None
    template_sections_list = [ 'FISH ANALYSIS SUMMARY' ]
    return template, template_sections_list