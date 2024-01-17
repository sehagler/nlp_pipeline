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
class KDLReports_static_data_object(Static_data_object):
    
    #
    def __init__(self, operation_mode, user, root_dir_flg, project_subdir=None):
        project_name = 'KDLReports'
        Static_data_object.__init__(self, operation_mode, user, root_dir_flg,
                                     project_name=project_name,
                                     project_subdir=project_subdir)
        self.project_subdir = project_subdir
        
        self.static_data['document_identifiers'] = \
            [ 'SOURCE_SYSTEM_UNIQUE_ID' ]
        if 'performance_data_files' in self.static_data.keys():
            self.static_data['performance_data_files'].append('CCC19/test/CCC19.performance.json')
        self.static_data['queries_list'] = \
            [ ('ER Nuclear Staining', None, 'BREAST_CANCER_BIOMARKERS_ER', 'ER_STATUS', 'single_value', True),
              ('ER Percent', None, 'BREAST_CANCER_BIOMARKERS_ER', 'ER_PERCENTAGE', 'single_value', True),
              ('ER Stain Score', None, 'BREAST_CANCER_BIOMARKERS_ER', 'ER_SCORE', 'single_value', True),
              ('ER_STRENGTH', None, 'BREAST_CANCER_BIOMARKERS_ER', 'ER_STRENGTH', 'single_value', True),
              ('Gata3 Nuclear Staining', None, 'BREAST_CANCER_BIOMARKERS_GATA3', 'GATA3_STATUS', 'single_value', True),
              ('Gata3 Percent', None, 'BREAST_CANCER_BIOMARKERS_GATA3', 'GATA3_PERCENTAGE', 'single_value', True),
              ('Gata3 Stain Score', None, 'BREAST_CANCER_BIOMARKERS_GATA3', 'GATA3_SCORE', 'single_value', True),
              ('Her2 IHC Nuclear Staining', None, 'BREAST_CANCER_BIOMARKERS_HER2', 'HER2_STATUS', 'single_value', True),
              ('Her2 IHC Percent', None, 'BREAST_CANCER_BIOMARKERS_HER2', 'HER2_PERCENTAGE', 'single_value', True),
              ('Her2 IHC Stain Score', None, 'BREAST_CANCER_BIOMARKERS_HER2', 'HER2_SCORE', 'single_value', True),
              ('Ki67 Nuclear Staining', None, 'BREAST_CANCER_BIOMARKERS_KI67', 'KI67_STATUS', 'single_value', True),
              ('Ki67 Percent', None, 'BREAST_CANCER_BIOMARKERS_KI67', 'KI67_PERCENTAGE', 'single_value', True),
              ('Ki67 Stain Score', None, 'BREAST_CANCER_BIOMARKERS_KI67', 'KI67_SCORE', 'single_value', True),
              ('PR Nuclear Staining', None, 'BREAST_CANCER_BIOMARKERS_PR', 'PR_STATUS', 'single_value', True),
              ('PR Percent', None, 'BREAST_CANCER_BIOMARKERS_PR', 'PR_PERCENTAGE', 'single_value', True),
              ('PR Stain Score', None, 'BREAST_CANCER_BIOMARKERS_PR', 'PR_SCORE', 'single_value', True),
              ('PR_STRENGTH', None, 'BREAST_CANCER_BIOMARKERS_PR', 'PR_STRENGTH', 'single_value', True) ] 
        self.static_data['validation_file'] = \
            'smmart_nlp_comparison.xlsx'
        if self.project_subdir == 'test':
            self.static_data['deidentifier_flg'] = True
            self.static_data['raw_data_files'] = {}
            self.static_data['raw_data_files']['RDW_BREAST_CANCER_PATIENTS_NLP_PATH_RESULTS_20220906_123020.XML'] = {}
            self.static_data['raw_data_files']['RDW_BREAST_CANCER_PATIENTS_NLP_PATH_RESULTS_20220906_123020.XML']['DATETIME_FORMAT'] = '%Y-%m-%d %H:%M:%S'
            self.static_data['raw_data_files']['RDW_BREAST_CANCER_PATIENTS_NLP_PATH_RESULTS_20220906_123020.XML']['DATETIME_KEY'] = 'SPECIMEN_COLLECTED_DATE'
            self.static_data['raw_data_files']['RDW_BREAST_CANCER_PATIENTS_NLP_PATH_RESULTS_20220906_123020.XML']['DOCUMENT_FRACTION'] = 1.0
            self.static_data['raw_data_files']['RDW_BREAST_CANCER_PATIENTS_NLP_PATH_RESULTS_20220906_123020.XML']['ENCODING'] = 'utf-8'
            self.static_data['raw_data_files']['RDW_BREAST_CANCER_PATIENTS_NLP_PATH_RESULTS_20220906_123020.XML']['NLP_MODE'] = 'SOURCE_SYSTEM_RESULT_ID'
            self.static_data['raw_data_files']['RDW_BREAST_CANCER_PATIENTS_NLP_PATH_RESULTS_20220906_123020.XML']['SOURCE_SYSTEM'] = 'Epic Beaker'
            self.static_data['raw_data_files_sequence'] = [ 'RDW_BREAST_CANCER_PATIENTS_NLP_PATH_RESULTS_20220906_123020.XML' ]
            
            #
            #data_set_flgs = [ 'testing', 'training' ]
            #data_set_flg = data_set_flgs[0]
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
                
            '''
            if data_set_flg == 'training':
                self._include_lists(docs_files, groups_files, [0])
            elif data_set_flg == 'testing':
                self._include_lists(docs_files, groups_files, [1])
            '''
            self._include_lists(docs_files, groups_files, [0, 1])
            
            raw_data_dir = \
                self.static_data['directory_object'].pull_directory('raw_data_dir')
            raw_data_file = os.path.join(raw_data_dir, 'smmart_nlp_comparison.xlsx')
            book = read_xlsx_file(raw_data_file)
            sheet = book.sheet_by_index(0)
            patient_list = list(set(sheet.col_values(0)[1:]))
            document_list = list(set(sheet.col_values(2)[1:]))
            
            self._trim_lists(document_list, patient_list)
        
    #
    def _trim_lists(self, document_list, patient_list):
        remove_document_list = self.static_data['document_list']
        self.static_data['document_list'] = \
            list(set(document_list) - set(remove_document_list))
        del self.static_data['patient_list']
        #remove_patient_list = self.static_data['patient_list']
        #self.static_data['patient_list'] = \
        #    list(set(patient_list) - set(remove_patient_list))