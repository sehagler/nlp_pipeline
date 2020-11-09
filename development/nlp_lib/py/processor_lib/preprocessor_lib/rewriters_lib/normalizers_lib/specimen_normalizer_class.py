# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 15:49:43 2020

@author: haglers
"""

#
from nlp_lib.py.base_class_lib.preprocessor_base_class import Preprocessor_base
from nlp_lib.py.tool_lib.processing_tools_lib.text_processing_tools \
    import class_label, part_label, specimen_label, s

#
class Specimen_normalizer(Preprocessor_base):
    
    #
    def _indicate_nonspecimens(self, mode_flg):
        if mode_flg == 'do':
            term_list = []
            term_list.append('class' + s())
            for term in term_list:
                match_str = '(?i)' + term + ' ' + class_label()
                self._general_command(match_str, {term + ' ' : term + '<HYPHEN>'})
            term_list = []
            term_list.append('part' + s())
            for term in term_list:
                match_str = '(?i)' + term + ' ' + part_label()
                self._general_command(match_str, {term + ' ' : term + '<HYPHEN>'})
        elif mode_flg == 'undo':
            term_list = []
            term_list.append('class' + s())
            term_list.append('part' + s())
            for term in term_list:
                match_str = '(?i)' + term + '<HYPHEN>'
                self._general_command(match_str, {term + '<HYPHEN>': ' '})
                
    #
    def process_specimens(self):
        self._indicate_nonspecimens('do')
        self._clear_command_list()
        self._general_command('(?i)[ \t][a-z]:[ \t]', {':' : '.'})
        self._general_command('(?i)[ \t][a-z]\.[ \t]', {'(?i)[ \t](?=[a-z])' : '\n\n'})
        self._process_command_list()
        self._indicate_nonspecimens('undo')