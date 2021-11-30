# -*- coding: utf-8 -*-
"""
Created on Fri Mar 08 12:13:29 2019

@author: haglers
"""

#
from nlp_lib.py.postprocessing_lib.base_class_lib.postprocessor_base_class \
    import Postprocessor_base
from nlp_lib.py.document_preprocessing_lib.base_class_lib.preprocessor_base_class \
    import Preprocessor_base
from tool_lib.py.query_tools_lib.antigens_tools import correct_antibodies

#
class Postprocessor(Postprocessor_base):
    
    #
    def __init__(self, static_data, data_file, data_dict):
        Postprocessor_base.__init__(self, static_data, data_file, data_dict,
                                    query_name='IMMUNOPHENOTYPE')
        self._extract_data_values()

    #
    def _extract_data_value(self, text_list):
        if len(text_list) > 0:
            text_list = text_list[0]
        antigens = text_list
        #antigens = self._prune_surface_antigens(antigens)
        value_list = []
        for antigen_str in antigens:
            value_list.extend([correct_antibodies(antigen_str)])
        value_dict_list = []
        for value in value_list:
            value_dict = {}
            value_dict['IMMUNOPHENOTYPE'] = value
            value_dict_list.append(value_dict)
        return value_dict_list
    
#
class Summarization(Preprocessor_base):
    
    #
    def remove_extraneous_text(self):
        self._clear_command_list()
        self._general_command('(?i)[\n\s]+(by)?(\( )?ARUP lab(s)?( \))?', {None : ''})
        self._process_command_list()