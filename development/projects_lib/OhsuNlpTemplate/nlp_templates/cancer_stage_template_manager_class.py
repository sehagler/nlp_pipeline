# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 17:18:08 2022

@author: haglers
"""

#
import ast
import os
import re

#
from tool_lib.py.processing_tools_lib.file_processing_tools \
    import read_xlsx_file, write_file, xml_diff
    
#
class Cancer_stage_template_manager(object):
    
    #
    def __init__(self, static_data_manager):
        self.static_data_manager = static_data_manager
        self._get_secondary_template_list()
            
    #
    def _annotate_primary_template_list(self, primary_template_list):
        cancer_scc_value = self._nlp_cancer_scc_value()
        cancer_stage_value = self._nlp_cancer_stage_value()
        cancer_type = self._nlp_cancer_type()
        for i in range(len(primary_template_list)):
            primary_template_list[i] = \
                re.sub('NLP_CANCER_SCC_VALUE', cancer_scc_value, primary_template_list[i])
            primary_template_list[i] = \
                re.sub('NLP_CANCER_STAGE_VALUE', cancer_stage_value, primary_template_list[i])
            primary_template_list[i] = \
                re.sub('NLP_CANCER_TYPE', cancer_type, primary_template_list[i] )
        return primary_template_list
    
    #
    def _atomize_primary_template_outline(self, primary_template_outline):
        atomized_primary_template_list = []
        for i in range(len(primary_template_outline)):
            item = primary_template_outline[i]
            atomized_primary_template_list.append(item.split())
        return atomized_primary_template_list
            
    #
    def _constitute_primary_template_list(self, atomized_primary_template_list):
        primary_template_list = []
        for i in range(len(atomized_primary_template_list)):
            item = atomized_primary_template_list[i]
            primary_template_list.append('(?i)' + ' '.join(item))
        return primary_template_list
                
    #
    def _get_secondary_template_list(self):
        cancer_scc_value = self._nlp_cancer_scc_value()
        cancer_stage_value = self._nlp_cancer_stage_value()
        cancer_type = self._nlp_cancer_type()
        self.secondary_template_list = []
        self.secondary_template_list.append(['(?i)(' + \
                                            cancer_stage_value[1:-1] + \
                                            '|' + \
                                            cancer_scc_value[1:-1] + \
                                            ')'])
        self.secondary_template_list.append(['(?i)' + cancer_type])
    
    #
    def _nlp_cancer_scc_value(self):
        nlp_cancer_sccis_value = '('
        nlp_cancer_sccis_value += 'scc(is)?'
        nlp_cancer_sccis_value += ')'
        return nlp_cancer_sccis_value
        
    #
    def _nlp_cancer_stage_value(self):
        nlp_cancer_stage_value = '('
        nlp_cancer_stage_value += 'stage [0-9IV]+([A-Za-z]([0-9]+)?)?'
        nlp_cancer_stage_value += '|'
        nlp_cancer_stage_value += '(early|end|extensive|mild|severe) stage'
        nlp_cancer_stage_value += '|'
        nlp_cancer_stage_value += 'in situ'
        nlp_cancer_stage_value += ')'
        return nlp_cancer_stage_value
    
    #
    def _nlp_cancer_type(self):
        nlp_cancer_type = '('
        nlp_cancer_type += '[A-Za-z]+(oma|CA)'
        nlp_cancer_type += '|'
        nlp_cancer_type += '(cancer|CA|metastasis|nodule)'
        nlp_cancer_type += '|'
        nlp_cancer_type += '(DLBCL|IDC|(R\-)?ISS|NSCLC)'
        nlp_cancer_type += ')'
        return nlp_cancer_type
    
    #
    def push_primary_template_outline(self, primary_template_outline):
        atomized_primary_template_list = \
            self._atomize_primary_template_outline(primary_template_outline)
        primary_template_list = \
            self._constitute_primary_template_list(atomized_primary_template_list)
        self.primary_template_list = \
            self._annotate_primary_template_list(primary_template_list)
        
    #
    def training_template(self):
        template_dict = {}
        template_dict['primary_template_list'] = self.primary_template_list
        template_dict['secondary_template_list'] = self.secondary_template_list
        template_dict['sections_list'] = None
        template_dict['template_headers'] = [ 'Cancer Stage Extract',
                                              'Cancer Stage', 'Cancer Type' ]
        return template_dict
    
    #
    def template(self):
        static_data = self.static_data_manager.get_static_data()
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