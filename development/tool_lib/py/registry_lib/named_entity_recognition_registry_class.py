# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 08:12:07 2018

@author: haglers
"""

#
from nlp_pipeline_lib.py.base_lib.preprocessor_base_class \
    import Preprocessor_base
from nlp_pipeline_lib.py.base_lib.preprocessor_registry_base_class \
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
    def _process_regular_initialisms(self):
        
        #
        self._normalize_regular_initialism('cerebrospinal fluid', 'CSF')
        self._normalize_regular_initialism('chronic kidney disease', 'CKD')
        self._normalize_regular_initialism('chronic renal disease( \( CRD \))?', 'CKD')
        self._normalize_regular_initialism('chronic renal failure( \( CRF \))?', 'CKD')
        self._normalize_regular_initialism('chronic renal (impairment|insufficiency)', 'CKD')
        self._normalize_regular_initialism('fluorescen(ce|t) in situ hybridization', 'FISH')
        self._normalize_regular_initialism('in situ hybridization', 'ISH')
        self._normalize_regular_initialism('past medical hx', 'PMH')
        self._normalize_regular_initialism('PMHx', 'PMH')
        self._normalize_regular_initialism('PMH / o', 'PMH')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)red blood cell', self.text, 'RBC')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)white blood cell', self.text, 'WBC')
        
        #
        self._normalize_regular_initialism('food and drug administration', 'FDA')
        self._normalize_regular_initialism('world health organization', 'WHO')
        
        # miscellaneous
        self._normalize_regular_initialism('columnar cell change', 'CCC')
        self._normalize_regular_initialism('eastern cooperative oncology group', 'ECOG')
        self._normalize_regular_initialism('flat epithelial atypia', 'FEA')
        self._normalize_regular_initialism('pathologic complete response', 'pCR')
        self._normalize_regular_initialism('residual ca(ncer)? burden', 'RCB')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)FAB (?=[0-9])', self.text, 'FAB M')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)HLA-Dr', self.text, 'HLA-DR')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)blasts ?(\+|and|plus) ?promonocytes', self.text, 'blasts/promonocytes')
        self._normalize_regular_initialism('(?i)minimal residual disease', 'MRD')
        self._normalize_regular_initialism('(?i)myelodysplastic syndrome', 'MDS')  
    
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