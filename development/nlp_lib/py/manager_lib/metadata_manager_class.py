# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 12:12:23 2018

@author: haglers
"""

#
import os

#
from nlp_lib.py.base_class_lib.packager_base_class import Packager_base
from nlp_lib.py.manager_lib.directory_manager_class import Directory_manager
from nlp_lib.py.tool_lib.processing_tools_lib.file_processing_tools import read_json_file, write_json_file

#
class Metadata_manager(Packager_base):
    
    #
    def __init__(self, project_data):
        directory_manager = project_data['directory_manager']
        Packager_base.__init__(self, project_data)
        self.metadata_json_file = \
            os.path.join(directory_manager.pull_directory('metadata_dir'), 'metadata.json')
        self.metadata_dict_dict = {}
        
    #
    def _sort_metadata_dict(self):
        metadata_dict_dict_tmp = self.metadata_dict_dict
        self.metadata_dict_dict = {}
        for key in sorted(metadata_dict_dict_tmp.keys()):
            self.metadata_dict_dict[key] = metadata_dict_dict_tmp[key]
        
    #
    def append_metadata_dicts(self, metadata_dict_key, source_metadata_dict, 
                             nlp_metadata_dict):
        self.metadata_dict_dict[metadata_dict_key] = {}
        self.metadata_dict_dict[metadata_dict_key][self.metadata_key] = \
            source_metadata_dict
        self.metadata_dict_dict[metadata_dict_key][self.nlp_metadata_key] = \
            nlp_metadata_dict
            
    #
    def append_nlp_metadata_value(self, label, value):
        for key in self.metadata_dict_dict.keys():
            self.metadata_dict_dict[key][self.nlp_metadata_key][label] = \
                value
            
    #
    def get_metadata_dict_dict(self):
        return self.metadata_dict_dict
    
    #
    def get_metadata_json_file(self):
        return self.metadata_json_file
    
    #
    def load_metadata(self):
        self.metadata_dict_dict = read_json_file(self.metadata_json_file)
        
    #
    def merge_copy(self, metadata_manager_copy):
        metadata_dict_dict_add = metadata_manager_copy.get_metadata_dict_dict()
        for key in metadata_dict_dict_add.keys():
            doc_idx = \
                metadata_dict_dict_add[key][self.nlp_metadata_key]['NLP_DOCUMENT_IDX']
            self.metadata_dict_dict[doc_idx] = metadata_dict_dict_add[key]
    
    #
    def read_metadata(self):
        self.load_metadata()
        metadata_keys = []
        for metadata_key in self.metadata_dict_dict.keys():
            for key in self.metadata_dict_dict[metadata_key].keys():
                if key not in metadata_keys:
                    metadata_keys.append(key)
        return self.metadata_dict_dict, metadata_keys
    
    #
    def save_metadata(self):
        self._sort_metadata_dict()
        write_json_file(self.metadata_json_file, self.metadata_dict_dict)