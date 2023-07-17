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
class CCC19_performance_data_manager(Performance_data_manager):
    
    #
    def __init__(self, static_data_object, logger_object, evaluation_manager,
                 json_manager_registry, metadata_manager,
                 xls_manager_registry):
        Performance_data_manager.__init__(self, static_data_object,
                                          logger_object, evaluation_manager,
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
        if validation_datum_key == 'NORMALIZED_SMOKING_PRODUCTS':
            performance = self._get_smoking_products_performance(csn,
                                                                 nlp_values,
                                                                 nlp_datum_key,
                                                                 validation_datum_key)
        else:
            display_flg = True
            performance = self._get_performance(csn, nlp_values,
                                                nlp_datum_key,
                                                validation_datum_key,
                                                display_flg)
        if performance is not None:
            nlp_performance_dict[validation_datum_key].append(performance)
        return nlp_performance_dict
    
    #
    def _get_smoking_products_performance(self, csn, nlp_values, nlp_datum_key,
                                          validation_datum_key):
            if csn in nlp_values.keys():    
                data_out = nlp_values[csn]
            else:
                data_out = None
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
            display_flg = True
            performance = \
                self.evaluation_manager.evaluation(nlp_smoking_products_value,
                                                   validation_smoking_products_value,
                                                   display_flg)
            return performance
    
    #
    def _validation_datum_keys(self):
        validation_datum_keys = [ 'CANCER_STAGE', 'NORMALIZED_ECOG_SCORE',
                                  'NORMALIZED_SMOKING_HISTORY',
                                  'NORMALIZED_SMOKING_STATUS' ]
        return validation_datum_keys
        
    #
    def _validation_data_manager_column_to_int(self):
        self.validation_data_manager.column_to_int('CANCER_STAGE')
        self.validation_data_manager.column_to_int('NORMALIZED_ECOG_SCORE')