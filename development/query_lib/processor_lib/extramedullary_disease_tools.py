# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 10:37:14 2019

@author: haglers
"""

#
import re

#
from tools_lib.processing_tools_lib.variable_processing_tools \
    import nlp_to_tuple, validation_to_tuple
from base_lib.postprocessor_base_class \
    import Postprocessor_base
    
#
def extramedullary_disease_performance(evaluation_manager, nlp_value,
                                       validation_value, display_flg):
    if nlp_value is not None:
        nlp_value = re.sub('SYNDROME', 'SYNDROMES', nlp_value)
        nlp_value_tmp = nlp_value
        nlp_value = []
        nlp_value.append(nlp_value_tmp)
    nlp_value = nlp_to_tuple(nlp_value)
    if validation_value is not None:
        if validation_value == '':
            validation_value = None
    validation_value = validation_to_tuple(validation_value)
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
            value_list = []
            for item in text_list[0]:
                value_list.append(item[0])
            value_dict_list = []
            for value in value_list:
                value_dict = {}
                value_dict['EXTRAMEDULLARY_DISEASE'] = value
                value_dict_list.append(value_dict)
            extracted_data_dict[key] = value_dict_list
        return extracted_data_dict