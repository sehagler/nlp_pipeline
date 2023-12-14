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
from static_data_lib.object_lib.static_data_object_class import Static_data_object

#
class BeatAML_Waves_1_And_2_static_data_object(Static_data_object):
    
    #
    def __init__(self, operation_mode, user, root_dir_flg, project_subdir=None):
        project_name = 'BeatAML_Waves_1_And_2'
        Static_data_object.__init__(self, operation_mode, user, root_dir_flg,
                                     project_name=project_name,
                                     project_subdir=project_subdir)
        self.project_subdir = project_subdir
        self.user = user
        
        self.static_data['document_identifiers'] = [ 'CSN' ]
        self.static_data['queries_list'] = \
            [ ('Antibodies.Tested', [ 'ANTIBODIES TESTED' ], 'ANTIGENS', 'ANTIBODIES_TESTED', 'multiple_values', True),
              ('dxAtSpecimenAcquisition', [ 'DX', 'COMMENT', 'AMENDMENT COMMENT' ], 'DIAGNOSIS', 'DIAGNOSIS', 'multiple_values', True),
              ('dx.Date', [ 'HX', 'COMMENT', 'AMENDMENT COMMENT', 'DX' ], 'DIAGNOSIS_DATE', 'DATE', 'multiple_values', True),
              ('Extramedullary.dx', [ 'DX', 'COMMENT', 'AMENDMENT COMMENT' ], 'EXTRAMEDULLARY_DISEASE', 'EXTRAMEDULLARY_DISEASE', 'multiple_values', True),
              ('FAB/Blast.Morphology', [ 'COMMENT', 'AMENDMENT COMMENT', 'BONE MARROW' ], 'FAB_CLASSIFICATION', 'FAB_CLASSIFICATION', 'multiple_values', True),
              ('FISH.Analysis.Summary', [ 'FISH ANALYSIS SUMMARY' ], 'FISH_ANALYSIS_SUMMARY', 'FISH_ANALYSIS_SUMMARY', 'multiple_values', True),
              ('Karyotype', [ 'KARYOTYPE', 'IMPRESSIONS AND RECOMMENDATIONS' ], 'KARYOTYPE', 'KARYOTYPE', 'multiple_values', True),
              ('%.Blasts.in.BM', [ 'DX', 'BONE MARROW DIFFERENTIAL', 'BONE MARROW ASPIRATE' ], 'BONE_MARROW_BLAST', 'BLAST_PERCENTAGE', 'multiple_values', True),
              ('%.Blasts.in.PB', [ 'DX', 'PERIPHERAL BLOOD MORPHOLOGY' ], 'PERIPHERAL_BLOOD_BLAST', 'BLAST_PERCENTAGE', 'multiple_values', True),
              ('Relapse.Date', [ 'HX', 'COMMENT', 'AMENDMENT COMMENT', 'DX' ], 'RELAPSE_DATE', 'DATE', 'multiple_values', True),
              ('Residual.dx', [ 'DX', 'COMMENT', 'AMENDMENT COMMENT' ], 'RESIDUAL_DISEASE', 'DIAGNOSIS', 'multiple_values', True),
              ('specificDxAtAcquisition', [ 'DX', 'COMMENT', 'AMENDMENT COMMENT' ], 'SPECIFIC_DIAGNOSIS', 'DIAGNOSIS', 'multiple_values', True),
              ('Surface.Antigens.(Immunohistochemical.Stains)', [ 'DX', 'COMMENT', 'AMENDMENT COMMENT' ], 'IMMUNOPHENOTYPE', 'IMMUNOPHENOTYPE', 'multiple_values', True) ]
        self.static_data['remove_date'] = False
        self.static_data['validation_file'] = 'Sup Table 5 Clinical summary.xlsx'
        if self.project_subdir == 'test':
            self.static_data['deidentifier_flg'] = True
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
            self.static_data['deidentifier_flg'] = False
            if isinstance(self.project_subdir, str):
                print('Bad project_subdir value: ' + self.project_subdir)
            elif self.project_subdir is None:
                print('Bad project_subdir value: None')
        
        #
        if self.project_subdir is not None:
            raw_data_dir = \
                '/home/groups/hopper2/RDW_NLP_WORKSPACE/NLP/NLP_Source_Data/BeatAML_Waves_1_And_2'
            raw_data_dir += '/' + self.project_subdir
        else:
            raw_data_dir = None
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