# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 12:13:23 2019

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
    def __init__(self, static_data, data_file, diagnosis_reader):
        Postprocessor_base.__init__(self, static_data, data_file,
                                    query_name='SPECIFIC_DIAGNOSIS')
        self.diagnosis_reader = diagnosis_reader
        for i in range(len(self.data_dict_list)):
            self.data_dict_list[i][self.nlp_data_key] = {}
        self._create_data_structure('(COMMENT|NOTE|SUMMARY)')
        self._extract_data_values()
        
    #
    def _extract_data_value(self, text_list):
        value_list = []
        if len(text_list) > 0:
            text_list = text_list[0]
        diagnosis_keys = self.diagnosis_reader.get_keys()
        entry_txt = text_list[0]
        entry_txt = re.sub('\(.*?\)', '', entry_txt)
        entry_txt = re.sub(' +', ' ', entry_txt)
        del_key = True
        for diagnosis_key in diagnosis_keys:
            diagnosis_dict = self.diagnosis_reader.get_dict_by_key(diagnosis_key)
            for diagnosis in diagnosis_dict['specific_diagnosis']:
                if not re.search('(?i)no evidence of marrow involvement by ' + diagnosis, entry_txt):
                    if re.search('(?i)(?<!/)' + diagnosis + '(?!/)', entry_txt):
                        del_key = False
                        value_list.append((diagnosis_key, diagnosis))
        value_dict_list = []
        for value in value_list:
            value_dict = {}
            value_dict['DIAGNOSIS'] = value
            value_dict_list.append(value_dict)
        return value_dict_list