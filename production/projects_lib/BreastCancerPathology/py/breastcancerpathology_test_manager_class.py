# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 09:55:47 2020

@author: haglers
"""

#
from nlp_lib.py.manager_lib.test_manager_class import Test_manager
from projects_lib.BreastCancerPathology.py.breastcancerpathology_project_manager_class \
    import BreastCancerPathology_project_manager

#
class BreastCancerPathology_test_manager(Test_manager):
    
    #
    def __init__(self, project_data, root_dir_flg):
        project_subdir = project_data['project_subdir']
        user = project_data['user']
        project_manager_development = \
            BreastCancerPathology_project_manager('development', project_subdir, user, root_dir_flg)
        project_manager_production = \
            BreastCancerPathology_project_manager('production', project_subdir, user, root_dir_flg)
        Test_manager.__init__(self, project_manager_development, project_manager_production)