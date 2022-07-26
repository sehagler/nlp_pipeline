# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 16:45:34 2020

@author: haglers
"""

#
from tool_lib.py.query_tools_lib.base_lib.preprocessor_base_class \
    import Preprocessor_base
from tool_lib.py.processing_tools_lib.text_processing_tools \
    import regex_from_list, s

#
class Preprocessor(Preprocessor_base):
    
    #
    def _normalize_chemical_abbreviations(self):
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('alcohol(?!i)', 'alcohol', self.text, 'ETOH')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('butyrate esterase', self.text, 'BE')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)immunohistochemi(cal|stry)', self.text, 'IHC')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('methotrexate', self.text, 'MTX')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('myeloperoxidase', self.text, 'MPO')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('sudan black B', self.text, 'SBB')
        
    #
    def run_preprocessor(self):
        self._normalize_chemical_abbreviations()