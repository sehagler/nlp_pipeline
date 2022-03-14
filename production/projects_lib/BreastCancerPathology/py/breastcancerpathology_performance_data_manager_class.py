# -*- coding: utf-8 -*-
"""
Created on Mon Mar 04 12:29:38 2019

@author: haglers
"""

#
import ast
import os

#
from nlp_lib.py.performance_data_lib.performance_data_manager_class \
    import Performance_data_manager
from tool_lib.py.query_tools_lib.date_tools import compare_dates

#
class BreastCancerPathology_performance_data_manager(Performance_data_manager):
    
    #
    def __init__(self, static_data_manager, json_manager_registry):
        Performance_data_manager.__init__(self,  static_data_manager,
                                          json_manager_registry)
        static_data = self.static_data_manager.get_static_data()
        if static_data['project_subdir'] == 'test':
            self.identifier_key = 'SOURCE_SYSTEM_DOCUMENT_ID'
            validation_data = self._read_validation_data()
            self.identifier_list = self._get_validation_csn_list(validation_data)
            self.queries = [ ('ER_BLOCK', None, 'BREAST_CANCER_BIOMARKERS_ER', 'ER_BLOCK', 'single_value', True), 
                             ('ER_PERCENTAGE', None, 'BREAST_CANCER_BIOMARKERS_ER', 'ER_PERCENTAGE', 'single_value', True),
                             ('ER_SCORE', None, 'BREAST_CANCER_BIOMARKERS_ER', 'ER_SCORE', 'single_value', True),
                             ('ER_STATUS', None, 'BREAST_CANCER_BIOMARKERS_ER', 'ER_STATUS', 'single_value', True),
                             ('ER_VARIABILITY', None, 'BREAST_CANCER_BIOMARKERS_ER', 'ER_VARIABILITY', 'single_value', True),
                             ('GATA3_BLOCK', None, 'BREAST_CANCER_BIOMARKERS_GATA3', 'GATA3_BLOCK', 'single_value', True),
                             ('GATA3_STATUS', None, 'BREAST_CANCER_BIOMARKERS_GATA3', 'GATA3_STATUS', 'single_value', True),
                             ('GATA3_VARIABILITY', None, 'BREAST_CANCER_BIOMARKERS_GATA3', 'GATA3_VARIABILITY', 'single_value', True),
                             ('HER2_BLOCK', None, 'BREAST_CANCER_BIOMARKERS_HER2', 'HER2_BLOCK', 'single_value', True),
                             #('HER2_PERCENTAGE', None, 'BREAST_CANCER_BIOMARKERS_HER2', 'HER2_PERCENTAGE', 'single_value', True),
                             ('HER2_SCORE', None, 'BREAST_CANCER_BIOMARKERS_HER2', 'HER2_SCORE', 'single_value', True), 
                             ('HER2_STATUS', None, 'BREAST_CANCER_BIOMARKERS_HER2', 'HER2_STATUS', 'single_value', True), 
                             ('HER2_VARIABILITY', None, 'BREAST_CANCER_BIOMARKERS_HER2', 'HER2_VARIABILITY', 'single_value', True),
                             ('KI67_BLOCK', None, 'BREAST_CANCER_BIOMARKERS_KI67', 'KI67_BLOCK', 'single_value', True),
                             ('KI67_PERCENTAGE', None, 'BREAST_CANCER_BIOMARKERS_KI67', 'KI67_PERCENTAGE', 'single_value', True),
                             #('KI67_STATUS', None, 'BREAST_CANCER_BIOMARKERS_KI67', 'KI67_STATUS', 'single_value', True),
                             ('KI67_VARIABILITY', None, 'BREAST_CANCER_BIOMARKERS_KI67', 'KI67_VARIABILITY', 'single_value', True),
                             ('PR_BLOCK', None, 'BREAST_CANCER_BIOMARKERS_PR', 'PR_BLOCK', 'single_value', True), 
                             ('PR_PERCENTAGE', None, 'BREAST_CANCER_BIOMARKERS_PR', 'PR_PERCENTAGE', 'single_value', True),
                             ('PR_SCORE', None, 'BREAST_CANCER_BIOMARKERS_PR', 'PR_SCORE', 'single_value', True), 
                             ('PR_STATUS', None, 'BREAST_CANCER_BIOMARKERS_PR', 'PR_STATUS', 'single_value', True),
                             ('PR_VARIABILITY', None, 'BREAST_CANCER_BIOMARKERS_PR', 'PR_VARIABILITY', 'single_value', True) ]
    
    #
    def _generate_nlp_performance(self, nlp_performance_dict, csn, nlp_values,
                                  nlp_datum_key, validation_data, validation_datum_key):
        performance = self._get_performance(csn, nlp_values, nlp_datum_key,
                                            validation_data, validation_datum_key)
        nlp_performance_dict[validation_datum_key].append(performance)
        return nlp_performance_dict
            
    #
    def _process_performance(self, nlp_values, validation_data):
        validation_data = self._trim_validation_data(validation_data)
        validation_csn_list = \
            self._get_validation_csn_list(validation_data)
        nlp_performance_wo_nlp_manual_review_dict = {}
        nlp_performance_nlp_manual_review_dict = {}
        wo_validation_manual_review_dict = {}
        wo_nlp_manual_review_dict = {}
        for i in range(len(self.queries)):
            validation_datum_key = self.queries[i][0]
            nlp_performance_wo_nlp_manual_review_dict[validation_datum_key] = []
            nlp_performance_nlp_manual_review_dict[validation_datum_key] = []
            wo_validation_manual_review_dict[validation_datum_key] = 0
            wo_nlp_manual_review_dict[validation_datum_key] = 0
        validation_datum_keys = []
        for query in self.queries:
            validation_datum_keys.append(query[0])
        nlp_values = \
            self._identify_manual_review(nlp_values, validation_datum_keys)
        for csn in validation_csn_list:
            print(csn)
            for i in range(len(self.queries)):
                nlp_datum_key = self.queries[i][3]
                validation_datum_key = self.queries[i][0]
                column_labels = validation_data[0]
                if nlp_values[csn] is not None:
                    if nlp_datum_key in nlp_values[csn].keys():
                        nlp_value = nlp_values[csn][nlp_datum_key]
                    else:
                        nlp_value = None
                else:
                    nlp_value = None
                if not ( nlp_value is not None and self.manual_review in nlp_value ):
                    nlp_performance_wo_nlp_manual_review_dict = \
                        self._generate_nlp_performance(nlp_performance_wo_nlp_manual_review_dict,
                                                       csn, nlp_values, nlp_datum_key,
                                                       validation_data, validation_datum_key)
                else:
                    nlp_performance_nlp_manual_review_dict = \
                        self._generate_nlp_performance(nlp_performance_nlp_manual_review_dict,
                                                       csn, nlp_values, nlp_datum_key,
                                                       validation_data, validation_datum_key)
                    wo_nlp_manual_review_dict[validation_datum_key] += 1
        N_total = len(validation_csn_list)
        self._generate_performance_statistics(nlp_performance_wo_nlp_manual_review_dict,
                                              nlp_performance_nlp_manual_review_dict,
                                              N_total, wo_nlp_manual_review_dict)
        
    #
    def _trim_validation_data(self, validation_data_in):
        static_data = self.static_data_manager.get_static_data()
        if 'patient_list' in static_data.keys():
            patient_list = static_data['patient_list']
            for i in range(len(patient_list)):
                patient_list[i] = int(patient_list[i])
        else:
            patient_list = None
        validation_data_out =  []
        validation_data_out.append(validation_data_in[0])
        validation_data_in = validation_data_in[1:]
        for item in validation_data_in:
            print(item[1])
            if patient_list is None or int(item[1]) in patient_list:
                validation_data_out.append(item)
        return validation_data_out