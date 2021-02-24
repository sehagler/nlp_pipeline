# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 10:37:14 2019

@author: haglers
"""

#
import re

#
from nlp_lib.py.base_class_lib.postprocessor_base_class import Postprocessor_base

#
class Postprocessor(Postprocessor_base):
    
    #
    def __init__(self, data_file, data_key_map, data_value_map, label):
        Postprocessor_base.__init__(self, label, data_file, data_key_map,
                                    data_value_map)
        self._get_fab_value()
        
    #
    def _get_fab_value(self):
        for i in range(len(self.data_dict_list)):
            for key in self.data_dict_list[i][self.nlp_data_key]:
                value_list = []
                try:
                    text_list = \
                        self.data_dict_list[i][self.nlp_data_key][key][self.label][self.nlp_text_key]
                except:
                    text_list = []
                for text in text_list:
                    text = re.sub(' (?=[0-9])', ' M', text)
                    text = re.sub('(AML|FAB)[\- ]', '', text)
                    text = re.sub('[\(\)]', '', text)
                    text = re.sub(' ', '', text)
                    text = re.sub('.*(?=M)', '', text)
                    value_list.append(text)
                self._append_data(i, key, value_list)