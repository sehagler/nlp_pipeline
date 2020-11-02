# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 08:18:53 2019

@author: haglers
"""

#
class Linguamatics_i2e_file_manager(object):

    #
    def __init__(self, project_data):
        project_name = project_data['project_name']
        directory_manager = project_data['directory_manager']
        json_files_key_value = project_data['json_files_key_value']
        self.directory_manager = directory_manager
        source_data_filename = project_name + ".source_data.zip"
        keywords_filename = project_name + ".keywords.txt"
        query_bundle_filename = project_name + ".query_bundle.zip"
        regions_filename = project_name + ".regions"
        xmlconf_filename = project_name + ".xml.conf"
        self.bundles_dict = {}
        self.bundles_dict['query_bundle_file'] = \
            self.directory_manager.pull_directory('processing_data_dir') + '/' + query_bundle_filename
        self.i2e_resources_dict = {}
        self.i2e_resources_dict['index_template'] = "/api;type=index_template/" + project_name
        self.i2e_resources_dict['region_list'] = "/api;type=region_list/" + regions_filename
        self.i2e_resources_dict['source_data'] = "/api;type=source_data/" + project_name
        self.i2e_resources_dict['xml_and_html_config_file'] = \
            '/api;type=xml_and_html_config_file/' + xmlconf_filename
        self.keywords_filename = \
            self.directory_manager.pull_directory('processing_data_dir') + '/' + keywords_filename
        self.resource_files_dict = {}
        self.resource_files_dict['region_list'] = \
            self.directory_manager.pull_directory('processing_data_dir') + '/' + regions_filename
        self.resource_files_dict['source_data'] = \
            self.directory_manager.pull_directory('source_data') + '/' + source_data_filename
        self.resource_files_dict['xml_and_html_config_file'] = \
            self.directory_manager.pull_directory('processing_data_dir') + '/' + xmlconf_filename
        self.server_files_dict = {}
        self.server_files_dict['keywords'] = \
            '/opt/linguamatics/i2e/bin/healthcare_preprocessing/keywords_default.txt'
            
    #
    def bundle(self, key):
        return self.bundles_dict[key]
    
    #
    def bundles_keys(self):
        return self.bundles_dict.keys()
    
    #
    def i2e_resource(self, key):
        return self.i2e_resources_dict[key]
    
    #
    def keywords_file(self):
        return self.keywords_filename
    
    #
    def preprocessing_data_directory(self):
        return self.directory_manager.pull_directory('preprocessing_data_out')
    
    #
    def processing_data_directory(self):
        return self.directory_manager.pull_directory('processing_data_dir')
    
    #
    def queries_source_directory(self):
        return self.directory_manager.pull_directory('i2e_queries')
    
    #
    def resource_file(self, key):
        return self.resource_files_dict[key]
    
    #
    def resource_files_keys(self):
        return self.resource_files_dict.keys()
    
    #
    def server_file(self, key):
        return self.server_files_dict[key]
    
    #
    def source_data_directory(self):
        return self.directory_manager.pull_directory('source_data')