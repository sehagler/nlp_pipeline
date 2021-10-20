# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 09:39:27 2020

@author: haglers
"""

#
import ast
import collections
from copy import deepcopy
from distutils.dir_util import copy_tree
import getpass
from jsondiff import diff
import os
import re
import shutil

#
from nlp_lib.py.file_lib.json_manager_class import Json_manager
from nlp_lib.py.logger_lib.logger_class import Logger
from tool_lib.py.processing_tools_lib.file_processing_tools \
    import write_file, xml_diff

#
class Performance_data_manager(object):
    
    #
    def __init__(self, static_data_manager, performance_json_manager,
                 project_json_manager):
        self.performance_json_manager = performance_json_manager
        self.project_json_manager = project_json_manager
        static_data = static_data_manager.get_static_data()
        self.directory_manager = static_data['directory_manager']
        self.save_dir = \
            self.directory_manager.pull_directory('processing_data_dir')
        
        self.log_dir = self.directory_manager.pull_directory('log_dir')
        self.logger = Logger(self.log_dir)
        self.static_data = static_data
        self.static_data_manager = static_data_manager
       
        json_structure_manager = static_data['json_structure_manager']
        self.document_wrapper_key = \
            json_structure_manager.pull_key('document_wrapper_key')
        self.documents_wrapper_key = \
            json_structure_manager.pull_key('documents_wrapper_key')
        self.metadata_key = \
            json_structure_manager.pull_key('metadata_key')
        self.nlp_data_key = \
            json_structure_manager.pull_key('nlp_data_key')
        self.nlp_datetime_key = \
            json_structure_manager.pull_key('nlp_datetime_key')
        self.nlp_datum_key = \
            json_structure_manager.pull_key('nlp_datum_key')
        self.nlp_metadata_key = \
            json_structure_manager.pull_key('nlp_metadata_key')
        self.nlp_performance_key = \
            json_structure_manager.pull_key('nlp_performance_key')
        self.nlp_query_key = \
            json_structure_manager.pull_key('nlp_query_key')
        self.nlp_section_key = \
            json_structure_manager.pull_key('nlp_section_key')
        self.nlp_specimen_key = \
            json_structure_manager.pull_key('nlp_specimen_key')
        self.nlp_source_text_key = \
            json_structure_manager.pull_key('nlp_source_text_key')
        self.nlp_text_element_key = \
            json_structure_manager.pull_key('nlp_text_element_key')
        self.nlp_text_key = \
            json_structure_manager.pull_key('nlp_text_key')
        self.nlp_value_key = \
            json_structure_manager.pull_key('nlp_value_key')
            
        # to be moved to appropriate location
        json_structure_manager = static_data['json_structure_manager']
        self.manual_review = \
            json_structure_manager.pull_key('manual_review')
        #
        
    #
    def _compare_data_values(self, x, y, value_range=None):
        if value_range is None:
            if (isinstance(x, list) or isinstance(x, tuple) or x is None) and \
               (isinstance(y, list) or isinstance(y, tuple) or y is None):
                result, display_data_flg = self._compare_lists(x, y)
            else:
                result, display_data_flg = self._compare_values(x, y)
        else:
            result, display_data_flg = self._compare_values_range(x, y, value_range)
        return result, display_data_flg
        
    #
    def _compare_lists(self, x, y):
        display_data_flg = False
        try:
            if self.manual_review in x:
                x = self.manual_review
        except:
            pass
        try:
            if len(x) == 0:
                x = None
        except:
            pass
        if x != self.manual_review:
            if y is not None:
                if x is not None:
                    if collections.Counter(x) == collections.Counter(y):
                        result = 'true positive'
                    else:
                        display_data_flg = True
                        result = 'false positive'
                else:
                    display_data_flg = True
                    result = 'false negative'
            else:
                if x is not None:
                    display_data_flg = True
                    result = 'false positive'
                else:
                    result = 'true negative'
        else:
            if y is not None:
                if self.manual_review in y:
                    result = 'manual review true positive'
                else:
                    result = 'manual review false positive + false negative'
            else:
                result = 'manual review false positive'
        if False:
            result = result.replace('manual review ', '')
        if 'true positive' not in result and 'true negative' not in result:
            print(x)
            print(y)
            print('')
        return result, display_data_flg
    
    '''
    #
    def _compare_strings(self, x, y):
        display_data_flg = False
        try:
            if self.manual_review in x:
                x = self.manual_review
        except:
            pass
        if x != self.manual_review:
            if y is not None:
                if x is not None:
                    if str(x) in str(y):
                        result = 'true positive'
                    else:
                        display_data_flg = True
                        result = 'false positive + false negative'
                elif x is None:
                    display_data_flg = True
                    result = 'false negative'
            else:
                if x is not None:
                    display_data_flg = True
                    result = 'false positive'
                else:
                    result = 'true negative'
        else:
            if y is not None:
                if self.manual_review in y:
                    result = 'manual review true positive'
                else:
                    result = 'manual review false positive + false negative'
            else:
                result = 'manual review false positive'
        if False:
            result = result.replace('manual review ', '')
        if 'true positive' not in result and 'true negative' not in result:
            print(x)
            print(y)
            print('')
        return result, display_data_flg
    '''
        
    #
    def _compare_values(self, x, y):
        display_data_flg = False
        try:
            if self.manual_review in x:
                x = self.manual_review
        except:
            pass
        if x != self.manual_review:
            if y is not None:
                if x is not None:
                    if str(x) == str(y):
                        result = 'true positive'
                    else:
                        display_data_flg = True
                        result = 'false positive + false negative'
                elif x is None:
                    display_data_flg = True
                    result = 'false negative'
            else:
                if x is not None:
                    display_data_flg = True
                    result = 'false positive'
                else:
                    result = 'true negative'
        else:
            if y is not None:
                if self.manual_review in y:
                    result = 'manual review true positive'
                else:
                    result = 'manual review false positive + false negative'
            else:
                result = 'manual review false positive'
        if False:
            result = result.replace('manual review ', '')
        if 'true positive' not in result and 'true negative' not in result:
            print(x)
            print(y)
            print('')
        return result, display_data_flg
    
    #
    def _compare_values_range(self, x, y, value_range):
        display_data_flg = False
        try:
            if self.manual_review in x:
                x = self.manual_review
        except:
            pass
        if x != self.manual_review:
            if y is not None:
                if x is not None:
                    if abs(float(x[0]) - float(y[0])) <= value_range:
                        result = 'true positive'
                    else:
                        display_data_flg = True
                        result = 'false positive + false negative'
                elif x is None:
                    display_data_flg = True
                    result = 'false negative'
            else:
                if x is not None:
                    display_data_flg = True
                    result = 'false positive'
                else:
                    result = 'true negative'
        else:
            if y is not None:
                if self.manual_review in y:
                    result = 'manual review true positive'
                else:
                    result = 'manual review false positive + false negative'
            else:
                result = 'manual review false positive'
        if False:
            result = result.replace('manual review ', '')
        if 'true positive' not in result and 'true negative' not in result:
            print(x)
            print(y)
            print('')
        return result, display_data_flg
    
    #
    def _difference(self, x, y):
        z = list(set(x) - set(y))
        return z
    
    #
    def _display_performance_statistics(self, performance_statistics_dict):
        for key in performance_statistics_dict.keys():
            print(key)
            print(' accuracy:\t' + performance_statistics_dict[key]['ACCURACY'])
            print(' precision:\t' + performance_statistics_dict[key]['PRECISION'])
            print(' recall:\t' + performance_statistics_dict[key]['RECALL'])
            print(' F1:\t\t' + performance_statistics_dict[key]['F1'])
    
    #
    def _get_data_value(self, node, section_key_list, target_key, data_key, 
                        mode_flg='multiple_values'):
        self.section_data_list = []
        self._walk(node, target_key, data_key, [], section_key_list)
        data_values = []
        if section_key_list is not None:
            for i in range(len(section_key_list)):
                section_key = section_key_list[i]
                if len(data_values) == 0:
                    for j in range(len(self.section_data_list)):
                        section_data = self.section_data_list[j]
                        if section_data[0] == section_key:
                            data_item = section_data[1]
                            if not isinstance(data_item, list):
                                data_tmp = []
                                data_tmp.append(data_item)
                                data_item = data_tmp
                            #data_values.append(tuple(data_item))
                            data_values.extend(data_item)
        else:
            for j in range(len(self.section_data_list)):
                section_data = self.section_data_list[j]
                data_item = section_data[1]
                if not isinstance(data_item, list):
                    data_tmp = []
                    data_tmp.append(data_item)
                    data_item = data_tmp
                #data_values.append(tuple(data_item))
                data_values.extend(data_item)
        if len(data_values) > 0:
            data_values = list(set(data_values))
            data_values.sort()
            data_values_tuple = tuple(data_values)
            data_values = []
            data_values.append(data_values_tuple)
        data_values = [tuple(i) for i in set(tuple(i) for i in data_values)]
        data_value = []
        if section_key_list is not None:  
            data_value = data_values
        else:
            if len(data_values) > 0:
                if mode_flg == 'multiple_values':
                    data_tmp = data_values[0][0].split(', ')
                    data_tmp = tuple(data_tmp)
                elif mode_flg == 'single_value':
                    data_tmp = data_values
                if isinstance(data_tmp, list):
                    data_tmp = tuple(data_tmp)
                elif isinstance(data_tmp, tuple):
                    data_tmp = tuple(data_tmp)
                data_value.append(data_tmp)
            else:
                data_value = data_values
        #data_value = list(set(data_value))
        data_value = [tuple(i) for i in set(tuple(i) for i in data_value)]
        if len(data_value) > 0:
            if len(data_value[0]) > 1:
                data_tmp = list(data_value[0])
                data_tmp = [ x for x in data_tmp if x != ('equivocal',) ]
                data_tmp = tuple(data_tmp)
                data_value[0] = data_tmp
        if mode_flg == 'single_value':
            if len(data_value) == 0:
                data_value = None
            elif len(data_value[0]) == 1:
                data_value = [ data_value[0][0] ]
            elif len(data_value[0]) > 1:
                data_value = [ 'MANUAL_REVIEW' ]
                data_value = tuple(data_value)
                data_value = [ data_value ]
        elif mode_flg == 'multiple_values':
            if len(data_value) == 0:
                data_value = None
        return data_value
    
    #
    def _get_validation_csn_list(self, validation_data):
        if 'document_list' in self.static_data.keys():
            csn_list = self.static_data['document_list']
        else:
            csn_list = None
        validation_csn_list =  []
        for item in validation_data:
            if csn_list is None or item[2] in csn_list:
                validation_csn_list.append(item[2])
        validation_csn_list = list(set(validation_csn_list))
        return validation_csn_list
    
    #
    def _intersection(self, x, y):
        z = list(set(x) & set(y))
        return z
    
    #
    def _nlp_to_tuple(self, value):
        if value is not None:
            value = list(value)
            for i in range(len(value)):
                value[i] = value[i].replace(' ', '')
            value_tuple = tuple(value)
        else:
            value_tuple = None
        return value_tuple
    
    #
    def _performance_values(self, input_list):
        FN = len([ x for x in input_list if x == 'false negative' ])
        FP = len([ x for x in input_list if x == 'false positive' ])
        FP_plus_FN = \
            len([ x for x in input_list if x == 'false positive + false negative' ])
        TN = len([ x for x in input_list if x == 'true negative' ])
        TP = len([ x for x in input_list if x == 'true positive' ])
        return FN, FP, FP_plus_FN, TN, TP
    
    #
    def _performance_statistics(self, FN, FP, FP_plus_FN, TN, TP, N):
        if N > 0:
            A = (TP + TN) / N
        else:
            A = -1
        if TP + FP + FP_plus_FN > 0:
            P = TP / (TP + FP + FP_plus_FN)
        else:
            P = -1
        if TP + FN > 0:
            R = TP / (TP + FN + FP_plus_FN)
        else:
            R = -1
        if P != -1 and R != -1:
            if P * R > 0:
                F1 = 2 / (1/P + 1/R)
            else:
                F1 = -1
        else:
            F1 = -1
        performance_statistics = {}
        performance_statistics['ACCURACY'] = str(round(A, 3))
        performance_statistics['F1'] = str(round(F1, 3))
        performance_statistics['PRECISION'] = str(round(P, 3))
        performance_statistics['RECALL'] = str(round(R, 3))
        return performance_statistics
    
    #
    def _process_validation_item(self, x):
        if x == '':
            x = None
        return x
    
    #
    def _read_metadata(self, nlp_data):
        metadata_keys = []
        metadata_dict_dict = {}
        for key in nlp_data.keys():
            metadata_dict_dict[key] = {}
            metadata_dict_dict[key]['METADATA'] = \
                nlp_data[key]['METADATA']
            metadata_dict_dict[key]['NLP_METADATA'] = \
                nlp_data[key]['NLP_METADATA']
        for metadata_key in metadata_dict_dict.keys():
            for key in metadata_dict_dict[metadata_key].keys():
                if key not in metadata_keys:
                    metadata_keys.append(key)
        return metadata_keys, metadata_dict_dict
    
    #
    def _read_nlp_value_data(self, nlp_data, validation_data):
        validation_csn_list = \
            self._get_validation_csn_list(validation_data)
        nlp_values = {}
        for csn in validation_csn_list:
            data_out = None
            for item in nlp_data:
                if nlp_data[item][self.metadata_key]['SOURCE_SYSTEM_DOCUMENT_ID'] == csn:
                    data_out = self._get_nlp_data(nlp_data[item][self.nlp_data_key])
            nlp_values[csn] = data_out
        return nlp_values
    
    #
    def _unique(self, lst):
        s = set()
        for el in lst:
            if isinstance(el, str):
                s.add(el)
            elif el[0] == 'not':
                s.add(tuple(*el))
            else:
                s.update(self._unique(el))
        return s
        
    #
    def _validation_to_tuple(self, text):
        if text is not None:
            text = text.replace(' ', '')
            text = text.replace(',', '\',\'')
            text = text.replace('(', '(\'')
            text = text.replace(')', '\')')
            text = '[\'' + text + '\']'
            text = text.replace('\'(', '(')
            text = text.replace(')\'', ')')
            text_list = eval(text)
            for i in range(len(text_list)):
                if isinstance(text_list[i], tuple):
                    text_list[i] = str(text_list[i])
                    text_list[i] = text_list[i].replace('\'', '')
                    text_list[i] = text_list[i].replace(' ', '')
            text_tuple = tuple(text_list)
        else:
            text_tuple = None
        return text_tuple
    
    #
    def _walk(self, node, target_key, data_key, key_list_in, section_key_list):
        for k, v in node.items():
            key_list = deepcopy(key_list_in)
            key_list.append(k)
            if k == target_key:
                section_key = ast.literal_eval(key_list[0])[0]
                section_key = re.sub(' [0-9]+$', '', section_key)
                if section_key_list is not None:
                    if section_key in section_key_list:
                        for v_item in v:
                            if data_key in v_item.keys():
                                self.section_data_list.append(tuple([section_key, v_item[data_key]]))
                else:
                    for v_item in v:
                        if data_key in v_item.keys():
                            self.section_data_list.append(tuple([section_key, v_item[data_key]]))
            elif isinstance(v, dict):
                self._walk(v, target_key, data_key, key_list, section_key_list)
                
    #
    def calculate_performance(self):
        validation_data = self._read_validation_data()
        nlp_values = self._read_nlp_value_data(self.nlp_data, validation_data)
        self.performance_statistics_dict = {}
        self._process_performance(nlp_values, validation_data)
        return self.performance_statistics_dict
        
    #
    def display_performance_data(self):
        self.display_performance(self.performance_statistics_dict)
        
    #
    def display_performance(self, performance_statistics_dict):
        self._display_performance_statistics(performance_statistics_dict)
        
    #
    def get_performance_data(self):
        self.read_nlp_data()
        self.performance_statistics_dict = \
            self.calculate_performance()
            
    #
    def read_nlp_data(self):
        self.nlp_data = \
            self.project_json_manager.read_nlp_data_from_package_json_file()
         
    #
    def write_performance_data(self):
        self.performance_json_manager.write_file(self.performance_statistics_dict)