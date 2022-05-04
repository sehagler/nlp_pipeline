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
from nlp_pipeline_lib.py.static_data_lib.static_data_manager_class \
    import Static_data_manager
from tool_lib.py.processing_tools_lib.file_processing_tools \
    import read_xlsx_file

#
class CCC19_static_data_manager(Static_data_manager):
    
    #
    def __init__(self, operation_mode, project_subdir, user, root_dir_flg):
        project_name = 'CCC19'
        Static_data_manager.__init__(self, operation_mode, project_name, 
                                     project_subdir, user, root_dir_flg)
        self.project_subdir = project_subdir
        
        self.static_data['document_identifiers'] = \
            [ 'CASE_NUMBER', 'SOURCE_SYSTEM_NOTE_CSN_ID' ]
        self.static_data['performance_data_files'].append('BreastCancerPathology/test/BreastCancerPathology.performance.json')
        self.static_data['test_postprocessing_data_in_files'] = \
            [ 'cancer_stage.csv', 'ecog_status.csv', 'smoking_history.csv',
              'smoking_products.csv', 'smoking_status.csv' ]
        self.static_data['validation_file'] = 'ccc19_testing.xlsx'
        if self.project_subdir == 'production':
            self.static_data['raw_data_files'] = {}
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220502_145729.XML'] = {}
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220502_145729.XML']['DATETIME_FORMAT'] = '%d-%b-%y'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220502_145729.XML']['ENCODING'] = 'utf-16'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220502_145729.XML']['FORMATTING'] = 'unformatted'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220502_145729.XML']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220502_145729.XML']['SOURCE_SYSTEM'] = 'BeakerAP'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220502_150815.XML'] = {}
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220502_150815.XML']['DATETIME_FORMAT'] = '%d-%b-%y'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220502_150815.XML']['ENCODING'] = 'utf-16'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220502_150815.XML']['FORMATTING'] = 'unformatted'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220502_150815.XML']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220502_150815.XML']['SOURCE_SYSTEM'] = 'BeakerAP'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220502_142636.XML'] = {}
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220502_142636.XML']['DATETIME_FORMAT'] = '%d-%b-%y'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220502_142636.XML']['ENCODING'] = 'utf-16'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220502_142636.XML']['FORMATTING'] = 'unformatted'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220502_142636.XML']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220502_142636.XML']['SOURCE_SYSTEM'] = 'BeakerAP'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220502_143804.XML'] = {}
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220502_143804.XML']['DATETIME_FORMAT'] = '%d-%b-%y'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220502_143804.XML']['ENCODING'] = 'utf-16'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220502_143804.XML']['FORMATTING'] = 'unformatted'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220502_143804.XML']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220502_143804.XML']['SOURCE_SYSTEM'] = 'BeakerAP'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220502_144728.XML'] = {}
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220502_144728.XML']['DATETIME_FORMAT'] = '%d-%b-%y'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220502_144728.XML']['ENCODING'] = 'utf-16'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220502_144728.XML']['FORMATTING'] = 'unformatted'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220502_144728.XML']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20220502_144728.XML']['SOURCE_SYSTEM'] = 'BeakerAP'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_PATH_RESULTS_20220502_142359.XML'] = {}
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_PATH_RESULTS_20220502_142359.XML']['DATETIME_FORMAT'] = '%d-%b-%y'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_PATH_RESULTS_20220502_142359.XML']['ENCODING'] = 'utf-8'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_PATH_RESULTS_20220502_142359.XML']['FORMATTING'] = 'unformatted'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_PATH_RESULTS_20220502_142359.XML']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_PATH_RESULTS_20220502_142359.XML']['SOURCE_SYSTEM'] = 'BeakerAP'
            self.static_data['raw_data_files_sequence'] = [ 'NAGLE_CCC19_NLP_HNO_NOTE_20220502_145729.XML',
                                                            'NAGLE_CCC19_NLP_HNO_NOTE_20220502_150815.XML',
                                                            'NAGLE_CCC19_NLP_HNO_NOTE_20220502_142636.XML',
                                                            'NAGLE_CCC19_NLP_HNO_NOTE_20220502_143804.XML',
                                                            'NAGLE_CCC19_NLP_HNO_NOTE_20220502_144728.XML',
                                                            'NAGLE_CCC19_NLP_PATH_RESULTS_20220502_142359.XML' ]
        elif self.project_subdir == 'test':
            self.static_data['raw_data_files'] = {}
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_covid_positive.xml'] = {}
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_covid_positive.xml']['DATETIME_FORMAT'] = '%d-%b-%y'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_covid_positive.xml']['DOCUMENT_FRACTION'] = 0.1
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_covid_positive.xml']['ENCODING'] = 'utf-8'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_covid_positive.xml']['FORMATTING'] = 'unformatted'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_covid_positive.xml']['NLP_MODE'] = 'NONE'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_covid_positive.xml']['SOURCE_SYSTEM'] = 'BeakerAP'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_first_general_set.xml'] = {}
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_first_general_set.xml']['DATETIME_FORMAT'] = '%d-%b-%y'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_first_general_set.xml']['DOCUMENT_FRACTION'] = 0.1
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_first_general_set.xml']['ENCODING'] = 'utf-8'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_first_general_set.xml']['FORMATTING'] = 'unformatted'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_first_general_set.xml']['NLP_MODE'] = 'NONE'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_first_general_set.xml']['SOURCE_SYSTEM'] = 'BeakerAP'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_second_general_set.xml'] = {}
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_second_general_set.xml']['DATETIME_FORMAT'] = '%d-%b-%y'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_second_general_set.xml']['ENCODING'] = 'utf-8'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_second_general_set.xml']['FORMATTING'] = 'unformatted'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_second_general_set.xml']['DOCUMENT_FRACTION'] = 0.1
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_second_general_set.xml']['NLP_MODE'] = 'NONE'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_second_general_set.xml']['SOURCE_SYSTEM'] = 'BeakerAP'
            self.static_data['raw_data_files_sequence'] = [ 'Nagle_CCC19_NLP_hno_note_v_covid_positive.xml',
                                                             'Nagle_CCC19_NLP_hno_note_v_second_general_set.xml',
                                                             'Nagle_CCC19_NLP_hno_note_v_first_general_set.xml' ]

            #
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
            for idx in [ 1, 2, 3, 4, 5, 6, 7 ]:
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