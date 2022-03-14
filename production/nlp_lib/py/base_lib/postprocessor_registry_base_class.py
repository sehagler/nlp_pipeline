# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 08:12:07 2018

@author: haglers
"""

#
class Postprocessor_registry_base(object):
    
    #
    def __init__(self, static_data_manager, metadata_manager):
        self.static_data = static_data_manager.get_static_data()
        self.data_dict_classes_list = []
        self.postprocessor_registry = {}
        self._import_postprocessors(static_data_manager)
        
    #
    def _import_postprocessors(self, static_data_manager):
        print('_import_postprocessors() not defined')
        
    #
    def _push_data_dict(self, postprocessor_name, data_dict, idx=0, filename=None):
        if idx == 0:
            self.postprocessor_registry[postprocessor_name].push_data_dict(data_dict, 
                                                                           filename=filename)
        else:
            self.postprocessor_registry[postprocessor_name].push_data_dict(data_dict, 
                                                                           idx=idx)
    
    #
    def _register_postprocessor(self, postprocessor_name, postprocessor):
        self.postprocessor_registry[postprocessor_name] = postprocessor
    
    #
    def pull_postprocessor_registry(self):
        return self.postprocessor_registry
            
    #
    def run_registry(self):
        for key in self.postprocessor_registry.keys():
            self.postprocessor_registry[key].run_postprocessor()