# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 13:07:13 2021

@author: haglers
"""

#
import datetime
import numpy as np
import os
import pickle
import re
from xml.dom import minidom
import xml.etree.ElementTree as ET

#
from nlp_lib.py.document_preprocessing_lib.document_preprocessing_manager_class \
    import Document_preprocessing_manager
from tool_lib.py.processing_tools_lib.file_processing_tools \
    import write_file
from tool_lib.py.processing_tools_lib.text_processing_tools \
    import make_ascii, make_xml_compatible

#
class Preprocessing_worker(object):
    
    #
    def __init__(self, static_data_manager, preprocess_files_flg):
        self.static_data_manager = static_data_manager
        static_data = self.static_data_manager.get_static_data()
        self.preprocess_files_flg = preprocess_files_flg
        self.server = static_data['acc_server'][2]
        self.user = static_data['user']
        self._create_managers(self.static_data_manager)
        self.metadata_keys = []
        
    #
    def _create_managers(self, static_data_manager):
        self.document_preprocessing_manager = \
            Document_preprocessing_manager(static_data_manager)
            
    #
    def _generate_xml_file(self, ctr, metadata, raw_text, rpt_text):
        static_data = self.static_data_manager.get_static_data()
        directory_manager = static_data['directory_manager']
        self._set_metadata(metadata)
        raw_text = make_ascii(raw_text)
        raw_text = make_xml_compatible(raw_text)
        keys = metadata.keys()
        for key in keys:
            key_value = metadata[key]
            if key_value is not None:
                key_value = key_value.replace('\'','\\\'')
            metadata[key] = key_value
        report = ET.Element('REPORT')
        for key in keys:
            subelement = ET.SubElement(report, key)
            subelement.text = metadata[key]
        subelement = ET.SubElement(report, 'RAW_TEXT')
        subelement.text = raw_text
        subelement = ET.SubElement(report, 'rpt_text')
        subelement.text = rpt_text
        xml_str = minidom.parseString(ET.tostring(report)).toprettyxml(indent = "   ")
        outdir = directory_manager.pull_directory('preprocessing_data_out')
        filename = str(ctr) + '.xml'
        write_file(os.path.join(outdir, filename), xml_str, False, False)
        ret_val = True
        return ret_val

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
                    if self.preprocess_files_flg:
                        xml_metadata = xml_metadata_list[i]
                        text_item = text_list[i]
                        self.dynamic_data_manager, processed_raw_text, \
                        processed_report_text = \
                            self.document_preprocessing_manager.process_document(self.dynamic_data_manager,
                                                                                 text_item, source_system,
                                                                                 formatting)
                        xml_ret_val = \
                            self._generate_xml_file(document_idx, xml_metadata,
                                                    processed_raw_text,
                                                    processed_report_text)
                        now = datetime.datetime.now()
                        document_end_datetime = now.strftime("%d-%b-%y %H:%M:%S.%f")[:-3]
                        nlp_metadata['DOCUMENT_PREPROCESSING_START_DATETIME'] = \
                            document_start_datetime
                        nlp_metadata['DOCUMENT_PREPROCESSING_END_DATETIME'] = \
                            document_end_datetime
                    else:
                        xml_ret_val = True
                    self.metadata_manager.append_metadata_dicts(str(document_idx),
                                                                source_metadata,
                                                                nlp_metadata)
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
        static_data = self.static_data_manager.get_static_data()
        raw_data_files_dict = static_data['raw_data_files']
        raw_data_files = list(raw_data_files_dict.keys())
        raw_data_files_extensions = []
        
        # kludge to handle legacy XLS or XLSX files missing some metadata
        for data_file in raw_data_files:
            filename, extension = os.path.splitext(data_file)
            raw_data_files_extensions.append(extension.lower())
        if '.xls' in raw_data_files_extensions or '.xlsx' in raw_data_files_extensions:
            extension = '.xls'
        else:
            extension = '.xml'
        #
            
        for data_file in raw_data_files:
            formatting = static_data['raw_data_files'][data_file]['FORMATTING']
            if extension.lower() in [ '.xml' ]:
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
                            
            # kludge to handle legacy XLS or XLSX files missing some metadata 
            elif extension.lower() in [ '.xls', '.xlsx' ]:
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
                                                      text_list, source_system,
                                                      formatting, document_ctr, 
                                                      fail_ctr, password)
            #
            
            else:
                print('invalid file extension: ' + extension)
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
        static_data = self.static_data_manager.get_static_data()
        
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