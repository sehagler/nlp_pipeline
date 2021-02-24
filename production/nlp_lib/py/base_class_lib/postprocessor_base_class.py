# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 13:39:32 2018

@author: haglers
"""

#
import csv
import re

#
from nlp_lib.py.base_class_lib.packager_base_class import Packager_base

#
class Postprocessor_base(Packager_base):
    
    #
    def __init__(self, label, data_file, data_key_map, data_value_map):
        Packager_base.__init__(self)
        self.label = label
        self.data_csv = {}
        try:
            with open(data_file,'r') as f:
                csv_reader = csv.reader(f, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if line_count > 0:
                        if row[1] not in self.data_csv.keys():
                            self.data_csv[row[1]] = []
                        self.data_csv[row[1]].append(row[2:])
                    line_count += 1
        except:
            pass
        self.data_dict_list = []
        if bool(self.data_csv):
            self._build_data_dictionary()
        if data_key_map is not None:
            self.data_key_map = data_key_map
            self.data_keys = ['EXTRACTED_TEXT']
            self.data_labels = [self.data_key_map['EXTRACTED_TEXT']]
            for key in self.data_key_map:
                if key != 'EXTRACTED_TEXT':
                    self.data_keys.append(key)
                    self.data_labels.append(self.data_key_map[key])
        if data_value_map is not None:
            self.data_value_map = data_value_map
        if data_key_map is not None:
            self._build_json_structure()
        
    #
    def _append_data(self, idx, key, value_list):
        if len(value_list) > 0:
            value_list = list(set(value_list))
            self.data_dict_list[idx][self.nlp_data_key][key][self.label][self.nlp_value_key] \
                = value_list
        self.data_dict_list[idx][self.nlp_data_key][key][self.label][self.nlp_query_key] \
            = self.label
        self.data_dict_list[idx][self.nlp_data_key][key][self.label][self.nlp_section_key] \
            = key[0]
        if key[1]:
            self.data_dict_list[idx][self.nlp_data_key][key][self.label][self.nlp_specimen_key] \
                = key[1]
    
    #
    def _build_data_dictionary(self):
        for key in self.data_csv.keys():
            document_dict = {}
            document_dict['DOCUMENT_ID'] = key
            document_frame = []
            document_frame = self._build_document_frame(self.data_csv[key])
            document_dict['DOCUMENT_FRAME'] = document_frame
            self.data_dict_list.append(document_dict)
            
    #
    def _build_document_frame(self, data_list):
        document_frame = []
        for item in data_list:
            entry = []
            entry.append(tuple([item[1], item[3]]))
            entry.append(item[4])
            document_frame.append(entry)
            num_elements = len(item) - 14
            for i in range(num_elements):
                entry.append(item[5+i])
        return(document_frame)
    
    #
    def _build_json_structure(self):
        for i in range(len(self.data_dict_list)):
            self.data_dict_list[i][self.nlp_data_key] = {}
            for j in range(len(self.data_dict_list[i]['DOCUMENT_FRAME'])):
                key = self.data_dict_list[i]['DOCUMENT_FRAME'][j][0]
                text = self.data_dict_list[i]['DOCUMENT_FRAME'][j][1]
                if len(self.data_dict_list[i]['DOCUMENT_FRAME'][j]) > 2:
                    elements = self.data_dict_list[i]['DOCUMENT_FRAME'][j][2:]
                else:
                    elements = []
                if key not in self.data_dict_list[i][self.nlp_data_key].keys():
                    self.data_dict_list[i][self.nlp_data_key][key] = {}
                    self.data_dict_list[i][self.nlp_data_key][key][self.label] = {}
                if self.nlp_text_key not in self.data_dict_list[i][self.nlp_data_key][key][self.label].keys():
                    self.data_dict_list[i][self.nlp_data_key][key][self.label][self.nlp_text_key] = []
                self.data_dict_list[i][self.nlp_data_key][key][self.label][self.nlp_text_key].append(text)
                for j in range(len(elements)):
                    if self.nlp_text_element_key+str(j) not in self.data_dict_list[i][self.nlp_data_key][key][self.label].keys():
                        self.data_dict_list[i][self.nlp_data_key][key][self.label][self.nlp_text_element_key+str(j)] = []
                    self.data_dict_list[i][self.nlp_data_key][key][self.label][self.nlp_text_element_key+str(j)].append(elements[j])
                    
    #
    def _create_data_structure(self, match_str):
        for i in range(len(self.data_dict_list)):
            for entry in self.data_dict_list[i]['DOCUMENT_FRAME']:
                if re.match(match_str, entry[0][0]):
                    key = (entry[0][0], '')
                    entry_text = entry[1]
                    if key not in self.data_dict_list[i][self.nlp_data_key]:
                        self.data_dict_list[i][self.nlp_data_key][key] = {}
                        self.data_dict_list[i][self.nlp_data_key][key][self.label] = {}
                    self.data_dict_list[i][self.nlp_data_key][key][self.label][self.nlp_text_key] = []
                    self.data_dict_list[i][self.nlp_data_key][key][self.label][self.nlp_text_key].append(entry_text)
    
    #
    def get_data_dict_base_keys_list(self):
        return [ 'DOCUMENT_ID', 'DOCUMENT_FRAME' ]
    
    #
    def get_data_dict_list(self):
        return self.data_dict_list     