# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 10:16:10 2020

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
from nlp_lib.py.processor_lib.preprocessor_lib.rewriters_lib.posttokenizers_lib.posttokenizer_class \
    import Posttokenizer
from nlp_lib.py.processor_lib.preprocessor_lib.rewriters_lib.pretokenizers_lib.pretokenizer_class \
    import Pretokenizer
from nlp_lib.py.processor_lib.preprocessor_lib.summarization_lib.summarization_class \
    import Summarization
from nlp_lib.py.processor_lib.preprocessor_lib.text_preparation_lib.text_preparation_class \
    import Text_preparation
from nlp_lib.py.processor_lib.preprocessor_lib.rewriters_lib.tokenizers_lib.tokenizer_class \
    import Tokenizer
from nlp_lib.py.tool_lib.query_tools_lib.serial_number_tools \
    import Summarization as Summarization_serial_number
    
#
class Template_base(Preprocessor_base):
    
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
        self.text = pretokenizer.pull_text()
        self._extract_section_headers()
        self._normalize_whitespace()
        
    #
    def _rewriter(self):
        self._pretokenizer()
        self._tokenizer()
        self._posttokenizer()
        
    #
    def _summarization(self):
        self._normalize_whitespace()
        summarization_serial_number = Summarization_serial_number()
        summarization_serial_number.push_text(self.text)
        summarization_serial_number.process_names()
        summarization_serial_number.remove_extraneous_text()
        self.text = summarization_serial_number.pull_text()
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
        text_preparation.remove_extraneous_text()
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