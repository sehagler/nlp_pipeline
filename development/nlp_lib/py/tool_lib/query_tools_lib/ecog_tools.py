# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 13:49:19 2019

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
        Postprocessor_base.__init__(self, project_data, label, data_file,
                                    data_key_map, data_value_map)
        self._get_ecog_status()
        
    #
    def _get_ecog_status(self):
        pattern = re.compile('[0-9]{1,3}%?(( ?\- ?| / )[0-9]{1,6}%?)?')
        for i in range(len(self.data_dict_list)):
            for key in self.data_dict_list[i][self.nlp_data_key]:
                try:
                    score_list = \
                        self.data_dict_list[i][self.nlp_data_key][key][self.label][self.nlp_text_element_key  + '0']
                except:
                    score_list = []
                try:
                    test_list = \
                        self.data_dict_list[i][self.nlp_data_key][key][self.label][self.nlp_text_element_key + '1']
                except:
                    test_list = []
                value_list = []
                for j in range(len(score_list)):
                    score = score_list[j]
                    test = test_list[j]
                    if re.search(pattern, score) is not None:
                        for m in re.finditer(pattern, score):
                            value = m.group(0)
                            value = re.sub('%', '', value)
                            value = re.sub('(\-|/)', ',', value)
                            value = re.sub(',', ' , ', value)
                            value = re.sub(' +', ' ', value)
                            if re.search(',', value) is not None:
                                values = value.split(' , ')
                                for k in range(len(values)):
                                    values[k] = int(values[k])
                                if test in [ 'karnofsky', 'lansky' ]:
                                    for k in range(len(values)):
                                        values[k] = self._map_to_zubrod(values[k])
                                values = [ int(x) for x in values ]
                                value = str(tuple(sorted(values)))
                            else:
                                if test in [ 'karnofsky', 'lansky' ]:
                                    value = self._map_to_zubrod(value)
                            value_list.append(value)
                self._append_data(i, key, value_list)
                    
    # map karnofsky and lansky value to zubrod values per
    # https://oncologypro.esmo.org/oncology-in-practice/practice-tools/performance-scales
    def _map_to_zubrod(self, value_in):
        if int(value_in) in range(96, 101):
            value_out = '0'
        elif int(value_in) in range(76, 96):
            value_out = '1'
        elif int(value_in) in range(56, 76):
            value_out = '2'
        elif int(value_in) in range(36, 56):
            value_out = '3'
        elif int(value_in) in range(6, 36):
            value_out = '4'
        elif int(value_in) in range(0, 6):
            value_out = '5'
        else:
            value_out = value_in
        return value_out
    
#
class Summarization(Preprocessor_base):
    
    #
    def process_ecog(self):
        self._general_command('(?i)(?<!{ )ecog( :)? (performance )?(status|score|ps)', {None : 'ECOG ( ZUBROD ) '})
        self._general_command('(?i)karnofsky (performance )?(status|score|ps)', {None : 'ECOG ( KARNOFSKY ) '})
        self._general_command('(?i)lansky (play performance )?(status|score|ps)', {None : 'ECOG ( LANSKY ) '})
        self._general_command('(?i)(?<!{ )ecog (?!\()', {None : 'ECOG ( ZUBROD ) '})