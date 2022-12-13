# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 08:12:07 2018

@author: haglers
"""

#
from copy import deepcopy
import os

#
from projects_lib.BeatAML_Waves_3_And_4.py.diagnosis_reader_class \
    import Diagnosis_reader
from query_lib.processor_lib.specific_diagnosis_tools \
    import Postprocessor as Postprocessor_specific_diagnosis
from processor_lib.registry_lib.postprocessor_registry_class \
    import Postprocessor_registry

#
class BeatAML_Waves_3_And_4_postprocessor_registry(Postprocessor_registry):
    
    #
    def create_postprocessor(self, filename):
        Postprocessor_registry.create_postprocessor(self, filename)
        if filename in [ 'sections.csv' ]:
            self._register_postprocessor('postprocessor_specific_diagnosis',
                                         Postprocessor_specific_diagnosis(self.static_data_object))

    #
    def push_data_dict(self, filename, data_dict):
        static_data = self.static_data_object.get_static_data()
        directory_manager = static_data['directory_manager']
        diagnosis_reader = \
            Diagnosis_reader(os.path.join(directory_manager.pull_directory('raw_data_dir'),'diagnoses.xlsx'))
        Postprocessor_registry.push_data_dict(self, filename, data_dict)
        if filename in [ 'diagnosis.csv' ]:
            self.postprocessor_registry['postprocessor_diagnosis'].push_diagnosis_reader(diagnosis_reader)
        if filename in [ 'sections.csv' ]:
            data_dict_copy = deepcopy(data_dict)
            self._push_data_dict('postprocessor_specific_diagnosis', data_dict_copy, filename=filename)
            self.postprocessor_registry['postprocessor_specific_diagnosis'].push_diagnosis_reader(diagnosis_reader)