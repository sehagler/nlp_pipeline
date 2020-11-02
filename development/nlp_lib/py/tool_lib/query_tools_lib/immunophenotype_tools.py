# -*- coding: utf-8 -*-
"""
Created on Fri Mar 08 12:13:29 2019

@author: haglers
"""

#
from nlp_lib.py.base_class_lib.postprocessor_base_class import Postprocessor_base
from nlp_lib.py.tool_lib.query_tools_lib.antigens_tools import correct_antibodies

#
class Postprocessor(Postprocessor_base):
    
    #
    def __init__(self, csv_file, data_key_map, data_value_map):
        self.data_key_map = data_key_map
        Postprocessor_base.__init__(self, csv_file, data_key_map, data_value_map, None)
        self._cleanup_antigens()

    #
    def _cleanup_antigens(self):
        for i in range(len(self.data_dict_list)):
            for key in self.data_dict_list[i]['DATA']:
                if self.data_key_map['EXTRACTED_TEXT'] in self.data_dict_list[i]['DATA'][key].keys():
                    antigens = self.data_dict_list[i]['DATA'][key][self.data_key_map['EXTRACTED_TEXT']]
                    #antigens = self._prune_surface_antigens(antigens)
                    antigens_tmp = []
                    for antigen_str in antigens:
                        antigens_tmp.extend([correct_antibodies(antigen_str)])
                    self.data_dict_list[i]['DATA'][key][self.data_key_map['EXTRACTED_TEXT']] = antigens_tmp