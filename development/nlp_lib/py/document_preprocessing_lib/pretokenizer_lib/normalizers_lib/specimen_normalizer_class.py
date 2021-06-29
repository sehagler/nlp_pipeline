# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 15:49:43 2020

@author: haglers
"""

#
from nlp_lib.py.document_preprocessing_lib.base_class_lib.preprocessor_base_class \
    import Preprocessor_base
from tool_lib.py.processing_tools_lib.text_processing_tools \
    import class_label, part_label, specimen_label, s

#
class Specimen_normalizer(Preprocessor_base):
    
    #
    def _indicate_nonspecimens(self, mode_flg):
        if mode_flg == 'do':
            term_list = []
            term_list.append('class')
            for term in term_list:
                match_str = '(?i)' + term   + s() + ' ' + class_label()
                self._general_command(match_str, {term + s() + ' ' : 'class<HYPHEN>'})
            term_list = []
            term_list.append('part')
            for term in term_list:
                match_str = '(?i)' + term  + s() + ' ' + part_label()
                self._general_command(match_str, {term + s() + ' ' : 'part<HYPHEN>'})
        elif mode_flg == 'undo':
            term_list = []
            term_list.append('class')
            term_list.append('part')
            for term in term_list:
                match_str = '(?i)' + term + '<HYPHEN>'
                self._general_command(match_str, {term + '<HYPHEN>' : ' '})
                
    #
    def _remove_false_specimen(self):
        self._clear_command_list()
        self._general_command('(?i) \((([a-l]|[o-s]|[u-z])+[0-9]+(,( )?)?)+\)', {None : ''})
        self._process_command_list()
                
    #
    def process_specimens(self):
        #self._indicate_nonspecimens('do')
        self._general_command('(?i)[ \t][a-z]:[ \t]', {':' : '.'})
        self._general_command('(?i)[ \t][a-z]\.[ \t]', {'(?i)[ \t](?=[a-z])' : '\n\n'})
        #self._indicate_nonspecimens('undo')