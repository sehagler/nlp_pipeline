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
from tool_lib.py.query_tools_lib.biomarker_tools \
    import Postprocessor as Postprocessor_biomarker
#from tool_lib.py.query_tools_lib.tnm_stage_tools \
#    import Postprocessor as Postprocessor_tnm_stage

#
class BreastCancerPathology_postprocessor(Postprocessing_manager):
    
    #
    def _import_reports_body(self, project_data):
        directory_manager = project_data['directory_manager']
        data_dir = directory_manager.pull_directory('postprocessing_data_in')
        '''
        self.output_manager.append(Postprocessor_tnm_stage(project_data,
                                                           os.path.join(data_dir,
                                                                        'section.csv'),
                                                           'TNM STAGE'))
        self.output_manager.append(Postprocessor_base(project_data,
                                                      'SECTION',
                                                      os.path.join(data_dir,
                                                                   'section.csv')))
        '''
        self.output_manager.append(Postprocessor_biomarker(project_data,
                                                           os.path.join(data_dir,
                                                                        'biomarkers.csv'),
                                                           'BIOMARKERS'))
        '''
        self.output_manager.append(Postprocessor_base(project_data,
                                                      'HISTOLOGICAL DIFFERENTIATION',
                                                      os.path.join(data_dir,
                                                                   'hist_diff.csv')))
        self.output_manager.append(Postprocessor_base(project_data,
                                                      'HISTOLOGICAL GRADE',
                                                      os.path.join(data_dir,
                                                                   'hist_grade.csv')))
        self.output_manager.append(Postprocessor_base(project_data,
                                                      'TUMOR MARGIN',
                                                      os.path.join(data_dir,
                                                                   'tumor_margin.csv')))
        self.output_manager.append(Postprocessor_base(project_data,
                                                      'TUMOR SIZE',
                                                      os.path.join(data_dir,
                                                                   'tumor_size.csv')))
        '''