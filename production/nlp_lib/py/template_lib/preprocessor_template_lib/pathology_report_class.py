# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 16:28:34 2018

@author: haglers
"""

#
import re

#
from nlp_lib.py.base_class_lib.preprocessor_base_class import Preprocessor_base
from nlp_lib.py.processor_lib.preprocessor_lib.deidentifier_lib.deidentifier_class \
    import Deidentifier
from nlp_lib.py.processor_lib.preprocessor_lib.named_entity_recognition_lib.named_entity_recognition_class \
    import Named_entity_recognition
from nlp_lib.py.processor_lib.preprocessor_lib.rewriters_lib.normalizers_lib.section_header_normalizer_pathology_report_class \
    import Section_header_normalizer_pathology_report
from nlp_lib.py.processor_lib.preprocessor_lib.rewriters_lib.posttokenizers_lib.posttokenizer_class \
    import Posttokenizer
from nlp_lib.py.processor_lib.preprocessor_lib.rewriters_lib.pretokenizers_lib.pretokenizer_class \
    import Pretokenizer
from nlp_lib.py.processor_lib.preprocessor_lib.rewriters_lib.tokenizers_lib.tokenizer_class \
    import Tokenizer
from nlp_lib.py.processor_lib.preprocessor_lib.summarization_lib.summarization_class \
    import Summarization
from nlp_lib.py.processor_lib.preprocessor_lib.text_preparation_lib.text_preparation_class \
    import Text_preparation

#
class Pathology_report(Preprocessor_base):
    
    #
    def __init__(self):
        Preprocessor_base.__init__(self)
        self.body_header = 'SUMMARY'
        
    #
    def _add_body_header(self):
        self.text = self.body_header + '\n' + self.text
        self.text = re.sub('^' + self.body_header + '\n' + self.body_header,
                           self.body_header + '\n', self.text)
        self.text = re.sub('^' + self.body_header + '[\n\s]*',
                           self.body_header + '\n\n', self.text)
        
    #
    def _deidentifier(self):
        deidentifier = Deidentifier()
        deidentifier.push_text(self.text)
        deidentifier.remove_phi(remove_date_flg=False)
        self.text = deidentifier.pull_text()
        
    #
    def _extract_section_headers(self):
        section_header_normalizer = Section_header_normalizer_pathology_report()
        self.linguamatics_i2e_writer.append_keywords_text(self.body_header)
        section_header_normalizer.push_linguamatics_i2e_writer(self.linguamatics_i2e_writer)
        section_header_normalizer.push_text(self.text)
        section_header_normalizer.amendment('formatted')
        section_header_normalizer.background('formatted')
        section_header_normalizer.comment('pull_out_section_header_to_bottom_of_report')
        section_header_normalizer.diagnosis('formatted')
        section_header_normalizer.explanation('formatted')
        section_header_normalizer.history('formatted')
        section_header_normalizer.impression_and_recommendation('formatted')
        section_header_normalizer.interpretation('formatted')
        section_header_normalizer.laboratory_data('formatted')
        section_header_normalizer.materials_received('formatted')
        section_header_normalizer.method('formatted')
        section_header_normalizer.person('formatted')
        section_header_normalizer.references('formatted')
        section_header_normalizer.synopsis('formatted')
        self.text = section_header_normalizer.pull_text()
        self.linguamatics_i2e_writer = section_header_normalizer.pull_linguamatics_i2e_writer()

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
        
    #
    def _format_powerpath(self):
        self._add_body_header()
        
    #
    def _named_entity_recognition(self):
        self._normalize_whitespace()
        named_entity_recognition = Named_entity_recognition()
        named_entity_recognition.push_text(self.text)
        named_entity_recognition.process_initialisms()
        self.text = named_entity_recognition.pull_text()
        self._normalize_whitespace()
        
    #
    def _normalize_table(self):
        pass
        
    #
    def _posttokenizer(self):
        self._normalize_whitespace()
        posttokenizer = Posttokenizer()
        posttokenizer.push_text(self.text)
        posttokenizer.process_general()
        self.text = posttokenizer.pull_text()
        self._normalize_whitespace()
        
    #
    def _pretokenizer(self):
        self._normalize_whitespace()
        pretokenizer = Pretokenizer()
        pretokenizer.push_text(self.text)
        pretokenizer.process_punctuation()
        pretokenizer.process_labels()
        pretokenizer.process_specimens()
        self.text = pretokenizer.pull_text()
        self._extract_section_headers()
        self._normalize_whitespace()
        
    #
    def _summarization(self):
        self._normalize_whitespace()
        summarization = Summarization()
        summarization.push_text(self.text)
        summarization.process_names()
        summarization.remove_extraneous_text()
        self.text = summarization.pull_text()
        self._normalize_whitespace()
        
    #
    def _text_setup(self):
        self._normalize_whitespace()
        text_preparation = Text_preparation()
        text_preparation.push_text(self.text)
        text_preparation.correct_common_typos()
        text_preparation.format_section_headers()
        self.text = text_preparation.pull_text()
        self._normalize_whitespace()
        
    #
    def _tokenizer(self):
        self._normalize_whitespace()
        tokenizer = Tokenizer()
        tokenizer.push_text(self.text)
        tokenizer.process_punctuation()
        tokenizer.process_initialisms()
        tokenizer.process_abbreviations()
        tokenizer.process_measurements()
        tokenizer.process_month()
        tokenizer.process_numbers()
        tokenizer.process_simplifications()
        self.text = tokenizer.pull_text()
        self._normalize_whitespace()
        
    #
    def _rewriter(self):
        self._pretokenizer()
        self._tokenizer()
        self._posttokenizer() 
     
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
        self._named_entity_recognition()
        self._summarization()
        self._make_text_xml_compatible()