# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 09:57:35 2020

@author: haglers
"""

#
import os
import xlrd

#
from nlp_lib.py.static_data_lib.static_data_manager_class \
    import Static_data_manager

#
class BeatAML_Waves_3_And_4_static_data_manager(Static_data_manager):
    
    #
    def __init__(self, operation_mode, project_subdir, user, root_dir_flg):
        project_name = 'BeatAML_Waves_3_And_4'
        Static_data_manager.__init__(self, operation_mode, project_name,
                                     project_subdir, user, root_dir_flg)
        self.project_subdir = project_subdir
        self.user = user
    
    #
    def get_static_data(self):
        self.static_data['document_identifiers'] = [ 'CSN' ]
        self.static_data['ohsu_nlp_template_files'] = \
            [ 'antigens.csv', 'fish_analysis_summary.csv', 'karyotype.csv' ]
        self.static_data['remove_date'] = False
        self.static_data['validation_file'] = \
            'wave3&4_unique_OHSU_clinical_summary_11_17_2020.xlsx'
        if self.project_subdir == 'test':
            self.static_data['raw_data_files'] = {}
            self.static_data['raw_data_files']['Beaker_Bone_Marrow_Morphology_Reports.xlsx'] = {}
            self.static_data['raw_data_files']['Beaker_Bone_Marrow_Morphology_Reports.xlsx']['DATETIME_FORMAT'] = '%m/%d/%Y'
            self.static_data['raw_data_files']['Beaker_Bone_Marrow_Morphology_Reports.xlsx']['FORMATTING'] = 'formatted'
            self.static_data['raw_data_files']['Beaker_Bone_Marrow_Morphology_Reports.xlsx']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['Beaker_Chromosome_Reports.xlsx'] = {}
            self.static_data['raw_data_files']['Beaker_Chromosome_Reports.xlsx']['DATETIME_FORMAT'] = '%m/%d/%Y'
            self.static_data['raw_data_files']['Beaker_Chromosome_Reports.xlsx']['FORMATTING'] = 'formatted'
            self.static_data['raw_data_files']['Beaker_Chromosome_Reports.xlsx']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['Beaker_Hematopathology_Reports.xlsx'] = {}
            self.static_data['raw_data_files']['Beaker_Hematopathology_Reports.xlsx']['DATETIME_FORMAT'] = '%m/%d/%Y'
            self.static_data['raw_data_files']['Beaker_Hematopathology_Reports.xlsx']['FORMATTING'] = 'formatted'
            self.static_data['raw_data_files']['Beaker_Hematopathology_Reports.xlsx']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['PowerPath_Chromosome_Reports.xlsx'] = {}
            self.static_data['raw_data_files']['PowerPath_Chromosome_Reports.xlsx']['DATETIME_FORMAT'] = '%m/%d/%Y'
            self.static_data['raw_data_files']['PowerPath_Chromosome_Reports.xlsx']['FORMATTING'] = 'formatted'
            self.static_data['raw_data_files']['PowerPath_Chromosome_Reports.xlsx']['NLP_MODE'] = 'CASE_NUMBER'
            self.static_data['raw_data_files']['PowerPath_Hematopathology_Reports.xlsx'] = {}
            self.static_data['raw_data_files']['PowerPath_Hematopathology_Reports.xlsx']['DATETIME_FORMAT'] = '%m/%d/%Y'
            self.static_data['raw_data_files']['PowerPath_Hematopathology_Reports.xlsx']['FORMATTING'] = 'formatted'
            self.static_data['raw_data_files']['PowerPath_Hematopathology_Reports.xlsx']['NLP_MODE'] = 'RESULT_ID'
        else:
            print('Bad project_subdir value')
        
        #
        raw_data_dir = \
            self.static_data['directory_manager'].pull_directory('raw_data_dir')
        data_file = os.path.join(raw_data_dir, 'wave3&4_unique_OHSU_clinical_summary_11_17_2020.xlsx')
        book = xlrd.open_workbook(data_file)
        sheet = book.sheet_by_index(0)
        patients = sheet.col_values(1)
        self.static_data['patient_list'] = patients[1:]
        
        #
        return self.static_data