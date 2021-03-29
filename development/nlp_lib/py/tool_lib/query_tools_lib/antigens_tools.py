# -*- coding: utf-8 -*-
"""
Created on Fri Mar 08 12:42:14 2019

@author: haglers
"""

#
import re

#
from nlp_lib.py.base_class_lib.postprocessor_base_class import Postprocessor_base
from nlp_lib.py.base_class_lib.preprocessor_base_class import Preprocessor_base

#
class Postprocessor(Postprocessor_base):
    
    #
    def __init__(self, project_data, data_file, data_key_map, data_value_map,
                 label):
        Postprocessor_base.__init__(self, project_data, label, data_file, None, 
                                    None)
        for i in range(len(self.data_dict_list)):
            self.data_dict_list[i][self.nlp_data_key] = {}
        self._create_data_structure('ANTIBODIES TESTED \d')
        self._get_antibodies_tested_list()
                    
    #
    def _get_antibodies_tested_list(self):
        for i in range(len(self.data_dict_list)):
            for key in self.data_dict_list[i][self.nlp_data_key]:
                entry_text = \
                    self.data_dict_list[i][self.nlp_data_key][key][self.label][self.nlp_text_key]
                entry_text_tmp = re.sub('/', ' ', entry_text[0])
                antibodies = list(set(entry_text_tmp.split()))
                nonantibodies = []
                for element in antibodies:
                    if not is_antibody(element):
                        nonantibodies.append(element)
                nonantibodies = list(set(nonantibodies))
                for nonantibody in nonantibodies:
                    antibodies.remove(nonantibody)
                antibodies.sort()
                if antibodies != []:
                    self._append_data(i, key, antibodies)

#
class Posttokenizer(Preprocessor_base):
    
    #
    def process_antigens(self):
        antigens = antigens_list()
        self._general_command('HLA ?DR', {None : 'HLA-DR'})
        self._general_command('(?i)dim(-| (/ )?)partial', {None : 'dim/partial'})
        self._general_command('(?i)dim (/ )?variable', {None : 'dim/variable'})
        self._general_command('(?i)(bright|dim|low|moderate|partial|subset|variable)CD', {None : ' CD'})
        self._general_command('(?i)partial (/ )?dim', {None : 'dim/partial'})
        self._general_command('(?<=CD) (?=[0-9])', {None : ''})
        self._general_command(antigens + '\(', {'\(' : ' ('})
        self._general_command(antigens + ' : ' + antigens, {' : ' : ':'})
        self._general_command(antigens + ' / ' + antigens, {' / ' : '/'})
        self._general_command(antigens + '-negative', {'-negative' : ' negative'})
        self._general_command(antigens + '-positive', {'-positive' : ' positive'})
        self._general_command(antigens + '-', {'-' : ' negative '})
        self._general_command(antigens + ' *\+', {'\+' : ' positive '})
        self._general_command(antigens + ' *\( \+ \)', {'\( \+ \)' : ' positive'})
        self._general_command('(?<=HLA) (negative|positive)(?=DR)', {None : '-'})

#
def antigens_list():
    return '([a-z]?CD[0-9]+|HLA-DR|MPO|T[Dd]T|kappa)'

#
def correct_antibodies(text):
    #text = re.sub('(?i)(\+|\-positive)', '', text)
    text = re.sub('HLA *- *DR', 'HLA-DR', text)
    return text

#
def extract_antigens(text):
    antigen_list = []
    tokens = text.split(' ')
    for token in tokens:
        if is_antibody(token):
            antigen_list.append(token)
    return antigen_list

#
def is_antibody(text, lower_flg=False):
    match_str = '^('
    match_str += '[a-z]?CD[0-9]+[a-z]?( \(subset\))?'
    match_str += '|HLA-DR'
    match_str += '|[a-z]?Kappa[a-z]?( \(mono\))?'
    match_str += '|[a-z]?Lambda[a-z]?( \(mono\))?'
    match_str += '|[a-z]?MPO'
    match_str += '|[a-z]?T[Dd]T'
    match_str += ')$'
    if lower_flg:
        match_str = match_str.lower()
    if re.match(match_str, text):
        return True
    else:
        return False
 
#
def is_antibody_value(text):
    match_str = '(?i)^('
    match_str += 'bright'
    match_str += '|dim(inished)?'
    match_str += '|focal'
    match_str += '|low'
    match_str += '|partial/dim'
    match_str += '|partial'
    match_str += '|variable'
    match_str += ')$'
    if re.match(match_str, text):
        return True
    else:
        return False