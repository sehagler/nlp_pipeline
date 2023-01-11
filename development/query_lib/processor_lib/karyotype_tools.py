# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 14:28:01 2019

@author: haglers
"""

#
from base_lib.postprocessor_base_class import Postprocessor_base
from base_lib.preprocessor_base_class import Preprocessor_base
import lambda_lib.object_lib.lambda_object_class as lambda_lib
from tools_lib.regex_lib.regex_tools \
    import (
        comma,
        s,
        tilde
    )

#
class Preprocessor(Preprocessor_base):
    
    #
    def run_preprocessor(self):
        text = self.text
        text = \
            lambda_lib.lambda_conversion('\) \(', text, ')(')
        text = \
            lambda_lib.lambda_conversion('\) \[', text, ')[')
        text = \
            lambda_lib.lambda_conversion('\] \(', text, '](')
        text = \
            lambda_lib.contextual_lambda_conversion('\( [pq]?[0-9\.]+[ ;]+[pq]?[0-9\.]+ ?\)', '\( ', text, '(')
        text = \
            lambda_lib.contextual_lambda_conversion('\( ?[pq]?[0-9\.]+[ ;]+[pq]?[0-9\.]+ \)', ' \)', text, ')')
        text = \
            lambda_lib.lambda_conversion('(?<=[XY]) \[', text, '[')
        text = \
            lambda_lib.lambda_conversion('(?<=[0-9]) , (?=[XY])', text, ',')
        text = \
            lambda_lib.contextual_lambda_conversion('\([pq]?[0-9\.]+ ; [pq]?[0-9\.]+\)', ' ; ', text, ';')
        text = \
            lambda_lib.contextual_lambda_conversion('[0-9]{1,2},[XY]+(\S*(\(\S+\)|\-[0-9]+))? , (\+|\-)?((add|inv)\(|mar|[0-9])', ' , ', text, ',')
        text = \
            lambda_lib.contextual_lambda_conversion('[0-9]{1,2},[XY]+\S* / [0-9]{1,2},[XY]+', ' / ', text, '/')
        text = \
            lambda_lib.contextual_lambda_conversion('([0-9]{1,2}~)?[0-9]{1,2},[XY]+.*\[.+]', ' ', text, '')
        text = \
            lambda_lib.lambda_conversion('(?i)inversion \(', text, 'inv(')
        self.text = text

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
def karyotype_performance(validation_data_manager, evaluation_manager,
                          labId, nlp_values, nlp_datum_key,
                          validation_datum_key):
    validation_data = validation_data_manager.get_validation_data()
    if labId in nlp_values.keys():
        keys0 = list(nlp_values[labId])
        if nlp_datum_key in nlp_values[labId][keys0[0]].keys():
            data_out = nlp_values[labId][keys0[0]][nlp_datum_key]
        else:
            data_out = None
    else:
        data_out = None
    if data_out is not None:
        
        # kludge to get BeatAML projects working
        if isinstance(data_out, list) and not isinstance(data_out, str):
            data_out = list(set(data_out))
            if len(data_out) > 1:
                data_out = 'MANUAL_REVIEW'
            else:
                data_out = data_out[0][0]
        # kludge to get BeatAML projects working
                
        data_out = data_out.replace('//', '/')
        data_out_tmp = data_out
        data_out_tmp = \
            data_out_tmp.replace(' ', '')
        data_out = []
        data_out.append(data_out_tmp)
    if data_out is not None:
        nlp_value = tuple(data_out)
    else:
        nlp_value = None
    labid_idx = validation_data[0].index('labId')
    validation_datum_idx = validation_data[0].index(validation_datum_key)
    validation_value = None
    for item in validation_data:
        if item[labid_idx] == labId:
            validation_value = item[validation_datum_idx]
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
    display_flg = True
    performance = \
        evaluation_manager.evaluation(nlp_value, validation_value, display_flg)
    return performance

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