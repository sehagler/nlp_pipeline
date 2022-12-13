# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 12:13:55 2020

@author: haglers
"""

#
from base_lib.preprocessor_base_class import Preprocessor_base
from tools_lib.processing_tools_lib.text_processing_tools \
    import block_label, case_number, part_label, slice_label, slide_label, s, test_label

#
class Preprocessor(Preprocessor_base):
    
    '''
    #
    def _remove_block(self):
        self.text = \
            self.lambda_object.deletion_lambda_conversion('(?i)(\n\s*)?\( block' + s() + ' (#( )?)?' + block_label() + '(-' + block_label() + ')? \)', self.text)
    '''
    
    #
    def _remove_case_number(self):
        self.text = \
            self.lambda_object.deletion_lambda_conversion('(?i)(\n\s*)?case number:[\n\s]+' + case_number(), self.text)
        self.text = \
            self.lambda_object.deletion_lambda_conversion('(?i)(\n\s*)?\( see case ' + case_number() + ' \)', self.text)
        
    #
    def _remove_part(self):
        self.text = \
            self.lambda_object.deletion_lambda_conversion('(?i)\s*\( part' + s() + '-' + part_label() + '((-to-|-)' + part_label() + ' )? \)', self.text)
        #match_str = '(?i)((\n\s*)?-( )?)?(please[\n\s]+)?see (also )?' + \
        #    'part' + s() + '( )?' + part_label() + '( to ' + part_label() + ')?'
        
    #
    def _remove_slice(self):
        self.text = \
            self.lambda_object.deletion_lambda_conversion('(?i)(\n\s*)?\( spans slices ' + slice_label() + '-' + slice_label() + ' \)', self.text)
        self.text = \
            self.lambda_object.deletion_lambda_conversion('(?i)slice (#( )?)?' + slice_label() + '((,)? )?(with clip((,)? )?)?', self.text)
        
    #
    def _remove_slide(self):
        self.text = \
            self.lambda_object.deletion_lambda_conversion('(?i)\( slide' + s() + ' [^n\)\]]+ \)', self.text)
        self.text = \
            self.lambda_object.deletion_lambda_conversion('(?i)(\n\s*)?\( (for example )?slide' + s() +  \
                                                           '[\n\s]+' + slide_label() + '(((,)? ' + slide_label() + ')+)?' + \
                                                           '(( and |-)' + slide_label() + ')? \)', self.text)
        self.text = \
            self.lambda_object.deletion_lambda_conversion('(?i)(\n\s*)?\( (for example )?slide' + s() + \
                                                           '[\n\s]+' + slide_label() + \
                                                           '(((,)? ' + slide_label() + ')+)?' + \
                                                           '(( and |-)' + slide_label() + ')? \)', self.text)
        self.text = \
            self.lambda_object.deletion_lambda_conversion('(?i)(\n\s*)?\( \d+ slide' + s() + ' \)', self.text)
        self.text = \
            self.lambda_object.deletion_lambda_conversion('(?i)(, )?slide ' + slide_label(), self.text)
        
    #
    def _remove_test(self):
        self.text = \
            self.lambda_object.deletion_lambda_conversion('(?i)\( test # ' + test_label() + ' \)', self.text)
        
    #
    def run_preprocessor(self):
        self._remove_case_number()
        self._remove_part()
        self._remove_slice()
        self._remove_slide()
        self._remove_test()