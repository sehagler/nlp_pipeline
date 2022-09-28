# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 12:12:23 2018

@author: haglers
"""

#
import os
import traceback

#
from tool_lib.py.processing_tools_lib.file_processing_tools \
    import read_json_file, write_file

#
class Metadata_manager(object):
    
    #
    def __init__(self, static_data_manager):
        self.static_data = static_data_manager.get_static_data()
        directory_manager = self.static_data['directory_manager']
        
        json_structure_manager = self.static_data['json_structure_manager']
        self.document_wrapper_key = \
            json_structure_manager.pull_key('document_wrapper_key')
        self.documents_wrapper_key = \
            json_structure_manager.pull_key('documents_wrapper_key')
        self.metadata_key = \
            json_structure_manager.pull_key('metadata_key')
        self.nlp_data_key = \
            json_structure_manager.pull_key('nlp_data_key')
        self.nlp_datetime_key = \
            json_structure_manager.pull_key('nlp_datetime_key')
        self.nlp_datum_key = \
            json_structure_manager.pull_key('nlp_datum_key')
        self.nlp_metadata_key = \
            json_structure_manager.pull_key('nlp_metadata_key')
        self.nlp_performance_key = \
            json_structure_manager.pull_key('nlp_performance_key')
        self.nlp_query_key = \
            json_structure_manager.pull_key('nlp_query_key')
        self.nlp_section_key = \
            json_structure_manager.pull_key('nlp_section_key')
        self.nlp_specimen_key = \
            json_structure_manager.pull_key('nlp_specimen_key')
        self.nlp_source_text_key = \
            json_structure_manager.pull_key('nlp_source_text_key')
        self.nlp_text_element_key = \
            json_structure_manager.pull_key('nlp_text_element_key')
        self.nlp_text_key = \
            json_structure_manager.pull_key('nlp_text_key')
        self.nlp_value_key = \
            json_structure_manager.pull_key('nlp_value_key')
            
        # to be moved to appropriate location
        self.manual_review = \
            json_structure_manager.pull_key('manual_review')
        #
    
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
        for id_key in self.static_data['document_identifiers']:
            if id_key in source_metadata_dict.keys():
                try:
                    source_metadata_dict['SOURCE_SYSTEM_DOCUMENT_ID'] = \
                        str(int(float(source_metadata_dict[id_key])))
                except Exception:
                    traceback.print_exc()
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