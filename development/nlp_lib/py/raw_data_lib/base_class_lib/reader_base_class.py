# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 09:32:11 2020

@author: haglers
"""

#
import datetime
import re
import xlrd

#
from tool_lib.py.processing_tools_lib.text_processing_tools \
    import make_ascii

#
class Reader_base(object):
    
    #
    def __init__(self, static_data, server_manager, password):
        self.static_data = static_data
        self.server_manager = server_manager
        
    #
    def _read_datetime(self, book, value):
        try:
            y, m, d, h, mi, s = \
                xlrd.xldate_as_tuple(value, book.datemode)
            datetime_str = str(m) + '/' + str(d) + '/' + str(y)
        except:
            datetime_str = ''
        return datetime_str
    
    #
    def _trim_data_by_document_identifier(self, data):
        document_identifiers = self.static_data['document_identifiers']
        data_csn_list = []
        for document_identifier in document_identifiers:
            if document_identifier in data.keys():
                data_csn_list.extend(data[document_identifier])
        if 'document_list' in self.static_data.keys():
            document_list = self.static_data['document_list']
        else:
            document_list = list(set(data_csn_list))
        csn_list = []
        delete_idx_list = []
        for i in range(len(data_csn_list)):
            if (data_csn_list[i] in document_list and
                data_csn_list[i] not in csn_list):
                csn_list.append(data_csn_list[i])
            else:
                delete_idx_list.append(i)
        for key in data.keys():
            for i in sorted(delete_idx_list, reverse=True):
                del data[key][i]
        return data
    
    #
    def _trim_data_by_document_list(self, data):
        document_identifiers = self.static_data['document_identifiers']
        data_csn_list = []
        for document_identifier in document_identifiers:
            if document_identifier in data.keys():
                data_csn_list.extend(data[document_identifier])
        if 'document_list' in self.static_data.keys():
            document_list = self.static_data['document_list']
        else:
            document_list = list(set(data_csn_list))
        csn_list = []
        delete_idx_list = []
        for i in range(len(data_csn_list)):
            if (data_csn_list[i] in document_list and
                data_csn_list[i] not in csn_list):
                csn_list.append(data_csn_list[i])
            else:
                delete_idx_list.append(i)
        for key in data.keys():
            for i in sorted(delete_idx_list, reverse=True):
                del data[key][i]
        return data
    
    #
    def _trim_data_by_patient_list(self, data):
        patient_list = self.static_data['patient_list']
        delete_idxs = []
        for key in self.static_data['patient_identifiers']:
            if key in data.keys():
                patient_identifiers = data[key]
                for i in range(len(patient_identifiers)):
                    if patient_identifiers[i] not in patient_list:
                        delete_idxs.append(i)
        delete_idxs.sort(reverse=True)
        for i in range(len(delete_idxs)):
            idx = delete_idxs[i]
            for key in data.keys():
                del data[key][idx]
        return data
    
    #
    def read_files(self, raw_data_files_dict, raw_data_file):
        data = self._read_data_file(raw_data_files_dict, raw_data_file)
        if 'document_list' in self.static_data:
            data = self._trim_data_by_document_list(data)
        if 'patient_list' in self.static_data:
            data = self._trim_data_by_patient_list(data)
        return data