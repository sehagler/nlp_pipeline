# -*- coding: utf-8 -*-
"""
Created on Mon Mar 04 12:29:38 2019

@author: haglers
"""

#
from json import JSONEncoder
import os

#
from nlp_lib.py.manager_lib.directory_manager_class import Directory_manager
from nlp_lib.py.tool_lib.processing_tools_lib.file_processing_tools import read_json_file, write_json_file

#
class Packager(object):
    
    #
    def __init__(self, project_data):
        self.directory_manager = project_data['directory_manager']
        self.load_dir = self.directory_manager.pull_directory('postprocessing_data_out')
        self.save_dir = self.directory_manager.pull_directory('processing_data_dir')
        self.project_name = project_data['project_name']
        self._create_data_json()
        self._save_data_json()
    
    #
    def _create_data_json(self):
        self.data = {}
        for filename in os.listdir(self.load_dir):
            key = filename[0:-5]
            self.data[key] = read_json_file(os.path.join(self.load_dir, filename))
                
    #
    def _save_data_json(self):
        data = []
        data_json = {}
        for key in self.data.keys():
            data_wrapped = {}
            data_wrapped['RECORD_ID'] = self.data[key]
            data.append(data_wrapped)
        data_json['NLP_DATA'] = data
        write_json_file(os.path.join(self.save_dir, self.project_name + '.json'), data_json)
        