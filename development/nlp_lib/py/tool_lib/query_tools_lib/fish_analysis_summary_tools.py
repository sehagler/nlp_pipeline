# -*- coding: utf-8 -*-
"""
Created on Fri Feb 01 13:28:54 2019

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
        Postprocessor_base.__init__(self, label, data_file, None, None)
        for i in range(len(self.data_dict_list)):
            self.data_dict_list[i][self.nlp_data_key] = {}
        self._create_data_structure('FISH ANALYSIS SUMMARY \d')
        self._get_fish_analysis_summary()
        
    #
    def _get_fish_analysis_summary(self):
        for i in range(len(self.data_dict_list)):
            for key in self.data_dict_list[i][self.nlp_data_key]:
                entry_text = \
                    self.data_dict_list[i][self.nlp_data_key][key][self.label][self.nlp_text_key][0]
                entry_text = re.sub('\( ', '(', entry_text)
                entry_text = re.sub(' (?=(:|,|\)))', '', entry_text)
                entry_text = re.sub('(?i)preliminary (report date|results).*', '', entry_text)
                entry_text = re.sub('(?i)\*\*amended (for|to).*', '', entry_text)
                entry_text = re.sub(':[ \n\t]*$', '', entry_text)
                self.data_dict_list[i][self.nlp_data_key][key][self.label][self.nlp_text_key] = []
                self.data_dict_list[i][self.nlp_data_key][key][self.label][self.nlp_text_key].append(entry_text)
                self._append_data(i, key, [])