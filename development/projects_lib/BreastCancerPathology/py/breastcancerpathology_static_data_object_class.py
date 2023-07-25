# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 09:57:35 2020

@author: haglers
"""

#
import os

#
from static_data_lib.object_lib.static_data_object_class import Static_data_object
from tools_lib.processing_tools_lib.file_processing_tools \
    import read_xlsx_file

#
class BreastCancerPathology_static_data_object(Static_data_object):
    
    #
    def __init__(self, operation_mode, user, root_dir_flg, project_subdir=None):
        project_name = 'BreastCancerPathology'
        Static_data_object.__init__(self, operation_mode, user, root_dir_flg,
                                     project_name=project_name,
                                     project_subdir=project_subdir)
        self.project_subdir = project_subdir
        
        self.static_data['document_identifiers'] = \
            [ 'CSN', 'SOURCE_SYSTEM_UNIQUE_ID' ]
        if 'performance_data_files' in self.static_data.keys():
            self.static_data['performance_data_files'].append('CCC19/test/CCC19.performance.json')
            self.static_data['performance_data_files'].append('NewBiomarkers/test/NewBiomarkers.performance.json')
        self.static_data['queries_list'] = \
            [ ('ER_BLOCK', None, 'BREAST_CANCER_BIOMARKERS_ER', 'ER_BLOCK', 'single_value', True), 
              ('ER_PERCENTAGE', None, 'BREAST_CANCER_BIOMARKERS_ER', 'ER_PERCENTAGE', 'single_value', True),
              ('ER_SCORE', None, 'BREAST_CANCER_BIOMARKERS_ER', 'ER_SCORE', 'single_value', True),
              ('ER_STATUS', None, 'BREAST_CANCER_BIOMARKERS_ER', 'ER_STATUS', 'single_value', True),
              ('ER_STRENGTH', None, 'BREAST_CANCER_BIOMARKERS_ER', 'ER_STRENGTH', 'single_value', True),
              ('ER_VARIABILITY', None, 'BREAST_CANCER_BIOMARKERS_ER', 'ER_VARIABILITY', 'single_value', True),
              ('GATA3_BLOCK', None, 'BREAST_CANCER_BIOMARKERS_GATA3', 'GATA3_BLOCK', 'single_value', True),
              ('GATA3_STATUS', None, 'BREAST_CANCER_BIOMARKERS_GATA3', 'GATA3_STATUS', 'single_value', True),
              ('GATA3_VARIABILITY', None, 'BREAST_CANCER_BIOMARKERS_GATA3', 'GATA3_VARIABILITY', 'single_value', True),
              ('HER2_BLOCK', None, 'BREAST_CANCER_BIOMARKERS_HER2', 'HER2_BLOCK', 'single_value', True),
              ('HER2_PERCENTAGE', None, 'BREAST_CANCER_BIOMARKERS_HER2', 'HER2_PERCENTAGE', 'single_value', True),
              ('HER2_SCORE', None, 'BREAST_CANCER_BIOMARKERS_HER2', 'HER2_SCORE', 'single_value', True), 
              ('HER2_STATUS', None, 'BREAST_CANCER_BIOMARKERS_HER2', 'HER2_STATUS', 'single_value', True), 
              ('HER2_VARIABILITY', None, 'BREAST_CANCER_BIOMARKERS_HER2', 'HER2_VARIABILITY', 'single_value', True),
              ('KI67_BLOCK', None, 'BREAST_CANCER_BIOMARKERS_KI67', 'KI67_BLOCK', 'single_value', True),
              ('KI67_PERCENTAGE', None, 'BREAST_CANCER_BIOMARKERS_KI67', 'KI67_PERCENTAGE', 'single_value', True),
              #('KI67_STATUS', None, 'BREAST_CANCER_BIOMARKERS_KI67', 'KI67_STATUS', 'single_value', True),
              ('KI67_VARIABILITY', None, 'BREAST_CANCER_BIOMARKERS_KI67', 'KI67_VARIABILITY', 'single_value', True),
              ('PR_BLOCK', None, 'BREAST_CANCER_BIOMARKERS_PR', 'PR_BLOCK', 'single_value', True), 
              ('PR_PERCENTAGE', None, 'BREAST_CANCER_BIOMARKERS_PR', 'PR_PERCENTAGE', 'single_value', True),
              ('PR_SCORE', None, 'BREAST_CANCER_BIOMARKERS_PR', 'PR_SCORE', 'single_value', True), 
              ('PR_STATUS', None, 'BREAST_CANCER_BIOMARKERS_PR', 'PR_STATUS', 'single_value', True),
              ('PR_STRENGTH', None, 'BREAST_CANCER_BIOMARKERS_PR', 'PR_STRENGTH', 'single_value', True),
              ('PR_VARIABILITY', None, 'BREAST_CANCER_BIOMARKERS_PR', 'PR_VARIABILITY', 'single_value', True),
              ('TNM_STAGING', None, 'TNM_STAGING', 'TNM_STAGING', 'single_value', True), 
              ('TUMOR_SIZE', None, 'TUMOR_SIZE', 'TUMOR_SIZE', 'single_value', True) ]
        self.static_data['validation_file'] = \
            'breastcancerpathology_testing.xlsx'
        if self.project_subdir == 'production':
            self.static_data['raw_data_files'] = {}
            self.static_data['raw_data_files']['RDW_BREAST_CANCER_PATIENTS_NLP_PATH_RESULTS_20230717_055320.XML'] = {}
            self.static_data['raw_data_files']['RDW_BREAST_CANCER_PATIENTS_NLP_PATH_RESULTS_20230717_055320.XML']['DATETIME_FORMAT'] = '%Y-%m-%d %H:%M:%S'
            self.static_data['raw_data_files']['RDW_BREAST_CANCER_PATIENTS_NLP_PATH_RESULTS_20230717_055320.XML']['DATETIME_KEY'] = 'SPECIMEN_COLLECTED_DATE'
            self.static_data['raw_data_files']['RDW_BREAST_CANCER_PATIENTS_NLP_PATH_RESULTS_20230717_055320.XML']['DOCUMENT_FRACTION'] = 1.0
            self.static_data['raw_data_files']['RDW_BREAST_CANCER_PATIENTS_NLP_PATH_RESULTS_20230717_055320.XML']['ENCODING'] = 'utf-8'
            self.static_data['raw_data_files']['RDW_BREAST_CANCER_PATIENTS_NLP_PATH_RESULTS_20230717_055320.XML']['NLP_MODE'] = 'SOURCE_SYSTEM_RESULT_ID'
            self.static_data['raw_data_files']['RDW_BREAST_CANCER_PATIENTS_NLP_PATH_RESULTS_20230717_055320.XML']['SOURCE_SYSTEM'] = 'Epic Beaker'
            self.static_data['raw_data_files_sequence'] = [ 'RDW_BREAST_CANCER_PATIENTS_NLP_PATH_RESULTS_20230717_055320.XML' ]
        elif self.project_subdir == 'test':
            self.static_data['raw_data_files'] = {}
            self.static_data['raw_data_files']['BreastCancerPathology.xls'] = {}
            self.static_data['raw_data_files']['BreastCancerPathology.xls']['DATETIME_FORMAT'] = '%m/%d/%Y'
            self.static_data['raw_data_files']['BreastCancerPathology.xls']['DATETIME_KEY'] = 'SPECIMEN_COLL_DT'
            self.static_data['raw_data_files']['BreastCancerPathology.xls']['DOCUMENT_FRACTION'] = 0.5
            self.static_data['raw_data_files']['BreastCancerPathology.xls']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['DORR_HAGLER_NLP_PATH_RESULTS_20211115_114000.XML'] = {}
            self.static_data['raw_data_files']['DORR_HAGLER_NLP_PATH_RESULTS_20211115_114000.XML']['DATETIME_FORMAT'] = '%Y-%m-%d %H:%M:%S'
            self.static_data['raw_data_files']['DORR_HAGLER_NLP_PATH_RESULTS_20211115_114000.XML']['DATETIME_KEY'] = 'SPECIMEN_COLLECTED_DATE'
            self.static_data['raw_data_files']['DORR_HAGLER_NLP_PATH_RESULTS_20211115_114000.XML']['DOCUMENT_FRACTION'] = 1.0
            self.static_data['raw_data_files']['DORR_HAGLER_NLP_PATH_RESULTS_20211115_114000.XML']['ENCODING'] = 'utf-8'
            self.static_data['raw_data_files']['DORR_HAGLER_NLP_PATH_RESULTS_20211115_114000.XML']['NLP_MODE'] = 'SOURCE_SYSTEM_RESULT_ID'
            self.static_data['raw_data_files']['DORR_HAGLER_NLP_PATH_RESULTS_20211115_114000.XML']['SOURCE_SYSTEM'] = 'Epic Beaker'
            self.static_data['raw_data_files_sequence'] = [ 'BreastCancerPathology.xls',
                                                            'DORR_HAGLER_NLP_PATH_RESULTS_20211115_114000.XML' ]
            
            #
            data_set_flgs = [ 'testing', 'training' ]
            data_set_flg = data_set_flgs[0]
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
                
            if data_set_flg == 'training':
                self._include_lists(docs_files, groups_files, [0])
            elif data_set_flg == 'testing':
                self._include_lists(docs_files, groups_files, [1])
            
            raw_data_dir = \
                self.static_data['directory_object'].pull_directory('raw_data_dir')
            raw_data_file = os.path.join(raw_data_dir, 'breastcancerpathology_testing.xlsx')
            book = read_xlsx_file(raw_data_file)
            sheet = book.sheet_by_index(0)
            patient_list = list(set(sheet.col_values(1)[1:]))
            document_list = list(set(sheet.col_values(2)[1:]))

            self._trim_lists(document_list, patient_list)
        
    #
    def _trim_lists(self, document_list, patient_list):
        self.static_data['document_list'] = \
            list(set(self.static_data['document_list']).intersection(document_list))
        self.static_data['patient_list'] = \
            list(set(self.static_data['patient_list']).intersection(patient_list))