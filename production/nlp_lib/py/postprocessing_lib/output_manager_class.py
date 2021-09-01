# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 14:28:32 2018

@author: haglers
"""

#
import glob
import os
import urllib3

#
from tool_lib.py.processing_tools_lib.file_processing_tools \
    import read_xml_file, write_file

#
urllib3.disable_warnings()

#
class Output_manager(object):

    #
    def __init__(self, static_data, metadata_manager):
        json_structure_manager = static_data['json_structure_manager']
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
        self.multiple_specimens = \
            json_structure_manager.pull_key('multiple_specimens')
        self.multiple_values = \
            json_structure_manager.pull_key('multiple_values')
        #
    
        self.project_name = static_data['project_name']
        self.metadata_manager = metadata_manager
        self.merged_data_dict_list = []
        self.data_dict_classes_list = []

    #
    def _get_data_dict_lists(self):
        data_dict_lists = []
        for data_dict_class in self.data_dict_classes_list:
            data_dict_lists.append(data_dict_class.get_data_dict_list())
        return data_dict_lists

    #
    def _get_data_dict_base_keys_list(self):
        data_dict_base_keys = []
        for data_dict_class in self.data_dict_classes_list:
            data_dict_base_keys.append(data_dict_class.get_data_dict_base_keys_list())
        return data_dict_base_keys

    #
    def _get_document_ids(self):
        document_ids = []
        data_dict_lists = self._get_data_dict_lists()
        data_dict_base_keys = self._get_data_dict_base_keys_list()
        for i in range(len(data_dict_lists)):
            data_dict_list = data_dict_lists[i]
            for data_dict in data_dict_list:
                keys = data_dict.keys()
                if len(keys) > len(data_dict_base_keys[i]):
                    document_ids.append(data_dict['DOCUMENT_ID'])
        document_ids = sorted(list(set(document_ids)))
        return document_ids

    #
    def _merge_two_dicts(self, x, y):
        z = x.copy()
        z.update(y)
        return z
    
    #
    def append(self, data_dict):
        self.data_dict_classes_list.append(data_dict)
        
    #
    def cleanup_json_files_dir(self):
        outdir = self.data_out + '/' + self.project_name
        file_list = glob.glob(os.path.join(outdir, '*.json'))
        for f in file_list:
            os.remove(f)

    #
    def create_json_files(self):
        for data_dict in self.merged_data_dict_list:
            if self.nlp_data_key in data_dict.keys():
                if bool(data_dict[self.nlp_data_key]):
                    outdir = self.data_out
                    filename = data_dict['DOCUMENT_ID'] + '.json'
                    data_dict.pop('DOCUMENT_ID', None)
                    write_file(os.path.join(outdir, filename), data_dict,
                                    False, False)
    
    #
    def get_data(self):
        return self.merged_data_dict_list
    
    #
    def include_metadata(self):
        self.metadata_manager.load_metadata()
        self.metadata_dict_dict, self.metadata_keys = self.metadata_manager.read_metadata()
        for i in range(len(self.merged_data_dict_list)):
            document_id = self.merged_data_dict_list[i]['DOCUMENT_ID']
            self.merged_data_dict_list[i][self.metadata_key] = \
                self.metadata_dict_dict[document_id][self.metadata_key]
            self.merged_data_dict_list[i][self.nlp_metadata_key] = \
                self.metadata_dict_dict[document_id][self.nlp_metadata_key]
    
    #
    def include_text(self):
        for i in range(len(self.merged_data_dict_list)):
            document_id = self.merged_data_dict_list[i]['DOCUMENT_ID']
            filename = os.path.join(self.preprocessing_data_out, document_id + '.xml')
            tree = read_xml_file(filename)
            raw_text = tree.find('RAW_TEXT')
            self.merged_data_dict_list[i]['RAW_TEXT'] = raw_text.text
            rpt_text = tree.find('rpt_text')
            self.merged_data_dict_list[i]['PREPROCESSED_TEXT'] = rpt_text.text
    
    #
    def merge_data_dict_lists(self):
        merged_data_dict_list = []
        document_ids = self._get_document_ids()
        for document_id in document_ids:
            merged_dict = {}
            merged_dict['DOCUMENT_ID'] = document_id
            merged_dict[self.nlp_data_key] = {}
            for data_dict_class in self.data_dict_classes_list:
                data_dict_list = data_dict_class.get_data_dict_list()
                for data_dict in data_dict_list:
                    if data_dict['DOCUMENT_ID'] == document_id:
                        data_keys_x = data_dict[self.nlp_data_key].keys()
                        for data_key in data_keys_x:
                            if str(data_key) not in merged_dict[self.nlp_data_key].keys():
                                merged_dict[self.nlp_data_key][str(data_key)] = {}
                            merged_dict[self.nlp_data_key][str(data_key)] = \
                                self._merge_two_dicts(merged_dict[self.nlp_data_key][str(data_key)],
                                                      data_dict[self.nlp_data_key][data_key])
            merged_data_dict_list.append(merged_dict)
        self.merged_data_dict_list = merged_data_dict_list
        
    #
    def set_data_dirs(self, directory_manager):
        self.preprocessing_data_out = \
            directory_manager.pull_directory('preprocessing_data_out')
        self.data_out = directory_manager.pull_directory('postprocessing_data_out')