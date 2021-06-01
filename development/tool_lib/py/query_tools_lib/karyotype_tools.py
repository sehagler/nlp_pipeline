# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 14:28:01 2019

@author: haglers
"""

#
import re

#
from nlp_lib.py.postprocessing_lib.base_class_lib.postprocessor_base_class \
    import Postprocessor_base
from nlp_lib.py.document_preprocessing_lib.base_class_lib.preprocessor_base_class \
    import Preprocessor_base

#
class Named_entity_recognition(Preprocessor_base):
    
    #
    def process_karyotype(self):
        self._general_command('(?i)inversion \(', {None : 'inv('})

#
class Postprocessor(Postprocessor_base):
    
    #
    def __init__(self, project_data, data_file, label):
        Postprocessor_base.__init__(self, project_data, label, data_file)
        for i in range(len(self.data_dict_list)):
            self.data_dict_list[i][self.nlp_data_key] = {}
        self._create_data_structure('(KARYOTYPE \d|IMPRESSIONS AND RECOMMENDATIONS \d)')
        self._extract_data_values()
        
    #
    def _extract_data_value(self, text_list):
        if len(text_list) > 0:
            text_list = text_list[0]
        entry_text = text_list[0]
        if entry_text[-1] == ',':
            entry_text = entry_text[:-1]
        entry_text = re.sub('(?i)karyotype results : ', '', entry_text)
        entry_text = re.sub('\]' , '] ', entry_text)
        entry_text = re.sub(' +', ' ', entry_text)
        entry_text = re.sub('(?<=\]) ?[0-9A-Za-z(].*', '', entry_text)
        entry_text = re.sub('[ \n]', '', entry_text)
        entry_text = re.sub('&lt;', '<', entry_text)
        entry_text = re.sub('&gt;', '>', entry_text)
        try:
            if entry_text[:2] == '//':
                entry_text = entry_text[2:]
        except:
            pass
        match_str = '([0-9]{1,2}~)?[0-9]{1,2},[XY]+.*\[.+]'
        match = re.search(match_str, entry_text)
        if match is not None:
            karyotype = match.group(0)
            try:
                atomized_karyotype = atomize_karyotype(karyotype)
            except:
                atomized_karyotype = ''
            value_list = []
            value_list.append(entry_text)
        else:
            value_list = []
        value_dict_list = []
        for value in value_list:
            value_dict = {}
            value_dict['KARYOTYPE'] = value
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