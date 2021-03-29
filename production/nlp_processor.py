# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 09:52:09 2020

@author: haglers
"""

#
from workspace_lib.workspace_manager_class import Workspace_manager
from workspace_lib.pipeline_manager_class import Pipeline_manager

#
class Nlp_processor(object):
    
    #
    def __init__(self, password, operation_mode, project, project_subdir,
                 root_dir_flg):
        self.operation_mode = operation_mode
        self.project = project
        self.project_subdir = project_subdir
        self.root_dir_flg = root_dir_flg
        if self.root_dir_flg == 'server':
            if self.operation_mode == 'development':
                self.root_dir_flg = 'dev_server'
            elif self.operation_mode == 'production':
                self.root_dir_flg = 'prod_server'
        self.nlp_workspace = Workspace_manager(password, self.root_dir_flg)
        self.nlp_pipeline = \
            Pipeline_manager(password, self.operation_mode, self.project,
                             self.project_subdir, self.root_dir_flg)
        
    #
    def download_queries(self):
        self.nlp_pipeline.download_queries()
    
    #
    def generate_training_data_sets(self):
        self.nlp_pipeline.generate_training_data_sets()
    
    #
    def move_software(self):
        if self.root_dir_flg == 'X':
            dest_drive = 'Z'
        elif self.root_dir_flg == 'Z':
            dest_drive = 'X'
        else:
            print('bad root directory')
        self.nlp_workspace.copy_x_nlp_software_to_nlp_sandbox(dest_drive)
    
    #
    def post_queries(self):
        self.nlp_pipeline.post_queries()
        
    #
    def pre_queries(self, password):
        self.nlp_pipeline.pre_queries(password)
        
    #
    def calculate_performance(self):
        self.nlp_pipeline.calculate_performance()