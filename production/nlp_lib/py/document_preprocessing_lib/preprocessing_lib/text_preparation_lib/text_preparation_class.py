# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 13:28:29 2020

@author: haglers
"""

#
from nlp_lib.py.document_preprocessing_lib.base_class_lib.preprocessor_base_class import Preprocessor_base

#
class Text_preparation(Preprocessor_base):
        
    #
    def correct_common_typos(self):
        self._general_command('(?i)adenomcarcinoa', {None : 'adenocarcinoma'})
        self._general_command('(?i)diagnosises', {None : 'diagnoses'})
        self._general_command('(?i)eddible', {None : 'edible'})
        self._general_command('(?i)florescen', {None : 'fluorescen'})
        self._general_command('(?i)pateint', {None : 'patient'})
        self._general_command('(?i)refrral', {None : 'referral'})
        self._general_command('(?i)repector', {None : 'receptor'})
        self._general_command('(?i)serous', {None : 'serious'})
        
    #
    def format_section_headers(self):
        self._general_command('(?i)progress note \d+/(\d+|\*+)/\d+', {'\d+/(\d+|\*+)/\d+' : ''})
        
    #
    def remove_extraneous_text(self):
        self._general_command('(?i)\(HCC\)', {None : ''})