# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 16:28:34 2018

@author: haglers
"""

#
import re

#
from nlp_lib.py.base_class_lib.template_base_class import Template_base
from nlp_lib.py.processor_lib.preprocessor_lib.rewriters_lib.normalizers_lib.label_normalizer_class \
    import Label_normalizer
from nlp_lib.py.processor_lib.preprocessor_lib.rewriters_lib.normalizers_lib.section_header_normalizer_pathology_report_class \
    import Section_header_normalizer_pathology_report
from nlp_lib.py.processor_lib.preprocessor_lib.rewriters_lib.normalizers_lib.specimen_normalizer_class \
    import Specimen_normalizer
from nlp_lib.py.processor_lib.preprocessor_lib.rewriters_lib.pretokenizers_lib.pretokenizer_class \
    import Pretokenizer

#
class Pathology_report(Template_base):
        
    #
    def _extract_section_headers(self):
        section_header_normalizer = Section_header_normalizer_pathology_report()
        self.linguamatics_i2e_writer.append_keywords_text(self.body_header)
        section_header_normalizer.push_linguamatics_i2e_writer(self.linguamatics_i2e_writer)
        section_header_normalizer.push_text(self.text)
        section_header_normalizer.amendment_section_header('formatted')
        section_header_normalizer.background_section_header('formatted')
        section_header_normalizer.comment_section_header('pull_out_section_header_to_bottom_of_report')
        section_header_normalizer.diagnosis_section_header('formatted')
        section_header_normalizer.explanation_section_header('formatted')
        section_header_normalizer.history_section_header('formatted')
        section_header_normalizer.impression_and_recommendation_section_header('formatted')
        section_header_normalizer.interpretation_section_header('formatted')
        section_header_normalizer.laboratory_data_section_header('formatted')
        section_header_normalizer.materials_received_section_header('formatted')
        section_header_normalizer.method_section_header('formatted')
        section_header_normalizer.person_section_header('formatted')
        section_header_normalizer.references_section_header('formatted')
        section_header_normalizer.synopsis_section_header('formatted')
        self.text = section_header_normalizer.pull_text()
        self.linguamatics_i2e_writer = section_header_normalizer.pull_linguamatics_i2e_writer()
        
    #
    def _pretokenizer(self):
        self._normalize_whitespace()
        pretokenizer = Pretokenizer()
        pretokenizer.push_text(self.text)
        pretokenizer.process_punctuation()
        self.text = pretokenizer.pull_text()
        specimen_normalizer = Specimen_normalizer()
        specimen_normalizer.push_text(self.text)
        specimen_normalizer.process_specimens()
        self.text = specimen_normalizer.pull_text()
        label_normalizer = Label_normalizer()
        label_normalizer.push_text(self.text)
        label_normalizer.process_labels()
        self.text = label_normalizer.pull_text()
        self._extract_section_headers()
        self._normalize_whitespace()
        
    #
    def normalize_report(self):
        self._make_text_ascii()
        self._deidentifier()
        self._text_setup()
        self._rewriter()
        self._named_entity_recognition()
        self._summarization()
        self._make_text_xml_compatible()