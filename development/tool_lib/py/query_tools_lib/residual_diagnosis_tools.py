# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 10:37:14 2019

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
    def __init__(self, static_data, data_file):
        Postprocessor_base.__init__(self, static_data, data_file)
        self._extract_data_values()
        
    #
    def _extract_data_value(self, text_list):
        text_list = text_list[0]
        value_list = text_list
        value_dict_list = []
        for value in value_list:
            value_dict = {}
            value_dict['DIAGNOSIS'] = value
            value_dict_list.append(value_dict)
        return value_dict_list