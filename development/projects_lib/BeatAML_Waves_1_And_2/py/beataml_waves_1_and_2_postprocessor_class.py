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
from projects_lib.BeatAML_Waves_1_And_2.py.diagnosis_reader_class \
    import Diagnosis_reader
from tool_lib.py.query_tools_lib.antigens_tools \
    import Postprocessor as Postprocessor_antigens
from tool_lib.py.query_tools_lib.blasts_tools \
    import Postprocessor as Postprocessor_blasts
from tool_lib.py.query_tools_lib.date_tools \
    import Postprocessor as Postprocessor_date
from tool_lib.py.query_tools_lib.diagnosis_tools \
    import Postprocessor as Postprocessor_diagnosis
from tool_lib.py.query_tools_lib.extramedullary_disease_tools \
    import Postprocessor as Postprocessor_extramedullary_disease
from tool_lib.py.query_tools_lib.fab_classification_tools \
    import Postprocessor as Postprocessor_fab_classification
from tool_lib.py.query_tools_lib.fish_analysis_summary_tools \
    import Postprocessor as Postprocessor_fish_analysis_summary
from tool_lib.py.query_tools_lib.immunophenotype_tools \
    import Postprocessor as Postprocessor_immunophenotype
from tool_lib.py.query_tools_lib.karyotype_tools \
    import Postprocessor as Postprocessor_karyotype
from tool_lib.py.query_tools_lib.residual_diagnosis_tools \
    import Postprocessor as Postprocessor_residual_diagnosis
from tool_lib.py.query_tools_lib.specific_diagnosis_tools \
    import Postprocessor as Postprocessor_specific_diagnosis

#
class BeatAML_Waves_1_And_2_postprocessor(Postprocessing_manager):

    #
    def _import_reports_body(self, project_data):
        directory_manager = project_data['directory_manager']
        data_dir = directory_manager.pull_directory('postprocessing_data_in')
        diagnosis_reader = Diagnosis_reader(os.path.join(directory_manager.pull_directory('raw_data_dir'),'diagnoses.xlsx'))
        data_key_map, data_value_map = self._business_rules('BONE MARROW BLAST TEXT')
        self.output_manager.append(Postprocessor_blasts(project_data,
                                                        os.path.join(data_dir,
                                                                     'bone_marrow_blast.csv'),
                                                        data_key_map,
                                                        data_value_map,
                                                        'BONE_MARROW_BLAST'))
        data_key_map, data_value_map = self._business_rules('DIAGNOSIS TEXT')
        self.output_manager.append(Postprocessor_diagnosis(project_data,
                                                           os.path.join(data_dir,
                                                                        'diagnosis.csv'),
                                                           data_key_map,
                                                           data_value_map,
                                                           'DIAGNOSIS',
                                                           diagnosis_reader))
        data_key_map, data_value_map = self._business_rules('DIAGNOSIS DATE TEXT')
        self.output_manager.append(Postprocessor_date(project_data,
                                                      os.path.join(data_dir,
                                                                   'diagnosis_date.csv'),
                                                      data_key_map,
                                                      data_value_map,
                                                      'DIAGNOSIS_DATE'))
        data_key_map, data_value_map = self._business_rules('EXTRAMEDULLARY DISEASE TEXT')
        self.output_manager.append(Postprocessor_extramedullary_disease(project_data,
                                                                        os.path.join(data_dir,
                                                                                     'extramedullary_disease.csv'),
                                                                        data_key_map,
                                                                        data_value_map,
                                                                        'EXTRAMEDULARY_DISEASE'))
        data_key_map, data_value_map = self._business_rules('FAB CLASSIFICATION TEXT')
        self.output_manager.append(Postprocessor_fab_classification(project_data,
                                                                    os.path.join(data_dir,
                                                                                 'fab_classification.csv'),
                                                                    data_key_map,
                                                                    data_value_map,
                                                                    'FAB_CLASSIFICATION'))
        data_key_map, data_value_map = self._business_rules('SURFACE ANTIGENS TEXT')
        self.output_manager.append(Postprocessor_immunophenotype(project_data,
                                                                 os.path.join(data_dir,
                                                                              'immunophenotype.csv'),
                                                                 data_key_map,
                                                                 data_value_map,
                                                                 'SURFACE_ANTIGENS'))
        data_key_map, data_value_map = self._business_rules('PERIPHERAL BLOOD BLAST TEXT')
        self.output_manager.append(Postprocessor_blasts(project_data,
                                                        os.path.join(data_dir,
                                                                     'peripheral_blood_blast.csv'),
                                                        data_key_map,
                                                        data_value_map,
                                                        'PERIPHERAL_BLOOD_BLAST'))
        data_key_map, data_value_map = self._business_rules('RELAPSE DATE TEXT')
        self.output_manager.append(Postprocessor_date(project_data,
                                                      os.path.join(data_dir,
                                                                   'relapse_date.csv'),
                                                      data_key_map,
                                                      data_value_map,
                                                      'RELAPSE_DATE'))
        data_key_map, data_value_map = self._business_rules('RESIDUAL DISEASE TEXT')
        self.output_manager.append(Postprocessor_residual_diagnosis(project_data,
                                                                    os.path.join(data_dir,
                                                                                 'residual_disease.csv'),
                                                                    data_key_map,
                                                                    data_value_map, 
                                                                    'RESIDUAL_DISEASE'))
        self.output_manager.append(Postprocessor_antigens(project_data,
                                                          os.path.join(data_dir,
                                                                       'sections.csv'),
                                                          None, None, 
                                                          'ANTIBODIES_TESTED'))
        self.output_manager.append(Postprocessor_fish_analysis_summary(project_data,
                                                                       os.path.join(data_dir,
                                                                                    'sections.csv'),
                                                                       None,
                                                                       None,
                                                                       'FISH_ANALYSIS_SUMMARY'))
        self.output_manager.append(Postprocessor_karyotype(project_data,
                                                           os.path.join(data_dir,
                                                                        'sections.csv'),
                                                           None, None, 
                                                           'KARYOTYPE'))
        self.output_manager.append(Postprocessor_specific_diagnosis(project_data,
                                                                    os.path.join(data_dir,
                                                                                 'sections.csv'), 
                                                                    None, None,
                                                                    'SPECIFIC_DIAGNOSIS', 
                                                                    diagnosis_reader))