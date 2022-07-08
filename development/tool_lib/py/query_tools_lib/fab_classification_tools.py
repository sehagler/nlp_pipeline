# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 10:37:14 2019

@author: haglers
"""

#
import re

#
from tool_lib.py.query_tools_lib.base_lib.postprocessor_base_class \
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
                text = \
                    self.lambda_manager.lambda_conversion(' (?=[0-9])', text, ' M')
                text = \
                    self.lambda_manager.lambda_conversion('(AML|FAB)[\- ]', text, '')
                text = \
                    self.lambda_manager.lambda_conversion('[\(\)]', text, '')
                text = \
                    self.lambda_manager.lambda_conversion(' ', text, '')
                text = \
                    self.lambda_manager.lambda_conversion('.*(?=M)', text, '')
                value_list.append(text)
            value_dict_list = []
            for value in value_list:
                value_dict = {}
                value_dict['FAB_CLASSIFICATION'] = value
                value_dict_list.append(value_dict)
            extracted_data_dict[key] = value_dict_list
        return extracted_data_dict