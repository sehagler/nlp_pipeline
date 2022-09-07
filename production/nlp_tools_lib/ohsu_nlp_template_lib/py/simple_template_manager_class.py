# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 12:10:43 2022

@author: haglers
"""

#
import csv
import datetime
import itertools
import os
import re

#
class Simple_template_manager(object):
    
    #
    def __init__(self):
        self.template_output = []
    
    #
    def _apply_template(self, primary_template_list, secondary_template_list,
                        template_sections_list, text_dict):
        for document_id in text_dict.keys():
            template_output_list = []
            for key in text_dict[document_id].keys():
                offset_base = text_dict[document_id][key]['OFFSET_BASE']
                section = text_dict[document_id][key]['TEXT']
                now = datetime.datetime.now()
                timestamp = now.strftime("%m/%d/%Y %H:%M:%S")
                if primary_template_list is not None:
                    create_output_flg = True
                    if template_sections_list is not None:
                        create_output_flg = False
                        for section_name in template_sections_list:
                            if section_name in key[0]:
                                create_output_flg = True
                else:
                    create_output_flg = False
                if create_output_flg:
                    section = self._remove_newlines(section)
                    for primary_template in primary_template_list:
                        if re.search(primary_template, section) is not None:
                            primary_matches = re.finditer(primary_template, section)
                            if bool(primary_matches):
                                for primary_match in primary_matches:
                                    primary_query_output = primary_match.group(0)
                                    start = primary_match.start() + offset_base
                                    end = primary_match.end() + offset_base - 1
                                    offset = [ (start, end) ]
                                    snippet = section
                                    if primary_query_output is not None:
                                        secondary_query_outputs = {}
                                        for i in range(len(secondary_template_list)):
                                            secondary_query_outputs[i] = []
                                            for j in range(len(secondary_template_list[i])):
                                                secondary_template = \
                                                    secondary_template_list[i][j]
                                                secondary_template = \
                                                    re.compile(secondary_template)
                                                secondary_matches = \
                                                    secondary_template.finditer(primary_query_output)
                                                if bool(secondary_matches):
                                                    for secondary_match in secondary_matches:
                                                        secondary_query_outputs[i].append(secondary_match.group(0))
                                        for i in range(len(secondary_query_outputs)):
                                            if len(secondary_query_outputs[i]) == 0:
                                                secondary_query_outputs[i].append('')
                                        secondary_values_list_tmp = []
                                        for i in range(len(secondary_query_outputs)):
                                            secondary_values_list_tmp.append(secondary_query_outputs[i])
                                        secondary_values_list = \
                                            list(itertools.product(*secondary_values_list_tmp))
                                        for secondary_values in secondary_values_list:
                                            template_output = \
                                                [ document_id, timestamp, key[0], key[1],
                                                  primary_query_output ]
                                            for i in range(len(secondary_values)):
                                                template_output.append(secondary_values[i])
                                            template_output.append(snippet)
                                            template_output.append(offset)
                                            template_output_list.append(template_output)
                                            
                                    else:
                                        template_output = \
                                            [ document_id, timestamp, key[0], key[1],
                                              primary_query_output, snippet, offset ]
                                        template_output_list.append(template_output)
                else:
                    if template_sections_list is not None:
                        create_output_flg = False
                        for section_name in template_sections_list:
                            if section_name in key[0]:
                                create_output_flg = True
                    if create_output_flg:
                        query_output = section
                        snippet = section
                        offset = []
                        template_output = \
                            [ document_id, timestamp, key[0], key[1],
                              query_output, snippet, offset ]
                        template_output_list.append(template_output)
            template_output_list = \
                self._unique_elements(template_output_list)
            template_output_list = \
                self._unique_linguamatics_specimens(template_output_list)
            template_output_list = \
                self._maximal_elements(template_output_list)
            for template_output in template_output_list:
                self.template_output.append(template_output)
                                
    #
    def _maximal_elements(self, data_list_in):
        data_list_tmp = data_list_in.copy()
        data_list_out = []
        while len(data_list_tmp) > 0:
            item = data_list_tmp[0]
            del data_list_tmp[0]
            idxs = []
            append_item_flg = True
            for i in range(len(data_list_tmp)):
                if len(item[-1]) > 0 and len(data_list_tmp[i][-1]) > 0:
                    if item[-1][0][0] <= data_list_tmp[i][-1][0][0] and \
                       item[-1][0][1] >= data_list_tmp[i][-1][0][1]:
                        idxs.append(i)
                    if data_list_tmp[i][-1][0][0] <= item[-1][0][0] and \
                       data_list_tmp[i][-1][0][1] >= item[-1][0][1]:
                        append_item_flg = False
                        data_list_out.append(data_list_tmp[i])
                        idxs.append(i)
            if append_item_flg:
                data_list_out.append(item)
            idxs = list(set(idxs))
            idxs.sort(reverse=True)
            for idx in idxs:
                del data_list_tmp[idx]
        return data_list_out
    
    #
    def _remove_newlines(self, text):
        text = re.sub('\n', ' ', text)
        text = re.sub(' +', ' ', text)
        return text
                
    #
    def _unique_elements(self, data_list_in):
        data_list_tmp = data_list_in.copy()
        data_list_out = []
        while len(data_list_tmp) > 0:
            item = data_list_tmp[0]
            del data_list_tmp[0]
            data_list_out.append(item)
            idxs = []
            for i in range(len(data_list_tmp)):
                match_flg = True
                for j in range(len(item)):
                    if item[j] != data_list_tmp[i][j]:
                        match_flg = False
                if match_flg:
                    idxs.append(i)
            idxs.sort(reverse=True)
            for idx in idxs:
                del data_list_tmp[idx]
        return data_list_out
    
        
    #
    def _unique_linguamatics_specimens(self, data_list_in):
        data_list_tmp = data_list_in.copy()
        data_list_out = []
        while len(data_list_tmp) > 0:
            item = data_list_tmp[0]
            del data_list_tmp[0]
            idxs = []
            append_item_flg = True
            for i in range(len(data_list_tmp)):
                match_flg = True
                for j in range(len(item)):
                    if j != 3 and j != len(item)-2 and item[j] != data_list_tmp[i][j]:
                        match_flg = False
                if match_flg:
                    if item[3] == '' and data_list_tmp[i][3] != '':
                        append_item_flg = False
                        data_list_out.append(data_list_tmp[i])
                        idxs.append(i)
                    elif item[3] != '' and data_list_tmp[i][3] == '':
                        idxs.append(i)
            if append_item_flg:
                data_list_out.append(item)
            idxs.sort(reverse=True)
            for idx in idxs:
                del data_list_tmp[idx]
        return data_list_out
    
    #
    def clear_template_output(self):
        self.template_output = []
        
    #
    def run_template(self, template_manager, text_dict):
        template_dict = template_manager.simple_template()
        primary_template_list = template_dict['primary_template_list']
        if 'secondary_template_list' in template_dict.keys():
            secondary_template_list = template_dict['secondary_template_list']
        else:
            secondary_template_list = []
        template_sections_list = template_dict['sections_list']
        self._apply_template(primary_template_list, secondary_template_list,
                             template_sections_list, text_dict)
        
    #
    def write_template_output(self, template_manager, data_dir, filename):
        template_dict = template_manager.simple_template()
        template_headers = template_dict['template_headers']
        header = [ 'DOCUMENT_ID', 'DATETIME', 'Section Title', 'Specimen Id' ]
        for i in range(len(template_headers)):
            header.append(template_headers[i])
        header.append('Snippet')
        header.append('Coords')
        with open(os.path.join(data_dir, filename), 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(self.template_output)