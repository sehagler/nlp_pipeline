# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 17:37:17 2022

@author: haglers
"""

#
from remote_lib.manager_lib.server_lib.server_manager_class import Server_manager

#
class Remote_registry(object):
    
    #
    def __init__(self, static_data_object, update_static_data_object,
                 logger_object, root_dir, password):
        self.remote_manager_registry = {}
        self._server_manager(static_data_object, logger_object, password)
        self._update_manager(static_data_object, update_static_data_object,
                             logger_object, root_dir, password)
            
    #
    def _server_manager(self, static_data_object, logger_object, password):
        self.remote_manager_registry['server_manager'] = \
            Server_manager(static_data_object, logger_object, password)
            
    #
    def _update_manager(self, static_data_object, update_static_data_object,
                        logger_object, root_dir, password):
        static_data = static_data_object.get_static_data()
        user = static_data['user']
        self.remote_manager_registry['update_manager'] = \
            Server_manager(update_static_data_object, logger_object, password)
            
    #
    def get_manager(self, manager_name):
        return self.remote_manager_registry[manager_name]