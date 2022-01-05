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
from tool_lib.py.query_tools_lib.antigens_tools \
    import Postprocessor as Postprocessor_antigens
from tool_lib.py.query_tools_lib.date_tools \
    import Postprocessor as Postprocessor_date
from tool_lib.py.query_tools_lib.diagnosis_tools \
    import Postprocessor as Postprocessor_diagnosis
from tool_lib.py.query_tools_lib.fish_analysis_summary_tools \
    import Postprocessor as Postprocessor_fish_analysis_summary
from tool_lib.py.query_tools_lib.karyotype_tools \
    import Postprocessor as Postprocessor_karyotype
from tool_lib.py.query_tools_lib.specific_diagnosis_tools \
    import Postprocessor as Postprocessor_specific_diagnosis
from tool_lib.py.registry_lib.postprocessor_registry_class \
    import Postprocessor_registry

#
class BeatAML_Waves_3_And_4_postprocessor_registry(Postprocessor_registry):
    
    #
    def create_postprocessor(self, filename):
        Postprocessor_registry.create_postprocessor(self, filename)
        if filename in [ 'diagnosis.csv' ]:
            self._register_postprocessor('postprocessor_diagnosis',
                                         Postprocessor_diagnosis(self.static_data))
        if filename in [ 'sections.csv' ]:
            self._register_postprocessor('postprocessor_antigens',
                                         Postprocessor_antigens(self.static_data))
            self._register_postprocessor('postprocessor_fish_analysis_summary',
                                         Postprocessor_fish_analysis_summary(self.static_data))
            self._register_postprocessor('postprocessor_karyotype',
                                         Postprocessor_karyotype(self.static_data))
            self._register_postprocessor('postprocessor_specific_diagnosis',
                                         Postprocessor_specific_diagnosis(self.static_data))

    #
    def push_data_dict(self, filename, data_dict):
        directory_manager = self.static_data['directory_manager']
        diagnosis_reader = \
            Diagnosis_reader(os.path.join(directory_manager.pull_directory('raw_data_dir'),'diagnoses.xlsx'))
        Postprocessor_registry.push_data_dict(self, filename, data_dict)
        if filename in [ 'diagnosis.csv' ]:
            self._push_data_dict('postprocessor_diagnosis', data_dict, filename=filename)
            self.postprocessor_registry['postprocessor_diagnosis'].push_diagnosis_reader(diagnosis_reader)
        if filename in [ 'sections.csv' ]:
            data_dict_copy = deepcopy(data_dict)
            self._push_data_dict('postprocessor_antigens', data_dict_copy, filename=filename)
            data_dict_copy = deepcopy(data_dict)
            self._push_data_dict('postprocessor_fish_analysis_summary', data_dict_copy, filename=filename)
            data_dict_copy = deepcopy(data_dict)
            self._push_data_dict('postprocessor_karyotype', data_dict_copy, filename=filename)
            data_dict_copy = deepcopy(data_dict)
            self._push_data_dict('postprocessor_specific_diagnosis', data_dict_copy, filename=filename)
            self.postprocessor_registry['postprocessor_specific_diagnosis'].push_diagnosis_reader(diagnosis_reader)