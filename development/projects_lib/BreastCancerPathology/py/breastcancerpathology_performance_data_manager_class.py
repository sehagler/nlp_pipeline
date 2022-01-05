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
from tool_lib.py.processing_tools_lib.file_processing_tools \
    import read_xlsx_file
from tool_lib.py.query_tools_lib.date_tools import compare_dates

#
class BreastCancerPathology_performance_data_manager(Performance_data_manager):
    
    #
    def __init__(self, static_data_manager, performance_json_manager,
                 project_json_manager):
        Performance_data_manager.__init__(self,  static_data_manager,
                                          performance_json_manager,
                                          project_json_manager)
        self.static_data = static_data_manager.get_static_data()
        self.identifier_key = 'SOURCE_SYSTEM_DOCUMENT_ID'
        validation_data = self._read_validation_data()
        self.identifier_list = self._get_validation_csn_list(validation_data)
        self.queries = [ ('ER_BLOCK', None, 'BREAST_CANCER_BIOMARKERS_ER', 'ER_BLOCK', 'single_value', True), 
                         ('ER_PERCENTAGE', None, 'BREAST_CANCER_BIOMARKERS_ER', 'ER_PERCENTAGE', 'single_value', True),
                         ('ER_SCORE', None, 'BREAST_CANCER_BIOMARKERS_ER', 'ER_SCORE', 'single_value', True),
                         ('ER_STATUS', None, 'BREAST_CANCER_BIOMARKERS_ER', 'ER_STATUS', 'single_value', True), 
                         ('HER2_BLOCK', None, 'BREAST_CANCER_BIOMARKERS_HER2', 'HER2_BLOCK', 'single_value', True),
                         ('HER2_PERCENTAGE', None, 'BREAST_CANCER_BIOMARKERS_HER2', 'HER2_PERCENTAGE', 'single_value', True),
                         ('HER2_SCORE', None, 'BREAST_CANCER_BIOMARKERS_HER2', 'HER2_SCORE', 'single_value', True), 
                         ('HER2_STATUS', None, 'BREAST_CANCER_BIOMARKERS_HER2', 'HER2_STATUS', 'single_value', True), 
                         ('KI67_BLOCK', None, 'BREAST_CANCER_BIOMARKERS_KI67', 'KI67_BLOCK', 'single_value', True),
                         ('KI67_PERCENTAGE', None, 'BREAST_CANCER_BIOMARKERS_KI67', 'KI67_PERCENTAGE', 'single_value', True),
                         ('KI67_STATUS', None, 'BREAST_CANCER_BIOMARKERS_KI67', 'KI67_STATUS', 'single_value', True),
                         ('PR_BLOCK', None, 'BREAST_CANCER_BIOMARKERS_PR', 'PR_BLOCK', 'single_value', True), 
                         ('PR_PERCENTAGE', None, 'BREAST_CANCER_BIOMARKERS_PR', 'PR_PERCENTAGE', 'single_value', True),
                         ('PR_SCORE', None, 'BREAST_CANCER_BIOMARKERS_PR', 'PR_SCORE', 'single_value', True), 
                         ('PR_STATUS', None, 'BREAST_CANCER_BIOMARKERS_PR', 'PR_STATUS', 'single_value', True) ]
        self.validation_filename = 'breastcancerpathology_testing.xlsx'
    
    #
    def _get_validation_csn_list(self, validation_data):
        if 'document_list' in self.static_data.keys():
            csn_list = self.static_data['document_list']
        else:
            csn_list = None
        validation_csn_list =  []
        for item in validation_data:
            if csn_list is None or item[2] in csn_list:
                validation_csn_list.append(item[2])
        validation_csn_list = list(set(validation_csn_list))
        return validation_csn_list
            
    #
    def _process_performance(self, nlp_values, validation_data):
        validation_csn_list = \
            self._get_validation_csn_list(validation_data)
        nlp_performance_dict = {}
        for i in range(len(self.queries)):
            validation_datum_key = self.queries[i][0]
            nlp_performance_dict[validation_datum_key] = []
        for csn in validation_csn_list:
            print(csn)
            for i in range(len(self.queries)):
                nlp_datum_key = self.queries[i][3]
                validation_datum_key = self.queries[i][0]
                performance = self._get_performance(csn, nlp_values,
                                                    nlp_datum_key,
                                                    validation_data,
                                                    validation_datum_key)
                nlp_performance_dict[validation_datum_key].append(performance)
        N = len(validation_csn_list)
        for key in nlp_performance_dict.keys():
            FN, FP, FP_plus_FN, TN, TP = \
                self._performance_values(nlp_performance_dict[key])
            self.performance_statistics_dict[key] = \
                self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
        
    #
    def _read_validation_data(self):
        validation_filename = 'breastcancerpathology_testing.xlsx'
        directory_manager = self.static_data['directory_manager']
        if 'patient_list' in self.static_data.keys():
            patient_list = self.static_data['patient_list']
        else:
            patient_list = None
        project_name = self.static_data['project_name']
        data_dir = directory_manager.pull_directory('raw_data_dir')
        book = read_xlsx_file(os.path.join(data_dir, validation_filename))
        sheet = book.sheet_by_index(0)
        ncols = sheet.ncols
        nrows = sheet.nrows
        validation_data = []
        for row_idx in range(nrows):
            validation_data_tmp = []
            for col_idx in range(ncols):
                cell_value = sheet.cell_value(row_idx, col_idx)
                try:
                    cell_value = str(int(cell_value))
                except:
                    pass
                validation_data_tmp.append(cell_value)
            validation_data.append(validation_data_tmp)
        return validation_data