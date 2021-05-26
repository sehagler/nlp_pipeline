# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 13:39:32 2018

@author: haglers
"""

#
import csv
import re

#
class Postprocessor_base(object):
    
    #
    def __init__(self, project_data, label, data_file, data_key_map,
                 data_value_map):
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
        self.nlp_element_key = \
            json_structure_manager.pull_key('nlp_text_element_key')
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
        self.nlp_tool_output_key = \
            json_structure_manager.pull_key('nlp_tool_output_key')
        self.nlp_value_key = \
            json_structure_manager.pull_key('nlp_value_key')
            
        # to be moved to appropriate location
        self.multiple_specimens = \
            json_structure_manager.pull_key('multiple_specimens')
        self.multiple_values = \
            json_structure_manager.pull_key('multiple_values')
        #
        
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
            try:
                value_list = list(set(value_list))
            except:
                pass
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
            entry.append(tuple([item[2], item[4]]))
            entry.append(item[0])
            entry.append(item[5])
            document_frame.append(entry)
            num_elements = len(item) - 15
            for i in range(num_elements):
                entry.append(item[6+i])
        return(document_frame)
    
    #
    def _build_json_structure(self):
        for i in range(len(self.data_dict_list)):
            self.data_dict_list[i][self.nlp_data_key] = {}
            for j in range(len(self.data_dict_list[i]['DOCUMENT_FRAME'])):
                key = self.data_dict_list[i]['DOCUMENT_FRAME'][j][0]
                datetime = self.data_dict_list[i]['DOCUMENT_FRAME'][j][1]
                text = self.data_dict_list[i]['DOCUMENT_FRAME'][j][2]
                if len(self.data_dict_list[i]['DOCUMENT_FRAME'][j]) > 3:
                    elements = self.data_dict_list[i]['DOCUMENT_FRAME'][j][3:]
                else:
                    elements = []
                if key not in self.data_dict_list[i][self.nlp_data_key].keys():
                    self.data_dict_list[i][self.nlp_data_key][key] = {}
                    self.data_dict_list[i][self.nlp_data_key][key][self.label] = {}
                if self.nlp_tool_output_key not in self.data_dict_list[i][self.nlp_data_key][key][self.label]:
                    self.data_dict_list[i][self.nlp_data_key][key][self.label][self.nlp_tool_output_key] = {}
                if self.nlp_datetime_key not in self.data_dict_list[i][self.nlp_data_key][key][self.label][self.nlp_tool_output_key].keys():
                    self.data_dict_list[i][self.nlp_data_key][key][self.label][self.nlp_tool_output_key][self.nlp_datetime_key] = []
                    self.data_dict_list[i][self.nlp_data_key][key][self.label][self.nlp_tool_output_key][self.nlp_element_key + str(0)] = []
                self.data_dict_list[i][self.nlp_data_key][key][self.label][self.nlp_tool_output_key][self.nlp_datetime_key].append(datetime)
                self.data_dict_list[i][self.nlp_data_key][key][self.label][self.nlp_tool_output_key][self.nlp_element_key + str(0)].append(text)
                for j in range(len(elements)):
                    if self.nlp_element_key+str(j+1) not in self.data_dict_list[i][self.nlp_data_key][key][self.label][self.nlp_tool_output_key].keys():
                        self.data_dict_list[i][self.nlp_data_key][key][self.label][self.nlp_tool_output_key][self.nlp_element_key+str(j+1)] = []
                    self.data_dict_list[i][self.nlp_data_key][key][self.label][self.nlp_tool_output_key][self.nlp_element_key+str(j+1)].append(elements[j])
    
    #
    def _create_data_structure(self, match_str):
        for i in range(len(self.data_dict_list)):
            for entry in self.data_dict_list[i]['DOCUMENT_FRAME']:
                if re.match(match_str, entry[0][0]):
                    key = (entry[0][0], '')
                    entry_text = entry[2]
                    if key not in self.data_dict_list[i][self.nlp_data_key]:
                        self.data_dict_list[i][self.nlp_data_key][key] = {}
                        self.data_dict_list[i][self.nlp_data_key][key][self.label] = {}
                        self.data_dict_list[i][self.nlp_data_key][key][self.label][self.nlp_tool_output_key] = {}
                    self.data_dict_list[i][self.nlp_data_key][key][self.label][self.nlp_tool_output_key][self.nlp_element_key + str(0)] = []
                    self.data_dict_list[i][self.nlp_data_key][key][self.label][self.nlp_tool_output_key][self.nlp_element_key + str(0)].append(entry_text)
    
    #
    def _extract_data_value(self, text_list):
        print('self._extract_data_value function not defined')
        
    #
    def _extract_data_values(self):
        for i in range(len(self.data_dict_list)):
            for key in self.data_dict_list[i][self.nlp_data_key]:
                try:
                    text_list = \
                        self.data_dict_list[i][self.nlp_data_key][key][self.label][self.nlp_tool_output_key][self.nlp_element_key + str(0)]
                except:
                    text_list = []
                value_list = self._extract_data_value(text_list)
                self._append_data(i, key, value_list)
                
    #
    def _extract_data_values(self):
        for i in range(len(self.data_dict_list)):
            for key in self.data_dict_list[i][self.nlp_data_key]:
                try:
                    keys = \
                        self.data_dict_list[i][self.nlp_data_key][key][self.label][self.nlp_tool_output_key].keys()
                    element_keys = [k for k in keys if self.nlp_element_key in k]
                    element_keys = list(set(element_keys))
                    if len(element_keys) > 0:
                        text_list = []
                        for j in range(len(element_keys)):
                            text_list.append(self.data_dict_list[i][self.nlp_data_key][key][self.label][self.nlp_tool_output_key][self.nlp_element_key + str(j)])
                except:
                    text_list = []
                value_list = self._extract_data_value(text_list)
                self._append_data(i, key, value_list)
    
    #
    def get_data_dict_base_keys_list(self):
        return [ 'DOCUMENT_ID', 'DOCUMENT_FRAME' ]
    
    #
    def get_data_dict_list(self):
        return self.data_dict_list     