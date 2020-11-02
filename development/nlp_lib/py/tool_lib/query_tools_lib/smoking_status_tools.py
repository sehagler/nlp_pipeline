# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 13:49:19 2019

@author: haglers
"""

#
import re

#
from nlp_lib.py.base_class_lib.postprocessor_base_class import Postprocessor_base

#
class Postprocessor(Postprocessor_base):
    
    #
    def __init__(self, json_file, data_key_map, data_value_map, label):
        self.label = label
        Postprocessor_base.__init__(self, json_file, data_key_map, data_value_map, None)
        self._get_smoking_status()
        
    #
    def _get_smoking_status(self):
        for i in range(len(self.data_dict_list)):
            for key in self.data_dict_list[i]['DATA']:
                try:
                    text_list = self.data_dict_list[i]['DATA'][key][self.label + ' TEXT']
                except:
                    text_list = []
                value_list = []
                for text in text_list:
                    if re.search('(?i)(abstain|quit)', text) is not None:
                        value_list.append('former smoker')
                    if re.search('(?i)current ((every|some) day )?(:|hx|smoker)', text) is not None:
                        value_list.append('current smoker')
                    if re.search('(?i)former', text) is not None:
                        value_list.append('former smoker')
                    if re.search('(?i)never', text) is not None:
                        value_list.append('never smoker')
                    if re.search('(?i)(?!no )smoking (:|hx)', text) is not None:
                        value_list.append('current smoker')
                    if re.search('(?i)no smoking hx', text) is not None:
                        value_list.append('never smoker')
                if len(value_list) > 0:
                    value_list = list(set(value_list))
                    self.data_dict_list[i]['DATA'][key][self.label + ' VALUE']  = value_list