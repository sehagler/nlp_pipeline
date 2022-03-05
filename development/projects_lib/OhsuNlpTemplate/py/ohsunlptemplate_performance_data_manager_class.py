# -*- coding: utf-8 -*-
"""
Created on Mon Mar 04 12:29:38 2019

@author: haglers
"""

#
import os

#
from nlp_lib.py.performance_data_lib.performance_data_manager_class \
    import Performance_data_manager
from tool_lib.py.query_tools_lib.date_tools import compare_dates

#
class OhsuNlpTemplate_performance_data_manager(Performance_data_manager):
    
    #
    def __init__(self, static_data_manager, performance_json_manager,
                 project_json_manager):
        Performance_data_manager.__init__(self, static_data_manager, 
                                          performance_json_manager,
                                          project_json_manager)
        self.static_data = static_data_manager.get_static_data()
        self.identifier_key = 'SOURCE_SYSTEM_DOCUMENT_ID'
        validation_data = self._read_validation_data()
        self.identifier_list = self._get_validation_csn_list(validation_data)
        self.queries = [ ('CANCER_STAGE', None, 'CANCER_STAGE', 'CANCER_STAGE', 'single_value', True),
                         ('NORMALIZED_ECOG_SCORE', None, 'ECOG_STATUS', 'NORMALIZED_ECOG_SCORE', 'single_value', True),
                         ('NORMALIZED_SMOKING_HISTORY', None, 'SMOKING_HISTORY', 'NORMALIZED_SMOKING_HISTORY', 'single_value', True),
                         ('NORMALIZED_SMOKING_PRODUCTS', None, 'SMOKING_PRODUCTS', 'NORMALIZED_SMOKING_PRODUCTS', 'multiple_values', False),
                         ('NORMALIZED_SMOKING_STATUS', None, 'SMOKING_STATUS', 'NORMALIZED_SMOKING_STATUS', 'single_value', True) ]
                
    #
    def _generate_nlp_performance(self, nlp_performance_dict, csn, nlp_values,
                                  nlp_datum_key, validation_data, validation_datum_key):
        if validation_datum_key == 'NORMALIZED_SMOKING_PRODUCTS':
            performance = self._get_smoking_products_performance(csn,
                                                                 nlp_values,
                                                                 nlp_datum_key,
                                                                 validation_data,
                                                                 validation_datum_key)
        else:
            performance = self._get_performance(csn, nlp_values,
                                                nlp_datum_key,
                                                validation_data,
                                                validation_datum_key)
        nlp_performance_dict[validation_datum_key].append(performance)
        return nlp_performance_dict
    
    #
    def _get_smoking_products_performance(self, csn, nlp_values, nlp_datum_key,
                                          validation_data, validation_datum_key):
            data_out = nlp_values[csn]
            if data_out is not None:
                if nlp_datum_key in data_out.keys():
                    nlp_smoking_products_value = \
                        data_out[nlp_datum_key]
                    nlp_smoking_products_value_tmp = \
                        nlp_smoking_products_value
                    nlp_smoking_products_value = []
                    for item0 in nlp_smoking_products_value_tmp:
                        for item1 in item0:
                            nlp_smoking_products_value.append(item1)
                    nlp_smoking_products_value = \
                        list(set(nlp_smoking_products_value))
                else:
                    nlp_smoking_products_value = None
            else:
                nlp_smoking_products_value = None
            for item in validation_data:
                if item[2] == csn:
                    validation_smoking_products_value = \
                        self._process_validation_item(item[7])
            nlp_smoking_products_value = \
                self._nlp_to_tuple(nlp_smoking_products_value)
            validation_smoking_products_value = \
                self._validation_to_tuple(validation_smoking_products_value)
            performance, flg = \
                self._compare_data_values(nlp_smoking_products_value,
                                          validation_smoking_products_value)
            return performance
        
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
        validation_datum_keys = [ 'CANCER_STAGE', 'NORMALIZED_ECOG_SCORE',
                                  'NORMALIZED_SMOKING_HISTORY',
                                  'NORMALIZED_SMOKING_STATUS' ]
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
        if 'patient_list' in self.static_data.keys():
            patient_list = self.static_data['patient_list']
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