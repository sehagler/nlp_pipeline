# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 15:49:43 2020

@author: haglers
"""

#
from lambda_lib.lambda_manager_class import Lambda_manager
from regex_lib.regex_tools \
    import class_label, part_label, specimen_label, s

#
class Specimen_normalizer(object):
    
    #
    def __init__(self):
        self.lambda_manager = Lambda_manager()
    
    #
    def _indicate_nonspecimens(self, mode_flg):
        if mode_flg == 'do':
            term_list = []
            term_list.append('class')
            for term in term_list:
                match_str = '(?i)' + term   + s() + ' ' + class_label()
                self.text = \
                    self.lambda_manager.contextual_lambda_conversion(match_str, term + s() + ' ', self.text, 'class<HYPHEN>')
            term_list = []
            term_list.append('part')
            for term in term_list:
                match_str = '(?i)' + term  + s() + ' ' + part_label()
                self.text = \
                    self.lambda_manager.contextual_lambda_conversion(match_str, term + s() + ' ', self.text, 'part<HYPHEN>')
        elif mode_flg == 'undo':
            term_list = []
            term_list.append('class')
            term_list.append('part')
            for term in term_list:
                match_str = '(?i)' + term + '<HYPHEN>'
                self.text = \
                    self.lambda_manager.contextual_lambda_conversion(match_str, term + '<HYPHEN>', self.text, ' ')
                
    #
    def _remove_false_specimen(self):
        self.text = \
            self.lambda_manager.deletion_lambda_conversion(' \((([a-l]|[o-s]|[u-z])+[0-9]+(,( )?)?)+\)',
                                                           self.text)
                
    #
    def normalize_text(self, text):
        self.text = text
        #self._indicate_nonspecimens('do')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('[ \t][a-z]\.[ \t]', '\.', self.text, ':')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('[ \t][a-z]\.[ \t]', '(?i)[ \t](?=[a-z])', self.text, '\n\n')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('(\n[A-Z]\: +)(?=[A-Za-z])', '\n', self.text, '\nSPECIMEN ')
        #self._indicate_nonspecimens('undo')
        return text