# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 08:12:07 2018

@author: haglers
"""

#
import os

#
from nlp_pipeline_lib.registry_lib.postprocessor_registry_class \
    import Postprocessor_registry
from projects_lib.BeatAML_Waves_3_And_4.py.diagnosis_reader_class \
    import Diagnosis_reader
from query_lib.processor_lib.specific_diagnosis_tools \
    import Postprocessor as Postprocessor_specific_diagnosis

#
class BeatAML_Waves_3_And_4_postprocessor_registry(Postprocessor_registry):
    
    #
    def __init__(self, static_data_object, logger_object, metadata_manager):
        Postprocessor_registry.__init__(self, static_data_object,
                                        logger_object, metadata_manager)
    
    #
    def register_object(self, filename):
        Postprocessor_registry.register_object(self, filename)
        diagnosis_reader = \
            Diagnosis_reader(os.path.join(self.raw_data_dir,'diagnoses.xlsx'))
        if filename in [ 'diagnosis.csv' ]:
            self.registry_dict['postprocessor_diagnosis'].push_diagnosis_reader(diagnosis_reader)
        if filename in [ 'sections.csv' ]:
            self._register_object('postprocessor_specific_diagnosis',
                                  Postprocessor_specific_diagnosis(self.static_data_object,
                                                                   self.logger_object))