# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 15:18:12 2021

@author: haglers
"""

#
import re

#
from nlp_lib.py.postprocessing_lib.base_class_lib.postprocessor_base_class \
    import Postprocessor_base

#
class Postprocessor(Postprocessor_base):
    
    #
    def __init__(self, static_data, data_file):
        Postprocessor_base.__init__(self, static_data, data_file)
        self._extract_data_values()
        
    #
    def _extract_data_value(self, text_list):
        if len(text_list) > 0:
            block_input_text_list = text_list[1]
            context_text_list = text_list[2]
        else:
            block_text_list = []
            context_text_list = []
        contexts = []
        for i in range(len(context_text_list)):
            contexts.append(context_text_list[i])
        unique_contexts = list(set(contexts))
        block_value_list = []
        for context in unique_contexts:
            block_text_list = []
            for i in range(len(context_text_list)):
                if context_text_list[i] == context:
                    block = block_input_text_list[i].upper()
                    block = self._process_block(block)
                    if len(block) > 0:
                        block_text_list.append(block)
            block_text_list = list(set(block_text_list))
            block_text_list.sort()
            block_value_list.append((block_text_list, context))
        value_dict_list = []
        for value in block_value_list:
            value_dict = {}
            value_dict['BLOCK'] = value[0]
            value_dict['CONTEXT'] = value[1]
            value_dict_list.append(value_dict)
        return value_dict_list
    
    #
    def _process_block(self, block):
        match = re.search('[A-Z][0-9]+ - [0-9]+', block)
        if match is not None:
            specimen = block[0]
            block = re.sub(' - ', '-' + specimen, block)
        match = re.search('[A-Z][0-9]+-[A-Z][0-9]+', block)
        if match is not None:
            block = re.sub('-', ',', match.group(0))
            block = '(' + block + ')'
        return block