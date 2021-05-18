# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 09:44:25 2018

@author: haglers
"""

#
from nlp_lib.py.document_preprocessing_lib.base_class_lib.report_preprocessor_base_class \
    import Report_preprocessor_base_class
from nlp_lib.py.document_preprocessing_lib.preprocessing_lib.rewriters_lib.normalizers_lib.section_header_normalizer_class \
    import Section_header_normalizer
from tool_lib.py.query_tools_lib.karyotype_tools \
    import Posttokenizer as Posttokenizer_karyotype

#
class Cytogenetics_report_preprocessor(Report_preprocessor_base_class):
    
    #
    def _extract_section_headers(self):
        section_header_normalizer = Section_header_normalizer(self.project_data)
        self.dynamic_data_manager.append_keywords_text(self.body_header)
        section_header_normalizer.push_dynamic_data_manager(self.dynamic_data_manager)
        section_header_normalizer.push_text(self.text)
        section_header_normalizer.amendment_section_header(self.formatting)
        section_header_normalizer.comment_section_header('pull_out_section_header_to_bottom_of_report')
        section_header_normalizer.history_section_header(self.formatting)
        section_header_normalizer.person_section_header(self.formatting)
        section_header_list = \
            [ 'BACKGROUND', 'CYTOGENETIC ANALYSIS SUMMARY',
              'PREAMENDMENT DIAGNOSIS', 'DIAGNOSIS', 'EXPLANATION',
              'FISH ANALYSIS SUMMARY', 'IMPRESSION AND RECOMMENDATION',
              'INTERPRETATION', 'KARYOTYPE', 'LAB DATA', 'MATERIALS RECEIVED',
              'METHOD', 'REFERENCES', 'SYNOPSIS' ]
        section_header_normalizer.normalize_section_header(section_header_list,
                                                           self.formatting)
        self.text = section_header_normalizer.pull_text()
        self.dynamic_memory_manager = \
            section_header_normalizer.pull_dynamic_data_manager()
    
    #
    def _posttokenizer(self, clear_section_headers=True):
        Report_preprocessor_base_class._posttokenizer(self)
        posttokenizer_karyotype = Posttokenizer_karyotype(self.project_data)
        posttokenizer_karyotype.push_text(self.text)
        posttokenizer_karyotype.process_karyotype()
        self.text = posttokenizer_karyotype.pull_text()
        if clear_section_headers:
            self._clear_section_header_tags()