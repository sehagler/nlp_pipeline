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

#
from tool_lib.py.processing_tools_lib.file_processing_tools \
    import read_json_file, write_file
    
#
class Json_manager(object):
    
    #
    def __init__(self, static_data_manager, filename):
        self.filename = filename
        self.static_data = static_data_manager.get_static_data()
        self.directory_manager = self.static_data['directory_manager']
        self.save_dir = \
            self.directory_manager.pull_directory('processing_data_dir')
        
        json_structure_manager = self.static_data['json_structure_manager']
        self.document_wrapper_key = \
            json_structure_manager.pull_key('document_wrapper_key')
        self.documents_wrapper_key = \
            json_structure_manager.pull_key('documents_wrapper_key')
        self.metadata_key = \
            json_structure_manager.pull_key('metadata_key')
        self.nlp_data_key = \
            json_structure_manager.pull_key('nlp_data_key')
        self.nlp_datetime_key = \
            json_structure_manager.pull_key('nlp_datetime_key')
        self.nlp_datum_key = \
            json_structure_manager.pull_key('nlp_datum_key')
        self.nlp_metadata_key = \
            json_structure_manager.pull_key('nlp_metadata_key')
        self.nlp_performance_key = \
            json_structure_manager.pull_key('nlp_performance_key')
        self.nlp_performance_metadata_key = \
            json_structure_manager.pull_key('nlp_performance_metadata_key')
        self.nlp_query_key = \
            json_structure_manager.pull_key('nlp_query_key')
        self.nlp_section_key = \
            json_structure_manager.pull_key('nlp_section_key')
        self.nlp_specimen_key = \
            json_structure_manager.pull_key('nlp_specimen_key')
        self.nlp_source_text_key = \
            json_structure_manager.pull_key('nlp_source_text_key')
        self.nlp_text_element_key = \
            json_structure_manager.pull_key('nlp_text_element_key')
        self.nlp_text_key = \
            json_structure_manager.pull_key('nlp_text_key')
        self.nlp_tool_output_key = \
            json_structure_manager.pull_key('nlp_tool_output_key')
        self.nlp_value_key = \
            json_structure_manager.pull_key('nlp_value_key')
            
        # to be moved to appropriate location
        self.manual_review = \
            json_structure_manager.pull_key('manual_review')
        #
        
        self.project_name = self.static_data['project_name']
        
    #
    def _trim_data(self, documents_wrapper_in):
        document_wrappers_in = \
            documents_wrapper_in[self.documents_wrapper_key]
        document_wrappers = []
        for document_wrapper in document_wrappers_in:
            document = document_wrapper[self.document_wrapper_key]
            nlp_data = document[self.nlp_data_key]
            delete_idxs = []
            for i in range(len(nlp_data)):
                section_i = \
                    nlp_data[i][self.nlp_datum_key][self.nlp_section_key]
                section_i_lbl = re.sub(' \d+', '', section_i)
                try:
                    section_i_num = int(re.sub('[A-Z ]*', '', section_i))
                except:
                    section_i_num = None
                nlp_output_i = \
                    nlp_data[i][self.nlp_datum_key][self.nlp_value_key]
                if section_i_num is not None:
                    for item_i in nlp_output_i:
                        keys_i = list(item_i.keys())
                        keys_i.remove('CONTEXT')
                        for j in range(len(nlp_data)-i-1):
                            section_j = \
                                nlp_data[i+j+1][self.nlp_datum_key][self.nlp_section_key]
                            section_j_lbl = re.sub(' \d+', '', section_j)
                            try:
                                section_j_num = int(re.sub('[A-Z ]*', '', section_j))
                            except:
                                section_j_num = None
                            nlp_output_j = \
                                nlp_data[i+j+1][self.nlp_datum_key][self.nlp_value_key]
                            if section_j_num is not None and \
                               ( section_i_lbl == section_j_lbl ) and \
                               ( section_i_num <= section_j_num ):
                                for item_j in nlp_output_j:
                                    keys_j = list(item_j.keys())
                                    keys_j.remove('CONTEXT')
                                    if Counter(keys_i) == Counter(keys_j):
                                        delete_key = True
                                        for key in keys_i:
                                            if item_i[key] != item_j[key]:
                                                delete_key = False
                                        if delete_key:
                                            delete_idxs.append(i+j+1)
            delete_idxs = list(set(delete_idxs))
            delete_idxs.sort(reverse=True)
            for i in range(len(delete_idxs)):
                del nlp_data[delete_idxs[i]]
            document[self.nlp_data_key] = nlp_data
            document_wrapper = {}
            document_wrapper[self.document_wrapper_key] = \
                document
            document_wrappers.append(document_wrapper)
        documents_wrapper = {}
        documents_wrapper[self.documents_wrapper_key] = \
            document_wrappers
        return documents_wrapper
        
    #
    def read_json_file(self):
        data = read_json_file(self.filename)
        return data
    
    #
    def read_nlp_data_from_package_json_file(self):
        static_data = self.static_data
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
    def write_performance_data_0(self, performance_statistics_dict,
                                 include_datetime_flg, multiple_files_flg):
        project_json_filename = self.filename
        production_json_filename = project_json_filename
        production_json = read_json_file(production_json_filename)
        nlp_performance_metadata = \
            production_json[self.documents_wrapper_key][0][self.document_wrapper_key][self.nlp_metadata_key]
        nlp_performance_metadata['DOCUMENT_PREPROCESSING_END_DATETIMES'] = []
        nlp_performance_metadata['DOCUMENT_PREPROCESSING_END_DATETIMES'].append(nlp_performance_metadata['DOCUMENT_PREPROCESSING_END_DATETIME'])
        del nlp_performance_metadata['DOCUMENT_PREPROCESSING_END_DATETIME']
        nlp_performance_metadata['DOCUMENT_PREPROCESSING_START_DATETIMES'] = []
        nlp_performance_metadata['DOCUMENT_PREPROCESSING_START_DATETIMES'].append(nlp_performance_metadata['DOCUMENT_PREPROCESSING_START_DATETIME'])
        del nlp_performance_metadata['DOCUMENT_PREPROCESSING_START_DATETIME']
        nlp_performance_metadata['FILENAMES'] = []
        nlp_performance_metadata['FILENAMES'].append(nlp_performance_metadata['FILENAME'])
        del nlp_performance_metadata['FILENAME']
        del nlp_performance_metadata['NLP_DOCUMENT_IDX']
        nlp_performance_metadata['NLP_MODES'] = []
        nlp_performance_metadata['NLP_MODES'].append(nlp_performance_metadata['NLP_MODE'])
        del nlp_performance_metadata['NLP_MODE']
        nlp_performance_metadata['NOTE_TYPES'] = []
        nlp_performance_metadata['NOTE_TYPES'].append(nlp_performance_metadata['NOTE_TYPE'])
        del nlp_performance_metadata['NOTE_TYPE']
        del nlp_performance_metadata['PREPROCESSING_PROCESSOR_IDX']
        for i in range(len(production_json[self.documents_wrapper_key])-1):
            nlp_performance_metadata_tmp = production_json[self.documents_wrapper_key][i+1][self.document_wrapper_key][self.nlp_metadata_key]
            nlp_performance_metadata['DOCUMENT_PREPROCESSING_END_DATETIMES'].append(nlp_performance_metadata_tmp['DOCUMENT_PREPROCESSING_END_DATETIME'])
            nlp_performance_metadata['DOCUMENT_PREPROCESSING_START_DATETIMES'].append(nlp_performance_metadata_tmp['DOCUMENT_PREPROCESSING_START_DATETIME'])
            nlp_performance_metadata['FILENAMES'].append(nlp_performance_metadata_tmp['FILENAME'])
            if 'NOTE_TYPE' in nlp_performance_metadata_tmp.keys():
                nlp_performance_metadata['NOTE_TYPES'].append(nlp_performance_metadata_tmp['NOTE_TYPE'])
        datetime_list = [ datetime.strptime(date, '%d-%b-%y %H:%M:%S.%f') for date in nlp_performance_metadata['DOCUMENT_PREPROCESSING_END_DATETIMES'] ]
        end_datetime = max(datetime_list)
        nlp_performance_metadata['DOCUMENT_SET_PREPROCESSING_END_DATETIME'] = \
            end_datetime.strftime('%d-%b-%y %H:%M:%S.%f')[:-3]
        del nlp_performance_metadata['DOCUMENT_PREPROCESSING_END_DATETIMES']
        datetime_list = [ datetime.strptime(date, '%d-%b-%y %H:%M:%S.%f') for date in nlp_performance_metadata['DOCUMENT_PREPROCESSING_START_DATETIMES'] ]
        start_datetime = min(datetime_list)
        nlp_performance_metadata['DOCUMENT_SET_PREPROCESSING_START_DATETIME'] = \
            start_datetime.strftime('%d-%b-%y %H:%M:%S.%f')[:-3]
        del nlp_performance_metadata['DOCUMENT_PREPROCESSING_START_DATETIMES']
        nlp_performance_metadata['FILENAMES'] = \
            list(set(nlp_performance_metadata['FILENAMES']))
        nlp_performance_metadata['NLP_MODES'] = \
            list(set(nlp_performance_metadata['NLP_MODES']))
        nlp_performance_metadata['NOTE_TYPES'] = \
            list(set(nlp_performance_metadata['NOTE_TYPES']))
                
        documents_wrapper = read_json_file(project_json_filename)
        documents_wrapper = self._trim_data(documents_wrapper)
        for i in range(len(documents_wrapper[self.documents_wrapper_key])):
            nlp_data = \
                documents_wrapper[self.documents_wrapper_key][i][self.document_wrapper_key][self.nlp_data_key]
            query_list = []
            for nlp_datum in nlp_data:
                query_list.append(nlp_datum[self.nlp_datum_key][self.nlp_query_key])
            query_list = list(set(query_list))
            performance_statistics_dict_tmp = []
            tmp_dict = {}
            for key in performance_statistics_dict.keys():
                if key in query_list:
                    tmp_dict = performance_statistics_dict[key]
                    tmp_dict['QUERY'] = key
                    performance_statistics_dict_tmp.append(tmp_dict)
            if tmp_dict:
                documents_wrapper[self.documents_wrapper_key][i][self.document_wrapper_key][self.nlp_performance_metadata_key] = \
                    nlp_performance_metadata
                documents_wrapper[self.documents_wrapper_key][i][self.document_wrapper_key][self.nlp_performance_key] = \
                    tmp_dict
        else:
            datetime_str = ''
        write_file(self.filename, documents_wrapper, include_datetime_flg,
                   multiple_files_flg)
    
    #
    def write_performance_data_1(self, performance_statistics_dict,
                                 include_datetime_flg, multiple_files_flg):
        project_json_filename = self.filename
        documents_wrapper = read_json_file(project_json_filename)
        for i in range(len(documents_wrapper[self.documents_wrapper_key])):
            nlp_data = \
                documents_wrapper[self.documents_wrapper_key][i][self.document_wrapper_key][self.nlp_data_key]
            query_list = []
            for nlp_datum in nlp_data:
                if self.nlp_query_key in nlp_datum[self.nlp_datum_key].keys():
                    query_list.append(nlp_datum[self.nlp_datum_key][self.nlp_query_key])
            query_list = list(set(query_list))
            performance_statistics_dict_tmp = []
            tmp_dict = {}
            for key in performance_statistics_dict.keys():
                if key in query_list:
                    tmp_dict = performance_statistics_dict[key]
                    tmp_dict['QUERY'] = key
            if tmp_dict:    
                documents_wrapper[self.documents_wrapper_key][i][self.document_wrapper_key][self.nlp_performance_key] = \
                    tmp_dict
        else:
            datetime_str = ''
        write_file(self.filename, documents_wrapper, include_datetime_flg,
                   multiple_files_flg)
    
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