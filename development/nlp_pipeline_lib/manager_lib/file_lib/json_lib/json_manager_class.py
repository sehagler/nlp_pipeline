# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 16:17:52 2021

@author: haglers
"""

#
from collections import Counter
from datetime import datetime
import os
import re
import traceback

#
from base_lib.manager_base_class import Manager_base
from tools_lib.processing_tools_lib.file_processing_tools \
    import read_json_file, write_file
    
#
class Json_manager(Manager_base):
    
    #
    def __init__(self, static_data_object, directory_object, logger_object,
                 filename):
        Manager_base.__init__(self, static_data_object, directory_object,
                              logger_object)
        self.filename = filename
        
    #
    def read_json_file(self):
        data = read_json_file(self.filename)
        return data
    
    #
    def read_nlp_data_from_package_json_file(self):
        static_data = self.static_data_object.get_static_data()
        nlp_data_tmp = read_json_file(self.filename)
        patient_identifiers = static_data['patient_identifiers']
        if 'patient_list' in static_data.keys():
            patient_list = static_data['patient_list']
        else:
            patient_list = None
        nlp_data_tmp = nlp_data_tmp[self.documents_wrapper_key]
        nlp_data = {}
        for item in nlp_data_tmp:
            for key in item[self.document_wrapper_key][self.metadata_key].keys():
                for patient_identifier in patient_identifiers:
                    if patient_identifier in key:
                        patient = \
                            item[self.document_wrapper_key][self.metadata_key][key]
            document_idx = \
                item[self.document_wrapper_key][self.nlp_metadata_key]['NLP_DOCUMENT_IDX']
            if patient_list is None or patient in patient_list:
                nlp_data[document_idx] = {}
                for key in item[self.document_wrapper_key].keys():
                    if key not in [self.nlp_data_key]:
                        nlp_data[document_idx][key] = \
                            item[self.document_wrapper_key][key]
                    else:
                        data_in = item[self.document_wrapper_key][key]
                data = {}
                for item in data_in:
                    if self.nlp_query_key in item[self.nlp_datum_key].keys():
                        nlp_query_key_tmp = \
                            item[self.nlp_datum_key][self.nlp_query_key]
                    else:
                        nlp_query_key_tmp = ''
                    if self.nlp_section_key in item[self.nlp_datum_key].keys():
                        nlp_section_key_tmp = \
                            item[self.nlp_datum_key][self.nlp_section_key]
                    else:
                        nlp_section_key_tmp = ''
                    if self.nlp_specimen_key in item[self.nlp_datum_key].keys():
                        nlp_specimen_key_tmp = \
                            item[self.nlp_datum_key][self.nlp_specimen_key]
                    else:
                        nlp_specimen_key_tmp = ''
                    key_0 = str((nlp_section_key_tmp, nlp_specimen_key_tmp))
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
                                data[key_0][nlp_query_key_tmp + '_' + key_1] = \
                                    item[self.nlp_datum_key][key_1]
                nlp_data[document_idx][self.nlp_data_key] = data
        return nlp_data
    
    #
    def read_performance_data(self):
        performance_statistics_dict = read_json_file(self.filename)
        return performance_statistics_dict
    
    #
    def write_file(self, data):
        write_file(self.filename, data, False, False)
    
    #
    def write_performance_data_to_package_json_file(self, data_in):
        documents = []
        for key_0 in data_in.keys():
            document_in = data_in[key_0]
            document = {}
            for key_1 in document_in.keys():
                if key_1 != 'RAW_TEXT':
                    if key_1 not in [self.nlp_data_key, 'PREPROCESSED_TEXT']:
                        document[key_1] = document_in[key_1]
                    elif key_1 == 'PREPROCESSED_TEXT':
                        document[self.nlp_source_text_key] = document_in[key_1]
                    else:
                        data_tmp = document_in[key_1]
            data = []
            for key_1 in data_tmp:
                for key_2 in data_tmp[key_1]:
                    data.append({ self.nlp_datum_key : data_tmp[key_1][key_2] })
            document[self.nlp_data_key] = data
            document_wrapper = {}
            document_wrapper[self.document_wrapper_key] = document
            documents.append(document_wrapper)
        documents_wrapper = {}
        documents_wrapper[self.documents_wrapper_key] = documents
        write_file(self.filename, documents_wrapper, False, False)