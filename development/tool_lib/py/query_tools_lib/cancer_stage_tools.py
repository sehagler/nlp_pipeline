# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 13:49:19 2019

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
    def __init__(self, static_data, data_file, data_dict):
        Postprocessor_base.__init__(self, static_data, data_file, data_dict)
        self._extract_data_values()
        
    #
    def _extract_data_value(self, text_list):
        if len(text_list) > 0:
            cancer_stage_text_list = text_list[1]
            cancer_type_text_list = text_list[2]
            context_text_list = text_list[3]
        else:
            cancer_stage_text_list = []
            cancer_type_text_list = []
            context_text_list = []
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
            value_dict['CONTEXT'] = value[2]
            value_dict_list.append(value_dict)
        return value_dict_list
    
    #
    def _process_cancer_stage_text_list(self, cancer_stage_text_list):
        switch_dict = {}
        switch_dict['0'] = '0'
        switch_dict['1'] = 'I'
        switch_dict['2'] = 'II'
        switch_dict['3'] = 'III'
        switch_dict['4'] = 'IV'
        switch_dict['5'] = 'V'
        pattern0 = \
            re.compile('(?i)stage( is now)? [IV]{1,3}([A-Da-d][0-9]?)?( (\-|/) [IV]{1,3}([A-Da-d][0-9]?)?)?( |$)')
        pattern1 = \
            re.compile('(?i)stage( is now)? [0-5]([A-Da-d][0-9]?)?( (\-|/) [0-5]([A-Da-d][0-9]?)?)?( |$)')
        for i in range(len(cancer_stage_text_list)):
            cancer_stage_text_raw = cancer_stage_text_list[i]
            stage_0_flg = False
            stage_0_text_list = [ 'DCIS', 'LCIS', 'SCCIS', 'in situ' ]
            for item in stage_0_text_list:
                if re.search('(?i)' + item, cancer_stage_text_raw) is not None:
                    stage_0_flg = True
            if re.search(pattern0, cancer_stage_text_raw) is not None:
                for m in re.finditer(pattern0, cancer_stage_text_raw):
                    cancer_stage_text_processed = m.group(0)
                    cancer_stage_text_processed = \
                        re.sub('(?i)stage( is now)?', '', cancer_stage_text_processed)
                    cancer_stage_text_processed = \
                        re.sub(' ', '', cancer_stage_text_processed)
                    cancer_stage_text_processed = \
                        re.sub('[A-Da-d][0-9]?', '', cancer_stage_text_processed)
            elif re.search(pattern1, cancer_stage_text_raw) is not None:
                for m in re.finditer(pattern1, cancer_stage_text_raw):
                    cancer_stage_text_processed = m.group(0)
                    cancer_stage_text_processed = \
                        re.sub('(?i)stage( is now)?', '', cancer_stage_text_processed)
                    cancer_stage_text_processed = \
                        re.sub(' ', '', cancer_stage_text_processed)
                    cancer_stage_text_processed = \
                        re.sub('[A-Da-d][0-9]?', '', cancer_stage_text_processed)
                    cancer_stage_text_processed = \
                        switch_dict[cancer_stage_text_processed]
            elif stage_0_flg:
                cancer_stage_text_processed = '0'
            elif re.search('(?i)early stage', cancer_stage_text_raw) is not None:
                cancer_stage_text_processed = 'early'
            elif re.search('(?i)end stage', cancer_stage_text_raw) is not None:
                cancer_stage_text_processed = 'end'
            elif re.search('(?i)extensive stage', cancer_stage_text_raw) is not None:
                cancer_stage_text_processed = 'extensive'
            else:
                cancer_stage_text_processed = cancer_stage_text_raw
            cancer_stage_text_list[i] = cancer_stage_text_processed
        return cancer_stage_text_list