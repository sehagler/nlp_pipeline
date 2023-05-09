# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 15:52:26 2022

@author: haglers
"""

#
import re

#
from tools_lib.processing_tools_lib.variable_processing_tools \
    import nlp_to_tuple, validation_to_tuple
from query_lib.processor_lib.base_lib.date_tools_base \
    import Postprocessor as Postprocessor_base
from query_lib.processor_lib.base_lib.date_tools_base \
    import Tokenizer as Tokenizer_base
    
#
def residual_disease_performance(evaluation_manager, nlp_value,
                                 validation_value, display_flg):
    if nlp_value is not None:
        nlp_value = nlp_value.lower()
        nlp_value_tmp = nlp_value
        nlp_value = []
        nlp_value.append(nlp_value_tmp)
    nlp_value = nlp_to_tuple(nlp_value)
    if validation_value is not None:
        validation_value = \
            re.sub('(?i)acute myeloid leukemia', 'AML', validation_value)
        validation_value = validation_value.lower()
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
    pass

#
class Tokenizer(Tokenizer_base):
    pass