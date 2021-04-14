# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 10:38:15 2020

@author: haglers
"""

#
import re

#
from nlp_lib.py.base_class_lib.preprocessor_base_class import Preprocessor_base

#
class Pretokenizer(Preprocessor_base):
        
    #
    def process_punctuation(self):
        self._general_command('(?i)(\n)[A-Z]:[ \t]', {':' : '.'})
        self._general_command('(\s)?\(\n', {None : '\n'})
        self._general_command('(?i)-grade', {None : ' grade'})
        self._general_command('(?i)-to-', {None : ' to '})
        self._general_command('(?i)in-situ', {None : 'in situ'})
        self._general_command('(?i)in-toto', {None : 'in toto'})
        self._general_command('____+(\n_+)*', {None : '' })