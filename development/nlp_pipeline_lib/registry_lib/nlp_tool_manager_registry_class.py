# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 17:37:17 2022

@author: haglers
"""

#
from nlp_tools_lib.linguamatics_i2e_lib.py.linguamatics_i2e_manager_class \
    import Linguamatics_i2e_manager
from nlp_tools_lib.melax_clamp_lib.py.melax_clamp_manager_class \
    import Melax_clamp_manager
from nlp_tools_lib.ohsu_nlp_template_lib.py.ohsu_nlp_template_manager_class \
    import Ohsu_nlp_template_manager

#
class Nlp_tool_manager_registry(object):
    
    #
    def __init__(self, static_data_manager, remote_manager_registry,
                 password):
        self.static_data_manager = static_data_manager
        self.nlp_tool_manager_registry = {}
        self._linguamatics_i2e_manager(remote_manager_registry, password)
        self.nlp_tool_manager_registry['melax_clamp_manager'] = \
            Melax_clamp_manager(static_data_manager)
        self.nlp_tool_manager_registry['ohsu_nlp_template_manager'] = \
            Ohsu_nlp_template_manager(static_data_manager)
            
    #
    def _linguamatics_i2e_manager(self, remote_manager_registry, password):
        server_manager = remote_manager_registry.get_manager('server_manager')
        static_data = self.static_data_manager.get_static_data()
        linguamatics_i2e_file_manager = \
            static_data['linguamatics_i2e_file_manager']
        project_name = static_data['project_name']
        server = static_data['acc_server'][2]
        user = static_data['user']
        self.nlp_tool_manager_registry['linguamatics_i2e_manager'] = \
            Linguamatics_i2e_manager(linguamatics_i2e_file_manager, 
                                     server_manager, project_name, server,
                                     user, password)
            
    #
    def get_manager(self, manager_name):
        return self.nlp_tool_manager_registry[manager_name]