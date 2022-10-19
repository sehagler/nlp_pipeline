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
from nlp_pipeline_lib.static_data_lib.static_data_manager_class \
    import Static_data_manager
from tool_lib.py.processing_tools_lib.file_processing_tools \
    import read_xlsx_file

#
class CCC19_static_data_manager(Static_data_manager):
    
    #
    def __init__(self, operation_mode, user, root_dir_flg, project_subdir=None):
        project_name = 'CCC19'
        Static_data_manager.__init__(self, operation_mode, user, root_dir_flg,
                                     project_name=project_name,
                                     project_subdir=project_subdir)
        self.project_subdir = project_subdir
        
        self.static_data['document_identifiers'] = \
            [ 'CASE_NUMBER', 'SOURCE_SYSTEM_NOTE_CSN_ID' ]
        if 'performance_data_files' in self.static_data.keys():
            self.static_data['performance_data_files'].append('BreastCancerPathology/test/BreastCancerPathology.performance.json')
        self.static_data['queries_list'] = \
            [ ('CANCER_STAGE', None, 'CANCER_STAGE', 'CANCER_STAGE', 'single_value', True),
              ('NORMALIZED_ECOG_SCORE', None, 'ECOG_STATUS', 'NORMALIZED_ECOG_SCORE', 'single_value', True),
              ('NORMALIZED_SMOKING_HISTORY', None, 'SMOKING_HISTORY', 'NORMALIZED_SMOKING_HISTORY', 'single_value', True),
              ('NORMALIZED_SMOKING_PRODUCTS', None, 'SMOKING_PRODUCTS', 'NORMALIZED_SMOKING_PRODUCTS', 'multiple_values', False),
              ('NORMALIZED_SMOKING_STATUS', None, 'SMOKING_STATUS', 'NORMALIZED_SMOKING_STATUS', 'single_value', True) ] 
        self.static_data['test_postprocessing_data_in_files'] = \
            [ 'cancer_stage.csv', 'ecog_status.csv', 'smoking_history.csv',
              'smoking_products.csv', 'smoking_status.csv' ]
        self.static_data['validation_file'] = 'ccc19_testing.xlsx'
        if self.project_subdir == 'production':
            self.static_data['raw_data_files'] = {}
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220906_113714.XML'] = {}
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220906_113714.XML']['DATETIME_FORMAT'] = '%d-%b-%y %H:%M:%S'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220906_113714.XML']['DATETIME_KEY'] = 'NOTE_DATE'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220906_113714.XML']['ENCODING'] = 'utf-16'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220906_113714.XML']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220906_113714.XML']['SOURCE_SYSTEM'] = 'Epic Beaker'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220906_115047.XML'] = {}
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220906_115047.XML']['DATETIME_FORMAT'] = '%d-%b-%y %H:%M:%S'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220906_115047.XML']['DATETIME_KEY'] = 'NOTE_DATE'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220906_115047.XML']['ENCODING'] = 'utf-16'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220906_115047.XML']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220906_115047.XML']['SOURCE_SYSTEM'] = 'Epic Beaker'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220906_120437.XML'] = {}
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220906_120437.XML']['DATETIME_FORMAT'] = '%d-%b-%y %H:%M:%S'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220906_120437.XML']['DATETIME_KEY'] = 'NOTE_DATE'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220906_120437.XML']['ENCODING'] = 'utf-16'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220906_120437.XML']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220906_120437.XML']['SOURCE_SYSTEM'] = 'Epic Beaker'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220906_121817.XML'] = {}
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220906_121817.XML']['DATETIME_FORMAT'] = '%d-%b-%y %H:%M:%S'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220906_121817.XML']['DATETIME_KEY'] = 'NOTE_DATE'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220906_121817.XML']['ENCODING'] = 'utf-16'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220906_121817.XML']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220906_121817.XML']['SOURCE_SYSTEM'] = 'Epic Beaker'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220906_123247.XML'] = {}
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220906_123247.XML']['DATETIME_FORMAT'] = '%d-%b-%y %H:%M:%S'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220906_123247.XML']['DATETIME_KEY'] = 'NOTE_DATE'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220906_123247.XML']['ENCODING'] = 'utf-16'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220906_123247.XML']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220906_123247.XML']['SOURCE_SYSTEM'] = 'Epic Beaker'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_PATH_RESULTS_20220906_113701.XML'] = {}
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_PATH_RESULTS_20220906_113701.XML']['DATETIME_FORMAT'] = '%d-%b-%y %H:%M:%S'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_PATH_RESULTS_20220906_113701.XML']['DATETIME_KEY'] = 'NOTE_DATE'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_PATH_RESULTS_20220906_113701.XML']['ENCODING'] = 'utf-8'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_PATH_RESULTS_20220906_113701.XML']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_PATH_RESULTS_20220906_113701.XML']['SOURCE_SYSTEM'] = 'Epic Beaker'
            self.static_data['raw_data_files_sequence'] = [ 'NAGLE_CCC19_NLP_HNO_NOTE_20220906_113714.XML',
                                                            'NAGLE_CCC19_NLP_HNO_NOTE_20220906_115047.XML',
                                                            'NAGLE_CCC19_NLP_HNO_NOTE_20220906_120437.XML',
                                                            'NAGLE_CCC19_NLP_HNO_NOTE_20220906_121817.XML',
                                                            'NAGLE_CCC19_NLP_HNO_NOTE_20220906_123247.XML',
                                                            'NAGLE_CCC19_NLP_PATH_RESULTS_20220906_113701.XML' ]
        elif self.project_subdir == 'test':
            self.static_data['raw_data_files'] = {}
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_covid_positive.xml'] = {}
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_covid_positive.xml']['DATETIME_FORMAT'] = '%d-%b-%y'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_covid_positive.xml']['DATETIME_KEY'] = 'NOTE_DATE'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_covid_positive.xml']['DOCUMENT_FRACTION'] = 0.1
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_covid_positive.xml']['ENCODING'] = 'utf-8'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_covid_positive.xml']['NLP_MODE'] = 'NONE'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_covid_positive.xml']['SOURCE_SYSTEM'] = 'Epic Beaker'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_first_general_set.xml'] = {}
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_first_general_set.xml']['DATETIME_FORMAT'] = '%d-%b-%y'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_first_general_set.xml']['DATETIME_KEY'] = 'NOTE_DATE'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_first_general_set.xml']['DOCUMENT_FRACTION'] = 0.1
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_first_general_set.xml']['ENCODING'] = 'utf-8'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_first_general_set.xml']['NLP_MODE'] = 'NONE'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_first_general_set.xml']['SOURCE_SYSTEM'] = 'Epic Beaker'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_second_general_set.xml'] = {}
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_second_general_set.xml']['DATETIME_FORMAT'] = '%d-%b-%y'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_second_general_set.xml']['DATETIME_KEY'] = 'NOTE_DATE'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_second_general_set.xml']['ENCODING'] = 'utf-8'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_second_general_set.xml']['DOCUMENT_FRACTION'] = 0.1
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_second_general_set.xml']['NLP_MODE'] = 'NONE'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_second_general_set.xml']['SOURCE_SYSTEM'] = 'Epic Beaker'
            self.static_data['raw_data_files_sequence'] = [ 'Nagle_CCC19_NLP_hno_note_v_covid_positive.xml',
                                                             'Nagle_CCC19_NLP_hno_note_v_second_general_set.xml',
                                                             'Nagle_CCC19_NLP_hno_note_v_first_general_set.xml' ]

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
            source_dir = base_dir + '/NLP/NLP_Source_Data/CCC19'
            training_data_dir = source_dir + '/test/pkl'
            docs_files = []
            docs_files.append(os.path.join(training_data_dir,
                              'training_docs_covid_positive.pkl'))
            docs_files.append(os.path.join(training_data_dir,
                              'training_docs_first_general_set.pkl'))
            docs_files.append(os.path.join(training_data_dir,
                              'training_docs_second_general_set.pkl'))
            groups_files = []
            groups_files.append(os.path.join(training_data_dir,
                                'training_groups_covid_positive.pkl'))
            #groups_files.append(os.path.join(training_data_dir,
            #                    'training_groups_first_general_set.pkl'))
            groups_files.append(os.path.join(training_data_dir,
                                'training_groups_second_general_set.pkl'))
            if data_set_flg == 'training':    
                self._include_lists(docs_files, groups_files, [0])
            elif data_set_flg == 'testing':
                self._include_lists(docs_files, groups_files, [1, 2, 3])
            evaluation_docs_file = \
                os.path.join(training_data_dir, 'training_docs_evaluation.pkl')
            idx_list = [0, 1, 2]
            with open(evaluation_docs_file, 'rb') as f:
                document_list = pickle.load(f)
            for idx in idx_list:
                self.static_data['document_list'].extend(document_list[idx])
            self.static_data['document_list'] = \
                list(set(self.static_data['document_list']))
            trainng_groups_first_general_set_file = \
                os.path.join(training_data_dir, 'training_groups_first_general_set.pkl')
            with open(trainng_groups_first_general_set_file, 'rb') as f:
                patient_list = pickle.load(f)
            if data_set_flg == 'training':
                idx_list = [0]
            elif data_set_flg == 'testing':
                idx_list =[ 1, 2, 3, 4, 5, 6, 7 ]
            for idx in idx_list:
                self.static_data['patient_list'].extend(patient_list[idx])
            self.static_data['patient_list'] = \
                list(set(self.static_data['patient_list']))
            
            raw_data_dir = \
                self.static_data['directory_manager'].pull_directory('raw_data_dir')
            raw_data_file = os.path.join(raw_data_dir, 'ccc19_testing.xlsx')
            book = read_xlsx_file(raw_data_file)
            sheet = book.sheet_by_index(0)
            patient_list = list(set(sheet.col_values(1)[1:]))
            document_list = list(set(sheet.col_values(2)[1:]))
            
            self._trim_lists(document_list, patient_list)
                
        else:
            print('Bad project_subdir value')
            
    #
    def _trim_lists(self, document_list, patient_list):
        self.static_data['document_list'] = \
            list(set(self.static_data['document_list']).intersection(document_list))
        self.static_data['patient_list'] = \
            list(set(self.static_data['patient_list']).intersection(patient_list))