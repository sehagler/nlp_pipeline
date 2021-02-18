# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 13:07:13 2021

@author: haglers
"""

#
import re

#
from nlp_lib.py.template_lib.preprocessor_template_lib.raw_report_preprocessor_class \
    import Raw_report_preprocessor
from nlp_lib.py.tool_lib.processing_tools_lib.text_processing_tools \
    import remove_repeated_substrings
from nlp_lib.py.tool_lib.processing_tools_lib.variable_processing_tools \
    import delete_key

#
class Preprocessing_worker(object):
    
    #
    def __init__(self, project_data, preprocess_files_flg):
        self.preprocess_files_flg = preprocess_files_flg
        self.project_data = project_data
        self.raw_report_preprocessor = Raw_report_preprocessor(project_data)

    #
    def _preprocess_document(self, raw_data_reader, data_tmp, 
                             start_idx, document_ctr, fail_ctr):
        do_beakerap_flg = self.project_data['do_beakerap_flg']
        try:
            multiprocessing_flg = self.project_data['flags']['multiprocessing']
        except:
            multiprocessing_flg = False
        xml_metadata_keys = self.project_data['xml_metadata_keys']
        if multiprocessing_flg:
            document_idx = data_tmp['NLP_DOCUMENT_IDX'][0]
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
                metadata_list, raw_text_list, rpt_text_list = \
                    self._read_data_wrapper(source_system, data_tmp, do_beakerap_flg)
                for i in range(len(rpt_text_list)):
                    metadata = metadata_list[i]
                    raw_text = raw_text_list[i]
                    rpt_text = rpt_text_list[i]
                    self.metadata_manager.append_metadata_dict(str(document_idx), metadata)
                    if self.preprocess_files_flg:
                        xml_metadata = {}
                        xml_metadata['DOCUMENT_ID'] = str(document_idx)
                        for key in xml_metadata_keys:
                            xml_metadata[key] = metadata[key]
                        self.raw_report_preprocessor.push_text(raw_text)
                        self.raw_report_preprocessor.normalize_report()
                        report_preprocessor = self._report_preprocessor(xml_metadata)
                        report_preprocessor.push_linguamatics_i2e_writer(self.linguamatics_i2e_writer)
                        report_preprocessor.push_text(rpt_text)
                        report_preprocessor.format_report(source_system)
                        report_preprocessor.normalize_report()
                        self.linguamatics_i2e_writer = report_preprocessor.pull_linguamatics_i2e_writer()
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
                metadata_list, raw_text_list, rpt_text_list = \
                    self._read_data_wrapper(source_system, data_tmp, do_beakerap_flg)
                metadata = metadata_list[0]
                self.metadata_manager.append_metadata_dict(str(document_ctr), metadata)
                xml_ret_val = True
            if not xml_ret_val:
                fail_ctr += 1
                print(str(document_ctr))
        return document_ctr, fail_ctr
    
    #
    def _preprocess_documents(self, raw_data_reader, start_idx, document_ctr,
                              fail_ctr):
        print('_preprocess_documents not defined')
        
    #
    def _prune_metadata(self, metadata):
        delete_key(metadata, 'RAW_TEXT')
        delete_key(metadata, 'REPORT_GROUP')
        delete_key(metadata, 'REPORT_HEADER')
        delete_key(metadata, 'REPORT_LINE')
        return metadata
        
    #
    def _read_beakerap_data(self, data_tmp):
        
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
                metadata = {}
                for key in data_tmp_tmp.keys():
                    metadata[key] = data_tmp_tmp[key][0]
                metadata = self._prune_metadata(metadata)
                
                #
                metadata_list.append(metadata)
                raw_text_list.append(raw_text)
                rpt_text_list.append(rpt_text)
                
        #
        return metadata_list, raw_text_list, rpt_text_list
    
    #
    def _read_data(self, data_tmp):
        if 'RAW_TEXT' in data_tmp.keys() and \
           data_tmp['RAW_TEXT'][0] is not None:
            raw_text = data_tmp['RAW_TEXT']
            raw_text = ''.join(raw_text)
            raw_text = remove_repeated_substrings(raw_text)
            rpt_text = raw_text
        else:
            raw_text = None
            rpt_text = None
        metadata = {}
        for key in data_tmp.keys():
            metadata[key] = data_tmp[key][0]
        metadata = self._prune_metadata(metadata)
        return [metadata], [raw_text], [rpt_text]
    
    #
    def _read_data_wrapper(self, source_system, data_tmp, do_beakerap_flg):
        if do_beakerap_flg and source_system == 'BeakderAP':
            metadata_list, raw_text_list, rpt_text_list = \
                self._read_beakerap_data(data_tmp)
        else:
            metadata_list, raw_text_list, rpt_text_list = \
                self._read_data(data_tmp)
        return metadata_list, raw_text_list, rpt_text_list
        
    #
    def process_raw_data(self, queue, linguamatics_i2e_writer, metadata_manager,
                         raw_data_reader, process_idx, start_idx):
        self.linguamatics_i2e_writer = linguamatics_i2e_writer
        self.metadata_manager = metadata_manager
        self.raw_data_reader = raw_data_reader
        document_ctr = 0
        fail_ctr = 0
        document_ctr, fail_ctr = self._preprocess_documents(self.raw_data_reader,
                                                            start_idx, document_ctr,
                                                            fail_ctr)
        queue.put([self.linguamatics_i2e_writer, self.metadata_manager])
        print('Process ' + str(process_idx))
        print('Number documents processed: %d' % document_ctr)
        print('Number of failed documents: %d' % fail_ctr)