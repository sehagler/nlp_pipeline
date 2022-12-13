# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 13:07:13 2021

@author: haglers
"""

#
import datetime
import numpy as np
import pickle
    
#
class Preprocessing_worker(object):
    
    #
    def __init__(self, static_data_object, text_normalization_object,
                 nlp_tool_manager_registry, preprocess_files_flg):
        self.static_data_object = static_data_object
        self.text_normalization_object = text_normalization_object
        self.nlp_tool_manager_registry = nlp_tool_manager_registry
        static_data = self.static_data_object.get_static_data()
        self.directory_manager = static_data['directory_manager']
        self.preprocess_files_flg = preprocess_files_flg
        self.server = static_data['acc_server'][2]
        self.user = static_data['user']
        self.metadata_keys = []

    #
    def _preprocess_document(self, raw_data_manager, data_tmp, start_idx, 
                             document_idx, source_metadata_list,
                             nlp_metadata_list, xml_metadata_list,
                             text_list, source_system, document_ctr, fail_ctr,
                             password):
        linguamatics_outdir = \
            self.directory_manager.pull_directory('linguamatics_i2e_preprocessing_data_out')
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
                    if self.preprocess_files_flg:
                        xml_metadata = xml_metadata_list[i]
                        text_item = text_list[i]
                        self.dynamic_data_manager, processed_raw_text, \
                        processed_report_text = \
                            self.text_normalization_object.process_document(self.dynamic_data_manager,
                                                                             text_item, source_system)
                        self._set_metadata(xml_metadata)
                        linguamatics_i2e_object = \
                            self.nlp_tool_manager_registry.get_manager('linguamatics_i2e_object')
                        generate_data_file_ret_val = \
                            linguamatics_i2e_object.create_source_data_file(linguamatics_outdir,
                                                                             document_idx,
                                                                             xml_metadata,
                                                                             processed_raw_text,
                                                                             processed_report_text)
                        '''
                        melax_clamp_manager = \
                            self.nlp_tool_manager_registry.get_manager('melax_clamp_manager')
                        generate_data_file_ret_val = \
                            melax_clamp_manager.create_source_data_file(document_idx,
                                                                        processed_report_text)
                        ohsu_nlp_template_manager = \
                            self.nlp_tool_manager_registry.get_manager('ohsu_nlp_template_manager')
                        generate_data_file_ret_val = \
                            ohsu_nlp_template_manager.create_source_data_file(document_idx,
                                                                              processed_report_text)
                        '''
                        now = datetime.datetime.now()
                        document_end_datetime = now.strftime("%d-%b-%y %H:%M:%S.%f")[:-3]
                        nlp_metadata['DOCUMENT_PREPROCESSING_START_DATETIME'] = \
                            document_start_datetime
                        nlp_metadata['DOCUMENT_PREPROCESSING_END_DATETIME'] = \
                            document_end_datetime
                    else:
                        generate_data_file_ret_val = True
                    self.metadata_manager.append_metadata_dicts(str(document_idx),
                                                                source_metadata,
                                                                nlp_metadata)
                else:
                    generate_data_file_ret_val = True
        else:
            generate_data_file_ret_val = True
        if not generate_data_file_ret_val:
            fail_ctr += 1
            print(str(document_idx))
        return document_ctr, fail_ctr
    
    #
    def _preprocess_documents(self, raw_data_manager, start_idx,
                              document_ctr, fail_ctr, password):
        static_data = self.static_data_object.get_static_data()
        raw_data_files_dict = static_data['raw_data_files']
        raw_data_files = list(raw_data_files_dict.keys())
        raw_data_files_extensions = []
        for data_file in raw_data_files:
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
                                                  document_ctr, fail_ctr,
                                                  password)
        return document_ctr, fail_ctr
    
    #
    def _set_metadata(self, metadata):
        self.metadata_keys += tuple(metadata.keys())
        self.metadata_keys = tuple(np.unique(self.metadata_keys))
        
    #
    def process_raw_data(self, queue, dynamic_data_manager, metadata_manager,
                         num_processes, process_idx, start_idx, i2e_version,
                         password):
        self.i2e_version = i2e_version
        self.dynamic_data_manager = dynamic_data_manager
        self.metadata_manager = metadata_manager
        self.num_processes = num_processes
        self.process_idx = process_idx
        
        #
        static_data = self.static_data_object.get_static_data()
        
        # Read data kludge to be done properly later
        operation_mode = static_data['operation_mode']
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