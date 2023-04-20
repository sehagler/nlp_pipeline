# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 10:18:29 2021

@author: haglers
"""

#
import copy

#
import lambda_lib.tool_lib.lambda_tools as lambda_tools
from nlp_text_normalization_lib.artifact_normalizer_lib.artifact_normalizer \
    import artifact_normalizer
from nlp_text_normalization_lib.character_normalizer_lib.character_normalizer \
    import character_normalizer
from nlp_text_normalization_lib.deidentifier_lib.deidentifier \
    import deidentifier, deidentify_date
from nlp_text_normalization_lib.layout_normalizer_lib.layout_normalizer_class \
    import Layout_normalizer
from nlp_text_normalization_lib.specimen_normalizer_lib.specimen_normalizer \
    import specimen_normalizer
from nlp_text_normalization_lib.spelling_normalizer_lib.spelling_normalizer_class \
    import Spelling_normalizer
from nlp_text_normalization_lib.style_normalizer_lib.style_normalizer \
    import style_normalizer
from nlp_text_normalization_lib.table_normalizer_lib.table_normalizer \
    import table_normalizer
from tools_lib.processing_tools_lib.function_processing_tools \
    import sequential_composition
from tools_lib.processing_tools_lib.text_processing_tools \
    import make_ascii, make_xml_compatible
    
#
def normalize_whitespace(text):
    
    #
    text = \
        lambda_tools.lambda_conversion('\r', text, '\n')
    
    #
    text = \
        lambda_tools.lambda_conversion('\n+\n\n', text, '\n\n')
    
    #
    text = \
        lambda_tools.lambda_conversion(' +', text, ' ')
    text = \
        lambda_tools.lambda_conversion(' \n', text, '\n')
    text = \
        lambda_tools.lambda_conversion('\n ', text, '\n')
    
    #
    text = \
        lambda_tools.lambda_conversion('\t+', text, '\t')
    text = \
        lambda_tools.lambda_conversion(' \t', text, '\t')
    text = \
        lambda_tools.lambda_conversion('\t ', text, '\t')
    text = \
        lambda_tools.lambda_conversion('\t\n', text, '\n')
    text = \
        lambda_tools.lambda_conversion('\n\t', text, '\n')

    #text = \
    #    lambda_tools.lambda_conversion('[\n\s]*\n\s*\n', text, '\n\n')
    text = \
        lambda_tools.lambda_conversion('\n-', text, '\n\t-')
    text = \
        lambda_tools.deletion_lambda_conversion('^[\n\s]*', text)
    text = \
        lambda_tools.deletion_lambda_conversion('[\n\s]*$', text)
    text = \
        lambda_tools.contextual_lambda_conversion('^ +[-]', ' ', text, '')

    return text

#
class Text_normalization_object(object):
    
    #
    def __init__(self, preprocessor_registry, section_header_structure, 
                 remove_date_flg):
        self.remove_date_flg = remove_date_flg
        self.layout_normalizer = Layout_normalizer(section_header_structure)
        self.preprocessor_registry = preprocessor_registry
        self.spelling_normalizer = Spelling_normalizer()
        
    #
    def _normalize_raw_text(self, raw_text):
        raw_text = make_ascii(raw_text)
        raw_text = make_xml_compatible(raw_text)
        return raw_text
    
    #
    def _normalize_rpt_text(self, dynamic_data_manager, rpt_text, source_system):
        rpt_text = make_ascii(rpt_text)
        rpt_text = normalize_whitespace(rpt_text)
        rpt_text = self.spelling_normalizer.normalize_text(rpt_text)
        rpt_text = normalize_whitespace(rpt_text)
        dynamic_data_manager, rpt_text = \
            self.layout_normalizer.format_text(dynamic_data_manager, rpt_text,
                                               source_system)
        normalize_text = sequential_composition(normalize_whitespace,
                                            table_normalizer,
                                            normalize_whitespace,
                                            specimen_normalizer,
                                            normalize_whitespace,
                                            style_normalizer,
                                            normalize_whitespace,
                                            character_normalizer,
                                            normalize_whitespace,
                                            deidentifier,
                                            normalize_whitespace,
                                            artifact_normalizer,
                                            normalize_whitespace)
        rpt_text = normalize_text(rpt_text)
        rpt_text = self.preprocessor_registry.run_registry(rpt_text)
        rpt_text = normalize_whitespace(rpt_text)  
        if self.remove_date_flg:
            rpt_text = deidentify_date(rpt_text)
        rpt_text = normalize_whitespace(rpt_text)  
        rpt_text = make_xml_compatible(rpt_text)
        return dynamic_data_manager, rpt_text
            
    #
    def process_document(self, dynamic_data_manager, text, source_system):
        raw_text = self._normalize_raw_text(text)
        dynamic_data_manager, rpt_text = \
            self._normalize_rpt_text(dynamic_data_manager, copy.copy(text),
                                     source_system)
        return dynamic_data_manager, raw_text, rpt_text