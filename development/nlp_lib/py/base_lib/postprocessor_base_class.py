# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 13:39:32 2018

@author: haglers
"""

#
import os
import re

#
class Postprocessor_base(object):
    
    #
    def __init__(self, static_data):
        self.data_dict_list = {}
        self.filename = None
        
        #
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
        self.manual_review = \
            json_structure_manager.pull_key('manual_review')
        #
    
    #
    def _append_data(self, idx, key, data_dict_list, value_list):
        if len(value_list) > 0:
            data_dict_list[idx][self.nlp_data_key][0][key][self.query_name][self.nlp_value_key] \
                = value_list
            data_dict_list[idx][self.nlp_data_key][0][key][self.query_name][self.nlp_query_key] \
                = self.query_name
            data_dict_list[idx][self.nlp_data_key][0][key][self.query_name][self.nlp_section_key] \
                = key[0]
            if key[1]:
                data_dict_list[idx][self.nlp_data_key][0][key][self.query_name][self.nlp_specimen_key] \
                    = key[1]
        return data_dict_list
    
    #
    def _build_json_structure(self, data_dict_list):
        for i in range(len(data_dict_list)):
            data_dict_list[i][self.nlp_data_key] = {}
            for j in range(len(data_dict_list[i]['DOCUMENT_FRAME'])):
                key = data_dict_list[i]['DOCUMENT_FRAME'][j][0]
                datetime = data_dict_list[i]['DOCUMENT_FRAME'][j][1]
                text = data_dict_list[i]['DOCUMENT_FRAME'][j][2]
                if len(data_dict_list[i]['DOCUMENT_FRAME'][j]) > 3:
                    elements = data_dict_list[i]['DOCUMENT_FRAME'][j][3:]
                else:
                    elements = []
                if key not in data_dict_list[i][self.nlp_data_key].keys():
                    data_dict_list[i][self.nlp_data_key][key] = {}
                if self.query_name not in data_dict_list[i][self.nlp_data_key][key]:
                    data_dict_list[i][self.nlp_data_key][key][self.query_name] = {}
                if self.nlp_tool_output_key not in data_dict_list[i][self.nlp_data_key][key][self.query_name]:
                    data_dict_list[i][self.nlp_data_key][key][self.query_name][self.nlp_tool_output_key] = {}
                if self.nlp_datetime_key not in data_dict_list[i][self.nlp_data_key][key][self.query_name][self.nlp_tool_output_key].keys():
                    data_dict_list[i][self.nlp_data_key][key][self.query_name][self.nlp_tool_output_key][self.nlp_datetime_key] = []
                    data_dict_list[i][self.nlp_data_key][key][self.query_name][self.nlp_tool_output_key][self.nlp_element_key + str(0)] = []
                data_dict_list[i][self.nlp_data_key][key][self.query_name][self.nlp_tool_output_key][self.nlp_datetime_key].append(datetime)
                data_dict_list[i][self.nlp_data_key][key][self.query_name][self.nlp_tool_output_key][self.nlp_element_key + str(0)].append(text)
                for j in range(len(elements)):
                    if self.nlp_element_key+str(j+1) not in data_dict_list[i][self.nlp_data_key][key][self.query_name][self.nlp_tool_output_key].keys():
                        data_dict_list[i][self.nlp_data_key][key][self.query_name][self.nlp_tool_output_key][self.nlp_element_key+str(j+1)] = []
                    data_dict_list[i][self.nlp_data_key][key][self.query_name][self.nlp_tool_output_key][self.nlp_element_key+str(j+1)].append(elements[j])
        return data_dict_list
    
    #
    def _create_data_structure(self, match_str, data_dict_list):
        for i in range(len(data_dict_list)):
            data_dict_list[i][self.nlp_data_key] = {}
        for i in range(len(data_dict_list)):
            for entry in data_dict_list[i]['DOCUMENT_FRAME']:
                if re.match(match_str, entry[0][0]):
                    key = (entry[0][0], '')
                    entry_text = entry[2]
                    if key not in data_dict_list[i][self.nlp_data_key]:
                        data_dict_list[i][self.nlp_data_key][key] = {}
                        data_dict_list[i][self.nlp_data_key][key][self.query_name] = {}
                        data_dict_list[i][self.nlp_data_key][key][self.query_name][self.nlp_tool_output_key] = {}
                    if self.nlp_element_key + str(0) not in data_dict_list[i][self.nlp_data_key][key][self.query_name][self.nlp_tool_output_key].keys():
                        data_dict_list[i][self.nlp_data_key][key][self.query_name][self.nlp_tool_output_key][self.nlp_element_key + str(0)] = []
                    data_dict_list[i][self.nlp_data_key][key][self.query_name][self.nlp_tool_output_key][self.nlp_element_key + str(0)].append(entry_text)
        return data_dict_list
    
    #
    def _extract_data_value(self, text_list):
        print('self._extract_data_value function not defined')
    
    #
    def _extract_data_values(self, data_dict_list):
        for i in range(len(data_dict_list)):
            num_components = len(data_dict_list[i][self.nlp_data_key])
            element_keys_dict = {}
            text_list_dict = {}
            for idx in range(num_components):
                element_keys_dict[idx] = {}
                text_list_dict[idx] = {}
                if len(data_dict_list[i][self.nlp_data_key][idx]) > 0:
                    for key in data_dict_list[i][self.nlp_data_key][idx].keys():
                        keys = \
                            data_dict_list[i][self.nlp_data_key][idx][key][self.query_name][self.nlp_tool_output_key].keys()
                        element_keys = [k for k in keys if self.nlp_element_key in k]
                        element_keys = list(set(element_keys))
                        element_keys_dict[idx][key] = element_keys
                    for key in element_keys_dict[idx].keys():
                        element_keys = element_keys_dict[idx][key]
                        if len(element_keys) > 0:
                            text_list = []
                            for j in range(len(element_keys)):
                                text_list.append(data_dict_list[i][self.nlp_data_key][idx][key][self.query_name][self.nlp_tool_output_key][self.nlp_element_key + str(j)])
                            text_list_dict[idx][key] = text_list
            keys = []
            for idx in range(num_components):
                keys.extend(list(text_list_dict[idx].keys()))
            keys = sorted(list(set(keys)))
            for key in keys:
                text_list = {}
                for idx in range(num_components):
                    if key in text_list_dict[idx].keys():
                        text_list[idx] = text_list_dict[idx][key]
                    else:
                        text_list[idx] = []
                value_list = self._extract_data_value(text_list)
                data_dict_list =\
                    self._append_data(i, key, data_dict_list, value_list)
        for i in range(len(data_dict_list)):
            try:
                data_dict_list[i][self.nlp_data_key] = \
                    data_dict_list[i][self.nlp_data_key][0]
            except:
                pass
        return data_dict_list
    
    #
    def _merge_data_dicts(self, data_dict_list):
        num_components = len(data_dict_list)
        doc_ids = []
        for idx in range(num_components):
            for i in range(len(data_dict_list[idx])):
                doc_ids.append(data_dict_list[idx][i]['DOCUMENT_ID'])
        doc_ids = sorted(list(set(doc_ids)))
        data_dict_list_out = []
        for doc_id in doc_ids:
            document_frame = {}
            nlp_data = {}
            for idx in range(num_components):
                document_frame[idx] = None
                nlp_data[idx] = None
                for i in range(len(data_dict_list[idx])):
                    if data_dict_list[idx][i]['DOCUMENT_ID'] == doc_id:
                        document_frame[idx] = data_dict_list[idx][i]['DOCUMENT_FRAME']
                        nlp_data[idx] = data_dict_list[idx][i][self.nlp_data_key]
                        break
                if document_frame[idx] is None:
                    document_frame[idx] = []
                if nlp_data[idx] is None:
                    nlp_data[idx] = []
            data_dict = {}
            data_dict['DOCUMENT_ID'] = doc_id
            data_dict['DOCUMENT_FRAME'] = []
            data_dict[self.nlp_data_key] = []
            for idx in range(num_components):
                data_dict['DOCUMENT_FRAME'].append(document_frame[idx])
                data_dict[self.nlp_data_key].append(nlp_data[idx])
            data_dict_list_out.append(data_dict)
        return data_dict_list_out
    
    #
    def pull_data_dict_base_keys_list(self):
        return [ 'DOCUMENT_ID', 'DOCUMENT_FRAME' ]
    
    #
    def pull_data_dict_list(self):
        return self.data_dict_list     
    
    #
    def push_data_dict(self, data_dict_list, idx=0, filename=None):
        self.data_dict_list[idx] = data_dict_list
        if idx == 0:
            self.filename = filename
        
    #
    def push_diagnosis_reader(self, diagnosis_reader):
        self.diagnosis_reader = diagnosis_reader
    
    #
    def run_postprocessor(self, query_name=None, section_name=None):
        if query_name is None:
            base = os.path.basename(self.filename)
            query_name = os.path.splitext(base)[0]
            query_name = query_name.upper()
        self.query_name = query_name
        num_components = len(self.data_dict_list)
        for idx in range(num_components):
            self.data_dict_list[idx] = \
                self._build_json_structure(self.data_dict_list[idx])
            if section_name is not None:
                self.data_dict_list[idx] = \
                    self._create_data_structure(section_name, self.data_dict_list[idx])
        data_dict_list_tmp = self.data_dict_list
        self.data_dict_list = {}
        for idx in range(num_components):
            self.data_dict_list[idx] = data_dict_list_tmp[idx]
        self.data_dict_list = self._merge_data_dicts(self.data_dict_list)
        self.data_dict_list = self._extract_data_values(self.data_dict_list)