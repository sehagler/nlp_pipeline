# -*- coding: utf-8 -*-
"""
Created on Tue May  9 15:07:01 2023

@author: haglers
"""

#
import os
import traceback

#
from base_lib.manager_base_class import Manager_base

#
class Evaluator_registry(Manager_base):
    
    #
    def __init__(self, static_data_object, logger_object):
        Manager_base.__init__(self, static_data_object, logger_object)
        self.evaluator_registry = {}
    
    #
    def _register_evaluator(self, evaluator_name, evaluator):
        self.evaluator_registry[evaluator_name] = evaluator
    
    #
    def get_keys(self):
        return self.evaluator_registry.keys()
    
    #
    def push_software_directory(self, directory):
        self.software_dir = directory
        
    #
    def register_item(self, file, import_cmd):
        filename, extension = os.path.splitext(os.path.basename(file))
        try:
            exec(import_cmd, globals())
            log_text = 'Evaluator_' + filename + ' import succeeded'
            self.logger_object.print_log(log_text)
            evaluator_imported_flg = True
        except Exception:
            log_text = 'Evaluator_' + filename + ' import failed'
            self.logger_object.print_log(log_text)
            log_text = traceback.format_exc()
            self.logger_object.print_exc(log_text)
            evaluator_imported_flg = False
        if evaluator_imported_flg:
            try:
                self._register_evaluator('evaluator_' + filename,
                                         Evaluator(self.static_data_object,
                                                   self.logger_object))
                log_text = filename + ' registration succeeded'
                self.logger_object.print_log(log_text)
            except Exception:
                log_text = traceback.format_exc()
                self.logger_object.print_exc(log_text)
                log_text = filename + ' registration failed'
                self.logger_object.print_log(log_text)
        
    #
    def register_items(self):
        static_data = self.static_data_object.get_static_data()
        operation_mode = static_data['operation_mode']
        root_dir = \
            os.path.join(self.software_dir, os.path.join(operation_mode, 'query_lib/processor_lib'))
        log_text = root_dir
        self.logger_object.print_log(log_text)
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                filename, extension = os.path.splitext(os.path.basename(file))
                import_cmd = 'from query_lib.processor_lib.' + filename + \
                             ' import Evaluator'
                self.register_item(file, import_cmd)
                filename, extension = os.path.splitext(os.path.basename(file))
                import_cmd = 'from query_lib.processor_lib.base_lib.' + filename + \
                             ' import Evaluator'
                self.register_item(file, import_cmd)
    
    #
    def run_evaluator(self, evaluator, evaluation_manager, nlp_value, 
                      validation_value, display_flg):
        performance = \
            self.evaluator_registry['evaluator_' + evaluator].evaluate(evaluation_manager, 
                                                                       nlp_value,
                                                                       validation_value,
                                                                       display_flg)
        return performance
    
    #
    def run_evaluator_a(self, evaluator, evaluation_manager, nlp_value, 
                        validation_value, display_flg, value_range):
        performance = \
            self.evaluator_registry['evaluator_' + evaluator].evaluate(evaluation_manager, 
                                                                       nlp_value,
                                                                       validation_value,
                                                                       display_flg,
                                                                       value_range)
        return performance