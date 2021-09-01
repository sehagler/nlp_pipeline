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
    def __init__(self, static_data_manager, performance_json_manager,
                 project_json_manager):
        self.static_data_manager = static_data_manager
        self.performance_json_manager = performance_json_manager
        self.project_json_manager = project_json_manager
        self.static_data = self.static_data_manager.get_static_data()
        self.directory_manager = self.static_data['directory_manager']
        
    #
    def create_preperformance_test_data_json(self):
        load_dir = \
            self.directory_manager.pull_directory('postprocessing_data_out')
        data = {}
        for filename in os.listdir(load_dir):
            json_file = Json_manager(self.static_data_manager,
                                     os.path.join(load_dir, filename))
            key = filename[0:-5]
            data[key] = json_file.read_json_file()
        self.project_json_manager.write_performance_data_to_package_json_file(data)
        
    #
    def create_postperformance_production_data_json(self):
        performance_statistics_dict = \
            self.performance_json_manager.read_performance_data()
        self.project_json_manager.write_performance_data_0(performance_statistics_dict,
                                                           True, True)
                          
    #
    def create_postperformance_test_data_json(self):
        performance_statistics_dict = \
            self.performance_json_manager.read_performance_data()
        self.project_json_manager.write_performance_data_1(performance_statistics_dict,
                                                           False, False)