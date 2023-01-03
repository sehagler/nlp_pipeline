# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 12:06:14 2020

@author: haglers
"""

#
import os
import re
import sys

#
from tool_lib.py.processing_tools_lib.text_processing_tools \
    import remove_repeated_substrings
from tool_lib.py.processing_tools_lib.variable_processing_tools \
    import delete_key

#
class Raw_data_manager(object):
    
    #
    def __init__(self, static_data_manager, multiprocessing_flg, password):
        self.static_data_manager = static_data_manager
        static_data = self.static_data_manager.get_static_data()
        self.multiprocessing_flg = multiprocessing_flg
        self.raw_data = []
        if self.multiprocessing_flg:
            self.num_processes = static_data['num_processes']
        else:
            self.num_processes = 1
        
    #
    def _finish_document_data(self, data_file, document_data, document_ctr):
        if self.multiprocessing_flg:
            document_idx = int(document_data['NLP_DOCUMENT_IDX'][0])
        else:
            document_idx = document_ctr
            document_data['NLP_DOCUMENT_IDX'] = []
            document_data['NLP_DOCUMENT_IDX'].append(document_idx)
        filename, extension = os.path.splitext(data_file)
        if extension.lower() in [ '.xls', '.xlsx' ]:
            header_key = 'REPORT_HEADER'
            header_value_list = [ 'Final Diagnosis', 'Final Pathologic Diagnosis',
                                  'Karyotype', 'Clinical History',
                                  'Immunologic Analysis', 'Laboratory Data',
                                  'Microscopic Description',
                                  'Cytogenetic Analysis Summary',
                                  'Impressions and Recommendations' ]
            raw_text = ''
            for header_value in header_value_list:
                header_value = re.sub(':', '', header_value)
                for i in range(len(document_data[header_key])):
                    data_value = \
                        re.sub(':', '', document_data[header_key][i])
                    if header_value.lower() == data_value.lower():
                        raw_text += '\n' + header_value + '\n'
                        raw_text += '\n' + document_data['RAW_TEXT'][i] + '\n'
            for key in document_data.keys():
                document_data[key] = list(set(document_data[key]))
            document_data['RAW_TEXT'] = raw_text
        return document_data, document_idx
                
    #
    def _get_data_by_document_value(self, data_file, document_value,
                                    document_value_key=None):
        document_data = {}
        for i in range(len(self.data)):
            if self.data[i]['FILENAME'][0] == data_file:
                data = self.data[i]
        nlp_mode = data['NLP_MODE'][0]
        if nlp_mode in [ 'RESULT_ID', 'SOURCE_SYSTEM_RESULT_ID' ]:
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
        static_data = self.static_data_manager.get_static_data()
        num_processes = static_data['num_processes']
        partitioned_data = {}
        partitioned_data = {}
        if self.multiprocessing_flg:
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
    def _prune_metadata(self, metadata):
        delete_key(metadata, 'RAW_TEXT')
        delete_key(metadata, 'REPORT_GROUP')
        delete_key(metadata, 'REPORT_HEADER')
        delete_key(metadata, 'REPORT_LINE')
        return metadata
               
    #
    def _read_beaker_ap_data(self, poject_datda, data_tmp, password,
                            i2e_version, num_processes, process_idx):
        
        # initialize lists
        metadata_list = []
        text_list = []
        
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
                text = remove_repeated_substrings(raw_text)
                
                #
                source_metadata = {}
                for key in data_tmp_tmp.keys():
                    metadata[key] = data_tmp_tmp[key][0]
                source_metadata = self._prune_metadata(source_metadata)
                
                #
                source_metadata_list.append(source_metadata)
                text_list.append(text)
                
        #
        nlp_metadata_list = []
        for i in range(len(source_metadata_list)):
            nlp_metadata = _get_nlp_metadata(static_data, password, i2e_version,
                                             num_processes, process_idx)
            nlp_metadata['FILENAME'] = source_metadata_list[i]['FILENAME']
            del source_metadata_list[i]['FILENAME']
            nlp_metadata['NLP_DOCUMENT_IDX'] = \
                str(source_metadata_list[i]['NLP_DOCUMENT_IDX'])
            del source_metadata_list[i]['NLP_DOCUMENT_IDX']
            nlp_metadata['NLP_MODE'] = source_metadata_list[i]['NLP_MODE']
            del source_metadata_list[i]['NLP_MODE']
            try:
                nlp_metadata['NOTE_TYPE'] = \
                    source_metadata_list[i]['NOTE_TYPE']
                xml_metadata_keys = ['NOTE_TYPE']
            except:
                xml_metadata_keys = []
            nlp_metadata_list.append(nlp_metadata)
                
        #
        return source_metadata_list, nlp_metadata_list, text_list, \
               xml_metadata_keys
               
    #
    def _read_data(self, static_data, data_tmp, password, i2e_version,
                   num_processes, process_idx):
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
        source_metadata = self._prune_metadata(source_metadata)
        nlp_metadata = {}
        nlp_metadata = _get_nlp_metadata(static_data, password, i2e_version,
                                         num_processes, process_idx)
        nlp_metadata['FILENAME'] = source_metadata['FILENAME']
        del source_metadata['FILENAME']
        nlp_metadata['NLP_DOCUMENT_IDX'] = \
            str(source_metadata['NLP_DOCUMENT_IDX'])
        del source_metadata['NLP_DOCUMENT_IDX']
        nlp_metadata['NLP_MODE'] = source_metadata['NLP_MODE']
        del source_metadata['NLP_MODE']
        try:
            nlp_metadata['NOTE_TYPE'] = \
                source_metadata['NOTE_TYPE']
            xml_metadata_keys = [ 'NOTE_TYPE']
        except:
            xml_metadata_keys = []
        return [source_metadata], [nlp_metadata], [text], xml_metadata_keys
    
    #
    def _read_data_wrapper(self, password, data_tmp, i2e_version,
                           num_processes, process_idx):
        static_data = self.static_data_manager.get_static_data()
        do_beaker_ap_flg = static_data['do_beaker_ap_flg']
        if 'SOURCE_SYSTEM' in data_tmp.keys():
            source_system = data_tmp['SOURCE_SYSTEM'][0]
        else:
            source_system = 'UNKNOWN'
        if do_beaker_ap_flg and source_system == 'BeakderAP':
            source_metadata_list, nlp_metadata_list, text_list, \
            xml_metadata_keys = \
                    self._read_beaker_ap_data(static_data, data_tmp, password, 
                                             i2e_version, num_processes,
                                             process_idx)
        else:
            source_metadata_list, nlp_metadata_list, text_list, \
            xml_metadata_keys = \
                    self._read_data(static_data, data_tmp, password,
                                    i2e_version, num_processes, process_idx)
        return source_metadata_list, nlp_metadata_list, text_list, \
               xml_metadata_keys, source_system
                       
    #
    def append_raw_data(self, raw_data):
        self.raw_data.append(raw_data)
    
    #
    def get_data_by_document_number(self, data_file, document_number,
                                    document_ctr, i2e_version, num_processes,
                                    process_idx, password):
        document_data = {}
        document_found = False
        for i in range(len(self.data)):
            if len(self.data[i]['FILENAME']) > 0 and self.data[i]['FILENAME'][0] == data_file:
                data = self.data[i]
                keys = list(data.keys())
                if document_number in data[keys[0]]:
                    doc_idx = data[keys[0]].index(document_number)
                    for key in keys:
                        document_data[key] = [ data[key][doc_idx] ]
        document_data, document_idx = \
            self._finish_document_data(data_file, document_data, document_ctr)
            
        #
        source_metadata_list, nlp_metadata_list, text_list, \
            xml_metadata_keys, source_system = \
                self._read_data_wrapper(password, document_data, i2e_version,
                                        num_processes, process_idx)
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
    def get_data_by_document_value(self, data_file, document_value_key,
                                   document_value, document_ctr, i2e_version,
                                   num_processes, process_idx, password):
        document_data = \
            self._get_data_by_document_value(data_file, document_value, 
                                             document_value_key)
        document_data, document_idx = \
            self._finish_document_data(data_file, document_data, document_ctr)
        
        #
        source_metadata_list, nlp_metadata_list, text_list, \
            xml_metadata_keys, source_system = \
                self._read_data_wrapper(password, document_data, i2e_version,
                                        num_processes, process_idx)
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
        doc_num = 0
        for data in self.data:
            if len(data['FILENAME']) > 0 and data['FILENAME'][0] == data_file:
                keys = list(data.keys())
                document_numbers.extend(data[keys[0]])
        return document_numbers
    
    #
    def get_document_values(self, data_file):
        static_data = self.static_data_manager.get_static_data()
        directory_manager = static_data['directory_manager']
        raw_data_dir = \
            directory_manager.pull_directory('raw_data_dir')
        document_value_dict = {}
        for i in range(len(self.data)):
            filename = self.data[i]['FILENAME'][0]
            document_value_dict[os.path.join(raw_data_dir, filename)] = {}
            nlp_mode = self.data[i]['NLP_MODE'][0]
            if nlp_mode == 'CASE_NUMBER':
                label0 = 'MRN'
                label1 = 'CASE_NUMBER'
            elif nlp_mode == 'RESULT_ID':
                label0 = 'RESULT_ID'
                label1 = 'RESULT_ID'
            elif nlp_mode == 'SOURCE_SYSTEM_RESULT_ID':
                label0 = 'SOURCE_SYSTEM_RESULT_ID'
                label1 = 'SOURCE_SYSTEM_RESULT_ID'
            data_label0 = self.data[i][label0]
            data_label1 = self.data[i][label1]
            items = sorted(set(data_label0))
            for item in items:
                document_value_list = []
                idxs = [j for j, x in enumerate(data_label0) if x == item ]
                document_value_list.append([data_label1[j] for j in idxs])
                document_value_dict[os.path.join(raw_data_dir, filename)][item] = \
                    sorted(list(set(document_value_list[0])))
        document_value_keys = \
            sorted(document_value_dict[os.path.join(raw_data_dir, data_file)].keys())
        document_values = []
        for i in range(len(document_value_keys)):
            document_value_key = document_value_keys[i]
            document_values_tmp = \
                sorted(document_value_dict[os.path.join(raw_data_dir, data_file)][document_value_key])
            for j in range(len(document_values_tmp)):
                document_values.append([document_value_key, document_values_tmp[j]])
        return document_values
    
    #
    def get_multiprocessing_flg(self):
        return self.multiprocessing_flg
    
    #
    def get_number_of_processes(self):
        return self.num_processes
    
    #
    def partition_data(self):
        self.partitioned_data = \
            self._partition_data_by_thread(self.raw_data)
    
    #
    def print_num_of_docs_in_preprocessing_set(self):
        num_docs = 0
        for key in self.partitioned_data.keys():
            for data in self.partitioned_data[key]:
                keys = list(data.keys())
                num_docs += len(data[keys[0]])
        print('Number of documents in preprocessing set: ' + str(num_docs))
        
    #
    def select_process(self, process_idx):
        self.data = self.partitioned_data[process_idx]
        
#
def _get_nlp_metadata(static_data, password, i2e_version, num_processes,
                      process_idx):
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