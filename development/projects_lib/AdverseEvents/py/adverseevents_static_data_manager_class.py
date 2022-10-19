# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 09:57:35 2020

@author: haglers
"""

#
from nlp_pipeline_lib.static_data_lib.static_data_manager_class \
    import Static_data_manager

#
class AdverseEvents_static_data_manager(Static_data_manager):
    
    #
    def __init__(self, operation_mode, user, root_dir_flg, project_subdir=None):
        project_name = 'AdverseEvents'
        Static_data_manager.__init__(self, operation_mode, user, root_dir_flg,
                                     project_name=project_name,
                                     project_subdir=project_subdir)
        self.project_subdir = project_subdir
    
        self.static_data['document_identifiers'] = [ 'SOURCE_SYSTEM_NOTE_CSN_ID' ]
        self.static_data['patient_identifiers'] = [ 'MRN_CD', 'OHSU_MRN', 'SRC_SYSTM_PAT_ID' ]
        if self.project_subdir == 'test':
            self.static_data['raw_data_files'] = {}
            self.static_data['raw_data_files']['Schuff_Hagler_AE_NLP_HNO_Notes.xml'] = {}
            self.static_data['raw_data_files']['Schuff_Hagler_AE_NLP_HNO_Notes.xml']['DATETIME_FORMAT'] = '%Y/%m/%d %H:%M:%S'
            self.static_data['raw_data_files']['Schuff_Hagler_AE_NLP_HNO_Notes.xml']['DATETIME_KEY'] = 'NOTE_CREATED_DATE'
            self.static_data['raw_data_files']['Schuff_Hagler_AE_NLP_HNO_Notes.xml']['ENCODING'] = 'utf-16'
            self.static_data['raw_data_files']['Schuff_Hagler_AE_NLP_HNO_Notes.xml']['NLP_MODE'] = 'NONE'
            self.static_data['raw_data_files']['Schuff_Hagler_AE_NLP_HNO_Notes.xml']['SOURCE_SYSTEM'] = 'Epic Beaker'
            self.static_data['raw_data_files_sequence'] = [ 'Schuff_Hagler_AE_NLP_HNO_Notes.xml' ]
        else:
            print('Bad project_subdir value')   