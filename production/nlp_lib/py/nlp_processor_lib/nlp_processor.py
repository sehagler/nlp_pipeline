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
    def fix_linguamatics_i2e_queries(self):
        self.nlp_pipeline.fix_linguamatics_i2e_queries()
    
    #
    def generate_training_data_sets(self, password):
        self.nlp_pipeline.generate_training_data_sets(password)
    
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
    def pipeline_manager(self, server, root_dir, project_subdir, project_name,
                         password):
        if root_dir == 'server':
            if server == 'development':
                root_dir = 'dev_server'
            elif server == 'production':
                root_dir = 'prod_server'
        import_cmd = 'from projects_lib.' + project_name + '.py.' + \
                     project_name.lower() + \
                     '_static_data_manager_class import ' + project_name + \
                     '_static_data_manager as Static_data_manager'
        exec(import_cmd, globals())
        user = getpass.getuser()
        static_data_manager = Static_data_manager(server, project_subdir,
                                                  user, root_dir)
        static_data = static_data_manager.get_static_data()
        server_manager = Server_manager(static_data, password)
        self.nlp_pipeline = Pipeline_manager(static_data_manager,
                                             server_manager, root_dir,
                                             password)
        
    #
    def postqueries_postperformance(self):
        self.nlp_pipeline.postqueries_postperformance()
            
    #
    def postqueries_preperformance(self):
        self.nlp_pipeline.postqueries_preperformance()
    
    #
    def post_queries(self):
        self.nlp_pipeline.post_queries()
        
    #
    def prequeries(self, password):
        self.nlp_pipeline.prequeries(password)
        
    #
    def software_manager(self, password, root_dir_flg):
        self.root_dir_flg = root_dir_flg
        user = getpass.getuser()
        static_data_manager = \
            Static_data_manager('development', None, None, user, root_dir_flg)
        static_data = static_data_manager.get_static_data()
        server_manager = Server_manager(static_data, password)
        self.nlp_software = Software_manager(static_data_manager,
                                             server_manager)