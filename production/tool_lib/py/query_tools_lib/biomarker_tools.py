# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 12:50:00 2020

@author: haglers
"""

#
from nlp_lib.py.document_preprocessing_lib.base_class_lib.preprocessor_base_class import Preprocessor_base
from tool_lib.py.processing_tools_lib.text_processing_tools import s

#
class Named_entity_recognition(Preprocessor_base):
    
    #
    def process_biomarkers(self):
        self._general_command('(?i)estrogen and progesterone( receptor' + s() + ')?',
                              {None : 'ER and PR'})
        self._general_command('(?i)progesterone and estrogen( receptor' + s() + ')?',
                              {None : 'PR and ER'})
        self._general_command('(?i)estrogen receptor( \( ER( , clone [A-Z0-9]+)? \))?', {None : 'ER'})
        self._general_command('(?i)HER(-| / )?2(( | / )?neu)?( \( cerb2 \))?', {None : 'HER2'})
        self._general_command('(?i)progesterone receptor( \( PR( , clone [A-Z0-9]+)? \))?', {None : 'PR'})

#
class Summarization(Preprocessor_base):
    
    #
    def _receptor_predicate(self):
        return('(ampification|antigen|clone|(over)?expression|immunoreactivity|protein|receptor|status)')
        
    #
    def process_estrogen_receptor(self):
        self._general_command('(?i)\nERs', {None : '\nER'})
        self._general_command('(?i)\sERs', {None : ' ER'})
        self._general_command('(?i)ER SP1', {None : 'ER'})
        self._general_command('[\n\s]+ER-', {None : ' ER '})
        search_str = 'ER ' + self._receptor_predicate() + s()
        for _ in range(3):
            self._general_command('(?i)\n' + search_str, {None : '\nER'})
            self._general_command('(?i)\s' + search_str, {None : ' ER'})
            self._general_command('(?i)' + search_str, {None : 'ER'})
        search_str = 'ER,? ' + self._receptor_predicate() + s() + ' [a-zA-Z0-9]*'
        for _ in range(2):
            self._general_command('(?i)[\n\s]+\( ' + search_str + ' \)', {None : ''})
            self._general_command('(?i)[\n\s]+' + search_str, {None : ''})
        self._general_command('(?i)\nER( :)?( )?-', {None : '\nER negative'})
        self._general_command('(?i)\sER( :)?( )?-', {None : ' ER negative'})
        self._general_command('(?i)\nER( :)?( )?\+', {None : '\nER positive'})
        self._general_command('(?i)\sER( :)?( )?\+', {None : ' ER positive'})
        
    #
    def process_her2(self):
        self._general_command('(?i)HER2( :)?( )?-', {None : 'HER2 negative'})
        self._general_command('(?i)HER2( :)?( )?\+', {None : 'HER2 positive'})
        for _ in range(7):
            search_str = '(?i)HER2 ([a-z]* for )?' + \
                         self._receptor_predicate() + s()
            self._general_command(search_str, {None : 'HER2'})
        for _ in range(7):
            search_str = self._receptor_predicate() + s() + '\s' + 'for HER2'
            self._general_command(search_str, {None : 'for HER2'})
        self._general_command('(?i)' + self._receptor_predicate() + ' of HER2', {None : 'HER2'})
        self._general_command('(?i)HER2 ' + self._receptor_predicate(), {None : 'HER2'})
        
    #
    def process_progesterone_receptor(self):
        self._general_command('(?i)\nPRs', {None : '\nPR'})
        self._general_command('(?i)\sPRs', {None : ' PR'})
        self._general_command('(?i)PR IE2', {None : 'PR'})
        self._general_command('[\n\s]+PR-', {None : ' PR '})
        search_str = 'PR ' + self._receptor_predicate() + s()
        for _ in range(3):
            self._general_command('(?i)\n' + search_str, {None : '\nPR'})
            self._general_command('(?i)\s' + search_str, {None : ' PR'})
            self._general_command('(?i)' + search_str, {None : 'PR'})
        search_str = 'PR,? ' + self._receptor_predicate() + s() + ' [a-zA-Z0-9]*'
        for _ in range(2):
            self._general_command('(?i)[\n\s]+\( ' + search_str + ' \)', {None : ''})
            self._general_command('(?i)[\n\s]+' + search_str, {None : ''})
        self._general_command('(?i)\nPR( :)?( )?-', {None : '\nPR negative'})
        self._general_command('(?i)\sPR( :)?( )?-', {None : ' PR negative'})
        self._general_command('(?i)\nPR( :)?( )?\+', {None : '\nPR positive'})
        self._general_command('(?i)\sPR( :)?( )?\+', {None : ' PR positive'})