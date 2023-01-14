# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 08:18:53 2019

@author: haglers
"""

#
class Linguamatics_i2e_file_manager(object):

    #
    def __init__(self, project_name, user):
        self.i2e_files_dict = {}
        if project_name is not None:
            self.i2e_files_dict['query_bundle'] = project_name + ".query_bundle.zip"
            self.i2e_files_dict['regions'] = project_name + ".regions"
            self.i2e_files_dict['source_data'] = project_name + ".source_data.zip"
            self.i2e_files_dict['xmlconf'] = project_name + ".xml.conf"
        else:
            self.i2e_files_dict['query_bundle'] = None
            self.i2e_files_dict['regions'] = None
            self.i2e_files_dict['source_data'] = None
            self.i2e_files_dict['xmlconf'] = None
        self.server_files_dict = {}
        self.server_files_dict['keywords'] = \
            '/opt/linguamatics/i2e/bin/python_preprocessing/i2e/preprocessors/healthcare/keywords_default.txt'
    
    #
    def filename(self, key):
        return self.i2e_files_dict[key]
    
    #
    def query_bundle_filename(self):
        return self.i2e_files_dict['query_bundle']
    
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