# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 09:24:59 2020

@author: haglers
"""

#
from nlp_lib.py.document_preprocessing_lib.base_class_lib.preprocessor_base_class \
    import Preprocessor_base
from tool_lib.py.processing_tools_lib.text_processing_tools \
    import note_label, part_label, specimen_label, s

#
class Label_normalizer(Preprocessor_base):
    
    #
    def process_labels(self):
        term_list = []
        term_list.append('note' + s())
        for term in term_list:
            self._general_command('(?i)' + term + ' #?' + note_label(), {' ' : '-'})
            self._general_command('(?i)' + term + '-#' + note_label(), {'#' : ''})
            self._general_command('(?i)' + term + '-' + note_label() + ' to', {' ' : '-'})
            self._general_command('(?i)' + term + '-' + note_label() + '-to #?' + note_label(), {' ' : '-'})
            self._general_command('(?i)' + term + '-' + note_label() + '-to-#' + note_label(), {'#' : ''})
        term_list = []
        term_list.append('part' + s())
        for term in term_list:
            self._general_command('(?i)' + term + ' #?' + part_label(), {' ' : '-'})
            self._general_command('(?i)' + term + '-#' + part_label(), {'#' : ''})
            self._general_command('(?i)' + term + '-' + part_label() + ' to', {' ' : '-'})
            self._general_command('(?i)' + term + '-' + part_label() + '-to #?' + part_label(), {' ' : '-'})
            self._general_command('(?i)' + term + '-' + part_label() + '-to-#' + part_label(), {'#' : ''})
        term_list = []
        term_list.append('specimen' + s())
        for term in term_list:
            self._general_command('(?i)' + term + ' #?' + specimen_label(), {' ' : '-'})
            self._general_command('(?i)' + term + '-#' + specimen_label(), {'#' : ''})
            self._general_command('(?i)' + term + '-' + specimen_label() + ' to', {' ' : '-'})
            self._general_command('(?i)' + term + '-' + specimen_label() + '-to #?' + specimen_label(), {' ' : '-'})
            self._general_command('(?i)' + term + '-' + specimen_label() + '-to-#' + specimen_label(), {'#' : ''})