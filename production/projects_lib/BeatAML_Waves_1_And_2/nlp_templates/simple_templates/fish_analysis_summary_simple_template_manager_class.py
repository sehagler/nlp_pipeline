# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 17:18:08 2022

@author: haglers
"""

#
from base_lib.manager_base_class import Manager_base
from query_lib.processor_lib.fish_analysis_summary_tools \
    import simple_template as fish_analysis_summary_simple_template

#
class Fish_analysis_summary_simple_template_manager(Manager_base):
    
    #
    def __init__(self, static_data_object, logger_object):
        Manager_base.__init__(self, static_data_object, logger_object)
        
    #
    def simple_template(self):
        return fish_analysis_summary_simple_template()