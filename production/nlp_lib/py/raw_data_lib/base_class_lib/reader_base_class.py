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
    def __init__(self, project_data, server_manager, password):
        self.project_data = project_data
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
    
    '''
    #
    def _trim_data_by_patient_identifier(self, data):
        if 'patient_list' in self.project_data:
            patient_list = self.project_data['patient_list']
        else:
            patient_list = None
        patient_identifier = None
        for key in self.project_data['patient_identifiers']:
            try:
                patient_identifier = list(set(data[key]))
            except:
                pass
        if len(patient_identifier) < 2:
            if patient_identifier_list is not None:
                if patient_identifier[0] in patient_identifier_list:
                    do_analysis_flg = True
                else:
                    do_analysis_flg = False
            else:
                do_analysis_flg = True
        #print(patient_identifier)
        return data
    '''
    
    #
    def _trim_data_by_csn(self, data):
        document_identifiers = self.project_data['document_identifiers']
        data_csn_list = []
        for document_identifier in document_identifiers:
            if document_identifier in data.keys():
                data_csn_list.extend(data[document_identifier])
        if 'document_list' in self.project_data.keys():
            document_list = self.project_data['document_list']
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
    def _trim_data_by_csn(self, data):
        document_identifiers = self.project_data['document_identifiers']
        data_csn_list = []
        for document_identifier in document_identifiers:
            if document_identifier in data.keys():
                data_csn_list.extend(data[document_identifier])
        if 'document_list' in self.project_data.keys():
            document_list = self.project_data['document_list']
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
    def read_files(self, raw_data_files_dict, raw_data_file):
        data = self._read_data_file(raw_data_files_dict, raw_data_file)
        if self.project_data['flags']['trim_data_by_csn']:
            data = self._trim_data_by_csn(data)
        #data = self._trim_data_by_patient_identifier(data)
        return data