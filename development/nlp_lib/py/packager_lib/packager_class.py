# -*- coding: utf-8 -*-
"""
Created on Mon Mar 04 12:29:38 2019

@author: haglers
"""

#
import os

#
from nlp_lib.py.base_class_lib.packager_base_class import Packager_base
from nlp_lib.py.manager_lib.directory_manager_class import Directory_manager
from nlp_lib.py.tool_lib.processing_tools_lib.file_processing_tools \
    import read_json_file

#
class Packager(Packager_base):
    
    #
    def __init__(self, project_data):
        Packager_base.__init__(self, project_data)
        self.directory_manager = project_data['directory_manager']
        self.load_dir = self.directory_manager.pull_directory('postprocessing_data_out')
        self.project_name = project_data['project_name']
        self._create_data_json()
        self._save_data_json()
    
    #
    def _create_data_json(self):
        self.data = {}
        for filename in os.listdir(self.load_dir):
            key = filename[0:-5]
            self.data[key] = read_json_file(os.path.join(self.load_dir, filename))
        