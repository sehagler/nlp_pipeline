# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 09:55:47 2020

@author: haglers
"""

#
from nlp_lib.py.manager_lib.test_manager_class import Test_manager
from projects_lib.AdverseEvents.py.adverseevents_project_manager_class \
    import AdverseEvents_project_manager

#
class AdverseEvents_test_manager(Test_manager):
    
    #
    def __init__(self, project_data, root_dir_flg):
        user = project_data['user']
        project_manager_development = AdverseEvents_project_manager('development', user, root_dir_flg)
        project_manager_production = AdverseEvents_project_manager('production', user, root_dir_flg)
        Test_manager.__init__(self, project_manager_development, project_manager_production)