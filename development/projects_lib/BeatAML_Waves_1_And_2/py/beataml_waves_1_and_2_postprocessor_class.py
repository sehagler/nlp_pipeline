# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 08:12:07 2018

@author: haglers
"""

#
from copy import deepcopy
import os

#
from nlp_lib.py.postprocessing_lib.base_class_lib.postprocessor_base_class \
    import Postprocessor_base
from nlp_lib.py.postprocessing_lib.postprocessing_manager_class \
    import Postprocessing_manager
from projects_lib.BeatAML_Waves_1_And_2.py.diagnosis_reader_class \
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

#
class BeatAML_Waves_1_And_2_postprocessor(Postprocessing_manager):

    #
    def select_postprocessor(self, filename, data_dict):
        directory_manager = self.static_data['directory_manager']
        diagnosis_reader = \
            Diagnosis_reader(os.path.join(directory_manager.pull_directory('raw_data_dir'),'diagnoses.xlsx'))
        Postprocessing_manager.select_postprocessor(self, filename, data_dict)
        if filename in [ 'diagnosis.csv' ]:
            self.output_manager.append(Postprocessor_diagnosis(self.static_data,
                                                               filename,
                                                               data_dict,
                                                               diagnosis_reader))
        if filename in [ 'sections.csv' ]:
            data_dict_copy = deepcopy(data_dict)
            self.output_manager.append(Postprocessor_antigens(self.static_data,
                                                              filename,
                                                              data_dict_copy))
            data_dict_copy = deepcopy(data_dict)
            self.output_manager.append(Postprocessor_fish_analysis_summary(self.static_data,
                                                                           filename,
                                                                           data_dict_copy))
            data_dict_copy = deepcopy(data_dict)
            self.output_manager.append(Postprocessor_karyotype(self.static_data,
                                                               filename,
                                                               data_dict_copy))
            data_dict_copy = deepcopy(data_dict)
            self.output_manager.append(Postprocessor_specific_diagnosis(self.static_data,
                                                                        filename,
                                                                        data_dict_copy,
                                                                        diagnosis_reader))