# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 08:12:07 2018

@author: haglers
"""

#
from nlp_lib.py.base_lib.preprocessor_registry_base_class \
    import Preprocessor_registry_base
from tool_lib.py.query_tools_lib.blasts_tools \
    import Named_entity_recognition as Named_entity_recognition_blasts
from tool_lib.py.query_tools_lib.breast_cancer_biomarkers_tools \
    import Named_entity_recognition \
        as Named_entity_recognition_breast_cancer_biomarkers
from tool_lib.py.query_tools_lib.cancer_tools \
    import Named_entity_recognition as Named_entity_recognition_cancer
from tool_lib.py.query_tools_lib.histological_grade_tools \
    import Named_entity_recognition \
        as Named_entity_recognition_histological_grade
from tool_lib.py.query_tools_lib.karyotype_tools \
    import Named_entity_recognition as Named_entity_recognition_karyotype
from tool_lib.py.query_tools_lib.smoking_tools \
    import Named_entity_recognition as Named_entity_recognition_smoking

#
class Named_entity_recognition_registry(Preprocessor_registry_base):
    
    #
    def create_preprocessors(self):
        self._register_preprocessor('named_entity_recognition_blasts',
                                    Named_entity_recognition_blasts(self.static_data))
        self._register_preprocessor('named_entity_recognition_breast_cancer_biomarkers',
                                    Named_entity_recognition_breast_cancer_biomarkers(self.static_data))
        self._register_preprocessor('named_entity_recognition_cancer',
                                    Named_entity_recognition_cancer(self.static_data))
        self._register_preprocessor('named_entity_recognition_histological_grade',
                                    Named_entity_recognition_histological_grade(self.static_data))
        self._register_preprocessor('named_entity_recognition_karyotype',
                                    Named_entity_recognition_karyotype(self.static_data))
        self._register_preprocessor('named_entity_recognition_smoking',
                                    Named_entity_recognition_smoking(self.static_data))