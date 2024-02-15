# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 16:41:11 2021

@author: haglers
"""

#
import lambda_lib.tool_lib.lambda_tools as lambda_tools
from tools_lib.regex_lib.regex_tools \
    import (
        article,
        minus_sign,
        s,
        space
    )
from tools_lib.processing_tools_lib.function_processing_tools \
    import sequential_composition
from query_lib.processor_lib.base_lib.date_tools_base \
    import Tokenizer as Tokenizer_date
    
#
def _normalize_abbreviation(text):
    text = \
        lambda_tools.space_correction_lambda_conversion('percentage', text, '%AGE')
    text = \
        lambda_tools.space_correction_lambda_conversion('diagnosis', text, 'DX')
    text = \
        lambda_tools.space_correction_lambda_conversion('diagnosed', text, 'DXED')
    text = \
        lambda_tools.space_correction_lambda_conversion('diagnoses', text, 'DXES')
    text = \
        lambda_tools.space_correction_lambda_conversion('follow(' + minus_sign() + '|' + space() + ')up', text, 'F/U')
    text = \
        lambda_tools.space_correction_lambda_conversion('for example', text, 'E.G.')
    text = \
        lambda_tools.space_correction_lambda_conversion('from (' + article() + ' )?nipple', text, 'FN')
    text = \
        lambda_tools.space_correction_lambda_conversion('history', text, 'HX')
    text = \
        lambda_tools.space_correction_lambda_conversion('hx' + space() + 'of', text, 'H/O')
    text = \
        lambda_tools.space_correction_lambda_conversion('laboratories', text, 'LABS')
    text = \
        lambda_tools.space_correction_lambda_conversion('laboratory', text, 'LAB')
    text = \
        lambda_tools.space_correction_lambda_conversion('medical record number', text, 'MRN')
    text = \
        lambda_tools.space_correction_lambda_conversion('MRN \(', text, 'MRN ')
    text = \
        lambda_tools.space_correction_lambda_conversion('(?<=MRN \d{8} )\)', text, '')
    text = \
        lambda_tools.space_correction_lambda_conversion('months', text, 'MOS')
    text = \
        lambda_tools.space_correction_lambda_conversion('month', text, 'MO')
    text = \
        lambda_tools.space_correction_lambda_conversion('patients', text, 'PTS')
    text = \
        lambda_tools.space_correction_lambda_conversion('patient', text, 'PT')
    text = \
        lambda_tools.space_correction_lambda_conversion('refills', text, 'RFL')
    text = \
        lambda_tools.space_correction_lambda_conversion('resection', text, 'RSXN')
    text = \
        lambda_tools.space_correction_lambda_conversion('surgical procedure', text, 'S/P')
    text = \
        lambda_tools.space_correction_lambda_conversion('weeks', text, 'WKS')
    text = \
        lambda_tools.space_correction_lambda_conversion('week', text, 'WK')
    text = \
        lambda_tools.space_correction_lambda_conversion('years', text, 'YRS')
    text = \
        lambda_tools.space_correction_lambda_conversion('year', text, 'YR')
    text = \
        lambda_tools.space_correction_lambda_conversion('yr?s?(' + minus_sign() + '|' + space() + ')old', text, 'Y/O')
    text = \
        lambda_tools.space_correction_lambda_conversion('y\.o\.', text, 'Y/O')
    text = \
        lambda_tools.space_correction_lambda_conversion('(?<=[0-9])yo(?= )', text, 'Y/O')
    text = \
        lambda_tools.space_correction_lambda_conversion('(?<=[0-9][\- ])yo(?= )', text, 'Y/O')
    return text
        
#
def _normalize_colon(text):
    text = \
        lambda_tools.lambda_conversion(' M/E ', text, ' M:E ')
    text = \
        lambda_tools.lambda_conversion(' N/C ', text, ' N:C ')
    return text
    
#
def _normalize_credentials(text):
    text = \
        lambda_tools.lambda_conversion('D(\. )?O\.', text, 'DO')
    text = \
        lambda_tools.lambda_conversion('Dr\.', text, 'Dr')
    text = \
        lambda_tools.lambda_conversion('m(\. )?d\.', text, 'MD')
    text = \
        lambda_tools.lambda_conversion('ph(\. )?d\.', text, 'PhD')
    return text
    
#
def _normalize_datetime(text):
    tokenizer_date = Tokenizer_date()
    text = \
        lambda_tools.lambda_conversion('[\n\s]+o(\')?clock', text, ' : 00')
    text = \
        lambda_tools.lambda_conversion('a(\. )?m\.', text, 'AM')
    text = \
        lambda_tools.lambda_conversion('p(\. )?m\.', text, 'PM')
    text = tokenizer_date.process_month(text)
    return text
    
#
def _normalize_equals_sign(text):
    text = \
        lambda_tools.lambda_conversion('equals', text, '=')
    text = \
        lambda_tools.lambda_conversion('is equal to', text, '=')
    return text
        
#
def _normalize_greater_than_sign(text):
    text = \
        lambda_tools.lambda_conversion('at least', text, '>')
    text = \
        lambda_tools.lambda_conversion('(greater|more) th(a|e)n', text, '>')
    return text
        
#
def _normalize_less_than_sign(text):
    text = \
        lambda_tools.lambda_conversion('at most', text, '<')
    text = \
        lambda_tools.lambda_conversion('less th(a|e)n', text, '<')
    text = \
        lambda_tools.lambda_conversion('up to( ~)?', text, '<')
    return text

#
def _normalize_minus_sign(text):
    text = \
        lambda_tools.lambda_conversion('fine needle', text, 'fine-needle')
    text = \
        lambda_tools.lambda_conversion('-grade', text, ' grade')
    text = \
        lambda_tools.lambda_conversion('-to-', text, ' to ')
    text = \
        lambda_tools.lambda_conversion('in-situ', text, 'in situ')
    text = \
        lambda_tools.lambda_conversion('in-toto', text, 'in toto')
    text = \
        lambda_tools.lambda_conversion('intermediate to strong', text, 'intermediate-strong')
    text = \
        lambda_tools.lambda_conversion('moderate to strong', text, 'moderate-strong')
    text = \
        lambda_tools.lambda_conversion('moderate to weak', text, 'weak-moderate')
    text = \
        lambda_tools.lambda_conversion('over-expression', text, 'overexpression')
    text = \
        lambda_tools.lambda_conversion('strong to moderate', text, 'moderate-strong')
    text = \
        lambda_tools.lambda_conversion('weak to moderate', text, 'weak-moderate')
    text = \
        lambda_tools.lambda_conversion('weak to strong', text, 'weak-strong')
    text = \
        lambda_tools.lambda_conversion('(?<![0-9]) - (?![0-9])', text, '\n- ')
    return text
        
#
def _normalize_newline(text):
    text = \
        lambda_tools.lambda_conversion('\n +', text, '\n')
    return text
        
#
def _normalize_number_sign(text):
    text = \
        lambda_tools.contextual_lambda_conversion('blocks? +#', '#', text, '')
    return text
        
#
def _normalize_of(text):
    text = \
        lambda_tools.lambda_conversion('(?<=[0-9])of', text, ' of')
    text = \
        lambda_tools.lambda_conversion('of(?=[0-9])', text, 'of ')
    return text
        
#
def _normalize_per(text):
    text = \
        lambda_tools.lambda_conversion('according to', text, 'per')
    return text
        
#
def _normalize_plural(text):
    text = \
        lambda_tools.lambda_conversion('margin\(s\)', text, 'margins')
    return text
        
#
def _normalize_slash(text):
    text = \
        lambda_tools.contextual_lambda_conversion('(<=(\d+)(\-|\+)?) ((out )?of|per) (?= [0-9])', 
                                                ' ((out )?of|per) ', text, '/')
    return text
        
#
def _normalize_tilde(text):
    text = \
        lambda_tools.lambda_conversion('(only )?about', text, '~')
    text = \
        lambda_tools.lambda_conversion('approx(( \.)|imate(ly)?)?', text, '~')
    text = \
        lambda_tools.lambda_conversion('estimated', text, '~')
    text = \
        lambda_tools.lambda_conversion('roughly', text, '~')
    return text
        
#
def _normalize_units(text):
    text = \
        lambda_tools.initialism_lambda_conversion('high(-| )?power(ed)? field' + s(), text, 'HPF')
    text = \
        lambda_tools.lambda_conversion('HPF(\')?s', text, 'HPF')
    text = \
        lambda_tools.lambda_conversion('cmfn', text, 'cm fn')
    text = \
        lambda_tools.erasure_lambda_conversion('-(?=(cm|mm))', text)
    text = \
        lambda_tools.lambda_conversion('(?<=[0-9])cm', text, ' cm ')
    text = \
        lambda_tools.lambda_conversion('(?<=[0-9] )hour', text, 'hr')
    text = \
        lambda_tools.lambda_conversion('(?<=[0-9] )minute', text, 'min')
    text = \
        lambda_tools.lambda_conversion('(?<=[0-9])mm', text, ' mm ')
    text = \
        lambda_tools.lambda_conversion('(?<=[0-9] )second', text, 'sec')
    text = \
        lambda_tools.deletion_lambda_conversion('(?<=(cm|mm))\.', text)
    return text
        
#
def _normalize_with(text):
    text = \
        lambda_tools.lambda_conversion(' w/ ', text, ' with ')
    return text
        
                
#
def _remove_superfluous_text(text):
    text = \
        lambda_tools.lambda_conversion('histologic grade', text, 'grade')
    text = \
        lambda_tools.deletion_lambda_conversion('day 0( is equal to | ?= ?)', text)
    return text
        
#
def style_normalizer(text):
    text = sequential_composition([_normalize_colon,
                                   _normalize_equals_sign,
                                   _normalize_greater_than_sign,
                                   _normalize_less_than_sign,
                                   _normalize_minus_sign,
                                   _normalize_newline,
                                   _normalize_number_sign,
                                   _normalize_slash,
                                   _normalize_tilde,
                                   _normalize_abbreviation,
                                   _normalize_credentials,
                                   _normalize_datetime,
                                   _normalize_of,
                                   _normalize_per,
                                   _normalize_plural,
                                   _normalize_units,
                                   _normalize_with,
                                   _remove_superfluous_text], text)
    return text