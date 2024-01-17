# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 14:28:32 2018

@author: haglers
"""

#
import os
import urllib3

#
from base_lib.manager_base_class \
    import Manager_base
from tools_lib.processing_tools_lib.file_processing_tools \
    import read_xml_file
    
#
def _get_data_dict_lists(data_dict_classes_list):
    data_dict_lists = []
    for data_dict_class in data_dict_classes_list:
        data_dict_lists.append(data_dict_class.pull_data_dict_list())
    return data_dict_lists

#
def _get_data_dict_base_keys_list(data_dict_classes_list):
    data_dict_base_keys = []
    for data_dict_class in data_dict_classes_list:
        data_dict_base_keys.append(data_dict_class.pull_data_dict_base_keys_list())
    return data_dict_base_keys

#
def _get_document_ids(data_dict_classes_list):
    document_ids = []
    data_dict_lists = \
        _get_data_dict_lists(data_dict_classes_list)
    data_dict_base_keys = \
        _get_data_dict_base_keys_list(data_dict_classes_list)
    for i in range(len(data_dict_lists)):
        data_dict_list = data_dict_lists[i]
        for data_dict in data_dict_list:
            keys = data_dict.keys()
            if len(keys) > len(data_dict_base_keys[i]):
                document_ids.append(data_dict['DOCUMENT_ID'])
    document_ids = sorted(list(set(document_ids)))
    return document_ids
    
#
def _merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z

#
urllib3.disable_warnings()

#
class Output_manager(Manager_base):

    #
    def __init__(self, static_data_object, logger_object, metadata_manager):
        Manager_base.__init__(self, static_data_object, logger_object)
        self.metadata_manager = metadata_manager
        static_data = self.static_data_object.get_static_data()
        self.project_name = static_data['project_name']
        self.merged_data_dict_list = []
        self.data_dict_classes_list = []
    
    #
    def append(self, data_dict):
        self.data_dict_classes_list.append(data_dict)
    
    #
    def get_data(self):
        return self.merged_data_dict_list
    
    #
    def get_merged_data_dict_list(self):
        return self.merged_data_dict_list
    
    #
    def include_metadata(self):
        self.metadata_manager.load_metadata()
        self.metadata_dict_dict, self.metadata_keys = self.metadata_manager.read_metadata()
        for i in range(len(self.merged_data_dict_list)):
            document_id = self.merged_data_dict_list[i]['DOCUMENT_ID']
            self.merged_data_dict_list[i][self.metadata_key] = \
                self.metadata_dict_dict[document_id][self.metadata_key]
            self.merged_data_dict_list[i][self.nlp_metadata_key] = \
                self.metadata_dict_dict[document_id][self.nlp_metadata_key]
    
    #
    def include_text(self):
        for i in range(len(self.merged_data_dict_list)):
            document_id = self.merged_data_dict_list[i]['DOCUMENT_ID']
            filename = os.path.join(self.preprocessing_data_out, document_id + '.xml')
            tree = read_xml_file(filename)
            raw_text = tree.find('RAW_TEXT')
            self.merged_data_dict_list[i]['RAW_TEXT'] = raw_text.text
            rpt_text = tree.find('rpt_text')
            self.merged_data_dict_list[i]['PREPROCESSED_TEXT'] = rpt_text.text
    
    #
    def merge_data_dict_lists(self):
        merged_data_dict_list = []
        document_ids = _get_document_ids(self.data_dict_classes_list)
        for document_id in document_ids:
            merged_dict = {}
            merged_dict['DOCUMENT_ID'] = document_id
            merged_dict[self.nlp_data_key] = {}
            for data_dict_class in self.data_dict_classes_list:
                data_dict_list = data_dict_class.pull_data_dict_list()
                for data_dict in data_dict_list:
                    if data_dict['DOCUMENT_ID'] == document_id:
                        if isinstance(data_dict[self.nlp_data_key], dict):
                            data_keys_x = list(data_dict[self.nlp_data_key].keys())
                        else:
                            data_keys_x = []
                        for data_key in data_keys_x:
                            if str(data_key) not in merged_dict[self.nlp_data_key].keys():
                                merged_dict[self.nlp_data_key][str(data_key)] = {}
                            merged_dict[self.nlp_data_key][str(data_key)] = \
                                _merge_two_dicts(merged_dict[self.nlp_data_key][str(data_key)],
                                                 data_dict[self.nlp_data_key][data_key])
            merged_data_dict_list.append(merged_dict)
        self.merged_data_dict_list = merged_data_dict_list
        
    #
    def push_linguamatics_i2e_preprocessing_data_out_dir(self, directory):
        self.preprocessing_data_out = directory
        
    #
    def push_postprocessing_data_out_dir(self, directory):
        self.data_out = directory