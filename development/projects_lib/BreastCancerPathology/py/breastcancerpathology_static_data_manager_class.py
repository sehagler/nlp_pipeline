# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 09:57:35 2020

@author: haglers
"""

#
import os
import pickle
import xlrd

#
from nlp_lib.py.static_data_lib.static_data_manager_class \
    import Static_data_manager

#
class BreastCancerPathology_static_data_manager(Static_data_manager):
    
    #
    def __init__(self, operation_mode, project_subdir, user, root_dir_flg):
        project_name = 'BreastCancerPathology'
        Static_data_manager.__init__(self, operation_mode, project_name, 
                                     project_subdir, user, root_dir_flg)
        self.project_subdir = project_subdir
    
    #
    def get_static_data(self):
        self.static_data['document_identifiers'] = [ 'CSN', 'SOURCE_SYSTEM_UNIQUE_ID' ]
        if self.project_subdir == 'test':
            self.static_data['raw_data_files'] = {}
            self.static_data['raw_data_files']['BreastCancerPathology.xls'] = {}
            self.static_data['raw_data_files']['BreastCancerPathology.xls']['DATETIME_FORMAT'] = '%m/%d/%Y'
            self.static_data['raw_data_files']['BreastCancerPathology.xls']['DOCUMENT_FRACTION'] = 0.5
            self.static_data['raw_data_files']['BreastCancerPathology.xls']['FORMATTING'] = 'formatted'
            self.static_data['raw_data_files']['BreastCancerPathology.xls']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['DORR_HAGLER_NLP_PATH_RESULTS_20211115_114000.XML'] = {}
            self.static_data['raw_data_files']['DORR_HAGLER_NLP_PATH_RESULTS_20211115_114000.XML']['DATETIME_FORMAT'] = '%m/%d/%Y'
            self.static_data['raw_data_files']['DORR_HAGLER_NLP_PATH_RESULTS_20211115_114000.XML']['DOCUMENT_FRACTION'] = 1.0
            self.static_data['raw_data_files']['DORR_HAGLER_NLP_PATH_RESULTS_20211115_114000.XML']['FORMATTING'] = 'formatted'
            self.static_data['raw_data_files']['DORR_HAGLER_NLP_PATH_RESULTS_20211115_114000.XML']['NLP_MODE'] = 'SOURCE_SYSTEM_RESULT_ID'
            self.static_data['raw_data_files']['DORR_HAGLER_NLP_PATH_RESULTS_20211115_114000.XML']['SOURCE_SYSTEM'] = 'BeakerAP'
            self.static_data['raw_data_files_sequence'] = [ 'BreastCancerPathology.xls',
                                                            'DORR_HAGLER_NLP_PATH_RESULTS_20211115_114000.XML' ]
            
            #
            if True:
                if self.static_data['root_dir_flg'] == 'X':
                    base_dir = 'Z:'
                elif self.static_data['root_dir_flg'] == 'Z':
                    base_dir = 'Z:'
                elif self.static_data['root_dir_flg'] == 'dev_server':
                    base_dir = '/home/groups/hopper2/RDW_NLP_WORKSPACE'
                elif self.static_data['root_dir_flg'] == 'prod_server':
                    base_dir = '/home/groups/hopper2/RDW_NLP_WORKSPACE'
                source_dir = base_dir + '/NLP/NLP_Source_Data/BreastCancerPathology'
                training_data_dir = source_dir + '/test/pkl'
                training_docs_file = \
                    os.path.join(training_data_dir, 'training_docs.pkl')
                training_groups_file = \
                    os.path.join(training_data_dir, 'training_groups.pkl')
                try:
                    self.static_data['document_list'] = []
                    idx_list = [0]
                    with open(training_docs_file, 'rb') as f:
                        document_list = pickle.load(f)
                    for idx in idx_list:
                        self.static_data['document_list'].extend(document_list[idx])
                    self.static_data['document_list'] = \
                        list(set(self.static_data['document_list']))
                except:
                    pass
                try:
                    self.static_data['patient_list'] = []
                    idx_list = [0]
                    with open(training_groups_file, 'rb') as f:
                        patient_lists = pickle.load(f)
                    patient_list = []
                    for idx in idx_list:
                        patient_list.extend(patient_lists[idx])
                    self.static_data['patient_list'].extend(patient_list)
                    self.static_data['patient_list'] = \
                        list(set(self.static_data['patient_list']))
                except:
                    pass        

        return self.static_data