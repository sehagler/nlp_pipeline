# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 15:04:20 2020

@author: haglers
"""

#
from nlp_lib.py.document_preprocessing_lib.base_class_lib.preprocessor_base_class import Preprocessor_base

#
class Named_entity_recognition(Preprocessor_base):
    
    #
    def process_initialisms(self):
        
        #
        self._normalize_regular_initialism('packs?( (/|per))? days?', 'PPD')
        self._normalize_regular_initialism(' ppd', ' PPD')
        self._normalize_regular_initialism('packs?( (/|per))? wks?', 'PPW')
        self._normalize_regular_initialism(' ppw', ' PPW')
        self._normalize_regular_initialism('packs?( (/|per))? yrs?', 'PPY')
        self._normalize_regular_initialism(' ppy', ' PPY')