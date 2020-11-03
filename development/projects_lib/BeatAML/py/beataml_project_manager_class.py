# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 09:57:35 2020

@author: haglers
"""

#
import os
import pickle

#
from nlp_lib.py.manager_lib.project_manager_class import Project_manager

#
class BeatAML_project_manager(Project_manager):
    
    #
    def __init__(self, operation_mode, user, root_dir_flg):
        project_name = 'BeatAML'
        Project_manager.__init__(self, project_name, operation_mode, user, root_dir_flg)
        self.user = user
    
    #
    def get_project_data(self):
        self.project_data['date_identifiers'] = {}
        self.project_data['date_identifiers'][ 'RESULT_COMPLETED_DT' ] = '%m/%d/%Y'
        self.project_data['header_values'] = [ 'Final Diagnosis', 'Final Pathologic Diagnosis',
                                               'Karyotype', 'Clinical History', 'Immunologic Analysis',
                                               'Laboratory Data', 'Microscopic Description',
                                               'Cytogenetic Analysis Summary', 'Impressions and Recommendations' ]
        self.project_data['json_files_key_value'] = [ ('bone_marrow_blast_file', 'bone_marrow_blast.json'),
                                                      ('diagnosis_file', 'diagnosis.json'),
                                                      ('diagnosis_date_file', 'diagnosis_date.json'),
                                                      ('extramedullary_disease_file', 'extramedullary_disease.json'),
                                                      ('fab_classification_file', 'fab_classification.json'),
                                                      ('immunophenotype_file', 'immunophenotype.json'),
                                                      ('peripheral_blood_blast_file', 'peripheral_blood_blast.json'),
                                                      ('relapse_date_file', 'relapse_date.json'),
                                                      ('residual_disease_file', 'residual_disease.json'),
                                                      ('sections_file', 'sections.json') ]
        self.project_data['patient_identifiers'] = ['MRN']
        self.project_data['raw_data_encoding'] = 'utf-8'
        self.project_data['raw_data_files'] = {}
        self.project_data['raw_data_files']['Beaker Results.xls'] = {}
        self.project_data['raw_data_files']['Beaker Results.xls']['NLP_MODE'] = 'RESULT_ID'
        self.project_data['raw_data_files']['Beaker Results.xls']['NLP_PROCESS'] = 'BEATAML_REPORT'
        self.project_data['raw_data_files']['Bone Marrow Morph Report.xls'] = {}
        self.project_data['raw_data_files']['Bone Marrow Morph Report.xls']['NLP_MODE'] = 'RESULT_ID'
        self.project_data['raw_data_files']['Bone Marrow Morph Report.xls']['NLP_PROCESS'] = 'BEATAML_REPORT'
        self.project_data['raw_data_files']['Chromosome Reports w Karyotype.xlsx'] = {}
        self.project_data['raw_data_files']['Chromosome Reports w Karyotype.xlsx']['NLP_MODE'] = 'RESULT_ID'
        self.project_data['raw_data_files']['Chromosome Reports w Karyotype.xlsx']['NLP_PROCESS'] = 'CYTOGENETICS_REPORT'
        self.project_data['raw_data_files']['PowerPath Results.xls'] = {}
        self.project_data['raw_data_files']['PowerPath Results.xls']['NLP_MODE'] = 'RESULT_ID'
        self.project_data['raw_data_files']['PowerPath Results.xls']['NLP_PROCESS'] = 'BEATAML_REPORT'
        self.project_data['raw_data_files']['Beaker Chromosome Reports.xls'] = {}
        self.project_data['raw_data_files']['Beaker Chromosome Reports.xls']['NLP_MODE'] = 'CASE_NUMBER'
        self.project_data['raw_data_files']['Beaker Chromosome Reports.xls']['NLP_PROCESS'] = 'CYTOGENETICS_REPORT'
        '''
        self.project_data['raw_data_files_sequence'] = [ 'PowerPath Results.xls',
                                                         'Beaker Results.xls',
                                                         'Bone Marrow Morph Report.xls',
                                                         'Chromosome Reports w Karyotype.xlsx',
                                                         'Beaker Chromosome Reports.xls' ]
        '''
        self.project_data['xml_metadata_keys'] = [ 'NLP_PROCESS', 'SOURCE_SYSTEM' ]
        self._create_processors()
        
        #
        raw_data_dir = \
            self.project_data['directory_manager'].pull_directory('raw_data_dir')
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
            self.project_data['patient_list'] = patient_list
        except:
            pass
        
        #
        return self.project_data