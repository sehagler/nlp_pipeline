# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 08:56:52 2021

@author: haglers
"""

#
import re

#
import lambda_lib.tool_lib.lambda_tools as lambda_tools
from tools_lib.processing_tools_lib.function_processing_tools \
    import composite_function

#
def _normalize_asterisk(text):
    text = \
        lambda_tools.deletion_lambda_conversion('\*', text)
    text = \
        lambda_tools.lambda_conversion('(?<=[a-z0-9])\*', text,' *')
    return text
        
#
def _normalize_colon(text):
    text = \
        lambda_tools.contextual_lambda_conversion('(\n)[A-Z]\.[ \t]', '\.', text, ':')
    text = \
        lambda_tools.contextual_lambda_conversion('(?<!(:|\d))\d+-\d+:00',
                                                         '-', text, ' : 00-')
    text = \
        lambda_tools.lambda_conversion(':', text, ' : ')
    text = \
        lambda_tools.lambda_conversion('(?<=[0-9]) : (?=[0-9])', text, ':')
    text = \
        lambda_tools.lambda_conversion('(?<= [A-Za-z]) : (?=[A-Za-z] )', text, ':')
    return text
        
#
def _normalize_comma(text):
    text = \
        lambda_tools.lambda_conversion(',', text, ' , ')
    text = \
        lambda_tools.lambda_conversion('(?<=[0-9]) , (?=[0-9])', text, ',')
    text = \
        lambda_tools.lambda_conversion('(?<=[0-9]),(?=[0-9]{4})', text, ' , ')
    text = \
        lambda_tools.lambda_conversion('(?<=[0-9]),(?=[0-9]+/)', text, ' , ')
    return text
        
#
def _normalize_equals_sign(text):
    text = \
        lambda_tools.lambda_conversion('=', text, ' = ')
    return text
        
#
def _normalize_greater_than_sign(text):
    text = \
        lambda_tools.lambda_conversion('>', text, ' > ')
    return text
        
#
def _normalize_less_than_sign(text):
    text = \
        lambda_tools.lambda_conversion('<', text, ' < ')
    return text
        
#
def _normalize_minus_sign(text):
    text = \
        lambda_tools.lambda_conversion('(?<=[0-9])-(?=[0-9])', text, ' - ')
    text = \
        lambda_tools.lambda_conversion('(?<=[0-9] )-(?=[0-9]+%)', text, '- ')
    text = \
        lambda_tools.lambda_conversion('(?<=[0-9])-(?= [0-9]+%)', text, ' -')
    text = \
        lambda_tools.lambda_conversion('(?<= )-(?=[A-Za-z])', text, '- ')
    text = \
        lambda_tools.lambda_conversion('(?<=[A-Za-z])-(?= )', text, ' -')
    return text
        
#
def _normalize_newline(text):
    text = \
        lambda_tools.lambda_conversion('(\s)?\(\n', text, '\n')
    return text
        
#
def _normalize_number(text):
    word_list = list(set(filter(None, re.split('[ \n\t]+', text))))
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
        text = \
            lambda_tools.contextual_lambda_conversion('[ \n\t]' + change[0] + '[ \n\t]',
                                                             change[0], text, change[1])
    text = \
        lambda_tools.contextual_lambda_conversion('\( [0-9]+ - [0-9]+ \)', ' \)', text, '.0 )')
    text = \
        lambda_tools.contextual_lambda_conversion('\( [0-9]+ - [0-9]+\.[0-9]+ \)', ' - ', text, '.0 - ')
    return text
            
#
def _normalize_number_sign(text):
    text = \
        lambda_tools.lambda_conversion('#', text, ' # ')
    return text
        
#
def _normalize_parentheses(text):
    text_list = [ 'negative', 'positive']
    for text_str in text_list:
        regex_str = '(?<=' + text_str + ')\('
        text = \
            lambda_tools.lambda_conversion(regex_str, text, ' (')
    text = \
        lambda_tools.lambda_conversion('\)\(', text, ') (')
    text = \
        lambda_tools.lambda_conversion('\(', text, '( ')
    text = \
        lambda_tools.lambda_conversion('\)', text, ' )')
    text = \
        lambda_tools.contextual_lambda_conversion('\( [0-9\.]+ ?\)', '\( ', text, '(')
    text = \
        lambda_tools.contextual_lambda_conversion('\( ?[0-9\.]+ \)', ' \)', text, ')')
    text = \
        lambda_tools.deletion_lambda_conversion('\( ! \)', text)
    return text
        
#
def _normalize_percent_sign(text):
    text = \
        lambda_tools.lambda_conversion('(?<=[0-9])%(?=[A-Za-z])', text, '% ')
    text = \
        lambda_tools.lambda_conversion('(?<=\d) %', text, '%')
    text = \
        lambda_tools.contextual_lambda_conversion('(?<!(:|\d))\d+ ?- ?\d+%',
                                                         ' ?- ?', text, '%-')
    text = \
        lambda_tools.contextual_lambda_conversion('(?<!(:|\d))\d+ to \d+%',
                                                         ' to ', text, '%-')
    return text
        
#
def _normalize_period(text):
    text = \
        lambda_tools.contextual_lambda_conversion('(\n)[A-Z] :[ \t]', ':', text, '.')
    text = \
        lambda_tools.lambda_conversion('\.(?![0-9])', text, ' . ')
    text = \
        lambda_tools.lambda_conversion('e \. g \.', text, 'e.g.')
    return text
        
#
def _normalize_plus_sign(text):
    text = \
        lambda_tools.lambda_conversion('(?<=[0-9])\+(?=[A-Za-z])', text, '+ ')
    return text
        
#
def _normalize_question_mark(text):
    text = \
        lambda_tools.deletion_lambda_conversion(' \?', text)
    return text
        
#
def _normalize_semicolon(text):
    text = \
        lambda_tools.lambda_conversion(';', text, ' ; ')
    return text
        
#
def _normalize_slash(text):
    text = \
        lambda_tools.lambda_conversion('\/', text, ' / ')
    text = \
        lambda_tools.lambda_conversion('(?<=[\n ][A-Za-z]) / (?=[A-Za-z][\n ])', text, '/')
    return text
        
#
def _normalize_tilde(text):
    text = \
        lambda_tools.lambda_conversion('~', text, ' ~ ')
    return text
    
#
def _normalize_underscore(text):
    text = \
        lambda_tools.deletion_lambda_conversion('____+(\n_+)*', text)
    text = \
        lambda_tools.contextual_lambda_conversion('_[A-Z][0-9]+_', '_', text, '')
    return text
    
#
def character_normalizer(text):
    normalize_text = composite_function(_normalize_underscore,
                                        _normalize_tilde,
                                        _normalize_slash,
                                        _normalize_semicolon,
                                        _normalize_question_mark,
                                        _normalize_plus_sign,
                                        _normalize_period,
                                        _normalize_percent_sign,
                                        _normalize_parentheses,
                                        _normalize_newline,
                                        _normalize_number_sign,
                                        _normalize_number,
                                        _normalize_minus_sign,
                                        _normalize_less_than_sign,
                                        _normalize_greater_than_sign,
                                        _normalize_equals_sign,
                                        _normalize_comma,
                                        _normalize_colon,
                                        _normalize_asterisk)
    text = normalize_text(text)
    return text