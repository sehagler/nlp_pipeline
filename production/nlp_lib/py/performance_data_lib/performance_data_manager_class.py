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
    import read_xlsx_file, write_file, xml_diff

#
class Performance_data_manager(object):
    
    #
    def __init__(self, static_data_manager, json_manager_registry):
        self.static_data_manager = static_data_manager
        self.json_manager_registry = json_manager_registry
        
        static_data = self.static_data_manager.get_static_data()
        self.directory_manager = static_data['directory_manager']
        self.save_dir = \
            self.directory_manager.pull_directory('processing_data_dir')
        self.log_dir = self.directory_manager.pull_directory('log_dir')
        self.logger = Logger(self.log_dir)
       
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
                    result = 'true positive'
                else:
                    result = 'false positive + false negative'
            else:
                result = 'false positive'
        if 'true positive' not in result and 'true negative' not in result:
            print(x)
            print(y)
            print('')
        return result, display_data_flg
        
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
                    result = 'true positive'
                else:
                    result = 'false positive + false negative'
            else:
                result = 'false positive'
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
                    result = 'true positive'
                else:
                    result = 'false positive + false negative'
            else:
                result = 'false positive'
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
    def _display_performance_statistics(self):
        for key in self.performance_statistics_overall_dict.keys():
            print(key)
            print(' N:\t\t' + self.performance_statistics_overall_dict[key]['N']['NLP_WITHOUT_MANUAL_REVIEW'] + '\t' + \
                  self.performance_statistics_overall_dict[key]['N']['NLP_MANUAL_REVIEW'])
            print(' accuracy:\t' + self.performance_statistics_overall_dict[key]['ACCURACY']['NLP_WITHOUT_MANUAL_REVIEW'] + '\t' + \
                  self.performance_statistics_overall_dict[key]['ACCURACY']['NLP_MANUAL_REVIEW'])
            print(' precision:\t' + self.performance_statistics_overall_dict[key]['PRECISION']['NLP_WITHOUT_MANUAL_REVIEW'] + '\t' + \
                  self.performance_statistics_overall_dict[key]['PRECISION']['NLP_MANUAL_REVIEW'])
            print(' recall:\t' + self.performance_statistics_overall_dict[key]['RECALL']['NLP_WITHOUT_MANUAL_REVIEW'] + '\t' + \
                  self.performance_statistics_overall_dict[key]['RECALL']['NLP_MANUAL_REVIEW'])
            print(' F1:\t\t' + self.performance_statistics_overall_dict[key]['F1']['NLP_WITHOUT_MANUAL_REVIEW'] + '\t' + \
                  self.performance_statistics_overall_dict[key]['F1']['NLP_MANUAL_REVIEW'])
    
    #
    def _generate_performance_statistics(self, nlp_performance_wo_nlp_manual_review_dict,
                                         nlp_performance_nlp_manual_review_dict,
                                         N_total, wo_nlp_manual_review_dict):
        for key0 in nlp_performance_wo_nlp_manual_review_dict.keys():
            N_manual_review = wo_nlp_manual_review_dict[key0]
            N = N_total - N_manual_review
            FN, FP, FP_plus_FN, TN, TP = \
                self._performance_values(nlp_performance_wo_nlp_manual_review_dict[key0])
            performance_statistics_wo_nlp_manual_review_dict = \
                self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
            FN, FP, FP_plus_FN, TN, TP = \
                self._performance_values(nlp_performance_nlp_manual_review_dict[key0])
            performance_statistics_nlp_manual_review_dict = \
                self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N_manual_review)
            self.performance_statistics_overall_dict[key0] = {}
            for key1 in performance_statistics_wo_nlp_manual_review_dict.keys():
                self.performance_statistics_overall_dict[key0][key1] = {}
                self.performance_statistics_overall_dict[key0][key1]['NLP_WITHOUT_MANUAL_REVIEW'] = \
                    performance_statistics_wo_nlp_manual_review_dict[key1]
                self.performance_statistics_overall_dict[key0][key1]['NLP_MANUAL_REVIEW'] = \
                    performance_statistics_nlp_manual_review_dict[key1]
                
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
            
            ###
            data_values = [x for x in data_values if x]
            ###
            
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
                    if len(data_values[0]) > 0:
                        data_tmp = data_values[0][0].split(', ')
                        data_tmp = tuple(data_tmp)
                    else:
                        data_tmp = ''
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
    def _get_nlp_data(self, data_in, queries):
        data_out = {}
        for query in self.queries:
            key = query[0]
            sections = query[1]
            query_name = query[2]
            data_key = query[3]
            mode_flg = query[4]
            strip_flg = query[5]
            data_out[key] = \
                self._get_data_value(data_in, sections,
                                     query_name + '_' + self.nlp_value_key,
                                     data_key, mode_flg=mode_flg)
            if strip_flg and data_out[key] is not None:
                data_out[key] = data_out[key][0]
        del_keys = []
        for key in data_out:
            if data_out[key] is None:
                del_keys.append(key)
        for key in del_keys:
            del data_out[key]  
        if not data_out:
            data_out = None
        return data_out
    
    #
    def _get_nlp_values(self, nlp_data, data_json, identifier_list):
        nlp_values = data_json
        for identifier in identifier_list:
            if identifier not in nlp_values.keys():
                nlp_values[identifier] = None
        return nlp_values
    
    #
    def _get_performance(self, csn, nlp_values, nlp_datum_key, 
                         validation_data, validation_datum_key):
        data_out = nlp_values[csn]
        if data_out is not None:
            if nlp_datum_key in data_out.keys():
                nlp_value = data_out[nlp_datum_key]
            else:
                nlp_value = None
        else:
            nlp_value = None
        nlp_value = self._nlp_to_tuple(nlp_value)
        column_labels = validation_data[0]
        for i in range(1, len(validation_data)):
            item = validation_data[i]
            validation_idx = \
                [j for j in range(len(column_labels)) \
                 if column_labels[j] == validation_datum_key][0]
            if item[2] == csn:
                validation_value = \
                    self._process_validation_item(item[validation_idx])
        validation_value = self._validation_to_tuple(validation_value)
        performance, flg = \
            self._compare_data_values(nlp_value, validation_value)
        return performance
    
    #
    def _get_validation_csn_list(self, validation_data):
        static_data = self.static_data_manager.get_static_data()
        if 'document_list' in static_data.keys():
            csn_list = static_data['document_list']
        else:
            csn_list = None
        validation_csn_list =  []
        for item in validation_data:
            if csn_list is None or item[2] in csn_list:
                validation_csn_list.append(item[2])
        validation_csn_list = list(set(validation_csn_list))
        return validation_csn_list
    
    #
    def _identify_manual_review(self, nlp_values, validation_datum_keys):
        for validation_datum_key in validation_datum_keys:
            for key in nlp_values.keys():
                if nlp_values[key] is not None and validation_datum_key in nlp_values[key]:
                    if len(nlp_values[key][validation_datum_key]) > 1:
                        nlp_values[key][validation_datum_key] = 'MANUAL_REVIEW',
        return nlp_values
    
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
            A = 'NA'
        if TP + FP + FP_plus_FN > 0:
            P = TP / (TP + FP + FP_plus_FN)
        else:
            P = 'NA'
        if TP + FN + FP_plus_FN > 0:
            R = TP / (TP + FN + FP_plus_FN)
        else:
            R = 'NA'
        if P != 'NA' and R != 'NA':
            if P * R > 0:
                F1 = 2 / (1/P + 1/R)
            else:
                F1 = 'NA'
        else:
            F1 = 'NA'
        performance_statistics = {}
        if isinstance(A, str):
            performance_statistics['ACCURACY'] = A
        else:
            performance_statistics['ACCURACY'] = str(round(A, 3))
        if isinstance(F1, str):
            performance_statistics['F1'] = F1
        else:
            performance_statistics['F1'] = str(round(F1, 3))
        if isinstance(N, str):
            performance_statistics['N'] = N
        else:
            performance_statistics['N'] = str(N)
        if isinstance(P, str):
            performance_statistics['PRECISION'] = P
        else:
            performance_statistics['PRECISION'] = str(round(P, 3))
        if isinstance(R, str):
            performance_statistics['RECALL'] = R
        else:
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
    def _read_nlp_value(self, nlp_data, data_json, key, identifier):
        data_out = self._get_nlp_data(nlp_data[key][self.nlp_data_key],
                                      self.queries)
        data_json[identifier] = data_out
        return data_json
    
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
        data_json = {}
        for key in self.nlp_data.keys():
            identifier = \
                self.nlp_data[key][self.metadata_key][self.identifier_key]
            if identifier in self.identifier_list:
                data_json = self._read_nlp_value(self.nlp_data, data_json,
                                                 key, identifier)
        nlp_values = self._get_nlp_values(self.nlp_data, data_json, 
                                          self.identifier_list)
        self.performance_statistics_overall_dict = {}
        validation_data = self._read_validation_data()
        self._process_performance(nlp_values, validation_data)
    
    #
    def display_performance_data(self):
        self.display_performance()
        
    #
    def display_performance(self):
        self._display_performance_statistics()
        
    #
    def get_performance_data(self):
        self.read_nlp_data()
        self.calculate_performance()
            
    #
    def read_nlp_data(self):
        static_data = self.static_data_manager.get_static_data()
        filename = static_data['project_name'] + '/' + \
                   static_data['project_subdir'] + '/' + \
                   static_data['project_name'] + '.json'
        self.nlp_data = \
            self.json_manager_registry[filename].read_nlp_data_from_package_json_file()
                
    #
    def _read_validation_data(self):
        static_data = self.static_data_manager.get_static_data()
        validation_filename = static_data['validation_file']
        directory_manager = static_data['directory_manager']
        project_name = static_data['project_name']
        data_dir = directory_manager.pull_directory('raw_data_dir')
        book = read_xlsx_file(os.path.join(data_dir, validation_filename))
        sheet = book.sheet_by_index(0)
        ncols = sheet.ncols
        nrows = sheet.nrows
        validation_data = []
        for row_idx in range(nrows):
            validation_data_tmp = []
            for col_idx in range(ncols):
                cell_value = sheet.cell_value(row_idx, col_idx)
                try:
                    cell_value = str(int(cell_value))
                except:
                    pass
                validation_data_tmp.append(cell_value)
            validation_data.append(validation_data_tmp)
        return validation_data
         
    #
    def write_performance_data(self):
        static_data = self.static_data_manager.get_static_data()
        filename = static_data['project_name'] + '/test/' + \
                   static_data['project_name'] + '.performance.json'
        self.json_manager_registry[filename].write_file(self.performance_statistics_overall_dict)