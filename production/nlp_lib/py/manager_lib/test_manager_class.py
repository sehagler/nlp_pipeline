# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 09:39:27 2020

@author: haglers
"""

#
from distutils.dir_util import copy_tree
import getpass
from jsondiff import diff
import os
import shutil

#
from nlp_lib.py.manager_lib.directory_manager_class import Directory_manager
from nlp_lib.py.tool_lib.processing_tools_lib.file_processing_tools import read_json_file, xml_diff

#
class Test_manager(object):
    
    #
    def __init__(self, project_manager_development, project_manager_production):
        self.project_data_development = project_manager_development.get_project_data()
        self.directory_manager_development = self.project_data_development['directory_manager']
        self.project_data_production = project_manager_production.get_project_data()
        self.directory_manager_production = self.project_data_production['directory_manager']
        
    #
    def compare_postprocessor_output(self):
        development_dir = self.directory_manager_development.pull_directory('postprocessing_data_out')
        production_dir = self.directory_manager_production.pull_directory('postprocessing_data_out')
        filenames = sorted(list(set(os.listdir(development_dir)) | set(os.listdir(production_dir))))
        error_ctr = 0
        file_ctr = len(filenames)
        for filename in filenames:
            file0 = os.path.join(development_dir, filename)
            file1 = os.path.join(production_dir, filename)
            if os.path.exists(file0):
                json0 = read_json_file(file0)
            else:
                print(file0 + ' does not exist')
            if os.path.exists(file1):
                json1 = read_json_file(file1)
            else:
                print(file1 + ' does not exist')
            if os.path.exists(file0) and os.path.exists(file1):
                diff_output = diff(json0, json1)
                if len(diff_output) > 0:
                    error_flg = True
                    if len(diff_output) == 1:
                        if 'SYSTEM_INFO' in diff_output.keys():
                            error_flg = False
                        elif 'NLP_PROCESS' in diff_output.keys():
                            error_flg = False
                    if len(diff_output) == 2:
                        if 'SYSTEM_INFO' in diff_output.keys() and 'NLP_PROCESS' in diff_output.keys():
                            error_flg = False
                    if error_flg:
                        error_ctr += 1
                        print('\n')
                        print(filename)
                        print('\n')
                        print(diff_output)
                        print('\n')
        print(error_ctr / file_ctr)
    
    #
    def compare_preprocessor_output(self):
        development_dir = self.directory_manager_development.pull_directory('preprocessing_data_out')
        production_dir = self.directory_manager_production.pull_directory('preprocessing_data_out')
        filenames = sorted(list(set(os.listdir(development_dir)) | set(os.listdir(production_dir))))
        error_ctr = 0
        file_ctr = len(filenames)
        for filename in filenames:
            file0 = os.path.join(development_dir, filename)
            file1 = os.path.join(production_dir, filename)
            if not os.path.exists(file0):
                print(file0 + ' does not exist')
            if not os.path.exists(file1):
                print(file1 + ' does not exist')
            if os.path.exists(file0) and os.path.exists(file1):
                diff_output = xml_diff(file0, file1)
                if len(diff_output) > 0:
                    error_ctr += 1
                    print(filename)
        print(error_ctr / file_ctr)