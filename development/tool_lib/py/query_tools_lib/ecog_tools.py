# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 13:49:19 2019

@author: haglers
"""

#
import re

#
from nlp_lib.py.postprocessing_lib.base_class_lib.postprocessor_base_class \
    import Postprocessor_base
from nlp_lib.py.document_preprocessing_lib.base_class_lib.preprocessor_base_class import Preprocessor_base

#
class Postprocessor(Postprocessor_base):
    
    #
    def __init__(self, project_data, data_file, label):
        Postprocessor_base.__init__(self, project_data, label, data_file)
        self._extract_data_values()
        
    #
    def _extract_data_value(self, text_list):
        if len(text_list) > 0:
            ecog_score_text_list = text_list[1]
            test_text_list = text_list[2]
            context_text_list = text_list[3]
        else:
            ecog_score_text_list = []
            test_text_list = []
            context_text_list = []
        value_list = []
        normalized_ecog_score_text_list = \
            self._process_ecog_score_text_list(ecog_score_text_list, test_text_list)
        value_list = []
        for i in range(len(ecog_score_text_list)):
            value_list.append((ecog_score_text_list[i],
                               normalized_ecog_score_text_list[i],
                               test_text_list[i],
                               context_text_list[i]))
        value_list = list(set(value_list))
        value_dict_list = []
        for value in value_list:
            value_dict = {}
            value_dict['ECOG_SCORE'] = value[0]
            value_dict['NORMALIZED_ECOG_SCORE'] = value[1]
            value_dict['ECOG_TEST'] = value[2]
            value_dict['CONTEXT'] = value[3]
            value_dict_list.append(value_dict)
        return value_dict_list
                    
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
    def _process_ecog_score_text_list(self, score_list, test_list):
        pattern = re.compile('[0-9]{1,3}%?(( ?\- ?| / )[0-9]{1,6}%?)?')
        processed_score_list = []
        for i in range(len(score_list)):
            score_raw = score_list[i]
            test = test_list[i]
            if re.search(pattern, score_raw) is not None:
                for m in re.finditer(pattern, score_raw):
                    score_processed = m.group(0)
                    score_processed = re.sub('%', '', score_processed)
                    score_processed = re.sub('(\-|/)', ',', score_processed)
                    score_processed = re.sub(',', ' , ', score_processed)
                    score_processed = re.sub(' +', ' ', score_processed)
                    if re.search(',', score_processed) is not None:
                        scores_processed = score_processed.split(' , ')
                        for k in range(len(scores_processed)):
                            scores_processed[k] = int(scores_processed[k])
                        if test in [ 'karnofsky', 'lansky' ]:
                            for k in range(len(scores_processed)):
                                scores_processed[k] = \
                                    self._map_to_zubrod(scores_processed[k])
                        scores_processed = [ int(x) for x in scores_processed ]
                        score_processed = str(tuple(sorted(scores_processed)))
                    else:
                        if test in [ 'karnofsky', 'lansky' ]:
                            score_processed = self._map_to_zubrod(score_processed)
            processed_score_list.append(score_processed)
        return processed_score_list
        
    
#
class Summarization(Preprocessor_base):
    
    #
    def process_ecog(self):
        self._general_command('(?i)(?<!{ )ecog( :)? (performance )?(status|score|ps)', {None : 'ECOG ( ZUBROD ) '})
        self._general_command('(?i)karnofsky (performance )?(status|score|ps)', {None : 'ECOG ( KARNOFSKY ) '})
        self._general_command('(?i)lansky (play performance )?(status|score|ps)', {None : 'ECOG ( LANSKY ) '})
        self._general_command('(?i)(?<!{ )ecog (?!\()', {None : 'ECOG ( ZUBROD ) '})