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

#
class Postprocessor(Postprocessor_base):
    
    #
    def __init__(self, project_data, data_file, data_key_map, data_value_map,
                 label):
        Postprocessor_base.__init__(self, project_data, label, data_file,
                                    data_key_map, data_value_map)
        self._get_cancer_stage()
        
    #
    def _get_cancer_stage(self):
        switch_dict = {}
        switch_dict['0'] = '0'
        switch_dict['1'] = 'I'
        switch_dict['2'] = 'II'
        switch_dict['3'] = 'III'
        switch_dict['4'] = 'IV'
        switch_dict['5'] = 'V'
        pattern0 = \
            re.compile('(?i)stage( is now)? [IV]{1,3}([A-Da-d][0-9]?)?( (\-|/) [IV]{1,3}([A-Da-d][0-9]?)?)?( |$)')
        pattern1 = \
            re.compile('(?i)stage( is now)? [0-5]([A-Da-d][0-9]?)?( (\-|/) [0-5]([A-Da-d][0-9]?)?)?( |$)')
        for i in range(len(self.data_dict_list)):
            for key in self.data_dict_list[i][self.nlp_data_key]:
                try:
                    text_list = \
                        self.data_dict_list[i][self.nlp_data_key][key][self.label][self.nlp_text_key]
                except:
                    text_list = []
                value_list = []
                for text in text_list:
                    stage_0_flg = False
                    stage_0_text_list = [ 'DCIS', 'LCIS', 'SCCIS', 'in situ' ]
                    for item in stage_0_text_list:
                        if re.search('(?i)' + item, text) is not None:
                            stage_0_flg = True
                    if re.search(pattern0, text) is not None:
                        for m in re.finditer(pattern0, text):
                            value = m.group(0)
                            value = re.sub('(?i)stage( is now)?', '', value)
                            value = re.sub(' ', '', value)
                            value = re.sub('[A-Da-d][0-9]?', '', value)
                            value_list.append(value)
                    elif re.search(pattern1, text) is not None:
                        for m in re.finditer(pattern1, text):
                            value = m.group(0)
                            value = re.sub('(?i)stage( is now)?', '', value)
                            value = re.sub(' ', '', value)
                            value = re.sub('[A-Da-d][0-9]?', '', value)
                            value = switch_dict[value]
                            value_list.append(value)
                    elif stage_0_flg:
                        value = '0'
                        value_list.append(value)
                    elif re.search('(?i)early stage', text) is not None:
                        value_list.append('early')
                    elif re.search('(?i)end stage', text) is not None:
                        value_list.append('end')
                    elif re.search('(?i)extensive stage', text) is not None:
                        value_list.append('extensive')
                self._append_data(i, key, value_list)