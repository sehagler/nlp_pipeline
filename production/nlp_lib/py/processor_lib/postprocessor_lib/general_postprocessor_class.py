# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 10:37:36 2021

@author: haglers
"""

#
from nlp_lib.py.base_class_lib.postprocessor_base_class import Postprocessor_base

#
class General_postprocessor(Postprocessor_base):
    
    #
    def __init__(self, data_file, data_key_map, data_value_map, label):
        Postprocessor_base.__init__(self, label, data_file, data_key_map, 
                                    data_value_map)
        for i in range(len(self.data_dict_list)):
            for key in self.data_dict_list[i][self.nlp_data_key]:
                self._append_data(i, key, [])