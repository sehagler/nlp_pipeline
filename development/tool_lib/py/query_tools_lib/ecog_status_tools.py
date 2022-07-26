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
from tool_lib.py.query_tools_lib.base_lib.preprocessor_base_class import Preprocessor_base

#
class Postprocessor(Postprocessor_base):
        
    #
    def _extract_data_value(self, value_list_dict):
        extracted_data_dict = {}
        for key in value_list_dict.keys():
            text_list = value_list_dict[key]
            ecog_score_text_list = []
            test_text_list = []
            context_text_list = []
            for item in text_list[0]:
                if item[1] != '[0-9]+':
                    ecog_score_text_list.append(item[1])
                    test_text_list.append(item[2])
                    context_text_list.append(item[3])
            value_list = []
            normalized_ecog_score_text_list = \
                self._process_ecog_score_text_list(ecog_score_text_list, test_text_list)
            value_list = []
            for i in range(len(ecog_score_text_list)):
                value_list.append((ecog_score_text_list[i],
                                   normalized_ecog_score_text_list[i],
                                   test_text_list[i],
                                   context_text_list[i]))
            value_list = list(set(value_list))
            value_dict_list = []
            for value in value_list:
                value_dict = {}
                value_dict['ECOG_SCORE'] = value[0]
                value_dict['NORMALIZED_ECOG_SCORE'] = value[1]
                value_dict['ECOG_TEST'] = value[2]
                value_dict['SNIPPET'] = value[3]
                value_dict_list.append(value_dict)
            extracted_data_dict[key] = value_dict_list
        return extracted_data_dict
                    
    # map karnofsky and lansky value to zubrod values per
    # https://oncologypro.esmo.org/oncology-in-practice/practice-tools/performance-scales
    def _map_to_zubrod(self, value_in):
        if int(value_in) in range(96, 101):
            value_out = '0'
        elif int(value_in) in range(76, 96):
            value_out = '1'
        elif int(value_in) in range(56, 76):
            value_out = '2'
        elif int(value_in) in range(36, 56):
            value_out = '3'
        elif int(value_in) in range(6, 36):
            value_out = '4'
        elif int(value_in) in range(0, 6):
            value_out = '5'
        else:
            value_out = value_in
        return value_out
    
    #
    def _process_ecog_score_text_list(self, score_list, test_list):
        ecog_status_context_regex = re.compile('[0-9]+%?( ?- ?[0-9]+%?)?')
        ecog_status_regex = re.compile('[0-9]+')
        processed_score_list = []
        for i in range(len(score_list)):
            score_raw = score_list[i]
            test = test_list[i]
            score_processed = score_list[i]
            if test.lower() in [ 'karnofsky', 'lansky' ]:
                status_val_list = self._extract_value(ecog_status_context_regex, 
                                                      ecog_status_regex,
                                                      self._map_to_zubrod,
                                                      score_raw)
            else:
                status_val_list = self._extract_value(ecog_status_context_regex, 
                                                      ecog_status_regex, None,
                                                      score_raw)
            if len(status_val_list) == 1:
                score_processed = status_val_list[0]
            else:
                score_processed = 'MANUAL_REVIEW'
            processed_score_list.append(score_processed)
        return processed_score_list
        
    
#
class Preprocessor(Preprocessor_base):
    
    #
    def run_preprocessor(self):
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)(?<!{ )ecog( :)? (performance )?(status|score|ps)',
                                                  self.text, 'ECOG ( ZUBROD ) ')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)karnofsky (performance )?(status|score|ps)',
                                                  self.text, 'ECOG ( KARNOFSKY ) ')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)lansky (play performance )?(status|score|ps)',
                                                  self.text, 'ECOG ( LANSKY ) ')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)(?<!{ )ecog (?!\()',
                                                  self.text, 'ECOG ( ZUBROD ) ')