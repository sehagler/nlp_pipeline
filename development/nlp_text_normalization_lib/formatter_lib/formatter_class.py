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
    def format_text(self, dynamic_data_manager, text, source_system):
        self.dynamic_data_manager = dynamic_data_manager
        self.text = text
        self._add_report_text_header()
        
        self.dynamic_data_manager.append_keywords_text(self.report_text_header, 0)
        self.text = self.section_header_normalizer.pull_out_section_headers(self.text)
        self.section_header_normalizer.push_dynamic_data_manager(self.dynamic_data_manager)
        self.text = \
            self.section_header_normalizer.normalize_section_header(self.text)
        self.text = \
            self.section_header_normalizer.clear_section_header_tags(self.text)
        self.dynamic_memory_manager = \
            self.section_header_normalizer.pull_dynamic_data_manager()
        
        self.text = \
            self.table_normalizer.normalize_hematopathology_table(self.text)
        self.text = self.table_normalizer.process_text(self.text)
        
        return self.dynamic_data_manager, self.text