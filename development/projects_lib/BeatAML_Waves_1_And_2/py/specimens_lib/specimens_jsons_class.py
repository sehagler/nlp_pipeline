# -*- coding: utf-8 -*-
"""
Created on Fri Mar 01 08:34:59 2019

@author: haglers
"""

#
import ast
from copy import deepcopy
import json
import os
from pathlib import Path
import xlrd

#
from nlp_pipeline_lib.logger_lib.logger_class import Logger
from nlp_pipeline_lib.specimens_lib.lib.specimens_base_class \
    import Specimens_base
from tool_lib.py.query_tools_lib.base_lib.date_tools_base import get_date_difference

#
class Specimens_jsons(Specimens_base):
    
    #
    def __init__(self, static_data, data_json):
        self.directory_manager = static_data['directory_manager']
        self.log_dir = self.directory_manager.pull_directory('log_dir')
        self.logger = Logger(self.log_dir)
        specimen_tree = self._identify_documents_with_same_proc_nm(deepcopy(data_json))
        specimen_tree = self._identify_documents_for_same_specimen(specimen_tree)
        specimen_dict = self._cluster_specimens(specimen_tree)
        specimen_tree = self._trim_documents_wrapper(specimen_tree, specimen_dict)
        specimen_tree = self._trim_specimen_tree(specimen_tree)
        self._generate_document_map(specimen_tree)
        self.logger.create_file('file_map.txt')
        self.data_json = self._correct_merged_data(data_json)
        self._evaluate_features()
        
    #
    def _cluster_specimens(self, specimen_tree_in):
        deidentifier_key_dict = self._get_deidentifier_keys()
        specimen_dict = {}
        for key0 in specimen_tree_in.keys():
            if key0 in deidentifier_key_dict.keys():
                if key0 not in specimen_dict.keys():
                    specimen_dict[key0] = {}
                labid_dict = deidentifier_key_dict[key0]['labIds']
                for key1 in labid_dict.keys():
                    if key1 not in specimen_dict[key0].keys():
                        specimen_dict[key0][key1] = {}
                    for key2 in specimen_tree_in[key0].keys():
                        documents = specimen_tree_in[key0][key2]
                        for document in documents:
                            proc_nm = self.metadata_dict_dict[document.split('_')[0]]['METADATA']['PROC_NM']
                            for document in documents:
                                if self.metadata_dict_dict[document.split('_')[0]]['METADATA']['PROC_NM'] == proc_nm:
                                    doc_label = document.split('_')[1]
                                    lower_bound_days, upper_bound_days = self._get_days_window(proc_nm)
                                    date_diff = get_date_difference(key2, key1)
                                    if ( lower_bound_days <= date_diff ) and ( date_diff <= upper_bound_days ):
                                        process_label = self._get_process_label(proc_nm, doc_label)
                                        if process_label not in specimen_dict[key0][key1].keys():
                                            specimen_dict[key0][key1][process_label] = []
                                        specimen_dict[key0][key1][process_label].append([date_diff, document])
        return specimen_dict
        
    #
    def _correct_merged_data(self, raw_data_json):
        filename = 'file_map.txt'
        config = Path(os.path.join(self.log_dir, filename))
        if config.is_file():
            correction_patientIds = []
            correction_labIds = []
            correction_documents = []
            with open(os.path.join(self.log_dir, filename), 'r') as f:
                line = f.readline()
                while line:
                    data_map = line.split('\t')
                    correction_patientIds.append(data_map[0])
                    correction_labIds.append(data_map[1])
                    correction_documents.append(ast.literal_eval(data_map[4]))
                    line = f.readline()
            corrected_data_json = {}
            for i in range(len(correction_documents)):
                if correction_patientIds[i] not in corrected_data_json.keys():
                    corrected_data_json[correction_patientIds[i]] = {}
                if correction_labIds[i] not in corrected_data_json[correction_patientIds[i]].keys():
                    documents = {}
                    for key0 in raw_data_json.keys():
                        for key1 in raw_data_json[key0].keys():
                            for key2 in raw_data_json[key0][key1].keys():
                                for key3 in raw_data_json[key0][key1][key2].keys():
                                    if key3 in correction_documents[i]:
                                        documents[key3] = raw_data_json[key0][key1][key2][key3]
                    corrected_data_json[correction_patientIds[i]][correction_labIds[i]] = \
                        self._merge_documents(documents)
                else:
                    corrected_data_json[correction_patientIds[i]][correction_labIds[i]] = \
                        self.manual_review
        else:
            corrected_data_json = {}
        return corrected_data_json
                    
    #
    def _generate_document_map(self, specimen_tree):
        deidentifier_key_dict = self._get_deidentifier_keys()
        for key0 in specimen_tree.keys():
            labid_dicts = []
            for key in deidentifier_key_dict.keys():
                    if deidentifier_key_dict[key]['patientId'] == key0:
                        labid_dicts.append(deidentifier_key_dict[key]['labIds'])    
            if len(labid_dicts) == 1:
                labid_dict = labid_dicts[0]
            else:
                labid_dict = {}
            for key1 in specimen_tree[key0].keys():
                date_str = []
                for key in labid_dict.keys():
                    if labid_dict[key] == key1:
                        date_str.append(key)
                documents = specimen_tree[key0][key1]
                documents = list(set(documents))
                self.logger.log_entry_merge_documents(key0, key1, date_str, key[0], documents)
                
    #
    def _get_deidentifier_keys(self):
        deidentifier_key_dict = {}
        book = xlrd.open_workbook(self.deidentifier_xlsx)
        sheet = book.sheet_by_index(0)
        patientids = sheet.col_values(0)[1:]
        mrns = sheet.col_values(1)[1:]
        labids = sheet.col_values(2)[1:]
        specimen_dates = self._make_strings(sheet.col_values(3)[1:])
        for mrn in list(set(mrns)):
            idxs = [ i for i, j in enumerate(mrns) if j == mrn ]
            patientid_tmp = list(set([ patientids[i] for i in idxs ]))
            for i in range(len(patientid_tmp)):
                patientid_tmp[i] = int(patientid_tmp[i])
            tmp_list = [ [labids[i], specimen_dates[i]] for i in idxs ]
            doc_dict = {}
            for item in tmp_list:
                doc_dict[item[1]] = item[0]
            if len(patientid_tmp) == 1:
                deidentifier_key_dict[mrn] = {}
                deidentifier_key_dict[mrn]['patientId'] = str(patientid_tmp[0])
                deidentifier_key_dict[mrn]['labIds'] = doc_dict
        return deidentifier_key_dict
    
    #
    def _get_specimen_dict(self, specimen_tree, key0, key1):
        specimen_dict = {}
        for key2 in specimen_tree[key0].keys():
            documents = specimen_tree[key0][key2]
            for document in documents:
                proc_nm = self.metadata_dict_dict[document]['PROC_NM']
                for document in documents:
                    if self.metadata_dict_dict[document]['PROC_NM'] == proc_nm:
                        lower_bound_days, upper_bound_days = self._get_days_window(proc_nm)
                        date_diff = self._get_date_difference(key2, key1)
                        if ( lower_bound_days <= date_diff ) and ( date_diff <= upper_bound_days ):
                            process_label = self._get_process_label(proc_nm)
                            if process_label not in specimen_dict.keys():
                                specimen_dict[process_label] = []
                            specimen_dict[process_label].append([date_diff, document])
        return specimen_dict
    
    #
    def _identify_documents_for_same_specimen(self, specimen_tree):
        for key0 in specimen_tree.keys():
            for key1 in specimen_tree[key0].keys():
                documents = []
                for key2 in specimen_tree[key0][key1].keys():
                    documents.extend(specimen_tree[key0][key1][key2])
                specimen_tree[key0][key1] = documents
        return specimen_tree
    
    #
    def _identify_documents_with_same_proc_nm(self, data_json):
        specimen_tree = data_json
        for key0 in specimen_tree.keys():
            for key1 in specimen_tree[key0].keys():
                for key2 in specimen_tree[key0][key1].keys():
                    documents = specimen_tree[key0][key1][key2]
                    specimen_tree[key0][key1][key2] = documents.keys()
        return specimen_tree
    
    #
    def _merge_documents(self, documents_in):
        document = {}
        doc_keys = []
        doc_nums = ''
        for key in sorted(documents_in.keys()):
            doc_nums+= '_' + key
            doc_keys.extend(documents_in[key].keys())
        doc_keys = list(set(doc_keys))
        doc_nums = doc_nums[1:]
        document[doc_nums] = {}
        for doc_key in doc_keys:
            document[doc_nums][doc_key] = []
        for key in documents_in.keys():
            for doc_key in doc_keys:
                if doc_key in documents_in[key].keys():
                    document[doc_nums][doc_key].extend(documents_in[key][doc_key])
        return document
                    
    #
    def _trim_data_value(self, data_value):
        data_value_tmp = data_value
        data_value = []
        for item in data_value_tmp:
            data_value.extend(item)
        try:
            data_value = list(set(data_value))
        except:
            pass
        return data_value
    
    #
    def _trim_documents(self, specimen_dict):
        min_abs_date_diff = {}
        for process_label in specimen_dict.keys():
            if process_label not in min_abs_date_diff.keys():
                min_abs_date_diff[process_label] = None
        for process_label in specimen_dict.keys():
            document_list = specimen_dict[process_label]
            if len(document_list) > 0:
                if min_abs_date_diff[process_label] is None:
                    min_abs_date_diff[process_label] = abs(document_list[0][0])
                for item in document_list:
                    if abs(item[0]) < min_abs_date_diff[process_label]:
                        min_abs_date_diff[process_label] = abs(item[0])
        document_dict = {}
        for process_label in specimen_dict.keys():
            document_list = specimen_dict[process_label]
            for item in document_list:
                date_diff = item[0]
                if abs(date_diff) == min_abs_date_diff[process_label]:
                    document = item[1]
                    if process_label not in document_dict.keys():
                        document_dict[process_label] = {}
                    if date_diff not in document_dict[process_label]:
                        document_dict[process_label][date_diff] = []
                    document_dict[process_label][date_diff].append(document)
        return document_dict
    
    #
    def _trim_documents_wrapper(self, specimen_tree_in, specimen_dict):
        deidentifier_key_dict = self._get_deidentifier_keys()
        specimen_tree = {}
        document_dict = {}
        for key0 in specimen_tree_in.keys():
            if key0 in deidentifier_key_dict.keys():
                document_dict[key0] = {}
                patientid = deidentifier_key_dict[key0]['patientId']
                labid_dict = deidentifier_key_dict[key0]['labIds']
                for key1 in labid_dict.keys():
                    document_dict[key0][key1] = self._trim_documents(specimen_dict[key0][key1])
                    if bool(document_dict[key0][key1]):
                        labid = labid_dict[key1]
                        if patientid not in specimen_tree.keys():
                            specimen_tree[patientid] = {}
                        if labid not in specimen_tree[patientid].keys():
                            specimen_tree[patientid][labid] = {}
                        specimen_tree[patientid][labid] = document_dict[key0][key1]
        return specimen_tree
    
    #
    def _trim_specimen_tree(self, specimen_tree_in):
        specimen_tree = {}
        for key0 in specimen_tree_in.keys():
            specimen_tree[key0] = {}
            for key1 in specimen_tree_in[key0].keys():
                specimen_tree[key0][key1] = []
                for key2 in specimen_tree_in[key0][key1].keys():
                    keys = specimen_tree_in[key0][key1][key2].keys()
                    min_abs_key = min(list(set([abs(i) for i in keys])))
                    key = [ i for i in keys if abs(i) == min_abs_key ]
                    if len(key) == 1:
                        document = specimen_tree_in[key0][key1][key2][key[0]]
                        specimen_tree[key0][key1].extend(document)  
                    else:
                        print('error')
        return specimen_tree