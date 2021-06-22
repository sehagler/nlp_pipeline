# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 09:39:27 2020

@author: haglers
"""

#
import ast
import collections
from copy import deepcopy
import re

#
from distutils.dir_util import copy_tree
import getpass
from jsondiff import diff
import os
import shutil

#
from nlp_lib.py.logger_lib.logger_class import Logger
from tool_lib.py.processing_tools_lib.file_processing_tools \
    import read_nlp_data_from_package_json_file, write_json_file, xml_diff

#
class Performance_data_manager(object):
    
    #
    def __init__(self, static_data_manager):
        project_data = static_data_manager.get_project_data()
        self.directory_manager = project_data['directory_manager']
        self.save_dir = \
            self.directory_manager.pull_directory('processing_data_dir')
        self.project_data = project_data
        
        self.log_dir = self.directory_manager.pull_directory('log_dir')
        self.logger = Logger(self.log_dir)
        self.static_data = project_data
       
        json_structure_manager = project_data['json_structure_manager']
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
        json_structure_manager = project_data['json_structure_manager']
        self.multiple_specimens = \
            json_structure_manager.pull_key('multiple_specimens')
        self.multiple_values = \
            json_structure_manager.pull_key('multiple_values')
        #
    
        self.directory_manager = project_data['directory_manager']
        
    #
    def _compare_data_values(self, x, y):
        if (isinstance(x, list) or isinstance(x, tuple) or x is None) and \
           (isinstance(y, list) or isinstance(y, tuple) or y is None):
            result, display_data_flg = self._compare_lists(x, y)
        else:
            result, display_data_flg = self._compare_values(x, y)
        return result, display_data_flg
        
    #
    def _compare_lists(self, x, y):
        display_data_flg = False
        try:
            if self.multiple_values in x:
                x = self.multiple_values
        except:
            pass
        if x is not self.multiple_values:
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
            result = 'multiple values'
        #if result != 'true positive' and result != 'true negative':
        #    print(x)
        #    print(y)
        #    print('')
        return result, display_data_flg
    
    #
    def _compare_strings(self, x, y):
        display_data_flg = False
        try:
            if self.multiple_values in x:
                x = self.multiple_values
        except:
            pass
        if x is not self.multiple_values:
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
            result = 'multiple values'
        return result, display_data_flg
        
    #
    def _compare_values(self, x, y):
        display_data_flg = False
        try:
            if self.multiple_values in x:
                x = self.multiple_values
        except:
            pass
        if x is not self.multiple_values:
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
            result = 'multiple values'
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
                            data_values.append(tuple(data_item))
        else:
            for j in range(len(self.section_data_list)):
                section_data = self.section_data_list[j]
                data_item = section_data[1]
                if not isinstance(data_item, list):
                    data_tmp = []
                    data_tmp.append(data_item)
                    data_item = data_tmp
                data_values.append(tuple(data_item))
        #data_values = list(set(data_values))
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
    def _intersection(self, x, y):
        z = list(set(x) & set(y))
        return z
    
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
    def _read_nlp_value_data(self, validation_csn_list, nlp_data):
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
        self.nlp_data = read_nlp_data_from_package_json_file(self.static_data)
         
    #
    def write_performance_data(self):
        project_name = self.project_data['project_name']
        write_json_file(os.path.join(self.save_dir, project_name + '.performance.json'),
                        self.performance_statistics_dict)