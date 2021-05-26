# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 09:57:35 2020

@author: haglers
"""

#
from nlp_lib.py.static_data_lib.static_data_manager_class \
    import Static_data_manager

#
class BreastCancerPathology_project_manager(Static_data_manager):
    
    #
    def __init__(self, operation_mode, project_subdir, user, root_dir_flg):
        project_name = 'BreastCancerPathology'
        Static_data_manager.__init__(self, operation_mode, project_name, 
                                     project_subdir, user, root_dir_flg)
        self.project_subdir = project_subdir
    
    #
    def get_project_data(self):
        self.static_data['date_identifiers'] = {}
        self.static_data['date_identifiers'][ 'RESULT_COMPLETED_DT' ] = '%m/%d/%Y'
        self.static_data['document_identifiers'] = [ 'CSN' ]
        self.static_data['flags'] = {}
        self.static_data['flags']['remove_date'] = True
        self.static_data['flags']['trim_data_by_csn'] = True
        self.static_data['formatting'] = 'formatted'
        self.static_data['header_values'] = [ 'Final Pathologic Diagnosis' ]
        self.static_data['json_files_key_value'] = [ ('biomarker_json_file', 'biomarker.json'),
                                                      ('hist_diff_json_file', 'hist diff.json'),
                                                      ('hist_grade_json_file', 'hist grade.json'),
                                                      ('tumor_margin_json_file', 'tumor_margin.json'),
                                                      ('section_json_file', 'section.json'),
                                                      ('tumor_size_json_file', 'tumor size.json') ]
        self.static_data['patient_identifiers'] = ['MRN']
        self.static_data['raw_data_encoding'] = 'utf-8'
        self.static_data['raw_data_files'] = {}
        self.static_data['read_data_mode'] = 'get_data_by_document_value'
        if self.project_subdir == 'test':
            self.static_data['raw_data_files']['BreastCancerPathology.xls'] = {}
            self.static_data['raw_data_files']['BreastCancerPathology.xls']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['BreastCancerPathology.xls']['NLP_PROCESS'] = 'BREAST_CANCER_PATHOLOGY_REPORT'
        else:
            print('Bad project_subdir value')   
        return self.static_data