# -*- coding: utf-8 -*-
"""
Created on Mon Mar 04 12:29:38 2019

@author: haglers
"""

#
import ast
import os

#
from nlp_pipeline_lib.py.performance_data_lib.performance_data_manager_class \
    import Performance_data_manager
from tool_lib.py.query_tools_lib.base_lib.date_tools_base import compare_dates

#
class BreastCancerPathology_performance_data_manager(Performance_data_manager):
    
    #
    def __init__(self, static_data_manager, json_manager_registry,
                 xls_manager_registry, evaluation_manager):
        Performance_data_manager.__init__(self,  static_data_manager,
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
            self.queries = static_data['queries_list']
    
    #
    def _generate_nlp_performance(self, nlp_performance_dict, csn, nlp_values,
                                  nlp_datum_key, validation_datum_key):
        performance = self._get_performance(csn, nlp_values, nlp_datum_key,
                                            validation_datum_key)
        nlp_performance_dict[validation_datum_key].append(performance)
        return nlp_performance_dict
            
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