# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 09:39:27 2020

@author: haglers
"""

#
import ast
from copy import deepcopy
import os
import re
import traceback

#
from tools_lib.processing_tools_lib.function_processing_tools \
    import parallel_composition, sequential_composition

#
from base_lib.manager_base_class import Manager_base
            
#
def _get_data_value(section_data_list, section_key_list, mode_flg):
    data_values = []
    if section_key_list is not None:
        for i in range(len(section_key_list)):
            section_key = section_key_list[i]
            if len(data_values) == 0:
                for j in range(len(section_data_list)):
                    section_data = section_data_list[j]
                    if section_data[0] == section_key:
                        data_item = section_data[1]
                        if not isinstance(data_item, list):
                            data_tmp = []
                            data_tmp.append(data_item)
                            data_item = data_tmp
                        #data_values.append(tuple(data_item))
                        data_values.extend(data_item)
    else:
        for j in range(len(section_data_list)):
            section_data = section_data_list[j]
            data_item = section_data[1]
            if not isinstance(data_item, list):
                data_tmp = []
                data_tmp.append(data_item)
                data_item = data_tmp
            #data_values.append(tuple(data_item))
            data_values.extend(data_item)
    data_values = list(set(data_values))
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
                data_value = data_values
                '''
                if len(data_values[0]) > 0:
                    data_tmp = data_values[0].split(', ')
                    data_tmp = tuple(data_tmp)
                else:
                    data_tmp = ''
                '''
            if mode_flg == 'single_value':
                data_tmp = data_values
            if isinstance(data_tmp, list):
                data_tmp = tuple(data_tmp)
            elif isinstance(data_tmp, tuple):
                data_tmp = tuple(data_tmp)
            data_value.append(data_tmp)
        else:
            data_value = data_values
    data_value = [tuple(i) for i in set(tuple(i) for i in data_value)]
    if len(data_value) > 0:
        if len(data_value[0]) > 1:
            data_tmp = list(data_value[0])
            data_tmp = tuple(data_tmp)
            data_value[0] = data_tmp
    if mode_flg == 'single_value':
        if len(data_value) == 0:
            data_value = None
        elif len(data_value[0]) == 1:
            data_value = [ data_value[0][0] ]
        elif len(data_value[0]) > 1:
            data_value = [ self.manual_review ]
            data_value = tuple(data_value)
            data_value = [ data_value ]
    elif mode_flg == 'multiple_values':
        if len(data_value) == 0:
            data_value = None
    return data_value, section_data_list

#
def _get_nlp_value(arg_dict):
    identifier = arg_dict['identifier']
    manual_review = arg_dict['manual_review']
    nlp_values = arg_dict['nlp_values']
    validation_datum_key = arg_dict['validation_datum_key']
    if identifier in nlp_values.keys():
        if nlp_values[identifier] is not None:
            if validation_datum_key in nlp_values[identifier].keys():
                nlp_value = nlp_values[identifier][validation_datum_key]
            else:
                nlp_value = None
        else:
            nlp_value = None
    else:
        nlp_value = None
    nlp_value = _nlp_to_tuple(nlp_value, manual_review)
    return nlp_value

#
def _get_nlp_values(nlp_data, data_json):
    nlp_values = data_json
    return nlp_values

#
def _identify_manual_review(nlp_values, validation_datum_keys, manual_review):
    for validation_datum_key in validation_datum_keys:
        for key in nlp_values.keys():
            if nlp_values[key] is not None and validation_datum_key in nlp_values[key]:
                
                ### Kludge to handle HER2 biomarker
                if len(nlp_values[key][validation_datum_key]) > 1:
                    data_tmp = \
                        [ x for x in nlp_values[key][validation_datum_key] if x != 'equivocal' ]
                    nlp_values[key][validation_datum_key] = tuple(data_tmp)
                ### Kludge to handle HER2 biomarker
                    
                if len(nlp_values[key][validation_datum_key]) > 1:
                    nlp_values[key][validation_datum_key] = manual_review,
    return nlp_values

#
def _normalize_percentage_range(text):
    if re.match("[0-9]+%?\-[0-9]+%", text):
        text = re.sub('-', '%-', text)
        text = re.sub('%+', '%', text)
    return text

#
def _nlp_to_tuple(value, manual_review):
    if value is not None:
        value_tmp = []
        value = list(value)
        for i in range(len(value)):
            if type(value[i]) is not tuple:
                if value[i] != manual_review:
                    value[i] = value[i].lower()
                value[i] = value[i].replace(' ', '')
                value_tmp.append(value[i])
            else:
                if len(value[i]) > 0:
                    for j in range(len(value[i])):
                        value_tmp.append(value[i][j])
        value = value_tmp
        value = list(set(value))
        value_tuple = tuple(value)
    else:
        value_tuple = None
    return value_tuple

#
def _performance_values(input_list):
    FN = len([ x for x in input_list if x == 'false negative' ])
    FP = len([ x for x in input_list if x == 'false positive' ])
    FP_plus_FN = \
        len([ x for x in input_list if x == 'false positive + false negative' ])
    TN = len([ x for x in input_list if x == 'true negative' ])
    TP = len([ x for x in input_list if x == 'true positive' ])
    return FN, FP, FP_plus_FN, TN, TP

#
def _performance_statistics(FN, FP, FP_plus_FN, TN, TP,
                            N_validation_documents,
                            N_validation_hit_documents):
    N = N_validation_documents
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
    if type(A) is str:
        performance_statistics['ACCURACY'] = A
    else:
        performance_statistics['ACCURACY'] = str(round(A, 3))
    if type(F1) is str:
        performance_statistics['F1'] = F1
    else:
        performance_statistics['F1'] = str(round(F1, 3))
    if type(N_validation_documents) is str:
        performance_statistics['N_VALIDATION_DOCUMENTS'] = \
            N_validation_documents
    else:
        performance_statistics['N_VALIDATION_DOCUMENTS'] = \
            str(N_validation_documents)
    if N_validation_hit_documents is not None:
        if isinstance(N_validation_hit_documents, str):
            performance_statistics['N_VALIDATION_HIT_DOCUMENTS'] = \
                N_validation_hit_documents
        else:
            performance_statistics['N_VALIDATION_HIT_DOCUMENTS'] = \
                str(N_validation_hit_documents)
    else:
        performance_statistics['N_VALIDATION_HIT_DOCUMENTS'] = 'NA'
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
def _process_validation_item(x):
    if x == '':
        x = None
    return x

#
class Performance_data_manager(Manager_base):
    
    #
    def __init__(self, static_data_object, directory_object, logger_object,
                 evaluation_manager, json_manager_registry, metadata_manager,
                 xls_manager_registry):
        Manager_base.__init__(self, static_data_object, directory_object,
                              logger_object)
        self.evaluation_manager = evaluation_manager
        self.json_manager_registry = json_manager_registry
        self.metadata_manager = metadata_manager
        self.xls_manager_registry = xls_manager_registry
        self.save_dir = \
            self.directory_object.pull_directory('processing_data_dir')
        self.log_dir = self.directory_object.pull_directory('log_dir')
        self.csv_body = ''
        self.csv_header = ''
        
    #
    def _append_csv_body(self, value, newline_flg):
        if value == None: value = ''
        if type(value) is tuple:
            value_tmp = ''
            for item in value: value_tmp += str(item) + '; '
            value = value_tmp[:-2]
        if newline_flg:
            self.csv_body += '\n' + str(value) + ', '
        else:
            self.csv_body += str(value) + ', '
        
    #
    def _append_csv_header(self, text):
        self.csv_header += text
    
    #
    def _evaluate_performance(self, N_documents):
        N_hit_documents_wo_validation_manual_review_dict = {}
        for key in self.hit_documents_dict.keys():
            N_hit_documents_wo_validation_manual_review_dict[key] = \
                len(list(set(self.hit_documents_dict[key])))
        N_hit_documents_w_validation_manual_review_dict = {}
        for key in self.hit_manual_review_dict.keys():
            N_hit_documents_w_validation_manual_review_dict[key] = \
                len(list(set(self.hit_manual_review_dict[key])))
        self._generate_performance_statistics(self.nlp_performance_wo_validation_manual_review_dict,
                                              self.nlp_performance_w_validation_manual_review_dict,
                                              N_documents, self.N_manual_review,
                                              N_hit_documents_wo_validation_manual_review_dict,
                                              N_hit_documents_w_validation_manual_review_dict)
        
    #
    def _generate_performance_statistics(self, nlp_performance_wo_nlp_manual_review_dict,
                                         nlp_performance_nlp_manual_review_dict, 
                                         N_documents, N_manual_review,
                                         N_hit_documents_wo_nlp_manual_review_dict,
                                         N_hit_documents_nlp_manual_review_dict):
        for key0 in nlp_performance_wo_nlp_manual_review_dict.keys():
            N_validation_documents = N_documents - N_manual_review[key0]
            if N_hit_documents_nlp_manual_review_dict is not None:
                N_validation_hit_manual_review = \
                    N_hit_documents_nlp_manual_review_dict[key0]
            else:
                N_validation_hit_manual_review = None
            if N_hit_documents_wo_nlp_manual_review_dict is not None:
                N_hit_documents = N_hit_documents_wo_nlp_manual_review_dict[key0]
                N_validation_hit_documents = \
                    N_hit_documents - N_validation_hit_manual_review
            else:
                N_validation_hit_documents = None
            FN, FP, FP_plus_FN, TN, TP = \
                _performance_values(nlp_performance_wo_nlp_manual_review_dict[key0])
            performance_statistics_wo_nlp_manual_review_dict = \
                _performance_statistics(FN, FP, FP_plus_FN, TN, TP,
                                        N_validation_documents,
                                        N_validation_hit_documents)
            FN, FP, FP_plus_FN, TN, TP = \
                _performance_values(nlp_performance_nlp_manual_review_dict[key0])
            performance_statistics_nlp_manual_review_dict = \
                _performance_statistics(FN, FP, FP_plus_FN, TN, TP, 
                                        N_manual_review[key0], 
                                        N_validation_hit_manual_review)
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
        section_data_list = \
            self._walk(node, target_key, data_key, [], section_key_list)
        data_value, section_data_list = _get_data_value(section_data_list,
                                                        section_key_list,
                                                        mode_flg)
        self.section_data_list = section_data_list
        return data_value
    
    #
    def _get_nlp_values(self, nlp_data, data_json):
        return _get_nlp_values(nlp_data, data_json)
    
    #
    def _get_validation_value(self, arg_dict):
        identifier = arg_dict['identifier']
        validation_datum_key = arg_dict['validation_datum_key']
        validation_value = None
        column_labels = self.validation_data_manager.column_labels()
        for i in range(1, self.validation_data_manager.length()):
            row = self.validation_data_manager.row(i)
            validation_idx = \
                [j for j in range(len(column_labels)) \
                 if column_labels[j] == validation_datum_key]
            if len(validation_idx) > 0:
                if row[2] == identifier:
                    validation_value = \
                        _process_validation_item(row[validation_idx[0]])
        validation_value = self._validation_to_tuple(validation_value,
                                                     self.manual_review)
        return validation_value
    
    #
    def _identify_manual_review(self, nlp_values, validation_datum_keys):
        return _identify_manual_review(nlp_values, validation_datum_keys,
                                       self.manual_review)
    
    #
    def _initialize_performance_dicts(self):
        self.nlp_performance_wo_validation_manual_review_dict = {}
        self.nlp_performance_w_validation_manual_review_dict = {}
        for i in range(len(self.queries)):
            validation_datum_key = self.queries[i][0]
            self.nlp_performance_wo_validation_manual_review_dict[validation_datum_key] = []
            self.nlp_performance_w_validation_manual_review_dict[validation_datum_key] = []
        self.N_manual_review = {}
        self.hit_documents_dict = {}
        self.hit_manual_review_dict = {}
    
    #
    def _process_performance(self, nlp_values, validation_datum_keys,
                             display_flg):
        self._initialize_performance_dicts()
        self.validation_data_manager.trim_validation_data()
        self._validation_data_manager_column_to_int()
        document_csn_list = \
            self.metadata_manager.pull_document_identifier_list('SOURCE_SYSTEM_DOCUMENT_ID')
        nlp_values = \
            self._identify_manual_review(nlp_values, validation_datum_keys)
        validation_csn_list = \
            self.validation_data_manager.get_validation_csn_list()
        for csn in document_csn_list:
            log_text = csn
            self.logger_object.print_log(log_text)
            self._append_csv_header('\n' + 'DOCUMENT_IDENTIFIER' + ', ')
            self._append_csv_body(csn, newline_flg=True)
            for i in range(len(self.queries)):
                validation_datum_key = self.queries[i][0]
                arg_dict = {}
                arg_dict['identifier'] = csn
                arg_dict['manual_review'] = self.manual_review
                arg_dict['nlp_values'] = nlp_values
                arg_dict['validation_datum_key'] = validation_datum_key
                return_dict = parallel_composition([self._get_validation_value,
                                                    _get_nlp_value],
                                                   arg_dict)
                arg_dict = {}
                arg_dict['display_flg'] = display_flg
                arg_dict['identifier'] = csn
                arg_dict['identifier_list'] = validation_csn_list
                arg_dict['nlp_value'] = \
                    return_dict[_get_nlp_value.__name__]
                arg_dict['validation_datum_key'] = validation_datum_key
                arg_dict['validation_value'] = \
                    return_dict[self._get_validation_value.__name__]
                sequential_composition([self.evaluation_manager.evaluation,
                                        self._update_performance_dicts],
                                       arg_dict)
                nlp_value = return_dict[_get_nlp_value.__name__]
                self._append_csv_header(validation_datum_key + ', ')
                self._append_csv_body(nlp_value, newline_flg=False)
        N_documents = len(document_csn_list)
        self._evaluate_performance(N_documents)
    
    #
    def _process_validation_item(self, x):
        return _process_validation_item(x)
    
    #
    def _read_nlp_value(self, nlp_data, data_json, key, identifier):
        data_in = nlp_data[key][self.nlp_data_key]
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
        data_json[identifier] = data_out
        return data_json
    
    #
    def _update_performance_dicts(self, arg_dict):
        identifier = arg_dict['identifier']
        identifier_list = arg_dict['identifier_list']
        nlp_value = arg_dict['nlp_value']
        performance = arg_dict['performance']
        validation_datum_key = arg_dict['validation_datum_key']
        validation_value = arg_dict['validation_value']
        if validation_datum_key not in self.N_manual_review.keys():
            self.N_manual_review[validation_datum_key] = 0
        if validation_datum_key not in self.hit_documents_dict.keys():
            self.hit_documents_dict[validation_datum_key] = []
        if validation_datum_key not in self.hit_manual_review_dict.keys():
            self.hit_manual_review_dict[validation_datum_key] = []
        if nlp_value is not None:
            if identifier_list is None or identifier in identifier_list:
                if not ( validation_value is not None and self.manual_review in validation_value ):
                    self.nlp_performance_wo_validation_manual_review_dict[validation_datum_key].append(performance)
                else:
                    self.nlp_performance_w_validation_manual_review_dict[validation_datum_key].append(performance)
            self.hit_documents_dict[validation_datum_key].append(identifier)
            if validation_value is not None and self.manual_review in validation_value:
                self.hit_manual_review_dict[validation_datum_key].append(identifier)
        else:
            if validation_value == None:
                self.nlp_performance_wo_validation_manual_review_dict[validation_datum_key].append('true negative')
            elif self.manual_review in validation_value:
                self.nlp_performance_w_validation_manual_review_dict[validation_datum_key].append('false negative')
                self.logger_object.print_log('false negative')
                self.logger_object.print_log(None)
                self.logger_object.print_log(validation_value)
                self.logger_object.print_log('')
            else:
                self.nlp_performance_wo_validation_manual_review_dict[validation_datum_key].append('false negative')
                self.logger_object.print_log('false negative')
                self.logger_object.print_log(None)
                self.logger_object.print_log(validation_value)
                self.logger_object.print_log('')
        if validation_value is not None and self.manual_review in validation_value:
            self.N_manual_review[validation_datum_key] += 1
            
    #
    def _validation_data_manager_column_to_int(self):
        pass
    
    #
    def _validation_datum_keys(self):
        validation_datum_keys = []
        for query in self.queries:
            validation_datum_keys.append(query[0])
        return validation_datum_keys

    #
    def _validation_to_tuple(self, value, manual_review):
        if value is not None:
            if value != manual_review:
                value = value.lower()
            value = _normalize_percentage_range(value)
            value = value.replace(' ', '')
            value = value.replace(',', '\',\'')
            value = value.replace('(', '(\'')
            value = value.replace(')', '\')')
            value = value.replace('\'(', '(')
            value = value.replace(')\'', ')')
            try:
                value_eval = '[\'' + value + '\']'
                value_list = eval(value_eval)
            except Exception:
                log_text = traceback.format_exc()
                self.logger_object.print_exc(log_text)
                value = value.replace('(\'', '(')
                value = value.replace('\')', ')')
                value_eval = '[\'' + value + '\']'
                value_list = eval(value_eval)
            for i in range(len(value_list)):
                if type(value_list[i]) is not tuple:
                    value_list[i] = str(value_list[i])
                    value_list[i] = value_list[i].replace('\'', '')
                    value_list[i] = value_list[i].replace(' ', '')
            value_tuple = tuple(value_list)
        else:
            value_tuple = None
        return value_tuple
    
    #
    def _walker(self, node, target_key, data_key, key_list_in, section_key_list):
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
                self._walker(v, target_key, data_key, key_list, section_key_list)
                
    #
    def _walk(self, node, target_key, data_key, key_list_in, section_key_list):
        self.section_data_list = []
        self._walker(node, target_key, data_key, key_list_in, section_key_list)
        section_data_list = self.section_data_list
        del self.section_data_list
        return section_data_list
                
    #
    def calculate_performance(self, display_flg):
        data_json = {}
        for key in self.nlp_data.keys():
            identifier = \
                self.nlp_data[key][self.metadata_key][self.identifier_key]
            data_json = self._read_nlp_value(self.nlp_data, data_json, key,
                                             identifier)
        nlp_values = self._get_nlp_values(self.nlp_data, data_json)
        self.performance_statistics_overall_dict = {}
        static_data = self.static_data_object.get_static_data()
        validation_filename = static_data['validation_file']
        data_dir = self.directory_object.pull_directory('raw_data_dir')
        filename = os.path.join(data_dir, validation_filename)
        self.validation_data_manager = self.xls_manager_registry[filename]
        self.validation_data_manager.read_validation_data()
        validation_datum_keys = self._validation_datum_keys()
        self._process_performance(nlp_values, validation_datum_keys,
                                  display_flg)
        
    #
    def display_performance_statistics(self):
        for key in self.performance_statistics_overall_dict.keys():
            log_text = key
            self.logger_object.print_log(log_text)
            log_text = '\t\t\tNON_MAN_REV\tMAN_REV'
            self.logger_object.print_log(log_text)
            log_text = 'N documents:\t\t ' + self.performance_statistics_overall_dict[key]['N_VALIDATION_DOCUMENTS']['NLP_WITHOUT_MANUAL_REVIEW'] + \
                       '\t\t ' + self.performance_statistics_overall_dict[key]['N_VALIDATION_DOCUMENTS']['NLP_MANUAL_REVIEW']
            self.logger_object.print_log(log_text)
            log_text = ' N hit documents:\t ' + self.performance_statistics_overall_dict[key]['N_VALIDATION_HIT_DOCUMENTS']['NLP_WITHOUT_MANUAL_REVIEW'] + \
                       '\t\t ' + self.performance_statistics_overall_dict[key]['N_VALIDATION_HIT_DOCUMENTS']['NLP_MANUAL_REVIEW']
            self.logger_object.print_log(log_text)
            log_text = ' accuracy:\t\t ' + self.performance_statistics_overall_dict[key]['ACCURACY']['NLP_WITHOUT_MANUAL_REVIEW'] + \
                       '\t\t ' + self.performance_statistics_overall_dict[key]['ACCURACY']['NLP_MANUAL_REVIEW']
            self.logger_object.print_log(log_text)
            log_text = ' precision:\t\t ' + self.performance_statistics_overall_dict[key]['PRECISION']['NLP_WITHOUT_MANUAL_REVIEW'] + \
                       '\t\t ' + self.performance_statistics_overall_dict[key]['PRECISION']['NLP_MANUAL_REVIEW']
            self.logger_object.print_log(log_text)
            log_text = ' recall:\t\t ' + self.performance_statistics_overall_dict[key]['RECALL']['NLP_WITHOUT_MANUAL_REVIEW'] + \
                       '\t\t ' + self.performance_statistics_overall_dict[key]['RECALL']['NLP_MANUAL_REVIEW']
            self.logger_object.print_log(log_text)
            log_text = ' F1:\t\t\t ' + self.performance_statistics_overall_dict[key]['F1']['NLP_WITHOUT_MANUAL_REVIEW'] + \
                       '\t\t ' + self.performance_statistics_overall_dict[key]['F1']['NLP_MANUAL_REVIEW']
            self.logger_object.print_log(log_text)
        
    #
    def generate_csv_file(self):
        self.csv_header = re.sub('^\n', '', self.csv_header)
        self.csv_header = re.sub('\n.*', '', self.csv_header)
        self.csv_header = re.sub(', $', '', self.csv_header)
        self.csv_body = re.sub('^\n', '', self.csv_body)
        self.csv_body = re.sub(', \n', '\n', self.csv_body)
        self.csv_body = re.sub(', $', '', self.csv_body)
        csv_text = self.csv_header + '\n' + self.csv_body
        with open('nlp_output.csv', 'w') as f:
            f.write(csv_text)
        
    #
    def get_performance_data(self, display_flg):
        self.read_nlp_data()
        self.calculate_performance(display_flg)
            
    #
    def read_nlp_data(self):
        static_data = self.static_data_object.get_static_data()
        filename = static_data['project_name'] + '/' + \
                   static_data['project_subdir'] + '/' + \
                   static_data['project_name'] + '.json'
        self.nlp_data = \
            self.json_manager_registry[filename].read_nlp_data_from_package_json_file()
         
    #
    def write_performance_data(self):
        static_data = self.static_data_object.get_static_data()
        filename = static_data['project_name'] + '/test/' + \
                   static_data['project_name'] + '.performance.json'
        self.json_manager_registry[filename].write_file(self.performance_statistics_overall_dict)