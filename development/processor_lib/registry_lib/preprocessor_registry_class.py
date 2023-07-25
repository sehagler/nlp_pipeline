# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 08:12:07 2018

@author: haglers
"""

#
import os
import re
import traceback

#
class Preprocessor_registry(object):
    
    #
    def __init__(self, static_data_object, logger_object):
        self.static_data_object = static_data_object
        self.logger_object = logger_object
        self.preprocessor_registry = {}
    
    #
    def _register_preprocessor(self, preprocessor_name, preprocessor):
        self.preprocessor_registry[preprocessor_name] = preprocessor
    
    #
    def create_preprocessors(self):
        static_data = self.static_data_object.get_static_data()
        directory_object = static_data['directory_object']
        operation_mode = static_data['operation_mode']
        software_dir = directory_object.pull_directory('software_dir')
        root_dir = \
            os.path.join(software_dir, os.path.join(operation_mode, 'query_lib/processor_lib'))
        log_text = root_dir
        self.logger_object.print_log(log_text)
        for root, dirs, files in os.walk(root_dir):
            relpath = '.' + os.path.relpath(root, root_dir) + '.'
            relpath = re.sub('\.+', '.', relpath)
            for file in files:
                filename, extension = os.path.splitext(os.path.basename(file))
                try:
                    import_cmd = 'from query_lib.processor_lib' + relpath + \
                                 filename + ' import Preprocessor'
                    exec(import_cmd, globals())
                    self._register_preprocessor(filename, Preprocessor())
                    log_text = 'Registered Preprocessor from ' + filename
                    self.logger_object.print_log(log_text)
                except Exception:
                    log_text = traceback.format_exc()
                    self.logger_object.print_exc(log_text)
                    
    #
    def push_text_normalization_object(self, text_normalization_object):
        self._register_preprocessor('text_normalization_object',
                                    text_normalization_object)
                    
    #
    def run_registry(self, dynamic_data_manager, text, source_system):
        dynamic_data_manager, raw_text, rpt_text = \
            self.preprocessor_registry['text_normalization_object'].run_preprocessor(dynamic_data_manager,
                                                                                     text,
                                                                                     source_system)
        for key in self.preprocessor_registry.keys():
            if key != 'text_normalization_object':
                rpt_text = \
                    self.preprocessor_registry[key].run_preprocessor(rpt_text)
        return dynamic_data_manager, raw_text, rpt_text