# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 12:32:58 2019

@author: haglers
"""

#
import re

#
from nlp_lib.py.base_class_lib.postprocessor_base_class import Postprocessor_base

#
class Postprocessor(Postprocessor_base):
    
    #
    def __init__(self, csv_file, data_key_map, data_value_map, diagnosis_reader):
        self.data_key_map = data_key_map
        self.diagnosis_reader = diagnosis_reader
        Postprocessor_base.__init__(self, csv_file, data_key_map, data_value_map, None)
        self._get_diagnosis()
        
    #
    def _get_diagnosis(self):
        diagnosis_keys = self.diagnosis_reader.get_keys()
        for i in range(len(self.data_dict_list)):
            for key in self.data_dict_list[i]['DATA']:
                if self.data_key_map['EXTRACTED_TEXT'] in self.data_dict_list[i]['DATA'][key].keys():
                    for diagnosis_text in self.data_dict_list[i]['DATA'][key][self.data_key_map['EXTRACTED_TEXT']]:
                        if not re.search('(?i)(not?|rather)', diagnosis_text):
                            diagnosis = ''
                            for diagnosis_key in diagnosis_keys:
                                diagnosis_dict = self.diagnosis_reader.get_dict_by_key(diagnosis_key)
                                if diagnosis_dict['abbreviation'] != '':
                                    diagnosis = diagnosis_dict['abbreviation']
                                else:
                                    diagnosis = diagnosis_key
                                if re.search('(?i)(?<!/)' + diagnosis + '(?![\-/])', diagnosis_text):
                                    if 'DIAGNOSIS' not in self.data_dict_list[i]['DATA'][key].keys():
                                        self.data_dict_list[i]['DATA'][key]['DIAGNOSIS'] = []
                                    self.data_dict_list[i]['DATA'][key]['DIAGNOSIS'].append(diagnosis_key)