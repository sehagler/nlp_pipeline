# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 12:29:58 2021

@author: haglers
"""

#
from nlp_text_normalization_lib.base_lib.preprocessor_base_class \
    import Preprocessor_base
from tool_lib.py.processing_tools_lib.text_processing_tools \
    import article, be, note_label, s, specimen_label, substitution_endings_list
from tool_lib.py.registry_lib.summarization_registry_class \
    import Summarization_registry

#
class Summarization(Preprocessor_base):
    
    #
    def __init__(self, static_data):
        Preprocessor_base.__init__(self, static_data)
        self.summarization_registry = Summarization_registry(self.static_data)
        self.summarization_registry.create_preprocessors()
   
    #
    def _remove_extraneous_text(self):
        self._remove_mychart()
        self._remove_see()
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('[\n\s]+based on pathologic finding' + s(), self.text)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?<=Dr [A-Z])\.', self.text)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('my electronic signature.*' + article() + ' final diagnosis( \.)?', self.text)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('i have reviewed.*and final diagnosis( \.)?', self.text)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?i)inclu(des|sive of) all specimens', self.text)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?i)pathologist interpretation ' + be() + ' based on ' + article() + ' review.*representative hematoxylin and eosin stains( \.)?', self.text)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?i)' + article() + ' test ' + be() + ' developed.*FDA( \.)?', self.text)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?i)' + article() + ' clinical interpretation ' + be() + ' made by ' + article() + ' clinical geneticist( \.)?', self.text)
    
    #
    def _remove_mychart(self):
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('display progress note in mychart : (no|yes)', self.text)
        
    #
    def _remove_see(self):
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?i)(\n\s*)?\( (please )?see [^\n\)\]]* \)', self.text)
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)\s*see\n', self.text, '\n')
        match_str = '(?i)((\n\s*)?-( )?)?(please[\n\s]+)?see[\n\s]+' + \
                    '(the )?(second )?(amendment|cancer|note|synoptic)?( )?' + \
                    '(below|comment|report|synops(e|i))' + s() + \
                    '( and synoptic summary)?( and tumor protocol)?' + \
                    '( below)?( for (additional|technical) (details|information))?( \.)?'
        self.text = substitution_endings_list(self.text, match_str)
        match_str = '(?i)((\n\s*)?-( )?)?(please[\n\s]+)?see ' + \
                    '(note|(staging )?summary|(cancer )?synopsis|synoptic report)' + \
                    '( below)?( for (additional|technical) details)?'
        self.text = substitution_endings_list(self.text, match_str)
        match_str = '(?i)((\n\s*)?-( )?)?(please[\n\s]+)?see (also )?' + \
                    'note' + s() + '( )?' + note_label() + '( to ' + note_label() + ')?'
        self.text = substitution_endings_list(self.text, match_str)
        match_str = '(?i)((\n\s*)?-( )?)?(please[\n\s]+)?see (also )?' + \
                    'specimen' + s() + '( )?' + specimen_label() + '( to ' + specimen_label() + ')?'
        self.text = substitution_endings_list(self.text, match_str)
        
    '''
    #
    def _substitution_endings_list(self, search_str):
        self.text = \
            self.lambda_manager.lambda_conversion(search_str + '\n', self.text, '\n')
        self.text = \
            self.lambda_manager.lambda_conversion(search_str + '\t', self.text, '\t')
        self.text = \
            self.lambda_manager.lambda_conversion(search_str + ' ', self.text, ' ')
        self.text = \
            self.lambda_manager.lambda_conversion(search_str + ',', self.text, ',')
        self.text = \
            self.lambda_manager.lambda_conversion(search_str + '\.', self.text, '.')
        self.text = \
            self.lambda_manager.lambda_conversion(search_str + ';', self.text, ';')
        self.text = \
            self.lambda_manager.lambda_conversion(search_str + '( )?-', self.text, '-')
    '''
    
    #
    def process_document(self, text):
        self.text = text
        self._normalize_whitespace()
        self.text = self.summarization_registry.run_registry(self.text)
        self._remove_extraneous_text()
        self._normalize_whitespace()
        return self.text