# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 12:32:58 2019

@author: haglers
"""

#
import re

#
from tools_lib.processing_tools_lib.variable_processing_tools \
    import trim_data_value
from query_lib.processor_lib.base_lib.diagnosis_tools_base \
    import Postprocessor as Postprocessor_base

#
class Postprocessor(Postprocessor_base):
    pass

#
def diagnosis_performance(evaluation_manager, nlp_value, validation_value,
                          display_flg):
    if nlp_value is not None:
        nlp_value = nlp_value[0][0]
        nlp_value = re.sub('SYNDROME(?!S)', 'SYNDROMES', nlp_value)
        nlp_value_tmp = nlp_value
        nlp_value = []
        nlp_value.append(nlp_value_tmp)
    if nlp_value is not None:
        nlp_value = tuple(nlp_value)
    else:
        nlp_value = None
    if validation_value is not None:
        validation_value = re.sub('LEUKAEMIA', 'LEUKEMIA', validation_value)
        validation_value = re.sub('leukaemia', 'leukemia', validation_value)
        validation_value = \
            re.sub('SYNDROME(?!S)', 'SYNDROMES', validation_value)
        if validation_value == '':
            validation_value = None
    if validation_value is not None:
        validation_value_tmp = validation_value
        validation_value = []
        validation_value.append(validation_value_tmp)
        validation_value = tuple(validation_value)
    arg_dict = {}
    arg_dict['display_flg'] = display_flg
    arg_dict['nlp_value'] = nlp_value
    arg_dict['validation_value'] = validation_value
    ret_dict = evaluation_manager.evaluation(arg_dict)
    return ret_dict['performance']

#                 
def evaluate_diagnosis(data_json):
    data_json_tmp = data_json
    for key0 in data_json_tmp.keys():
        for key1 in data_json_tmp[key0].keys():
            for key2 in data_json_tmp[key0][key1].keys():
                if 'dx' in data_json_tmp[key0][key1][key2].keys():
                    dx_values = data_json_tmp[key0][key1][key2]['dx']
                else:
                    dx_values = None
                if 'specificDx' in data_json_tmp[key0][key1][key2].keys():
                    specificdx_values = \
                        data_json_tmp[key0][key1][key2]['specificDx']
                else:
                    specificdx_values = None
                values = []
                if dx_values is not None:
                    dx_values = list(set(dx_values))
                    for dx_value in dx_values:
                        values.extend([dx_value[0]])
                if specificdx_values is not None:
                    specificdx_values = list(set(specificdx_values))
                    for specificdx_value in specificdx_values:
                        values.append(specificdx_value[0])
                if len(values) > 0:
                    values = [ values ]
                if len(values) > 0:
                    values = trim_data_value(values)
                    values = list(set(values))
                    if len(values) == 1:
                        value = values[0]
                    elif len(values) > 1:
                        value = 'MANUAL_REVIEW'
                    else:
                        value = None
                    if value is not None:
                        data_json[key0][key1][key2]['dx'] = value
                    else:
                        del data_json[key0][key1][key2]['dx']
                else:
                    pass
    return data_json