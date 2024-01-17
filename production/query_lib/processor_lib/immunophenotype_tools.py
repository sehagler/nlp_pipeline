# -*- coding: utf-8 -*-
"""
Created on Fri Mar 08 12:13:29 2019

@author: haglers
"""

#
import re

#
from query_lib.processor_lib.antigens_tools \
    import cleanup_antigens, extract_antigens
from base_lib.evaluator_base_class import Evaluator_base
from base_lib.postprocessor_base_class import Postprocessor_base
import lambda_lib.tool_lib.lambda_tools as lambda_tools
from query_lib.processor_lib.antigens_tools import correct_antibodies

#
class Evaluator(Evaluator_base):
    
    #
    def run_object(self, evaluation_manager, nlp_value, validation_value,
                 display_flg):
        if nlp_value is not None:
            if isinstance(nlp_value, list):
                nlp_value = self.manual_review
        if nlp_value is not None and \
           nlp_value != self.manual_review:
            nlp_value = re.sub('dim', 'dim ', nlp_value)
            nlp_value = re.sub('\+', ' +', nlp_value)
            nlp_value = re.sub('(?i)(-)?positive', ' +', nlp_value)
            nlp_value = extract_antigens(nlp_value)
            nlp_value = list(set(nlp_value))
        if nlp_value is not None and \
           nlp_value != self.manual_review:
            nlp_value = tuple(nlp_value)
        else:
            nlp_value = None
        if validation_value is not None:
            validation_value = cleanup_antigens(validation_value)
            validation_value = re.sub('(?i)n/a', '', validation_value)
            validation_value = \
                re.sub('(?i)not (available|run)', '', validation_value)
            if validation_value == '':
                validation_value = None
        if validation_value is not None:
            validation_value = re.sub('dim', 'dim ', validation_value)
            validation_value = re.sub('\+', ' +', validation_value)
            validation_value = re.sub('(?i)(-)?positive', ' +', validation_value)
            validation_value = extract_antigens(validation_value)
            validation_value = list(set(validation_value))
        if validation_value is not None:
            validation_value = \
                tuple(validation_value)
        arg_dict = {}
        arg_dict['display_flg'] = display_flg
        arg_dict['nlp_value'] = nlp_value
        arg_dict['validation_value'] = validation_value
        ret_dict = evaluation_manager.evaluation(arg_dict)
        return ret_dict['performance']

#
class Postprocessor(Postprocessor_base):

    #
    def _extract_data_value(self, value_list_dict):
        extracted_data_dict = {}
        for key in value_list_dict.keys():
            text_list = value_list_dict[key]
            antigens_list = []
            for item in text_list[0]:
                antigens_list.append(item[0])
            #antigens = self._prune_surface_antigens(antigens)
            value_list = []
            for antigens in antigens_list:
                value_list.extend([correct_antibodies(antigens)])
            value_dict_list = []
            for value in value_list:
                value_dict = {}
                value_dict['IMMUNOPHENOTYPE'] = value
                value_dict_list.append(value_dict)
            extracted_data_dict[key] = value_dict_list
        return extracted_data_dict
    
#
class Preprocessor(object):

    #
    def __init__(self, static_data_object, logger_object):
        self.static_data_object = static_data_object
        self.logger_object = logger_object
    
    #
    def run_object(self, text):
        text = \
            lambda_tools.deletion_lambda_conversion('(?i)[\n\s]+(by)?(\( )?ARUP lab(s)?( \))?', text)
        return text