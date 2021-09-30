# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 10:14:44 2019

@author: haglers
"""

#
from copy import deepcopy
import datetime
import multiprocessing
import os
import pickle
import shutil
import time

#
from nlp_lib.py.dynamic_data_lib.dynamic_data_manager_class \
    import Dynamic_data_manager
from nlp_lib.py.packaging_lib.packaging_manager_class import Packaging_manager
from nlp_lib.py.process_lib.worker_lib.preprocessing_worker_class \
    import Preprocessing_worker
from nlp_lib.py.postprocessing_lib.postprocessing_manager_class \
    import Postprocessing_manager
from nlp_lib.py.raw_data_lib.raw_data_manager_class import Raw_data_manager

#
class Process_manager(object):
    
    #
    def __init__(self, static_data_manager, linguamatics_i2e_manager,
                 metadata_manager, server_manager, performance_json_manager,
                 project_json_manager, password):
        self.static_data_manager = static_data_manager
        self.linguamatics_i2e_manager = linguamatics_i2e_manager
        self.metadata_manager = metadata_manager
        self.server_manager = server_manager
        self._project_imports(static_data_manager)
        self._create_managers(static_data_manager, server_manager, 
                              performance_json_manager, project_json_manager,
                              password)
        self.password = password
        self.static_data = static_data_manager.get_static_data()
        
    #
    def _create_managers(self, static_data_manager, server_manager, 
                         performance_json_manager, project_json_manager,
                         password):
        self.dynamic_data_manager = Dynamic_data_manager()
        self.packaging_manager = Packaging_manager(static_data_manager,
                                                   performance_json_manager,
                                                   project_json_manager)
        self.postprocessing_manager = Postprocessing_manager(static_data_manager,
                                                             self.metadata_manager)
        
    #
    def _project_imports(self, static_data_manager):
        static_data = static_data_manager.get_static_data()
        project_name = static_data['project_name']
        try:
            import_cmd = 'from projects_lib.' + project_name + '.py.' + \
                         project_name.lower() + \
                         '_postprocessor_class import ' + project_name + \
                         '_postprocessor as Postprocessing_manager'
            exec(import_cmd, globals())
            print('Postprocessor: ' + project_name + '_postprocessor')
        except Exception as e:
            print(e)
        
    #
    def download_queries(self):
        query_folder = '/api;type=saved_query/__private__/' + \
                       self.static_data['user']
        destination_folder = \
            self.static_data['directory_manager'].pull_directory('sandbox_dir') + \
                '/NLP_Sandbox'
        self.linguamatics_i2e_manager.login()
        self.linguamatics_i2e_manager.folder_downloader(query_folder,
                                                        destination_folder)
        self.linguamatics_i2e_manager.logout()
    
    #
    def indexer(self):
        now = datetime.datetime.now()
        index_start_datetime = now.strftime("%d-%b-%y %H:%M:%S.%f")[:-3]
        self.metadata_manager.load_metadata()
        self.metadata_manager.append_nlp_metadata_value('DOCUMENT_SET_INDEXING_START_DATETIME',
                                                        index_start_datetime)
        self.metadata_manager.save_metadata()
        self.linguamatics_i2e_manager.login()
        self.linguamatics_i2e_manager.make_index_runner()
        self.linguamatics_i2e_manager.logout()
        now = datetime.datetime.now()
        index_end_datetime = now.strftime("%d-%b-%y %H:%M:%S.%f")[:-3]
        self.metadata_manager.load_metadata()
        self.metadata_manager.append_nlp_metadata_value('DOCUMENT_SET_INDEXING_END_DATETIME',
                                                        index_end_datetime)
        self.metadata_manager.save_metadata()
        
    #
    def postindexer(self):
        self.metadata_manager.save_metadata()
        
    #
    def postperformance(self):
        if self.static_data['project_subdir'] == 'test':
            self.packaging_manager.create_postperformance_test_data_json()
        elif self.static_data['project_subdir'] == 'production':
            self.packaging_manager.create_postperformance_production_data_json()

    #
    def postprocessor(self, cleanup_flg=True):
        if cleanup_flg:
            self.static_data['directory_manager'].cleanup_directory('postprocessing_data_out')
        self.postprocessing_manager.set_data_dirs()
        self.postprocessing_manager.import_reports()
        self.postprocessing_manager.create_json_files()
        
    #
    def preindexer(self):
        self.static_data['directory_manager'].cleanup_directory('source_data')
        self.linguamatics_i2e_manager.login()
        self.linguamatics_i2e_manager.preindexer()
        self.linguamatics_i2e_manager.logout()
        
    #
    def preperformance(self):
        self.packaging_manager.create_preperformance_test_data_json()
    
    #
    def preprocessor(self, password, start_idx, cleanup_flg,
                     preprocess_files_flg=True):
        self.preprocess_files_flg = preprocess_files_flg
        if start_idx > 0:
            cleanup_flg = False
        if cleanup_flg:
            self.static_data['directory_manager'].cleanup_directory('preprocessing_data_out')
        i2e_version = \
            self.linguamatics_i2e_manager.get_i2e_version(password)
        try:
            multiprocessing_flg = self.static_data['multiprocessing']
        except:
            multiprocessing_flg = False
        if multiprocessing_flg:
            num_processes = self.static_data['num_processes']
        else:
            num_processes = 1
        self.raw_data_manager = Raw_data_manager(self.static_data, 
                                                 self.server_manager, password)
            
        # Read data kludge to be done properly later
        operation_mode = self.static_data['operation_mode']
        pkl_file = 'raw_data_' + operation_mode + '.pkl'
        self.raw_data_manager.print_num_of_docs_in_preprocessing_set()
        pickle.dump(self.raw_data_manager, open(pkl_file, 'wb'))
        del self.raw_data_manager
        # Read data klude to be done properly later
            
        num_docs_preprocessed = 0
        queue = multiprocessing.Queue()
        processes = []
        rets = []
        for process_idx in range(num_processes):
            w = Preprocessing_worker(self.static_data_manager,
                                     self.preprocess_files_flg)
            dynamic_data_manager_copy = \
                deepcopy(self.dynamic_data_manager)
            linguamatics_i2e_manager_copy = \
                deepcopy(self.linguamatics_i2e_manager)
            metadata_manager_copy = deepcopy(self.metadata_manager)
            p = multiprocessing.Process(target=w.process_raw_data, 
                                        args=(queue,
                                              dynamic_data_manager_copy,
                                              linguamatics_i2e_manager_copy,
                                              metadata_manager_copy,
                                              num_processes, process_idx,
                                              start_idx, i2e_version, 
                                              password))
            processes.append(p)
        for p in processes:
            p.start()
        for p in processes:
            ret = queue.get()
            self.dynamic_data_manager.merge_copy(ret[0])
            self.metadata_manager.merge_copy(ret[1])
            num_docs_preprocessed += ret[2]
        for p in processes:
            p.join()
            
        # Read data kludge to be done properly later
        os.remove(pkl_file)
        # Read data kludge to be done properly later
        
        print('Number of documents preprocessed: ' + str(num_docs_preprocessed))
        if self.preprocess_files_flg:
            self.linguamatics_i2e_manager.generate_i2e_resource_files(self.dynamic_data_manager)
        self.metadata_manager.save_metadata()