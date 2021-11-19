# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 13:07:13 2021

@author: haglers
"""

#
import datetime
import os
import pickle
import re

#
from nlp_lib.py.document_preprocessing_lib.document_preprocessing_manager_class \
    import Document_preprocessing_manager

#
class Preprocessing_worker(object):
    
    #
    def __init__(self, static_data_manager, preprocess_files_flg):
        self.static_data = static_data_manager.get_static_data()
        self.preprocess_files_flg = preprocess_files_flg
        self.server = self.static_data['acc_server'][2]
        self.user = self.static_data['user']
        self._create_managers(static_data_manager)
        
    #
    def _create_managers(self, static_data_manager):
        self.document_preprocessing_manager = \
            Document_preprocessing_manager(static_data_manager)

    #
    def _preprocess_document(self, raw_data_manager, data_tmp, start_idx, 
                             document_idx, source_metadata_list,
                             nlp_metadata_list, xml_metadata_list,
                             text_list, source_system, formatting, 
                             document_ctr, fail_ctr, password):
        document_ctr += 1
        if document_idx >= start_idx:
            if 'RAW_TEXT' in data_tmp.keys() and \
               not (len(data_tmp['RAW_TEXT']) == 1 and data_tmp['RAW_TEXT'][0] is None):
                now = datetime.datetime.now()
                document_start_datetime = \
                    now.strftime("%d-%b-%y %H:%M:%S.%f") [:-3]
                if len(text_list) > 1:
                    print(len(text_list))
                for i in range(len(text_list)):
                    source_metadata = source_metadata_list[i]
                    nlp_metadata = nlp_metadata_list[i]
                    xml_metadata = xml_metadata_list[i]
                    text_item = text_list[i]
                    if self.preprocess_files_flg:
                        self.dynamic_data_manager, processed_raw_text, \
                        processed_report_text = \
                            self.document_preprocessing_manager.process_document(self.dynamic_data_manager,
                                                                                 text_item, source_system,
                                                                                 formatting)
                        xml_ret_val = \
                            self.linguamatics_i2e_manager.generate_xml_file(document_idx,
                                                                            xml_metadata,
                                                                            processed_raw_text,
                                                                            processed_report_text)
                        now = datetime.datetime.now()
                        document_end_datetime = now.strftime("%d-%b-%y %H:%M:%S.%f")[:-3]
                        nlp_metadata['DOCUMENT_PREPROCESSING_START_DATETIME'] = \
                            document_start_datetime
                        nlp_metadata['DOCUMENT_PREPROCESSING_END_DATETIME'] = \
                            document_end_datetime
                        self.metadata_manager.append_metadata_dicts(str(document_idx),
                                                                    source_metadata,
                                                                    nlp_metadata)
                    else:
                        xml_ret_val = True
                else:
                    xml_ret_val = True
        else:
            xml_ret_val = True
        if not xml_ret_val:
            fail_ctr += 1
            print(str(document_idx))
        return document_ctr, fail_ctr
    
    #
    def _preprocess_documents(self, raw_data_manager, start_idx,
                              document_ctr, fail_ctr, password):
        raw_data_files_dict = self.static_data['raw_data_files']
        raw_data_files = list(raw_data_files_dict.keys())
        for data_file in raw_data_files:
            filename, extension = os.path.splitext(data_file)
            formatting = self.static_data['raw_data_files'][data_file]['FORMATTING']
            if extension.lower() in [ '.xls', '.xlsx' ]:
                document_values = \
                    raw_data_manager.get_document_values(data_file)
                for i in range(len(document_values)):
                    document_value = document_values[i]
                    data_tmp, document_idx, source_metadata_list, \
                    nlp_metadata_list, text_list, xml_metadata_list, \
                    source_system = \
                        raw_data_manager.get_data_by_document_value(data_file,
                                                                    document_value[0],
                                                                    document_value[1],
                                                                    document_ctr,
                                                                    self.i2e_version,
                                                                    self.num_processes,
                                                                    self.process_idx,
                                                                    password)
                    if bool(data_tmp):
                        document_ctr, fail_ctr = \
                            self._preprocess_document(raw_data_manager, data_tmp, 
                                                      start_idx, document_idx,
                                                      source_metadata_list,
                                                      nlp_metadata_list,
                                                      xml_metadata_list,
                                                      text_list,
                                                      source_system,
                                                      formatting, document_ctr, 
                                                      fail_ctr,
                                                      password)
            elif extension.lower() in [ '.xml' ]:
                document_numbers = \
                    raw_data_manager.get_document_numbers(data_file)
                for document_number in document_numbers:
                    data_tmp, document_idx, source_metadata_list, \
                    nlp_metadata_list, text_list, xml_metadata_list, \
                    source_system = \
                        raw_data_manager.get_data_by_document_number(data_file,
                                                                     document_number,
                                                                     document_ctr,
                                                                     self.i2e_version,
                                                                     self.num_processes,
                                                                     self.process_idx,
                                                                     password)
                    if bool(data_tmp):
                        document_ctr, fail_ctr = \
                            self._preprocess_document(raw_data_manager, data_tmp, 
                                                      start_idx, document_idx,
                                                      source_metadata_list,
                                                      nlp_metadata_list,
                                                      xml_metadata_list,
                                                      text_list, source_system, 
                                                      formatting, document_ctr,
                                                      fail_ctr, password)
            else:
                print('invalid file extension: ' + extension)
        return document_ctr, fail_ctr
        
    #
    def process_raw_data(self, queue, dynamic_data_manager,
                         linguamatics_i2e_manager, metadata_manager, 
                         num_processes, process_idx, start_idx, i2e_version,
                         password):
        self.i2e_version = i2e_version
        self.dynamic_data_manager = dynamic_data_manager
        self.linguamatics_i2e_manager = linguamatics_i2e_manager
        self.metadata_manager = metadata_manager
        self.num_processes = num_processes
        self.process_idx = process_idx
        
        # Read data kludge to be done properly later
        operation_mode = self.static_data['operation_mode']
        pkl_file = 'raw_data_' + operation_mode + '.pkl'
        self.raw_data_manager = pickle.load(open(pkl_file, 'rb'))
        self.raw_data_manager.select_process(process_idx)
        # Read data kludge to be done properly later
        
        print('Process ' + str(process_idx) + ' starting')
        document_ctr = 0
        fail_ctr = 0
        document_ctr, fail_ctr = self._preprocess_documents(self.raw_data_manager,
                                                            start_idx, document_ctr,
                                                            fail_ctr, password)
        queue.put([self.dynamic_data_manager, self.metadata_manager, document_ctr])
        print('Process ' + str(process_idx) + ' finished')
        print(' Number documents processed: %d' % document_ctr)
        print(' Number of failed documents: %d' % fail_ctr)