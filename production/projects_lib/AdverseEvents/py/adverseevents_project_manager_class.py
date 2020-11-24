# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 09:57:35 2020

@author: haglers
"""

#
from nlp_lib.py.manager_lib.project_manager_class import Project_manager

#
class AdverseEvents_project_manager(Project_manager):
    
    #
    def __init__(self, operation_mode, user, root_dir_flg):
        project_name = 'AdverseEvents'
        Project_manager.__init__(self, project_name, operation_mode, user, root_dir_flg)
    
    #
    def get_project_data(self):
        self.project_data['date_identifiers'] = {}
        self.project_data['date_identifiers'][ 'NOTE_DATE' ] = '%d-%b-%y'
        self.project_data['document_identifiers'] = [ 'SOURCE_SYSTEM_NOTE_CSN_ID' ]
        self.project_data['flags'] = {}
        self.project_data['flags']['remove_date'] = True
        self.project_data['flags']['trim_data_by_csn'] = True
        self.project_data['json_files_key_value'] = []
        self.project_data['patient_identifiers'] = [ 'MRN_CD', 'OHSU_MRN', 'SRC_SYSTM_PAT_ID' ]
        self.project_data['raw_data_encoding'] = 'utf-8'
        self.project_data['raw_data_files'] = {}
        self.project_data['raw_data_files']['Schuff_Hagler_AE_NLP_HNO_Notes.xml'] = {}
        self.project_data['raw_data_files']['Schuff_Hagler_AE_NLP_HNO_Notes.xml']['NLP_MODE'] = 'RESULT_ID'
        self.project_data['raw_data_files']['Schuff_Hagler_AE_NLP_HNO_Notes.xml']['NLP_PROCESS'] = 'NOTE'
        self.project_data['raw_data_files']['Schuff_Hagler_AE_NLP_HNO_Notes.xml']['SOURCE_SYSTEM'] = 'BeakerAP'
        self.project_data['raw_data_files_sequence'] = [ 'Schuff_Hagler_AE_NLP_HNO_Notes.xml' ]
        self.project_data['text_identifiers'] = [ 'COMMENT_TEXT', 'ITEM_FREE_TEXT', 
                                                  'NOTE_TEXT', 'RESULT_TEXT' ]
        self.project_data['xml_metadata_keys'] = ['NLP_PROCESS']
        self._create_processors()    
        return self.project_data