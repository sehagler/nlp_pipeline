# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 17:37:17 2022

@author: haglers
"""

#
from nlp_pipeline_lib.py.static_data_lib.static_data_manager_class \
    import Static_data_manager
from remote_lib.server_lib.server_manager_class import Server_manager

#
class Remote_manager_registry(object):
    
    #
    def __init__(self, static_data_manager, update_static_data_manager,
                 root_dir, password):
        self.remote_manager_registry = {}
        self._server_manager(static_data_manager, password)
        self._update_manager(static_data_manager, update_static_data_manager,
                             root_dir, password)
            
    #
    def _server_manager(self, static_data_manager, password):
        self.remote_manager_registry['server_manager'] = \
            Server_manager(static_data_manager, password)
            
    #
    def _update_manager(self, static_data_manager, update_static_data_manager,
                        root_dir, password):
        static_data = static_data_manager.get_static_data()
        user = static_data['user']
        self.remote_manager_registry['update_manager'] = \
            Server_manager(update_static_data_manager, password)
            
    #
    def get_manager(self, manager_name):
        return self.remote_manager_registry[manager_name]