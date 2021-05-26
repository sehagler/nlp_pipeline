# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 16:28:34 2018

@author: haglers
"""

#
import re

#
from nlp_lib.py.document_preprocessing_lib.base_class_lib.preprocessor_base_class \
    import Preprocessor_base
from nlp_lib.py.document_preprocessing_lib.preprocessing_lib.deidentifier_lib.deidentifier_class \
    import Deidentifier
from nlp_lib.py.document_preprocessing_lib.preprocessing_lib.named_entity_recognition_lib.named_entity_recognition_class \
    import Named_entity_recognition
from nlp_lib.py.document_preprocessing_lib.preprocessing_lib.rewriters_lib.normalizers_lib.label_normalizer_class \
    import Label_normalizer
from nlp_lib.py.document_preprocessing_lib.preprocessing_lib.rewriters_lib.normalizers_lib.specimen_normalizer_class \
    import Specimen_normalizer
from nlp_lib.py.document_preprocessing_lib.preprocessing_lib.rewriters_lib.normalizers_lib.table_normalizer_class \
    import Table_normalizer
from nlp_lib.py.document_preprocessing_lib.preprocessing_lib.rewriters_lib.posttokenizers_lib.posttokenizer_class \
    import Posttokenizer
from nlp_lib.py.document_preprocessing_lib.preprocessing_lib.rewriters_lib.pretokenizers_lib.pretokenizer_class \
    import Pretokenizer
from nlp_lib.py.document_preprocessing_lib.preprocessing_lib.rewriters_lib.tokenizers_lib.tokenizer_class \
    import Tokenizer
from nlp_lib.py.document_preprocessing_lib.preprocessing_lib.summarization_lib.summarization_class \
    import Summarization
from nlp_lib.py.document_preprocessing_lib.preprocessing_lib.text_preparation_lib.text_preparation_class \
    import Text_preparation
from tool_lib.py.query_tools_lib.date_tools \
    import Tokenizer as Tokenizer_date

#
class Report_preprocessor_base_class(Preprocessor_base):
    
    #
    def __init__(self, project_data, formatting):
        Preprocessor_base.__init__(self, project_data)
        self.body_header = 'SUMMARY'
        self.formatting = formatting
        
    #
    def _add_body_header(self):
        self.text = self.body_header + '\n' + self.text
        self.text = re.sub('^' + self.body_header + '\n' + self.body_header,
                           self.body_header + '\n', self.text)
        self.text = re.sub('^' + self.body_header + '[\n\s]*',
                           self.body_header + '\n\n', self.text)
        
    #
    def _deidentifier(self):
        deidentifier = Deidentifier(self.project_data)
        deidentifier.push_text(self.text)
        deidentifier.remove_phi()
        self.text = deidentifier.pull_text()
        
    #
    def _format_beakerap(self):
        self._clear_command_list()
        self._pull_out_section_header('(?i)[ \t]case (reviewed|seen) by:?')
        self._pull_out_section_header('(?i)[ \t]clinical history')
        self._pull_out_section_header('(?i)[ \t]comment(s)?( )?(\([a-z0-9 ]*\))?:')
        self._pull_out_section_header('(?i)[ \t]note( )?(\([a-z0-9 ]*\))?:')
        self._process_command_list()
        self._add_body_header()
        self._clear_command_list()
        self._general_command('(?<![0-9]) - (?![0-9])', {None : '\n- '})
        self._general_command('\n +', {None : '\n'})
        self._process_command_list()
        self._format_section_headers()
        
    #
    def _format_powerpath(self):
        self._add_body_header()
        self._format_section_headers()
        
    #
    def _format_section_headers(self):
        pass
        
    #
    def _named_entity_recognition(self):
        self._normalize_whitespace()
        named_entity_recognition = Named_entity_recognition(self.project_data)
        named_entity_recognition.push_text(self.text)
        named_entity_recognition.do_named_entity_recognition()
        self.text = named_entity_recognition.pull_text()
        self._normalize_whitespace()
        
    #
    def _normalize_table(self):
        table_normalizer = Table_normalizer()
        table_normalizer.push_text(self.text)
        table_normalizer.normalize_table()
        self.text = table_normalizer.pull_text()
        
    #
    def _posttokenizer(self, clear_section_headers=True):
        self._normalize_whitespace()
        posttokenizer = Posttokenizer(self.project_data)
        posttokenizer.push_text(self.text)
        posttokenizer.process_general()
        posttokenizer.process_medical_abbreviations()
        self.text = posttokenizer.pull_text()
        self._normalize_whitespace()  
        if clear_section_headers:
            self._clear_section_header_tags()
        
    #
    def _pretokenizer(self):
        self._normalize_whitespace()
        pretokenizer = Pretokenizer(self.project_data)
        pretokenizer.push_text(self.text)
        pretokenizer.process_punctuation()
        self.text = pretokenizer.pull_text()
        specimen_normalizer = Specimen_normalizer(self.project_data)
        specimen_normalizer.push_text(self.text)
        specimen_normalizer.process_specimens()
        self.text = specimen_normalizer.pull_text()
        label_normalizer = Label_normalizer(self.project_data)
        label_normalizer.push_text(self.text)
        label_normalizer.process_labels()
        self.text = label_normalizer.pull_text()
        self._extract_section_headers()
        self._normalize_whitespace()
        self._normalize_table
        
    #
    def _remove_false_specimen(self):
        self._clear_command_list()
        self._general_command('(?i) \((([a-l]|[o-s]|[u-z])+[0-9]+(,( )?)?)+\)', {None : ''})
        self._process_command_list()
        
    #
    def _rewriter(self):
        self._pretokenizer()
        self._tokenizer()
        self._posttokenizer()
        
    #
    def _summarization(self):
        self._normalize_whitespace()
        summarization = Summarization(self.project_data)
        summarization.push_text(self.text)
        summarization.do_summarization()
        self.text = summarization.pull_text()
        self._normalize_whitespace()
        
    #
    def _text_cleanup(self):
        self._normalize_whitespace()
        
    #
    def _text_setup(self):
        self._normalize_whitespace()
        text_preparation = Text_preparation(self.project_data)
        text_preparation.push_text(self.text)
        text_preparation.correct_common_typos()
        text_preparation.format_section_headers()
        text_preparation.remove_extraneous_text()
        self.text = text_preparation.pull_text()
        self._normalize_whitespace()
        
    #
    def _tokenizer(self):
        self._normalize_whitespace()
        tokenizer = Tokenizer(self.project_data)
        tokenizer.push_text(self.text)
        tokenizer.process_punctuation()
        tokenizer.process_initialisms()
        tokenizer.process_abbreviations()
        tokenizer.process_chemical_abbreviations()
        tokenizer.process_measurements()
        tokenizer.process_medical_abbreviations()
        tokenizer.process_numbers()
        tokenizer.process_simplifications()
        self.text = tokenizer.pull_text()
        tokenizer_date = Tokenizer_date(self.project_data)
        tokenizer_date.push_text(self.text)
        tokenizer_date.process_month()
        self.text = tokenizer_date.pull_text()
        self._normalize_whitespace()
        
    #
    def format_report(self, source_system):
        if source_system == 'BeakerAP':
            self._format_beakerap()
        else:
            self._format_powerpath()
        
    #
    def normalize_report(self):
        self._make_text_ascii()
        self._deidentifier()
        self._text_setup()
        self._rewriter()
        self._clear_section_header_tags()
        self._named_entity_recognition()
        self._summarization()
        self._make_text_xml_compatible()
        self._text_cleanup()