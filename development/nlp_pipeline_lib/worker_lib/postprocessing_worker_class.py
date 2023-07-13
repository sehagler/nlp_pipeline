# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 10:24:26 2023

@author: haglers
"""

#
import os

#
from base_lib.worker_base_class import Worker_base
from nlp_pipeline_lib.manager_lib.file_lib.json_lib.json_manager_class \
    import Json_manager

#
class Postprocessing_worker(Worker_base):
    
    #
    def __init__(self, static_data_object, output_manager):
        Worker_base.__init__(self, static_data_object)
        static_data = self.static_data_object.get_static_data()
        self.directory_manager = static_data['directory_manager']
        self.output_manager = output_manager
        
    #
    def _process_data(self, argument_dict):
        data_dict_dict = argument_dict['data_dict_dict']
        doc_list = argument_dict['doc_list']
        file_list = argument_dict['file_list']
        filename = argument_dict['filename']
        self.json_manager_registry = argument_dict['json_manager_registry']
        nlp_data_key = argument_dict['nlp_data_key']
        self.postprocessor_registry = argument_dict['postprocessor_registry']
        for filename in file_list:
            filename_base, extension = os.path.splitext(filename)
            if extension in [ '.csv' ]:
                self.postprocessor_registry.push_data_dict(filename, data_dict_dict[filename_base],
                                                           data_dict_dict['sections'],
                                                           doc_list)
        self.postprocessor_registry.run_registry()
        postprocessor_registry = \
            self.postprocessor_registry.pull_postprocessor_registry()
        for key in postprocessor_registry.keys():
            self.output_manager.append(postprocessor_registry[key])
        self.output_manager.merge_data_dict_lists()
        self.output_manager.include_metadata()
        self.output_manager.include_text()
        merged_data_dict_list = \
            self.output_manager.get_merged_data_dict_list()
        processing_base_dir = \
            self.directory_manager.pull_directory('processing_base_dir')
        data_out = \
            self.directory_manager.pull_directory('postprocessing_data_out')
        for data_dict in merged_data_dict_list:
            if nlp_data_key in data_dict.keys():
                if bool(data_dict[nlp_data_key]):
                    outdir = data_out
                    filename = data_dict['DOCUMENT_ID'] + '.json'
                    data_dict.pop('DOCUMENT_ID', None)
                    file = os.path.join(outdir, filename)
                    filename = file.replace(processing_base_dir + '/', '')
                    self.json_manager_registry[filename] = \
                        Json_manager(self.static_data_object, file)
                    self.json_manager_registry[filename].write_file(data_dict)
        return_dict = {}
        return return_dict