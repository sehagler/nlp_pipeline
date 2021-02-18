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
        self.data = {}
        self.project_data = project_data
        self.xml_reader = Xml_reader(project_data, password)
        self.xlsx_reader = Xlsx_reader(project_data, password)
                
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
    
    #
    def _partition_data_by_thread(self, data):
        num_processes = self.project_data['num_processes']
        try:
            multiprocessing_flg = self.project_data['flags']['multiprocessing']
        except:
            multiprocessing_flg = False
        partitioned_data = {}
        if multiprocessing_flg:
            for i in range(num_processes):
                partitioned_data[i] = []
            for i in range(len(data)):
                for j in range(num_processes):
                    data_tmp = {}
                    data_tmp['NLP_DOCUMENT_IDX'] = []
                    for key in data[i].keys():
                        data_tmp[key] = []
                    partitioned_data[j].append(data_tmp)
            doc_idx = 0
            for i in range(len(data)):
                keys = list(data[i].keys())
                num_entries = len(data[i][keys[0]])
                for j in range(num_entries):
                    idx = j % num_processes
                    partitioned_data[idx][i]['NLP_DOCUMENT_IDX'].append(doc_idx)
                    for key in data[i].keys():
                        partitioned_data[idx][i][key].append(data[i][key][j])
                    doc_idx += 1
        else:
            partitioned_data[0] = data
        return partitioned_data
    
    #
    def get_data_by_document_number(self, document_number):
        document_data = {}
        document_found = False
        for i in range(len(self.data)):
            if not bool(document_data):
                data = self.data[i]
                keys = list(data.keys())
                num_documents = len(data[keys[0]])
                if document_number+1 > num_documents:
                    document_number -= num_documents
                else:
                    for key in keys:
                        document_data[key] = [ data[key][document_number] ]
        return document_data
    
    #
    def get_data_by_document_value(self, data_file,
                                   document_value_key, document_value):
        document_data = \
            self._get_data_by_document_value(data_file, document_value, 
                                             document_value_key)
        return document_data
      
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
    
    #
    def read_data(self, raw_data_files_dict, raw_data_files):
        data = []
        for i in range(len(raw_data_files)):
            filename, file_extension = os.path.splitext(raw_data_files[i])
            if file_extension.lower() in [ '.xls', '.xlsx' ]:
                data_tmp = self.xlsx_reader.read_files(raw_data_files_dict, 
                                                       raw_data_files[i])
                data.append(data_tmp)
            elif file_extension.lower() in [ '.xml' ]:
                data_tmp = self.xml_reader.read_files(raw_data_files_dict, 
                                                      raw_data_files[i])
                data.append(data_tmp)
            else:
                print('invalid file extension: ' + file_extension)
        partitioned_data = self._partition_data_by_thread(data)
        self.data = partitioned_data
        
    #
    def select_process(self, process_idx):
        self.data = self.data[process_idx]