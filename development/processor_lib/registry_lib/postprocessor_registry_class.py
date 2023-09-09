# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 08:12:07 2018

@author: haglers
"""

#
import os
import traceback

#
class Postprocessor_registry(object):
    
    #
    def __init__(self, static_data_object, logger_object, metadata_manager):
        self.static_data_object = static_data_object
        self.logger_object = logger_object
        self.data_dict_classes_list = []
        self.postprocessor_registry = {}
        self._import_postprocessors(static_data_object)
        
    #
    def _import_postprocessors(self, static_data_object):
        log_text = '_import_postprocessors() not defined'
        self.logger_object.print_log(log_text)
        
    #
    def _push_data_dict(self, postprocessor_name, filename, data_dict,
                        sections_data_dict, document_list):
        self.postprocessor_registry[postprocessor_name].push_data_dict(postprocessor_name,
                                                                       filename,
                                                                       data_dict, 
                                                                       sections_data_dict,
                                                                       document_list)

    #
    def _register_postprocessor(self, postprocessor_name, postprocessor):
        self.postprocessor_registry[postprocessor_name] = postprocessor
                
    #
    def pull_postprocessor_registry(self):
        return self.postprocessor_registry
     
    #
    def push_data_dict(self, filename, data_dict, sections_data_dict,
                       document_list):
        filename_base, extension = os.path.splitext(filename)
        if extension == '.csv' and filename_base != 'sections':
            for key in self.postprocessor_registry.keys():
                self._push_data_dict(key, filename_base, data_dict,
                                     sections_data_dict, document_list)
                
    #
    def push_raw_data_directory(self, directory):
        self.raw_data_dir = directory
        
    #
    def register_item(self, file):
        filename, extension = os.path.splitext(file)
        import_cmd = 'from query_lib.processor_lib.' + filename + \
                     '_tools import Postprocessor'
        try:
            exec(import_cmd, globals())
            log_text = 'Postprocessor_' + filename + ' import succeeded'
            self.logger_object.print_log(log_text)
            postprocessor_imported_flg = True
        except Exception:
            log_text = 'Postprocessor_' + filename + ' import failed'
            self.logger_object.print_log(log_text)
            log_text = traceback.format_exc()
            self.logger_object.print_exc(log_text)
            postprocessor_imported_flg = False
        if postprocessor_imported_flg:
            try:
                self._register_postprocessor('postprocessor_' + filename,
                                             Postprocessor(self.static_data_object,
                                                           self.logger_object))
                log_text = filename + ' registration succeeded'
                self.logger_object.print_log(log_text)
            except Exception:
                log_text = traceback.format_exc()
                self.logger_object.print_exc(log_text)
                log_text = filename + ' registration failed'
                self.logger_object.print_log(log_text)
            
    #
    def run_registry(self):
        for key in self.postprocessor_registry.keys():
            self.postprocessor_registry[key].run_postprocessor()