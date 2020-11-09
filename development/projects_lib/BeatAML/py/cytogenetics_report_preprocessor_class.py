# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 09:44:25 2018

@author: haglers
"""

#
from nlp_lib.py.processor_lib.preprocessor_lib.rewriters_lib.normalizers_lib.section_header_normalizer_pathology_report_class \
    import Section_header_normalizer_pathology_report
from nlp_lib.py.tool_lib.query_tools_lib.karyotype_tools import Posttokenizer as Posttokenizer_karyotype
from nlp_lib.py.template_lib.preprocessor_template_lib.cytogenetics_report_class import Cytogenetics_report

#
class Cytogenetics_report_preprocessor(Cytogenetics_report):
    
        #
    def _extract_section_headers(self):
        Cytogenetics_report._extract_section_headers(self)
        section_header_normalizer = Section_header_normalizer_pathology_report()
        section_header_normalizer.push_linguamatics_i2e_writer(self.linguamatics_i2e_writer)
        section_header_normalizer.push_text(self.text)
        section_header_normalizer.cytogenetic_analysis_summary_section_header('formatted')
        section_header_normalizer.fish_analysis_summary_section_header('formatted')
        section_header_normalizer.karyotype_section_header('formatted')
        self.text = section_header_normalizer.pull_text()
        self.linguamatics_i2e_writer = section_header_normalizer.pull_linguamatics_i2e_writer()
    
    #
    def _posttokenizer(self, clear_section_headers=True):
        Cytogenetics_report._posttokenizer(self)
        posttokenizer_karyotype = Posttokenizer_karyotype()
        posttokenizer_karyotype.push_text(self.text)
        posttokenizer_karyotype.process_karyotype()
        self.text = posttokenizer_karyotype.pull_text()
        #self._clear_command_list()
        #self._general_command('q[0-9\.]+\) ;', {' ;' : ';'}) 
        #self._process_command_list()
        if clear_section_headers:
            self._clear_section_header_tags()