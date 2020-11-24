# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 14:28:01 2019

@author: haglers
"""

#
import re

#
from nlp_lib.py.base_class_lib.postprocessor_base_class import Postprocessor_base
from nlp_lib.py.base_class_lib.preprocessor_base_class import Preprocessor_base

#
class Named_entity_recognition(Preprocessor_base):
    
    #
    def process_karyotype(self):
        self._general_command('(?i)inversion \(', {None : 'inv('})

#
class Postprocessor(Postprocessor_base):
    
    #
    def __init__(self, csv_file):
        Postprocessor_base.__init__(self, csv_file, None, None, None)
        for i in range(len(self.data_dict_list)):
            self.data_dict_list[i]['DATA'] = {}
        self._get_karyotype()
        
    #
    def _get_karyotype(self):
        for i in range(len(self.data_dict_list)):
            for entry in self.data_dict_list[i]['DOCUMENT_FRAME']:
                entry_tmp = ''
                for j in range(len(entry)-1):
                    entry_tmp += entry[j+1]
                if entry_tmp[-1] == ',':
                    entry_tmp = entry_tmp[:-1]
                entry_tmp = re.sub('[ \n]', '', entry_tmp)
                entry_tmp = re.sub('(?i)karyotyperesults[:\.]', '', entry_tmp)
                entry_tmp = re.sub('(?i)impressionsandrecommendations[:\.]', '', entry_tmp)
                entry_tmp = re.sub('(?i)(all)?[0-9]+(of[0-9]+)?metaphasecell.*', '', entry_tmp)
                try:
                    if entry_tmp[:2] == '//':
                        entry_tmp = entry_tmp[2:]
                except:
                    pass
                if re.match('KARYOTYPE \d', entry[0][0]) or re.match('IMPRESSIONS AND RECOMMENDATIONS \d', entry[0][0]):
                    match_str = '([0-9]{1,2}~)?[0-9]{1,2},[XY]+.*\[.+]'
                    match = re.search(match_str, entry_tmp)
                    if match is not None:
                        key = entry[0]
                        #atomized_karyotype = atomize_karyotype(match)
                        if key not in self.data_dict_list[i]['DATA'].keys():
                            self.data_dict_list[i]['DATA'][key] = {}
                        if 'KARYOTYPE TEXT' not in self.data_dict_list[i]['DATA'][key].keys():
                            self.data_dict_list[i]['DATA'][key]['KARYOTYPE TEXT'] = []
                        self.data_dict_list[i]['DATA'][key]['KARYOTYPE TEXT'].append(entry_tmp)
                        #if 'KARYOTYPE VALUE' not in self.data_dict_list[i]['DATA'][key].keys():
                        #    self.data_dict_list[i]['DATA'][key]['KARYOTYPE VALUE'] = []
                        #self.data_dict_list[i]['DATA'][key]['KARYOTYPE VALUE'].append(atomized_karyotype)

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