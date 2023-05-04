# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 11:45:17 2020

@author: haglers
"""

#
import lambda_lib.tool_lib.lambda_tools as lambda_tools
from tools_lib.processing_tools_lib.function_processing_tools \
    import sequential_composition_new as sequential_composition
       
#
def _process_mitotic_rate(text):
    text = \
        lambda_tools.lambda_conversion('(?i)(points )?for mito(s(e|i)s|tic)( (activity|count|figure(s)?|index|rate))', text, 'for mitoses')
    match_str0 = '(?i)mito(s(e|i)s|tic)( (activity|count|figure(s)?|index|rate))? \( \d \)'
    match_str1 = '(?i)mito(s(e|i)s|tic)( (activity|count|figure(s)?|index|rate))?'
    text = \
        lambda_tools.contextual_lambda_conversion(match_str0, match_str1, text, 'mitoses = ')
    match_str0 = '(?i)mito(s(e|i)s|tic)( (activity|count|figure(s)?|index|rate))?' + \
                 '(:)?((\s)?(grade|score)?( of)?)? \d'
    match_str1 = '(?i)mito(s(e|i)s|tic)( (activity|count|figure(s)?|index|rate))?' + \
                 '(:)?((\s)?(grade|score)?( of)?)?'
    text = \
        lambda_tools.contextual_lambda_conversion(match_str0, match_str1, text, 'mitoses = ')
    text = \
        lambda_tools.lambda_conversion('(?i)mito(ses|sis|tic) (activity|count|figure(s)?|index|rate)', text, 'mitoses')
    text = \
        lambda_tools.lambda_conversion('(?i)mitos(e|i)s', text, 'mitoses')
    text = \
        lambda_tools.lambda_conversion('(?i)mito(ses|sis|tic) (activity|count|figure(s)?|index|rate)', text, 'mitoses')
    text = \
        lambda_tools.lambda_conversion('(?i) mitoses per ', text, '/')
    text = \
        lambda_tools.lambda_conversion(' a mitoses', text, ' mitoses')
    return text
    
#
def _process_nuclear_pleomorphism(text):
    text = \
        lambda_tools.lambda_conversion('(?i)pleomorphism', text, 'nuclear pleomorphism')
    text = \
        lambda_tools.lambda_conversion('(?i)nuclear nuclear', text, 'nuclear')
    text = \
        lambda_tools.lambda_conversion('(?i)(points )?for nuclear (atypia|grade|pleomorphism|score)', text, 'for nuclei')
    match_str = '(?i)nuclear (atypia|grade|pleomorphism|score) \( \d \)'
    text = \
        lambda_tools.contextual_lambda_conversion(match_str, ' \)', text, '')
    match_str = '(?i)nuclear (atypia|grade|pleomorphism|score) \( \d'
    text = \
        lambda_tools.contextual_lambda_conversion(match_str, '\( ', text, '')
    match_str0 = '(?i)nuclear (atypia|grade|pleomorphism|score) \d'
    match_str1 = '(?i)nuclear (atypia|grade|pleomorphism|score)'
    text = \
        lambda_tools.contextual_lambda_conversion(match_str0, match_str1, text, 'nuclei = ')
    match_str0 = '(?i)nucle(ar|i)( (atypia|grade|pleomorphism|score))?' + \
                '(:)?((\s)?(grade|score)?( of)?)? \d'
    match_str1 = '(?i)nucle(ar|i)( (atypia|grade|pleomorphism|score))?' + \
                '(:)?((\s)?(grade|score)?( of)?)?'
    text = \
        lambda_tools.contextual_lambda_conversion(match_str0, match_str1, text, 'nuclei = ')
    text = \
        lambda_tools.lambda_conversion('(?i)nuclei', text, 'nuclei')
    text = \
        lambda_tools.lambda_conversion('(?i)nuclear (atypia|grade|pleomorphism|score)', text, 'nuclei')
    text = \
        lambda_tools.lambda_conversion(' a nuclei', text, ' nuclei')
    return text
    
#
def _process_tubule_formation(text):
    match_str = '(?i)(points )?for (glandular )?(\(acinar\)-)?tub(al|ular|ule(s)?)' + \
                '( (differentiation|formation))?'
    text = \
        lambda_tools.lambda_conversion(match_str, text, 'for tubules')
    match_str = '(?i)(glandular )?(\(acinar\)-)?tub(al|ular|ule(s)?)' + \
                '( (differentiation|formation))? \( \d \)'
    text = \
        lambda_tools.contextual_lambda_conversion(match_str, ' \)', text, '')
    match_str = '(?i)(glandular )?(\(acinar\)-)?tub(al|ular|ule(s)?)' + \
                '( (differentiation|formation))? \( \d'
    text = \
        lambda_tools.contextual_lambda_conversion(match_str, '\( ', text, '')
    match_str0 = '(?i)(glandular )?(\(acinar\)-)?tub(al|ular|ule(s)?)' + \
                 '( (differentiation|formation))? \d'
    match_str1 = '(?i)(glandular )?(\(acinar\)-)?tub(al|ular|ule(s)?)' + \
                 '( (differentiation|formation))?'
    text = \
        lambda_tools.contextual_lambda_conversion(match_str0, match_str1, text, 'tubules = ')
    match_str0 = '(?i)(glandular )?(\(acinar\)-)?tub(al|ular|ule(s)?)' + \
                 '( (differentiation|formation))?' + \
                 '(:)?((\s)?(grade|score)?( of)?)? \d'
    match_str1 = '(?i)(glandular )?(\(acinar\)-)?tub(al|ular|ule(s)?)' + \
                 '( (differentiation|formation))?' + \
                 '(:)?((\s)?(grade|score)?( of)?)?'
    text = \
        lambda_tools.contextual_lambda_conversion(match_str0, match_str1, text, 'tubules = ')
    match_str = '(?i)(glandular )?(\(acinar\)-)?tub(al|ular|ule(s)?)' + \
                '( (differentiation|formation))'
    text = \
        lambda_tools.lambda_conversion(match_str, text, 'tubules')
    text = \
        lambda_tools.lambda_conversion(' a tubules', text, ' tubules')
    return text

#
class Preprocessor(object):
        
    #
    def run_preprocessor(self, text):
        text = \
            lambda_tools.lambda_conversion('(?<= )I( / | of )III(?=( |\n))', text, '1 / 3')
        text = \
            lambda_tools.lambda_conversion('(?<= )II( / | of )III(?=( |\n))', text, '2 / 3')
        text = \
            lambda_tools.lambda_conversion('(?<= )III( / | of )III(?=( |\n))', text, '3 / 3')
        text = \
            lambda_tools.lambda_conversion('(?<= )1 of 3(?=( |\n))', text, '1 / 3')
        text = \
            lambda_tools.lambda_conversion('(?<= )2 of 3(?=( |\n))', text, '2 / 3')
        text = \
            lambda_tools.lambda_conversion('(?<= )3 of 3(?=( |\n))', text, '3 / 3')
        text_list = []
        text_list.append('(?i)modified Scarff(-| )Bloom(-| )(and(-| ))?Richardson( \(mSBR\))?')
        text_list.append('(?i)modified Bloom(-| )(and(-| ))?Richardson( \(mBR\))?')
        text_list.append('(?i)Scarff(-| )Bloom(-| )(and(-| ))?Richardson( \(SBR\))?')
        text_list.append('(?i)modified Richardson')
        text_list.append('(?i)Bloom(-| )(and(-| ))?Richardson( \(BR\))?')
        for item in text_list:
            text = \
                lambda_tools.lambda_conversion(item, text, 'mSBR')
        text = sequential_composition([_process_mitotic_rate,
                                       _process_nuclear_pleomorphism,
                                       _process_tubule_formation], text)
        return text