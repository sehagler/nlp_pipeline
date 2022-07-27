# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 13:49:19 2019

@author: haglers
"""

#
import re

#
from tool_lib.py.query_tools_lib.base_lib.postprocessor_base_class \
    import Postprocessor_base
from tool_lib.py.processing_tools_lib.text_processing_tools \
    import regex_from_list
from tool_lib.py.query_tools_lib.cancer_tools \
    import nonnumeric_stage, numeric_stage

#
class Postprocessor(Postprocessor_base):
        
    #
    def _extract_data_value(self, value_list_dict):
        extracted_data_dict = {}
        for key in value_list_dict.keys():
            text_list = value_list_dict[key]
            cancer_stage_text_list = []
            cancer_type_text_list = []
            context_text_list = []
            for item in text_list[0]:
                cancer_stage_text_list.append(item[1])
                cancer_type_text_list.append(item[2])
                context_text_list.append(item[3])
            cancer_stage_text_list = \
                self._process_cancer_stage_text_list(cancer_stage_text_list)
            value_list = []
            for i in range(len(cancer_stage_text_list)):
                value_list.append((cancer_stage_text_list[i],
                                   cancer_type_text_list[i],
                                   context_text_list[i]))
            value_list = list(set(value_list))
            value_dict_list = []
            for value in value_list:
                value_dict = {}
                value_dict['CANCER_STAGE'] = value[0]
                value_dict['CANCER_TYPE'] = value[1]
                value_dict['SNIPPET'] = value[2]
                value_dict_list.append(value_dict)
            extracted_data_dict[key] = value_dict_list
        return extracted_data_dict
    
    #
    def _map_to_cancer_stage(self, value_in):
        switch_dict = {}
        switch_dict['0'] = '0'
        switch_dict['1'] = 'I'
        switch_dict['2'] = 'II'
        switch_dict['3'] = 'III'
        switch_dict['4'] = 'IV'
        switch_dict['5'] = 'V'
        if value_in in switch_dict.keys():
            value_out = switch_dict[value_in]
        else:
            value_out = value_in
        return value_out
    
    #
    def _process_cancer_stage_text_list(self, cancer_stage_text_list):
        numeric_stage_context_regex = \
            re.compile('(?i)stage (.* )?' + numeric_stage())
        numeric_stage_regex = ('(?i)(?<=[ ^])([0-9]+|[IV]+)')
        nonnumeric_stage_context_regex = \
            re.compile('(?i)' + nonnumeric_stage() + ' stage')
        nonnumeric_stage_regex = \
            re.compile('(?i)' + nonnumeric_stage())
        in_situ_list = [ 'DCIS', 'LCIS', 'SCCIS', 'in situ' ]
        in_situ_regex = re.compile('(?i)' + regex_from_list(in_situ_list))
        for i in range(len(cancer_stage_text_list)):
            cancer_stage_text_raw = cancer_stage_text_list[i]
            cancer_stage_text_processed = []
            stage_val_list = self._extract_value(numeric_stage_context_regex, 
                                                 numeric_stage_regex,
                                                 self._map_to_cancer_stage,
                                                 cancer_stage_text_raw)
            for item in stage_val_list:
                cancer_stage_text_processed.append(item)
            stage_val_list = self._extract_value(nonnumeric_stage_context_regex, 
                                                 nonnumeric_stage_regex, None,
                                                 cancer_stage_text_raw)
            for item in stage_val_list:
                cancer_stage_text_processed.append(item.lower())
            stage_val_list = self._extract_value(in_situ_regex, in_situ_regex, 
                                                 None, cancer_stage_text_raw)
            for item in stage_val_list:
                cancer_stage_text_processed.append('0')
            if len(cancer_stage_text_processed) == 1:
                cancer_stage_text_list[i] = cancer_stage_text_processed[0]
            else:
                cancer_stage_text_list[i] = 'MANUAL_REVIEW'
        return cancer_stage_text_list