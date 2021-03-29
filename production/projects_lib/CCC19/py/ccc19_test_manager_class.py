# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 09:55:47 2020

@author: haglers
"""

#
from nlp_lib.py.manager_lib.test_manager_class import Test_manager
from projects_lib.CCC19.py.ccc19_project_manager_class import CCC19_project_manager
from projects_lib.CCC19.py.ccc19_validation_manager_class import CCC19_validation_manager

#
class CCC19_test_manager(Test_manager):
    
    #
    def __init__(self, project_data, root_dir_flg):
        project_subdir = project_data['project_subdir']
        user = project_data['user']
        project_manager_development = CCC19_project_manager('development', project_subdir, user, root_dir_flg)
        project_manager_production = CCC19_project_manager('production', project_subdir, user, root_dir_flg)
        Test_manager.__init__(self, project_manager_development, project_manager_production)
        
    #
    def calculate_performance(self):
        #CCC19_validation_manager(self.project_data_development)
        CCC19_validation_manager(self.project_data_production)