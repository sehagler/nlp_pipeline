# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 17:37:17 2022

@author: haglers
"""

#
from nlp_tools_lib.linguamatics_i2e_lib.object_lib.linguamatics_i2e_object_class \
    import Linguamatics_i2e_object
from nlp_tools_lib.melax_clamp_lib.manager_lib.melax_clamp_manager_class \
    import Melax_clamp_manager
from nlp_tools_lib.ohsu_nlp_template_lib.manager_lib.ohsu_nlp_template_manager_class \
    import Ohsu_nlp_template_manager

#
class Nlp_tool_registry(object):
    
    #
    def __init__(self, static_data_object, directory_object,logger_object, 
                 remote_manager_registry, password):
        self.static_data_object = static_data_object
        self.nlp_tool_manager_registry = {}
        self._linguamatics_i2e_object(remote_manager_registry, password)
        self.nlp_tool_manager_registry['melax_clamp_manager'] = \
            Melax_clamp_manager(static_data_object, directory_object,
                                logger_object)
        self.nlp_tool_manager_registry['ohsu_nlp_template_manager'] = \
            Ohsu_nlp_template_manager(static_data_object, directory_object,
                                      logger_object)
            
    #
    def _linguamatics_i2e_object(self, remote_manager_registry, password):
        server_manager = remote_manager_registry.get_manager('server_manager')
        static_data = self.static_data_object.get_static_data()
        project_name = static_data['project_name']
        server = static_data['acc_server'][2]
        user = static_data['user']
        self.nlp_tool_manager_registry['linguamatics_i2e_object'] = \
            Linguamatics_i2e_object(server_manager, project_name, server,
                                    user, password)
            
    #
    def get_manager(self, manager_name):
        return self.nlp_tool_manager_registry[manager_name]