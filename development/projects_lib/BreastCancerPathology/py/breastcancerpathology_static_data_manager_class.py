# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 09:57:35 2020

@author: haglers
"""

#
import os
import xlrd

#
from nlp_lib.py.static_data_lib.static_data_manager_class \
    import Static_data_manager
from tool_lib.py.processing_tools_lib.file_processing_tools \
    import read_xlsx_file

#
class BreastCancerPathology_static_data_manager(Static_data_manager):
    
    #
    def __init__(self, operation_mode, project_subdir, user, root_dir_flg):
        project_name = 'BreastCancerPathology'
        Static_data_manager.__init__(self, operation_mode, project_name, 
                                     project_subdir, user, root_dir_flg)
        self.project_subdir = project_subdir
        
    #
    def _trim_lists(self, document_list, patient_list):
        self.static_data['document_list'] = \
            list(set(self.static_data['document_list']).intersection(document_list))
        self.static_data['patient_list'] = \
            list(set(self.static_data['patient_list']).intersection(patient_list))
    
    #
    def get_static_data(self):
        self.static_data['document_identifiers'] = \
            [ 'CSN', 'SOURCE_SYSTEM_UNIQUE_ID' ]
        self.static_data['ohsu_nlp_template_files'] = \
            [ 'breast_cancer_tnm_stage.csv' ]
        self.static_data['validation_file'] = \
            'breastcancerpathology_testing.xlsx'
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
            docs_files = []
            docs_files.append(os.path.join(training_data_dir, 'training_docs.pkl'))
            groups_files = []
            groups_files.append(os.path.join(training_data_dir, 'training_groups.pkl'))
                
            self._include_lists(docs_files, groups_files, [1])
            
            raw_data_dir = \
                self.static_data['directory_manager'].pull_directory('raw_data_dir')
            raw_data_file = os.path.join(raw_data_dir, 'breastcancerpathology_testing.xlsx')
            book = read_xlsx_file(raw_data_file)
            sheet = book.sheet_by_index(0)
            patient_list = list(set(sheet.col_values(1)[1:]))
            document_list = list(set(sheet.col_values(2)[1:]))

            self._trim_lists(document_list, patient_list)

        return self.static_data