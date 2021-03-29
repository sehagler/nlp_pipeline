# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 12:06:14 2020

@author: haglers
"""

#
import datetime
import os
import requests
import sys

#
from nlp_lib.py.reader_lib.readers_lib.xml_reader_class import Xml_reader
from nlp_lib.py.reader_lib.readers_lib.xlsx_reader_class import Xlsx_reader
from nlp_lib.py.tool_lib.processing_tools_lib.text_processing_tools \
    import remove_repeated_substrings
from nlp_lib.py.tool_lib.processing_tools_lib.variable_processing_tools \
    import delete_key

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
                    partitioned_data[idx][i]['NLP_DOCUMENT_IDX'].append(str(doc_idx))
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
        
#
def _get_nlp_metadata(server, user, password):
    auth_values = (user, password)
    with requests.get(server + '/api', auth=auth_values, verify=False) as r:
        try:
            i2e_version = r.headers['X-Version']
        except:
            i2e_version = 'FAILED_TO_CONNECT'
    python_version = \
        str(sys.version_info[0]) + '.' + \
        str(sys.version_info[1]) + '.' + \
        str(sys.version_info[2])
    now = datetime.datetime.now()
    now_str = now.strftime("%d-%b-%y %H:%M:%S")
    nlp_metadata = {}
    nlp_metadata['I2E_VERSION'] = i2e_version
    nlp_metadata['PYTHON_VERSION'] = python_version
    nlp_metadata['PREPROCESSING_DATETIME'] = now_str.upper()
    return nlp_metadata
        
#
def _prune_metadata(metadata):
    delete_key(metadata, 'RAW_TEXT')
    delete_key(metadata, 'REPORT_GROUP')
    delete_key(metadata, 'REPORT_HEADER')
    delete_key(metadata, 'REPORT_LINE')
    return metadata
        
#
def read_beakerap_data(data_tmp, server, user, password):
    
    # initialize lists
    metadata_list = []
    raw_text_list = []
    rpt_text_list = []
    
    # iterate through filtered data by result IDs
    RESULT_IDS = sorted(set(data_tmp['RESULT_ID']))
    for result_id in RESULT_IDS:
        
        # filter filtered data by result ID
        data_tmp_tmp = {}
        idxs = [i for i, x in enumerate(data_tmp['RESULT_ID']) \
                if x == result_id]
        for key in data_tmp.keys():
            data_tmp_tmp[key] = [data_tmp[key][i] for i in idxs]

        # iterate through filtered filtered data by report groups
        REPORT_GROUPS = sorted(set(data_tmp_tmp['REPORT_GROUP']))
        for report_group in REPORT_GROUPS:
            
            #
            idxs = [i for i, x in enumerate(data_tmp_tmp['REPORT_GROUP']) \
                    if x == report_group]
            REPORT_LINE = [data_tmp_tmp['REPORT_LINE'][i] for i in idxs]
            LINE = [data_tmp_tmp['RAW_TEXT'][i] for i in idxs]
            raw_text = []
            for i in range(len(REPORT_LINE)):
                idxss = [j for j, x in enumerate(REPORT_LINE) if x == i+1]
                if len(idxss) == 1:
                    idx = idxss[0]
                    raw_text.append(LINE[idx])
                    
            #
            raw_text = ''.join(raw_text)
            raw_text = remove_repeated_substrings(raw_text)
            rpt_text = raw_text
            
            #
            source_metadata = {}
            for key in data_tmp_tmp.keys():
                metadata[key] = data_tmp_tmp[key][0]
            source_metadata = _prune_metadata(source_metadata)
            
            #
            source_metadata_list.append(source_metadata)
            raw_text_list.append(raw_text)
            rpt_text_list.append(rpt_text)
            
    #
    nlp_metadata_list = []
    for i in range(len(source_metadata_list)):
        nlp_metadata = s_get_nlp_metadata(server, user, password)
        nlp_metadata['FILENAME'] = source_metadata_list[i]['FILENAME']
        del source_metadata_list[i]['FILENAME']
        nlp_metadata['NLP_DOCUMENT_IDX'] = \
            source_metadata_list[i]['NLP_DOCUMENT_IDX']
        del source_metadata_list[i]['NLP_DOCUMENT_IDX']
        nlp_metadata['NLP_MODE'] = source_metadata_list[i]['NLP_MODE']
        del source_metadata_list[i]['NLP_MODE']
        nlp_metadata['NLP_PROCESS'] = \
            source_metadata_list[i]['NLP_PROCESS']
        del source_metadata_list[i]['NLP_PROCESS']
        try:
            nlp_metadata['NOTE_TYPE'] = \
                source_metadata_list[i]['NOTE_TYPE']
            xml_metadata_keys = ['NLP_PROCESS', 'NOTE_TYPE']
        except:
            xml_metadata_keys = ['NLP_PROCESS' ]
        nlp_metadata_list.append(nlp_metadata)
            
    #
    return source_metadata_list, nlp_metadata_list, raw_text_list, \
           rpt_text_list, xml_metadata_keys

#
def read_data(data_tmp, server, user, password):
    if 'RAW_TEXT' in data_tmp.keys() and \
       data_tmp['RAW_TEXT'][0] is not None:
        raw_text = data_tmp['RAW_TEXT']
        raw_text = ''.join(raw_text)
        raw_text = remove_repeated_substrings(raw_text)
        rpt_text = raw_text
    else:
        raw_text = None
        rpt_text = None
    source_metadata = {}
    for key in data_tmp.keys():
        source_metadata[key] = data_tmp[key][0]
    source_metadata = _prune_metadata(source_metadata)
    nlp_metadata = {}
    nlp_metadata = _get_nlp_metadata(server, user, password)
    nlp_metadata['FILENAME'] = source_metadata['FILENAME']
    del source_metadata['FILENAME']
    nlp_metadata['NLP_DOCUMENT_IDX'] = \
        source_metadata['NLP_DOCUMENT_IDX']
    del source_metadata['NLP_DOCUMENT_IDX']
    nlp_metadata['NLP_MODE'] = source_metadata['NLP_MODE']
    del source_metadata['NLP_MODE']
    nlp_metadata['NLP_PROCESS'] = \
        source_metadata['NLP_PROCESS']
    del source_metadata['NLP_PROCESS']
    try:
        nlp_metadata['NOTE_TYPE'] = \
            source_metadata['NOTE_TYPE']
        xml_metadata_keys = ['NLP_PROCESS', 'NOTE_TYPE']
    except:
        xml_metadata_keys = ['NLP_PROCESS' ]
    return [source_metadata], [nlp_metadata], [raw_text], [rpt_text], \
           xml_metadata_keys