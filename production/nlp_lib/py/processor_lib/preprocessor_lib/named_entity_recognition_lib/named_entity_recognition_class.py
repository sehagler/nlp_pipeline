# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 10:17:40 2020

@author: haglers
"""

#
from nlp_lib.py.base_class_lib.preprocessor_base_class import Preprocessor_base
from nlp_lib.py.tool_lib.processing_tools_lib.text_processing_tools import s

#
class Named_entity_recognition(Preprocessor_base):
        
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
    def process_initialisms(self):
        self._process_regular_initialisms()