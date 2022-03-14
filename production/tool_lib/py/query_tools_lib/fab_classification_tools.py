# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 10:37:14 2019

@author: haglers
"""

#
import re

#
from nlp_lib.py.base_lib.postprocessor_base_class \
    import Postprocessor_base

#
class Postprocessor(Postprocessor_base):
      
    #
    def _extract_data_value(self, text_list):
        fab_text_list = []
        for item in text_list[0]:
            fab_text_list.append(item[0])
        value_list = []
        for text in fab_text_list:
            text = re.sub(' (?=[0-9])', ' M', text)
            text = re.sub('(AML|FAB)[\- ]', '', text)
            text = re.sub('[\(\)]', '', text)
            text = re.sub(' ', '', text)
            text = re.sub('.*(?=M)', '', text)
            value_list.append(text)
        value_dict_list = []
        for value in value_list:
            value_dict = {}
            value_dict['FAB_CLASSIFICATION'] = value
            value_dict_list.append(value_dict)
        return value_dict_list