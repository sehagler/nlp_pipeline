# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 13:49:19 2019

@author: haglers
"""

#
import re
import statistics

#
from nlp_lib.py.base_class_lib.postprocessor_base_class import Postprocessor_base

#
class Postprocessor(Postprocessor_base):
    
    #
    def __init__(self, data_file, data_key_map, data_value_map, label):
        Postprocessor_base.__init__(self, label, data_file, data_key_map, 
                                    data_value_map)
        self._get_smoking_products()
        
    #
    def _get_smoking_products(self):
        for i in range(len(self.data_dict_list)):
            for key in self.data_dict_list[i][self.nlp_data_key]:
                try:
                    text_list = \
                        self.data_dict_list[i][self.nlp_data_key][key][self.label][self.nlp_text_key]
                except:
                    text_list = []
                value_list = []
                for text in text_list:
                    if re.search('(?i)(?<!e-)cigar(s)?(?!ette)', text) is not None:
                        match = re.search('(?i)(?<!e-)cigar(s)?(?!ette)', text)
                        value = match.group(0)
                        value = re.sub('(?i)cigar(s)?', 'cigars', value)
                        value_list.append(value.lower())
                    if re.search('(?i)(?<!e-)cigarette(s)?', text) is not None:
                        match = re.search('(?i)(?<!e-)cigarette(s)?', text)
                        value = match.group(0)
                        value = re.sub('(?i)cigarette(s)?', 'cigarettes', value)
                        value_list.append(value.lower())
                    if re.search('(?i)e-cigarette(s)?', text) is not None:
                        match = re.search('(?i)e-cigarette(s)?', text)
                        value = match.group(0)
                        value = re.sub('(?i)e-cigarette(s)?', 'e-cigarettes', value)
                        value_list.append(value.lower())
                    if re.search('(?i)(marijuana|pipe)', text):
                        value_list.append('other')
                    if re.search('(?i)(packs?|PPY)', text):
                        value_list.append('cigarettes')
                self._append_data(i, key, value_list)