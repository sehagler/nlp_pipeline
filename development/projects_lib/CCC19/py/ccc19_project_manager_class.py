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
class CCC19_project_manager(Static_data_manager):
    
    #
    def __init__(self, operation_mode, project_subdir, user, root_dir_flg):
        project_name = 'CCC19'
        Static_data_manager.__init__(self, operation_mode, project_name, 
                                     project_subdir, user, root_dir_flg)
        self.project_subdir = project_subdir
    
    #
    def get_project_data(self):
        self.static_data['datetime_identifiers'] = {}
        self.static_data['datetime_identifiers'][ 'NOTE_DATE' ] = '%d-%b-%y'
        self.static_data['document_identifiers'] = \
            [ 'CASE_NUMBER', 'SOURCE_SYSTEM_NOTE_CSN_ID' ]
        self.static_data['flags'] = {}
        self.static_data['flags']['multiprocessing'] = True
        self.static_data['flags']['remove_date'] = True
        self.static_data['flags']['trim_data_by_csn'] = True
        self.static_data['formatting'] = 'unformatted'
        self.static_data['json_files_key_value'] = []
        self.static_data['patient_identifiers'] = [ 'OHSU_MRN' ]
        self.static_data['raw_data_files'] = {}
        self.static_data['read_data_mode'] = 'get_data_by_document_number'
        self.static_data['text_identifiers'] = [ 'COMMENT_TEXT', 'NOTE_TEXT',
                                                 'PATHOLOGY_REPORT', 'RESULT_TEXT' ]
        if self.project_subdir == 'production':
            self.static_data['raw_data_encoding'] = 'utf-16'
            self.static_data['raw_data_files'] = {}
            '''
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20210409_153220.XML'] = {}
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20210409_153220.XML']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20210409_153220.XML']['NLP_PROCESS'] = 'NOTE'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20210409_153220.XML']['SOURCE_SYSTEM'] = 'BeakerAP'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20210409_153225.XML'] = {}
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20210409_153225.XML']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20210409_153225.XML']['NLP_PROCESS'] = 'NOTE'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20210409_153225.XML']['SOURCE_SYSTEM'] = 'BeakerAP'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20210409_153231.XML'] = {}
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20210409_153231.XML']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20210409_153231.XML']['NLP_PROCESS'] = 'NOTE'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20210409_153231.XML']['SOURCE_SYSTEM'] = 'BeakerAP'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20210409_153237.XML'] = {}
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20210409_153237.XML']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20210409_153237.XML']['NLP_PROCESS'] = 'NOTE'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20210409_153237.XML']['SOURCE_SYSTEM'] = 'BeakerAP'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20210409_153243.XML'] = {}
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20210409_153243.XML']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20210409_153243.XML']['NLP_PROCESS'] = 'NOTE'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20210409_153243.XML']['SOURCE_SYSTEM'] = 'BeakerAP'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_PATH_RESULTS_20210504_152315.XML'] = {}
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_PATH_RESULTS_20210504_152315.XML']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_PATH_RESULTS_20210504_152315.XML']['NLP_PROCESS'] = 'NOTE'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_PATH_RESULTS_20210504_152315.XML']['SOURCE_SYSTEM'] = 'BeakerAP'
            self.static_data['raw_data_files_sequence'] = [ 'NAGLE_CCC19_NLP_HNO_NOTE_20210409_153220.XML',
                                                            'NAGLE_CCC19_NLP_HNO_NOTE_20210409_153225.XML',
                                                            'NAGLE_CCC19_NLP_HNO_NOTE_20210409_153231.XML',
                                                            'NAGLE_CCC19_NLP_HNO_NOTE_20210409_153237.XML',
                                                            'NAGLE_CCC19_NLP_HNO_NOTE_20210409_153243.XML',
                                                            'NAGLE_CCC19_NLP_PATH_RESULTS_20210504_152315.XML' ]
            '''
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20210122_143223.XML'] = {}
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20210122_143223.XML']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20210122_143223.XML']['NLP_PROCESS'] = 'NOTE'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20210122_143223.XML']['SOURCE_SYSTEM'] = 'BeakerAP'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20210122_143857.XML'] = {}
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20210122_143857.XML']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20210122_143857.XML']['NLP_PROCESS'] = 'NOTE'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20210122_143857.XML']['SOURCE_SYSTEM'] = 'BeakerAP'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20210122_145226.XML'] = {}
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20210122_145226.XML']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20210122_145226.XML']['NLP_PROCESS'] = 'NOTE'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20210122_145226.XML']['SOURCE_SYSTEM'] = 'BeakerAP'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20210122_150629.XML'] = {}
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20210122_150629.XML']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20210122_150629.XML']['NLP_PROCESS'] = 'NOTE'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20210122_150629.XML']['SOURCE_SYSTEM'] = 'BeakerAP'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20210122_151845.XML'] = {}
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20210122_151845.XML']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20210122_151845.XML']['NLP_PROCESS'] = 'NOTE'
            self.static_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE_20210122_151845.XML']['SOURCE_SYSTEM'] = 'BeakerAP'
            self.static_data['raw_data_files_sequence'] = [ 'NAGLE_CCC19_NLP_HNO_NOTE_20210122_143223.XML',
                                                             'NAGLE_CCC19_NLP_HNO_NOTE_20210122_143857.XML',
                                                             'NAGLE_CCC19_NLP_HNO_NOTE_20210122_145226.XML',
                                                             'NAGLE_CCC19_NLP_HNO_NOTE_20210122_150629.XML',
                                                             'NAGLE_CCC19_NLP_HNO_NOTE_20210122_151845.XML' ]
        elif self.project_subdir == 'test':
            self.static_data['raw_data_encoding'] = 'utf-8'
            self.static_data['raw_data_files'] = {}
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_covid_positive.xml'] = {}
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_covid_positive.xml']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_covid_positive.xml']['NLP_PROCESS'] = 'NOTE'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_covid_positive.xml']['SOURCE_SYSTEM'] = 'BeakerAP'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_first_general_set.xml'] = {}
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_first_general_set.xml']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_first_general_set.xml']['NLP_PROCESS'] = 'NOTE'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_first_general_set.xml']['SOURCE_SYSTEM'] = 'BeakerAP'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_second_general_set.xml'] = {}
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_second_general_set.xml']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_second_general_set.xml']['NLP_PROCESS'] = 'NOTE'
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
                training_data_dir = source_dir + '/pkl'
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