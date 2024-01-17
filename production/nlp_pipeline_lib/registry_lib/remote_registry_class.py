# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 17:37:17 2022

@author: haglers
"""

#
from base_lib.registry_base_class import Registry_base
from remote_lib.manager_lib.server_lib.server_manager_class import Server_manager

#
class Remote_registry(Registry_base):
    
    #
    def register_server_manager(self, static_data_object, logger_object, password):
        self.registry_dict['server_manager'] = \
            Server_manager(static_data_object, logger_object, password)
            
    #
    def register_update_manager(self, static_data_object, update_static_data_object,
                        logger_object, root_dir, password):
        self.registry_dict['update_manager'] = \
            Server_manager(update_static_data_object, logger_object, password)