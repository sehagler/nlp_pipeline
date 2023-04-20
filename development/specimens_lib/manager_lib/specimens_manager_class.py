# -*- coding: utf-8 -*-
"""
Created on Mon Mar 04 10:19:41 2019

@author: haglers
"""

#
import ast
from copy import deepcopy
import json
import os
from pathlib import Path
import traceback

#
from base_lib.manager_base_class import Manager_base
from logger_lib.object_lib.logger_object_class import Logger_object
from tools_lib.processing_tools_lib.function_processing_tools \
    import sequential_composition
from tools_lib.processing_tools_lib.variable_processing_tools \
    import trim_data_value
    
#
def _correct_merged_data(raw_data_json, filename, log_dir, manual_review):
    config = Path(os.path.join(log_dir, filename))
    if config.is_file():
        correction_patientIds = []
        correction_labIds = []
        correction_documents = []
        with open(os.path.join(log_dir, filename), 'r') as f:
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
                                    documents[key3] = \
                                        raw_data_json[key0][key1][key2][key3]
                corrected_data_json[correction_patientIds[i]][correction_labIds[i]] = \
                    _merge_documents(documents)
            else:
                corrected_data_json[correction_patientIds[i]][correction_labIds[i]] = \
                    manual_review
    else:
        corrected_data_json = {}
    return corrected_data_json
    
#                 
def _evaluate_generic(entry_label, data_json):
    data_json_tmp = data_json
    for key0 in data_json_tmp.keys():
        for key1 in data_json_tmp[key0].keys():
            for key2 in data_json_tmp[key0][key1].keys():
                try:
                    values = data_json_tmp[key0][key1][key2][entry_label]
                    values = trim_data_value(values)
                    values = list(set(values))
                    if len(values) == 1:
                        value = values[0]
                    elif len(values) > 1:
                        value = 'MANUAL_REVIEW'
                        
                        # kludge to fix BeatAML projects
                        if entry_label == 'FISH.Analysis.Summary':
                            value = values[-1]
                        # kludge to fix BeatAML projects
                        
                    else:
                        value = None
                    if value is not None:
                        data_json[key0][key1][key2][entry_label] = value
                    else:
                        del data_json[key0][key1][key2][entry_label]
                except Exception:
                    traceback.print_exc()
    return data_json

#
def _get_document_map(argument_dict):
    specimen_tree = argument_dict['specimen_tree']
    deidentifier_key_dict = argument_dict['deidentifier_key_dict']
    document_map = []
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
            document_map.append([key0, key1, date_str, key[0], documents])
    return document_map
    
#
def _identify_documents_for_same_specimen(specimen_tree):
    for key0 in specimen_tree.keys():
        for key1 in specimen_tree[key0].keys():
            documents = []
            for key2 in specimen_tree[key0][key1].keys():
                documents.extend(specimen_tree[key0][key1][key2])
            specimen_tree[key0][key1] = documents
    return specimen_tree

#
def _identify_documents_with_same_proc_nm(data_json):
    specimen_tree = data_json
    for key0 in specimen_tree.keys():
        for key1 in specimen_tree[key0].keys():
            for key2 in specimen_tree[key0][key1].keys():
                documents = specimen_tree[key0][key1][key2]
                specimen_tree[key0][key1][key2] = documents.keys()
    return specimen_tree

#
def _make_strings(column_values):
    for i in range(len(column_values)):
        column_values[i] = str(column_values[i])
    return column_values

#
def _merge_documents(documents_in):
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
def _trim_documents(specimen_dict):
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
def _trim_documents_wrapper(argument_dict):
    specimen_tree_in = argument_dict['specimen_tree']
    specimen_dict = argument_dict['specimen_dict']
    deidentifier_key_dict = argument_dict['deidentifier_key_dict']
    specimen_tree = {}
    document_dict = {}
    for key0 in specimen_tree_in.keys():
        if key0 in deidentifier_key_dict.keys():
            document_dict[key0] = {}
            patientid = deidentifier_key_dict[key0]['patientId']
            labid_dict = deidentifier_key_dict[key0]['labIds']
            for key1 in labid_dict.keys():
                document_dict[key0][key1] = \
                    _trim_documents(specimen_dict[key0][key1])
                if bool(document_dict[key0][key1]):
                    labid = labid_dict[key1]
                    if patientid not in specimen_tree.keys():
                        specimen_tree[patientid] = {}
                    if labid not in specimen_tree[patientid].keys():
                        specimen_tree[patientid][labid] = {}
                    specimen_tree[patientid][labid] = document_dict[key0][key1]
    return_dict = {}
    return_dict['specimen_tree'] = specimen_tree
    return_dict['deidentifier_key_dict'] = deidentifier_key_dict
    return return_dict

#
def _trim_specimen_tree(argument_dict):
    specimen_tree_in = argument_dict['specimen_tree']
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
    return_dict = {}
    return_dict['specimen_tree'] = specimen_tree
    return_dict['deidentifier_key_dict'] = \
        argument_dict['deidentifier_key_dict']
    return return_dict

#
class Specimens_manager(Manager_base):
    
    #
    def __init__(self, static_data_object):
        Manager_base.__init__(self, static_data_object)
        static_data = static_data_object.get_static_data()
        self.directory_manager = static_data['directory_manager']
        self.log_dir = self.directory_manager.pull_directory('log_dir')
        self.logger_object = Logger_object(self.log_dir)
    
    #                 
    def _evaluate_generic(self, entry_label, data_json):
        return _evaluate_generic(entry_label, data_json)
    
    #
    def _make_strings(self, column_values):
        return _make_strings(column_values)
    
    #
    def generate_document_map(self, data_json, filename):
        deidentifier_key_dict = \
            self._get_deidentifier_keys(self.deidentifier_xlsx)
        generate_specimen_tree = \
            sequential_composition(_identify_documents_for_same_specimen,
                               _identify_documents_with_same_proc_nm)
        specimen_tree = generate_specimen_tree(deepcopy(data_json))
        specimen_dict = self._cluster_specimens(specimen_tree,
                                                deidentifier_key_dict)
        get_document_map = sequential_composition(_get_document_map,
                                              _trim_specimen_tree,
                                              _trim_documents_wrapper)
        argument_dict = {}
        argument_dict['specimen_tree'] = specimen_tree
        argument_dict['specimen_dict'] = specimen_dict
        argument_dict['deidentifier_key_dict'] = deidentifier_key_dict
        document_map = get_document_map(argument_dict)
        for i in range(len(document_map)):
            log_item = document_map[i]
            self.logger_object.log_entry_merge_documents(log_item[0],
                                                         log_item[1], 
                                                         log_item[2],
                                                         log_item[3],
                                                         log_item[4])
        self.logger_object.create_file(filename)
        self.data_json = _correct_merged_data(data_json, filename, 
                                              self.log_dir, self.manual_review)
        self._evaluate_features()
    
    #
    def generate_json_file(self, jsons_out_dir, filename):
        with open(os.path.join(jsons_out_dir, filename), 'w') as f:
            json.dump(self.data_json, f)
            
    #
    def get_data_json(self):
        return self.data_json