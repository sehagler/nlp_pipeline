# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 12:06:14 2020

@author: haglers
"""

#
import os

#
from nlp_lib.py.reader_lib.readers_lib.xml_reader_class import Xml_reader
from nlp_lib.py.reader_lib.readers_lib.xlsx_reader_class import Xlsx_reader

#
class Raw_data_reader(object):
    
    #
    def __init__(self, project_data, password):
        self.data = []
        self.project_data = project_data
        self.xml_reader = Xml_reader(project_data, password)
        self.xlsx_reader = Xlsx_reader()
                
    #
    def _get_data_by_document_value(self, data_file, document_value,
                                    document_value_key=None):
        document_data = {}
        data = self.data[data_file]
        nlp_mode = data['NLP_MODE'][0]
        if nlp_mode == 'RESULT_ID':
            document_value_key = None
        idxs = [i for i, x in enumerate(data[nlp_mode]) if x == document_value]
        if len(idxs) > 0:
            if document_value_key is not None:
                idxs0 = [i for i, x in enumerate(data['MRN']) if x == document_value_key]
                idxs = list(set(idxs) & set(idxs0))
            for key in data.keys():
                document_data[key] = [data[key][i] for i in idxs]
        return document_data
    
    '''
    #
    def _get_document_values(self, label0, label1):
        document_value_dict = {}
        for i in range(len(self.data)):
            document_value_dict[i] = {}
            data_label0 = self.data[i][label0]
            data_label1 = self.data[i][label1]
            items = sorted(set(data_label0))
            for item in items:
                document_value_list = []
                idxs = [j for j, x in enumerate(data_label0) if x == item ]
                document_value_list.append([data_label1[j] for j in idxs])
                document_value_dict[i][item] = sorted(list(set(document_value_list[0])))
        return document_value_dict
    '''
    
    #
    def get_data_by_document_number(self, document_number):
        document_data = {}
        document_found = False
        for i in range(len(self.data)):
            if not document_found:
                data = self.data[i]
                keys = list(data.keys())
                if len(data[keys[0]])-1 >= document_number:
                    document_found = True
                    for key in keys:
                        document_data[key] = [ data[key][document_number] ]
                else:
                    document_number -= len(data[keys[0]])-1
        return document_data
    
    #
    def get_data_by_document_value(self, data_file, document_value_key, document_value):
        document_data = \
            self._get_data_by_document_value(data_file, document_value,
                                             document_value_key)
        return document_data
        
    '''
    #
    def get_data_by_document_value_case_number(self, data_file, document_value_key, document_value):
        document_data = \
            self._get_data_by_document_value('CASE_NUMBER', data_file, document_value, document_value_key)
        return document_data
    
    #
    def get_data_by_document_value_result_id(self, data_file, document_value):
        document_data = self._get_data_by_document_value('RESULT_ID', data_file, document_value)
        return document_data
    '''
      
    #
    def get_document_numbers(self):
        doc_num = 0
        for data in self.data:
            keys = list(data.keys())
            doc_num += len(data[keys[0]])
        document_numbers = list(range(doc_num))
        return document_numbers
    
    #
    def get_document_values(self):
        document_value_dict = {}
        for i in range(len(self.data)):
            document_value_dict[i] = {}
            label1 = self.data[i]['NLP_MODE'][0]
            if label1 == 'CASE_NUMBER':
                label0 = 'MRN'
            elif label1 == 'RESULT_ID':
                label0 = 'RESULT_ID'
            data_label0 = self.data[i][label0]
            data_label1 = self.data[i][label1]
            items = sorted(set(data_label0))
            for item in items:
                document_value_list = []
                idxs = [j for j, x in enumerate(data_label0) if x == item ]
                document_value_list.append([data_label1[j] for j in idxs])
                document_value_dict[i][item] = sorted(list(set(document_value_list[0])))
        return document_value_dict
    
    '''
    #
    def get_document_values_case_number(self):
        document_value_dict = self._get_document_values('MRN', 'CASE_NUMBER')
        return document_value_dict
    
    #
    def get_document_values_result_id(self):
        document_value_dict = self._get_document_values('RESULT_ID', 'RESULT_ID')
        return document_value_dict
    '''
    
    #
    def read_data(self, raw_data_files_dict, raw_data_files):
        for i in range(len(raw_data_files)):
            filename, file_extension = os.path.splitext(raw_data_files[i])
            if file_extension.lower() in [ '.xls', '.xlsx' ]:
                data_tmp = self.xlsx_reader.read_files(raw_data_files_dict, raw_data_files[i],
                                                       self.project_data['datetime_keys'],
                                                       self.project_data['header_key'], 
                                                       self.project_data['header_values'])
                self.data.append(data_tmp)
            elif file_extension.lower() in [ '.xml' ]:
                data_tmp = self.xml_reader.read_files(raw_data_files_dict, 
                                                      raw_data_files[i])
                self.data.append(data_tmp)
            else:
                print('invalid file extension: ' + file_extension)