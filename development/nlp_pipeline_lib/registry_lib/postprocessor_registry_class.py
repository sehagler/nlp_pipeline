# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 08:12:07 2018

@author: haglers
"""

#
import os

#
from base_lib.registry_base_class import Registry_base

#
class Postprocessor_registry(Registry_base):
    
    #
    def __init__(self, static_data_object, logger_object, metadata_manager):
        Registry_base.__init__(self, static_data_object, logger_object)
        self.Tool_name = 'Postprocessor_'
        self.tool_name = 'postprocessor_'

        self.data_dict_classes_list = []
        
    #
    def _get_import_cmds(self, filename):
        import_cmds = [ 'from query_lib.processor_lib.' + filename + \
                        '_tools import Postprocessor as Object' ]
        return import_cmds
        
    #
    def _push_data_dict(self, postprocessor_name, filename, data_dict,
                        sections_data_dict, document_list):
        self.registry_dict[postprocessor_name].push_data_dict(postprocessor_name,
                                                              filename,
                                                              data_dict, 
                                                              sections_data_dict,
                                                              document_list)

    #
    def pull_postprocessor_registry(self):
        return self.registry_dict
     
    #
    def push_data_dict(self, filename, data_dict, sections_data_dict,
                       document_list):
        filename_base, extension = os.path.splitext(filename)
        if extension == '.csv' and filename_base != 'sections':
            for key in self.registry_dict.keys():
                self._push_data_dict(key, filename_base, data_dict,
                                     sections_data_dict, document_list)
                
    #
    def push_raw_data_directory(self, directory):
        self.raw_data_dir = directory