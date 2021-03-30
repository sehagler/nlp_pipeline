# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 12:51:07 2020

@author: haglers
"""

#
import os

#
from nlp_lib.py.processor_lib.postprocessor_lib.postprocessor_class import Postprocessor
from nlp_lib.py.tool_lib.query_tools_lib.cancer_stage_tools import Postprocessor as Postprocessor_cancer_stage
from nlp_lib.py.tool_lib.query_tools_lib.ecog_tools import Postprocessor as Postprocessor_ecog_score
from nlp_lib.py.tool_lib.query_tools_lib.smoking_history_tools import Postprocessor as Postprocessor_smoking_history
from nlp_lib.py.tool_lib.query_tools_lib.smoking_products_tools import Postprocessor as Postprocessor_smoking_products
from nlp_lib.py.tool_lib.query_tools_lib.smoking_status_tools import Postprocessor as Postprocessor_smoking_status

#
class CCC19_postprocessor(Postprocessor):

    #
    def _import_reports_body(self, project_data):
        directory_manager = project_data['directory_manager']
        data_dir = directory_manager.pull_directory('postprocessing_data_in')
        data_key_map, data_value_map = self._business_rules('CANCER STAGE TEXT')
        self.output_manager.append(Postprocessor_cancer_stage(project_data,
                                                              os.path.join(data_dir,
                                                                           'cancer_stage.csv'),
                                                              data_key_map,
                                                              data_value_map,
                                                              'CANCER STAGE'))
        data_key_map, data_value_map = self._business_rules('ECOG SCORE TEXT')
        self.output_manager.append(Postprocessor_ecog_score(project_data,
                                                            os.path.join(data_dir,
                                                                         'ecog_status.csv'),
                                                            data_key_map,
                                                            data_value_map,
                                                            'ECOG SCORE'))
        data_key_map, data_value_map = self._business_rules('SMOKING HISTORY TEXT')
        self.output_manager.append(Postprocessor_smoking_history(project_data,
                                                                 os.path.join(data_dir,
                                                                              'smoking_history.csv'),
                                                                 data_key_map,
                                                                 data_value_map,
                                                                 'SMOKING HISTORY'))
        data_key_map, data_value_map = self._business_rules('SMOKING PRODUCTS TEXT')
        self.output_manager.append(Postprocessor_smoking_products(project_data,
                                                                  os.path.join(data_dir,
                                                                               'smoking_products.csv'),
                                                                  data_key_map,
                                                                  data_value_map,
                                                                  'SMOKING PRODUCTS'))
        data_key_map, data_value_map = self._business_rules('SMOKING STATUS TEXT')
        self.output_manager.append(Postprocessor_smoking_status(project_data,
                                                                os.path.join(data_dir,
                                                                             'smoking_status.csv'),
                                                                data_key_map,
                                                                data_value_map,
                                                                'SMOKING STATUS'))