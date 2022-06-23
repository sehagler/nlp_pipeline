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
from tool_lib.py.query_tools_lib.cancer_tools \
    import get_initialisms, nonnumeric_stage, numeric_stage
    
#
class Cancer_stage_template_manager(object):
    
    #
    def __init__(self, static_data_manager):
        self.static_data_manager = static_data_manager
        self._get_secondary_template_list()
        self.blank_space = ' NLP_BLANK_SPACE '
            
    #
    def _annotate_primary_template_list(self, primary_template_list):
        cancer_is_value = self._nlp_cancer_is_value()
        cancer_stage_value = self._nlp_cancer_stage_value()
        cancer_type = self._nlp_cancer_type()
        for i in range(len(primary_template_list)):
            primary_template_list[i] = \
                re.sub('NLP_CANCER_IS_VALUE', cancer_is_value, primary_template_list[i])
            primary_template_list[i] = \
                re.sub('NLP_CANCER_STAGE_VALUE', cancer_stage_value, primary_template_list[i])
            primary_template_list[i] = \
                re.sub('NLP_CANCER_TYPE', cancer_type, primary_template_list[i] )
        return primary_template_list
    
    #
    def _finish_templates(self, template_list):
        for i in range(len(template_list)):
            template_list[i] = \
                re.sub(self.blank_space, '[ \n\r]', template_list[i])
            template_list[i] = \
                template_list[i].replace('[^A-Za-z0-9 ]+[ \n\r]', '([^A-Za-z0-9 ]+[ \n\r])?')
            template_list[i] = '(?i)' + template_list[i]
        #for i in range(len(template_list)):
        #    template_list[i] = \
        #        '(?i)(?<![A-Za-z0-9])' + template_list[i]
        #    template_list[i] += '(?![A-Za-z0-9])'
        return template_list
    
    #
    def _generate_XY_field_list(self, primary_template_list, A_label, B_label):
        AB_field_list = []
        for i in range(len(primary_template_list)):
            template_list = primary_template_list[i].split(self.blank_space)
            if A_label in template_list:
                A_idx = template_list.index(A_label)
            else:
                A_idx = None
            if B_label in template_list:
                B_idx = template_list.index(B_label)
            else:
                B_idx = None
            if A_idx is not None and B_idx is not None:
                field_idxs = list(range(A_idx+1, B_idx))
                field_list = []
                for j in range(len(field_idxs)):
                    field_list.append(template_list[field_idxs[j]])
                AB_field_list.append(self.blank_space.join(field_list))
        AB_field_list = list(set(AB_field_list))
        AB_field_list = sorted(AB_field_list, key=len, reverse=True)
        if '' in AB_field_list:
            AB_field_list.remove('')
        AB_field_list = \
            self._finish_templates(AB_field_list)
        return AB_field_list
        
    
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
    def push_primary_template_outline(self, primary_template_list):
        self.AB_field_list = \
            self._generate_XY_field_list(primary_template_list,
                                         'NLP_CANCER_TYPE',
                                         'NLP_CANCER_STAGE_VALUE')
        self.BA_field_list = \
            self._generate_XY_field_list(primary_template_list,
                                         'NLP_CANCER_STAGE_VALUE',
                                         'NLP_CANCER_TYPE')
        primary_template_list = \
            self._finish_templates(primary_template_list)
        self.primary_template_list = \
            self._annotate_primary_template_list(primary_template_list)
        
    #
    def training_template(self):
        template_dict = {}
        template_dict['AB_field_list'] = self.AB_field_list
        template_dict['BA_field_list'] = self.BA_field_list
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