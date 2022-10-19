# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 09:57:35 2020

@author: haglers
"""

#
import os
import pickle
import traceback

#
from nlp_pipeline_lib.static_data_lib.static_data_manager_class \
    import Static_data_manager

#
class BeatAML_Waves_1_And_2_static_data_manager(Static_data_manager):
    
    #
    def __init__(self, operation_mode, user, root_dir_flg, project_subdir=None):
        project_name = 'BeatAML_Waves_1_And_2'
        Static_data_manager.__init__(self, operation_mode, user, root_dir_flg,
                                     project_name=project_name,
                                     project_subdir=project_subdir)
        self.project_subdir = project_subdir
        self.user = user
        
        self.static_data['document_identifiers'] = [ 'CSN' ]
        self.static_data['queries_list'] = \
            [ ('Antibodies.Tested', [ 'ANTIBODIES TESTED' ], 'ANTIGENS', 'ANTIBODIES_TESTED', 'multiple_values', True),
              ('dxAtSpecimenAcquisition', [ 'DIAGNOSIS', 'COMMENT', 'AMENDMENT COMMENT' ], 'DIAGNOSIS', 'DIAGNOSIS', 'multiple_values', True),
              ('dx.Date', [ 'HISTORY', 'COMMENT', 'AMENDMENT COMMENT', 'DIAGNOSIS' ], 'DIAGNOSIS_DATE', 'DATE', 'multiple_values', True),
              ('Extramedullary.dx', [ 'DIAGNOSIS', 'COMMENT', 'AMENDMENT COMMENT' ], 'EXTRAMEDULLARY_DISEASE', 'EXTRAMEDULLARY_DISEASE', 'multiple_values', True),
              ('FAB/Blast.Morphology', [ 'COMMENT', 'AMENDMENT COMMENT', 'BONE MARROW' ], 'FAB_CLASSIFICATION', 'FAB_CLASSIFICATION', 'multiple_values', True),
              ('FISH.Analysis.Summary', [ 'FISH ANALYSIS SUMMARY' ], 'FISH_ANALYSIS_SUMMARY', 'FISH_ANALYSIS_SUMMARY', 'multiple_values', True),
              ('Karyotype', [ 'KARYOTYPE', 'IMPRESSIONS AND RECOMMENDATIONS' ], 'KARYOTYPE', 'KARYOTYPE', 'multiple_values', True),
              ('%.Blasts.in.BM', [ 'DIAGNOSIS', 'BONE MARROW DIFFERENTIAL', 'BONE MARROW ASPIRATE' ], 'BONE_MARROW_BLAST', 'BLAST_PERCENTAGE', 'multiple_values', True),
              ('%.Blasts.in.PB', [ 'DIAGNOSIS', 'PERIPHERAL BLOOD MORPHOLOGY' ], 'PERIPHERAL_BLOOD_BLAST', 'BLAST_PERCENTAGE', 'multiple_values', True),
              ('Relapse.Date', [ 'HISTORY', 'COMMENT', 'AMENDMENT COMMENT', 'DIAGNOSIS' ], 'RELAPSE_DATE', 'DATE', 'multiple_values', True),
              ('Residual.dx', [ 'DIAGNOSIS', 'COMMENT', 'AMENDMENT COMMENT' ], 'RESIDUAL_DISEASE', 'DIAGNOSIS', 'multiple_values', True),
              ('specificDxAtAcquisition', [ 'DIAGNOSIS', 'COMMENT', 'AMENDMENT COMMENT' ], 'SPECIFIC_DIAGNOSIS', 'DIAGNOSIS', 'multiple_values', True),
              ('Surface.Antigens.(Immunohistochemical.Stains)', [ 'DIAGNOSIS', 'COMMENT', 'AMENDMENT COMMENT' ], 'IMMUNOPHENOTYPE', 'IMMUNOPHENOTYPE', 'multiple_values', True) ]
        self.static_data['remove_date'] = False
        self.static_data['validation_file'] = 'Sup Table 5 Clinical summary.xlsx'
        if self.project_subdir == 'test':
            self.static_data['raw_data_files'] = {}
            self.static_data['raw_data_files']['Beaker Results.xls'] = {}
            self.static_data['raw_data_files']['Beaker Results.xls']['DATETIME_FORMAT'] = '%m/%d/%Y'
            self.static_data['raw_data_files']['Beaker Results.xls']['DATETIME_KEY'] = 'SPECIMEN_COLL_DT'
            self.static_data['raw_data_files']['Beaker Results.xls']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['Bone Marrow Morph Report.xls'] = {}
            self.static_data['raw_data_files']['Bone Marrow Morph Report.xls']['DATETIME_FORMAT'] = '%m/%d/%Y'
            self.static_data['raw_data_files']['Bone Marrow Morph Report.xls']['DATETIME_KEY'] = 'SPECIMEN_COLL_DT'
            self.static_data['raw_data_files']['Bone Marrow Morph Report.xls']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['Chromosome Reports w Karyotype.xlsx'] = {}
            self.static_data['raw_data_files']['Chromosome Reports w Karyotype.xlsx']['DATETIME_FORMAT'] = '%m/%d/%Y'
            self.static_data['raw_data_files']['Chromosome Reports w Karyotype.xlsx']['DATETIME_KEY'] = 'SPECIMEN_COLL_DT'
            self.static_data['raw_data_files']['Chromosome Reports w Karyotype.xlsx']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['PowerPath Results.xls'] = {}
            self.static_data['raw_data_files']['PowerPath Results.xls']['DATETIME_FORMAT'] = '%m/%d/%Y'
            self.static_data['raw_data_files']['PowerPath Results.xls']['DATETIME_KEY'] = 'SPECIMEN_COLL_DT'
            self.static_data['raw_data_files']['PowerPath Results.xls']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['Beaker Chromosome Reports.xls'] = {}
            self.static_data['raw_data_files']['Beaker Chromosome Reports.xls']['DATETIME_FORMAT'] = '%m/%d/%Y'
            self.static_data['raw_data_files']['Beaker Chromosome Reports.xls']['DATETIME_KEY'] = 'SPECIMEN_COLL_DT'
            self.static_data['raw_data_files']['Beaker Chromosome Reports.xls']['NLP_MODE'] = 'CASE_NUMBER'
        else:
            if isinstance(self.project_subdir, str):
                print('Bad project_subdir value: ' + self.project_subdir)
            elif self.project_subdir is None:
                print('Bad project_subdir value: None')
        
        #
        raw_data_dir = \
            self.static_data['directory_manager'].pull_directory('raw_data_dir')
        if raw_data_dir is not None:
            raw_data_dir = raw_data_dir + '/pkl'
            pkl_file = os.path.join(raw_data_dir, 'training_groups.pkl')
            try:
                with open(pkl_file, 'rb') as f:
                    patient_lists = pickle.load(f)
                patient_list = []
                patient_list.extend(patient_lists[0])
                patient_list.extend(patient_lists[1])
                patient_list.extend(patient_lists[2])
                patient_list.extend(patient_lists[3])
                self.static_data['patient_list'] = patient_list
            except Exception:
                traceback.print_exc()