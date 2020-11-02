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
        self.project_data['json_files_key_value'] = []
        self.project_data['patient_identifiers'] = [ 'MRN_CD', 'OHSU_MRN', 'SRC_SYSTM_PAT_ID' ]
        self.project_data['raw_data_files'] = {}
        self.project_data['raw_data_files']['Schuff_Hagler_AE_NLP_HNO_Notes.xml'] = {}
        self.project_data['raw_data_files']['Schuff_Hagler_AE_NLP_HNO_Notes.xml']['NLP_MODE'] = 'RESULT_ID'
        self.project_data['raw_data_files']['Schuff_Hagler_AE_NLP_HNO_Notes.xml']['NLP_PROCESS'] = 'NOTE'
        self.project_data['raw_data_files']['Schuff_Hagler_AE_NLP_HNO_Notes.xml']['SOURCE_SYSTEM'] = 'BeakerAP'
        '''
        self.project_data['raw_data_files']['Schuff_Hagler_AE_NLP_Lab_Reslt.xml'] = {}
        self.project_data['raw_data_files']['Schuff_Hagler_AE_NLP_Lab_Reslt.xml']['NLP_MODE'] = 'RESULT_ID'
        self.project_data['raw_data_files']['Schuff_Hagler_AE_NLP_Lab_Reslt.xml']['NLP_PROCESS'] = 'LAB_RESULT'
        self.project_data['raw_data_files']['Schuff_Hagler_AE_NLP_Lab_Reslt.xml']['SOURCE_SYSTEM'] = 'BeakerAP'
        self.project_data['raw_data_files']['Schuff_Hagler_AE_NLP_Micro.xml'] = {}
        self.project_data['raw_data_files']['Schuff_Hagler_AE_NLP_Micro.xml']['NLP_MODE'] = 'RESULT_ID'
        self.project_data['raw_data_files']['Schuff_Hagler_AE_NLP_Micro.xml']['NLP_PROCESS'] = 'MICRO'
        self.project_data['raw_data_files']['Schuff_Hagler_AE_NLP_Micro.xml']['SOURCE_SYSTEM'] = 'BeakerAP'
        self.project_data['raw_data_files']['Schuff_Hagler_AE_NLP_Result_Comments.xml'] = {}
        self.project_data['raw_data_files']['Schuff_Hagler_AE_NLP_Result_Comments.xml']['NLP_MODE'] = 'RESULT_ID'
        self.project_data['raw_data_files']['Schuff_Hagler_AE_NLP_Result_Comments.xml']['NLP_PROCESS'] = 'RESULT_COMMENTS'
        self.project_data['raw_data_files']['Schuff_Hagler_AE_NLP_Result_Comments.xml']['SOURCE_SYSTEM'] = 'BeakerAP'
        self.project_data['raw_data_files']['Schuff_Hagler_AE_NLP_Admin_Med.xml'] = 'ADMINISTERED_MEDICATION
        self.project_data['raw_data_files']['Schuff_Hagler_AE_NLP_Ambulatory.xml'] = 'AMBULATORY'
        self.project_data['raw_data_files']['Schuff_Hagler_AE_NLP_Curr_Med.xml'] = 'CURRENT_MEDICATION'
        self.project_data['raw_data_files']['Schuff_Hagler_AE_NLP_Demographics.xml'] = 'DEMOGRAPHICS'
        self.project_data['raw_data_files']['Schuff_Hagler_AE_NLP_Enc_Attributes.xml'] = 'ENC_ATTRIBUTES'
        self.project_data['raw_data_files']['Schuff_Hagler_AE_NLP_Enc_Dx.xml'] = 'ENC_DIAGNOSIS'
        self.project_data['raw_data_files']['Schuff_Hagler_AE_NLP_Hosp.xml'] = 'HOSPITAL'
        self.project_data['raw_data_files']['Schuff_Hagler_AE_NLP_Micro.xml'] = 'MICRO'
        self.project_data['raw_data_files']['Schuff_Hagler_AE_NLP_Order_Med.xml'] = 'ORDER_MEDICATION'
        self.project_data['raw_data_files']['Schuff_Hagler_AE_NLP_Order_Proc.xml'] = 'ORDER_PROCEDURE'
        self.project_data['raw_data_files']['Schuff_Hagler_AE_NLP_Prob_List.xml'] = 'PROBLEM_LIST'
        self.project_data['raw_data_files']['Schuff_Hagler_AE_NLP_Surgery.xml'] = 'SURGERY'
        self.project_data['raw_data_files']['Schuff_Hagler_AE_NLP_Vitals.xml'] = 'VITALS'
        '''
        self.project_data['raw_data_files_sequence'] = [ 'Schuff_Hagler_AE_NLP_HNO_Notes.xml' ]
        self.project_data['text_identifiers'] = [ 'COMMENT_TEXT', 'ITEM_FREE_TEXT', 
                                                  'NOTE_TEXT', 'RESULT_TEXT' ]
        self.project_data['xml_metadata_keys'] = ['NLP_PROCESS']
        self._create_processors()    
        return self.project_data