# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 09:57:35 2020

@author: haglers
"""

#
import os
import xlrd

#
from nlp_pipeline_lib.static_data_lib.static_data_manager_class \
    import Static_data_manager

#
class BeatAML_Waves_3_And_4_static_data_manager(Static_data_manager):
    
    #
    def __init__(self, operation_mode, user, root_dir_flg, project_subdir=None):
        project_name = 'BeatAML_Waves_3_And_4'
        Static_data_manager.__init__(self, operation_mode, user, root_dir_flg,
                                     project_name=project_name,
                                     project_subdir=project_subdir)
        self.project_subdir = project_subdir
        
        self.static_data['document_identifiers'] = [ 'CSN' ]
        self.static_data['queries_list'] = \
            [ ('Antibodies.Tested', [ 'ANTIBODIES TESTED' ], 'ANTIGENS', 'ANTIBODIES_TESTED', 'multiple_values', True),
              ('dxAtSpecimenAcquisition', [ 'DIAGNOSIS', 'COMMENT', 'AMENDMENT COMMENT' ], 'DIAGNOSIS', 'DIAGNOSIS', 'multiple_values', True),
              ('dx.Date', [ 'HISTORY', 'COMMENT', 'AMENDMENT COMMENT', 'DIAGNOSIS' ], 'DIAGNOSIS_DATE', 'DATE', 'multiple_values', True),
              ('Extramedullary.dx', [ 'DIAGNOSIS', 'COMMENT', 'AMENDMENT COMMENT' ], 'EXTRAMEDULLARY_DISEASE', 'EXTRAMEDULLARY_DISEASE', 'multiple_values', True),
              ('FAB/Blast.Morphology', [ 'COMMENT', 'AMENDMENT COMMENT', 'BONE MARROW' ], 'FAB_CLASSIFICATION', 'FAB_CLASSIFICATION', 'multiple_values', True),
              ('FISH.Analysis.Summary', [ 'FISH ANALYSIS SUMMARY' ], 'FISH_ANALYSIS_SUMMARY', 'FISH_ANALYSIS_SUMMARY', 'multiple_values', True),
              ('karyotype', [ 'KARYOTYPE', 'IMPRESSIONS AND RECOMMENDATIONS' ], 'KARYOTYPE', 'KARYOTYPE', 'multiple_values', True),
              ('%.Blasts.in.BM', [ 'DIAGNOSIS', 'BONE MARROW DIFFERENTIAL', 'BONE MARROW ASPIRATE' ], 'BONE_MARROW_BLAST', 'BLAST_PERCENTAGE', 'multiple_values', True),
              ('%.Blasts.in.PB', [ 'DIAGNOSIS', 'PERIPHERAL BLOOD MORPHOLOGY' ], 'PERIPHERAL_BLOOD_BLAST', 'BLAST_PERCENTAGE', 'multiple_values', True),
              ('Relapse.Date', [ 'HISTORY', 'COMMENT', 'AMENDMENT COMMENT', 'DIAGNOSIS' ], 'RELAPSE_DATE', 'DATE', 'multiple_values', True),
              ('Residual.dx', [ 'DIAGNOSIS', 'COMMENT', 'AMENDMENT COMMENT' ], 'RESIDUAL_DISEASE', 'DIAGNOSIS', 'multiple_values', True),
              ('specificDxAtAcquisition', [ 'DIAGNOSIS', 'COMMENT', 'AMENDMENT COMMENT' ], 'SPECIFIC_DIAGNOSIS', 'DIAGNOSIS', 'multiple_values', True),
              ('surfaceAntigensImmunohistochemicalStains', [ 'DIAGNOSIS', 'COMMENT', 'AMENDMENT COMMENT' ], 'IMMUNOPHENOTYPE', 'IMMUNOPHENOTYPE', 'multiple_values', True) ]
        self.static_data['remove_date'] = False
        self.static_data['validation_file'] = 'wave3&4_unique_OHSU_clinical_summary_11_17_2020.xlsx'
        if self.project_subdir == 'test':
            self.static_data['raw_data_files'] = {}
            self.static_data['raw_data_files']['Beaker_Bone_Marrow_Morphology_Reports.xlsx'] = {}
            self.static_data['raw_data_files']['Beaker_Bone_Marrow_Morphology_Reports.xlsx']['DATETIME_FORMAT'] = '%m/%d/%Y'
            self.static_data['raw_data_files']['Beaker_Bone_Marrow_Morphology_Reports.xlsx']['DATETIME_KEY'] = 'SPECIMEN_COLL_DT'
            self.static_data['raw_data_files']['Beaker_Bone_Marrow_Morphology_Reports.xlsx']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['Beaker_Chromosome_Reports.xlsx'] = {}
            self.static_data['raw_data_files']['Beaker_Chromosome_Reports.xlsx']['DATETIME_FORMAT'] = '%m/%d/%Y'
            self.static_data['raw_data_files']['Beaker_Chromosome_Reports.xlsx']['DATETIME_KEY'] = 'SPECIMEN_COLL_DT'
            self.static_data['raw_data_files']['Beaker_Chromosome_Reports.xlsx']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['Beaker_Hematopathology_Reports.xlsx'] = {}
            self.static_data['raw_data_files']['Beaker_Hematopathology_Reports.xlsx']['DATETIME_FORMAT'] = '%m/%d/%Y'
            self.static_data['raw_data_files']['Beaker_Hematopathology_Reports.xlsx']['DATETIME_KEY'] = 'SPECIMEN_COLL_DT'
            self.static_data['raw_data_files']['Beaker_Hematopathology_Reports.xlsx']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['PowerPath_Chromosome_Reports.xlsx'] = {}
            self.static_data['raw_data_files']['PowerPath_Chromosome_Reports.xlsx']['DATETIME_FORMAT'] = '%m/%d/%Y'
            self.static_data['raw_data_files']['PowerPath_Chromosome_Reports.xlsx']['DATETIME_KEY'] = 'SPECIMEN_COLL_DT'
            self.static_data['raw_data_files']['PowerPath_Chromosome_Reports.xlsx']['NLP_MODE'] = 'CASE_NUMBER'
            self.static_data['raw_data_files']['PowerPath_Hematopathology_Reports.xlsx'] = {}
            self.static_data['raw_data_files']['PowerPath_Hematopathology_Reports.xlsx']['DATETIME_FORMAT'] = '%m/%d/%Y'
            self.static_data['raw_data_files']['PowerPath_Hematopathology_Reports.xlsx']['DATETIME_KEY'] = 'SPECIMEN_COLL_DT'
            self.static_data['raw_data_files']['PowerPath_Hematopathology_Reports.xlsx']['NLP_MODE'] = 'RESULT_ID'
        else:
            if isinstance(self.project_subdir, str):
                print('Bad project_subdir value: ' + self.project_subdir)
            elif self.project_subdir is None:
                print('Bad project_subdir value: None')
        
        #
        raw_data_dir = \
            self.static_data['directory_manager'].pull_directory('raw_data_dir')
        if raw_data_dir is not None:
            data_file = \
                os.path.join(raw_data_dir, 'wave3&4_unique_OHSU_clinical_summary_11_17_2020.xlsx')
            book = xlrd.open_workbook(data_file)
            sheet = book.sheet_by_index(0)
            patients = sheet.col_values(1)
            self.static_data['patient_list'] = patients[1:]