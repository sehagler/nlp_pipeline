# -*- coding: utf-8 -*-
"""
Created on Mon Mar 04 12:29:38 2019

@author: haglers
"""

#
import os

#
from nlp_pipeline_lib.py.performance_data_lib.performance_data_manager_class \
    import Performance_data_manager
from tool_lib.py.query_tools_lib.base_lib.date_tools_base import compare_dates

#
class OhsuNlpTemplate_performance_data_manager(Performance_data_manager):
    
    #
    def __init__(self, static_data_manager, json_manager_registry,
                 xls_manager_registry, evaluation_manager):
        Performance_data_manager.__init__(self, static_data_manager, 
                                          json_manager_registry,
                                          xls_manager_registry,
                                          evaluation_manager)
        static_data = self.static_data_manager.get_static_data()
        if static_data['project_subdir'] == 'test':
            self.identifier_key = 'SOURCE_SYSTEM_DOCUMENT_ID'

            validation_filename = static_data['validation_file']
            directory_manager = static_data['directory_manager']
            project_name = static_data['project_name']
            data_dir = directory_manager.pull_directory('raw_data_dir')
            filename = os.path.join(data_dir, validation_filename)
            self.xls_manager_registry[filename].read_validation_data()
            self.identifier_list = self.xls_manager_registry[filename].get_validation_csn_list()
            
            self.queries = [ ('CANCER_STAGE', None, 'CANCER_STAGE', 'CANCER_STAGE', 'single_value', True),
                             ('NORMALIZED_ECOG_SCORE', None, 'ECOG_STATUS', 'NORMALIZED_ECOG_SCORE', 'single_value', True),
                             ('NORMALIZED_SMOKING_HISTORY', None, 'SMOKING_HISTORY', 'NORMALIZED_SMOKING_HISTORY', 'single_value', True),
                             ('NORMALIZED_SMOKING_PRODUCTS', None, 'SMOKING_PRODUCTS', 'NORMALIZED_SMOKING_PRODUCTS', 'multiple_values', False),
                             ('NORMALIZED_SMOKING_STATUS', None, 'SMOKING_STATUS', 'NORMALIZED_SMOKING_STATUS', 'single_value', True) ]
                
    #
    def _generate_nlp_performance(self, nlp_performance_dict, csn, nlp_values,
                                  nlp_datum_key, validation_datum_key):
        if validation_datum_key == 'NORMALIZED_SMOKING_PRODUCTS':
            performance = self._get_smoking_products_performance(csn,
                                                                 nlp_values,
                                                                 nlp_datum_key,
                                                                 validation_datum_key)
        else:
            performance = self._get_performance(csn, nlp_values,
                                                nlp_datum_key,
                                                validation_datum_key)
        nlp_performance_dict[validation_datum_key].append(performance)
        return nlp_performance_dict
    
    #
    def _get_smoking_products_performance(self, csn, nlp_values, nlp_datum_key,
                                          validation_datum_key):
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
            for i in range(1, self.validation_data_manager.length()):
                row = self.validation_data_manager.row(i)
                if row[2] == csn:
                    validation_smoking_products_value = \
                        self._process_validation_item(row[7])
            nlp_smoking_products_value = \
                self._nlp_to_tuple(nlp_smoking_products_value)
            validation_smoking_products_value = \
                self._validation_to_tuple(validation_smoking_products_value)
            performance, flg = \
                self.evaluation_manager.evaluation(nlp_smoking_products_value,
                                                   validation_smoking_products_value)
            return performance
        
    #
    def _process_performance(self, nlp_values):
        self.validation_data_manager.trim_validation_data()
        validation_csn_list = \
            self.validation_data_manager.get_validation_csn_list()
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
                column_labels = self.validation_data_manager.column_labels()
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
                                                       validation_datum_key)
                else:
                    nlp_performance_nlp_manual_review_dict = \
                        self._generate_nlp_performance(nlp_performance_nlp_manual_review_dict,
                                                       csn, nlp_values, nlp_datum_key,
                                                       validation_datum_key)
                    wo_nlp_manual_review_dict[validation_datum_key] += 1
        N_total = len(validation_csn_list)
        self._generate_performance_statistics(nlp_performance_wo_nlp_manual_review_dict,
                                              nlp_performance_nlp_manual_review_dict,
                                              N_total, wo_nlp_manual_review_dict)