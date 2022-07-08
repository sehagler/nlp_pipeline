# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 08:12:07 2018

@author: haglers
"""

#
from nlp_text_normalization_lib.base_lib.preprocessor_base_class \
    import Preprocessor_base
from nlp_text_normalization_lib.base_lib.preprocessor_registry_base_class \
    import Preprocessor_registry_base
from tool_lib.py.query_tools_lib.base_lib.blasts_tools_base \
    import Named_entity_recognition as Named_entity_recognition_blasts
from tool_lib.py.query_tools_lib.base_lib.breast_cancer_biomarkers_tools_base \
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
class Named_entity_recognition_base(Preprocessor_base):
    
    #
    def _process_organizations(self):
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('eastern cooperative oncology group', self.text, 'ECOG')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('(u( \. )?s( \.)? ?)?food and drug administration', self.text, 'FDA')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('world health organization', self.text, 'WHO')
    
    #
    def _process_past_medical_history(self):
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('past medical hx', self.text, 'PMH')
        self.text = \
            self.lambda_manager.lambda_conversion('PMHx', self.text, 'PMH')
        self.text = \
            self.lambda_manager.lambda_conversion('PMH / o', self.text, 'PMH')
        
    
    #
    def _process_regular_initialisms(self):
        
        #
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('cerebrospinal fluid', self.text, 'CSF')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('chronic kidney disease', self.text, 'CKD')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('chronic renal disease', self.text, 'CRD')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('chronic renal failure', self.text, 'CRF')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('fluorescen(ce|t) in situ hybridization', self.text, 'FISH')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('in situ hybridization', self.text, 'ISH')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('red blood cell', self.text, 'RBC')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('white blood cell', self.text, 'WBC')
            
        #
        self._process_past_medical_history()
        self._process_organizations()
        
        # miscellaneous
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('columnar cell change', self.text, 'CCC')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('flat epithelial atypia', self.text, 'FEA')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('pathologic complete response', self.text, 'pCR')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('residual ca(ncer)? burden', self.text, 'RCB')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)FAB (?=[0-9])', self.text, 'FAB M')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)HLA-Dr', self.text, 'HLA-DR')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)blasts ?(\+|and|plus) ?promonocytes', self.text, 'blasts/promonocytes')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('(?i)minimal residual disease', self.text, 'MRD')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('(?i)myelodysplastic syndrome', self.text, 'MDS')  
    
    #
    def run_preprocessor(self):
        self._normalize_whitespace()
        self._process_regular_initialisms()

#
class Named_entity_recognition_registry(Preprocessor_registry_base):
    
    #
    def create_preprocessors(self):
        self._register_preprocessor('named_entity_recognition_base',
                                    Named_entity_recognition_base(self.static_data))
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