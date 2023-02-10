# -*- coding: utf-8 -*-
"""
Created on Mon Mar 04 12:29:38 2019

@author: haglers
"""

#
import os

#
from nlp_pipeline_lib.manager_lib.performance_data_lib.performance_data_manager_class \
    import Performance_data_manager

#
class KDLReports_performance_data_manager(Performance_data_manager):
    
    #
    def __init__(self, static_data_object, evaluation_manager,
                 json_manager_registry, metadata_manager,
                 xls_manager_registry):
        Performance_data_manager.__init__(self, static_data_object,
                                          evaluation_manager,
                                          json_manager_registry,
                                          metadata_manager,
                                          xls_manager_registry)
        static_data = self.static_data_object.get_static_data()
        if static_data['project_subdir'] == 'test':
            self.identifier_key = 'SOURCE_SYSTEM_DOCUMENT_ID'
            validation_filename = static_data['validation_file']
            directory_manager = static_data['directory_manager']
            data_dir = directory_manager.pull_directory('raw_data_dir')
            filename = os.path.join(data_dir, validation_filename)
            self.xls_manager_registry[filename].read_validation_data()
            self.queries = static_data['queries_list']
    
    #
    def _generate_nlp_performance(self, nlp_performance_dict, csn, nlp_values,
                                  nlp_datum_key, validation_datum_key):
        display_flg = True
        performance = self._get_performance(csn, nlp_values, nlp_datum_key,
                                            validation_datum_key,
                                            display_flg)
        nlp_performance_dict[validation_datum_key].append(performance)
        return nlp_performance_dict
            
    #
    def _process_performance(self, nlp_values):
        document_csn_list = \
            self.metadata_manager.pull_document_identifier_list('SOURCE_SYSTEM_DOCUMENT_ID')
        self.validation_data_manager.trim_validation_data()
        validation_csn_list = \
            self.validation_data_manager.get_validation_csn_list()
        nlp_performance_wo_validation_manual_review_dict = {}
        nlp_performance_w_validation_manual_review_dict = {}
        wo_validation_manual_review_dict = {}
        wo_nlp_manual_review_dict = {}
        for i in range(len(self.queries)):
            validation_datum_key = self.queries[i][0]
            nlp_performance_wo_validation_manual_review_dict[validation_datum_key] = []
            nlp_performance_w_validation_manual_review_dict[validation_datum_key] = []
            wo_validation_manual_review_dict[validation_datum_key] = 0
            wo_nlp_manual_review_dict[validation_datum_key] = 0
        validation_datum_keys = []
        for query in self.queries:
            validation_datum_keys.append(query[0])
        nlp_values = \
            self._identify_manual_review(nlp_values, validation_datum_keys)
        N_manual_review = {}
        hit_documents_dict = {}
        hit_manual_review_dict = {}
        for csn in document_csn_list:
            print(csn)
            for i in range(len(self.queries)):
                nlp_datum_key = self.queries[i][3]
                if nlp_datum_key not in N_manual_review.keys():
                    N_manual_review[nlp_datum_key] = 0
                if nlp_datum_key not in hit_documents_dict.keys():
                    hit_documents_dict[nlp_datum_key] = []
                if nlp_datum_key not in hit_manual_review_dict.keys():
                    hit_manual_review_dict[nlp_datum_key] = []
                validation_datum_key = self.queries[i][0]
                column_labels = self.validation_data_manager.column_labels()
                for j in range(1, self.validation_data_manager.length()):
                    row = self.validation_data_manager.row(j)
                    validation_idx = \
                        [k for k in range(len(column_labels)) \
                         if column_labels[k] == validation_datum_key][0]
                    if row[2] == csn:
                        validation_value = \
                            self._process_validation_item(row[validation_idx])
                if validation_value is not None and self.manual_review in validation_value:
                        N_manual_review[nlp_datum_key] += 1
                if csn in nlp_values.keys() and nlp_values[csn] is not None:
                    if csn in nlp_values.keys():
                        if nlp_datum_key in nlp_values[csn].keys():
                            nlp_value = nlp_values[csn][nlp_datum_key]
                        else:
                            nlp_value = None
                    else:
                        nlp_value = None
                    if nlp_value is not None:
                        hit_documents_dict[nlp_datum_key].append(csn)
                        if validation_value is not None and self.manual_review in validation_value:
                            hit_manual_review_dict[nlp_datum_key].append(csn)
                    if csn in validation_csn_list:
                        if not ( validation_value is not None and self.manual_review in validation_value ):
                            nlp_performance_wo_validation_manual_review_dict = \
                                self._generate_nlp_performance(nlp_performance_wo_validation_manual_review_dict,
                                                               csn, nlp_values, nlp_datum_key,
                                                               validation_datum_key)
                        else:
                            nlp_performance_w_validation_manual_review_dict = \
                                self._generate_nlp_performance(nlp_performance_w_validation_manual_review_dict,
                                                               csn, nlp_values, nlp_datum_key,
                                                               validation_datum_key)
                else:
                    if validation_value == None:
                        nlp_performance_wo_validation_manual_review_dict[nlp_datum_key].append('true negative')
                    elif self.manual_review in validation_value:
                        nlp_performance_w_validation_manual_review_dict[nlp_datum_key].append('false negative')
                        print('false negative')
                        print(None)
                        print(validation_value)
                        print('')
                    else:
                        nlp_performance_wo_validation_manual_review_dict[nlp_datum_key].append('false negative')
                        print('false negative')
                        print(None)
                        print(validation_value)
                        print('')
        N_documents = len(document_csn_list)
        N_hit_documents_wo_validation_manual_review_dict = {}
        for key in hit_documents_dict.keys():
            N_hit_documents_wo_validation_manual_review_dict[key] = \
                len(list(set(hit_documents_dict[key])))
        N_hit_documents_w_validation_manual_review_dict = {}
        for key in hit_manual_review_dict.keys():
            N_hit_documents_w_validation_manual_review_dict[key] = \
                len(list(set(hit_manual_review_dict[key])))
        self._generate_performance_statistics(nlp_performance_wo_validation_manual_review_dict,
                                              nlp_performance_w_validation_manual_review_dict,
                                              N_documents, N_manual_review,
                                              N_hit_documents_wo_validation_manual_review_dict,
                                              N_hit_documents_w_validation_manual_review_dict)