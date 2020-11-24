# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 10:38:15 2020

@author: haglers
"""

#
from nlp_lib.py.base_class_lib.preprocessor_base_class import Preprocessor_base

#
class Posttokenizer(Preprocessor_base):
        
    #
    def process_general(self):
        self._general_command(' M [:/] E ', {None : ' M:E '})
        self._general_command(' N [:/] C ', {None : ' N:C '})
        self._general_command('(?i) n / a ', {None : ' n/a '})
        
    #
    def process_medical_abbreviations(self):
        self._general_command('(?i) f / u ', {None : ' f/u '})
        self._general_command('(?i) h / o ', {None : ' h/o '})
        self._general_command('(?i) s / p ', {None : ' s/p '})