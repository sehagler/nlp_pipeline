# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 08:18:53 2019

@author: haglers
"""

#
import os

#
class Linguamatics_i2e_file_manager(object):

    #
    def __init__(self, project_name, user):
        self.i2e_files_dict = {}
        self.i2e_files_dict['query_bundle'] = project_name + ".query_bundle.zip"
        self.i2e_files_dict['regions'] = project_name + ".regions"
        self.i2e_files_dict['source_data'] = project_name + ".source_data.zip"
        self.i2e_files_dict['xmlconf'] = project_name + ".xml.conf"
        self.i2e_resources_dict = {}
        self.i2e_resources_dict['index_template'] = \
            "/api;type=index_template/" + project_name
        self.i2e_resources_dict['region_list'] = \
            "/api;type=region_list/" + self.i2e_files_dict['regions']
        self.i2e_resources_dict['source_data'] = \
            "/api;type=source_data/" + project_name
        self.i2e_resources_dict['xml_and_html_config_file'] = \
            '/api;type=xml_and_html_config_file/' + self.i2e_files_dict['xmlconf']
        self.query_bundle_path = \
            '/Repository/Saved Queries/__private__/' + user + '/'
        self.server_files_dict = {}
        self.server_files_dict['keywords'] = \
            '/opt/linguamatics/i2e/bin/healthcare_preprocessing/keywords_default.txt'
            
    #
    def bundle(self, key):
        return self.bundles_dict[key]
    
    #
    def filename(self, key):
        return self.i2e_files_dict[key]
    
    #
    def i2e_resource(self, key):
        return self.i2e_resources_dict[key]
    
    #
    def query_bundle_filename(self):
        return self.i2e_files_dict['query_bundle']
    
    #
    def query_bundle_path_base(self):
        return self.query_bundle_path
    
    #
    def regions_filename(self):
        return self.i2e_files_dict['regions']
    
    #
    def server_file(self, key):
        return self.server_files_dict[key]
    
    #
    def source_data_filename(self):
        return self.i2e_files_dict['source_data']
    
    #
    def xmlconf_filename(self):
        return self.i2e_files_dict['xmlconf']