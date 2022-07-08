# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 15:04:20 2020

@author: haglers
"""

#
from nlp_text_normalization_lib.base_lib.preprocessor_base_class \
    import Preprocessor_base

#
class Named_entity_recognition(Preprocessor_base):
    
    #
    def run_preprocessor(self):
        self._normalize_whitespace()
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('packs?( (/|per))? days?', self.text, 'PPD')
        self.text = \
            self.lambda_manager.lambda_conversion(' ppd', self.text, ' PPD')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('packs?( (/|per))? wks?', self.text, 'PPW')
        self.text = \
            self.lambda_manager.lambda_conversion(' ppw', self.text, ' PPW')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('packs?( (/|per))? yrs?', self.text, 'PPY')
        self.text = \
            self.lambda_manager.lambda_conversion(' ppy', self.text, ' PPY')
        
#
class Summarization(Preprocessor_base):
    
    #
    def run_preprocessor(self):
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?i)check out the free oregon quit line(.*\n)*.*www . quitnow . net / oregon', self.text)