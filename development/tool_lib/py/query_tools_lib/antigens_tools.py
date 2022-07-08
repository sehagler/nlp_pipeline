# -*- coding: utf-8 -*-
"""
Created on Fri Mar 08 12:42:14 2019

@author: haglers
"""

#
import re

#
from lambda_lib.lambda_manager_class import Lambda_manager
from tool_lib.py.query_tools_lib.base_lib.postprocessor_base_class \
    import Postprocessor_base
from nlp_text_normalization_lib.base_lib.preprocessor_base_class \
    import Preprocessor_base

#
class Postprocessor(Postprocessor_base):

    #
    def _extract_data_value(self, value_list_dict):
        extracted_data_dict = {}
        for key in value_list_dict.keys():
            text_list = value_list_dict[key]
            value = []
            for item in text_list[0]:
                value.append(item[0])
            value_dict_list = []
            value_dict = {}
            value_dict['ANTIBODIES_TESTED'] = value
            value_dict_list.append(value_dict)
            extracted_data_dict[key] = value_dict_list
        return extracted_data_dict

#
class Posttokenizer(Preprocessor_base):
    
    #
    def process_antigens(self):
        antigens = antigens_list()
        self.text = self.lambda_manager.lambda_conversion('HLA ?DR', self.text, 'HLA-DR')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)dim(-| (/ )?)partial', self.text, 'dim/partial')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)dim (/ )?variable', self.text, 'dim/variable')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)(bright|dim|low|moderate|partial|subset|variable)CD', self.text, ' CD')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)partial (/ )?dim', self.text, 'dim/partial')
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?<=CD) (?=[0-9])', self.text)
        self.text = \
            self.lambda_manager.contextual_lambda_conversion(antigens + '\(', '\(', self.text, ' (')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion(antigens + ' : ' + antigens, ' : ', self.text, ':')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion(antigens + ' / ' + antigens, ' / ', self.text, '/')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion(antigens + '-negative', '-negative', self.text, ' negative')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion(antigens + '-positive', '-positive', self.text, ' positive')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion(antigens + '-', '-', self.text, ' negative ')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion(antigens + ' *\+', '\+', self.text, ' positive ')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion(antigens + ' *\( \+ \)', '\( \+ \)', self.text, ' positive')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=HLA) (negative|positive)(?=DR)', self.text, '-')

#
def antigens_list():
    return '([a-z]?CD[0-9]+|HLA-DR|MPO|T[Dd]T|Kappa|Lambda)'

#
def correct_antibodies(text):
    lambda_manager = Lambda_manager()
    text = lambda_manager.lambda_conversion('HLA *- *DR', text, 'HLA-DR')
    return text

#
def extract_antigens(text):
    antigen_list = []
    tokens = text.split(' ')
    for token in tokens:
        if is_antibody(token):
            antigen_list.append(token)
    return antigen_list

#
def is_antibody(text, lower_flg=False):
    match_str = '^('
    match_str += '[a-z]?CD[0-9]+[a-z]?( \(subset\))?'
    match_str += '|HLA-DR'
    match_str += '|[a-z]?Kappa[a-z]?( \(mono\))?'
    match_str += '|[a-z]?Lambda[a-z]?( \(mono\))?'
    match_str += '|[a-z]?MPO'
    match_str += '|[a-z]?T[Dd]T'
    match_str += ')$'
    if lower_flg:
        match_str = match_str.lower()
    if re.match(match_str, text):
        return True
    else:
        return False
 
#
def is_antibody_value(text):
    match_str = '(?i)^('
    match_str += 'bright'
    match_str += '|dim(inished)?'
    match_str += '|focal'
    match_str += '|low'
    match_str += '|partial/dim'
    match_str += '|partial'
    match_str += '|variable'
    match_str += ')$'
    if re.match(match_str, text):
        return True
    else:
        return False
    
#
def template():
    antigens = '[a-z]?(CD[0-9]+|HLA-DR|MPO|T[Dd]T|Kappa|Lambda)[a-z]?'
    template = '(' + antigens + ' ?){2,}'
    template_list = []
    template_list.append(template)
    sections_list = [ 'ANTIBODIES TESTED' ]
    template_dict = {}
    template_dict['primary_template_list'] = template_list
    template_dict['sections_list'] = sections_list
    template_dict['template_headers'] = [ 'Antigens' ]
    return template_dict