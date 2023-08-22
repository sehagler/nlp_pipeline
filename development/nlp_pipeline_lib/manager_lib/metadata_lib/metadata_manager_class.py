# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 12:12:23 2018

@author: haglers
"""

#
import os
import traceback

#
from base_lib.manager_base_class \
    import Manager_base
from tools_lib.processing_tools_lib.file_processing_tools \
    import read_json_file, write_file

#
class Metadata_manager(Manager_base):
    
    #
    def __init__(self, static_data_object, directory_object, logger_object):
        Manager_base.__init__(self, static_data_object, directory_object,
                              logger_object)
        self.clear_metadata()
        
    #
    def _sort_metadata_dict(self):
        metadata_dict_dict_tmp = self.metadata_dict_dict
        self.metadata_dict_dict = {}
        for key in sorted(metadata_dict_dict_tmp.keys()):
            self.metadata_dict_dict[key] = metadata_dict_dict_tmp[key]
        
    #
    def append_metadata_dicts(self, metadata_dict_key, source_metadata_dict, 
                              nlp_metadata_dict):
        static_data = self.static_data_object.get_static_data()
        for id_key in static_data['document_identifiers']:
            if id_key in source_metadata_dict.keys():
                try:
                    source_metadata_dict['SOURCE_SYSTEM_DOCUMENT_ID'] = \
                        str(int(float(source_metadata_dict[id_key])))
                except Exception:
                    #log_text = traceback.format_exc()
                    #self.logger_object.print_exc(log_text)
                    source_metadata_dict['SOURCE_SYSTEM_DOCUMENT_ID'] = \
                        source_metadata_dict[id_key]
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
    def clear_metadata(self):
        self.metadata_dict_dict = {}
    
    #
    def get_doc_idx_offset(self):
        if not bool(self.metadata_dict_dict):
            doc_idx_offset = 0
        else:
            doc_idxs = list(self.metadata_dict_dict.keys())
            doc_idxs = list(map(int, doc_idxs))
            doc_idx_offset = max(doc_idxs) + 1
        return doc_idx_offset
            
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
    def pull_document_identifier_list(self, document_identifier_key):
        self.load_metadata()
        document_identifier_list = []
        for key in self.metadata_dict_dict.keys():
            document = self.metadata_dict_dict[key]
            document_identifier_list.append(document['METADATA'][document_identifier_key])
        document_identifier_list = sorted(list(set(document_identifier_list)))
        return document_identifier_list
    
    #
    def push_directory(self, directory):
        self.metadata_json_file = \
            os.path.join(directory, 'metadata.json')
    
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
        write_file(self.metadata_json_file, self.metadata_dict_dict,
                        False, False)