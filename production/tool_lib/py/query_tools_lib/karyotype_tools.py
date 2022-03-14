# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 14:28:01 2019

@author: haglers
"""

#
import re

#
from nlp_lib.py.base_lib.postprocessor_base_class \
    import Postprocessor_base
from nlp_lib.py.base_lib.preprocessor_base_class \
    import Preprocessor_base

#
class Named_entity_recognition(Preprocessor_base):
    
    #
    def run_preprocessor(self):
        self._normalize_whitespace()
        self._general_command('(?i)inversion \(', {None : 'inv('})

#
class Postprocessor(Postprocessor_base):
        
    #
    def _extract_data_value(self, text_list):
        karyotype = []
        snippet = []
        for item in text_list[0]:
            karyotype.append(item[0])
            snippet.append(item[1])
        value_dict_list = []
        for i in range(len(karyotype)):
            value_dict = {}
            value_dict['KARYOTYPE'] = karyotype[i]
            value_dict['SNIPPET'] = snippet[i]
            value_dict_list.append(value_dict)
        return value_dict_list

#
class Posttokenizer(Preprocessor_base):
        
    #
    def process_karyotype(self):
        self._general_command('\) \(', {None : ')('})
        self._general_command('\) \[', {None : ')['})
        self._general_command('\] \(', {None : ']('})
        self._general_command('\( [pq]?[0-9\.]+[ ;]+[pq]?[0-9\.]+ ?\)', {'\( ' : '('})
        self._general_command('\( ?[pq]?[0-9\.]+[ ;]+[pq]?[0-9\.]+ \)',  {' \)' : ')'})
        self._general_command('(?<=[XY]) \[', {None : '['})
        self._general_command('(?<=[0-9]) , (?=[XY])', {None : ','})
        self._general_command('\([pq]?[0-9\.]+ ; [pq]?[0-9\.]+\)', {' ; ' : ';'})
        self._general_command('[0-9]{1,2},[XY]+(\S*(\(\S+\)|\-[0-9]+))? , (\+|\-)?((add|inv)\(|mar|[0-9])', 
                              {' , ' : ','})
        self._general_command('[0-9]{1,2},[XY]+\S* / [0-9]{1,2},[XY]+', {' / ' : '/'})
        self._general_command('([0-9]{1,2}~)?[0-9]{1,2},[XY]+.*\[.+]', {' ' : ''})
        
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
def template():
    template = '([0-9]{1,2} \~ )?[0-9]{1,2},[XY]+.*\[[0-9]+\]'
    template_sections_list = [ 'KARYOTYPE', 'IMPRESSIONS AND RECOMMENDATIONS' ]
    return template, template_sections_list