# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 13:49:19 2019

@author: haglers
"""

#
from decimal import Decimal
import re

#
from nlp_lib.py.base_lib.postprocessor_base_class \
    import Postprocessor_base

#
class Postprocessor(Postprocessor_base):
        
    #
    def _extract_data_value(self, text_list):
        smoking_history_text_list = []
        context_text_list = []
        for item in text_list[0]:
            smoking_history_text_list.append(item[0])
            context_text_list.append(item[1])
        normalized_smoking_history_text_list = \
            self._process_smoking_history_text_list(smoking_history_text_list)
        value_list = []
        for i in range(len(smoking_history_text_list)):
            value_list.append((smoking_history_text_list[i],
                               normalized_smoking_history_text_list[i],
                               context_text_list[i]))
        value_list = list(set(value_list))
        value_dict_list = []
        for value in value_list:
            value_dict = {}
            value_dict['SMOKING_HISTORY'] = value[0]
            value_dict['NORMALIZED_SMOKING_HISTORY'] = value[1]
            value_dict['SNIPPET'] = value[2]
            value_dict_list.append(value_dict)
        return value_dict_list
    
    #
    def _process_smoking_history_text_list(self, smoking_history_text_list):
        value_list = []
        for text in smoking_history_text_list:
            value_decimal = None
            if re.search('(?i)yrs since quitting( smoking)? :( ~)? [0-9]{1,2}(.[0-9])?', text) is not None:
                match = re.search('(?i)yrs since quitting( smoking)? :( ~)? [0-9]{1,2}(.[0-9])?', text)
                value = match.group(0)
                match = re.search('[0-9]{1,2}(.[0-9])?', value)
                value_decimal = Decimal(match.group(0))
            if re.search('(?i)quit( smoking)?( ~)? [0-9]{1,2}(.[0-9])?\+? yrs ago', text) is not None:
                match = re.search('(?i)quit( smoking)?( ~)? [0-9]{1,2}(.[0-9])?\+? yrs ago', text)
                value = match.group(0)
                match = re.search('[0-9]{1,2}(.[0-9])?', value)
                value_decimal = Decimal(match.group(0))
            if value_decimal is not None:
                if value_decimal < 1.0:
                    value = 'quit less than 1 year ago'
                elif value_decimal >= 1.0 and value_decimal < 6.0:
                    value = 'quit between 1 and 5 years ago'
                elif value_decimal >= 6.0 and value_decimal < 11.0:
                    value = 'quit between 6 and 10 years ago'
                elif value_decimal >= 11.0:
                    value = 'quit more than 10 years ago'
                value_list.append(value.lower())
            else:
                value_list.append('MANUAL_REVIEW')
        return value_list