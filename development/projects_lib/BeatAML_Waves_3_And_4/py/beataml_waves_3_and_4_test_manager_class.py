# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 09:52:44 2020

@author: haglers
"""

#
from nlp_lib.py.performance_data_lib.performance_data_manager_class \
    import Performance_data_manager
from projects_lib.BeatAML_Waves_3_And_4.py.beataml_waves_3_and_4_project_manager_class \
    import BeatAML_Waves_3_And_4_project_manager
from projects_lib.BeatAML_Waves_3_And_4.py.beataml_waves_3_and_4_validation_manager_class \
    import BeatAML_Waves_3_And_4_validation_manager

#
class BeatAML_Waves_3_And_4_test_manager(Performance_data_manager):
    
    #
    def __init__(self, project_data, root_dir_flg):
        operation_mode = project_data['operation_mode']
        project_subdir = project_data['project_subdir']
        user = project_data['user']
        project_manager = \
            BeatAML_Waves_3_And_4_project_manager(operation_mode, project_subdir, user, root_dir_flg)
        Performance_data_manager.__init__(self, project_manager)
        self.validation_manager = \
            BeatAML_Waves_3_And_4_validation_manager(project_data)