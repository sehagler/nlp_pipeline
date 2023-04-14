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
class BreastCancerPathology_performance_data_manager(Performance_data_manager):
    
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