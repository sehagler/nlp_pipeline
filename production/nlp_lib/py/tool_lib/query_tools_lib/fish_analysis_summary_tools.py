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
    def __init__(self, csv_file):
        Postprocessor_base.__init__(self, csv_file, None, None, None)
        for i in range(len(self.data_dict_list)):
            self.data_dict_list[i]['DATA'] = {}
        self._get_fish_analysis_summary()
        
    #
    def _get_fish_analysis_summary(self):
        for i in range(len(self.data_dict_list)):
            for entry in self.data_dict_list[i]['DOCUMENT_FRAME']:
                if re.match('FISH ANALYSIS SUMMARY \d', entry[0][0]):
                    key = entry[0]
                    value = entry[1]
                    value = re.sub('\( ', '(', value)
                    value = re.sub(' (?=(:|,|\)))', '', value)
                    value = re.sub('(?i)preliminary (report date|results).*', '', value)
                    value = re.sub('(?i)\*\*amended (for|to).*', '', value)
                    value = re.sub(':[ \n\t]*$', '', value)
                    if key not in self.data_dict_list[i]['DATA'].keys():
                        self.data_dict_list[i]['DATA'][key] = {}
                    if 'FISH ANALYSIS SUMMARY TEXT' not in self.data_dict_list[i]['DATA'][key].keys():
                        self.data_dict_list[i]['DATA'][key]['FISH ANALYSIS SUMMARY TEXT'] = []
                    self.data_dict_list[i]['DATA'][key]['FISH ANALYSIS SUMMARY TEXT'].append(value)