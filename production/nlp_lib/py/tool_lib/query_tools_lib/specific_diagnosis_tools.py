# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 12:13:23 2019

@author: haglers
"""

#
from copy import deepcopy
import re

#
from nlp_lib.py.base_class_lib.postprocessor_base_class import Postprocessor_base

#
class Postprocessor(Postprocessor_base):
    
    #
    def __init__(self, data_file, data_key_map, data_value_map, label, diagnosis_reader):
        Postprocessor_base.__init__(self, label, data_file, None, None)
        self.diagnosis_reader = diagnosis_reader
        for i in range(len(self.data_dict_list)):
            self.data_dict_list[i][self.nlp_data_key] = {}
        self._create_data_structure('(COMMENT|NOTE|SUMMARY)')
        self._get_specific_diagnosis()
        
    #
    def _get_specific_diagnosis(self):
        diagnosis_keys = self.diagnosis_reader.get_keys()
        for i in range(len(self.data_dict_list)):
            del_keys = []
            for key in self.data_dict_list[i][self.nlp_data_key]:
                entry_txt = self.data_dict_list[i][self.nlp_data_key][key][self.label][self.nlp_text_key][0]
                entry_txt = re.sub('\(.*?\)', '', entry_txt)
                entry_txt = re.sub(' +', ' ', entry_txt)
                del_key = True
                for diagnosis_key in diagnosis_keys:
                    diagnosis_dict = self.diagnosis_reader.get_dict_by_key(diagnosis_key)
                    for diagnosis in diagnosis_dict['specific_diagnosis']:
                        if not re.search('(?i)no evidence of marrow involvement by ' + diagnosis, entry_txt):
                            if re.search('(?i)(?<!/)' + diagnosis + '(?!/)', entry_txt):
                                del_key = False
                                self.data_dict_list[i][self.nlp_data_key][key][self.label]['DIAGNOSIS'] = []
                                self.data_dict_list[i][self.nlp_data_key][key][self.label]['DIAGNOSIS'].append(diagnosis_key)
                                self.data_dict_list[i][self.nlp_data_key][key][self.label][self.nlp_text_key] = []
                                self.data_dict_list[i][self.nlp_data_key][key][self.label][self.nlp_text_key].append(diagnosis)
                                self._append_data(i, key, [])
                if del_key:
                    del_keys.append(key)
            for key in del_keys:
                del self.data_dict_list[i][self.nlp_data_key][key]