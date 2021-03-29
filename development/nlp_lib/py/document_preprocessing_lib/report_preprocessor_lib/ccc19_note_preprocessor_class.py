# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 17:43:29 2020

@author: haglers
"""

#
from nlp_lib.py.document_preprocessing_lib.template_lib.preprocessor_template_lib.note_template_class \
    import Note_template
from nlp_lib.py.tool_lib.query_tools_lib.biomarker_tools \
    import Named_entity_recognition as Named_entity_recognition_biomarkers
from nlp_lib.py.tool_lib.query_tools_lib.biomarker_tools \
    import Summarization as Summarization_biomarkers
from nlp_lib.py.tool_lib.query_tools_lib.cancer_tools \
    import Named_entity_recognition as Named_entity_recognition_cancer
from nlp_lib.py.tool_lib.query_tools_lib.cancer_tools \
    import Posttokenizer as Posttokenizer_cancer
from nlp_lib.py.tool_lib.query_tools_lib.cancer_tools \
    import Text_preparation as Text_preparation_cancer
from nlp_lib.py.tool_lib.query_tools_lib.histological_grade_tools \
    import Named_entity_recognition as Named_entity_recognition_histological_grade
from nlp_lib.py.tool_lib.query_tools_lib.histological_grade_tools \
    import Posttokenizer as Posttokenizer_histological_grade
from nlp_lib.py.tool_lib.query_tools_lib.histological_grade_tools \
    import Summarization as Summarization_histological_grade

#
class CCC19_note_preprocessor(Note_template):
    
    #
    def _named_entity_recognition(self):
        Note_template._named_entity_recognition(self)
        self._normalize_whitespace()
        named_entity_recognition_biomarkers = Named_entity_recognition_biomarkers(self.project_data)
        named_entity_recognition_biomarkers.push_text(self.text)
        named_entity_recognition_biomarkers.process_biomarkers()
        self.text = named_entity_recognition_biomarkers.pull_text()
        named_entity_recognition_cancer = Named_entity_recognition_cancer(self.project_data)
        named_entity_recognition_cancer.push_text(self.text)
        named_entity_recognition_cancer.process_abbreviations()
        named_entity_recognition_cancer.process_initialisms()
        self.text = named_entity_recognition_cancer.pull_text()
        named_entity_recognition_histological_grade = Named_entity_recognition_histological_grade(self.project_data)
        named_entity_recognition_histological_grade.push_text(self.text)
        named_entity_recognition_histological_grade.process_msbr()
        self.text = named_entity_recognition_histological_grade.pull_text()
        self._normalize_whitespace()
    
    #
    def _posttokenizer(self, clear_section_headers=True):
        Note_template._posttokenizer(self)
        posttokenizer_cancer = Posttokenizer_cancer(self.project_data)
        posttokenizer_cancer.push_text(self.text)
        posttokenizer_cancer.process_general()
        self.text = posttokenizer_cancer.pull_text()
        posttokenizer_histological_grade = Posttokenizer_histological_grade(self.project_data)
        posttokenizer_histological_grade.push_text(self.text)
        posttokenizer_histological_grade.process_grade()
        self.text = posttokenizer_histological_grade.pull_text()
        if clear_section_headers:
            self._clear_section_header_tags()
            
    #
    def _summarization(self):
        Note_template._summarization(self)
        self._normalize_whitespace()
        summarization_biomarkers = Summarization_biomarkers(self.project_data)
        summarization_biomarkers.push_text(self.text)
        summarization_biomarkers.process_estrogen_receptor()
        summarization_biomarkers.process_her2()
        summarization_biomarkers.process_progesterone_receptor()
        self.text = summarization_biomarkers.pull_text()
        summarization_histological_grade = Summarization_histological_grade(self.project_data)
        summarization_histological_grade.push_text(self.text)
        summarization_histological_grade.process_mitotic_rate()
        summarization_histological_grade.process_nuclear_pleomorphism()
        summarization_histological_grade.process_tubule_formation()
        self.text = summarization_histological_grade.pull_text()
        self._normalize_whitespace()
            
    #
    def _text_cleanup(self):
        self._normalize_whitespace()
        text_preparation = Text_preparation_cancer(self.project_data)
        text_preparation.push_text(self.text)
        text_preparation.cleanup_text()
        self.text = text_preparation.pull_text()
        self._normalize_whitespace()
        
    #
    def _text_setup(self):
        Note_template._text_setup(self)
        self._normalize_whitespace()
        text_preparation = Text_preparation_cancer(self.project_data)
        text_preparation.push_text(self.text)
        text_preparation.normalize_text()
        text_preparation.setup_text()
        self.text = text_preparation.pull_text()
        self._normalize_whitespace()
        
    #
    def normalize_report(self):
        Note_template.normalize_report(self)
        self._text_cleanup()