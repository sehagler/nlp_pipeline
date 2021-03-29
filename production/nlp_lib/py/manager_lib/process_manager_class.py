# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 10:14:44 2019

@author: haglers
"""

#
from copy import deepcopy
import multiprocessing
import os
import shutil
import time

#
from nlp_lib.py.linguamatics_lib.linguamatics_i2e_client_manager_class \
    import Linguamatics_i2e_client_manager
from nlp_lib.py.linguamatics_lib.linguamatics_i2e_file_manager_class \
    import Linguamatics_i2e_file_manager
from nlp_lib.py.linguamatics_lib.linguamatics_i2e_writer_class \
    import Linguamatics_i2e_writer
from nlp_lib.py.manager_lib.directory_manager_class import Directory_manager
from nlp_lib.py.manager_lib.metadata_manager_class import Metadata_manager
from nlp_lib.py.manager_lib.server_manager_class import Server_manager
from nlp_lib.py.packager_lib.packager_class import Packager
from nlp_lib.py.reader_lib.raw_data_reader_class import Raw_data_reader

#
class Process_manager(object):
    
    #
    def __init__(self, project_data, password):
        self.password = password
        project_name = project_data['project_name']
        import_cmd = 'from projects_lib.' + project_name + '.py.' + \
                      project_name.lower() + \
                     '_preprocessing_worker_class import ' + project_name + \
                     '_preprocessing_worker as Preprocessing_worker'
        exec(import_cmd, globals())
        self.project_data = project_data
        self.server = self.project_data['acc_server']
        self.linguamatics_i2e_client_manager = \
            Linguamatics_i2e_client_manager(self.project_data, password)
        self.linguamatics_i2e_file_manager = \
            Linguamatics_i2e_file_manager(self.project_data)
        self.linguamatics_i2e_writer = \
            Linguamatics_i2e_writer(self.project_data, 
                                    self.linguamatics_i2e_file_manager,
                                    password)
        self.metadata_manager = self.project_data['metadata_manager']
        self.project_name = self.project_data['project_name']
        self.raw_data_reader = Raw_data_reader(self.project_data, password)
        self.report_postprocessor = self.project_data['report_postprocessor']
        self.report_postprocessor.set_data_dirs(self.project_data)
        self.server_manager = Server_manager(self.project_data, password)
    
    #
    def _read_raw_data(self):
        raw_data_files_dict = self.project_data['raw_data_files']
        if 'raw_data_files_sequence' in self.project_data.keys():
            raw_data_files_seq = self.project_data['raw_data_files_sequence']
        else:
            raw_data_files_seq = None
        if raw_data_files_seq is None:
            raw_data_files_seq = list(raw_data_files_dict.keys())
        raw_data_files = []
        for i in range(len(raw_data_files_seq)):
            raw_data_files.append(os.path.join(self.project_data['directory_manager'].pull_directory('raw_data_dir'),
                                               raw_data_files_seq[i]))
        self.raw_data_reader.read_data(raw_data_files_dict, raw_data_files)
        
    #
    def download_queries(self):
        query_folder = '/api;type=saved_query/__private__/' + \
                       self.project_data['user']
        destination_folder = \
            self.project_data['directory_manager'].pull_directory('sandbox_dir') + \
                '/NLP_Sandbox'
        self.linguamatics_i2e_client_manager.folder_downloader(query_folder,
                                                               destination_folder)
    
    #
    def indexer(self):
        keywords_tmp_file = '/tmp/keywords_default.txt'
        if self.project_data['root_dir_flg'] in ''.join([ 'X', 'Z' ]):
            self.linguamatics_i2e_writer.prepare_keywords_file_ssh(keywords_tmp_file)
        elif self.project_data['root_dir_flg'] in ''.join([ 'dev_server', 'prod_server' ]):
            self.linguamatics_i2e_writer.prepare_keywords_file(keywords_tmp_file)
        self.linguamatics_i2e_client_manager.login()
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
        for bundle_type in self.linguamatics_i2e_file_manager.bundles_keys():
            try:
                self.linguamatics_i2e_client_manager.upload_bundle(self.linguamatics_i2e_file_manager.bundle(bundle_type))
            except Exception as e:
                print(e)
        self.linguamatics_i2e_client_manager.make_index_runner(self.linguamatics_i2e_file_manager.i2e_resource('index_template'),
                                                               self.project_name)
        self.linguamatics_i2e_client_manager.logout()
    
    #
    def packager(self):
        self.packager = Packager(self.project_data)
        
    #
    def postindexer(self):
        pass

    #
    def postprocessor(self, cleanup_flg=True):
        if cleanup_flg:
            self.project_data['directory_manager'].cleanup_directory('postprocessing_data_out')
        self.report_postprocessor.import_reports(self.project_data)
        self.report_postprocessor.create_json_files()
        
    #
    def preindexer(self):
        self.project_data['directory_manager'].cleanup_directory('source_data')
        self.linguamatics_i2e_writer.generate_source_data_file(self.project_name)
    
    #
    def preprocessor(self, password, start_idx, cleanup_flg,
                     preprocess_files_flg=True):
        self.preprocess_files_flg = preprocess_files_flg
        if start_idx > 0:
            cleanup_flg = False
        if cleanup_flg:
            self.project_data['directory_manager'].cleanup_directory('preprocessing_data_out')
        self._read_raw_data()
        try:
            multiprocessing_flg = self.project_data['flags']['multiprocessing']
        except:
            multiprocessing_flg = False
        if multiprocessing_flg:
            num_processes = self.project_data['num_processes']
        else:
            num_processes = 1
        queue = multiprocessing.Queue()
        processes = []
        rets = []
        for process_idx in range(num_processes):
            w = Preprocessing_worker(self.project_data,
                                     self.preprocess_files_flg)
            linguamatics_i2e_writer_copy = \
                deepcopy(self.linguamatics_i2e_writer)
            metadata_manager_copy = deepcopy(self.metadata_manager)
            raw_data_reader_copy = deepcopy(self.raw_data_reader)
            raw_data_reader_copy.select_process(process_idx)
            p = multiprocessing.Process(target=w.process_raw_data, 
                                        args=(queue, 
                                              linguamatics_i2e_writer_copy,
                                              metadata_manager_copy,
                                              raw_data_reader_copy,
                                              process_idx, start_idx,
                                              password))
            processes.append(p)
        for p in processes:
            p.start()
        for p in processes:
            ret = queue.get()
            self.linguamatics_i2e_writer.merge_copy(ret[0])
            self.metadata_manager.merge_copy(ret[1])
        for p in processes:
            p.join()
        self.metadata_manager.save_metadata()
        if self.preprocess_files_flg:
            self.linguamatics_i2e_writer.generate_keywords_file()
            self.linguamatics_i2e_writer.generate_query_bundle_file(self.project_name)
            self.linguamatics_i2e_writer.generate_regions_file()
            self.linguamatics_i2e_writer.generate_xml_configuation_file()