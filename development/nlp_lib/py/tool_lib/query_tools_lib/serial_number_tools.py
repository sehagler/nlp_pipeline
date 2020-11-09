# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 12:13:55 2020

@author: haglers
"""

#
from nlp_lib.py.base_class_lib.preprocessor_base_class import Preprocessor_base
from nlp_lib.py.tool_lib.processing_tools_lib.text_processing_tools \
    import block_label, case_number, part_label, slice_label, slide_label, s, test_label

#
class Summarization(Preprocessor_base):
    
    #
    def _remove_block(self):
        self._clear_command_list()
        self._general_command('(?i)(\n\s*)?\( block' + s() + ' (#( )?)?' + block_label() + '(-' + block_label() + ')? \)', {None : ''})
        self._process_command_list()
    
    #
    def _remove_case_number(self):
        self._clear_command_list()
        self._general_command('(?i)(\n\s*)?case number:[\n\s]+' + case_number(), {None : ''})
        self._general_command('(?i)(\n\s*)?\( see case ' + case_number() + ' \)', {None : ''})
        self._process_command_list()
        
    #
    def _remove_part(self):
        self._clear_command_list()
        self._general_command('(?i)\s*\( part' + s() + '-' + part_label() + '((-to-|-)' + part_label() + ' )? \)', {None : ''})
        match_str = '(?i)((\n\s*)?-( )?)?(please[\n\s]+)?see (also )?' + \
            'part' + s() + '( )?' + part_label() + '( to ' + part_label() + ')?'
        self._substitution_endings_list(match_str)
        self._process_command_list()
        
    #
    def _remove_slice(self):
        self._clear_command_list()
        self._general_command('(?i)(\n\s*)?\( spans slices ' + slice_label() + '-' + slice_label() + ' \)', {None : ''})
        self._general_command('(?i)slice (#( )?)?' + slice_label() + '((,)? )?(with clip((,)? )?)?', {None : ''})
        self._process_command_list()
        
    #
    def _remove_slide(self):
        self._clear_command_list()
        self._general_command('(?i)\( slide' + s() + ' [^n\)\]]+ \)', {None : ''})
        self._general_command('(?i)(\n\s*)?\( (for example )?slide' + s() +  \
                              '[\n\s]+' + slide_label() + '(((,)? ' + slide_label() + ')+)?' + \
                              '(( and |-)' + slide_label() + ')? \)', {None : ''})
        self._general_command('(?i)(\n\s*)?\( (for example )?slide' + s() + \
                              '[\n\s]+' + slide_label() + \
                              '(((,)? ' + slide_label() + ')+)?' + \
                              '(( and |-)' + slide_label() + ')? \)', {None : ''})
        self._general_command('(?i)(\n\s*)?\( \d+ slide' + s() + ' \)', {None : ''})
        self._general_command('(?i)(, )?slide ' + slide_label(), {None : ''})
        self._process_command_list()
        
    #
    def _remove_test(self):
        self._clear_command_list()
        self._general_command('(?i)\( test # ' + test_label() + ' \)', {None : ''})
        self._process_command_list()
        
    #
    def remove_extraneous_text(self):
        self._remove_block()
        self._remove_case_number()
        self._remove_part()
        self._remove_slice()
        self._remove_slide()
        self._remove_test()