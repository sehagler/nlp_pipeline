# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 17:29:08 2023

@author: haglers
"""

#
import os
import traceback

#
from base_lib.manager_base_class import Manager_base

#
class Registry_base(Manager_base):
    
    #
    def __init__(self, static_data_object, logger_object):
        Manager_base.__init__(self, static_data_object, logger_object)
        self.registry_dict = {}
        
    #
    def _register_object(self, object_name, object):
        self.registry_dict[object_name] = object
        
    #
    def get_keys(self):
        return self.registry_dict.keys()
    
    #
    def pull_object(self, object_name):
        return self.registry_dict[object_name]
        
    #
    def register_object(self, file):
        filename, extension = os.path.splitext(file)
        import_cmds = self._get_import_cmds(filename)
        stop_flg = False
        for i in range(len(import_cmds)):
            if not stop_flg:
                import_cmd = import_cmds[i]
                try:
                    exec(import_cmd, globals())
                    log_text = self.Tool_name + filename + ' import succeeded'
                    self.logger_object.print_log(log_text)
                    object_imported_flg = True
                    stop_flg = True
                except Exception:
                    log_text = self.Tool_name + filename + ' import failed'
                    self.logger_object.print_log(log_text)
                    log_text = traceback.format_exc()
                    self.logger_object.print_exc(log_text)
                    object_imported_flg = False
                if object_imported_flg:
                    try:
                        self._register_object(self.tool_name + filename,
                                              Object(self.static_data_object,
                                                     self.logger_object))
                        log_text = filename + ' registration succeeded'
                        self.logger_object.print_log(log_text)
                    except Exception:
                        log_text = traceback.format_exc()
                        self.logger_object.print_exc(log_text)
                        log_text = filename + ' registration failed'
                        self.logger_object.print_log(log_text)
        
    #
    def run_registry(self):
        for key in self.registry_dict.keys():
            self.registry_dict[key].run_object()