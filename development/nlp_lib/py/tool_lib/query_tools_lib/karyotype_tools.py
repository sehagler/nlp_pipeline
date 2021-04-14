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
from nlp_lib.py.base_class_lib.preprocessor_base_class import Preprocessor_base

#
class Named_entity_recognition(Preprocessor_base):
    
    #
    def process_karyotype(self):
        self._general_command('(?i)inversion \(', {None : 'inv('})

#
class Postprocessor(Postprocessor_base):
    
    #
    def __init__(self, project_data, data_file, data_key_map, data_value_map,
                 label):
        Postprocessor_base.__init__(self, project_data, label, data_file, None,
                                    None)
        for i in range(len(self.data_dict_list)):
            self.data_dict_list[i][self.nlp_data_key] = {}
        self._create_data_structure('(KARYOTYPE \d|IMPRESSIONS AND RECOMMENDATIONS \d)')
        self._get_karyotype()
        
    #
    def _get_karyotype(self):
        for i in range(len(self.data_dict_list)):
            del_keys = []
            for key in self.data_dict_list[i][self.nlp_data_key]:
                entry_text = \
                    self.data_dict_list[i][self.nlp_data_key][key][self.label][self.nlp_text_key][0]
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
                    self.data_dict_list[i][self.nlp_data_key][key][self.label][self.nlp_text_key] = []
                    self.data_dict_list[i][self.nlp_data_key][key][self.label][self.nlp_text_key].append(entry_text)
                    self._append_data(i, key, atomized_karyotype)
                else:
                    del_keys.append(key)
            for key in del_keys:
                del self.data_dict_list[i][self.nlp_data_key][key]

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