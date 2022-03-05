# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 09:57:35 2020

@author: haglers
"""

#
import os
import pickle

#
from nlp_lib.py.static_data_lib.static_data_manager_class \
    import Static_data_manager

#
class BeatAML_Waves_1_And_2_static_data_manager(Static_data_manager):
    
    #
    def __init__(self, operation_mode, project_subdir, user, root_dir_flg):
        project_name = 'BeatAML_Waves_1_And_2'
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
            'Sup Table 5 Clinical summary.xlsx'
        if self.project_subdir == 'test':
            self.static_data['raw_data_files'] = {}
            self.static_data['raw_data_files']['Beaker Results.xls'] = {}
            self.static_data['raw_data_files']['Beaker Results.xls']['DATETIME_FORMAT'] = '%m/%d/%Y'
            self.static_data['raw_data_files']['Beaker Results.xls']['FORMATTING'] = 'formatted'
            self.static_data['raw_data_files']['Beaker Results.xls']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['Bone Marrow Morph Report.xls'] = {}
            self.static_data['raw_data_files']['Bone Marrow Morph Report.xls']['DATETIME_FORMAT'] = '%m/%d/%Y'
            self.static_data['raw_data_files']['Bone Marrow Morph Report.xls']['FORMATTING'] = 'formatted'
            self.static_data['raw_data_files']['Bone Marrow Morph Report.xls']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['Chromosome Reports w Karyotype.xlsx'] = {}
            self.static_data['raw_data_files']['Chromosome Reports w Karyotype.xlsx']['DATETIME_FORMAT'] = '%m/%d/%Y'
            self.static_data['raw_data_files']['Chromosome Reports w Karyotype.xlsx']['FORMATTING'] = 'formatted'
            self.static_data['raw_data_files']['Chromosome Reports w Karyotype.xlsx']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['PowerPath Results.xls'] = {}
            self.static_data['raw_data_files']['PowerPath Results.xls']['DATETIME_FORMAT'] = '%m/%d/%Y'
            self.static_data['raw_data_files']['PowerPath Results.xls']['FORMATTING'] = 'formatted'
            self.static_data['raw_data_files']['PowerPath Results.xls']['NLP_MODE'] = 'RESULT_ID'
            self.static_data['raw_data_files']['Beaker Chromosome Reports.xls'] = {}
            self.static_data['raw_data_files']['Beaker Chromosome Reports.xls']['DATETIME_FORMAT'] = '%m/%d/%Y'
            self.static_data['raw_data_files']['Beaker Chromosome Reports.xls']['FORMATTING'] = 'formatted'
            self.static_data['raw_data_files']['Beaker Chromosome Reports.xls']['NLP_MODE'] = 'CASE_NUMBER'
        else:
            print('Bad project_subdir value')
        
        #
        raw_data_dir = \
            self.static_data['directory_manager'].pull_directory('raw_data_dir')
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
        except:
            pass
        
        #
        return self.static_data