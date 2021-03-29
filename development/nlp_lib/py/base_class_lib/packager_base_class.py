# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 13:30:29 2021

@author: haglers
"""

#
import os

#
from nlp_lib.py.tool_lib.processing_tools_lib.file_processing_tools \
    import read_json_file, write_json_file

#
class Packager_base(object):
    
    #
    def __init__(self, project_data):
        self.project_data = project_data
        self.directory_manager = project_data['directory_manager']
        self.project_name = project_data['project_name']
        self.save_dir = self.directory_manager.pull_directory('processing_data_dir')
        self.document_wrapper_key = 'DOCUMENT'
        self.documents_wrapper_key = 'DOCUMENTS'
        self.metadata_key = 'METADATA'
        self.multiple_specimens = 'MULTIPLE_SPECIMENS'
        self.multiple_values = 'MULTIPLE_VALUES'
        self.nlp_data_key = 'NLP_DATA'
        self.nlp_datetime_key = 'DATETIME'
        self.nlp_datum_key = 'NLP_ELEMENT'
        self.nlp_metadata_key = 'NLP_METADATA'
        self.nlp_performance_key = 'NLP_PERFORMANCE'
        self.nlp_query_key = 'QUERY'
        self.nlp_section_key = 'SECTION'
        self.nlp_specimen_key = 'SPECIMEN'
        self.nlp_source_text_key = 'NLP_SOURCE_TEXT'
        self.nlp_text_element_key = 'TEXT_ELEMENT_'
        self.nlp_text_key = 'TEXT'
        self.nlp_value_key = 'VALUE'
        
    #
    def _load_data_json(self, project_data):
        project_name = project_data['project_name']
        directory_manager = project_data['directory_manager']
        data_dir = directory_manager.pull_directory('processing_data_dir')
        nlp_data = \
            read_json_file(os.path.join(data_dir, project_name + '.json'))
        return nlp_data
    
    #
    def _read_nlp_data(self, project_data):
        nlp_data_tmp = self._load_data_json(project_data)
        patient_identifiers = project_data['patient_identifiers']
        patient_list = project_data['patient_list']
        nlp_data_tmp = nlp_data_tmp[self.documents_wrapper_key]
        nlp_data = {}
        for item in nlp_data_tmp:
            for patient_identifier in patient_identifiers:
                try:
                    patient = \
                        item[self.document_wrapper_key][self.metadata_key][patient_identifier]
                except:
                    pass
            document_idx = \
                item[self.document_wrapper_key][self.nlp_metadata_key]['NLP_DOCUMENT_IDX']
            if patient in patient_list:
                nlp_data[document_idx] = {}
                for key in item[self.document_wrapper_key].keys():
                    if key not in [self.nlp_data_key]:
                        nlp_data[document_idx][key] = \
                            item[self.document_wrapper_key][key]
                    else:
                        data_in = item[self.document_wrapper_key][key]
                data = {}
                for item in data_in:
                    nlp_query_key = \
                        item[self.nlp_datum_key][self.nlp_query_key]
                    nlp_section_key = \
                        item[self.nlp_datum_key][self.nlp_section_key]
                    try:
                        nlp_specimen_key = \
                            item[self.nlp_datum_key][self.nlp_specimen_key]
                    except:
                        nlp_specimen_key = ''
                    key_0 = str((nlp_section_key, nlp_specimen_key))
                    for key_1 in item[self.nlp_datum_key].keys():
                        if key_0 not in data.keys():
                            data[key_0] = {}
                        if key_1 not in [self.nlp_query_key,
                                         self.nlp_section_key,
                                         self.nlp_specimen_key]:
                            if key_1 == 'DIAGNOSIS':
                                data[key_0]['DIAGNOSIS VALUE'] = \
                                    item[self.nlp_datum_key][key_1]
                            else:
                                data[key_0][nlp_query_key + ' ' + key_1] = \
                                    item[self.nlp_datum_key][key_1]
                nlp_data[document_idx][self.nlp_data_key] = data
        return nlp_data
    
    #
    def _save_data_json(self):
        documents = []
        for key_0 in self.data.keys():
            document_in = self.data[key_0]
            document = {}
            for key_1 in document_in.keys():
                if key_1 != 'RAW_TEXT':
                    if key_1 not in [self.nlp_data_key, 'PREPROCESSED_TEXT']:
                        document[key_1] = document_in[key_1]
                    elif key_1 == 'PREPROCESSED_TEXT':
                        document[self.nlp_source_text_key] = document_in[key_1]
                    else:
                        data_in = document_in[key_1]
            data = []
            for key_1 in data_in:
                for key_2 in data_in[key_1]:
                    data.append({ self.nlp_datum_key : data_in[key_1][key_2] })
            document[self.nlp_data_key] = data
            document_wrapper = {}
            document_wrapper[self.document_wrapper_key] = document
            documents.append(document_wrapper)
        documents_wrapper = {}
        documents_wrapper[self.documents_wrapper_key] = documents
        write_json_file(os.path.join(self.save_dir, self.project_name + '.json'),
                        documents_wrapper)
        
    #
    def _write_performance_data(self, performance_statistics_list):
        documents_wrapper = self._load_data_json(self.project_data)
        for i in range(len(documents_wrapper[self.documents_wrapper_key])):
            nlp_data = \
                documents_wrapper[self.documents_wrapper_key][i][self.document_wrapper_key][self.nlp_data_key]
            query_list = []
            for nlp_datum in nlp_data:
                query_list.append(nlp_datum[self.nlp_datum_key][self.nlp_query_key])
            query_list = list(set(query_list))
            performance_statistics_list_tmp = []
            for item in performance_statistics_list:
                if item[self.nlp_query_key] in query_list:
                    performance_statistics_list_tmp.append(item)
            documents_wrapper[self.documents_wrapper_key][i][self.document_wrapper_key][self.nlp_performance_key] = \
                performance_statistics_list_tmp
        write_json_file(os.path.join(self.save_dir, self.project_name + '.json'),
                        documents_wrapper)