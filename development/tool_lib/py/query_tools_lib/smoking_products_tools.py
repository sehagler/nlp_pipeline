# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 13:49:19 2019

@author: haglers
"""

#
import re
import statistics

#
from nlp_lib.py.base_lib.postprocessor_base_class \
    import Postprocessor_base

#
class Postprocessor(Postprocessor_base):
        
    #
    def _extract_data_value(self, text_list):
        text_list = text_list[0]
        if len(text_list) > 0:
            smoking_products_text_list = text_list[0]
            context_text_list = text_list[1]
        else:
            smoking_products_text_list = []
            context_text_list = []
        normalized_smoking_products_text_list = \
            self._process_smoking_products_text_list(smoking_products_text_list)
        value_list = []
        for i in range(len(smoking_products_text_list)):
            value_list.append((smoking_products_text_list[i],
                               normalized_smoking_products_text_list[i],
                               context_text_list[i]))
        value_list = list(set(value_list))
        value_dict_list = []
        for value in value_list:
            if value[1] is not None:
                value_dict = {}
                value_dict['SMOKING_PRODUCTS'] = value[0]
                value_dict['NORMALIZED_SMOKING_PRODUCTS'] = value[1]
                value_dict['CONTEXT'] = value[2]
                value_dict_list.append(value_dict)
        return value_dict_list
    
    #
    def _process_smoking_products_text_list(self, smoking_products_text_list):
        value_list = []
        for text in smoking_products_text_list:
            value_sublist = []
            if re.search('(?i)(?<!e-)cigar(s)?(?!ette)', text) is not None:
                match = re.search('(?i)(?<!e-)cigar(s)?(?!ette)', text)
                value = match.group(0)
                value = re.sub('(?i)cigar(s)?', 'cigars', value)
                value_sublist.append(value.lower())
            if re.search('(?i)(?<!e-)cigarette(s)?', text) is not None:
                match = re.search('(?i)(?<!e-)cigarette(s)?', text)
                value = match.group(0)
                value = re.sub('(?i)cigarette(s)?', 'cigarettes', value)
                value_sublist.append(value.lower())
            if re.search('(?i)e-cigarette(s)?', text) is not None:
                match = re.search('(?i)e-cigarette(s)?', text)
                value = match.group(0)
                value = re.sub('(?i)e-cigarette(s)?', 'e-cigarettes', value)
                value_sublist.append(value.lower())
            if re.search('(?i)(marijuana|pipe)', text):
                value = 'other'
                value_sublist.append(value.lower())
            if re.search('(?i)(packs?|PPY)', text):
                value_sublist.append('cigarettes')
            value_sublist = list(set(value_sublist))
            if len(value_sublist) > 0:
                value_str = ''
                for value in value_sublist:
                    value_str += value + ', '
                value_str = value_str[:-2]
                value_list.append(value_str)
            else:
                value_list.append('MANUAL_REVIEW')
        return value_list