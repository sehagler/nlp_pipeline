# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 08:12:07 2018

@author: haglers
"""

#
import os
import re
import traceback

#
class Preprocessor_registry(object):
    
    #
    def __init__(self, static_data):
        self.static_data = static_data
        self.preprocessor_registry = {}
    
    #
    def _register_preprocessor(self, preprocessor_name, preprocessor):
        self.preprocessor_registry[preprocessor_name] = preprocessor
    
    #
    def create_preprocessors(self):
        directory_manager = self.static_data['directory_manager']
        operation_mode = self.static_data['operation_mode']
        software_dir = directory_manager.pull_directory('software_dir')
        root_dir = \
            os.path.join(software_dir, os.path.join(operation_mode, 'query_lib/processor_lib'))
        print(root_dir)
        for root, dirs, files in os.walk(root_dir):
            relpath = '.' + os.path.relpath(root, root_dir) + '.'
            relpath = re.sub('\.+', '.', relpath)
            for file in files:
                filename, extension = os.path.splitext(os.path.basename(file))
                try:
                    import_cmd = 'from query_lib.processor_lib' + relpath + \
                                 filename + ' import Preprocessor'
                    exec(import_cmd, globals())
                    self._register_preprocessor(filename, Preprocessor())
                    print('Registered Preprocessor from ' + filename)
                except Exception:
                    traceback.print_exc()
                    
    #
    def run_registry(self, text):
        for key in self.preprocessor_registry.keys():
            self.preprocessor_registry[key].push_text(text)
            self.preprocessor_registry[key].run_preprocessor()
            text = self.preprocessor_registry[key].pull_text()
        return text