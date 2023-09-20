# -*- coding: utf-8 -*-
"""
Created on Tue May  9 15:07:01 2023

@author: haglers
"""

#
import os

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