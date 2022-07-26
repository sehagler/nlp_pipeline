# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 16:41:11 2021

@author: haglers
"""

#
from lambda_lib.lambda_manager_class import Lambda_manager
from tool_lib.py.processing_tools_lib.text_processing_tools import s
from tool_lib.py.query_tools_lib.base_lib.date_tools_base \
    import Tokenizer as Tokenizer_date

#
class Style_normalizer(object):
    
    #
    def __init__(self):
        self.lambda_manager = Lambda_manager()
        self.tokenizer_date = Tokenizer_date()
        
    #
    def _normalize_abbreviation(self):
        self.text = \
            self.lambda_manager.lambda_conversion('percentage', self.text, '%age')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=d)iagnosis', self.text, 'x')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=d)iagnose(?=[ds])', self.text, 'xe')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=f)ollow( |\-)up', self.text, '/u')
        self.text = \
            self.lambda_manager.lambda_conversion('for example', self.text, 'e.g.')
        self.text = \
            self.lambda_manager.lambda_conversion('from (the )?nipple', self.text, 'fn')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=h)istory', self.text, 'x')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=h)x of', self.text, '/o')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=l)aborator(ie|y)', self.text, 'ab')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=m)etastases', self.text, 'ets')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=m)onth', self.text, 'o')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=p)atient', self.text, 't')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=r)efills', self.text, 'fl')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=r)esection', self.text, 'sxn')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=s)urgical procedure', self.text, '/p')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=y)ear', self.text, 'r')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=y)(ear|r)?(s)?(-| )old', self.text, '/o')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=y)\.o\.', self.text, '/o')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[0-9]y)o(?= )', self.text, '/o')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[0-9][\- ]y)o(?= )', self.text, '/o')
            
    #
    def _normalize_colon(self):
        self.text = \
            self.lambda_manager.lambda_conversion(' M/E ', self.text, ' M:E ')
        self.text = \
            self.lambda_manager.lambda_conversion(' N/C ', self.text, ' N:C ')
        
    #
    def _normalize_credentials(self):
        self.text = \
            self.lambda_manager.lambda_conversion('D(\. )?O\.', self.text, 'DO')
        self.text = \
            self.lambda_manager.lambda_conversion('Dr\.', self.text, 'Dr')
        self.text = \
            self.lambda_manager.lambda_conversion('m(\. )?d\.', self.text, 'MD')
        self.text = \
            self.lambda_manager.lambda_conversion('ph(\. )?d\.', self.text, 'PhD')
        
    #
    def _normalize_datetime(self):
        self.text = \
            self.lambda_manager.lambda_conversion('[\n\s]+o(\')?clock', self.text, ' : 00')
        self.text = \
            self.lambda_manager.lambda_conversion('a(\. )?m\.', self.text, 'AM')
        self.text = \
            self.lambda_manager.lambda_conversion('p(\. )?m\.', self.text, 'PM')
        self.tokenizer_date.push_text(self.text)
        self.tokenizer_date.process_month()
        self.text = self.tokenizer_date.pull_text()
        
    #
    def _normalize_equals_sign(self):
        self.text = \
            self.lambda_manager.lambda_conversion('equals', self.text, '=')
        self.text = \
            self.lambda_manager.lambda_conversion('is equal to', self.text, '=')
            
    #
    def _normalize_greater_than_sign(self):
        self.text = \
            self.lambda_manager.lambda_conversion('at least', self.text, '>')
        self.text = \
            self.lambda_manager.lambda_conversion('(greater|more) th(a|e)n', self.text, '>')
            
    #
    def _normalize_less_than_sign(self):
        self.text = \
            self.lambda_manager.lambda_conversion('at most', self.text, '<')
        self.text = \
            self.lambda_manager.lambda_conversion('less th(a|e)n', self.text, '<')
        self.text = \
            self.lambda_manager.lambda_conversion('up to( ~)?', self.text, '<')
    
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
    def _normalize_number_sign(self):
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('blocks? +#', '#', self.text, '')
            
    #
    def _normalize_of(self):
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[0-9])of', self.text, ' of')
        self.text = \
            self.lambda_manager.lambda_conversion('of(?=[0-9])', self.text, 'of ')
            
    #
    def _normalize_per(self):
        self.text = \
            self.lambda_manager.lambda_conversion('according to', self.text, 'per')
            
    #
    def _normalize_plural(self):
        self.text = \
            self.lambda_manager.lambda_conversion('margin\(s\)', self.text, 'margins')
            
    #
    def _normalize_slash(self):
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('(<=(\d+)(\-|\+)?) ((out )?of|per) (?= [0-9])', 
                                                             ' ((out )?of|per) ', self.text, '/')
            
    #
    def _normalize_tilde(self):
        self.text = \
            self.lambda_manager.lambda_conversion('(only )?about', self.text, '~')
        self.text = \
            self.lambda_manager.lambda_conversion('approx(( \.)|imate(ly)?)?', self.text, '~')
        self.text = \
            self.lambda_manager.lambda_conversion('estimated', self.text, '~')
        self.text = \
            self.lambda_manager.lambda_conversion('roughly', self.text, '~')
            
    #
    def _normalize_units(self):
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('high(-| )?power(ed)? field' + s(), self.text, 'HPF')
        self.text = \
            self.lambda_manager.lambda_conversion('HPF(\')?s', self.text, 'HPF')
        self.text = \
            self.lambda_manager.lambda_conversion('cmfn', self.text, 'cm fn')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[0-9])cm', self.text, ' cm ')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[0-9])mm', self.text, ' mm ')
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?<=(cm|mm))\.', self.text)
            
    #
    def _normalize_with(self):
        self.text = \
            self.lambda_manager.lambda_conversion(' w/ ', self.text, ' with ')
            
                    
    #
    def _remove_superfluous_text(self):
        self.text = \
            self.lambda_manager.lambda_conversion('histologic grade', self.text, 'grade')
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('day 0( is equal to | ?= ?)', self.text)
        
    #
    def normalize_text(self, text):
        self.text = text
        self._normalize_abbreviation()
        self._normalize_colon()
        self._normalize_credentials()
        self._normalize_datetime()
        self._normalize_equals_sign()
        self._normalize_greater_than_sign()
        self._normalize_less_than_sign()
        self._normalize_minus_sign()
        self._normalize_number_sign()
        self._normalize_of()
        self._normalize_per()
        self._normalize_plural()
        self._normalize_slash()
        self._normalize_tilde()
        self._normalize_units()
        self._normalize_with()
        self._remove_superfluous_text()
        return self.text