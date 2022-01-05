# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 12:29:58 2021

@author: haglers
"""

#
from nlp_lib.py.base_lib.preprocessor_base_class \
    import Preprocessor_base
from tool_lib.py.processing_tools_lib.text_processing_tools \
    import article, be, note_label, s, specimen_label
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
        self._clear_command_list()
        self._general_command('(?i)[\n\s]+based on pathologic finding' + s(), {None : ''})
        self._general_command('(?i)(?<=Dr [A-Z])\.', {None : ''})
        self._general_command('(?i)my electronic signature.*' + article() + ' final diagnosis( \.)?', {None : ''})
        self._general_command('(?i)i have reviewed.*and final diagnosis( \.)?', {None : ''})
        self._general_command('(?i)inclu(des|sive of) all specimens', {None : ''})
        self._general_command('(?i)pathologist interpretation ' + be() + ' based on ' + article() + ' review.*representative hematoxylin and eosin stains( \.)?', {None : ''})
        self._general_command('(?i)' + article() + ' test ' + be() + ' developed.*FDA( \.)?', {None : ''})
        self._general_command('(?i)' + article() + ' clinical interpretation ' + be() + ' made by ' + article() + ' clinical geneticist( \.)?', {None : ''})
        self._process_command_list()
    
    #
    def _remove_mychart(self):
        self._clear_command_list()
        self._general_command('(?i)display progress note in mychart : (no|yes)', {None : ''})
        self._process_command_list()
        
    #
    def _remove_see(self):
        self._clear_command_list()
        self._general_command('(?i)(\n\s*)?\( (please )?see [^\n\)\]]* \)', {None : ''})
        self._general_command('(?i)\s*see\n', {None : '\n'})
        self._process_command_list()
        match_str = '(?i)((\n\s*)?-( )?)?(please[\n\s]+)?see[\n\s]+' + \
                    '(the )?(second )?(amendment|cancer|note|synoptic)?( )?' + \
                    '(below|comment|report|synops(e|i))' + s() + \
                    '( and synoptic summary)?( and tumor protocol)?' + \
                    '( below)?( for (additional|technical) (details|information))?( \.)?'
        self._substitution_endings_list(match_str)
        match_str = '(?i)((\n\s*)?-( )?)?(please[\n\s]+)?see ' + \
                    '(note|(staging )?summary|(cancer )?synopsis|synoptic report)' + \
                    '( below)?( for (additional|technical) details)?'
        self._substitution_endings_list(match_str)
        match_str = '(?i)((\n\s*)?-( )?)?(please[\n\s]+)?see (also )?' + \
                    'note' + s() + '( )?' + note_label() + '( to ' + note_label() + ')?'
        self._substitution_endings_list(match_str)
        match_str = '(?i)((\n\s*)?-( )?)?(please[\n\s]+)?see (also )?' + \
                    'specimen' + s() + '( )?' + specimen_label() + '( to ' + specimen_label() + ')?'
        self._substitution_endings_list(match_str)
        
    #
    def _substitution_endings_list(self, search_str):
        self._general_command(search_str + '\n', {None : '\n'})
        self._general_command(search_str + '\t', {None : '\t'})
        self._general_command(search_str + ' ', {None : ' '})
        self._general_command(search_str + ',', {None : ','})
        self._general_command(search_str + '\.', {None : '.'})
        self._general_command(search_str + ';', {None : ';'})
        self._general_command(search_str + '( )?-', {None : '-'})
    
    #
    def process_document(self, text):
        self.text = text
        self._normalize_whitespace()
        self.text = self.summarization_registry.run_registry(self.text)
        self._remove_extraneous_text()
        self._normalize_whitespace()
        return self.text