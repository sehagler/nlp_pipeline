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
class Postprocessor(Postprocessor_base):
      
    #
    def _extract_data_value(self, value_list_dict):
        extracted_data_dict = {}
        for key in value_list_dict.keys():
            text_list = value_list_dict[key]
            fab_text_list = []
            for item in text_list[0]:
                fab_text_list.append(item[0])
            value_list = []
            for text in fab_text_list:
                if re.search('(?i)M[0-9][A-Z]?', text):
                    match = re.search('(?i)M[0-9][A-Z]?', text)
                    value_list.append(match.group(0))
            value_dict_list = []
            for value in value_list:
                value_dict = {}
                value_dict['FAB_CLASSIFICATION'] = value
                value_dict_list.append(value_dict)
            extracted_data_dict[key] = value_dict_list
        return extracted_data_dict
    
#
def fab_classification_performance(validation_data_manager, evaluation_manager,
                                   labId, nlp_values, nlp_datum_key,
                                   validation_datum_key, display_flg):
    validation_data = validation_data_manager.get_validation_data()
    if labId in nlp_values.keys():
        keys0 = list(nlp_values[labId])
        if nlp_datum_key in nlp_values[labId][keys0[0]].keys():
            data_out = nlp_values[labId][keys0[0]][nlp_datum_key]
        else:
            data_out = None
    if data_out is not None:
        data_out_tmp = data_out
        data_out = []
        data_out.append(data_out_tmp)
    nlp_value = nlp_to_tuple(data_out)
    labid_idx = validation_data[0].index('labId')
    validation_datum_idx = validation_data[0].index(validation_datum_key)
    validation_value = None
    for item in validation_data:
        if item[labid_idx] == labId:
            validation_value = item[validation_datum_idx]
    if validation_value is not None:
        if validation_value == '':
            validation_value = None
    validation_value = validation_to_tuple(validation_value)
    performance = evaluation_manager.evaluation(nlp_value, validation_value,
                                                display_flg)
    return performance