# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 13:49:19 2019

@author: haglers
"""

#
import os
import re

#
from tools_lib.regex_lib.regex_tools import regex_from_list
from tools_lib.processing_tools_lib.file_processing_tools \
    import read_xlsx_file, write_file, xml_diff
from base_lib.postprocessor_base_class \
    import Postprocessor_base

#
class Postprocessor(Postprocessor_base):
        
    #
    def _extract_data_value(self, value_list_dict):
        extracted_data_dict = {}
        for key in value_list_dict.keys():
            text_list = value_list_dict[key]
            tumor_size_text_list = []
            snippet_text_list = []
            for item in text_list[0]:
                tumor_size_text_list.append(item[0])
                #snippet_text_list.append(item[2])
                snippet_text_list.append('')
            value_list = []
            for i in range(len(tumor_size_text_list)):
                value_list.append((tumor_size_text_list[i],
                                   snippet_text_list[i]))
            value_list = list(set(value_list))
            value_dict_list = []
            for value in value_list:
                value_dict = {}
                value_dict['TUMOR_SIZE'] = value[0]
                #value_dict['SNIPPET'] = value[1]
                value_dict_list.append(value_dict)
            extracted_data_dict[key] = value_dict_list
        return extracted_data_dict