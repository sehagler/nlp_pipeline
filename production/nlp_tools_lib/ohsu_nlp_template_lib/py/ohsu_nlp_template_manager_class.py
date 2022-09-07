# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 09:40:02 2022

@author: haglers
"""

#
from nlp_tools_lib.ohsu_nlp_template_lib.py.AB_fields_manager_class \
    import AB_fields_manager
from nlp_tools_lib.ohsu_nlp_template_lib.py.simple_template_manager_class \
    import Simple_template_manager

#
class Ohsu_nlp_template_manager(object):
    
    #
    def __init__(self, static_data_manager):
        self.ab_fields_manager = AB_fields_manager(static_data_manager)
        self.simple_template_manager = Simple_template_manager()
    
    #
    def clear_simple_template_output(self):
        self.simple_template_manager.clear_template_output()
    
    #
    def run_simple_template(self, template_manager, text_dict):
        self.simple_template_manager.run_template(template_manager, text_dict)
            
    #
    def train_ab_fields(self, template_manager, metadata_manager, data_dir,
                        text_dict):
        self.ab_fields_manager.train_template(template_manager, 
                                              metadata_manager, data_dir,
                                              text_dict)
        
    #
    def write_ab_fields(self, template_outlines_dir, filename):
        self.ab_fields_manager.write_ab_fields(template_outlines_dir, filename)

    #
    def write_simple_template_output(self, template_manager, data_dir, filename):
        self.simple_template_manager.write_template_output(template_manager, data_dir, filename)