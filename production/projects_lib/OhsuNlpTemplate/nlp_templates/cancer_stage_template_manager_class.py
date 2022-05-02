# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 17:18:08 2022

@author: haglers
"""

#
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
        seed_primary_template_list = \
            self._get_seed_primary_template_list()
        self._atomize_seed_primary_template_list(seed_primary_template_list)
        self._get_secondary_template_list()
            
    #
    def _annotate_seed_primary_template_list(self, seed_primary_template_list):
        cancer_sccis_value = self._nlp_cancer_sccis_value()
        cancer_stage_value = self._nlp_cancer_stage_value()
        cancer_type = self._nlp_cancer_type()
        for i in range(len(seed_primary_template_list)):
            seed_primary_template_list[i] = \
                re.sub('NLP_CANCER_SCCIS_VALUE', cancer_sccis_value, seed_primary_template_list[i])
            seed_primary_template_list[i] = \
                re.sub('NLP_CANCER_STAGE_VALUE', cancer_stage_value, seed_primary_template_list[i])
            seed_primary_template_list[i] = \
                re.sub('NLP_CANCER_TYPE', cancer_type, seed_primary_template_list[i] )
        return seed_primary_template_list
    
    #
    def _atomize_seed_primary_template_list(self, seed_primary_template_list):
        self.atomized_primary_template_list = []
        for i in range(len(seed_primary_template_list)):
            item = seed_primary_template_list[i]
            self.atomized_primary_template_list.append(item.split())
            
    #
    def _constitute_primary_template_list(self):
        primary_template_list = []
        for i in range(len(self.atomized_primary_template_list)):
            item = self.atomized_primary_template_list[i]
            primary_template_list.append('(?i)' + ' '.join(item))
        return primary_template_list

    #
    def _get_seed_primary_template_list(self):
        static_data = self.static_data_manager.get_static_data()
        validation_filename = 'ohsunlptemplate_templates.xlsx'
        directory_manager = static_data['directory_manager']
        project_name = static_data['project_name']
        data_dir = directory_manager.pull_directory('raw_data_dir')
        book = read_xlsx_file(os.path.join(data_dir, validation_filename))
        sheet = book.sheet_by_index(0)
        ncols = sheet.ncols
        nrows = sheet.nrows
        seed_primary_template_list = []
        for row_idx in range(nrows):
            if row_idx > 0:
                cell_value = sheet.cell_value(row_idx, 4)
                seed_primary_template_list.append(cell_value)
        return seed_primary_template_list
                
    #
    def _get_secondary_template_list(self):
        cancer_sccis_value = self._nlp_cancer_sccis_value()
        cancer_stage_value = self._nlp_cancer_stage_value()
        cancer_type = self._nlp_cancer_type()
        self.secondary_template_list = []
        self.secondary_template_list.append(['(?i)(' + \
                                            cancer_stage_value[1:-1] + \
                                            '|' + \
                                            cancer_sccis_value[1:-1] + \
                                            ')'])
        self.secondary_template_list.append(['(?i)' + cancer_type])
    
    #
    def _nlp_cancer_sccis_value(self):
        nlp_cancer_sccis_value = '('
        nlp_cancer_sccis_value += 'sccis'
        nlp_cancer_sccis_value += ')'
        return nlp_cancer_sccis_value
        
    #
    def _nlp_cancer_stage_value(self):
        nlp_cancer_stage_value = '('
        nlp_cancer_stage_value += 'stage [0-9IV]+'
        nlp_cancer_stage_value += ')'
        return nlp_cancer_stage_value
    
    #
    def _nlp_cancer_type(self):
        nlp_cancer_type = '('
        nlp_cancer_type += '[A-Za-z]*(carcinoma|sarcoma)'
        nlp_cancer_type += '|'
        nlp_cancer_type += '(cancer|CA)'
        nlp_cancer_type += '|'
        nlp_cancer_type += '(DLBCL|SCC)'
        nlp_cancer_type += ')'
        return nlp_cancer_type
        
    #
    def template(self):
        primary_template_list = \
            self._constitute_primary_template_list()
        primary_template_list = \
            self._annotate_seed_primary_template_list(primary_template_list)
        sections_list = None
        template_dict = {}
        template_dict['primary_template_list'] = primary_template_list
        template_dict['secondary_template_list'] = self.secondary_template_list
        template_dict['sections_list'] = sections_list
        template_dict['template_headers'] = [ 'Cancer Stage Extract',
                                              'Cancer Stage', 'Cancer Type' ]
        return template_dict