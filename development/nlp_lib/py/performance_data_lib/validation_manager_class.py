# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 16:29:37 2021

@author: haglers
"""

#
from nlp_lib.py.base_class_lib.packager_base_class import Packager_base
from nlp_lib.py.logger_lib.logger_class import Logger
from nlp_lib.py.tool_lib.processing_tools_lib.file_processing_tools \
    import read_json_file
    
#
class Validation_manager(Packager_base):
    
    #
    def __init__(self, project_data):
        Packager_base.__init__(self, project_data)
        self.directory_manager = project_data['directory_manager']
        self.log_dir = self.directory_manager.pull_directory('log_dir')
        self.logger = Logger(self.log_dir)
        self.project_data = project_data
        
    #
    def read_nlp_data(self):
        self.nlp_data = self._read_nlp_data(self.project_data)