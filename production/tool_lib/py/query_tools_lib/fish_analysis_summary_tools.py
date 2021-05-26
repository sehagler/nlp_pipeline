# -*- coding: utf-8 -*-
"""
Created on Fri Feb 01 13:28:54 2019

@author: haglers
"""

#
import re

#
from nlp_lib.py.postprocessing_lib.base_class_lib.postprocessor_base_class \
    import Postprocessor_base

#
class Postprocessor(Postprocessor_base):
    
    #
    def __init__(self,project_data, data_file, data_key_map, data_value_map,
                 label):
        Postprocessor_base.__init__(self, project_data, label, data_file, None,
                                    None)
        for i in range(len(self.data_dict_list)):
            self.data_dict_list[i][self.nlp_data_key] = {}
        self._create_data_structure('FISH ANALYSIS SUMMARY \d')
        self._extract_data_values()
        
    #
    def _extract_data_value(self, text_list):
        if len(text_list) > 0:
            text_list = text_list[0]
        entry_text = text_list[0]
        entry_text = re.sub('\( ', '(', entry_text)
        entry_text = re.sub(' (?=(:|,|\)))', '', entry_text)
        entry_text = re.sub('(?i)preliminary (report date|results).*', '', entry_text)
        entry_text = re.sub('(?i)\*\*amended (for|to).*', '', entry_text)
        entry_text = re.sub(':[ \n\t]*$', '', entry_text)
        value_list = []
        value_list.append(entry_text)
        value_dict_list = []
        for value in value_list:
            value_dict = {}
            value_dict['FISH_ANALYSIS_SUMMARY'] = value
            value_dict_list.append(value_dict)
        return value_dict_list