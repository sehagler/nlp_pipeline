# -*- coding: utf-8 -*-
"""
Created on Mon Mar 04 12:29:38 2019

@author: haglers
"""

#
from copy import deepcopy
from datetime import datetime
import os
import re

#
from tool_lib.py.processing_tools_lib.file_processing_tools \
    import read_json_file, read_nlp_data_from_package_json_file, \
           read_package_json_file, write_json_file, \
           write_nlp_data_to_package_json_file

#
class Packaging_manager(object):
    
    #
    def __init__(self, static_data_manager):
        self.static_data = static_data_manager.get_project_data()
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
        self.nlp_value_key = \
            json_structure_manager.pull_key('nlp_value_key')
            
        # to be moved to appropriate location
        json_structure_manager = self.static_data['json_structure_manager']
        self.multiple_specimens = \
            json_structure_manager.pull_key('multiple_specimens')
        self.multiple_values = \
            json_structure_manager.pull_key('multiple_values')
        #
    
    #
    def _write_performance_data(self, performance_data_filename,
                                production_json_filename, include_datetime):
        project_name = self.static_data['project_name']
        performance_statistics_dict = read_json_file(performance_data_filename)
        if production_json_filename is not None:
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
            nlp_performance_metadata['NLP_PROCESSES'] = []
            nlp_performance_metadata['NLP_PROCESSES'].append(nlp_performance_metadata['NLP_PROCESS'])
            del nlp_performance_metadata['NLP_PROCESS']
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
            nlp_performance_metadata['NLP_PROCESSES'] = \
                list(set(nlp_performance_metadata['NLP_PROCESSES']))
            nlp_performance_metadata['NOTE_TYPES'] = \
                list(set(nlp_performance_metadata['NOTE_TYPES']))
        documents_wrapper = read_package_json_file(self.static_data)
        for i in range(len(documents_wrapper[self.documents_wrapper_key])):
            nlp_data = \
                documents_wrapper[self.documents_wrapper_key][i][self.document_wrapper_key][self.nlp_data_key]
            query_list = []
            for nlp_datum in nlp_data:
                query_list.append(nlp_datum[self.nlp_datum_key][self.nlp_query_key])
            query_list = list(set(query_list))
            performance_statistics_dict_tmp = []
            for key in performance_statistics_dict.keys():
                if key in query_list:
                    tmp_dict = performance_statistics_dict[key]
                    tmp_dict['QUERY'] = key
            if production_json_filename is not None:
                documents_wrapper[self.documents_wrapper_key][i][self.document_wrapper_key][self.nlp_performance_metadata_key] = \
                    nlp_performance_metadata
            documents_wrapper[self.documents_wrapper_key][i][self.document_wrapper_key][self.nlp_performance_key] = \
                tmp_dict
        if include_datetime:
            now = datetime.now()
            datetime_str = now.strftime('_%Y%m%d_%H%M%S')
        else:
            datetime_str = ''
        write_json_file(os.path.join(self.save_dir,
                                     project_name + datetime_str + '.json'),
                        documents_wrapper)
        
    #
    def create_preperformance_test_data_json(self):
        load_dir = \
            self.directory_manager.pull_directory('postprocessing_data_out')
        data = {}
        for filename in os.listdir(load_dir):
            key = filename[0:-5]
            data[key] = \
                read_json_file(os.path.join(load_dir, filename))
        write_nlp_data_to_package_json_file(self.static_data, data)
        
    #
    def create_postperformance_production_data_json(self):
        project_name = self.static_data['project_name']
        performance_data_filename = self.save_dir
        performance_data_filename = \
            re.sub('/production$', '/test', performance_data_filename)
        performance_data_filename = \
            os.path.join(performance_data_filename, project_name + '.performance.json')
        production_json_filename = \
            os.path.join(self.save_dir, project_name + '.json')
        self._write_performance_data(performance_data_filename, 
                                     production_json_filename, True)
        
    #
    def create_postperformance_test_data_json(self):
        project_name = self.static_data['project_name']
        performance_data_filename = \
            os.path.join(self.save_dir, project_name + '.performance.json')
        self._write_performance_data(performance_data_filename, None, False)
        