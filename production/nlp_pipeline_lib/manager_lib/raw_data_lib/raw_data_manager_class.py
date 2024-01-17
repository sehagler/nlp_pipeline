# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 12:06:14 2020

@author: haglers
"""

#
import os
import sys

#
from base_lib.manager_base_class import Manager_base
from tools_lib.processing_tools_lib.text_processing_tools \
    import remove_repeated_substrings
from tools_lib.processing_tools_lib.variable_processing_tools \
    import delete_key
    
#
def _get_nlp_metadata(password, i2e_version, num_processes, process_idx):
    python_version = \
        str(sys.version_info[0]) + '.' + \
        str(sys.version_info[1]) + '.' + \
        str(sys.version_info[2])
    nlp_metadata = {}
    nlp_metadata['I2E_VERSION'] = i2e_version
    nlp_metadata['PYTHON_VERSION'] = python_version
    nlp_metadata['NUMBER_OF_PREPROCESSING_PROCESSORS'] = str(num_processes)
    nlp_metadata['PREPROCESSING_PROCESSOR_IDX'] = str(process_idx)
    return nlp_metadata

#
def _partition_data_by_thread(data, multiprocessing_flg, num_processes,
                              doc_idx_offset):
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
        doc_idx = doc_idx_offset
        for i in range(len(data)):
            keys = list(data[i].keys())
            num_entries = len(data[i][keys[0]])
            for j in range(num_entries):
                idx = j % num_processes
                partitioned_data[idx][i]['NLP_DOCUMENT_IDX'].append(str(doc_idx))
                for key in data[i].keys():
                    partitioned_data[idx][i][key].append(data[i][key][j])
                doc_idx += 1
    else:
        partitioned_data[0] = data
    return partitioned_data, doc_idx

#
def _read_data(data_tmp, password, i2e_version, num_processes, process_idx):
    if 'RAW_TEXT' in data_tmp.keys() and \
       data_tmp['RAW_TEXT'][0] is not None:
        raw_text = data_tmp['RAW_TEXT']
        raw_text = ''.join(raw_text)
        text = remove_repeated_substrings(raw_text)
    else:
        text = None
    source_metadata = {}
    for key in data_tmp.keys():
        source_metadata[key] = data_tmp[key][0]
    source_metadata = _prune_metadata(source_metadata)
    nlp_metadata = {}
    nlp_metadata = _get_nlp_metadata(password, i2e_version, num_processes,
                                     process_idx)
    nlp_metadata['FILENAME'] = source_metadata['FILENAME']
    del source_metadata['FILENAME']
    nlp_metadata['NLP_DOCUMENT_IDX'] = \
        str(source_metadata['NLP_DOCUMENT_IDX'])
    del source_metadata['NLP_DOCUMENT_IDX']
    nlp_metadata['NLP_MODE'] = source_metadata['NLP_MODE']
    del source_metadata['NLP_MODE']
    if 'NOTE_TYPE' in source_metadata.keys():
        nlp_metadata['NOTE_TYPE'] = \
            source_metadata['NOTE_TYPE']
        xml_metadata_keys = [ 'NOTE_TYPE']
    else:
        xml_metadata_keys = []
    return [source_metadata], [nlp_metadata], [text], xml_metadata_keys

#
def _read_data_wrapper(password, data_tmp, i2e_version, num_processes,
                       process_idx):
    if 'SOURCE_SYSTEM' in data_tmp.keys():
        source_system = data_tmp['SOURCE_SYSTEM'][0]
    else:
        source_system = 'UNKNOWN'
        
    source_metadata_list, nlp_metadata_list, text_list, \
    xml_metadata_keys = \
            _read_data(data_tmp, password, i2e_version, num_processes,
                       process_idx)     
    return source_metadata_list, nlp_metadata_list, text_list, \
           xml_metadata_keys, source_system
    
#
def _prune_metadata(metadata):
    delete_key(metadata, 'RAW_TEXT')
    delete_key(metadata, 'REPORT_GROUP')
    delete_key(metadata, 'REPORT_HEADER')
    delete_key(metadata, 'REPORT_LINE')
    return metadata

#
class Raw_data_manager(Manager_base):
    
    #
    def __init__(self, static_data_object, logger_object,
                 multiprocessing_flg, password):
        Manager_base.__init__(self, static_data_object, logger_object)
        static_data = self.static_data_object.get_static_data()
        self.multiprocessing_flg = multiprocessing_flg
        self.clear_raw_data()
        if self.multiprocessing_flg:
            self.num_processes = static_data['num_processes']
        else:
            self.num_processes = 1
                       
    #
    def append_raw_data(self, raw_data):
        self.raw_data.append(raw_data)
        
    #
    def clear_raw_data(self):
        self.raw_data = []
    
    #
    def get_data_by_document_number(self, data_file, document_number,
                                    i2e_version, process_idx, password):
        document_data = {}
        for i in range(len(self.data)):
            if len(self.data[i]['FILENAME']) > 0 and self.data[i]['FILENAME'][0] == data_file:
                data = self.data[i]
                keys = list(data.keys())
                if document_number in data[keys[0]]:
                    doc_idx = data[keys[0]].index(document_number)
                    for key in keys:
                        document_data[key] = [ data[key][doc_idx] ]
        if self.multiprocessing_flg:
            document_idx = int(document_data['NLP_DOCUMENT_IDX'][0])
        else:
            document_idx = document_ctr
            document_data['NLP_DOCUMENT_IDX'] = []
            document_data['NLP_DOCUMENT_IDX'].append(document_idx)
        filename, extension = os.path.splitext(data_file)
            
        #
        source_metadata_list, nlp_metadata_list, text_list, \
            xml_metadata_keys, source_system = \
                _read_data_wrapper(password, document_data, i2e_version,
                                   self.num_processes, process_idx)
        #
        
        xml_metadata_list = []
        for i in range(len(text_list)):
            source_metadata = source_metadata_list[i]
            nlp_metadata = nlp_metadata_list[i]
            xml_metadata = {}
            xml_metadata['DOCUMENT_ID'] = str(document_idx)
            xml_metadata['SOURCE_SYSTEM'] = \
                source_metadata['SOURCE_SYSTEM']
            for key in xml_metadata_keys:
                xml_metadata[key] = nlp_metadata[key]
            xml_metadata_list.append(xml_metadata)
        return document_data, document_idx, source_metadata_list, \
               nlp_metadata_list, text_list, xml_metadata_list, source_system
      
    #
    def get_document_numbers(self, data_file):
        document_numbers = []
        for i in range(len(self.data)):
            data = self.data[i]
            if len(data['FILENAME']) > 0 and data['FILENAME'][0] == data_file:
                keys = list(data.keys())
                document_numbers.extend(data[keys[0]])
        return document_numbers
    
    #
    def get_multiprocessing_flg(self):
        return self.multiprocessing_flg
    
    #
    def get_number_of_processes(self):
        return self.num_processes
    
    #
    def partition_data(self, doc_idx_offset):
        self.partitioned_data, doc_idx_offset = \
            _partition_data_by_thread(self.raw_data, self.multiprocessing_flg,
                                      self.num_processes, doc_idx_offset)
        return doc_idx_offset
    
    #
    def print_num_of_docs_in_preprocessing_set(self):
        num_docs = 0
        for key in self.partitioned_data.keys():
            for data in self.partitioned_data[key]:
                keys = list(data.keys())
                num_docs += len(data[keys[0]])
        log_text = 'Number of documents in preprocessing set: ' + str(num_docs)
        self.logger_object.print_log(log_text)
        
    #
    def select_process(self, process_idx):
        self.data = self.partitioned_data[process_idx]