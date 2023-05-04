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
    import sequential_composition_new as sequential_composition
from tools_lib.processing_tools_lib.text_processing_tools \
    import make_ascii, make_xml_compatible
from tools_lib.regex_lib.regex_tools \
    import article, be, note_label, s, specimen_label
from tools_lib.processing_tools_lib.text_processing_tools \
    import substitution_endings_list
    
#
def _process_organizations(text):
    text = \
        lambda_tools.initialism_lambda_conversion('eastern cooperative oncology group', text, 'ECOG')
    text = \
        lambda_tools.initialism_lambda_conversion('(u( \. )?s( \.)? ?)?food and drug administration', text, 'FDA')
    text = \
        lambda_tools.initialism_lambda_conversion('world health organization', text, 'WHO')
    return text

#
def _process_past_medical_history(text):
    text = \
        lambda_tools.initialism_lambda_conversion('past medical hx', text, 'PMH')
    text = \
        lambda_tools.lambda_conversion('PMHx', text, 'PMH')
    text = \
        lambda_tools.lambda_conversion('PMH / o', text, 'PMH')
    return text

#
def _process_regular_initialisms(text):
    
    #
    text = \
        lambda_tools.initialism_lambda_conversion('cerebrospinal fluid', text, 'CSF')
    text = \
        lambda_tools.initialism_lambda_conversion('chronic kidney disease', text, 'CKD')
    text = \
        lambda_tools.initialism_lambda_conversion('chronic renal disease', text, 'CRD')
    text = \
        lambda_tools.initialism_lambda_conversion('chronic renal failure', text, 'CRF')
    text = \
        lambda_tools.initialism_lambda_conversion('fluorescen(ce|t) in situ hybridization', text, 'FISH')
    text = \
        lambda_tools.initialism_lambda_conversion('in situ hybridization', text, 'ISH')
    text = \
        lambda_tools.initialism_lambda_conversion('red blood cell', text, 'RBC')
    text = \
        lambda_tools.initialism_lambda_conversion('white blood cell', text, 'WBC')
    
    # miscellaneous
    text = \
        lambda_tools.initialism_lambda_conversion('columnar cell change', text, 'CCC')
    text = \
        lambda_tools.initialism_lambda_conversion('flat epithelial atypia', text, 'FEA')
    text = \
        lambda_tools.initialism_lambda_conversion('pathologic complete response', text, 'pCR')
    text = \
        lambda_tools.initialism_lambda_conversion('residual ca(ncer)? burden', text, 'RCB')
    text = \
        lambda_tools.lambda_conversion('(?i)FAB (?=[0-9])', text, 'FAB M')
    text = \
        lambda_tools.lambda_conversion('(?i)HLA-Dr', text, 'HLA-DR')
    text = \
        lambda_tools.lambda_conversion('(?i)blasts ?(\+|and|plus) ?promonocytes', text, 'blasts/promonocytes')
    text = \
        lambda_tools.initialism_lambda_conversion('(?i)minimal residual disease', text, 'MRD')
    text = \
        lambda_tools.initialism_lambda_conversion('(?i)myelodysplastic syndrome', text, 'MDS')
    return text

#
def _remove_extraneous_text(text):
    text = \
        lambda_tools.deletion_lambda_conversion('[\n\s]+based on pathologic finding' + s(), text)
    text = \
        lambda_tools.deletion_lambda_conversion('(?<=Dr [A-Z])\.', text)
    text = \
        lambda_tools.deletion_lambda_conversion('my electronic signature.*' + article() + ' final diagnosis( \.)?', text)
    text = \
        lambda_tools.deletion_lambda_conversion('i have reviewed.*and final diagnosis( \.)?', text)
    text = \
        lambda_tools.deletion_lambda_conversion('(?i)inclu(des|sive of) all specimens', text)
    text = \
        lambda_tools.deletion_lambda_conversion('(?i)pathologist interpretation ' + be() + ' based on ' + article() + ' review.*representative hematoxylin and eosin stains( \.)?', text)
    text = \
        lambda_tools.deletion_lambda_conversion('(?i)' + article() + ' test ' + be() + ' developed.*FDA( \.)?', text)
    text = \
        lambda_tools.deletion_lambda_conversion('(?i)' + article() + ' clinical interpretation ' + be() + ' made by ' + article() + ' clinical geneticist( \.)?', text)
    return text

