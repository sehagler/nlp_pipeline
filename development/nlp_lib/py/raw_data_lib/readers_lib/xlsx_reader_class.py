# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 14:00:44 2018

@author: haglers
"""

# import packages
import os
import re

#
from nlp_lib.py.raw_data_lib.base_class_lib.reader_base_class import Reader_base
from tool_lib.py.processing_tools_lib.file_processing_tools import read_xlsx_file

#
class Xlsx_reader(Reader_base):
    
    #
    def _read_data_file(self, raw_data_files_dict, raw_data_file):
        datetime_keys = self.project_data['datetime_keys']
        header_key = self.project_data['header_key']
        header_value_list = self.project_data['header_values']
        if header_key != []:
            data = \
                self._read_data_file_key(raw_data_files_dict, raw_data_file,
                                         datetime_keys, header_key,
                                         header_value_list)
        else:
            data = \
                self._read_data_file_nokey(raw_data_files_dict, raw_data_file,
                                           datetime_keys)
        return data
    
    #
    def _read_data_file_key(self, raw_data_files_dict, raw_data_file, dt_labels, key_label, key_value_list):
        data = {}
        book = read_xlsx_file(raw_data_file)
        sheet = book.sheet_by_index(0)
        keys = sheet.row(0)
        for i in range(len(keys)):
            keys[i] = str(keys[i].value)
        if 'FILENAME' not in data.keys():
            data['FILENAME'] = []
        if 'NLP_MODE' not in data.keys():
            data['NLP_MODE'] = []
        for key in keys:
            if key not in data.keys():
                data[key] = []
        for row_idx in range(1, sheet.nrows):
            row = sheet.row(row_idx)
            idx = [ i for i, x in enumerate(keys) if x == key_label]
            REPORT_KEY_tmp = re.sub(':', '', row[idx[0]].value)
            if REPORT_KEY_tmp.lower() in map(str.lower, key_value_list):
                data['FILENAME'].append(os.path.basename(raw_data_file))
                data['NLP_MODE'].append(raw_data_files_dict[os.path.basename(raw_data_file)]['NLP_MODE'])
                for i in range(len(keys)):
                    if keys[i] in dt_labels:
                        data[keys[i]].append(self._read_datetime(book, row[i].value))
                    else:
                        data[keys[i]].append(row[i].value)
        if 'RAW_TEXT' not in data.keys():
            data['RAW_TEXT'] = data[keys[-1]]
        else:
            data['RAW_TEXT'].extend(data[keys[-1]])
        del data[keys[-1]]
        return data
    
    #
    def _read_data_file_nokey(self, raw_data_files_dict, raw_data_file, dt_labels):
        data = {}
        book = read_xlsx_file(raw_data_file)
        sheet = book.sheet_by_index(0)
        keys = sheet.row(0)
        for i in range(len(keys)):
            keys[i] = str(keys[i].value)
        if 'FILENAME' not in data.keys():
            data['FILENAME'] = []
        if 'NLP_MODE' not in data.keys():
            data['NLP_MODE'] = []
        for key in keys:
            if key not in data.keys():
                data[key] = []
        for row_idx in range(1, sheet.nrows):
            row = sheet.row(row_idx)
            data['FILENAME'].append(os.path.basename(raw_data_file))
            data['NLP_MODE'].append(raw_data_files_dict[os.path.basename(raw_data_file)]['NLP_MODE'])
            for i in range(len(keys)):
                if keys[i] in dt_labels:
                    data[keys[i]].append(self._read_datetime(book, row[i].value))
                else:
                    data[keys[i]].append(row[i].value)
        if 'RAW_TEXT' not in data.keys():
            data['RAW_TEXT'] = data[keys[-1]]
        else:
            data['RAW_TEXT'].extend(data[keys[-1]])
        del data[keys[-1]]
        return data