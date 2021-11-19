# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 10:18:29 2021

@author: haglers
"""

#
import copy

#
from nlp_lib.py.document_preprocessing_lib.deidentifier_lib.deidentifier_class \
    import Deidentifier
from nlp_lib.py.document_preprocessing_lib.formatter_lib.formatter_class \
    import Formatter
from nlp_lib.py.document_preprocessing_lib.named_entity_recognition_lib.named_entity_recognition_class \
    import Named_entity_recognition
from nlp_lib.py.document_preprocessing_lib.posttokenizer_lib.posttokenizer_class \
    import Posttokenizer
from nlp_lib.py.document_preprocessing_lib.pretokenizer_lib.pretokenizer_class \
    import Pretokenizer
from nlp_lib.py.document_preprocessing_lib.summarization_lib.summarization_class \
    import Summarization
from nlp_lib.py.document_preprocessing_lib.text_cleanup_lib.text_cleanup_class \
    import Text_cleanup
from nlp_lib.py.document_preprocessing_lib.tokenizer_lib.tokenizer_class \
    import Tokenizer
from tool_lib.py.processing_tools_lib.text_processing_tools \
    import make_ascii, make_xml_compatible

#
class Document_preprocessing_manager(object):
    
    #
    def __init__(self, static_data_manager):
        static_data = static_data_manager.get_static_data()
        self.deidentifier = Deidentifier(static_data)
        self.formatter = Formatter(static_data)
        self.named_entity_recognition = Named_entity_recognition(static_data)
        self.posttokenizer = Posttokenizer(static_data)
        self.pretokenizer = Pretokenizer(static_data)
        self.summarization = Summarization(static_data)
        self.text_cleanup = Text_cleanup(static_data)
        self.tokenizer = Tokenizer(static_data)
            
    #
    def process_document(self, dynamic_data_manager, text, source_system,
                         formatting):
        text = make_ascii(text)
        self.deidentifier.push_text(text)
        self.deidentifier.remove_phi()
        text = self.deidentifier.pull_text()
        raw_text = text
        rpt_text = copy.copy(text)
        rpt_text = self.formatter.process_document(rpt_text, source_system)
        self.pretokenizer.set_formatting(formatting)
        dynamic_data_manager, rpt_text = \
            self.pretokenizer.process_document(dynamic_data_manager, rpt_text)
        rpt_text = self.tokenizer.process_document(rpt_text)
        rpt_text = self.posttokenizer.process_document(rpt_text)
        rpt_text = self.named_entity_recognition.process_document(rpt_text)
        rpt_text = self.summarization.process_document(rpt_text)
        rpt_text = self.text_cleanup.process_document(rpt_text)
        raw_text = make_xml_compatible(raw_text)
        rpt_text = make_xml_compatible(rpt_text)
        return dynamic_data_manager, raw_text, rpt_text