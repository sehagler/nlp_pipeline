# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 08:12:07 2018

@author: haglers
"""

#
class Preprocessor_registry_base(object):
    
    #
    def __init__(self, static_data):
        self.static_data = static_data
        self.preprocessor_registry = {}
    
    #
    def _register_preprocessor(self, preprocessor_name, preprocessor):
        self.preprocessor_registry[preprocessor_name] = preprocessor
            
    #
    def run_registry(self, text):
        for key in self.preprocessor_registry.keys():
            self.preprocessor_registry[key].push_text(text)
            self.preprocessor_registry[key].run_preprocessor()
            text = self.preprocessor_registry[key].pull_text()
        return text