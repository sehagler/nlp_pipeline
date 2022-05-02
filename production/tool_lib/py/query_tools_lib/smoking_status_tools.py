# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 13:49:19 2019

@author: haglers
"""

#
import re

#
from nlp_pipeline_lib.py.base_lib.postprocessor_base_class \
    import Postprocessor_base

#
class Postprocessor(Postprocessor_base):
        
    #
    def _extract_data_value(self, value_list_dict):
        extracted_data_dict = {}
        for key in value_list_dict.keys():
            text_list = value_list_dict[key]
            smoking_status_text_list = []
            context_text_list = []
            for item in text_list[0]:
                smoking_status_text_list.append(item[0])
                context_text_list.append(item[1])
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
                value_dict['SNIPPET'] = value[2]
                value_dict_list.append(value_dict)
            extracted_data_dict[key] = value_dict_list
        return extracted_data_dict
    
    #
    def _process_smoking_status_text_list(self, smoking_status_text_list):
        value_list = []
        for text in smoking_status_text_list:
            value = 'MANUAL_REVIEW'
            if re.search('(?i)(abstain|quit)', text) is not None:
                value = 'former smoker'
            if re.search('(?i)current ((every|some) day )?(:|hx|smoker)', text) is not None:
                value = 'current smoker'
            if re.search('(?i)former', text) is not None:
                value = 'former smoker'
            if re.search('(?i)never', text) is not None:
                value = 'never smoker'
            if re.search('(?i)(?!no )smoking (:|hx)', text) is not None:
                value = 'current smoker'
            if re.search('(?i)no smoking hx', text) is not None:
                value = 'never smoker'
            value_list.append(value)
        return value_list