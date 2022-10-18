# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 12:58:14 2021

@author: haglers
"""

#
import re

#
from lambda_lib.lambda_manager_class import Lambda_manager
from nlp_text_normalization_lib.formatter_lib.normalizers_lib.section_header_normalizer_class \
    import Section_header_normalizer
from nlp_text_normalization_lib.formatter_lib.normalizers_lib.table_normalizer_class \
    import Table_normalizer

#
class Formatter(object):
    
    #
    def __init__(self, static_data):
        self.static_data = static_data
        self.lambda_manager = Lambda_manager()
        self.section_header_normalizer = \
            Section_header_normalizer(self.static_data)
        self.table_normalizer = Table_normalizer(self.static_data)
        self.report_text_header = 'REPORT TEXT'
        
    #
    def _add_report_text_header(self):
        self.text = self.report_text_header + '\n' + self.text
        self.text = \
            self.lambda_manager.lambda_conversion('^' + self.report_text_header + '\n' + self.report_text_header,
                                                  self.text, self.report_text_header + '\n')
        self.text = \
            self.lambda_manager.lambda_conversion('^' + self.report_text_header + '[\n\s]*',
                                                  self.text, self.report_text_header + '\n\n')
          
    #
    def _extract_section_headers(self):
        self.dynamic_data_manager.append_keywords_text(self.report_text_header, 0)
        self.section_header_normalizer.push_dynamic_data_manager(self.dynamic_data_manager)
        self.text = \
            self.section_header_normalizer.normalize_section_header(self.formatting,
                                                                    self.text)
        self.text = \
            self.section_header_normalizer.clear_section_header_tags(self.text)
        self.text = \
            self.section_header_normalizer.fix_section_headers(self.text)
        self.dynamic_memory_manager = \
            self.section_header_normalizer.pull_dynamic_data_manager()
            
    #
    def _insert_whitespace(self, match_str, whitespace):
        match = 0
        m_str = re.compile(match_str)
        while match is not None:
            match = m_str.search(self.text, re.IGNORECASE)
            if match is not None:
                self.text = self.text[:match.start()] + whitespace + \
                            self.text[match.start()+1:]
        
    #
    def _pull_out_section_header(self, command):
        self._insert_whitespace(command, '\n\n')
        
    #
    def _pull_out_table_entry(self, command):
        self._insert_whitespace(command, '\n')
        
    #
    def format_text(self, dynamic_data_manager, text, source_system, formatting):
        self.formatting = formatting
        self.dynamic_data_manager = dynamic_data_manager
        self.text = text
        self._pull_out_section_header('(?i)[ \t]case (reviewed|seen) by:?')
        self._pull_out_section_header('(?i)[ \t]clinical history')
        self._pull_out_section_header('(?i)[ \t]comment(s)?( )?(\([a-z0-9 ]*\))?:')
        self._pull_out_section_header('(?i)[ \t]note( )?(\([a-z0-9 ]*\))?:')
        self._add_report_text_header()
        self.text = \
            self.lambda_manager.lambda_conversion('(?<![0-9]) - (?![0-9])', self.text, '\n- ')
        self.text = \
            self.lambda_manager.lambda_conversion('\n +', self.text, '\n')
        self._pull_out_section_header('(?i)[ \t]antibodies tested')
        self._pull_out_section_header('(?i)[ \t]bone marrow aspirate smears')
        self._pull_out_section_header('(?i)[ \t]bone marrow (biopsy/)?clot section')
        self._pull_out_section_header('(?i)[ \t]bone marrow differential')
        self._pull_out_section_header('(?i)[ \t]cbc')
        self._pull_out_section_header('(?i)[ \t]component value')
        self._pull_out_section_header('(?i)[ \t]cytogenetic and fish studies')
        self._pull_out_section_header('(?i)[ \t]flow cytometric analysis')
        self._pull_out_section_header('(?i)[ \t]immunohistochemical stains:')
        self._pull_out_section_header('(?i)[ \t]immunologic analysis:')
        self._pull_out_section_header('(?i)[ \t]molecular studies:')
        self._pull_out_section_header('(?i)[ \t]peripheral blood differential')
        self._pull_out_section_header('(?i)[ \t]peripheral blood morphology')
        self._pull_out_section_header('(?i)[ \t]resulting agency')
        self._pull_out_section_header('(?i)[ \t]special stains')
        self.text = \
            self.table_normalizer.normalize_hematopathology_table(self.text)
        self.text = \
            self.lambda_manager.lambda_conversion('\nFinal Diagnosis\n', self.text, '\nFINAL DIAGNOSIS\n')
        self.text = \
            self.lambda_manager.lambda_conversion('\n(MANUAL|PERIPHERAL BLOOD) DIFFERENTIAL', self.text, '\n\nMANUAL DIFFERENTIAL')
        self.text = self.table_normalizer.process_text(self.text)
        self._extract_section_headers()
        return self.dynamic_data_manager, self.text