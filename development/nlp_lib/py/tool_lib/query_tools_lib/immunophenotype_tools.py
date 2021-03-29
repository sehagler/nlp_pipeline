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
    def __init__(self, project_data, data_file, data_key_map, data_value_map,
                 label):
        Postprocessor_base.__init__(self, project_data, label, data_file,
                                    data_key_map, data_value_map)
        self._cleanup_antigens()

    #
    def _cleanup_antigens(self):
        for i in range(len(self.data_dict_list)):
            for key in self.data_dict_list[i][self.nlp_data_key]:
                antigens = \
                    self.data_dict_list[i][self.nlp_data_key][key][self.label][self.nlp_text_key]
                #antigens = self._prune_surface_antigens(antigens)
                value_list = []
                for antigen_str in antigens:
                    value_list.extend([correct_antibodies(antigen_str)])
                self._append_data(i, key, value_list)