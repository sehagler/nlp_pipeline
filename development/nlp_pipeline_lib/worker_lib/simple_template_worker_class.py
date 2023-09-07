# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 10:24:26 2023

@author: haglers
"""

#
from base_lib.worker_base_class import Worker_base

#
class Simple_template_worker(Worker_base):
    
    #
    def __init__(self, static_data_object, logger_object,
                 ohsu_nlp_template_object):
        Worker_base.__init__(self, static_data_object, logger_object)
        self.ohsu_nlp_template_object = ohsu_nlp_template_object
        
    #
    def _process_data(self, argument_dict):
        self.ohsu_nlp_template_object.clear_simple_template_output()
        self.ohsu_nlp_template_object.run_simple_template(argument_dict)
        template_output = \
            self.ohsu_nlp_template_object.pull_simple_template_output()
        return_dict = {}
        return_dict['template_output'] = template_output
        return return_dict