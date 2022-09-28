# -*- coding: utf-8 -*-
"""
Created on Fri Feb 01 13:28:54 2019

@author: haglers
"""

#
from tool_lib.py.query_tools_lib.base_lib.postprocessor_base_class \
    import Postprocessor_base
from tool_lib.py.query_tools_lib.base_lib.preprocessor_base_class \
    import Preprocessor_base

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
                entry_text = self.lambda_manager.lambda_conversion('\( ', entry_text, '(')
                entry_text = \
                    self.lambda_manager.lambda_conversion(' (?=(:|,|\)))', entry_text, '')
                entry_text = \
                    self.lambda_manager.lambda_conversion('(?i)preliminary (report|results).*', entry_text, '')
                entry_text = \
                    self.lambda_manager.lambda_conversion('(?i)(\*\*)?amended (for|to).*', entry_text, '')
                entry_text = \
                    self.lambda_manager.lambda_conversion(':[ \n\t]*$', entry_text, '')
                value_list.append(entry_text)
            value_dict_list = []
            for value in value_list:
                value_dict = {}
                value_dict['FISH_ANALYSIS_SUMMARY'] = value
                value_dict_list.append(value_dict)
            extracted_data_dict[key] = value_dict_list
        return extracted_data_dict
    
#
class Preprocessor(Preprocessor_base):
    
    #
    def run_preprocessor(self):
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?i)[\n\s]+by FISH', self.text)
            
#
def fish_analysis_summary_performance(validation_data_manager,
                                      evaluation_manager,labId, nlp_values,
                                      nlp_datum_key, validation_datum_key):
    validation_data = validation_data_manager.get_validation_data()
    if labId in nlp_values.keys():
        keys0 = list(nlp_values[labId])
        if nlp_datum_key in nlp_values[labId][keys0[0]].keys():
            data_out = nlp_values[labId][keys0[0]][nlp_datum_key]
        else:
            data_out = None
    else:
        data_out = None
    if data_out is not None:
        data_out_tmp = data_out
        data_out_tmp = \
            data_out_tmp.replace(' ', '')
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
        if validation_value == '':
            validation_value = None
    if validation_value is not None:
        validation_value_tmp = validation_value
        validation_value_tmp = \
            validation_value_tmp.replace(' ', '')
        validation_value = []
        validation_value.append(validation_value_tmp)
    if validation_value is not None:
        validation_value = tuple(validation_value)
    display_flg = True
    performance = \
        evaluation_manager.evaluation(nlp_value, validation_value, display_flg)
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