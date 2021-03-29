# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 08:12:07 2018

@author: haglers
"""

#
from nlp_lib.py.manager_lib.output_manager_class import Output_manager

#
class Postprocessor(object):
    
    #
    def __init__(self, project_data, metadata_manager):
        self.output_manager = Output_manager(project_data, metadata_manager)
        self.data_dict_classes_list = []
        
    #
    def _business_rules(self, text_label):
        data_key_map = {}
        data_value_map = {}
        data_key_map['EXTRACTED_TEXT'] = text_label
        return data_key_map, data_value_map
        
    #
    def _import_reports_body(self, linguamatics_i2e_file_manager):
        pass
    
    #
    def cleanup_json_files_dir(self):
        self.output_manager.cleanup_json_files_dir()

    #
    def create_json_files(self):
        self.output_manager.create_json_files()
        
    #
    def import_reports(self, project_data):
        self._import_reports_body(project_data)
        self.output_manager.merge_data_dict_lists()
        self.output_manager.include_metadata()
        self.output_manager.include_text()
        self.merged_dict_list = self.output_manager.get_data()
        
    #
    def set_data_dirs(self, project_data):
        directory_manager = project_data['directory_manager']
        self.output_manager.set_data_dirs(directory_manager)