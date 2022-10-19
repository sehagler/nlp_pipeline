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
class OhsuNlpTemplate_static_data_manager(Static_data_manager):
    
    #
    def __init__(self, operation_mode, user, root_dir_flg, project_subdir=None):
        project_name = 'OhsuNlpTemplate'
        Static_data_manager.__init__(self, operation_mode, user, root_dir_flg,
                                     project_name=project_name,
                                     project_subdir=project_subdir)
        self.project_subdir = project_subdir
        self.static_data['document_identifiers'] = \
            [ 'CASE_NUMBER', 'SOURCE_SYSTEM_NOTE_CSN_ID' ]
        self.static_data['queries_list'] = \
            [ ('CANCER_STAGE', None, 'CANCER_STAGE', 'CANCER_STAGE', 'single_value', True) ]
        self.static_data['validation_file'] = 'ccc19_testing.xlsx'
        if self.project_subdir == 'production':
            pass
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
                
            self._include_lists(docs_files, groups_files, [0])
            #self._include_lists(docs_files, groups_files, [1, 2, 3])
            
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
            for idx in [ 0 ]:
            #for idx in [ 1, 2, 3, 4, 5, 6, 7 ]:
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