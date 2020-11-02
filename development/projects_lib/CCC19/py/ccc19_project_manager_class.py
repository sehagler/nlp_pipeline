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
from nlp_lib.py.manager_lib.project_manager_class import Project_manager
from nlp_lib.py.tool_lib.processing_tools_lib.file_processing_tools import read_xlsx_file

#
class CCC19_project_manager(Project_manager):
    
    #
    def __init__(self, operation_mode, user, root_dir_flg):
        project_name = 'CCC19'
        Project_manager.__init__(self, project_name, operation_mode, user, root_dir_flg)
    
    #
    def get_project_data(self):
        self.project_data['datetime_identifiers'] = {}
        self.project_data['datetime_identifiers'][ 'NOTE_DATE' ] = '%d-%b-%y'
        self.project_data['document_identifiers'] = [ 'SOURCE_SYSTEM_NOTE_CSN_ID' ]
        self.project_data['json_files_key_value'] = []
        self.project_data['patient_identifiers'] = [ 'OHSU_MRN' ]
        self.project_data['raw_data_files'] = {}
        '''
        self.project_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE.XML'] = {}
        self.project_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE.XML']['NLP_MODE'] = 'RESULT_ID'
        self.project_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE.XML']['NLP_PROCESS'] = 'NOTE'
        self.project_data['raw_data_files']['NAGLE_CCC19_NLP_HNO_NOTE.XML']['SOURCE_SYSTEM'] = 'BeakerAP'
        self.project_data['raw_data_files_sequence'] = [ 'NAGLE_CCC19_NLP_HNO_NOTE.XML' ]
        '''
        self.project_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_covid_positive.xml'] = {}
        self.project_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_covid_positive.xml']['NLP_MODE'] = 'RESULT_ID'
        self.project_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_covid_positive.xml']['NLP_PROCESS'] = 'NOTE'
        self.project_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_covid_positive.xml']['SOURCE_SYSTEM'] = 'BeakerAP'
        self.project_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_first_general_set.xml'] = {}
        self.project_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_first_general_set.xml']['NLP_MODE'] = 'RESULT_ID'
        self.project_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_first_general_set.xml']['NLP_PROCESS'] = 'NOTE'
        self.project_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_first_general_set.xml']['SOURCE_SYSTEM'] = 'BeakerAP'
        self.project_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_second_general_set.xml'] = {}
        self.project_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_second_general_set.xml']['NLP_MODE'] = 'RESULT_ID'
        self.project_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_second_general_set.xml']['NLP_PROCESS'] = 'NOTE'
        self.project_data['raw_data_files']['Nagle_CCC19_NLP_hno_note_v_second_general_set.xml']['SOURCE_SYSTEM'] = 'BeakerAP'
        self.project_data['raw_data_files_sequence'] = [ 'Nagle_CCC19_NLP_hno_note_v_covid_positive.xml',
                                                         'Nagle_CCC19_NLP_hno_note_v_second_general_set.xml',
                                                         'Nagle_CCC19_NLP_hno_note_v_first_general_set.xml' ]
        
        self.project_data['text_identifiers'] = [ 'COMMENT_TEXT', 'NOTE_TEXT', 'RESULT_TEXT' ]
        self.project_data['xml_metadata_keys'] = ['NLP_PROCESS', 'NOTE_TYPE']
        self._create_processors()

        #
        if False:
            if self.project_data['root_dir_flg'] == 'X':
                base_dir = 'Z:'
            elif self.project_data['root_dir_flg'] == 'Z':
                base_dir = 'Z:'
            elif self.project_data['root_dir_flg'] == 'dev_server':
                base_dir = '/home/groups/hopper2/RDW_NLP_WORKSPACE'
            elif self.project_data['root_dir_flg'] == 'prod_server':
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
                self.project_data['document_list'] = []
                idx_list = [0, 1, 2]
                with open(evaluation_docs_file, 'rb') as f:
                    document_list = pickle.load(f)
                for idx in idx_list:
                    self.project_data['document_list'].extend(document_list[idx])
                with open(covid_positive_docs_file, 'rb') as f:
                    document_list = pickle.load(f)
                self.project_data['document_list'].extend(document_list[0])
                with open(first_general_docs_file, 'rb') as f:
                    document_list = pickle.load(f)
                self.project_data['document_list'].extend(document_list[0])
                with open(second_general_docs_file, 'rb') as f:
                    document_list = pickle.load(f)
                self.project_data['document_list'].extend(document_list[0])
                self.project_data['document_list'] = \
                    list(set(self.project_data['document_list']))
            except:
                pass
            try:
                self.project_data['patient_list'] = []
                #idx_list = [0, 1, 2]
                idx_list = [3]
                with open(covid_positive_groups_file, 'rb') as f:
                    patient_lists = pickle.load(f)
                patient_list = []
                for idx in idx_list:
                    patient_list.extend(patient_lists[idx])
                self.project_data['patient_list'].extend(patient_list)
                with open(second_general_groups_file, 'rb') as f:
                    patient_lists = pickle.load(f)
                patient_list = []
                for idx in idx_list:
                    patient_list.extend(patient_lists[idx])
                self.project_data['patient_list'].extend(patient_list)
                self.project_data['patient_list'] = \
                    list(set(self.project_data['patient_list']))
            except:
                pass
        
        #
        if True:
            raw_data_dir = \
                self.project_data['directory_manager'].pull_directory('raw_data_dir')
            raw_data_file = os.path.join(raw_data_dir, 'ccc19_testing.xlsx')
            book = read_xlsx_file(raw_data_file)
            sheet = book.sheet_by_index(0)
            patient_list = sheet.col_values(1)
            document_list = sheet.col_values(2)
            self.project_data['patient_list'] = list(set(patient_list[1:]))
            self.project_data['document_list'] = list(set(document_list[1:]))

    	#
        return self.project_data