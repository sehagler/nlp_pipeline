# -*- coding: utf-8 -*-
"""
Created on Mon Mar 04 12:29:38 2019

@author: haglers
"""

#
from nlp_lib.py.managers_lib.directory_manager_class import Directory_manager
from project_lib.specimens_base_class import Specimens_base
from projects_lib.BeatAML_Waves_1_And_2.py.beataml_waves_1_and_2_specimens_class \
    import BeatAML_Waves_1_And_2_specimens

#
class Specimens(Specimens_base):
    
    #
    def __init__(self, project_data):
        self.directory_manager = project_data['directory_manager']
        self.data_dir = self.directory_manager.directory('postprocessing_data_out')
        self.packaging_dir = self.directory_manager.directory('packaging_dir')
        self.project_name = project_data['project_name']
        self._get_data()
    
    #
    def _get_data(self):
        validation_object = Beataml_packager(self.data_dir, self.packaging_dir, self.directory_manager)
        validation_object.generate_json_file(self.packaging_dir, self.project_name + '.json')
        self.validation_data = validation_object.get_data_json()