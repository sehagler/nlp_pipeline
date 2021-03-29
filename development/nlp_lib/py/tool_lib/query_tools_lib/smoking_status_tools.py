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
    def __init__(self, project_data, data_file, data_key_map, data_value_map,
                 label):
        Postprocessor_base.__init__(self, project_data, label, data_file,
                                    data_key_map, data_value_map)
        self._get_smoking_status()
        
    #
    def _get_smoking_status(self):
        for i in range(len(self.data_dict_list)):
            for key in self.data_dict_list[i][self.nlp_data_key]:
                try:
                    text_list = \
                        self.data_dict_list[i][self.nlp_data_key][key][self.label][self.nlp_text_key]
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
                self._append_data(i, key, value_list)