#
def _remove_mychart(text):
    text = \
        lambda_tools.deletion_lambda_conversion('display progress note in mychart : (no|yes)', text)
    return text

#
def _remove_see(text):
    text = \
        lambda_tools.deletion_lambda_conversion('(?i)(\n\s*)?\( (please )?see [^\n\)\]]* \)', text)
    text = \
        lambda_tools.lambda_conversion('(?i)\s*see\n', text, '\n')
    match_str = '(?i)((\n\s*)?-( )?)?(please[\n\s]+)?see[\n\s]+' + \
                '(the )?(second )?(amendment|cancer|note|synoptic)?( )?' + \
                '(below|comment|report|synops(e|i))' + s() + \
                '( and synoptic summary)?( and tumor protocol)?' + \
                '( below)?( for (additional|technical) (details|information))?( \.)?'
    text = substitution_endings_list(text, match_str)
    match_str = '(?i)((\n\s*)?-( )?)?(please[\n\s]+)?see ' + \
                '(note|(staging )?summary|(cancer )?synopsis|synoptic report)' + \
                '( below)?( for (additional|technical) details)?'
    text = substitution_endings_list(text, match_str)
    match_str = '(?i)((\n\s*)?-( )?)?(please[\n\s]+)?see (also )?' + \
                'note' + s() + '( )?' + note_label() + '( to ' + note_label() + ')?'
    text = substitution_endings_list(text, match_str)
    match_str = '(?i)((\n\s*)?-( )?)?(please[\n\s]+)?see (also )?' + \
                'specimen' + s() + '( )?' + specimen_label() + '( to ' + specimen_label() + ')?'
    text = substitution_endings_list(text, match_str)
    return text

'''
#
def _substitution_endings_list(text, search_str):
    text = \
        lambda_tools.lambda_conversion(search_str + '\n', text, '\n')
    text = \
        lambda_tools.lambda_conversion(search_str + '\t', text, '\t')
    text = \
        lambda_tools.lambda_conversion(search_str + ' ', text, ' ')
    text = \
        lambda_tools.lambda_conversion(search_str + ',', text, ',')
    text = \
        lambda_tools.lambda_conversion(search_str + '\.', text, '.')
    text = \
        lambda_tools.lambda_conversion(search_str + ';', text, ';')
    text = \
        lambda_tools.lambda_conversion(search_str + '( )?-', text, '-')
    return text
'''
    
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
    def __init__(self, section_header_structure, remove_date_flg):
        self.remove_date_flg = remove_date_flg
        self.layout_normalizer = Layout_normalizer(section_header_structure)
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
        rpt_text = sequential_composition([normalize_whitespace,
                                           artifact_normalizer,
                                           normalize_whitespace,
                                           deidentifier,
                                           normalize_whitespace,
                                           character_normalizer,
                                           normalize_whitespace,
                                           style_normalizer,
                                           normalize_whitespace,
                                           specimen_normalizer,
                                           normalize_whitespace,
                                           table_normalizer,
                                           normalize_whitespace,
                                           _process_regular_initialisms,
                                           normalize_whitespace,
                                           _process_past_medical_history,
                                           normalize_whitespace,
                                           _process_organizations,
                                           normalize_whitespace,
                                           _remove_mychart,
                                           normalize_whitespace,
                                           _remove_extraneous_text], rpt_text)
        if self.remove_date_flg:
            rpt_text = deidentify_date(rpt_text)
        rpt_text = normalize_whitespace(rpt_text)  
        rpt_text = make_xml_compatible(rpt_text)
        return dynamic_data_manager, rpt_text
            
    #
    def run_preprocessor(self, dynamic_data_manager, text, source_system):
        raw_text = self._normalize_raw_text(text)
        dynamic_data_manager, rpt_text = \
            self._normalize_rpt_text(dynamic_data_manager, copy.copy(text),
                                     source_system)
        return dynamic_data_manager, raw_text, rpt_text