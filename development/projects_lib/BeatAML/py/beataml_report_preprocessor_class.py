# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 15:14:40 2020

@author: haglers
"""

#
from projects_lib.BeatAML.py.cytogenetics_report_preprocessor_class \
    import Cytogenetics_report_preprocessor
from projects_lib.BeatAML.py.hematopathology_report_preprocessor_class \
    import Hematopathology_report_preprocessor

#
class BeatAML_report_preprocessor(Cytogenetics_report_preprocessor, Hematopathology_report_preprocessor):
    
    #
    def __init__(self, project_data, formatting):
        Hematopathology_report_preprocessor.__init__(self, project_data, formatting)
        
    #
    def _extract_section_headers(self):
        Hematopathology_report_preprocessor._extract_section_headers(self)
        Cytogenetics_report_preprocessor._extract_section_headers(self)
        
    #
    def _format_beakerap(self):
        Hematopathology_report_preprocessor._format_beakerap(self)
        Cytogenetics_report_preprocessor._format_beakerap(self)
        
    #
    def _format_powerpath(self):
        Hematopathology_report_preprocessor._format_powerpath(self)
        Cytogenetics_report_preprocessor._format_powerpath(self)
        
    #
    def _named_entity_recognition(self):
        Hematopathology_report_preprocessor._named_entity_recognition(self)
        Cytogenetics_report_preprocessor._named_entity_recognition(self)
        
    #
    def _normalize_punctuation(self):
        Hematopathology_report_preprocessor._normalize_punctuation(self)
        Cytogenetics_report_preprocessor._normalize_punctuation(self)
        
    #
    def _normalize_table(self):
        Hematopathology_report_preprocessor._normalize_table(self)
        Cytogenetics_report_preprocessor._normalize_table(self)
        
    #
    def _normalize_terminology(self):
        Hematopathology_report_preprocessor._normalize_terminology(self)
        Cytogenetics_report_preprocessor._normalize_terminology(self)
        
    #
    def _normalize_tokenized_text(self):
        Hematopathology_report_preprocessor._normalize_tokenized_text(self)
        Cytogenetics_report_preprocessor._normalize_tokenized_text(self)
        
    #
    def _normalize_whitespace(self):
        Hematopathology_report_preprocessor._normalize_whitespace(self)
        Cytogenetics_report_preprocessor._normalize_whitespace(self)
        
   #
    def _remove_false_specimen(self):
        Hematopathology_report_preprocessor._remove_false_specimen(self)
        Cytogenetics_report_preprocessor._remove_false_specimen(self)
        
    #
    def _posttokenizer(self):
        Hematopathology_report_preprocessor._posttokenizer(self, clear_section_headers=False)
        Cytogenetics_report_preprocessor._posttokenizer(self)
        
    #
    def _pretokenizer(self):
        Hematopathology_report_preprocessor._pretokenizer(self)
        Cytogenetics_report_preprocessor._pretokenizer(self)
        
    #
    def _summarization(self):
        Hematopathology_report_preprocessor._summarization(self)
        Cytogenetics_report_preprocessor._summarization(self)
        
    #
    def _tokenizer(self):
        Hematopathology_report_preprocessor._tokenizer(self)
        Cytogenetics_report_preprocessor._tokenizer(self)