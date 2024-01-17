# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 17:37:17 2022

@author: haglers
"""

#
from base_lib.registry_base_class import Registry_base
from nlp_tools_lib.linguamatics_i2e_lib.object_lib.linguamatics_i2e_object_class \
    import Linguamatics_i2e_object
from nlp_tools_lib.ohsu_nlp_template_lib.object_lib.ohsu_nlp_template_object_class \
    import Ohsu_nlp_template_object

#
class Nlp_tool_registry(Registry_base):
    
    #
    def __init__(self, static_data_object, logger_object, 
                 remote_manager_registry):
        Registry_base.__init__(self, static_data_object, logger_object)
        self.remote_manager_registry = remote_manager_registry
            
    #
    def _linguamatics_i2e_object(self, remote_manager_registry, password):
        server_manager = remote_manager_registry.pull_object('server_manager')
        static_data = self.static_data_object.get_static_data()
        project_name = static_data['project_name']
        server = static_data['acc_server'][2]
        user = static_data['user']
        self.registry_dict['linguamatics_i2e_object'] = \
            Linguamatics_i2e_object(server_manager, project_name, server,
                                    user, password)
            
    #
    def pull_manager(self, manager_name):
        return self.registry_dict[manager_name]
    
    #
    def push_linguamatics_i2e_common_queries_directory(self, directory):
        self.linguamatics_i2e_common_queries_dir = directory
        
    #
    def push_linguamatics_i2e_general_queries_directory(self, directory):
        self.linguamatics_i2e_general_queries_dir = directory
        
    #
    def push_linguamatics_i2e_project_queries_directory(self, directory):
        self.linguamatics_i2e_project_queries_dir = directory
    
    #
    def push_linguamatics_i2e_preprocessing_data_out_directory(self, directory):
        self.linguamatics_i2e_preprocessing_data_out_dir = directory
    
    #
    def push_processing_data_directory(self, directory):
        self.processing_data_dir = directory
        
    #
    def push_source_data_directory(self, directory):
        self.source_data_dir = directory
        
    #
    def register_linguamatics_i2e_object(self, password):
        self._linguamatics_i2e_object(self.remote_manager_registry, password)
        self.registry_dict['linguamatics_i2e_object'].push_linguamatics_i2e_common_queries_directory(self.linguamatics_i2e_common_queries_dir)
        self.registry_dict['linguamatics_i2e_object'].push_linguamatics_i2e_general_queries_directory(self.linguamatics_i2e_general_queries_dir)
        self.registry_dict['linguamatics_i2e_object'].push_linguamatics_i2e_preprocessing_data_out_directory(self.linguamatics_i2e_preprocessing_data_out_dir)
        self.registry_dict['linguamatics_i2e_object'].push_linguamatics_i2e_project_queries_directory(self.linguamatics_i2e_project_queries_dir)
        self.registry_dict['linguamatics_i2e_object'].push_processing_data_directory(self.processing_data_dir)
        self.registry_dict['linguamatics_i2e_object'].push_source_data_directory(self.source_data_dir)
        
    #
    def register_nlp_template_object(self):
        self.registry_dict['ohsu_nlp_template_object'] = \
            Ohsu_nlp_template_object(self.static_data_object)