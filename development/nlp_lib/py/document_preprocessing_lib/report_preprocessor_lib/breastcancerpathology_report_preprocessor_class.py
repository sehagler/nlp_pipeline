# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 09:19:40 2018
@author: haglers

"""

#
from nlp_lib.py.document_preprocessing_lib.preprocessing_lib.rewriters_lib.normalizers_lib.section_header_normalizer_pathology_report_class \
    import Section_header_normalizer_pathology_report
from nlp_lib.py.document_preprocessing_lib.preprocessing_lib.rewriters_lib.pretokenizers_lib.pretokenizer_class \
    import Pretokenizer
from nlp_lib.py.document_preprocessing_lib.template_lib.preprocessor_template_lib.pathology_report_class \
    import Pathology_report
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
class BreastCancerPathology_report_preprocessor(Pathology_report):
        
 #
    def _extract_section_headers(self, extract_section_headers_flg=True):
        if extract_section_headers_flg:
            Pathology_report._extract_section_headers(self)
        section_header_normalizer = Section_header_normalizer_pathology_report(self.project_data)
        section_header_normalizer.push_dynamic_data_manager(self.dynamic_data_manager)
        section_header_normalizer.push_text(self.text)
        section_header_normalizer.surgical_pathology_summary_section_header('formatted')
        self.text = section_header_normalizer.pull_text()
        self.dynamic_data_manager = section_header_normalizer.pull_dynamic_data_manager()
        
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
    def _normalize_table(self):
        pass
    
    #
    def _normalize_punctuation(self):
        Pathology_report._normalize_punctuation(self)
        self._clear_command_list()
        self._general_command('(?i)fine needle', {None : 'fine-needle'})
        self._general_command('(?i)over-expression', {None : 'overexpression'})
        self._process_command_list()
    
    #
    def _normalize_terminology(self):
        Pathology_report._normalize_terminology(self)
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
    def _normalize_whitespace(self):
        Pathology_report._normalize_whitespace(self)
        
    #
    def _posttokenizer(self, clear_section_headers=True):
        Pathology_report._posttokenizer(self)
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
    def _pretokenizer(self):
        Pathology_report._pretokenizer(self)
        
    #
    def _summarization(self):
        Pathology_report._summarization(self)
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
    def _remove_false_specimen(self):
        self._clear_command_list()
        self._general_command('(?i) \((([a-l]|[o-s]|[u-z])+[0-9]+(,( )?)?)+\)', {None : ''})
        self._process_command_list()
        
    #
    def _rewriter(self):
        Pathology_report._rewriter(self)
        
    #
    def _tokenizer(self):
        Pathology_report._tokenizer(self)
        self._normalize_whitespace()