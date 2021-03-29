# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 13:07:13 2021

@author: haglers
"""

#
import datetime
import pickle
import re

#
from linguamatics_i2e_lib.py.linguamatics_i2e_manager_class \
    import Linguamatics_i2e_manager
from nlp_lib.py.document_preprocessing_lib.document_preprocessing_manager_class \
    import Document_preprocessing_manager
from nlp_lib.py.template_lib.preprocessor_template_lib.raw_report_preprocessor_class \
    import Raw_report_preprocessor

#
class Preprocessing_worker(object):
    
    #
    def __init__(self, project_data, preprocess_files_flg, password):
        self.preprocess_files_flg = preprocess_files_flg
        self.project_data = project_data
        self.server = project_data['acc_server'][2]
        self.user = project_data['user']
        self.linguamatics_i2e_manager = \
            Linguamatics_i2e_manager(self.project_data, password)
        self.raw_report_preprocessor = Raw_report_preprocessor(project_data)

    #
    def _preprocess_document(self, raw_data_manager, data_tmp, start_idx, 
                             document_idx, source_metadata_list,
                             nlp_metadata_list, xml_metadata_list,
                             raw_text_list, rpt_text_list, source_system,
                             document_ctr, fail_ctr, password):
        document_ctr += 1
        if self.preprocess_files_flg:
            if document_idx >= start_idx:
                if 'RAW_TEXT' in data_tmp.keys() and \
                   not (len(data_tmp['RAW_TEXT']) == 1 and data_tmp['RAW_TEXT'][0] is None):
                    now = datetime.datetime.now()
                    document_start_datetime = \
                        now.strftime("%d-%b-%y %H:%M:%S.%f") [:-3]
                    if len(rpt_text_list) > 1:
                        print(len(rpt_text_list))
                    for i in range(len(rpt_text_list)):
                        source_metadata = source_metadata_list[i]
                        nlp_metadata = nlp_metadata_list[i]
                        xml_metadata = xml_metadata_list[i]
                        raw_text = raw_text_list[i]
                        rpt_text = rpt_text_list[i]
                        self.raw_report_preprocessor.push_text(raw_text)
                        self.raw_report_preprocessor.normalize_report()
                        report_preprocessor = \
                            self._report_preprocessor(xml_metadata)
                        report_preprocessor.push_dynamic_data_manager(self.dynamic_data_manager)
                        report_preprocessor.push_text(rpt_text)
                        report_preprocessor.format_report(source_system)
                        report_preprocessor.normalize_report()
                        self.dynamic_data_manager = \
                            report_preprocessor.pull_dynamic_data_manager()
                        xml_ret_val = \
                            self.linguamatics_i2e_manager.generate_xml_file(document_idx, xml_metadata,
                                                                            self.raw_report_preprocessor.pull_text(),
                                                                            report_preprocessor.pull_text())
                    else:
                        xml_ret_val = True
            else:
                if 'SOURCE_SYSTEM' in data_tmp.keys():
                    source_system = data_tmp['SOURCE_SYSTEM'][0]
                else:
                    source_system = 'UNKNOWN'
                source_metadata_list, nlp_metadata_list, raw_text_list, \
                    rpt_text_list, xml_metadata = \
                    read_data(self.project_data, password, source_system, 
                              data_tmp, self.i2e_version, self.num_processes,
                              self.process_idx, do_beakerap_flg)
                source_metadata = source_metadata_list[0]
                nlp_metadata = nlp_metadata_list[0]
                xml_ret_val = True
            now = datetime.datetime.now()
            document_end_datetime = now.strftime("%d-%b-%y %H:%M:%S.%f")[:-3]
            nlp_metadata['DOCUMENT_PREPROCESSING_START_DATETIME'] = \
                document_start_datetime
            nlp_metadata['DOCUMENT_PREPROCESSING_END_DATETIME'] = \
                document_end_datetime
            self.metadata_manager.append_metadata_dicts(str(document_ctr),
                                        source_metadata, nlp_metadata)
            if not xml_ret_val:
                fail_ctr += 1
                print(str(document_ctr))
        return document_ctr, fail_ctr
    
    #
    def _preprocess_documents(self, raw_data_manager, start_idx,
                              document_ctr, fail_ctr, password):
        if self.raw_data_manager_mode_flg == 'get_data_by_document_number':
            document_numbers = raw_data_manager.get_document_numbers()
            for document_number in document_numbers:
                data_tmp, document_idx, source_metadata_list, \
                    nlp_metadata_list, raw_text_list, rpt_text_list, \
                    xml_metadata_list, source_system = \
                    raw_data_manager.get_data_by_document_number(document_number,
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
                                                  raw_text_list, rpt_text_list,
                                                  source_system, document_ctr,
                                                  fail_ctr, password)
        else:
            document_value_dict = raw_data_manager.get_document_values()
            for data_file in document_value_dict:
                for document_value_key in sorted(document_value_dict[data_file].keys()):
                    for document_value in sorted(document_value_dict[data_file][document_value_key]):
                        data_tmp, document_idx, source_metadata_list, \
                            nlp_metadata_list, raw_text_list, rpt_text_list, \
                            xml_metadata_list, source_system = \
                            raw_data_manager.get_data_by_document_value(data_file,
                                                                        document_value_key,
                                                                        document_value,
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
                                                          raw_text_list,
                                                          rpt_text_list, 
                                                          source_system,
                                                          document_ctr, 
                                                          fail_ctr,
                                                          password)
        return document_ctr, fail_ctr
    
    #
    def _report_preprocessor(self, xml_metadata):
        print('no report preprocessor defined')
        
    #
    def process_raw_data(self, queue, dynamic_data_manager, metadata_manager, 
                         num_processes, process_idx, start_idx, i2e_version,
                         password):
        self.i2e_version = i2e_version
        self.dynamic_data_manager = dynamic_data_manager
        self.metadata_manager = metadata_manager
        self.num_processes = num_processes
        self.process_idx = process_idx
        
        # Read data kludge to be done properly later
        self.raw_data_manager = pickle.load(open('raw_data.pkl', 'rb'))
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