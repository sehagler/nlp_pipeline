# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 17:43:29 2020

@author: haglers
"""

#
import re

#
from nlp_lib.py.document_preprocessing_lib.base_class_lib.report_preprocessor_base_class \
    import Report_preprocessor_base_class
from nlp_lib.py.document_preprocessing_lib.preprocessing_lib.rewriters_lib.pretokenizers_lib.pretokenizer_class \
    import Pretokenizer
from nlp_lib.py.document_preprocessing_lib.preprocessing_lib.rewriters_lib.normalizers_lib.section_header_normalizer_class \
    import Section_header_normalizer

#
class Note_preprocessor(Report_preprocessor_base_class):
    
    #
    def _extract_section_headers(self):
        section_header_normalizer = Section_header_normalizer(self.project_data)
        self.dynamic_data_manager.append_keywords_text(self.body_header)
        section_header_normalizer.push_dynamic_data_manager(self.dynamic_data_manager)
        section_header_normalizer.push_text(self.text)
        section_header_normalizer.history_section_header(self.formatting)
        section_header_normalizer.person_section_header(self.formatting)
        section_header_list = [ 'DATETIME' ]
        section_header_normalizer.general_command(section_header_list,
                                                  self.formatting)
        section_header_list = \
            [ 'ALLERGIES', 'ASSESSMENT', 'DIAGNOSIS', 'EVALUATION', 'GOALS',
              'HOSPITAL COURSE', 'ICD-9', 'IMPRESSION AND RECOMMENDATION',
              'INSURANCE', 'INTERVENTION', 'LAB DATA AND MEDICATION', 
              'MEDICATION', 'LAB DATA', 'OBJECTIVE', 'OTHER', 'REASON',
              'SERVICE', 'SUBJECTIVE', 'TECHNIQUE', 'TWENTY-FOUR HOUR EVENTS' ]
        section_header_normalizer.normalize_section_header(section_header_list,
                                                           self.formatting)
        self.text = section_header_normalizer.pull_text()
        self.dynamic_memory_manager = \
            section_header_normalizer.pull_dynamic_data_manager()