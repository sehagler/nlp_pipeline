# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 12:32:58 2019

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
    def __init__(self, project_data, csv_file, data_key_map, data_value_map,
                 label, diagnosis_reader):
        Postprocessor_base.__init__(self, project_data, label, csv_file,
                                    data_key_map, data_value_map)
        self.data_key_map = data_key_map
        self.diagnosis_reader = diagnosis_reader
        self._extract_data_values()
        
    #
    def _extract_data_value(self, text_list):
        if len(text_list) > 0:
            text_list = text_list[0]
        diagnosis_keys = self.diagnosis_reader.get_keys()
        diagnosis_text = text_list[0]
        value_list = []
        if not re.search('(?i)(not?|rather)', diagnosis_text):
            diagnosis = ''
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
        value_dict_list = []
        for value in value_list:
            value_dict = {}
            value_dict['DIAGNOSIS'] = value
            value_dict_list.append(value_dict)
        return value_dict_list