# -*- coding: utf-8 -*-
"""
Created on Fri Mar 08 12:13:29 2019

@author: haglers
"""

#
import re

#
from tool_lib.py.query_tools_lib.antigens_tools \
    import cleanup_antigens, extract_antigens
from tool_lib.py.query_tools_lib.base_lib.postprocessor_base_class \
    import Postprocessor_base
from tool_lib.py.query_tools_lib.base_lib.preprocessor_base_class \
    import Preprocessor_base
from tool_lib.py.query_tools_lib.antigens_tools import correct_antibodies

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
class Preprocessor(Preprocessor_base):
    
    #
    def run_preprocessor(self):
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?i)[\n\s]+(by)?(\( )?ARUP lab(s)?( \))?', self.text)
            
#
def surface_antigens_performance(validation_data_manager, evaluation_manager,
                                 labId, nlp_values, nlp_datum_key, 
                                 validation_datum_key):
    validation_data = validation_data_manager.get_validation_data()
    if labId in nlp_values.keys():
        keys0 = list(nlp_values[labId])
        if nlp_datum_key in nlp_values[labId][keys0[0]].keys():
            data_out = nlp_values[labId][keys0[0]][nlp_datum_key][0][0]
            if data_out == '':
                data_out = None
        else:
            data_out = None
    else:
        data_out = None
    if data_out is not None:
        if isinstance(data_out, list):
            data_out = 'MANUAL_REVIEW'
    if data_out is not None and \
       data_out is not 'MANUAL_REVIEW':
        data_out = re.sub('dim', 'dim ', data_out)
        data_out = re.sub('\+', ' +', data_out)
        data_out = re.sub('(?i)(-)?positive', ' +', data_out)
        data_out = extract_antigens(data_out)
        data_out = list(set(data_out))
    if data_out is not None and \
       data_out is not 'MANUAL_REVIEW':
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
        validation_value = cleanup_antigens(validation_value)
        validation_value = re.sub('(?i)n/a', '', validation_value)
        validation_value = re.sub('(?i)not (available|run)', '', validation_value)
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
    display_flg = True
    performance = evaluation_manager.evaluation(nlp_value, validation_value,
                                                display_flg)
    return performance