# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 16:41:11 2021

@author: haglers
"""

#
from lambda_lib.lambda_manager_class import Lambda_manager

#
class Style_normalizer(object):
    
    #
    def __init__(self):
        self.lambda_manager = Lambda_manager()
 
    #
    def _normalize_colon(self):
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('(\n)[A-Z]\.[ \t]', '\.', self.text, ':')
    
    #
    def _normalize_minus_sign(self):
        self.text = \
            self.lambda_manager.lambda_conversion('fine needle', self.text, 'fine-needle')
        self.text = \
            self.lambda_manager.lambda_conversion('-grade', self.text, ' grade')
        self.text = \
            self.lambda_manager.lambda_conversion('-to-', self.text, ' to ')
        self.text = \
            self.lambda_manager.lambda_conversion('in-situ', self.text, 'in situ')
        self.text = \
            self.lambda_manager.lambda_conversion('in-toto', self.text, 'in toto')
        self.text = \
            self.lambda_manager.lambda_conversion('intermediate to strong', self.text, 'intermediate-strong')
        self.text = \
            self.lambda_manager.lambda_conversion('moderate to strong', self.text, 'moderate-strong')
        self.text = \
            self.lambda_manager.lambda_conversion('moderate to weak', self.text, 'weak-moderate')
        self.text = \
            self.lambda_manager.lambda_conversion('over-expression', self.text, 'overexpression')
        self.text = \
            self.lambda_manager.lambda_conversion('strong to moderate', self.text, 'moderate-strong')
        self.text = \
            self.lambda_manager.lambda_conversion('weak to moderate', self.text, 'weak-moderate')
        self.text = \
            self.lambda_manager.lambda_conversion('weak to strong', self.text, 'weak-strong')
            
    #
    def _normalize_newline(self):
        self.text = \
            self.lambda_manager.lambda_conversion('(\s)?\(\n', self.text, '\n')
            
    #
    def _normalize_parentheses(self):
        text_list = [ 'negative', 'positive']
        for text_str in text_list:
            regex_str = '(?<=' + text_str + ')\('
            self.text = \
                self.lambda_manager.lambda_conversion(regex_str, self.text, ' (')
            
    #
    def _normalize_period(self):
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('(\n)[A-Z] :[ \t]', ':', self.text, '.')
            
    #
    def _normalize_plural(self):
        self.text = \
            self.lambda_manager.lambda_conversion('margin\(s\)', self.text, 'margins')
            
    #
    def _normalize_underscore(self):
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('____+(\n_+)*', self.text)
        
    #
    def normalize_text(self, text):
        self.text = text
        self._normalize_colon()
        self._normalize_minus_sign()
        self._normalize_newline()
        self._normalize_parentheses()
        self._normalize_period()
        self._normalize_plural()
        self._normalize_underscore()
        return self.text