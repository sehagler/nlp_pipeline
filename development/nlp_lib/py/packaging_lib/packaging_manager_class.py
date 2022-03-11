# -*- coding: utf-8 -*-
"""
Created on Mon Mar 04 12:29:38 2019

@author: haglers
"""

#
import os
import re

#
from nlp_lib.py.file_lib.json_manager_class import Json_manager

#
class Packaging_manager(object):
    
    #
    def __init__(self, static_data_manager, json_manager_registry):
        self.static_data_manager = static_data_manager
        self.json_manager_registry = json_manager_registry
        self.static_data = self.static_data_manager.get_static_data()
        self.directory_manager = self.static_data['directory_manager']
        
    #
    def create_preperformance_test_data_json(self):
        static_data = self.static_data_manager.get_static_data()
        load_dir = \
            self.directory_manager.pull_directory('postprocessing_data_out')
        data = {}
        for filename in os.listdir(load_dir):
            json_file = Json_manager(self.static_data_manager,
                                     os.path.join(load_dir, filename))
            key = filename[0:-5]
            data[key] = json_file.read_json_file()
        filename = static_data['project_name'] + '/' + \
                   static_data['project_subdir'] + '/' + \
                   static_data['project_name'] + '.json'
        self.json_manager_registry[filename].write_performance_data_to_package_json_file(data)
        
    #
    def create_postperformance_production_data_json(self):
        static_data = self.static_data_manager.get_static_data()
        directory_manager = static_data['directory_manager']
        processing_base_dir = \
            directory_manager.pull_directory('processing_base_dir')
        performance_statistics_dict = {}
        for filename in static_data['performance_data_files']:
            file = os.path.join(processing_base_dir, filename)
            performance_statistics_dict_tmp = \
                self.json_manager_registry[filename].read_performance_data()
            for key in performance_statistics_dict_tmp.keys():
                performance_statistics_dict[key] = \
                    performance_statistics_dict_tmp[key]
        filename = static_data['project_name'] + '/' + \
                   static_data['project_subdir'] + '/' + \
                   static_data['project_name'] + '.json'
        self.json_manager_registry[filename].write_performance_data_1(performance_statistics_dict,
                                                                      True, True)
                          
    #
    def create_postperformance_test_data_json(self):
        static_data = self.static_data_manager.get_static_data()
        filename = static_data['project_name'] + '/test/' + \
                   static_data['project_name'] + '.performance.json'
        performance_statistics_dict = \
            self.json_manager_registry[filename].read_performance_data()
        filename = static_data['project_name'] + '/' + \
                   static_data['project_subdir'] + '/' + \
                   static_data['project_name'] + '.json'
        self.json_manager_registry[filename].write_performance_data_1(performance_statistics_dict,
                                                                      False, False)