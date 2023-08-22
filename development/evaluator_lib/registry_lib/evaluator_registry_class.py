# -*- coding: utf-8 -*-
"""
Created on Tue May  9 15:07:01 2023

@author: haglers
"""

#
import os
import re
import traceback

#
class Evaluator_registry(object):
    
    #
    def __init__(self, static_data_object, logger_object):
        self.static_data_object = static_data_object
        self.logger_object = logger_object
        self.evaluator_registry = {}
    
    #
    def _register_evaluator(self, evaluator_name, evaluator):
        self.evaluator_registry[evaluator_name] = evaluator
        
    #
    def create_evaluators(self):
        static_data = self.static_data_object.get_static_data()
        operation_mode = static_data['operation_mode']
        root_dir = \
            os.path.join(self.software_dir, os.path.join(operation_mode, 'query_lib/processor_lib'))
        log_text = root_dir
        self.logger_object.print_log(log_text)
        for root, dirs, files in os.walk(root_dir):
            relpath = '.' + os.path.relpath(root, root_dir) + '.'
            relpath = re.sub('\.+', '.', relpath)
            for file in files:
                filename, extension = os.path.splitext(os.path.basename(file))
                try:
                    import_cmd = 'from query_lib.processor_lib' + relpath + \
                                 filename + ' import Evaluator'
                    exec(import_cmd, globals())
                    evaluator = Evaluator(self.static_data_object,
                                          self.logger_object)
                    self._register_evaluator(filename, evaluator)
                    log_text = 'Registered Evaluator from ' + filename
                    self.logger_object.print_log(log_text)
                except Exception:
                    log_text = traceback.format_exc()
                    self.logger_object.print_exc(log_text)
    
    #
    def get_keys(self):
        return self.evaluator_registry.keys()
    
    #
    def push_directory(self, directory):
        self.software_dir = directory
    
    #
    def run_evaluator(self, evaluator, evaluation_manager, nlp_value, 
                      validation_value, display_flg):
        performance = \
            self.evaluator_registry[evaluator].evaluate(evaluation_manager, 
                                                        nlp_value,
                                                        validation_value,
                                                        display_flg)
        return performance
    
    #
    def run_evaluator_a(self, evaluator, evaluation_manager, nlp_value, 
                        validation_value, display_flg, value_range):
        performance = \
            self.evaluator_registry[evaluator].evaluate(evaluation_manager, 
                                                        nlp_value,
                                                        validation_value,
                                                        display_flg,
                                                        value_range)
        return performance