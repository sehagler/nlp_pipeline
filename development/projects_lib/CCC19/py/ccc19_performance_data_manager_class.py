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
    def __init__(self, static_data_object, directory_object, logger_object,
                 evaluation_manager, json_manager_registry, metadata_manager,
                 xls_manager_registry, specimens_manager):
        Performance_data_manager.__init__(self, static_data_object,
                                          directory_object, logger_object,
                                          evaluation_manager,
                                          json_manager_registry,
                                          metadata_manager,
                                          xls_manager_registry,
                                          specimens_manager)
    
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