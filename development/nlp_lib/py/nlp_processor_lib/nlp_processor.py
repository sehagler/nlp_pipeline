# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 09:52:09 2020

@author: haglers
"""

#
import getpass

#
from nlp_lib.py.pipeline_lib.pipeline_manager_class import Pipeline_manager
from nlp_lib.py.server_lib.server_manager_class import Server_manager
from nlp_lib.py.software_lib.software_manager_class import Software_manager
from nlp_lib.py.static_data_lib.static_data_manager_class \
    import Static_data_manager

#
class Nlp_processor(object):
    
    #
    def __init__(self):
        pass
    
    #
    def calculate_performance(self):
        self.nlp_pipeline.calculate_performance()
        
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
        self.nlp_software.copy_x_nlp_software_to_nlp_sandbox(dest_drive)
        
    #
    def pipeline_manager(self, password, operation_mode, project_name,
                         project_subdir, root_dir_flg):
        if root_dir_flg == 'server':
            if operation_mode == 'development':
                root_dir_flg = 'dev_server'
            elif operation_mode == 'production':
                root_dir_flg = 'prod_server'
        import_cmd = 'from projects_lib.' + project_name + '.py.' + \
                     project_name.lower() + \
                     '_project_manager_class import ' + project_name + \
                     '_project_manager as Project_manager'
        exec(import_cmd, globals())
        user = getpass.getuser()
        static_data_manager = Project_manager(operation_mode, project_subdir,
                                              user, root_dir_flg)
        static_data = static_data_manager.get_project_data()
        server_manager = Server_manager(static_data, password)
        self.nlp_pipeline = Pipeline_manager(static_data_manager,
                                             server_manager, root_dir_flg,
                                             password) 
    
    #
    def post_queries(self):
        self.nlp_pipeline.post_queries()
        
    #
    def pre_queries(self, password):
        self.nlp_pipeline.pre_queries(password)
        
    #
    def software_manager(self, password, root_dir_flg):
        self.root_dir_flg = root_dir_flg
        user = getpass.getuser()
        static_data_manager = \
            Static_data_manager('development', None, None, user, root_dir_flg)
        static_data = static_data_manager.get_project_data()
        server_manager = Server_manager(static_data, password)
        self.nlp_software = Software_manager(static_data_manager,
                                             server_manager)