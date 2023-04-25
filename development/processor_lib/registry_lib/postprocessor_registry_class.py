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
    def __init__(self, static_data_object, metadata_manager):
        self.static_data_object = static_data_object
        self.data_dict_classes_list = []
        self.postprocessor_registry = {}
        self._import_postprocessors(static_data_object)
        
    #
    def _import_postprocessors(self, static_data_object):
        print('_import_postprocessors() not defined')
        
    #
    def _push_data_dict(self, postprocessor_name, filename, data_dict,
                        sections_data_dict):
        self.postprocessor_registry[postprocessor_name].push_data_dict(postprocessor_name,
                                                                       filename,
                                                                       data_dict, 
                                                                       sections_data_dict)

    #
    def _register_postprocessor(self, postprocessor_name, postprocessor):
        self.postprocessor_registry[postprocessor_name] = postprocessor
    
    #
    def create_postprocessor(self, file):
        filename, extension = os.path.splitext(file)
        import_cmd = 'from query_lib.processor_lib.' + filename + \
                     '_tools import Postprocessor'
        try:
            exec(import_cmd, globals())
            print('Postprocessor_' + filename + ' import succeeded')
            postprocessor_imported_flg = True
        except Exception:
            print('Postprocessor_' + filename + ' import failed')
            traceback.print_exc()
            postprocessor_imported_flg = False
        if postprocessor_imported_flg:
            try:
                self._register_postprocessor('postprocessor_' + filename,
                                             Postprocessor(self.static_data_object))
                print(filename + ' registration succeeded')
            except Exception:
                traceback.print_exc()
                print(filename + ' registration failed')
                
    #
    def pull_postprocessor_registry(self):
        return self.postprocessor_registry
     
    #
    def push_data_dict(self, filename, data_dict, sections_data_dict):
        filename_base, extension = os.path.splitext(filename)
        if extension == '.csv' and filename_base != 'sections':
            for key in self.postprocessor_registry.keys():
                self._push_data_dict(key, filename_base, data_dict,
                                     sections_data_dict)
            
    #
    def run_registry(self):
        for key in self.postprocessor_registry.keys():
            self.postprocessor_registry[key].run_postprocessor()