# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 16:29:37 2021

@author: haglers
"""

#
import collections
import os

#
from nlp_lib.py.logger_lib.logger_class import Logger
from nlp_lib.py.tool_lib.processing_tools_lib.file_processing_tools \
    import read_json_file
    
#
class Validation_manager(object):
    
    #
    def __init__(self, project_data):
        self.directory_manager = project_data['directory_manager']
        self.log_dir = self.directory_manager.pull_directory('log_dir')
        self.logger = Logger(self.log_dir)
        self.nlp_data = self._read_nlp_data(project_data)
        self.project_data = project_data
        
    #
    def _compare_lists(self, x, y):
        display_data_flg = False
        try:
            if 'MULTIPLE VALUES' in x:
                x = 'MULTIPLE VALUES'
        except:
            pass
        if x is not 'MULTIPLE_VALUES':
            if y is not None:
                if len(x) > 0:
                    if collections.Counter(x) == collections.Counter(y):
                        result = 'true positive'
                    else:
                        display_data_flg = True
                        result = 'false positive'
                else:
                    display_data_flg = True
                    result = 'false negative'
            else:
                if len(x) > 0:
                    display_data_flg = True
                    result = 'false positive'
                else:
                    result = 'true negative'
        else:
            result = 'multiple values'
        #if display_data_flg:
        #        print(x)
        #        print(y)
        return result, display_data_flg
        
    #
    def _compare_values(self, x, y):
        display_data_flg = False
        try:
            if 'MULTIPLE VALUES' in x:
                x = 'MULTIPLE VALUES'
        except:
            pass
        if x is not 'MULTIPLE VALUES':
            if y is not None:
                if x is not None:
                    if str(x) == str(y):
                        result = 'true positive'
                    else:
                        display_data_flg = True
                        result = 'false positive + false negative'
                elif x is None:
                    display_data_flg = True
                    result = 'false negative'
            else:
                if x is not None:
                    display_data_flg = True
                    result = 'false positive'
                else:
                    result = 'true negative'
        else:
            result = 'multiple values'
        #if display_data_flg:
        #    print(str(x) + ' ' + str(y))
        return result, display_data_flg

    #
    def _performance_statistics(self, FN, FP, FP_plus_FN, TN, TP, N):
        #N = TP + TN + FN + FP + FP_plus_FN
        if N > 0:
            A = (TP + TN) / N
        else:
            A = -1
        if TP + FP + FP_plus_FN > 0:
            P = TP / (TP + FP + FP_plus_FN)
        else:
            P = -1
        if TP + FN > 0:
            R = TP / (TP + FN + FP_plus_FN)
        else:
            R = -1
        if P != -1 and R != -1:
            if P * R > 0:
                F1 = 2 / (1/P + 1/R)
            else:
                F1 = -1
        else:
            F1 = -1
        print(f'\taccuracy:  {A:.3f}')
        print(f'\tprecision: {P:.3f}')
        print(f'\trecall:    {R:.3f}')
        print(f'\tF1:        {F1:.3f}')
    
    #
    def _read_nlp_data(self, project_data):
        directory_manager = project_data['directory_manager']
        patient_identifiers = project_data['patient_identifiers']
        patient_list = project_data['patient_list']
        project_name = project_data['project_name']
        nlp_data = {}
        data_dir = directory_manager.pull_directory('processing_data_dir')
        nlp_data_tmp = \
            read_json_file(os.path.join(data_dir, project_name + '.json'))
        nlp_data_tmp = nlp_data_tmp['NLP_DATA']
        for item in nlp_data_tmp:
            for patient_identifier in patient_identifiers:
                try:
                    patient = item['RECORD_ID']['METADATA'][patient_identifier]
                except:
                    pass
            document_idx = item['RECORD_ID']['METADATA']['NLP_DOCUMENT_IDX']
            if patient in patient_list:
                nlp_data[document_idx] = item['RECORD_ID']
        return nlp_data