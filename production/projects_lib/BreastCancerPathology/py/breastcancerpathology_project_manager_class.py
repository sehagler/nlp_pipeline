# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 09:57:35 2020

@author: haglers
"""

#
from nlp_lib.py.manager_lib.project_manager_class import Project_manager

#
class BreastCancerPathology_project_manager(Project_manager):
    
    #
    def __init__(self, operation_mode, user, root_dir_flg):
        project_name = 'BreastCancerPathology'
        Project_manager.__init__(self, project_name, operation_mode, user, root_dir_flg)
    
    #
    def get_project_data(self):
        self.project_data['date_identifiers'] = {}
        self.project_data['date_identifiers'][ 'RESULT_COMPLETED_DT' ] = '%m/%d/%Y'
        self.project_data['header_values'] = [ 'Final Pathologic Diagnosis' ]
        self.project_data['json_files_key_value'] = [ ('biomarker_json_file', 'biomarker.json'),
                                                      ('hist_diff_json_file', 'hist diff.json'),
                                                      ('hist_grade_json_file', 'hist grade.json'),
                                                      ('tumor_margin_json_file', 'tumor_margin.json'),
                                                      ('section_json_file', 'section.json'),
                                                      ('tumor_size_json_file', 'tumor size.json') ]
        self.project_data['patient_identifiers'] = ['MRN']
        self.project_data['raw_data_encoding'] = 'utf-8'
        self.project_data['raw_data_files'] = {}
        self.project_data['raw_data_files']['BreastCancerPathology.xls'] = {}
        self.project_data['raw_data_files']['BreastCancerPathology.xls']['NLP_MODE'] = 'RESULT_ID'
        self.project_data['raw_data_files']['BreastCancerPathology.xls']['NLP_PROCESS'] = 'BREAST_CANCER_PATHOLOGY_REPORT'
        self.project_data['xml_metadata_keys'] = [ 'NLP_PROCESS', 'SOURCE_SYSTEM' ]
        self._create_processors()    
        return self.project_data