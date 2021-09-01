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
from tool_lib.py.query_tools_lib.tnm_stage_tools \
    import Postprocessor as Postprocessor_tnm_stage

#
class BreastCancerPathology_postprocessor(Postprocessing_manager):
    
    #
    def _import_reports_body(self, static_data):
        directory_manager = static_data['directory_manager']
        data_dir = directory_manager.pull_directory('postprocessing_data_in')
        for filename in os.listdir(data_dir):
            self._select_postprocessor(filename)
        '''
        self.output_manager.append(Postprocessor_tnm_stage(static_data,
                                                           'sections.csv'))
        self.output_manager.append(Postprocessor_base(static_data,
                                                      'hist_diff.csv'))
        self.output_manager.append(Postprocessor_base(static_data,
                                                      'hist_grade.csv'))
        self.output_manager.append(Postprocessor_base(static_data,
                                                      'tumor_margin.csv'))
        self.output_manager.append(Postprocessor_base(static_data,
                                                      'tumor_size.csv'))
        '''