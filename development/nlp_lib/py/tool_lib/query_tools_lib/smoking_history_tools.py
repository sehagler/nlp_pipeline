# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 13:49:19 2019

@author: haglers
"""

#
from decimal import Decimal
import re

#
from nlp_lib.py.base_class_lib.postprocessor_base_class import Postprocessor_base

#
class Postprocessor(Postprocessor_base):
    
    #
    def __init__(self, json_file, data_key_map, data_value_map, label):
        self.label = label
        Postprocessor_base.__init__(self, json_file, data_key_map, data_value_map, None)
        self._get_smoking_history()
        
    #
    def _get_smoking_history(self):
        for i in range(len(self.data_dict_list)):
            for key in self.data_dict_list[i]['DATA']:
                try:
                    text_list = self.data_dict_list[i]['DATA'][key][self.label + ' TEXT']
                except:
                    text_list = []
                value_list = []
                for text in text_list:
                    value_decimal = None
                    if re.search('(?i)yrs since quitting( smoking)? :( ~)? [0-9]{1,2}(.[0-9])?', text) is not None:
                        match = re.search('(?i)yrs since quitting( smoking)? :( ~)? [0-9]{1,2}(.[0-9])?', text)
                        value = match.group(0)
                        match = re.search('[0-9]{1,2}(.[0-9])?', value)
                        value_decimal = Decimal(match.group(0))
                    if re.search('(?i)quit( smoking)?( ~)? [0-9]{1,2}(.[0-9])?\+? yrs ago', text) is not None:
                        match = re.search('(?i)quit( smoking)?( ~)? [0-9]{1,2}(.[0-9])?\+? yrs ago', text)
                        value = match.group(0)
                        match = re.search('[0-9]{1,2}(.[0-9])?', value)
                        value_decimal = Decimal(match.group(0))
                    if value_decimal is not None:
                        if value_decimal < 1.0:
                            value = 'quit less than 1 year ago'
                        elif value_decimal >= 1.0 and value_decimal < 6.0:
                            value = 'quit between 1 and 5 years ago'
                        elif value_decimal >= 6.0 and value_decimal < 11.0:
                            value = 'quit between 6 and 10 years ago'
                        elif value_decimal >= 11.0:
                            value = 'quit more than 10 years ago'
                        value_list.append(value.lower())
                if len(value_list) > 0:
                    value_list = list(set(value_list))
                    self.data_dict_list[i]['DATA'][key][self.label + ' VALUE']  = value_list