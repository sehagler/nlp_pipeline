# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 13:07:13 2021

@author: haglers
"""

#
import datetime

#
from base_lib.worker_base_class import Worker_base
from tools_lib.processing_tools_lib.function_processing_tools \
    import parallel_composition
    
#
class Preprocessing_worker(Worker_base):
    
    #
    def __init__(self, static_data_object, logger_object, deidentifier_object,
                 preprocessor_registry, nlp_tool_registry):
        Worker_base.__init__(self, static_data_object, logger_object)
        self.deidentifier_object = deidentifier_object
        self.preprocessor_registry = preprocessor_registry
        self.nlp_tool_registry = nlp_tool_registry
        static_data = self.static_data_object.get_static_data()
        self.deidentifier_flg = static_data['deidentifier_flg']
        self.server = static_data['acc_server'][2]
        self.user = static_data['user']
        
    #
    def _append_document_dict(self, document_dict, document_idx, nlp_metadata,
                              processed_raw_text, processed_report_text,
                              source_metadata, xml_metadata):
            document_dict[document_idx] = {}
            document_dict[document_idx]['nlp_metadata'] = \
                nlp_metadata
            document_dict[document_idx]['processed_raw_text'] = \
                processed_raw_text
            document_dict[document_idx]['processed_report_text'] = \
                processed_report_text
            document_dict[document_idx]['source_metadata'] = \
                source_metadata
            document_dict[document_idx]['xml_metadata'] = \
                xml_metadata
            return document_dict
        
    #
    def _generate_files(self, argument_dict):
        document_dict = argument_dict['document_dict']
        linguamatics_i2e_preprocessing_data_out_dir = \
            argument_dict['linguamatics_i2e_preprocessing_data_out_dir']
        linguamatics_i2e_object = \
            self.nlp_tool_registry.pull_object('linguamatics_i2e_object')
        for document_idx in document_dict.keys():
            generate_data_file_ret_val = \
                linguamatics_i2e_object.create_source_data_file(linguamatics_i2e_preprocessing_data_out_dir,
                                                                document_idx,
                                                                document_dict)

    #
    def _preprocess_document(self, dynamic_data_manager, document_idx,
                             nlp_metadata, text_item, source_system):
        now = datetime.datetime.now()
        document_start_datetime = \
            now.strftime("%d-%b-%y %H:%M:%S.%f") [:-3]
        dynamic_data_manager, processed_report_text = \
            self.preprocessor_registry.run_registry(dynamic_data_manager,
                                                    text_item,
                                                    source_system)
        deidentified_report_text = \
            self.deidentifier_object.deidentify(processed_report_text)
        now = datetime.datetime.now()
        document_end_datetime = now.strftime("%d-%b-%y %H:%M:%S.%f")[:-3]
        nlp_metadata['DOCUMENT_PREPROCESSING_START_DATETIME'] = \
            document_start_datetime
        nlp_metadata['DOCUMENT_PREPROCESSING_END_DATETIME'] = \
            document_end_datetime
        return dynamic_data_manager, nlp_metadata, text_item, deidentified_report_text
    
    #
    def _preprocess_documents(self, dynamic_data_manager, start_idx, password):
        static_data = self.static_data_object.get_static_data()
        raw_data_files_dict = static_data['raw_data_files']
        raw_data_files = list(raw_data_files_dict.keys())
        document_dict = {}
        for data_file in raw_data_files:
            document_numbers = \
                self.raw_data_manager.get_document_numbers(data_file)
            for document_number in document_numbers:
                data_tmp, document_idx, source_metadata_list, \
                nlp_metadata_list, text_list, xml_metadata_list, \
                source_system = \
                    self.raw_data_manager.get_data_by_document_number(data_file,
                                                                      document_number,
                                                                      self.i2e_version,
                                                                      self.process_idx,
                                                                      password)
                text_item = text_list[0]
                nlp_metadata = nlp_metadata_list[0]
                source_metadata = source_metadata_list[0]
                xml_metadata = xml_metadata_list[0]
                if bool(data_tmp) and \
                   document_idx >= start_idx:
                    if 'RAW_TEXT' in data_tmp.keys() and \
                       not (len(data_tmp['RAW_TEXT']) == 1 and data_tmp['RAW_TEXT'][0] is None):
                        dynamic_data_manager, nlp_metadata, \
                        processed_raw_text, processed_report_text = \
                            self._preprocess_document(dynamic_data_manager,
                                                      document_idx,
                                                      nlp_metadata, text_item,
                                                      source_system)
                        document_dict = self._append_document_dict(document_dict,
                                                                   document_idx,
                                                                   nlp_metadata,
                                                                   processed_raw_text, 
                                                                   processed_report_text,
                                                                   source_metadata,
                                                                   xml_metadata)
        return dynamic_data_manager, document_dict
    
    def _process_data(self, argument_dict):
        self.i2e_version = argument_dict['i2e_version'] 
        dynamic_data_manager = argument_dict['dynamic_data_manager']
        linguamatics_i2e_preprocessing_data_out_dir = \
            argument_dict['linguamatics_i2e_preprocessing_data_out_dir']
        metadata_manager = argument_dict['metadata_manager'] 
        self.num_processes = argument_dict['num_processes']
        self.process_idx = argument_dict['process_idx']
        self.raw_data_manager = argument_dict['raw_data_manager']
        password = argument_dict['password']
        start_idx = argument_dict['start_idx']
        dynamic_data_manager, document_dict = \
            self._preprocess_documents(dynamic_data_manager, start_idx,
                                       password)
        argument_dict = {}
        argument_dict['document_dict'] = document_dict
        argument_dict['linguamatics_i2e_preprocessing_data_out_dir'] = \
            linguamatics_i2e_preprocessing_data_out_dir
        argument_dict['metadata_manager'] = metadata_manager
        return_dict = \
            parallel_composition([self._update_metadata_manager,
                                  self._generate_files], argument_dict)
        metadata_manager = \
            return_dict[self._update_metadata_manager.__name__]
        return_dict = {}
        return_dict['dynamic_data_manager'] = dynamic_data_manager
        return_dict['document_dict'] = document_dict
        return_dict['metadata_manager'] = metadata_manager
        return return_dict
            
    #
    def _update_metadata_manager(self, argument_dict):
        document_dict = argument_dict['document_dict']
        metadata_manager = argument_dict['metadata_manager']
        for document_idx in document_dict.keys():
            metadata_manager.append_metadata_dicts(str(document_idx),
                                                   document_dict[document_idx]['source_metadata'],
                                                   document_dict[document_idx]['nlp_metadata'])
        return metadata_manager