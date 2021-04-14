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
from nlp_lib.py.tool_lib.query_tools_lib.tnm_stage_tools \
    import Postprocessor as Postprocessor_tnm_stage

#
class BreastCancerPathology_postprocessor(Postprocessing_manager):

    #
    def _biomarker_business_rules(self):
        data_key_map, data_value_map = self._business_rules('Biomarkers Text')
        data_key_map['ER'] = 'ER'
        data_key_map['HER2'] = 'HER2'
        data_key_map['Ki67'] = 'Ki67'
        data_key_map['PR'] = 'PR'
        data_value_map['(?<!(/|\d))\d(\+)?(/\d(\+)?)?(?!(\d|%|\+))'] = 'SAME'
        data_value_map['absent'] = 'SAME'
        data_value_map['amplified'] = 'SAME'
        data_value_map['borderline'] = 'SAME'
        data_value_map['equivocal'] = 'SAME'
        data_value_map['high'] = 'SAME'
        data_value_map['low'] = 'SAME'
        data_value_map['negative'] = 'SAME'
        data_value_map['(non-|un)amplified'] = 'non-amplified'
        data_value_map['positive'] = 'SAME'
        data_value_map['present'] = 'SAME'
        return data_key_map, data_value_map

    #
    def _histological_grade_business_rules(self):
        data_key_map, data_value_map = self._business_rules('Histological Grade Text')
        data_key_map['Grade'] = 'Histological Grade'
        data_key_map['Mitoses'] = 'Mitoses'
        data_key_map['Nuclei'] = 'Nuclei'
        data_key_map['Tubules'] = 'Tubules'
        data_value_map['(low|(?<!(/|\d))1(/3)?)'] = '1'
        data_value_map['(intermediate|(?<!(/|\d))2(/3)?)'] = '2'
        data_value_map['(high|(?<!(/|\d))3(/3)?)'] = '3'
        data_value_map['(?<![a-z])I(?![a-z])'] = '1'
        data_value_map['1/111'] = '1'
        data_value_map['11/111'] = '2'
        data_value_map['111/111'] = '3'
        return data_key_map, data_value_map
    
    #
    def _import_reports_body(self, project_data):
        directory_manager = project_data['directory_manager']
        data_dir = directory_manager.pull_directory('postprocessing_data_in')
        self.output_manager.append(Postprocessor_tnm_stage(project_data,
                                                           os.path.join(data_dir,
                                                                        'section.csv'),
                                                           'TNM STAGE'))
        data_key_map, data_value_map, data_text_map = self._tumor_type_business_rules()
        self.output_manager.append(Postprocessor_base(project_data,
                                                      'SECTION',
                                                      os.path.join(data_dir,
                                                                   'section.csv'),
                                                      data_key_map,
                                                      data_value_map))
        data_key_map, data_value_map = self._biomarker_business_rules()
        self.output_manager.append(Postprocessor_base(project_data,
                                                      'BIOMARKER',
                                                      os.path.join(data_dir,
                                                                   'biomarker.csv'),
                                                      data_key_map,
                                                      data_value_map))
        data_key_map, data_value_map = \
            self._business_rules('Histological Differentiation Text')
        self.output_manager.append(Postprocessor_base(project_data,
                                                      'HISTOLOGICAL DIFFERENTIATION',
                                                      os.path.join(data_dir,
                                                                   'hist_diff.csv'),
                                                      data_key_map,
                                                      data_value_map))
        data_key_map, data_value_map = \
            self._histological_grade_business_rules()
        self.output_manager.append(Postprocessor_base(project_data,
                                                      'HISTOLOGICAL GRADE',
                                                      os.path.join(data_dir,
                                                                   'hist_grade.csv'),
                                                      data_key_map,
                                                      data_value_map))
        data_key_map, data_value_map = self._margin_business_rules()
        self.output_manager.append(Postprocessor_base(project_data,
                                                      'TUMOR MARGIN',
                                                      os.path.join(data_dir,
                                                                   'tumor_margin.csv'),
                                                      data_key_map,
                                                      data_value_map))
        data_key_map, data_value_map = self._business_rules('Tumor Size Text')
        self.output_manager.append(Postprocessor_base(project_data,
                                                      'TUMOR SIZE',
                                                      os.path.join(data_dir,
                                                                   'tumor_size.csv'),
                                                      data_key_map,
                                                      data_value_map))
        
    #
    def _margin_business_rules(self):
        data_key_map, data_value_map = self._business_rules('Margin Text')
        data_key_map['Margins?' ] = 'Margin'
        data_value_map['clear'] = 'SAME'
        data_value_map['free'] = 'SAME'
        data_value_map['negative'] = 'SAME'
        return data_key_map, data_value_map

    #
    def _tumor_type_business_rules(self):
        data_key_map, data_value_map = self._business_rules('Tumor Type Text')
        data_text_map = {}
        data_text_map['ADH'] = 'SAME'
        data_text_map['ALH'] = 'SAME'
        data_text_map['CCC'] = 'SAME'
        data_text_map['CCH'] = 'SAME'
        data_text_map['DCIS'] = 'SAME'
        data_text_map['FEA'] = 'SAME'
        data_text_map['IDC'] = 'SAME'
        data_text_map['ILC'] = 'SAME'
        data_text_map['LCIS'] = 'SAME'
        data_text_map['SCP'] = 'SAME'
        data_text_map['UDH'] = 'SAME'
        data_text_map['FEA'] = 'SAME'
        return data_key_map, data_value_map, data_text_map