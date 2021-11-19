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
    
    #
    def get_static_data(self):
        self.static_data['document_identifiers'] = \
            [ 'CASE_NUMBER', 'SOURCE_SYSTEM_NOTE_CSN_ID' ]
        if self.project_subdir == 'production':
            self.static_data['raw_data_files'] = {}
            self.static_data['raw_data_files']['CCC19_NLP_HNO_NOTE_20210723_120041.XML'] = {}
            self.static_data['raw_data_files']['CCC19_NLP_HNO_NOTE_20210723_120041.XML']['DATETIME_FORMAT'] = '%d-%b-%y'
            self.static_data['raw_data_files']['CCC19_NLP_HNO_NOTE_20210723_120041.XML']['FORMATTING'] = 'unformatted'
            self.static_data['raw_data_files']['CCC19_NLP_HNO_NOTE_20210723_120041.XML']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['CCC19_NLP_HNO_NOTE_20210723_120041.XML']['SOURCE_SYSTEM'] = 'BeakerAP'
            self.static_data['raw_data_files']['CCC19_NLP_HNO_NOTE_20210723_120510.XML'] = {}
            self.static_data['raw_data_files']['CCC19_NLP_HNO_NOTE_20210723_120510.XML']['DATETIME_FORMAT'] = '%d-%b-%y'
            self.static_data['raw_data_files']['CCC19_NLP_HNO_NOTE_20210723_120510.XML']['FORMATTING'] = 'unformatted'
            self.static_data['raw_data_files']['CCC19_NLP_HNO_NOTE_20210723_120510.XML']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['CCC19_NLP_HNO_NOTE_20210723_120510.XML']['SOURCE_SYSTEM'] = 'BeakerAP'
            self.static_data['raw_data_files']['CCC19_NLP_HNO_NOTE_20210723_120901.XML'] = {}
            self.static_data['raw_data_files']['CCC19_NLP_HNO_NOTE_20210723_120901.XML']['DATETIME_FORMAT'] = '%d-%b-%y'
            self.static_data['raw_data_files']['CCC19_NLP_HNO_NOTE_20210723_120901.XML']['FORMATTING'] = 'unformatted'
            self.static_data['raw_data_files']['CCC19_NLP_HNO_NOTE_20210723_120901.XML']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['CCC19_NLP_HNO_NOTE_20210723_120901.XML']['SOURCE_SYSTEM'] = 'BeakerAP'
            self.static_data['raw_data_files']['CCC19_NLP_HNO_NOTE_20210723_121254.XML'] = {}
            self.static_data['raw_data_files']['CCC19_NLP_HNO_NOTE_20210723_121254.XML']['DATETIME_FORMAT'] = '%d-%b-%y'
            self.static_data['raw_data_files']['CCC19_NLP_HNO_NOTE_20210723_121254.XML']['FORMATTING'] = 'unformatted'
            self.static_data['raw_data_files']['CCC19_NLP_HNO_NOTE_20210723_121254.XML']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['CCC19_NLP_HNO_NOTE_20210723_121254.XML']['SOURCE_SYSTEM'] = 'BeakerAP'
            self.static_data['raw_data_files']['CCC19_NLP_HNO_NOTE_20210723_121719.XML'] = {}
            self.static_data['raw_data_files']['CCC19_NLP_HNO_NOTE_20210723_121719.XML']['DATETIME_FORMAT'] = '%d-%b-%y'
            self.static_data['raw_data_files']['CCC19_NLP_HNO_NOTE_20210723_121719.XML']['FORMATTING'] = 'unformatted'
            self.static_data['raw_data_files']['CCC19_NLP_HNO_NOTE_20210723_121719.XML']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['CCC19_NLP_HNO_NOTE_20210723_121719.XML']['SOURCE_SYSTEM'] = 'BeakerAP'
            self.static_data['raw_data_files']['CCC19_NLP_PATH_RESULTS_20210723_115905.XML'] = {}
            self.static_data['raw_data_files']['CCC19_NLP_PATH_RESULTS_20210723_115905.XML']['DATETIME_FORMAT'] = '%d-%b-%y'
            self.static_data['raw_data_files']['CCC19_NLP_PATH_RESULTS_20210723_115905.XML']['FORMATTING'] = 'unformatted'
            self.static_data['raw_data_files']['CCC19_NLP_PATH_RESULTS_20210723_115905.XML']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['CCC19_NLP_PATH_RESULTS_20210723_115905.XML']['SOURCE_SYSTEM'] = 'BeakerAP'
            self.static_data['raw_data_files_sequence'] = [ 'CCC19_NLP_HNO_NOTE_20210723_120041.XML',
                                                            'CCC19_NLP_HNO_NOTE_20210723_120510.XML',
                                                            'CCC19_NLP_HNO_NOTE_20210723_120901.XML',
                                                            'CCC19_NLP_HNO_NOTE_20210723_121254.XML',
                                                            'CCC19_NLP_HNO_NOTE_20210723_121719.XML',
                                                            'CCC19_NLP_PATH_RESULTS_20210723_115905.XML' ]
        elif self.project_subdir == 'test':
            self.static_data['raw_data_files'] = {}
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_covid_positive.xml'] = {}
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_covid_positive.xml']['DATETIME_FORMAT'] = '%d-%b-%y'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_covid_positive.xml']['DOCUMENT_FRACTION'] = 0.1
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_covid_positive.xml']['FORMATTING'] = 'unformatted'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_covid_positive.xml']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_covid_positive.xml']['SOURCE_SYSTEM'] = 'BeakerAP'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_first_general_set.xml'] = {}
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_first_general_set.xml']['DATETIME_FORMAT'] = '%d-%b-%y'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_first_general_set.xml']['DOCUMENT_FRACTION'] = 0.1
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_first_general_set.xml']['FORMATTING'] = 'unformatted'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_first_general_set.xml']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_first_general_set.xml']['SOURCE_SYSTEM'] = 'BeakerAP'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_second_general_set.xml'] = {}
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_second_general_set.xml']['DATETIME_FORMAT'] = '%d-%b-%y'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_second_general_set.xml']['FORMATTING'] = 'unformatted'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_second_general_set.xml']['DOCUMENT_FRACTION'] = 0.1
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_second_general_set.xml']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_second_general_set.xml']['SOURCE_SYSTEM'] = 'BeakerAP'
            self.static_data['raw_data_files_sequence'] = [ 'Nagle_CCC19_NLP_hno_note_v_covid_positive.xml',
                                                             'Nagle_CCC19_NLP_hno_note_v_second_general_set.xml',
                                                             'Nagle_CCC19_NLP_hno_note_v_first_general_set.xml' ]

            #
            if False:
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
                covid_positive_docs_file = \
                    os.path.join(training_data_dir, 'training_docs_covid_positive.pkl')
                covid_positive_groups_file = \
                    os.path.join(training_data_dir, 'training_groups_covid_positive.pkl')
                first_general_docs_file = \
                    os.path.join(training_data_dir, 'training_docs_first_general_set.pkl')
                second_general_docs_file = \
                    os.path.join(training_data_dir, 'training_docs_second_general_set.pkl')
                second_general_groups_file = \
                    os.path.join(training_data_dir, 'training_groups_second_general_set.pkl')
                evaluation_docs_file = \
                    os.path.join(training_data_dir, 'training_docs_evaluation.pkl')
                try:
                    self.static_data['document_list'] = []
                    idx_list = [0, 1, 2]
                    with open(evaluation_docs_file, 'rb') as f:
                        document_list = pickle.load(f)
                    for idx in idx_list:
                        self.static_data['document_list'].extend(document_list[idx])
                    with open(covid_positive_docs_file, 'rb') as f:
                        document_list = pickle.load(f)
                    self.static_data['document_list'].extend(document_list[0])
                    with open(first_general_docs_file, 'rb') as f:
                        document_list = pickle.load(f)
                    self.static_data['document_list'].extend(document_list[0])
                    with open(second_general_docs_file, 'rb') as f:
                        document_list = pickle.load(f)
                    self.static_data['document_list'].extend(document_list[0])
                    self.static_data['document_list'] = \
                        list(set(self.static_data['document_list']))
                except:
                    pass
                try:
                    self.static_data['patient_list'] = []
                    #idx_list = [0, 1, 2]
                    idx_list = [3]
                    with open(covid_positive_groups_file, 'rb') as f:
                        patient_lists = pickle.load(f)
                    patient_list = []
                    for idx in idx_list:
                        patient_list.extend(patient_lists[idx])
                    self.static_data['patient_list'].extend(patient_list)
                    with open(second_general_groups_file, 'rb') as f:
                        patient_lists = pickle.load(f)
                    patient_list = []
                    for idx in idx_list:
                        patient_list.extend(patient_lists[idx])
                    self.static_data['patient_list'].extend(patient_list)
                    self.static_data['patient_list'] = \
                        list(set(self.static_data['patient_list']))
                except:
                    pass
            
            #
            if True:
                raw_data_dir = \
                    self.static_data['directory_manager'].pull_directory('raw_data_dir')
                raw_data_file = os.path.join(raw_data_dir, 'ccc19_testing.xlsx')
                book = read_xlsx_file(raw_data_file)
                sheet = book.sheet_by_index(0)
                patient_list = sheet.col_values(1)
                document_list = sheet.col_values(2)
                self.static_data['patient_list'] = list(set(patient_list[1:]))
                self.static_data['document_list'] = list(set(document_list[1:]))
                
        else:
            print('Bad project_subdir value')

    	#
        return self.static_data