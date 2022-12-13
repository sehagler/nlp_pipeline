# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 16:41:11 2021

@author: haglers
"""

#
from lambda_lib.object_lib.lambda_object_class import Lambda_object
from tools_lib.regex_lib.regex_tools \
    import (
        article,
        minus_sign,
        s,
        space
    )
from tools_lib.processing_tools_lib.function_processing_tools \
    import composite_function
from query_lib.processor_lib.base_lib.date_tools_base \
    import Tokenizer as Tokenizer_date
    
#
def _normalize_abbreviation(text):
    lambda_object = Lambda_object()
    text = \
        lambda_object.space_correction_lambda_conversion('percentage', text, '%AGE')
    text = \
        lambda_object.space_correction_lambda_conversion('diagnosis', text, 'DX')
    text = \
        lambda_object.space_correction_lambda_conversion('diagnosed', text, 'DXED')
    text = \
        lambda_object.space_correction_lambda_conversion('diagnoses', text, 'DXES')
    text = \
        lambda_object.space_correction_lambda_conversion('follow(' + minus_sign() + '|' + space() + ')up', text, 'F/U')
    text = \
        lambda_object.space_correction_lambda_conversion('for example', text, 'E.G.')
    text = \
        lambda_object.space_correction_lambda_conversion('from (' + article() + ' )?nipple', text, 'FN')
    text = \
        lambda_object.space_correction_lambda_conversion('history', text, 'HX')
    text = \
        lambda_object.space_correction_lambda_conversion('hx' + space() + 'of', text, 'H/O')
    text = \
        lambda_object.space_correction_lambda_conversion('laboratories', text, 'LABS')
    text = \
        lambda_object.space_correction_lambda_conversion('laboratory', text, 'LAB')
    #text = \
    #    lambda_object.space_correction_lambda_conversion('metastases', text, 'ets')
    text = \
        lambda_object.space_correction_lambda_conversion('months', text, 'MOS')
    text = \
        lambda_object.space_correction_lambda_conversion('month', text, 'MO')
    text = \
        lambda_object.space_correction_lambda_conversion('patients', text, 'PTS')
    text = \
        lambda_object.space_correction_lambda_conversion('patient', text, 'PT')
    text = \
        lambda_object.space_correction_lambda_conversion('refills', text, 'RFL')
    text = \
        lambda_object.space_correction_lambda_conversion('resection', text, 'RSXN')
    text = \
        lambda_object.space_correction_lambda_conversion('surgical procedure', text, 'S/P')
    text = \
        lambda_object.space_correction_lambda_conversion('weeks', text, 'WKS')
    text = \
        lambda_object.space_correction_lambda_conversion('week', text, 'WK')
    text = \
        lambda_object.space_correction_lambda_conversion('years', text, 'YRS')
    text = \
        lambda_object.space_correction_lambda_conversion('year', text, 'YR')
    text = \
        lambda_object.space_correction_lambda_conversion('yr?s?(' + minus_sign() + '|' + space() + ')old', text, 'Y/O')
    text = \
        lambda_object.space_correction_lambda_conversion('y\.o\.', text, 'Y/O')
    text = \
        lambda_object.space_correction_lambda_conversion('(?<=[0-9])yo(?= )', text, 'Y/O')
    text = \
        lambda_object.space_correction_lambda_conversion('(?<=[0-9][\- ])yo(?= )', text, 'Y/O')
    return text
        
#
def _normalize_colon(text):
    lambda_object = Lambda_object()
    text = \
        lambda_object.lambda_conversion(' M/E ', text, ' M:E ')
    text = \
        lambda_object.lambda_conversion(' N/C ', text, ' N:C ')
    return text
    
#
def _normalize_credentials(text):
    lambda_object = Lambda_object()
    text = \
        lambda_object.lambda_conversion('D(\. )?O\.', text, 'DO')
    text = \
        lambda_object.lambda_conversion('Dr\.', text, 'Dr')
    text = \
        lambda_object.lambda_conversion('m(\. )?d\.', text, 'MD')
    text = \
        lambda_object.lambda_conversion('ph(\. )?d\.', text, 'PhD')
    return text
    
#
def _normalize_datetime(text):
    lambda_object = Lambda_object()
    tokenizer_date = Tokenizer_date()
    text = \
        lambda_object.lambda_conversion('[\n\s]+o(\')?clock', text, ' : 00')
    text = \
        lambda_object.lambda_conversion('a(\. )?m\.', text, 'AM')
    text = \
        lambda_object.lambda_conversion('p(\. )?m\.', text, 'PM')
    tokenizer_date.push_text(text)
    tokenizer_date.process_month()
    text = tokenizer_date.pull_text()
    return text
    
#
def _normalize_equals_sign(text):
    lambda_object = Lambda_object()
    text = \
        lambda_object.lambda_conversion('equals', text, '=')
    text = \
        lambda_object.lambda_conversion('is equal to', text, '=')
    return text
        
#
def _normalize_greater_than_sign(text):
    lambda_object = Lambda_object()
    text = \
        lambda_object.lambda_conversion('at least', text, '>')
    text = \
        lambda_object.lambda_conversion('(greater|more) th(a|e)n', text, '>')
    return text
        
#
def _normalize_less_than_sign(text):
    lambda_object = Lambda_object()
    text = \
        lambda_object.lambda_conversion('at most', text, '<')
    text = \
        lambda_object.lambda_conversion('less th(a|e)n', text, '<')
    text = \
        lambda_object.lambda_conversion('up to( ~)?', text, '<')
    return text

#
def _normalize_minus_sign(text):
    lambda_object = Lambda_object()
    text = \
        lambda_object.lambda_conversion('fine needle', text, 'fine-needle')
    text = \
        lambda_object.lambda_conversion('-grade', text, ' grade')
    text = \
        lambda_object.lambda_conversion('-to-', text, ' to ')
    text = \
        lambda_object.lambda_conversion('in-situ', text, 'in situ')
    text = \
        lambda_object.lambda_conversion('in-toto', text, 'in toto')
    text = \
        lambda_object.lambda_conversion('intermediate to strong', text, 'intermediate-strong')
    text = \
        lambda_object.lambda_conversion('moderate to strong', text, 'moderate-strong')
    text = \
        lambda_object.lambda_conversion('moderate to weak', text, 'weak-moderate')
    text = \
        lambda_object.lambda_conversion('over-expression', text, 'overexpression')
    text = \
        lambda_object.lambda_conversion('strong to moderate', text, 'moderate-strong')
    text = \
        lambda_object.lambda_conversion('weak to moderate', text, 'weak-moderate')
    text = \
        lambda_object.lambda_conversion('weak to strong', text, 'weak-strong')
    text = \
        lambda_object.lambda_conversion('(?<![0-9]) - (?![0-9])', text, '\n- ')
    return text
        
#
def _normalize_newline(text):
    lambda_object = Lambda_object()
    text = \
        lambda_object.lambda_conversion('\n +', text, '\n')
    return text
        
#
def _normalize_number_sign(text):
    lambda_object = Lambda_object()
    text = \
        lambda_object.contextual_lambda_conversion('blocks? +#', '#', text, '')
    return text
        
#
def _normalize_of(text):
    lambda_object = Lambda_object()
    text = \
        lambda_object.lambda_conversion('(?<=[0-9])of', text, ' of')
    text = \
        lambda_object.lambda_conversion('of(?=[0-9])', text, 'of ')
    return text
        
#
def _normalize_per(text):
    lambda_object = Lambda_object()
    text = \
        lambda_object.lambda_conversion('according to', text, 'per')
    return text
        
#
def _normalize_plural(text):
    lambda_object = Lambda_object()
    text = \
        lambda_object.lambda_conversion('margin\(s\)', text, 'margins')
    return text
        
#
def _normalize_slash(text):
    lambda_object = Lambda_object()
    text = \
        lambda_object.contextual_lambda_conversion('(<=(\d+)(\-|\+)?) ((out )?of|per) (?= [0-9])', 
                                                         ' ((out )?of|per) ', text, '/')
    return text
        
#
def _normalize_tilde(text):
    lambda_object = Lambda_object()
    text = \
        lambda_object.lambda_conversion('(only )?about', text, '~')
    text = \
        lambda_object.lambda_conversion('approx(( \.)|imate(ly)?)?', text, '~')
    text = \
        lambda_object.lambda_conversion('estimated', text, '~')
    text = \
        lambda_object.lambda_conversion('roughly', text, '~')
    return text
        
#
def _normalize_units(text):
    lambda_object = Lambda_object()
    text = \
        lambda_object.initialism_lambda_conversion('high(-| )?power(ed)? field' + s(), text, 'HPF')
    text = \
        lambda_object.lambda_conversion('HPF(\')?s', text, 'HPF')
    text = \
        lambda_object.lambda_conversion('cmfn', text, 'cm fn')
    text = \
        lambda_object.erasure_lambda_conversion('-(?=(cm|mm))', text)
    text = \
        lambda_object.lambda_conversion('(?<=[0-9])cm', text, ' cm ')
    text = \
        lambda_object.lambda_conversion('(?<=[0-9])mm', text, ' mm ')
    text = \
        lambda_object.deletion_lambda_conversion('(?<=(cm|mm))\.', text)
    return text
        
#
def _normalize_with(text):
    lambda_object = Lambda_object()
    text = \
        lambda_object.lambda_conversion(' w/ ', text, ' with ')
    return text
        
                
#
def _remove_superfluous_text(text):
    lambda_object = Lambda_object()
    text = \
        lambda_object.lambda_conversion('histologic grade', text, 'grade')
    text = \
        lambda_object.deletion_lambda_conversion('day 0( is equal to | ?= ?)', text)
    return text
        
#
def style_normalizer(text):
    normalize_text = composite_function(_remove_superfluous_text,
                                        _normalize_with,
                                        _normalize_units,
                                        _normalize_plural,
                                        _normalize_per,
                                        _normalize_of,
                                        _normalize_datetime,
                                        _normalize_credentials,
                                        _normalize_abbreviation,
                                        _normalize_tilde,
                                        _normalize_slash,
                                        _normalize_number_sign,
                                        _normalize_newline,
                                        _normalize_minus_sign,
                                        _normalize_less_than_sign,
                                        _normalize_greater_than_sign,
                                        _normalize_equals_sign,
                                        _normalize_colon)
    text = normalize_text(text)
    return text