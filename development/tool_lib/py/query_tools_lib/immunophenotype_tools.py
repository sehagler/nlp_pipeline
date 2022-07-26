# -*- coding: utf-8 -*-
"""
Created on Fri Mar 08 12:13:29 2019

@author: haglers
"""

#
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