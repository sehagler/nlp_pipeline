# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 12:51:07 2020

@author: haglers
"""

#
import os

#
from nlp_lib.py.postprocessing_lib.postprocessing_manager_class \
    import Postprocessing_manager
from tool_lib.py.query_tools_lib.cancer_stage_tools \
    import Postprocessor as Postprocessor_cancer_stage
from tool_lib.py.query_tools_lib.ecog_tools \
    import Postprocessor as Postprocessor_ecog_score
from tool_lib.py.query_tools_lib.smoking_history_tools \
    import Postprocessor as Postprocessor_smoking_history
from tool_lib.py.query_tools_lib.smoking_products_tools \
    import Postprocessor as Postprocessor_smoking_products
from tool_lib.py.query_tools_lib.smoking_status_tools \
    import Postprocessor as Postprocessor_smoking_status

#
class CCC19_postprocessor(Postprocessing_manager):

    #
    def _import_reports_body(self, project_data):
        directory_manager = project_data['directory_manager']
        data_dir = directory_manager.pull_directory('postprocessing_data_in')
        self.output_manager.append(Postprocessor_cancer_stage(project_data,
                                                              os.path.join(data_dir,
                                                                           'cancer_stage.csv'),
                                                              'CANCER_STAGE'))
        self.output_manager.append(Postprocessor_ecog_score(project_data,
                                                            os.path.join(data_dir,
                                                                         'ecog_status.csv'),
                                                            'ECOG_SCORE'))
        self.output_manager.append(Postprocessor_smoking_history(project_data,
                                                                 os.path.join(data_dir,
                                                                              'smoking_history.csv'),
                                                                 'SMOKING_HISTORY'))
        self.output_manager.append(Postprocessor_smoking_products(project_data,
                                                                  os.path.join(data_dir,
                                                                               'smoking_products.csv'),
                                                                  'SMOKING_PRODUCTS'))
        self.output_manager.append(Postprocessor_smoking_status(project_data,
                                                                os.path.join(data_dir,
                                                                             'smoking_status.csv'),
                                                                'SMOKING_STATUS'))