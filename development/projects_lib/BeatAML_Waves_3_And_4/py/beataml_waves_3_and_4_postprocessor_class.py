# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 08:12:07 2018

@author: haglers
"""

#
import os

#
from nlp_lib.py.postprocessing_lib.base_class_lib.postprocessor_base_class \
    import Postprocessor_base
from nlp_lib.py.postprocessing_lib.postprocessing_manager_class \
    import Postprocessing_manager
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

#
class BeatAML_Waves_3_And_4_postprocessor(Postprocessing_manager):

    #
    def _import_reports_body(self, static_data):
        directory_manager = static_data['directory_manager']
        data_dir = directory_manager.pull_directory('postprocessing_data_in')
        for filename in os.listdir(data_dir):
            self._select_postprocessor(filename)
        diagnosis_reader = Diagnosis_reader(os.path.join(directory_manager.pull_directory('raw_data_dir'),'diagnoses.xlsx'))
        self.output_manager.append(Postprocessor_diagnosis(static_data,
                                                           'diagnosis.csv',
                                                           diagnosis_reader))
        self.output_manager.append(Postprocessor_antigens(static_data,
                                                          'sections.csv'))
        self.output_manager.append(Postprocessor_fish_analysis_summary(static_data,
                                                                       'sections.csv'))
        self.output_manager.append(Postprocessor_karyotype(static_data,
                                                           'sections.csv'))
        self.output_manager.append(Postprocessor_specific_diagnosis(static_data,
                                                                    'sections.csv',
                                                                    diagnosis_reader))