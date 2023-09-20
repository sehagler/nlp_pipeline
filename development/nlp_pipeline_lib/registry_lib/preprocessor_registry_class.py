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
from base_lib.registry_base_class import Registry_base

#
class Preprocessor_registry(Registry_base):
    
    #
    def __init__(self, static_data_object, logger_object):
        Registry_base.__init__(self, static_data_object, logger_object)
        self.Tool_name = 'Preprocessor_'
        self.tool_name = 'preprocessor_'
        
    #
    def _get_import_cmds(self, filename):
        import_cmds = [ 'from query_lib.processor_lib.' + filename + \
                        ' import Preprocessor as Object',
                        'from query_lib.processor_lib.base_lib.' + filename + \
                        ' import Preprocessor as Object' ]
        return import_cmds
    
    #
    def push_text_normalization_object(self, text_normalization_object):
        self._register_object('text_normalization_object',
                               text_normalization_object)
    
    #
    def run_registry(self, dynamic_data_manager, text, source_system):
        dynamic_data_manager, raw_text, rpt_text = \
            self.registry_dict['text_normalization_object'].run_object(dynamic_data_manager,
                                                                       text,
                                                                       source_system)
        for key in self.registry_dict.keys():
            if key != 'text_normalization_object':
                rpt_text = \
                    self.registry_dict[key].run_object(rpt_text)
        return dynamic_data_manager, raw_text, rpt_text