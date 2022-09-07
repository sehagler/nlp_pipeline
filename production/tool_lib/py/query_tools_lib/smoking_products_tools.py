# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 13:49:19 2019

@author: haglers
"""

#
import re
import statistics

#
from tool_lib.py.query_tools_lib.base_lib.postprocessor_base_class \
    import Postprocessor_base

#
class Postprocessor(Postprocessor_base):
        
    #
    def _extract_data_value(self, value_list_dict):
        extracted_data_dict = {}
        for key in value_list_dict.keys():
            text_list = value_list_dict[key]
            smoking_products_text_list = []
            context_text_list = []
            for item in text_list[0]:
                smoking_products_text_list.append(item[0])
                context_text_list.append(item[1])
            normalized_smoking_products_text_list = \
                self._process_smoking_products_text_list(smoking_products_text_list)
            value_list = []
            for i in range(len(smoking_products_text_list)):
                value_list.append((smoking_products_text_list[i],
                                   normalized_smoking_products_text_list[i],
                                   context_text_list[i]))
            value_dict_list = []
            for value in value_list:
                if value[1] is not None:
                    value_dict = {}
                    value_dict['SMOKING_PRODUCTS'] = value[0]
                    value_dict['NORMALIZED_SMOKING_PRODUCTS'] = value[1]
                    value_dict['SNIPPET'] = value[2]
                    value_dict_list.append(value_dict)
            extracted_data_dict[key] = value_dict_list
        return extracted_data_dict
    
    #
    def _process_smoking_products_text_list(self, smoking_products_text_list):
        value_list = []
        for text in smoking_products_text_list:
            value_sublist = []
            if re.search('(?i)(?<!e-)cigar(s)?(?!ette)', text) is not None:
                match = re.search('(?i)(?<!e-)cigar(s)?(?!ette)', text)
                value = match.group(0)
                value = \
                    self.lambda_manager.lambda_conversion('(?i)cigar(s)?', value, 'cigars')
                value_sublist.append(value.lower())
            if re.search('(?i)(?<!e-)cigarette(s)?', text) is not None:
                match = re.search('(?i)(?<!e-)cigarette(s)?', text)
                value = match.group(0)
                value = \
                    self.lambda_manager.lambda_conversion('(?i)cigarette(s)?', value, 'cigarettes')
                value_sublist.append(value.lower())
            if re.search('(?i)e-cigarette(s)?', text) is not None:
                match = re.search('(?i)e-cigarette(s)?', text)
                value = match.group(0)
                value = \
                    self.lambda_manager.lambda_conversion('(?i)e-cigarette(s)?', value, 'e-cigarettes')
                value_sublist.append(value.lower())
            if re.search('(?i)(marijuana|pipe|thc)', text):
                value = 'other'
                value_sublist.append(value.lower())
            if re.search('(?i)(packs?|pp[dwy])', text):
                value_sublist.append('cigarettes')
            value_sublist = list(set(value_sublist))
            value_str = ''
            for value in value_sublist:
                value_str += value + ', '
            value_str = value_str[:-2]
            value_list.append(value_str)
        return value_list