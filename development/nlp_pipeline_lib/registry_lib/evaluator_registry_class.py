# -*- coding: utf-8 -*-
"""
Created on Tue May  9 15:07:01 2023

@author: haglers
"""

#
import os
import traceback

#
from base_lib.registry_base_class import Registry_base

#
class Evaluator_registry(Registry_base):
    
    #
    def __init__(self, static_data_object, logger_object):
        Registry_base.__init__(self, static_data_object, logger_object)
        self.Tool_name = 'Evaluator_'
        self.tool_name = 'evaluator_'
            
    #
    def _get_import_cmds(self, filename):
        import_cmds = [ 'from query_lib.processor_lib.' + filename + \
                        ' import Evaluator as Object',
                        'from query_lib.processor_lib.base_lib.' + filename + \
                        ' import Evaluator as Object' ]
        return import_cmds
    
    #
    def push_software_directory(self, directory):
        self.software_dir = directory
        
    #
    def register_objects(self):
        static_data = self.static_data_object.get_static_data()
        operation_mode = static_data['operation_mode']
        root_dir = \
            os.path.join(self.software_dir, os.path.join(operation_mode, 'query_lib/processor_lib'))
        log_text = root_dir
        self.logger_object.print_log(log_text)
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                file = os.path.basename(file)
                self.register_object(file)
    
    #
    def run_object(self, evaluator, evaluation_manager, nlp_value, 
                      validation_value, display_flg):
        performance = \
            self.registry_dict[self.tool_name + evaluator].run_object(evaluation_manager, 
                                                                      nlp_value,
                                                                      validation_value,
                                                                      display_flg)
        return performance
    
    #
    def run_object_a(self, evaluator, evaluation_manager, nlp_value, 
                        validation_value, display_flg, value_range):
        performance = \
            self.registry_dict[self.tool_name + evaluator].run_object(evaluation_manager, 
                                                                      nlp_value,
                                                                      validation_value,
                                                                      display_flg,
                                                                      value_range)
        return performance