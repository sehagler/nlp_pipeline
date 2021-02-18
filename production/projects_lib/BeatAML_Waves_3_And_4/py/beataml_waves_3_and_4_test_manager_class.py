# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 09:52:44 2020

@author: haglers
"""

#
from nlp_lib.py.manager_lib.test_manager_class import Test_manager
from projects_lib.BeatAML_Waves_3_And_4.py.beataml_waves_3_and_4_project_manager_class \
    import BeatAML_Waves_3_And_4_project_manager
from projects_lib.BeatAML_Waves_3_And_4.py.beataml_waves_3_and_4_validation_manager_class \
    import BeatAML_Waves_3_And_4_validation_manager

#
class BeatAML_Waves_3_And_4_test_manager(Test_manager):
    
    #
    def __init__(self, project_data, root_dir_flg):
        user = project_data['user']
        project_manager_development = BeatAML_Waves_3_And_4_project_manager('development', user, root_dir_flg)
        project_manager_production = BeatAML_Waves_3_And_4_project_manager('production', user, root_dir_flg)
        Test_manager.__init__(self, project_manager_development, project_manager_production)
    
    #
    def data_validation(self):
        #BeatAML_Waves_3_And_4_validation_manager(self.project_data_development)
        BeatAML_Waves_3_And_4_validation_manager(self.project_data_production)