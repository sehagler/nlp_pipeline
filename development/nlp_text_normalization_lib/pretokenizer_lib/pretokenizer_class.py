# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 16:41:11 2021

@author: haglers
"""

#
from nlp_text_normalization_lib.base_lib.preprocessor_base_class \
    import Preprocessor_base
from nlp_text_normalization_lib.pretokenizer_lib.normalizers_lib.personal_name_normalizer_class \
    import Personal_name_normalizer
from nlp_text_normalization_lib.pretokenizer_lib.normalizers_lib.section_header_normalizer_class \
    import Section_header_normalizer
from nlp_text_normalization_lib.pretokenizer_lib.normalizers_lib.specimen_normalizer_class \
    import Specimen_normalizer
from nlp_text_normalization_lib.pretokenizer_lib.normalizers_lib.table_normalizer_class \
    import Table_normalizer
from tool_lib.py.query_tools_lib.cancer_tools \
    import Text_preparation as Text_preparation_cancer

#
class Pretokenizer(Preprocessor_base):
    
    #
    def __init__(self, static_data):
        Preprocessor_base.__init__(self, static_data)    
        self.body_header = 'SUMMARY'
        self.personal_name_normalizer = \
            Personal_name_normalizer(self.static_data)
        self.section_header_normalizer = \
            Section_header_normalizer(self.static_data)
        self.specimen_normalizer = Specimen_normalizer(self.static_data)
        self.table_normalizer = Table_normalizer(self.static_data)
        self.text_preparation_cancer = \
            Text_preparation_cancer(self.static_data)
        
    #
    def _extract_section_headers(self):
        self.dynamic_data_manager.append_keywords_text(self.body_header, 0)
        self.section_header_normalizer.push_dynamic_data_manager(self.dynamic_data_manager)
        self.section_header_normalizer.push_text(self.text)
        self.section_header_normalizer.comment_section_header('pull_out_section_header_to_bottom_of_report')
        self.section_header_normalizer.history_section_header(self.formatting)
        self.section_header_normalizer.normalize_section_header(self.formatting)
        self.section_header_normalizer.amendment_section_header(self.formatting)
        self.section_header_normalizer.clear_section_header_tags()
        self.section_header_normalizer.fix_section_headers()
        self.text = self.section_header_normalizer.pull_text()
        self.dynamic_memory_manager = \
            self.section_header_normalizer.pull_dynamic_data_manager()
            
    #
    def _format_section_headers(self):
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('progress note \d+/(\d+|\*+)/\d+', '\d+/(\d+|\*+)/\d+', self.text, '')
        
    #
    def _normalize_punctuation(self):
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('(\n)[A-Z]:[ \t]', ':', self.text, '.')
        self.text = \
            self.lambda_manager.lambda_conversion('(\s)?\(\n', self.text, '\n')
        self.text = \
            self.lambda_manager.lambda_conversion('-grade', self.text, ' grade')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)-to-', self.text, ' to ')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)in-situ', self.text, 'in situ')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)in-toto', self.text, 'in toto')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)intermediate to strong', self.text, 'intermediate-strong')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)moderate to strong', self.text, 'moderate-strong')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)moderate to weak', self.text, 'weak-moderate')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)over-expression', self.text, 'overexpression')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)strong to moderate', self.text, 'moderate-strong')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)weak to moderate', self.text, 'weak-moderate')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)weak to strong', self.text, 'weak-strong')
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('____+(\n_+)*', self.text)
        text_list = [ 'negative', 'positive']
        for text_str in text_list:
            regex_str = '(?i)(?<=' + text_str + ')\('
            self.text = \
                self.lambda_manager.lambda_conversion(regex_str, self.text, ' (')
    
    #
    def _remove_extraneous_text(self):
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?i)\(HCC\)', self.text)
    
    #
    def _text_setup(self):
        self._normalize_whitespace()
        self._format_section_headers()
        self._normalize_punctuation()
        self._remove_extraneous_text()
        self.text_preparation_cancer.push_text(self.text)
        self.text_preparation_cancer.normalize_text()
        self.text_preparation_cancer.setup_text()
        self.text = self.text_preparation_cancer.pull_text()
        self._normalize_whitespace()
        
    #
    def process_document(self, dynamic_data_manager, text):
        self.dynamic_data_manager = dynamic_data_manager
        self.text = text
        self._text_setup()
        self._normalize_whitespace()
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('(?i)(\n)[A-Z]\.[ \t]', '\.', self.text, ':')
        self.text = \
            self.lambda_manager.lambda_conversion('(\s)?\(\n', self.text, '\n')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)-grade', self.text, ' grade')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)-to-', self.text, ' to ')
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('____+(\n_+)*', self.text)
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)fine needle', self.text, 'fine-needle')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)in-situ', self.text, 'in situ')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)in-toto', self.text, 'in toto')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)over-expression', self.text, 'overexpression')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)margin\(s\)', self.text, 'margins')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)from (the )?nipple', self.text, 'fn')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)histologic grade', self.text, 'grade')
        self.text = self.personal_name_normalizer.process_text(self.text)
        self.text = self.table_normalizer.process_text(self.text)
        self.specimen_normalizer.push_text(self.text)
        self.specimen_normalizer.process_specimens()
        self.text = self.specimen_normalizer.pull_text()
        self._extract_section_headers()
        self._normalize_whitespace()
        return self.dynamic_data_manager, self.text
    
    #
    def set_formatting(self, formatting):
        self.formatting = formatting