# -*- coding: utf-8 -*-
"""
Created on Fri Feb 01 13:28:54 2019

@author: haglers
"""

#
from base_lib.evaluator_base_class import Evaluator_base
from base_lib.postprocessor_base_class import Postprocessor_base
import lambda_lib.tool_lib.lambda_tools as lambda_tools

#
def _evaluate(evaluation_manager, nlp_value, validation_value, display_flg):
    if nlp_value is not None:
        nlp_value_tmp = nlp_value
        nlp_value_tmp = nlp_value_tmp.replace(' ', '')
        nlp_value = []
        nlp_value.append(nlp_value_tmp)
    if nlp_value is not None:
        nlp_value = tuple(nlp_value)
    else:
        nlp_value = None
    if validation_value is not None:
        if validation_value == '':
            validation_value = None
    if validation_value is not None:
        validation_value_tmp = validation_value
        validation_value_tmp = validation_value_tmp.replace(' ', '')
        validation_value = []
        validation_value.append(validation_value_tmp)
    if validation_value is not None:
        validation_value = tuple(validation_value)
    arg_dict = {}
    arg_dict['display_flg'] = display_flg
    arg_dict['nlp_value'] = nlp_value
    arg_dict['validation_value'] = validation_value
    performance = \
        evaluation_manager.evaluation(arg_dict)
    return performance
        
#
def simple_template():
    template_list = None
    sections_list = [ 'FISH ANALYSIS SUMMARY' ]
    template_dict = {}
    template_dict['primary_template_list'] = template_list
    template_dict['sections_list'] = sections_list
    template_dict['template_headers'] = [ 'FISH Analysis Summary' ]
    return template_dict

#
class Evaluator(Evaluator_base):
    
    #
    def run_object(self, evaluation_manager, nlp_value, validation_value,
                 display_flg):
        return _evaluate(evaluation_manager, nlp_value, validation_value,
                         display_flg)

#
class Postprocessor(Postprocessor_base):
 
    #
    def _extract_data_value(self, value_list_dict):
        extracted_data_dict = {}
        for key in value_list_dict.keys():
            text_list = value_list_dict[key]
            fish_text_list = []
            for item in text_list[0]:
                fish_text_list.append(item[0])
            value_list = []
            for entry_text in fish_text_list:
                entry_text = lambda_tools.lambda_conversion('\( ', entry_text, '(')
                entry_text = \
                    lambda_tools.deletion_lambda_conversion(' (?=(:|,|\)))', entry_text)
                entry_text = \
                    lambda_tools.deletion_lambda_conversion('(?i)preliminary (report|results).*', entry_text)
                entry_text = \
                    lambda_tools.deletion_lambda_conversion('(?i)this test.*', entry_text)
                entry_text = \
                    lambda_tools.deletion_lambda_conversion('(?i)(\*\*)?amended (for|to).*', entry_text)
                entry_text = \
                    lambda_tools.deletion_lambda_conversion(':[ \n\t]*$', entry_text)
                entry_text = \
                    lambda_tools.deletion_lambda_conversion('( \.)* ?$', entry_text)
                value_list.append(entry_text)
            value_dict_list = []
            for value in value_list:
                value_dict = {}
                value_dict['FISH_ANALYSIS_SUMMARY'] = value
                value_dict_list.append(value_dict)
            extracted_data_dict[key] = value_dict_list
        return extracted_data_dict
    
#
class Preprocessor(object):
    
    #
    def run_object(self, text):
        text = \
            lambda_tools.deletion_lambda_conversion('(?i)[\n\s]+by FISH', text)
        return text
            
#
class Section_header_structure():
    
    #
    def add_section_header(self, section_header_dict):
        regex_dict = {}
        regex_list = []
        regex_list.append('(interphase )?fish analysis summary')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        section_header_dict['FISH ANALYSIS SUMMARY'] = regex_dict
        return section_header_dict