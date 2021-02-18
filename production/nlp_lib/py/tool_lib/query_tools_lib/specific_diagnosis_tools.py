# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 12:13:23 2019

@author: haglers
"""

#
import re

#
from nlp_lib.py.base_class_lib.postprocessor_base_class import Postprocessor_base

#
class Postprocessor(Postprocessor_base):
    
    #
    def __init__(self, csv_file, diagnosis_reader):
        self.diagnosis_reader = diagnosis_reader
        Postprocessor_base.__init__(self, csv_file, None, None, None)
        for i in range(len(self.data_dict_list)):
            self.data_dict_list[i]['DATA'] = {}
        self._get_specific_diagnosis()
                            
    #
    def _get_specific_diagnosis(self):
        diagnosis_keys = self.diagnosis_reader.get_keys()
        for i in range(len(self.data_dict_list)):
            for entry in self.data_dict_list[i]['DOCUMENT_FRAME']:
                if re.match('(COMMENT|NOTE|SUMMARY)', entry[0][0]):
                    entry_txt = entry[1]
                    entry_txt = re.sub('\(.*?\)', '', entry_txt)
                    entry_txt = re.sub(' +', ' ', entry_txt)
                    for diagnosis_key in diagnosis_keys:
                        diagnosis_dict = self.diagnosis_reader.get_dict_by_key(diagnosis_key)
                        for diagnosis in diagnosis_dict['specific_diagnosis']:
                            if not re.search('(?i)no evidence of marrow involvement by ' + diagnosis, entry_txt):
                                if re.search('(?i)(?<!/)' + diagnosis + '(?!/)', entry_txt):
                                    key = entry[0]
                                    if 'DATA' not in self.data_dict_list[i]:
                                        self.data_dict_list[i]['DATA'] = {}
                                    if key not in self.data_dict_list[i]['DATA'].keys():
                                        self.data_dict_list[i]['DATA'][key] = {}
                                    if key not in self.data_dict_list[i]['DATA'].keys():
                                        self.data_dict_list[i]['DATA'][key] = {}
                                    if 'DIAGNOSIS' not in self.data_dict_list[i]['DATA'][key].keys():
                                        self.data_dict_list[i]['DATA'][key]['DIAGNOSIS'] = []
                                    self.data_dict_list[i]['DATA'][key]['DIAGNOSIS'].append(diagnosis_key)
                                    if 'SPECIFIC DIAGNOSIS TEXT' not in self.data_dict_list[i]['DATA'][key].keys():
                                        self.data_dict_list[i]['DATA'][key]['SPECIFIC DIAGNOSIS TEXT'] = []
                                    self.data_dict_list[i]['DATA'][key]['SPECIFIC DIAGNOSIS TEXT'].append(diagnosis)