# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 15:04:20 2020

@author: haglers
"""

#
from nlp_lib.py.base_lib.preprocessor_base_class \
    import Preprocessor_base

#
class Named_entity_recognition(Preprocessor_base):
    
    #
    def run_preprocessor(self):
        self._normalize_whitespace()
        self._normalize_regular_initialism('packs?( (/|per))? days?', 'PPD')
        self._normalize_regular_initialism(' ppd', ' PPD')
        self._normalize_regular_initialism('packs?( (/|per))? wks?', 'PPW')
        self._normalize_regular_initialism(' ppw', ' PPW')
        self._normalize_regular_initialism('packs?( (/|per))? yrs?', 'PPY')
        self._normalize_regular_initialism(' ppy', ' PPY')
        
#
class Summarization(Preprocessor_base):
    
    #
    def run_preprocessor(self):
        self._clear_command_list()
        self._general_command('(?i)check out the free oregon quit line(.*\n)*.*www . quitnow . net / oregon', {None : ''})
        self._process_command_list()