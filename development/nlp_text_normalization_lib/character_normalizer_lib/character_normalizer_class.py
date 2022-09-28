# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 08:56:52 2021

@author: haglers
"""

#
import re

#
from lambda_lib.lambda_manager_class import Lambda_manager

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
            self.lambda_manager.lambda_conversion('(?<=[a-z0-9])\*', self.text,' *')
            
    #
    def _normalize_colon(self):
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('(\n)[A-Z]\.[ \t]', '\.', self.text, ':')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('(?<!(:|\d))\d+-\d+:00',
                                                             '-', self.text, ' : 00-')
        self.text = \
            self.lambda_manager.lambda_conversion(':', self.text, ' : ')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[0-9]) : (?=[0-9])', self.text, ':')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<= [A-Za-z]) : (?=[A-Za-z] )', self.text, ':')
            
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
            
    #
    def _normalize_less_than_sign(self):
        self.text = \
            self.lambda_manager.lambda_conversion('<', self.text, ' < ')
            
    #
    def _normalize_minus_sign(self):
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[0-9])-(?=[0-9])', self.text, ' - ')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[0-9] )-(?=[0-9]+%)', self.text, '- ')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[0-9])-(?= [0-9]+%)', self.text, ' -')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<= )-(?=[A-Za-z])', self.text, '- ')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[A-Za-z])-(?= )', self.text, ' -')
            
    #
    def _normalize_newline(self):
        self.text = \
            self.lambda_manager.lambda_conversion('(\s)?\(\n', self.text, '\n')
            
    #
    def _normalize_number(self):
        word_list = list(set(filter(None, re.split('[ \n\t]+', self.text))))
        change_list = []
        for word in word_list:
            if not re.search('(?i)([0-9]|point)', word):
                do_w2n = True
                if re.search('-', word):
                    element_list = word.split('-')
                    for element in element_list:
                        if 'w2n' in locals():
                            num = w2n.word_to_num(element)
                        else:
                            do_w2n = False
                if do_w2n:
                    if 'w2n' in locals():
                        num = w2n.word_to_num(word)
                        if num < 100:
                            change_list.append([word, str(num)])
        change_list.sort(key=lambda x: len(x[0]), reverse=True)
        for change in change_list:
            self.text = \
                self.lambda_manager.contextual_lambda_conversion('[ \n\t]' + change[0] + '[ \n\t]',
                                                                 change[0], self.text, change[1])
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('\( [0-9]+ - [0-9]+ \)', ' \)', self.text, '.0 )')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('\( [0-9]+ - [0-9]+\.[0-9]+ \)', ' - ', self.text, '.0 - ')
                
    #
    def _normalize_number_sign(self):
        self.text = \
            self.lambda_manager.lambda_conversion('#', self.text, ' # ')
            
    #
    def _normalize_parentheses(self):
        text_list = [ 'negative', 'positive']
        for text_str in text_list:
            regex_str = '(?<=' + text_str + ')\('
            self.text = \
                self.lambda_manager.lambda_conversion(regex_str, self.text, ' (')
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
            self.lambda_manager.lambda_conversion('(?<=[0-9])%(?=[A-Za-z])', self.text, '% ')
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
            self.lambda_manager.contextual_lambda_conversion('(\n)[A-Z] :[ \t]', ':', self.text, '.')
        self.text = \
            self.lambda_manager.lambda_conversion('\.(?![0-9])', self.text, ' . ')
        self.text = \
            self.lambda_manager.lambda_conversion('e \. g \.', self.text, 'e.g.')
            
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
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[\n ][A-Za-z]) / (?=[A-Za-z][\n ])', self.text, '/')
            
    #
    def _normalize_tilde(self):
        self.text = \
            self.lambda_manager.lambda_conversion('~', self.text, ' ~ ')
        
    #
    def _normalize_underscore(self):
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('____+(\n_+)*', self.text)
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
        self._normalize_number()
        self._normalize_number_sign()
        self._normalize_newline()
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