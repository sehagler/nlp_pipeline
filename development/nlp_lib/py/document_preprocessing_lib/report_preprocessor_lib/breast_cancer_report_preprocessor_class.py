# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 09:19:40 2018
@author: haglers

"""

#
from nlp_lib.py.document_preprocessing_lib.base_class_lib.report_preprocessor_base_class \
    import Report_preprocessor_base_class
from nlp_lib.py.document_preprocessing_lib.preprocessing_lib.rewriters_lib.normalizers_lib.section_header_normalizer_class \
    import Section_header_normalizer
from nlp_lib.py.document_preprocessing_lib.preprocessing_lib.rewriters_lib.pretokenizers_lib.pretokenizer_class \
    import Pretokenizer
from tool_lib.py.query_tools_lib.biomarker_tools \
    import Named_entity_recognition as Named_entity_recognition_biomarkers
from tool_lib.py.query_tools_lib.biomarker_tools \
    import Summarization as Summarization_biomarkers
from tool_lib.py.query_tools_lib.cancer_tools \
    import Named_entity_recognition as Named_entity_recognition_cancer
from tool_lib.py.query_tools_lib.cancer_tools \
    import Posttokenizer as Posttokenizer_cancer
from tool_lib.py.query_tools_lib.cancer_tools \
    import Text_preparation as Text_preparation_cancer
from tool_lib.py.query_tools_lib.histological_grade_tools \
    import Named_entity_recognition as Named_entity_recognition_histological_grade
from tool_lib.py.query_tools_lib.histological_grade_tools \
    import Posttokenizer as Posttokenizer_histological_grade
from tool_lib.py.query_tools_lib.histological_grade_tools \
    import Summarization as Summarization_histological_grade

#
class Breast_cancer_report_preprocessor(Report_preprocessor_base_class):
        
    #
    def _extract_section_headers(self, extract_section_headers_flg=True):
        section_header_normalizer = Section_header_normalizer(self.project_data)
        self.dynamic_data_manager.append_keywords_text(self.body_header)
        section_header_normalizer.push_dynamic_data_manager(self.dynamic_data_manager)
        section_header_normalizer.push_text(self.text)
        section_header_normalizer.amendment_section_header(self.formatting)
        section_header_normalizer.comment_section_header('pull_out_section_header_to_bottom_of_report')
        section_header_normalizer.history_section_header(self.formatting)
        section_header_normalizer.person_section_header(self.formatting)
        section_header_list = \
            [ 'BACKGROUND', 'PREAMENDMENT DIAGNOSIS', 'DIAGNOSIS',
              'EXPLANATION', 'IMPRESSION AND RECOMMENDATION', 'INTERPRETATION',
              'LAB DATA', 'MATERIALS RECEIVED', 'METHOD', 'REFERENCES',
              'SURGICAL PATHOLOGY SUMMARY', 'SYNOPSIS' ]
        section_header_normalizer.normalize_section_header(section_header_list,
                                                           self.formatting)
        self.text = section_header_normalizer.pull_text()
        self.dynamic_memory_manager = \
            section_header_normalizer.pull_dynamic_data_manager()
    
    #
    def _named_entity_recognition(self):
        Report_preprocessor_base_class._named_entity_recognition(self)
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
    def _normalize_punctuation(self):
        Report_preprocessor_base_class._normalize_punctuation(self)
        self._clear_command_list()
        self._general_command('(?i)fine needle', {None : 'fine-needle'})
        self._general_command('(?i)over-expression', {None : 'overexpression'})
        self._process_command_list()
    
    #
    def _normalize_terminology(self):
        Report_preprocessor_base_class._normalize_terminology(self)
        pretokenizer = Pretokenizer(self.project_data)
        pretokenizer.push_text(self.text)
        pretokenizer.process_initialisms()
        self.text = pretokenizer.pull_text()
        self._clear_command_list()
        self._general_command('(?i)margin\(s\)', {None : 'margins'})
        self._general_command('(?i)from (the )?nipple', {None : 'fn'})
        self._general_command('(?i)histologic grade', {None : 'grade'})
        self._process_command_list()
        
    #
    def _posttokenizer(self, clear_section_headers=True):
        Report_preprocessor_base_class._posttokenizer(self)
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
        Report_preprocessor_base_class._summarization(self)
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