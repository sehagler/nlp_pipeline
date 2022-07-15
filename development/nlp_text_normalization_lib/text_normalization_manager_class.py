# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 10:18:29 2021

@author: haglers
"""

#
import copy

#
from lambda_lib.lambda_manager_class import Lambda_manager
from nlp_text_normalization_lib.artifact_normalizer_lib.artifact_normalizer_class \
    import Artifact_normalizer
from nlp_text_normalization_lib.character_normalizer_lib.character_normalizer_class \
    import Character_normalizer
from nlp_text_normalization_lib.deidentifier_lib.deidentifier_class \
    import Deidentifier
from nlp_text_normalization_lib.formatter_lib.formatter_class \
    import Formatter
from nlp_text_normalization_lib.posttokenizer_lib.posttokenizer_class \
    import Posttokenizer
from nlp_text_normalization_lib.specimen_normalizer_lib.specimen_normalizer_class \
    import Specimen_normalizer
from nlp_text_normalization_lib.style_normalizer_lib.style_normalizer_class \
    import Style_normalizer
from nlp_text_normalization_lib.summarization_lib.summarization_class \
    import Summarization
from nlp_text_normalization_lib.tokenizer_lib.tokenizer_class \
    import Tokenizer
from tool_lib.py.processing_tools_lib.text_processing_tools \
    import make_ascii, make_xml_compatible
from tool_lib.py.registry_lib.named_entity_recognition_registry_class \
    import Named_entity_recognition_registry

#
class Text_normalization_manager(object):
    
    #
    def __init__(self, static_data_manager):
        static_data = static_data_manager.get_static_data()
        self.artifact_normalizer = Artifact_normalizer()
        self.character_normalizer = Character_normalizer()
        self.deidentifier = Deidentifier(static_data)
        self.formatter = Formatter(static_data)
        self.lambda_manager = Lambda_manager()
        self.named_entity_recognition_registry = \
            Named_entity_recognition_registry(static_data)
        self.named_entity_recognition_registry.create_preprocessors()
        self.posttokenizer = Posttokenizer(static_data)
        self.specimen_normalizer = Specimen_normalizer()
        self.style_normalizer = Style_normalizer()
        self.summarization = Summarization(static_data)
        self.tokenizer = Tokenizer(static_data)
        
    #
    def _normalize_whitespace(self):
        self.text = \
            self.lambda_manager.lambda_conversion('\n\t', self.text, '\n')
        self.text = \
            self.lambda_manager.lambda_conversion('\r\n', self.text, '\n')
        self.text = \
            self.lambda_manager.lambda_conversion('\n*\n\n', self.text, '\n\n')
        self.text = \
            self.lambda_manager.lambda_conversion('[\n\s]*\n\s*\n', self.text, '\n\n')
        self.text = \
            self.lambda_manager.lambda_conversion('\n *', self.text, '\n')
        self.text = \
            self.lambda_manager.lambda_conversion(' *\n', self.text, '\n')
        self.text = \
            self.lambda_manager.lambda_conversion('\n-', self.text, '\n\t-')
        self.text = \
            self.lambda_manager.lambda_conversion('\t+', self.text, '\t')
        self.text = \
            self.lambda_manager.lambda_conversion(' ?\t ?', self.text, '\t')
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('^[\n\s]*', self.text)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('[\n\s]*$', self.text)
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('^ +[-]', ' ', self.text, '')
        self.text = \
            self.lambda_manager.lambda_conversion(' +', self.text, ' ')
        for _ in range(2):
            self.text = \
                self.lambda_manager.lambda_conversion(' \n', self.text, '\n')
            
    #
    def process_document(self, dynamic_data_manager, text, source_system,
                         formatting):
        self.raw_text = make_ascii(copy.copy(text))
        self.text = make_ascii(text)
        self._normalize_whitespace()
        self.text = self.artifact_normalizer.normalize_text(self.text)
        self._normalize_whitespace()
        self.text = self.style_normalizer.normalize_text(self.text)
        self._normalize_whitespace()
        self.text = self.specimen_normalizer.normalize_text(self.text)
        self._normalize_whitespace()
        dynamic_data_manager, self.text = \
            self.formatter.format_text(dynamic_data_manager, self.text, source_system, formatting)
        self._normalize_whitespace()
        self.text = self.character_normalizer.normalize_text(self.text)
        self._normalize_whitespace()
        self.text = self.deidentifier.deidentify_text(self.text)
        self._normalize_whitespace()
        
        #
        self._normalize_whitespace()
        self.text = self.tokenizer.normalize_text(self.text)
        self._normalize_whitespace()
        rpt_text = self.text
        rpt_text = self.posttokenizer.process_document(rpt_text)
        rpt_text = \
            self.named_entity_recognition_registry.run_registry(rpt_text)
        rpt_text = self.summarization.process_document(rpt_text)
        self.text = rpt_text
        #
        
        self.raw_text = make_xml_compatible(self.raw_text)
        self.text = make_xml_compatible(self.text)
        return dynamic_data_manager, self.raw_text, self.text