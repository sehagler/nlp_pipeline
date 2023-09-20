# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 14:28:01 2019

@author: haglers
"""

#
from base_lib.evaluator_base_class import Evaluator_base
from base_lib.postprocessor_base_class import Postprocessor_base
import lambda_lib.tool_lib.lambda_tools as lambda_tools
from tools_lib.regex_lib.regex_tools \
    import (
        comma,
        s,
        tilde
    )

#
def atomize_karyotype(full_karyotype):
    karyotype_atoms = {}
    karyotypes_0 = full_karyotype.split('//')
    for karyotype_0 in karyotypes_0:
        karyotypes_1 = karyotype_0.split('/')
        for karyotype_1 in karyotypes_1:
            karyotype_1 = karyotype_1.split('[')
            if len(karyotype_1) == 2:
                count = '[' + karyotype_1[1]
            else:
                count = ''
            karyotype_1 = karyotype_1[0]
            karyotype_1_atoms = karyotype_1.split(',')
            if 'chromosome count' not in karyotype_atoms.keys():
                karyotype_atoms['chromosome count'] = karyotype_1_atoms[0] + count
            else:
                karyotype_atoms['chromosome count'] += '/' + karyotype_1_atoms[0] + count
            if 'sex chromosomes' not in karyotype_atoms.keys():
                karyotype_atoms['sex chromosomes'] = karyotype_1_atoms[1] + count
            else:
                karyotype_atoms['sex chromosomes'] += '/' + karyotype_1_atoms[1] + count
            for i in range(len(karyotype_1_atoms)-2):
                if karyotype_1_atoms[i+2] not in karyotype_atoms.keys():
                    karyotype_atoms[karyotype_1_atoms[i+2]] = count
                else:
                    karyotype_atoms[karyotype_1_atoms[i+2]] += '/' + count
    return karyotype_atoms

#
def simple_template():
    template = '([0-9]{1,2}' + tilde() + ')?[0-9]{1,2}' + comma() + '[XY]+.*\[[0-9]+\]'
    template_list = []
    template_list.append(template)
    sections_list = [ 'KARYOTYPE', 'IMPRESSIONS AND RECOMMENDATIONS' ]
    template_dict = {}
    template_dict['primary_template_list'] = template_list
    template_dict['sections_list'] = sections_list
    template_dict['template_headers'] = [ 'Karyotype' ]
    return template_dict

#
class Evaluator(Evaluator_base):
    
    #
    def run_object(self, evaluation_manager, nlp_value, validation_value,
                 display_flg):
        if nlp_value is not None:
            
            # kludge to get BeatAML projects working
            if isinstance(nlp_value, list) and not isinstance(nlp_value, str):
                nlp_value = list(set(nlp_value))
                if len(nlp_value) > 1:
                    nlp_value = self.manual_review
                else:
                    nlp_value = nlp_value[0][0]
            # kludge to get BeatAML projects working
                    
            nlp_value = nlp_value.replace('//', '/')
            nlp_value_tmp = nlp_value
            nlp_value_tmp = nlp_value_tmp.replace(' ', '')
            nlp_value = []
            nlp_value.append(nlp_value_tmp)
        if nlp_value is not None:
            nlp_value = tuple(nlp_value)
        else:
            nlp_value = None
        if validation_value is not None:
            validation_value = validation_value.replace('//', '/')
            if validation_value == '':
                validation_value = None
            if validation_value == 'N/A':
                validation_value = None
            if validation_value == 'Not available':
                validation_value = None
            if validation_value == 'None':
                validation_value = None
        if validation_value is not None:
            validation_value_tmp = validation_value
            validation_value_tmp = \
                validation_value_tmp.replace(' ', '')
            validation_value = []
            validation_value.append(validation_value_tmp)
        if validation_value is not None:
            validation_value = tuple(validation_value)
        arg_dict = {}
        arg_dict['display_flg'] = display_flg
        arg_dict['nlp_value'] = nlp_value
        arg_dict['validation_value'] = validation_value
        ret_dict = evaluation_manager.evaluation(arg_dict)
        return ret_dict['performance']
    
#
class Postprocessor(Postprocessor_base):
        
    #
    def _extract_data_value(self, value_list_dict):
        extracted_data_dict = {}
        for key in value_list_dict.keys():
            text_list = value_list_dict[key]
            karyotype = []
            snippet = []
            for item in text_list[0]:
                karyotype.append(item[0])
                snippet.append(item[1])
            value_dict_list = []
            for i in range(len(karyotype)):
                value_dict = {}
                value_dict['KARYOTYPE'] = karyotype[i].replace(' ', '')
                value_dict['SNIPPET'] = snippet[i]
                value_dict_list.append(value_dict)
            extracted_data_dict[key] = value_dict_list
        return extracted_data_dict

#
class Preprocessor(object):
    
    #
    def run_preprocessor(self, text):
        text = \
            lambda_tools.lambda_conversion('\) \(', text, ')(')
        text = \
            lambda_tools.lambda_conversion('\) \[', text, ')[')
        text = \
            lambda_tools.lambda_conversion('\] \(', text, '](')
        text = \
            lambda_tools.contextual_lambda_conversion('\( [pq]?[0-9\.]+[ ;]+[pq]?[0-9\.]+ ?\)', '\( ', text, '(')
        text = \
            lambda_tools.contextual_lambda_conversion('\( ?[pq]?[0-9\.]+[ ;]+[pq]?[0-9\.]+ \)', ' \)', text, ')')
        text = \
            lambda_tools.lambda_conversion('(?<=[XY]) \[', text, '[')
        text = \
            lambda_tools.lambda_conversion('(?<=[0-9]) , (?=[XY])', text, ',')
        text = \
            lambda_tools.contextual_lambda_conversion('\([pq]?[0-9\.]+ ; [pq]?[0-9\.]+\)', ' ; ', text, ';')
        text = \
            lambda_tools.contextual_lambda_conversion('[0-9]{1,2},[XY]+(\S*(\(\S+\)|\-[0-9]+))? , (\+|\-)?((add|inv)\(|mar|[0-9])', ' , ', text, ',')
        text = \
            lambda_tools.contextual_lambda_conversion('[0-9]{1,2},[XY]+\S* / [0-9]{1,2},[XY]+', ' / ', text, '/')
        text = \
            lambda_tools.contextual_lambda_conversion('([0-9]{1,2}~)?[0-9]{1,2},[XY]+.*\[.+]', ' ', text, '')
        text = \
            lambda_tools.lambda_conversion('(?i)inversion \(', text, 'inv(')
        return text
    
#
class Section_header_structure():
    
    #
    def add_section_header(self, section_header_dict):
        regex_dict = {}
        regex_list = []
        regex_list.append('karyotype' + s())
        regex_list.append('karyotype result' + s())
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        section_header_dict['KARYOTYPE'] = regex_dict
        return section_header_dict