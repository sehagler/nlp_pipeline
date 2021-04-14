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
class BeatAML_Waves_3_And_4_project_manager(Static_data_manager):
    
    #
    def __init__(self, operation_mode, project_subdir, user, root_dir_flg):
        project_name = 'BeatAML_Waves_3_And_4'
        Static_data_manager.__init__(self, operation_mode, project_name,
                                     project_subdir, user, root_dir_flg)
        self.project_subdir = project_subdir
        self.user = user
    
    #
    def get_project_data(self):
        self.static_data['datetime_identifiers'] = {}
        self.static_data['datetime_identifiers'][ 'RESULT_COMPLETED_DT' ] = '%m/%d/%Y'
        self.static_data['document_identifiers'] = [ 'CSN' ]
        self.static_data['flags'] = {}
        self.static_data['flags']['remove_date'] = False
        self.static_data['flags']['trim_data_by_csn'] = False
        self.static_data['formatting'] = 'formatted'
        self.static_data['header_values'] = [ 'Final Diagnosis', 'Final Pathologic Diagnosis',
                                               'Karyotype', 'Clinical History', 'Immunologic Analysis',
                                               'Laboratory Data', 'Microscopic Description',
                                               'Cytogenetic Analysis Summary', 'Impressions and Recommendations' ]
        self.static_data['json_files_key_value'] = [ ('bone_marrow_blast_file', 'bone_marrow_blast.json'),
                                                      ('diagnosis_file', 'diagnosis.json'),
                                                      ('diagnosis_date_file', 'diagnosis_date.json'),
                                                      ('extramedullary_disease_file', 'extramedullary_disease.json'),
                                                      ('fab_classification_file', 'fab_classification.json'),
                                                      ('immunophenotype_file', 'immunophenotype.json'),
                                                      ('peripheral_blood_blast_file', 'peripheral_blood_blast.json'),
                                                      ('relapse_date_file', 'relapse_date.json'),
                                                      ('residual_disease_file', 'residual_disease.json'),
                                                      ('sections_file', 'sections.json') ]
        self.static_data['patient_identifiers'] = ['MRN']
        self.static_data['raw_data_encoding'] = 'utf-8'
        self.static_data['raw_data_files'] = {}
        self.static_data['read_data_mode'] = 'get_data_by_document_value'
        if self.project_subdir == 'test':
            self.static_data['raw_data_files']['Beaker_Bone_Marrow_Morphology_Reports.xlsx'] = {}
            self.static_data['raw_data_files']['Beaker_Bone_Marrow_Morphology_Reports.xlsx']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['Beaker_Bone_Marrow_Morphology_Reports.xlsx']['NLP_PROCESS'] = 'BEATAML_REPORT'
            self.static_data['raw_data_files']['Beaker_Chromosome_Reports.xlsx'] = {}
            self.static_data['raw_data_files']['Beaker_Chromosome_Reports.xlsx']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['Beaker_Chromosome_Reports.xlsx']['NLP_PROCESS'] = 'CYTOGENETICS_REPORT'
            self.static_data['raw_data_files']['Beaker_Hematopathology_Reports.xlsx'] = {}
            self.static_data['raw_data_files']['Beaker_Hematopathology_Reports.xlsx']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['Beaker_Hematopathology_Reports.xlsx']['NLP_PROCESS'] = 'BEATAML_REPORT'
            self.static_data['raw_data_files']['PowerPath_Chromosome_Reports.xlsx'] = {}
            self.static_data['raw_data_files']['PowerPath_Chromosome_Reports.xlsx']['NLP_MODE'] = 'CASE_NUMBER'
            self.static_data['raw_data_files']['PowerPath_Chromosome_Reports.xlsx']['NLP_PROCESS'] = 'CYTOGENETICS_REPORT'
            self.static_data['raw_data_files']['PowerPath_Hematopathology_Reports.xlsx'] = {}
            self.static_data['raw_data_files']['PowerPath_Hematopathology_Reports.xlsx']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['PowerPath_Hematopathology_Reports.xlsx']['NLP_PROCESS'] = 'BEATAML_REPORT'
            self.static_data['raw_data_files_sequence'] = [ 'Beaker_Bone_Marrow_Morphology_Reports.xlsx',
                                                             'Beaker_Chromosome_Reports.xlsx',
                                                             'Beaker_Hematopathology_Reports.xlsx',
                                                             'PowerPath_Chromosome_Reports.xlsx',
                                                             'PowerPath_Hematopathology_Reports.xlsx' ]
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