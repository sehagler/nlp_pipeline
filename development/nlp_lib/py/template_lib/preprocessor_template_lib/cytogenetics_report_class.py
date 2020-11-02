# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 09:44:25 2018

@author: haglers
"""

#
import re

#
from nlp_lib.py.template_lib.preprocessor_template_lib.pathology_report_class import Pathology_report
from nlp_lib.py.tool_lib.query_tools_lib.karyotype_tools import Named_entity_recognition as Named_entity_recognition_karyotype

#
class Cytogenetics_report(Pathology_report):
    
    #
    def __init__(self):
        Pathology_report.__init__(self)
        self.body_header = 'SUMMARY'
        
    #
    def _add_body_header(self):
        self.text = self.body_header + '\n' + self.text
        self.text = re.sub('^' + self.body_header + '\n' + self.body_header,
                           self.body_header + '\n', self.text)
        self.text = re.sub('^' + self.body_header + '[\n\s]*',
                           self.body_header + '\n\n', self.text)
        
    #
    def _extract_section_headers(self):
        Pathology_report._extract_section_headers(self)
        
    #
    def _format_beakerap(self):
        Pathology_report._format_beakerap(self)
        
    #
    def _format_powerpath(self):
        Pathology_report._format_powerpath(self)
        
    #
    def _format_section_headers(self):
        pass
    
    #
    def _named_entity_recognition(self):
        Pathology_report._named_entity_recognition(self)
        named_entity_recognition_karyotype = Named_entity_recognition_karyotype()
        named_entity_recognition_karyotype.push_text(self.text)
        named_entity_recognition_karyotype.process_karyotype()
        self.text = named_entity_recognition_karyotype.pull_text()
        self._normalize_whitespace()
        
    #
    def _normalize_punctuation(self):
        Pathology_report._normalize_punctuation(self)
        
    #
    def _normalize_table(self):
        pass
        
    #
    def _normalize_terminology(self):
        Pathology_report._normalize_terminology(self)
        
    #
    def _normalize_whitespace(self):
        Pathology_report._normalize_whitespace(self)
        
    #
    def _posttokenizer(self):
        Pathology_report._posttokenizer(self)
        
    #
    def _pretokenizer(self):
        Pathology_report._pretokenizer(self)
        
    #
    def _remove_false_specimen(self):
        pass
    
    #
    def _summarization(self):
        Pathology_report._summarization(self)
        
    #
    def _text_setup(self):
        Pathology_report._text_setup(self)
    
    #
    def _tokenizer(self):
        Pathology_report._tokenizer(self)
        
    #
    def _rewriter(self):
        Pathology_report._rewriter(self)
