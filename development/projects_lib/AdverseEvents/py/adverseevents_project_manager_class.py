# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 09:57:35 2020

@author: haglers
"""

#
from nlp_lib.py.static_data_lib.static_data_manager_class \
    import Static_data_manager

#
class AdverseEvents_project_manager(Static_data_manager):
    
    #
    def __init__(self, operation_mode, project_subdir, user, root_dir_flg):
        project_name = 'AdverseEvents'
        Static_data_manager.__init__(self, operation_mode, project_name, 
                                     project_subdir, user, root_dir_flg)
        self.project_subdir = project_subdir
    
    #
    def get_project_data(self):
        self.static_data['date_identifiers'] = {}
        self.static_data['date_identifiers'][ 'NOTE_DATE' ] = '%d-%b-%y'
        self.static_data['document_identifiers'] = [ 'SOURCE_SYSTEM_NOTE_CSN_ID' ]
        self.static_data['flags'] = {}
        self.static_data['flags']['remove_date'] = True
        self.static_data['flags']['trim_data_by_csn'] = True
        self.static_data['formatting'] = 'unformatted'
        self.static_data['json_files_key_value'] = []
        self.static_data['patient_identifiers'] = [ 'MRN_CD', 'OHSU_MRN', 'SRC_SYSTM_PAT_ID' ]
        self.static_data['raw_data_encoding'] = 'utf-8'
        self.static_data['text_identifiers'] = [ 'COMMENT_TEXT', 'ITEM_FREE_TEXT', 
                                                  'NOTE_TEXT', 'RESULT_TEXT' ]
        self.static_data['raw_data_files'] = {}
        self.static_data['read_data_mode'] = 'get_data_by_document_number'
        if self.project_subdir == 'test':
            self.static_data['raw_data_files']['Schuff_Hagler_AE_NLP_HNO_Notes.xml'] = {}
            self.static_data['raw_data_files']['Schuff_Hagler_AE_NLP_HNO_Notes.xml']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['Schuff_Hagler_AE_NLP_HNO_Notes.xml']['SOURCE_SYSTEM'] = 'BeakerAP'
            self.static_data['raw_data_files_sequence'] = [ 'Schuff_Hagler_AE_NLP_HNO_Notes.xml' ]
        else:
            print('Bad project_subdir value')   
        return self.static_data