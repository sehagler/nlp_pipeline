# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 10:24:26 2023

@author: haglers
"""

#
import os

#
from base_lib.worker_base_class import Worker_base
from nlp_pipeline_lib.manager_lib.file_lib.json_lib.json_manager_class \
    import Json_manager

#
class Simple_template_worker(Worker_base):
    
    #
    def __init__(self, static_data_object):
        Worker_base.__init__(self, static_data_object)
        
    #
    def _process_data(self, argument_dict):
        return_dict = argument_dict
        return return_dict