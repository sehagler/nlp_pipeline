# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 13:49:19 2019

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
    def __init__(self, project_data, data_file, data_key_map, data_value_map,
                 label):
        Postprocessor_base.__init__(self, project_data, label, data_file,
                                    data_key_map, data_value_map)
        self._extract_data_values()
        
    #
    def _extract_data_value(self, text_list):
        if len(text_list) > 0:
            smoking_status_text_list = text_list[0]
            context_text_list = text_list[1]
        else:
            smoking_status_text_list = []
            context_text_list = []
        normalized_smoking_status_text_list = \
            self._process_smoking_status_text_list(smoking_status_text_list)
        value_list = []
        for i in range(len(smoking_status_text_list)):
            value_list.append((smoking_status_text_list[i],
                               normalized_smoking_status_text_list[i],
                               context_text_list[i]))
        value_list = list(set(value_list))
        value_dict_list = []
        for value in value_list:
            value_dict = {}
            value_dict['SMOKING_STATUS'] = value[0]
            value_dict['NORMALIZED_SMOKING_STATUS'] = value[1]
            value_dict['CONTEXT'] = value[2]
            value_dict_list.append(value_dict)
        return value_dict_list
    
    #
    def _process_smoking_status_text_list(self, smoking_status_text_list):
        value_list = []
        for text in smoking_status_text_list:
            value_sublist = []
            if re.search('(?i)(abstain|quit)', text) is not None:
                value_sublist.append('former smoker')
            if re.search('(?i)current ((every|some) day )?(:|hx|smoker)', text) is not None:
                value_sublist.append('current smoker')
            if re.search('(?i)former', text) is not None:
                value_sublist.append('former smoker')
            if re.search('(?i)never', text) is not None:
                value_sublist.append('never smoker')
            if re.search('(?i)(?!no )smoking (:|hx)', text) is not None:
                value_sublist.append('current smoker')
            if re.search('(?i)no smoking hx', text) is not None:
                value_sublist.append('never smoker')
            value_sublist = list(set(value_sublist))
            if len(value_sublist) > 0:
                value_str = ''
                for value in value_sublist:
                    value_str += value + ''
                value_list.append(value_str)
            else:
                value_list.append('MANUAL_REVIEW')
        return value_list