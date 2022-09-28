# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 12:32:58 2019

@author: haglers
"""

#
import re

#
from tool_lib.py.processing_tools_lib.variable_processing_tools \
    import trim_data_value
from tool_lib.py.query_tools_lib.base_lib.diagnosis_tools_base \
    import Postprocessor as Postprocessor_base

#
class Postprocessor(Postprocessor_base):
    pass

#
def diagnosis_performance(validation_data_manager, evaluation_manager, labId,
                          nlp_values, nlp_datum_key, validation_datum_key):
    validation_data = validation_data_manager.get_validation_data()
    if labId in nlp_values.keys():
        keys0 = list(nlp_values[labId])
        if nlp_datum_key in nlp_values[labId][keys0[0]].keys():
            data_out = nlp_values[labId][keys0[0]][nlp_datum_key][0][0]
        else:
            data_out = None
    if data_out is not None:
        data_out = re.sub('SYNDROME(?!S)', 'SYNDROMES', data_out)
        data_out_tmp = data_out
        data_out = []
        data_out.append(data_out_tmp)
    if data_out is not None:
        nlp_value = tuple(data_out)
    else:
        nlp_value = None
    labid_idx = validation_data[0].index('labId')
    validation_datum_idx = validation_data[0].index(validation_datum_key)
    validation_value = None
    for item in validation_data:
        if item[labid_idx] == labId:
            validation_value = item[validation_datum_idx]
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
    display_flg = True
    performance = evaluation_manager.evaluation(nlp_value, validation_value,
                                                display_flg)
    return performance

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