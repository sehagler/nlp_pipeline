# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 08:56:52 2021

@author: haglers
"""

#
from lambda_lib.lambda_manager_class import Lambda_manager
from tool_lib.py.processing_tools_lib.text_processing_tools import s

#
class Character_normalizer(object):
    
    #
    def __init__(self):
        self.lambda_manager = Lambda_manager()
            
    #
    def _normalize_asterisk(self):
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('\*', self.text)
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)(?<=[a-z0-9])\*', self.text,' *')
            
    #
    def _normalize_colon(self):
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('(?<!(:|\d))\d+-\d+:00',
                                                             '-', self.text, ' : 00-')
        self.text = \
            self.lambda_manager.lambda_conversion(':', self.text, ' : ')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[0-9]) : (?=[0-9])', self.text, ':')
            
    #
    def _normalize_comma(self):
        self.text = \
            self.lambda_manager.lambda_conversion(',', self.text, ' , ')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[0-9]) , (?=[0-9])', self.text, ',')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[0-9]),(?=[0-9]{4})', self.text, ' , ')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[0-9]),(?=[0-9]+/)', self.text, ' , ')
            
    #
    def _normalize_equals_sign(self):
        self.text = \
            self.lambda_manager.lambda_conversion('=', self.text, ' = ')
            
    #
    def _normalize_greater_than_sign(self):
        self.text = \
            self.lambda_manager.lambda_conversion('>', self.text, ' > ')
        self.text = \
            self.lambda_manager.lambda_conversion('at least', self.text, '>')
        self.text = \
            self.lambda_manager.lambda_conversion('(greater|more) th(a|e)n', self.text, '>')
            
    #
    def _normalize_less_than_sign(self):
        self.text = \
            self.lambda_manager.lambda_conversion('<', self.text, ' < ')
        self.text = \
            self.lambda_manager.lambda_conversion('less th(a|e)n', self.text, '<')
        self.text = \
            self.lambda_manager.lambda_conversion('up to( ~)?', self.text, '<')
            
    #
    def _normalize_minus_sign(self):
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[0-9])-(?=[0-9])', self.text, ' - ')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[0-9]) -(?=[0-9]+%)', self.text, ' - ')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[0-9])- (?=[0-9]+%)', self.text, ' - ')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<= )-(?=[A-Za-z])', self.text, ' - ')
                
    #
    def _normalize_number_sign(self):
        self.text = \
            self.lambda_manager.lambda_conversion('#', self.text, ' # ')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('blocks? +#', '#', self.text, '')
            
    #
    def _normalize_parentheses(self):
        self.text = \
            self.lambda_manager.lambda_conversion('\)\(', self.text, ') (')
        self.text = \
            self.lambda_manager.lambda_conversion('\(', self.text, '( ')
        self.text = \
            self.lambda_manager.lambda_conversion('\)', self.text, ' )')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('\( [0-9\.]+ ?\)', '\( ', self.text, '(')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('\( ?[0-9\.]+ \)', ' \)', self.text, ')')
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('\( ! \)', self.text)
            
    #
    def _normalize_percent_sign(self):
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=\d) %', self.text, '%')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('(?<!(:|\d))\d+ ?- ?\d+%',
                                                             ' ?- ?', self.text, '%-')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('(?<!(:|\d))\d+ to \d+%',
                                                             ' to ', self.text, '%-')
            
    #
    def _normalize_period(self):
        self.text = \
            self.lambda_manager.lambda_conversion('\.(?![0-9])', self.text, ' . ')
            
    #
    def _normalize_plus_sign(self):
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[0-9])\+(?=[A-Za-z])', self.text, '+ ')
            
    #
    def _normalize_question_mark(self):
        self.text = \
            self.lambda_manager.deletion_lambda_conversion(' \?', self.text)
            
    #
    def _normalize_semicolon(self):
        self.text = \
            self.lambda_manager.lambda_conversion(';', self.text, ' ; ')
            
    #
    def _normalize_slash(self):
        self.text = \
            self.lambda_manager.lambda_conversion('\/', self.text, ' / ')
            
    #
    def _normalize_tilde(self):
        self.text = \
            self.lambda_manager.lambda_conversion('~', self.text, ' ~ ')
        self.text = \
            self.lambda_manager.lambda_conversion('(only )?about', self.text, '~')
        self.text = \
            self.lambda_manager.lambda_conversion('approx(( \.)|imate(ly)?)?', self.text, '~')
        self.text = \
            self.lambda_manager.lambda_conversion('estimated', self.text, '~')
        self.text = \
            self.lambda_manager.lambda_conversion('roughly', self.text, '~')
        
    #
    def _normalize_underscore(self):
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('_[A-Z][0-9]+_', '_', self.text, '')
    
    #
    def normalize_text(self, text):
        self.text = text
        self._normalize_asterisk()
        self._normalize_colon()
        self._normalize_comma()
        self._normalize_equals_sign()
        self._normalize_greater_than_sign()
        self._normalize_less_than_sign()
        self._normalize_minus_sign()
        self._normalize_number_sign()
        self._normalize_parentheses()
        self._normalize_percent_sign()
        self._normalize_period()
        self._normalize_plus_sign()
        self._normalize_question_mark()
        self._normalize_semicolon()
        self._normalize_slash()
        self._normalize_tilde()
        self._normalize_underscore()
        return self.text