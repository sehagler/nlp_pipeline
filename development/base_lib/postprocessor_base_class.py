# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 13:39:32 2018

@author: haglers
"""

#
import os
import re

#
from base_lib.manager_base_class \
    import Manager_base
from lambda_lib.object_lib.lambda_object_class import Lambda_object

#
class Postprocessor_base(Manager_base):
    
    #
    def __init__(self, static_data_object):
        Manager_base.__init__(self, static_data_object)
        self.lambda_object = Lambda_object()
        self.data_dict_list = {}
        self.filename = None
    
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
                    data_dict_list[i][self.nlp_data_key][key][self.query_name][self.nlp_tool_output_key][self.nlp_text_element_key + str(0)] = []
                data_dict_list[i][self.nlp_data_key][key][self.query_name][self.nlp_tool_output_key][self.nlp_datetime_key].append(datetime)
                data_dict_list[i][self.nlp_data_key][key][self.query_name][self.nlp_tool_output_key][self.nlp_text_element_key + str(0)].append(text)
                for j in range(len(elements)):
                    if self.nlp_text_element_key+str(j+1) not in data_dict_list[i][self.nlp_data_key][key][self.query_name][self.nlp_tool_output_key].keys():
                        data_dict_list[i][self.nlp_data_key][key][self.query_name][self.nlp_tool_output_key][self.nlp_text_element_key+str(j+1)] = []
                    data_dict_list[i][self.nlp_data_key][key][self.query_name][self.nlp_tool_output_key][self.nlp_text_element_key+str(j+1)].append(elements[j])
        return data_dict_list
    
    #
    def _extract_data_value(self, text_list):
        print('self._extract_data_value function not defined')
    
    #
    def _extract_data_values(self, data_dict_list):
        for i in range(len(data_dict_list)):
            document_frames = data_dict_list[i]['DOCUMENT_FRAME']
            keys = []
            for j in range(len(document_frames)):
                for item in document_frames[j]:
                    keys.append(item[0])
            value_list_dict = {}
            for key in list(set(keys)):
                value_list = []
                for j in range(len(document_frames)):
                    value_list_tmp = []
                    for item in document_frames[j]:
                        if item[0] == key:
                            item[-2] = self._trim_snippet(item)
                            value_list_tmp.append(item[2:])
                    value_list.append(value_list_tmp)
                value_list_dict[key] = value_list
            extracted_data_dict = self._extract_data_value(value_list_dict)
            for key in extracted_data_dict.keys():
                data_dict_list =\
                    self._append_data(i, key, data_dict_list,
                                      extracted_data_dict[key])
        for i in range(len(data_dict_list)):
            try:
                data_dict_list[i][self.nlp_data_key] = \
                    data_dict_list[i][self.nlp_data_key][0]
            except Exception:
                traceback.print_exc()
        return data_dict_list
    
    #
    def _extract_value(self, context_regex, regex, map_func, text):
        val_list = []
        for m in re.finditer(context_regex, text):
            val_list_tmp = []
            for n in re.finditer(regex, m.group(0)):
                if map_func is not None:
                    val_list_tmp.append(map_func(n.group(0)))
                else:
                    val_list_tmp.append(n.group(0))
            if len(val_list_tmp) == 1:
                val_list.append(val_list_tmp[0])
            elif len(val_list_tmp) > 1:
                val_list_tmp = sorted(val_list_tmp)
                val_list_tmp = [ val_list_tmp[0], val_list_tmp[-1] ]
                val_list.append('-'.join(val_list_tmp))
        val_list = list(set(val_list))
        return val_list
    
    #
    def _generate_data_table(self, value_list_dict):
        data_table = []
        for key in value_list_dict.keys():
            text_list = value_list_dict[key]
            for item in text_list[0]:
                data_row = [ key ]
                for i in range(len(item)):
                    data_row.append(item[i])
                data_table.append(data_row)
        return data_table
    
    #
    def _generate_data_subtable(self, data_table, key):
        data_subtable = []
        for data_row in data_table:
            if data_row[0] == key:
                data_subtable.append(data_row)
        return data_subtable
        
    #
    def _get_data_table_keys(self, data_table):
        keys = []
        for data_row in data_table:
            keys.append(data_row[0])
        keys = list(set(keys))
        return keys
    
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
    def _trim_snippet(self, data_row):
        snippet_max_length = 250
        query_match = data_row[2]
        snippet = data_row[-2]
        if len(snippet) > snippet_max_length:
            match = re.search(re.escape(query_match), snippet)
            if match:
                match_start = match.span(0)[0]
                match_end = match.span(0)[1]
                preceding_match = snippet[:match_start]
                following_match = snippet[match_end:]
                residual_length = ( snippet_max_length - \
                                    (match_end - match_start) ) // 2
                if len(preceding_match) < residual_length:
                    residual_length = 2*residual_length - len(preceding_match)
                    delete_length = len(following_match) - residual_length
                    snippet = snippet[:-delete_length]
                elif len(following_match) < residual_length:
                    residual_length = 2*residual_length - len(following_match)
                    delete_length = len(preceding_match) - residual_length
                    snippet = snippet[delete_length:]
                else:
                    preceding_delete_length = len(preceding_match) - \
                                              residual_length
                    following_delete_length = len(following_match) - \
                                              residual_length
                    snippet = \
                        snippet[preceding_delete_length:-following_delete_length]
        return snippet
    
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
        data_dict_list_tmp = self.data_dict_list
        self.data_dict_list = {}
        for idx in range(num_components):
            self.data_dict_list[idx] = data_dict_list_tmp[idx]
        self.data_dict_list = self._merge_data_dicts(self.data_dict_list)
        self.data_dict_list = self._extract_data_values(self.data_dict_list)