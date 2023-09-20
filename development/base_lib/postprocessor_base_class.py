# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 13:39:32 2018

@author: haglers
"""

#
import os
import re
import traceback

#
from base_lib.manager_base_class import Manager_base
from tools_lib.processing_tools_lib.function_processing_tools \
    import parallel_composition, sequential_composition
    
#
def _build_data_dictionary(data_dict, document_list):
    data_dict_list = []
    if bool(data_dict):
        for key in data_dict.keys():
            if key in document_list:
                document_dict = {}
                document_dict['DOCUMENT_ID'] = key
                document_frame = []
                document_frame = _build_document_frame(data_dict[key])
                document_dict['DOCUMENT_FRAME'] = document_frame
                data_dict_list.append(document_dict)
    return data_dict_list
    
#
def _build_document_frame(data_list):
    document_frame = []
    for item in data_list:
        entry = []
        entry.append(tuple([item[1], item[2]]))
        entry.append(item[0])
        entry.append(item[3])
        document_frame.append(entry)
        num_elements = len(item) - 4
        for i in range(num_elements):
            entry.append(item[4+i])
    return document_frame
    
#
def _extract_value(context_regex, regex, map_func, text):
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
def _generate_data_table(value_list_dict):
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
def _generate_data_subtable(data_table, key):
    data_subtable = []
    for data_row in data_table:
        if data_row[0] == key:
            data_subtable.append(data_row)
    return data_subtable
    
#
def _get_data_table_keys(data_table):
    keys = []
    for data_row in data_table:
        keys.append(data_row[0])
    keys = list(set(keys))
    return keys

#
def _get_query_name(argument_dict):
    filename = argument_dict['filename']
    query_name = argument_dict['query_name']
    if query_name is None:
        base = os.path.basename(filename)
        query_name = os.path.splitext(base)[0]
        query_name = query_name.upper()
    return query_name

#
def _trim_snippet(data_row):
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
class Postprocessor_base(Manager_base):
    
    #
    def __init__(self, static_data_object, logger_object):
        Manager_base.__init__(self, static_data_object, logger_object)
        self.data_dict_list = {}
        self.filename = None
        self.sections_data_dict_list = {}
        self.sections_filename = None
        
    #
    def _append_data(self, idx, key, data_dict_list, value_list, query_name):
        nlp_data_key = self.json_structure_tools.pull_key('nlp_data_key')
        nlp_query_key = self.json_structure_tools.pull_key('nlp_query_key')
        nlp_section_key = self.json_structure_tools.pull_key('nlp_section_key')
        nlp_specimen_key = self.json_structure_tools.pull_key('nlp_specimen_key')
        nlp_value_key = self.json_structure_tools.pull_key('nlp_value_key')
        if len(value_list) > 0:
            data_dict_list[idx][nlp_data_key][0][key][query_name][nlp_value_key] \
                = value_list
            data_dict_list[idx][nlp_data_key][0][key][query_name][nlp_query_key] \
                = query_name
            data_dict_list[idx][nlp_data_key][0][key][query_name][nlp_section_key] \
                = key[0]
            if key[1]:
                data_dict_list[idx][nlp_data_key][0][key][query_name][nlp_specimen_key] \
                    = key[1]
        return data_dict_list
        
    #
    def _build_json_structure(self, data_dict_list, query_name):
        nlp_data_key = self.json_structure_tools.pull_key('nlp_data_key')
        nlp_datetime_key = self.json_structure_tools.pull_key('nlp_datetime_key')
        nlp_text_element_key = self.json_structure_tools.pull_key('nlp_text_element_key')
        nlp_tool_output_key = self.json_structure_tools.pull_key('nlp_tool_output_key')
        for i in range(len(data_dict_list)):
            data_dict_list[i][nlp_data_key] = {}
            for j in range(len(data_dict_list[i]['DOCUMENT_FRAME'])):
                key = data_dict_list[i]['DOCUMENT_FRAME'][j][0]
                datetime = data_dict_list[i]['DOCUMENT_FRAME'][j][1]
                text = data_dict_list[i]['DOCUMENT_FRAME'][j][2]
                if len(data_dict_list[i]['DOCUMENT_FRAME'][j]) > 3:
                    elements = data_dict_list[i]['DOCUMENT_FRAME'][j][3:]
                else:
                    elements = []
                if key not in data_dict_list[i][nlp_data_key].keys():
                    data_dict_list[i][nlp_data_key][key] = {}
                if query_name not in data_dict_list[i][nlp_data_key][key]:
                    data_dict_list[i][nlp_data_key][key][query_name] = {}
                if nlp_tool_output_key not in data_dict_list[i][nlp_data_key][key][query_name]:
                    data_dict_list[i][nlp_data_key][key][query_name][nlp_tool_output_key] = {}
                if nlp_datetime_key not in data_dict_list[i][nlp_data_key][key][query_name][nlp_tool_output_key].keys():
                    data_dict_list[i][nlp_data_key][key][query_name][nlp_tool_output_key][nlp_datetime_key] = []
                    data_dict_list[i][nlp_data_key][key][query_name][nlp_tool_output_key][nlp_text_element_key + str(0)] = []
                data_dict_list[i][nlp_data_key][key][query_name][nlp_tool_output_key][nlp_datetime_key].append(datetime)
                data_dict_list[i][nlp_data_key][key][query_name][nlp_tool_output_key][nlp_text_element_key + str(0)].append(text)
                for j in range(len(elements)):
                    if nlp_text_element_key+str(j+1) not in data_dict_list[i][nlp_data_key][key][query_name][nlp_tool_output_key].keys():
                        data_dict_list[i][nlp_data_key][key][query_name][nlp_tool_output_key][nlp_text_element_key+str(j+1)] = []
                    data_dict_list[i][nlp_data_key][key][query_name][nlp_tool_output_key][nlp_text_element_key+str(j+1)].append(elements[j])
        return data_dict_list
        
    #
    def _build_json_structures(self, argument_dict):
        data_dict_list = argument_dict['data_dict_list']
        query_name = argument_dict['query_name']
        data_dict_list_out = {}
        for idx in range(len(data_dict_list)):
            data_dict_list_out[idx] = \
                self._build_json_structure(data_dict_list[idx], query_name)
        return_dict = {}
        return_dict['data_dict_list'] = data_dict_list_out
        return_dict['query_name'] = argument_dict['query_name']
        return return_dict
    
    #
    def _extract_data_value(self, text_list):
        log_text = 'self._extract_data_value function not defined'
        self.logger_object.print_log(log_text)
    
    #
    def _extract_data_values(self, argument_dict):
        data_dict_list = argument_dict['data_dict_list']
        query_name = argument_dict['query_name']
        nlp_data_key = self.json_structure_tools.pull_key('nlp_data_key')
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
                            item[-2] = _trim_snippet(item)
                            value_list_tmp.append(item[2:])
                    value_list.append(value_list_tmp)
                value_list_dict[key] = value_list
            extracted_data_dict = self._extract_data_value(value_list_dict)
            for key in extracted_data_dict.keys():
                data_dict_list =\
                    self._append_data(i, key, data_dict_list,
                                      extracted_data_dict[key], query_name)
        for i in range(len(data_dict_list)):
            try:
                data_dict_list[i][nlp_data_key] = \
                    data_dict_list[i][nlp_data_key][0]
            except Exception:
                log_text = traceback.format_exc()
                self.logger_object.print_exc(log_text)
        return data_dict_list
    
    #
    def _extract_value(self, context_regex, regex, map_func, text):
        return _extract_value(context_regex, regex, map_func, text)
    
    #
    def _generate_data_table(self, value_list_dict):
        return _generate_data_table(value_list_dict)
    
    #
    def _generate_data_subtable(self, data_table, key):
        return _generate_data_subtable(data_table, key)
        
    #
    def _get_data_table_keys(self, data_table):
        return _get_data_table_keys(data_table)
    
    #
    def _include_full_section(self, argument_dict):
        data_dict_list = argument_dict['data_dict_list']
        for idx in range(len(data_dict_list)):
            for i in range(len(data_dict_list[idx])):
                document_id = data_dict_list[idx][i]['DOCUMENT_ID']
                for j in range(len(self.sections_data_dict)):
                    if self.sections_data_dict[j]['DOCUMENT_ID'] == document_id:
                        sections = self.sections_data_dict[j]['DOCUMENT_FRAME']
                for j in range(len(data_dict_list[idx][i]['DOCUMENT_FRAME'])):
                    offsets = data_dict_list[idx][i]['DOCUMENT_FRAME'][j][-1]
                    offsets.append('NONE')
                    data_dict_list[idx][i]['DOCUMENT_FRAME'][j] = \
                        data_dict_list[idx][i]['DOCUMENT_FRAME'][j][:-1]
                    data_dict_list[idx][i]['DOCUMENT_FRAME'][j].append('NONE')
                    data_dict_list[idx][i]['DOCUMENT_FRAME'][j].append(offsets)
                    section = data_dict_list[idx][i]['DOCUMENT_FRAME'][j][0]
                    for k in range(len(sections)):
                        if sections[k][0] == section:
                            data_dict_list[idx][i]['DOCUMENT_FRAME'][j][-2] = \
                                sections[k][-2]
                            data_dict_list[idx][i]['DOCUMENT_FRAME'][j][-1][-1] = \
                                sections[k][-1][0]
        return data_dict_list
    
    #
    def _include_snippets(self, argument_dict):
        data_dict_list = sequential_composition([self._include_full_section,
                                                 self._trim_sections],
                                                argument_dict)
        return data_dict_list
    
    #
    def _merge_data_dicts(self, argument_dict):
        data_dict_list = argument_dict['data_dict_list']
        nlp_data_key = self.json_structure_tools.pull_key('nlp_data_key')
        doc_ids = []
        for idx in range(len(data_dict_list)):
            for i in range(len(data_dict_list[idx])):
                doc_ids.append(data_dict_list[idx][i]['DOCUMENT_ID'])
        doc_ids = sorted(list(set(doc_ids)))
        document_frame_dict = {}
        nlp_data_dict = {}
        for doc_id in doc_ids:
            document_frame = {}
            nlp_data = {}
            for idx in range(len(data_dict_list)):
                document_frame[idx] = None
                nlp_data[idx] = None
                for i in range(len(data_dict_list[idx])):
                    if data_dict_list[idx][i]['DOCUMENT_ID'] == doc_id:
                        document_frame[idx] = data_dict_list[idx][i]['DOCUMENT_FRAME']
                        nlp_data[idx] = data_dict_list[idx][i][nlp_data_key]
                        break
                if document_frame[idx] is None:
                    document_frame[idx] = []
                if nlp_data[idx] is None:
                    nlp_data[idx] = []
            document_frame_dict[doc_id] = document_frame
            nlp_data_dict[doc_id] = nlp_data
        return_dict = {}
        return_dict['document_frame_dict'] = document_frame_dict
        return_dict['nlp_data_dict'] = nlp_data_dict
        return_dict['query_name'] = argument_dict['query_name']
        return return_dict
    
    #
    def _package_merged_dicts(self, argument_dict):
        document_frame_dict = argument_dict['document_frame_dict']
        nlp_data_dict = argument_dict['nlp_data_dict']
        nlp_data_key = self.json_structure_tools.pull_key('nlp_data_key')
        num_components = len(self.data_dict_list)
        data_dict_list = []
        for doc_id in document_frame_dict.keys():  
            document_frame = document_frame_dict[doc_id]
            nlp_data = nlp_data_dict[doc_id]
            data_dict = {}
            data_dict['DOCUMENT_ID'] = doc_id
            data_dict['DOCUMENT_FRAME'] = []
            data_dict[nlp_data_key] = []
            for idx in range(num_components):
                data_dict['DOCUMENT_FRAME'].append(document_frame[idx])
                data_dict[nlp_data_key].append(nlp_data[idx])
            data_dict_list.append(data_dict)
        return_dict = {}
        return_dict['data_dict_list'] = data_dict_list
        return_dict['query_name'] = argument_dict['query_name']
        return return_dict
    
    #
    def _trim_sections(self, data_dict_list):
        snippet_size = 250
        for idx in range(len(data_dict_list)):
            for i in range(len(data_dict_list[idx])):
                for j in range(len(data_dict_list[idx][i]['DOCUMENT_FRAME'])):
                    i2e_extract = \
                        data_dict_list[idx][i]['DOCUMENT_FRAME'][j][2]
                    section = \
                        data_dict_list[idx][i]['DOCUMENT_FRAME'][j][-2]
                    i2e_extract_offsets = \
                        data_dict_list[idx][i]['DOCUMENT_FRAME'][j][-1][0]
                    section_offsets = \
                        data_dict_list[idx][i]['DOCUMENT_FRAME'][j][-1][-1]
                    m_idxs = \
                        [m.start() for m in re.finditer(re.escape(i2e_extract), section)]
                    if len(m_idxs) == 1:
                        m_idx = m_idxs[0]
                        neighborhood = (snippet_size - len(i2e_extract)) // 2
                        if neighborhood <= m_idx:
                            start = m_idx - neighborhood
                            remainder = 0
                        else:
                            start = 0
                            remainder = neighborhood - m_idx
                        if m_idx + len(i2e_extract) + neighborhood + remainder <= len(section):
                            stop = m_idx + len(i2e_extract) + neighborhood + remainder
                        else:
                            stop = len(section)
                        snippet = section[start:stop]
        return data_dict_list
    
    #
    def pull_data_dict_base_keys_list(self):
        return [ 'DOCUMENT_ID', 'DOCUMENT_FRAME' ]
    
    #
    def pull_data_dict_list(self):
        return self.merged_data_dict_list     
    
    #
    def push_data_dict(self, postprocessor_name, filename, data_dict,
                       sections_data_dict, document_list):
        data_dict_list = _build_data_dictionary(data_dict, document_list)
        sections_data_dict_list = _build_data_dictionary(sections_data_dict,
                                                         document_list)
        postprocessor_name = re.sub('postprocessor_', '', postprocessor_name)
        if postprocessor_name == filename:
            self.data_dict_list[0] = data_dict_list
            self.sections_data_dict = sections_data_dict_list
            self.filename = filename
        
    #
    def push_diagnosis_reader(self, diagnosis_reader):
        self.diagnosis_reader = diagnosis_reader
    
    #
    def run_object(self, query_name=None, section_name=None):
        argument_dict = {}
        argument_dict['data_dict_list'] = self.data_dict_list
        argument_dict['filename'] = self.filename
        argument_dict['query_name'] = query_name
        return_dict = parallel_composition([_get_query_name,
                                            self._include_snippets],
                                           argument_dict)
        argument_dict = {}
        argument_dict['data_dict_list'] = \
            return_dict[self._include_snippets.__name__]
        argument_dict['query_name'] = return_dict[_get_query_name.__name__]
        self.merged_data_dict_list = sequential_composition([self._build_json_structures,
                                                             self._merge_data_dicts,
                                                             self._package_merged_dicts,
                                                             self._extract_data_values],
                                                            argument_dict)