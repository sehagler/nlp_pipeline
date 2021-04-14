# -*- coding: utf-8 -*-
"""
Created on Mon Mar 04 12:29:38 2019

@author: haglers
"""

#
import os

#
#from nlp_lib.py.packaging_lib.base_class_lib.packager_base_class import \
#    Packager_base
from nlp_lib.py.tool_lib.processing_tools_lib.file_processing_tools \
    import read_json_file, write_json_file

#
class Packaging_manager(object):
    
    #
    def __init__(self, static_data_manager):
        self.static_data = static_data_manager.get_project_data()
        project_data = self.static_data
        
        self.project_data = project_data
        self.directory_manager = project_data['directory_manager']
        json_structure_manager = project_data['json_structure_manager']
        self.project_name = project_data['project_name']
        self.save_dir = self.directory_manager.pull_directory('processing_data_dir')
        
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
        self.multiple_specimens = \
            json_structure_manager.pull_key('multiple_specimens')
        self.multiple_values = \
            json_structure_manager.pull_key('multiple_values')
        #
        
        self.directory_manager = self.static_data['directory_manager']
    
    #
    def _create_data_json(self, load_dir):
        self.data = {}
        for filename in os.listdir(load_dir):
            key = filename[0:-5]
            self.data[key] = \
                read_json_file(os.path.join(load_dir, filename))
                
    # 
    def _load_data_json(self, project_data):
        project_name = project_data['project_name']
        directory_manager = project_data['directory_manager']
        data_dir = directory_manager.pull_directory('processing_data_dir')
        nlp_data = \
            read_json_file(os.path.join(data_dir, project_name + '.json'))
        return nlp_data
    #
                
    #
    def _write_data_json(self):
        documents = []
        for key_0 in self.data.keys():
            document_in = self.data[key_0]
            document = {}
            for key_1 in document_in.keys():
                if key_1 != 'RAW_TEXT':
                    if key_1 not in [self.nlp_data_key, 'PREPROCESSED_TEXT']:
                        document[key_1] = document_in[key_1]
                    elif key_1 == 'PREPROCESSED_TEXT':
                        document[self.nlp_source_text_key] = document_in[key_1]
                    else:
                        data_in = document_in[key_1]
            data = []
            for key_1 in data_in:
                for key_2 in data_in[key_1]:
                    data.append({ self.nlp_datum_key : data_in[key_1][key_2] })
            document[self.nlp_data_key] = data
            document_wrapper = {}
            document_wrapper[self.document_wrapper_key] = document
            documents.append(document_wrapper)
        documents_wrapper = {}
        documents_wrapper[self.documents_wrapper_key] = documents
        write_json_file(os.path.join(self.save_dir, self.project_name + '.json'),
                        documents_wrapper)
            
    #
    def create_data_json(self):
        load_dir = \
            self.directory_manager.pull_directory('postprocessing_data_out')
        self.project_name = self.static_data['project_name']
        self._create_data_json(load_dir)
        self._write_data_json()
        