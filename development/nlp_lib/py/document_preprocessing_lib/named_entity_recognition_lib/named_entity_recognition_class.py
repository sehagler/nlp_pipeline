# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 11:46:26 2021

@author: haglers
"""

#
from nlp_lib.py.document_preprocessing_lib.base_class_lib.preprocessor_base_class \
    import Preprocessor_base
from tool_lib.py.processing_tools_lib.text_processing_tools import s
from tool_lib.py.query_tools_lib.biomarker_tools \
    import Named_entity_recognition as Named_entity_recognition_biomarkers
from tool_lib.py.query_tools_lib.cancer_tools \
    import Named_entity_recognition as Named_entity_recognition_cancer
from tool_lib.py.query_tools_lib.histological_grade_tools \
    import Named_entity_recognition as Named_entity_recognition_histological_grade
from tool_lib.py.query_tools_lib.karyotype_tools \
    import Named_entity_recognition as Named_entity_recognition_karyotype
from tool_lib.py.query_tools_lib.smoking_tools \
    import Named_entity_recognition as Named_entity_recognition_smoking

#
class Named_entity_recognition(Preprocessor_base): 
    
    #
    def __init__(self, static_data):
        Preprocessor_base.__init__(self, static_data)
        self.named_entity_recognition_biomarkers = \
            Named_entity_recognition_biomarkers(self.static_data)        
        self.named_entity_recognition_cancer = \
            Named_entity_recognition_cancer(self.static_data)
        self.named_entity_recognition_histological_grade = \
            Named_entity_recognition_histological_grade(self.static_data)
        self.named_entity_recognition_karyotype = \
            Named_entity_recognition_karyotype(self.static_data)
        self.named_entity_recognition_smoking = \
            Named_entity_recognition_smoking(self.static_data)
            
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
        self._general_command('(?i)red blood cell', {None : 'RBC'})
        self._general_command('(?i)white blood cell', {None : 'WBC'})
        
        #
        self._normalize_regular_initialism('food and drug administration', 'FDA')
        self._normalize_regular_initialism('world health organization', 'WHO')
        
        # miscellaneous
        self._normalize_regular_initialism('columnar cell change', 'CCC')
        self._normalize_regular_initialism('eastern cooperative oncology group', 'ECOG')
        self._normalize_regular_initialism('flat epithelial atypia', 'FEA')
        self._normalize_regular_initialism('pathologic complete response', 'pCR')
        self._normalize_regular_initialism('residual ca(ncer)? burden', 'RCB')
        self._general_command('(?i)FAB (?=[0-9])', {None : 'FAB M'})
        self._general_command('(?i)HLA-Dr', {None : 'HLA-DR'})
        self._general_command('(?i)blasts ?(\+|and|plus) ?promonocytes', {None : 'blasts/promonocytes'})
        self._normalize_regular_initialism('(?i)minimal residual disease', 'MRD')
        self._normalize_regular_initialism('(?i)myelodysplastic syndrome', 'MDS')       
    
    #
    def process_document(self, text):
        self.text = text
        self._normalize_whitespace()
        self._process_regular_initialisms()
        self.named_entity_recognition_biomarkers.push_text(self.text)
        self.named_entity_recognition_biomarkers.process_biomarkers()
        self.text = self.named_entity_recognition_biomarkers.pull_text()
        self.named_entity_recognition_cancer.push_text(self.text)
        self.named_entity_recognition_cancer.process_abbreviations()
        self.named_entity_recognition_cancer.process_initialisms()
        self.text = self.named_entity_recognition_cancer.pull_text()
        self.named_entity_recognition_histological_grade.push_text(self.text)
        self.named_entity_recognition_histological_grade.process_msbr()
        self.text = self.named_entity_recognition_histological_grade.pull_text()
        self.named_entity_recognition_karyotype.push_text(self.text)
        self.named_entity_recognition_karyotype.process_karyotype()
        self.text = self.named_entity_recognition_karyotype.pull_text()
        self.named_entity_recognition_smoking.push_text(self.text)
        self.named_entity_recognition_smoking.process_initialisms()
        self.text = self.named_entity_recognition_smoking.pull_text()
        self._normalize_whitespace()
        return self.text