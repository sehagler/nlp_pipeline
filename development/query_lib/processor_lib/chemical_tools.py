# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 16:45:34 2020

@author: haglers
"""

#
from base_lib.preprocessor_base_class import Preprocessor_base
import lambda_lib.object_lib.lambda_object_class as lambda_lib
    
#
def _normalize_chemical_abbreviations(text):
    text = \
        lambda_lib.contextual_lambda_conversion('alcohol(?!i)', 'alcohol', text, 'ETOH')
    text = \
        lambda_lib.initialism_lambda_conversion('butyrate esterase', text, 'BE')
    text = \
        lambda_lib.lambda_conversion('(?i)immunohistochemi(cal|stry)', text, 'IHC')
    text = \
        lambda_lib.initialism_lambda_conversion('methotrexate', text, 'MTX')
    text = \
        lambda_lib.initialism_lambda_conversion('myeloperoxidase', text, 'MPO')
    text = \
        lambda_lib.initialism_lambda_conversion('sudan black B', text, 'SBB')
    return text

#
class Preprocessor(Preprocessor_base):
        
    #
    def run_preprocessor(self):
        self.text = _normalize_chemical_abbreviations(self.text)