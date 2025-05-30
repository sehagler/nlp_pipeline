# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 12:13:55 2020

@author: haglers
"""

#
import lambda_lib.tool_lib.lambda_tools as lambda_tools
from tools_lib.processing_tools_lib.text_processing_tools \
    import block_label, case_number, part_label, slice_label, slide_label, s, test_label

#
def _remove_case_number(text):
    text = \
        lambda_tools.deletion_lambda_conversion('(?i)(\n\s*)?case number:[\n\s]+' + case_number(), text)
    text = \
        lambda_tools.deletion_lambda_conversion('(?i)(\n\s*)?\( see case ' + case_number() + ' \)', text)
    return text
    
#
def _remove_part(text):
    text = \
        lambda_tools.deletion_lambda_conversion('(?i)\s*\( part' + s() + '-' + part_label() + '((-to-|-)' + part_label() + ' )? \)', text)
    #match_str = '(?i)((\n\s*)?-( )?)?(please[\n\s]+)?see (also )?' + \
    #    'part' + s() + '( )?' + part_label() + '( to ' + part_label() + ')?'
    return text
    
#
def _remove_slice(text):
    text = \
        lambda_tools.deletion_lambda_conversion('(?i)(\n\s*)?\( spans slices ' + slice_label() + '-' + slice_label() + ' \)', text)
    text = \
        lambda_tools.deletion_lambda_conversion('(?i)slice (#( )?)?' + slice_label() + '((,)? )?(with clip((,)? )?)?', text)
    return text
    
#
def _remove_slide(text):
    text = \
        lambda_tools.deletion_lambda_conversion('(?i)\( slide' + s() + ' [^n\)\]]+ \)', text)
    text = \
        lambda_tools.deletion_lambda_conversion('(?i)(\n\s*)?\( (for example )?slide' + s() +  \
                                                       '[\n\s]+' + slide_label() + '(((,)? ' + slide_label() + ')+)?' + \
                                                       '(( and |-)' + slide_label() + ')? \)', text)
    text = \
        lambda_tools.deletion_lambda_conversion('(?i)(\n\s*)?\( (for example )?slide' + s() + \
                                                       '[\n\s]+' + slide_label() + \
                                                       '(((,)? ' + slide_label() + ')+)?' + \
                                                       '(( and |-)' + slide_label() + ')? \)', text)
    text = \
        lambda_tools.deletion_lambda_conversion('(?i)(\n\s*)?\( \d+ slide' + s() + ' \)', text)
    text = \
        lambda_tools.deletion_lambda_conversion('(?i)(, )?slide ' + slide_label(), text)
    return text
    
#
def _remove_test(text):
    text = \
        lambda_tools.deletion_lambda_conversion('(?i)\( test # ' + test_label() + ' \)', text)
    return text

#
class Preprocessor(object):

    #
    def __init__(self, static_data_object, logger_object):
        self.static_data_object = static_data_object
        self.logger_object = logger_object
    
    #
    def run_object(self, text):
        text = sequential_composition([_remove_test,
                                       _remove_slide,
                                       _remove_slice,
                                       _remove_part,
                                       _remove_case_number], text)
        text = normalize_text(self.text)