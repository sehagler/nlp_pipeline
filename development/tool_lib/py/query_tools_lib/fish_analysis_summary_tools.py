# -*- coding: utf-8 -*-
"""
Created on Fri Feb 01 13:28:54 2019

@author: haglers
"""

#
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
class Summarization(Preprocessor_base):
    
    #
    def run_preprocessor(self):
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?i)[\n\s]+by FISH', self.text)
        
#
def template():
    template_list = None
    sections_list = [ 'FISH ANALYSIS SUMMARY' ]
    template_dict = {}
    template_dict['primary_template_list'] = template_list
    template_dict['sections_list'] = sections_list
    template_dict['template_headers'] = [ 'FISH Analysis Summary' ]
    return template_dict