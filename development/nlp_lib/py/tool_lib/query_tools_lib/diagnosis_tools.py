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
    def __init__(self, project_data, csv_file, data_key_map, data_value_map,
                 label, diagnosis_reader):
        Postprocessor_base.__init__(self, project_data, label, csv_file,
                                    data_key_map, data_value_map)
        self.data_key_map = data_key_map
        self.diagnosis_reader = diagnosis_reader
        self._get_diagnosis()
        
    #
    def _get_diagnosis(self):
        diagnosis_keys = self.diagnosis_reader.get_keys()
        for i in range(len(self.data_dict_list)):
            del_keys = []
            for key in self.data_dict_list[i][self.nlp_data_key]:
                diagnosis_text = self.data_dict_list[i][self.nlp_data_key][key][self.label][self.nlp_text_key][0]
                if not re.search('(?i)(not?|rather)', diagnosis_text):
                    diagnosis = ''
                    value_list = []
                    for diagnosis_key in diagnosis_keys:
                        diagnosis_dict = self.diagnosis_reader.get_dict_by_key(diagnosis_key)
                        diagnoses_tmp = []
                        if diagnosis_dict['abbreviation'] != '':
                            diagnoses_tmp.append(diagnosis_dict['abbreviation'])
                        #diagnoses_tmp.extend(diagnosis_dict['specific_diagnosis'])
                        diagnoses_tmp = list(set(diagnoses_tmp))
                        diagnoses = []
                        if len(diagnoses_tmp) > 0:
                            diagnoses.extend(diagnoses_tmp)
                        else:
                            diagnoses.append(diagnosis_key)
                        for diagnosis in diagnoses:
                            if re.search('(?i)(?<!/)' + diagnosis + '(?![\-/])', diagnosis_text):
                                value_list.append(diagnosis_key)
                                '''
                                if 'DIAGNOSIS' not in self.data_dict_list[i][self.nlp_data_key][key].keys():
                                    self.data_dict_list[i][self.nlp_data_key][key]['DIAGNOSIS'] = []
                                self.data_dict_list[i][self.nlp_data_key][key]['DIAGNOSIS'].append(diagnosis_key)
                                '''
                    self._append_data(i, key, value_list)
                else:
                    del_keys.append(key)
            for key in del_keys:
                del self.data_dict_list[i][self.nlp_data_key][key]