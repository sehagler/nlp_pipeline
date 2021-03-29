# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 13:07:13 2021

@author: haglers
"""

#
import re

#
from nlp_lib.py.reader_lib.raw_data_reader_class import read_beakerap_data, read_data
from nlp_lib.py.template_lib.preprocessor_template_lib.raw_report_preprocessor_class \
    import Raw_report_preprocessor

#
class Preprocessing_worker(object):
    
    #
    def __init__(self, project_data, preprocess_files_flg):
        self.preprocess_files_flg = preprocess_files_flg
        self.project_data = project_data
        self.server = project_data['acc_server'][2]
        self.user = project_data['user']
        self.raw_report_preprocessor = Raw_report_preprocessor(project_data)

    #
    def _preprocess_document(self, raw_data_reader, data_tmp, start_idx, 
                             document_ctr, fail_ctr, password):
        do_beakerap_flg = self.project_data['do_beakerap_flg']
        try:
            multiprocessing_flg = self.project_data['flags']['multiprocessing']
        except:
            multiprocessing_flg = False
        if multiprocessing_flg:
            document_idx = int(data_tmp['NLP_DOCUMENT_IDX'][0])
        else:
            document_idx = document_ctr
            data_tmp['NLP_DOCUMENT_IDX'] = []
            data_tmp['NLP_DOCUMENT_IDX'].append(document_idx)
        document_ctr += 1
        if document_idx >= start_idx:
            if 'RAW_TEXT' in data_tmp.keys() and \
               not (len(data_tmp['RAW_TEXT']) == 1 and data_tmp['RAW_TEXT'][0] is None):
                if 'header_values' in self.project_data.keys():
                    if len(self.project_data['header_values']) > 1:
                        raw_text = ''
                        for header_value in self.project_data['header_values']:
                            header_value = re.sub(':', '', header_value)
                            for i in range(len(data_tmp[self.project_data['header_key']])):
                                data_value = re.sub(':', '', data_tmp[self.project_data['header_key']][i])
                                if header_value.lower() == data_value.lower():
                                    raw_text += '\n' + header_value + '\n'
                                    raw_text += '\n' + data_tmp['RAW_TEXT'][i] + '\n'
                        for key in data_tmp.keys():
                            data_tmp[key] = list(set(data_tmp[key]))
                        data_tmp['RAW_TEXT'] = raw_text
                if 'SOURCE_SYSTEM' in data_tmp.keys():
                    source_system = data_tmp['SOURCE_SYSTEM'][0]
                else:
                    source_system = 'UNKNOWN'
                source_metadata_list, nlp_metadata_list, raw_text_list, \
                    rpt_text_list, xml_metadata_keys = \
                    self._read_data_wrapper(source_system, data_tmp, do_beakerap_flg, password)
                for i in range(len(rpt_text_list)):
                    source_metadata = source_metadata_list[i]
                    nlp_metadata = nlp_metadata_list[i]
                    raw_text = raw_text_list[i]
                    rpt_text = rpt_text_list[i]
                    self.metadata_manager.append_metadata_dicts(str(document_idx),
                                                                source_metadata,
                                                                nlp_metadata)
                    if self.preprocess_files_flg:
                        xml_metadata = {}
                        xml_metadata['DOCUMENT_ID'] = str(document_idx)
                        xml_metadata['SOURCE_SYSTEM'] = \
                            source_metadata['SOURCE_SYSTEM']
                        for key in xml_metadata_keys:
                            xml_metadata[key] = nlp_metadata[key]
                        self.raw_report_preprocessor.push_text(raw_text)
                        self.raw_report_preprocessor.normalize_report()
                        report_preprocessor = \
                            self._report_preprocessor(xml_metadata)
                        report_preprocessor.push_linguamatics_i2e_writer(self.linguamatics_i2e_writer)
                        report_preprocessor.push_text(rpt_text)
                        report_preprocessor.format_report(source_system)
                        report_preprocessor.normalize_report()
                        self.linguamatics_i2e_writer = \
                            report_preprocessor.pull_linguamatics_i2e_writer()
                        xml_ret_val = \
                            self.linguamatics_i2e_writer.generate_xml_file(document_idx, xml_metadata,
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
                    self._read_data_wrapper(source_system, data_tmp, do_beakerap_flg, password)
                source_metadata = source_metadata_list[0]
                nlp_metadata = nlp_metadata_list[0]
                self.metadata_manager.append_metadata_dicts(str(document_ctr),
                                                            source_metadata,
                                                            nlp_metadata)
                xml_ret_val = True
            if not xml_ret_val:
                fail_ctr += 1
                print(str(document_ctr))
        return document_ctr, fail_ctr
    
    #
    def _preprocess_documents(self, raw_data_reader, start_idx, document_ctr,
                              fail_ctr, password):
        print('_preprocess_documents not defined')
    
    #
    def _read_data_wrapper(self, source_system, data_tmp, do_beakerap_flg, password):
        if do_beakerap_flg and source_system == 'BeakderAP':
            source_metadata_list, nlp_metadata_list, raw_text_list, \
                rpt_text_list, xml_metadata_keys = \
                    read_beakerap_data(data_tmp, self.server, self.user, password)
        else:
            source_metadata_list, nlp_metadata_list, raw_text_list, \
                rpt_text_list, xml_metadata_keys = \
                    read_data(data_tmp, self.server, self.user, password)
        return source_metadata_list, nlp_metadata_list, raw_text_list, \
               rpt_text_list, xml_metadata_keys
        
    #
    def process_raw_data(self, queue, linguamatics_i2e_writer, metadata_manager,
                         raw_data_reader, process_idx, start_idx, password):
        self.linguamatics_i2e_writer = linguamatics_i2e_writer
        self.metadata_manager = metadata_manager
        self.raw_data_reader = raw_data_reader
        document_ctr = 0
        fail_ctr = 0
        document_ctr, fail_ctr = self._preprocess_documents(self.raw_data_reader,
                                                            start_idx, document_ctr,
                                                            fail_ctr, password)
        queue.put([self.linguamatics_i2e_writer, self.metadata_manager])
        print('Process ' + str(process_idx))
        print('Number documents processed: %d' % document_ctr)
        print('Number of failed documents: %d' % fail_ctr)