# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 13:49:19 2019

@author: haglers
"""

#
import ast
import os
import re

#
from base_lib.manager_base_class import Manager_base
from tools_lib.regex_lib.regex_tools import regex_from_list
from tools_lib.processing_tools_lib.file_processing_tools \
    import read_xlsx_file, write_file, xml_diff
from base_lib.postprocessor_base_class \
    import Postprocessor_base
from query_lib.processor_lib.cancer_tools \
    import get_initialisms, nonnumeric_stage, numeric_stage
    
#
class AB_fields_template_manager(Manager_base):
    
    #
    def __init__(self, static_data_object, logger_object):
        Manager_base.__init__(self, static_data_object, logger_object)
        self.xls_manager = None
        self._get_secondary_template_list()
        self.blank_space = ' NLP_BLANK_SPACE '
        self.linguamatics_i2e_AB_fields_path = None
        self.training_data_file = None
    
    #
    def _get_initialisms(self):
        return get_initialisms()
                
    #
    def _get_secondary_template_list(self):
        cancer_is_value = self._nlp_cancer_is_value()
        cancer_stage_value = self._nlp_cancer_stage_value()
        cancer_type = self._nlp_cancer_type()
        self.secondary_template_list = []
        self.secondary_template_list.append(['(?i)(' + \
                                            cancer_stage_value[1:-1] + \
                                            '|' + \
                                            cancer_is_value[1:-1] + \
                                            ')'])
        self.secondary_template_list.append(['(?i)' + cancer_type])
    
    #
    def _nlp_cancer_is_value(self):
        nlp_cancer_is_value = '('
        nlp_cancer_is_value += self._get_initialisms() + 'is'
        nlp_cancer_is_value += ')'
        return nlp_cancer_is_value
        
    #
    def _nlp_cancer_stage_value(self):
        nlp_cancer_stage_value = '('
        nlp_cancer_stage_value += \
            '(clinical (: )?)?stage( is( now)?)? ' + numeric_stage()
        nlp_cancer_stage_value += '|'
        nlp_cancer_stage_value += \
            nonnumeric_stage() + ' (clinical (: )?)?stage'
        nlp_cancer_stage_value += '|'
        nlp_cancer_stage_value += 'in situ'
        nlp_cancer_stage_value += ')'
        return nlp_cancer_stage_value
    
    #
    def _nlp_cancer_type(self):
        nlp_cancer_type = '('
        nlp_cancer_type += '[A-Za-z]+(ca(ncer)?s?|omas?)'
        nlp_cancer_type += '|'
        nlp_cancer_type += '(ca(ncer)?s?|metastas(e|i)s|nodules?|tumors?)'
        nlp_cancer_type += '|'
        nlp_cancer_type += self._get_initialisms()
        nlp_cancer_type += ')'
        return nlp_cancer_type
    
    #
    def pull_A_charge(self):
        return 'NLP_CANCER_TYPE'
    
    #
    def pull_B_charge(self):
        return 'NLP_CANCER_STAGE_VALUE'
    
    #
    def pull_linguamatics_i2e_AB_fields_path(self):
        return self.linguamatics_i2e_AB_fields_path
    
    #
    def pull_primary_template_list(self):
        return self.xls_manager.column('ANNOTATED_CANCER_STAGE_EXTRACT')
    
    #
    def pull_training_data_file(self):
        return self.training_data_file
    
    #
    def push_primary_template_list(self, AB_field_list, BA_field_list):
        self.AB_field_list = AB_field_list
        self.BA_field_list = BA_field_list
        
    #
    def push_xls_manager(self, xls_manager):
        self.xls_manager = xls_manager
        
    #
    def training_template(self):
        template_dict = {}
        template_dict['AB_field_list'] = self.AB_field_list
        template_dict['BA_field_list'] = self.BA_field_list
        template_dict['secondary_template_list'] = self.secondary_template_list
        template_dict['sections_list'] = None
        template_dict['template_headers'] = [ 'Cancer Stage Extract',
                                              'Cancer Stage', 'Cancer Type' ]
        return template_dict
    
    #
    def template(self):
        static_data = self.static_data_object.get_static_data()
        directory_manager = static_data['directory_manager']
        template_outlines_dir = \
            directory_manager.pull_directory('template_outlines_dir')
        filename = 'cancer_stage_template_outline.txt'
        with open(os.path.join(template_outlines_dir, filename), 'r') as f:
            primary_template_str = f.read()
        primary_template_list = \
            ast.literal_eval(primary_template_str)
        template_dict = {}
        template_dict['primary_template_list'] = primary_template_list
        template_dict['secondary_template_list'] = self.secondary_template_list
        template_dict['sections_list'] = None
        template_dict['template_headers'] = [ 'Cancer Stage Extract',
                                              'Cancer Stage', 'Cancer Type' ]
        return template_dict

#
class Postprocessor(Postprocessor_base):
        
    #
    def _extract_data_value(self, value_list_dict):
        extracted_data_dict = {}
        for key in value_list_dict.keys():
            text_list = value_list_dict[key]
            histologic_stage_text_list = []
            histologic_type_text_list = []
            tumor_site_text_list = []
            snippet_text_list = []
            for item in text_list[0]:
                histologic_stage_text_list.append(item[1])
                histologic_type_text_list.append(item[2])
                tumor_site_text_list.append(item[3])
                snippet_text_list.append(item[4])
            histologic_stage_text_list = \
                self._process_histologic_stage_text_list(histologic_stage_text_list)
            value_list = []
            for i in range(len(histologic_stage_text_list)):
                value_list.append((histologic_stage_text_list[i],
                                   histologic_type_text_list[i],
                                   tumor_site_text_list[i],
                                   snippet_text_list[i]))
            value_list = list(set(value_list))
            value_dict_list = []
            for value in value_list:
                value_dict = {}
                value_dict['CANCER_STAGE'] = value[0]
                value_dict['HISTOLOGIC_TYPE'] = value[1]
                value_dict['TUMOR_SITE'] = value[2]
                value_dict['SNIPPET'] = value[3]
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
    def _process_histologic_stage_text_list(self, histologic_stage_text_list):
        numeric_stage_context_regex = \
            re.compile('(?i)stage (.* )?' + numeric_stage())
        numeric_stage_regex = \
            ('[0-9IV]{1,3}([A-Za-z]([0-9])?)?((-|/)[0-9IV]{1,3}([A-Za-z]([0-9])?)?)?')
        nonnumeric_stage_context_regex = \
            re.compile('(?i)' + nonnumeric_stage() + ' stage')
        nonnumeric_stage_regex = \
            re.compile('(?i)' + nonnumeric_stage())
        in_situ_list = [ 'DCIS', 'LCIS', 'SCCIS', 'in situ' ]
        in_situ_regex = re.compile('(?i)' + regex_from_list(in_situ_list))
        for i in range(len(histologic_stage_text_list)):
            cancer_stage_text_raw = histologic_stage_text_list[i]
            cancer_stage_text_processed = []
            stage_val_list = self._extract_value(numeric_stage_context_regex, 
                                                 numeric_stage_regex,
                                                 self._map_to_cancer_stage,
                                                 cancer_stage_text_raw)
            for item in stage_val_list:
                if '-' in item:
                    item_list = item.split('-')
                    item0 = re.match('(?i)([0-9]+|[IV]+)', item_list[0])
                    item1 = re.match('(?i)([0-9]+|[IV]+)', item_list[1])
                    item = item0.group(0) + '-' + item1.group(0)
                else:
                    item = re.match('(?i)([0-9]+|[IV]+)', item)
                    item = item.group(0)
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
                histologic_stage_text_list[i] = cancer_stage_text_processed[0]
            else:
                histologic_stage_text_list[i] = 'MANUAL_REVIEW'
        return histologic_stage_text_list