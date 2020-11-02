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
    def __init__(self, csv_file, data_key_map, data_value_map):
        Postprocessor_base.__init__(self, csv_file, data_key_map, data_value_map, None)
        self._get_fab_value()
        
    #
    def _get_fab_value(self):
        for i in range(len(self.data_dict_list)):
            for key in self.data_dict_list[i]['DATA']:
                value_list = []
                try:
                    text_list = self.data_dict_list[i]['DATA'][key]['FAB CLASSIFICATION TEXT']
                except:
                    text_list = []
                for text in text_list:
                    text = re.sub(' (?=[0-9])', ' M', text)
                    text = re.sub('(AML|FAB)[\- ]', '', text)
                    text = re.sub('[\(\)]', '', text)
                    text = re.sub(' ', '', text)
                    text = re.sub('.*(?=M)', '', text)
                    value_list.append(text)
                self.data_dict_list[i]['DATA'][key]['FAB CLASSIFICATION VALUE'] = value_list