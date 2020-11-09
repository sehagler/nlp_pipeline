# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 10:14:44 2019

@author: haglers
"""

#
import os
import re
import shutil
import time

#
from nlp_lib.py.linguamatics_lib.linguamatics_i2e_file_manager_class \
    import Linguamatics_i2e_file_manager
from nlp_lib.py.linguamatics_lib.linguamatics_i2e_writer_class \
    import Linguamatics_i2e_writer
from nlp_lib.py.manager_lib.directory_manager_class import Directory_manager
from nlp_lib.py.manager_lib.metadata_manager_class import Metadata_manager
from nlp_lib.py.manager_lib.server_manager_class import Server_manager
from nlp_lib.py.packager_lib.packager_class import Packager
from nlp_lib.py.reader_lib.raw_data_reader_class import Raw_data_reader
from nlp_lib.py.template_lib.preprocessor_template_lib.raw_report_preprocessor_class \
    import Raw_report_preprocessor
from nlp_lib.py.tool_lib.processing_tools_lib.text_processing_tools \
    import remove_repeated_substrings
from nlp_lib.py.tool_lib.processing_tools_lib.variable_processing_tools \
    import delete_key

#
class Process_manager(object):
    
    #
    def __init__(self, project_data, password):
        self.project_data = project_data
        self.server = self.project_data['acc_server']
        from nlp_lib.py.linguamatics_lib.linguamatics_i2e_client_manager_class \
            import Linguamatics_i2e_client_manager
        self.linguamatics_i2e_client_manager = \
            Linguamatics_i2e_client_manager(self.project_data, password)
        self.linguamatics_i2e_file_manager = \
            Linguamatics_i2e_file_manager(self.project_data)
        self.linguamatics_i2e_writer = \
            Linguamatics_i2e_writer(self.linguamatics_i2e_file_manager)
        self.metadata_manager = self.project_data['metadata_manager']
        self.project_name = self.project_data['project_name']
        self.raw_data_reader = Raw_data_reader(self.project_data, password)
        self.raw_report_preprocessor = Raw_report_preprocessor()
        self.report_postprocessor = self.project_data['report_postprocessor']
        self.report_postprocessor.set_credentials(self.project_data, password)
        self.report_postprocessor.set_data_dirs(self.project_data)
        self.server_manager = Server_manager(self.project_data, password)

    #
    def _preprocess_document(self, raw_data_reader, do_beakerap_flg, data_tmp, 
                             start_idx, patient_identifier_list, xml_metadata_keys,
                             document_ctr, fail_ctr):
        patient_identifier = None
        for key in self.project_data['patient_identifiers']:
            try:
                patient_identifier = list(set(data_tmp[key]))
            except:
                pass
        if patient_identifier is None:
            print(data_tmp)
        if len(patient_identifier) < 2:
            if patient_identifier_list is not None:
                if patient_identifier[0] in patient_identifier_list:
                    do_analysis_flg = True
                else:
                    do_analysis_flg = False
            else:
                do_analysis_flg = True
            if do_analysis_flg:
                document_ctr += 1
                if document_ctr >= start_idx:
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
                            self.metadata_manager.append_metadata_dict(str(document_ctr), metadata)
                            if self.preprocess_files_flg:
                                xml_metadata = {}
                                xml_metadata['DOCUMENT_ID'] = str(document_ctr)
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
                                    self.linguamatics_i2e_writer.generate_xml_file(document_ctr, xml_metadata,
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
    def _preprocess_documents(self, raw_data_reader, start_idx, patient_list, xml_metadata_keys, 
                              document_ctr, fail_ctr, do_beakerap_flg):
        print('_preprocess_documents not defined')
    
    #
    def _preprocessor_document_set(self, raw_data_files_dict, raw_data_files_seq,
                                   start_idx, patient_list, xml_metadata_keys,
                                   document_ctr, fail_ctr, do_beakerap_flg):
        if raw_data_files_seq is None:
            raw_data_files_seq = list(raw_data_files_dict.keys())
        raw_data_files = []
        for i in range(len(raw_data_files_seq)):
            raw_data_files.append(os.path.join(self.project_data['directory_manager'].pull_directory('raw_data_dir'),
                                               raw_data_files_seq[i]))
        self.raw_data_reader.read_data(raw_data_files_dict, raw_data_files)
        document_ctr, fail_ctr = self._preprocess_documents(self.raw_data_reader, start_idx, 
                                                            patient_list, xml_metadata_keys,
                                                            document_ctr, fail_ctr,
                                                            do_beakerap_flg)
        return document_ctr, fail_ctr
    
    #
    def _preprocessor_document_sets(self, start_idx, patient_list,
                                    xml_metadata_keys, do_beakerap_flg):
        raw_data_files_dict = self.project_data['raw_data_files']
        if 'raw_data_files_sequence' in self.project_data.keys():
            raw_data_files_seq = self.project_data['raw_data_files_sequence']
        else:
            raw_data_files_seq = None
        document_ctr = 0
        fail_ctr = 0
        document_ctr, fail_ctr = \
                self._preprocessor_document_set(raw_data_files_dict, raw_data_files_seq,
                                                start_idx, patient_list, xml_metadata_keys, 
                                                document_ctr, fail_ctr, do_beakerap_flg)
        return document_ctr, fail_ctr
        
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
    def _report_preprocessor(self, xml_metadata):
        print('_report_preprocessor not defined')
    
    #
    def indexer(self):
        keywords_tmp_file = '/tmp/keywords_default.txt'
        if self.project_data['root_dir_flg'] in ''.join([ 'X', 'Z' ]):
            self.linguamatics_i2e_writer.prepare_keywords_file_ssh(keywords_tmp_file)
        elif self.project_data['root_dir_flg'] in ''.join([ 'dev_server', 'prod_server' ]):
            self.linguamatics_i2e_writer.prepare_keywords_file(keywords_tmp_file)
        for resource_type in self.linguamatics_i2e_file_manager.resource_files_keys():
            try:
                self.linguamatics_i2e_client_manager.delete_resource(self.linguamatics_i2e_file_manager.i2e_resource(resource_type))
            except Exception as e:
                print(e)
            if resource_type == 'source_data':
                data_dir = self.linguamatics_i2e_file_manager.source_data_directory()
                for source_data_file in sorted(os.listdir(data_dir)):
                    try:
                        self.linguamatics_i2e_client_manager.create_resource(self.project_name, resource_type,
                                                                             os.path.join(data_dir, source_data_file))
                    except Exception as e:
                        print(e)
            else:
                try:
                    self.linguamatics_i2e_client_manager.create_resource(None, resource_type,
                                                                         self.linguamatics_i2e_file_manager.resource_file(resource_type))
                except Exception as e:
                    print(e)
        self.linguamatics_i2e_client_manager.make_index_runner(self.linguamatics_i2e_file_manager.i2e_resource('index_template'),
                                                               self.project_name)
    
    #
    def packager(self):
        self.packager = Packager(self.project_data)
        
    #
    def postindexer(self):
        for bundle_type in self.linguamatics_i2e_file_manager.bundles_keys():
            try:
                self.linguamatics_i2e_client_manager.upload_bundle(self.linguamatics_i2e_file_manager.bundle(bundle_type))
            except Exception as e:
                print(e)

    #
    def postprocessor(self, cleanup_flg=True):
        if cleanup_flg:
            self.project_data['directory_manager'].cleanup_directory('postprocessing_data_out')
        self.report_postprocessor.import_reports(self.project_data)
        self.report_postprocessor.create_json_files()
        
    #
    def preindexer(self, start_idx, cleanup_flg):
        if start_idx > 0:
            cleanup_flg = False
        if cleanup_flg:
            self.project_data['directory_manager'].cleanup_directory('source_data')
        self.linguamatics_i2e_writer.generate_query_bundle_file(self.project_name)
        self.linguamatics_i2e_writer.generate_source_data_file(self.project_name, start_idx)
    
    #
    def preprocessor(self, start_idx, cleanup_flg, preprocess_files_flg=True):
        self.preprocess_files_flg = preprocess_files_flg
        if start_idx > 1:
            cleanup_flg = False
        do_beakerap_flg = self.project_data['do_beakerap_flg']
        if 'patient_list' in self.project_data:
            patient_list = self.project_data['patient_list']
        else:
            patient_list = None
        xml_metadata_keys = self.project_data['xml_metadata_keys']
        if cleanup_flg:
            self.project_data['directory_manager'].cleanup_directory('preprocessing_data_out')
        document_ctr, fail_ctr = \
            self._preprocessor_document_sets(start_idx, patient_list,
                                             xml_metadata_keys, do_beakerap_flg)
        self.metadata_manager.save_metadata()
        if self.preprocess_files_flg:
            self.linguamatics_i2e_writer.generate_keywords_file()
            self.linguamatics_i2e_writer.generate_regions_file()
            self.linguamatics_i2e_writer.generate_xml_configuation_file()
        print('Number documents processed: %d' % document_ctr)
        print('Number of failed documents: %d' % fail_ctr)