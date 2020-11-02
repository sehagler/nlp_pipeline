# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 10:38:15 2020

@author: haglers
"""

#
import re

#
from nlp_lib.py.base_class_lib.preprocessor_base_class import Preprocessor_base
from nlp_lib.py.tool_lib.processing_tools_lib.text_processing_tools import note_label, part_label, specimen_label, s

#
class Pretokenizer(Preprocessor_base):
    
    #
    def _class_label(self):
        return('[A-Z0-9]{1}')
    
    #
    def _indicate_nonspecimens(self, mode_flg):
        if mode_flg == 'do':
            term_list = []
            term_list.append('class' + s())
            for term in term_list:
                match_str = '(?i)' + term + ' ' + self._class_label()
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
    def process_labels(self):
        term_list = []
        term_list.append('note' + s())
        self._clear_command_list()
        for term in term_list:
            self._general_command('(?i)' + term + ' #?' + note_label(), {' ' : '-'})
            self._general_command('(?i)' + term + '-#' + note_label(), {'#' : ''})
            self._general_command('(?i)' + term + '-' + note_label() + ' to', {' ' : '-'})
            self._general_command('(?i)' + term + '-' + note_label() + '-to #?' + note_label(), {' ' : '-'})
            self._general_command('(?i)' + term + '-' + note_label() + '-to-#' + note_label(), {'#' : ''})
        self._process_command_list()
        term_list = []
        term_list.append('part' + s())
        self._clear_command_list()
        for term in term_list:
            self._general_command('(?i)' + term + ' #?' + part_label(), {' ' : '-'})
            self._general_command('(?i)' + term + '-#' + part_label(), {'#' : ''})
            self._general_command('(?i)' + term + '-' + part_label() + ' to', {' ' : '-'})
            self._general_command('(?i)' + term + '-' + part_label() + '-to #?' + part_label(), {' ' : '-'})
            self._general_command('(?i)' + term + '-' + part_label() + '-to-#' + part_label(), {'#' : ''})
        self._process_command_list()
        term_list = []
        term_list.append('specimen' + s())
        self._clear_command_list()
        for term in term_list:
            self._general_command('(?i)' + term + ' #?' + specimen_label(), {' ' : '-'})
            self._general_command('(?i)' + term + '-#' + specimen_label(), {'#' : ''})
            self._general_command('(?i)' + term + '-' + specimen_label() + ' to', {' ' : '-'})
            self._general_command('(?i)' + term + '-' + specimen_label() + '-to #?' + specimen_label(), {' ' : '-'})
            self._general_command('(?i)' + term + '-' + specimen_label() + '-to-#' + specimen_label(), {'#' : ''})
        self._process_command_list()
        
    #
    def process_punctuation(self):
        self._clear_command_list()
        self._general_command('(?i)(\n)[A-Z]:[ \t]', {':' : '.'})
        self._general_command('(\s)?\(\n', {None : '\n'})
        self._general_command('(?i)-grade', {None : ' grade'})
        self._general_command('(?i)-to-', {None : ' to '})
        self._general_command('(?i)in-situ', {None : 'in situ'})
        self._general_command('(?i)in-toto', {None : 'in toto'})
        self._general_command('____+(\n_+)*', {None : '' })
        self._process_command_list()
        
    #
    def process_specimens(self):
        self._indicate_nonspecimens('do')
        self._clear_command_list()
        self._general_command('(?i)[ \t][a-z]:[ \t]', {':' : '.'})
        self._general_command('(?i)[ \t][a-z]\.[ \t]', {'(?i)[ \t](?=[a-z])' : '\n\n'})
        self._process_command_list()
        self._indicate_nonspecimens('undo')