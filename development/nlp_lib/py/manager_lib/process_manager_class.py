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
from linguamatics_i2e_lib.py.linguamatics_i2e_manager_class \
    import Linguamatics_i2e_manager
from nlp_lib.py.manager_lib.directory_manager_class import Directory_manager
from nlp_lib.py.manager_lib.dynamic_data_manager_class \
    import Dynamic_data_manager
from nlp_lib.py.manager_lib.metadata_manager_class import Metadata_manager
from nlp_lib.py.manager_lib.server_manager_class import Server_manager
from nlp_lib.py.packager_lib.packager_class import Packager
from nlp_lib.py.raw_data_lib.raw_data_manager_class import Raw_data_manager

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
        self.dynamic_data_manager = Dynamic_data_manager()
        self.linguamatics_i2e_manager = \
            Linguamatics_i2e_manager(self.project_data, password)
        self.metadata_manager = self.project_data['metadata_manager']
        self.project_name = self.project_data['project_name']
        self.report_postprocessor = self.project_data['report_postprocessor']
        self.report_postprocessor.set_data_dirs(self.project_data)
        self.server_manager = Server_manager(self.project_data, password)
        
    #
    def download_queries(self):
        query_folder = '/api;type=saved_query/__private__/' + \
                       self.project_data['user']
        destination_folder = \
            self.project_data['directory_manager'].pull_directory('sandbox_dir') + \
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
    def packager(self):
        self.packager = Packager(self.project_data)
        
    #
    def postindexer(self):
        self.metadata_manager.save_metadata()

    #
    def postprocessor(self, cleanup_flg=True):
        if cleanup_flg:
            self.project_data['directory_manager'].cleanup_directory('postprocessing_data_out')
        self.report_postprocessor.import_reports(self.project_data)
        self.report_postprocessor.create_json_files()
        
    #
    def preindexer(self):
        self.project_data['directory_manager'].cleanup_directory('source_data')
        self.linguamatics_i2e_manager.login()
        self.linguamatics_i2e_manager.preindexer()
        self.linguamatics_i2e_manager.logout()
    
    #
    def preprocessor(self, password, start_idx, cleanup_flg,
                     preprocess_files_flg=True):
        self.preprocess_files_flg = preprocess_files_flg
        if start_idx > 0:
            cleanup_flg = False
        if cleanup_flg:
            self.project_data['directory_manager'].cleanup_directory('preprocessing_data_out')
        i2e_version = \
            self.linguamatics_i2e_manager.get_i2e_version(password)
        try:
            multiprocessing_flg = self.project_data['flags']['multiprocessing']
        except:
            multiprocessing_flg = False
        if multiprocessing_flg:
            num_processes = self.project_data['num_processes']
        else:
            num_processes = 1
        self.raw_data_manager = Raw_data_manager(self.project_data, password)
            
        # Read data kludge to be done properly later
        self.raw_data_manager.print_num_of_docs_in_preprocessing_set()
        pickle.dump(self.raw_data_manager, open('raw_data.pkl', 'wb'))
        del self.raw_data_manager
        # Read data klude to be done properly later
            
        num_docs_preprocessed = 0
        queue = multiprocessing.Queue()
        processes = []
        rets = []
        for process_idx in range(num_processes):
            w = Preprocessing_worker(self.project_data,
                                     self.preprocess_files_flg, password)
            dynamic_data_manager_copy = \
                deepcopy(self.dynamic_data_manager)
            metadata_manager_copy = deepcopy(self.metadata_manager)
            p = multiprocessing.Process(target=w.process_raw_data, 
                                        args=(queue,
                                              dynamic_data_manager_copy,
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
        os.remove('raw_data.pkl')
        # Read data kludge to be done properly later
        
        print('Number of documents preprocessed: ' + str(num_docs_preprocessed))
        if self.preprocess_files_flg:
            self.linguamatics_i2e_manager.generate_i2e_resource_files(self.dynamic_data_manager)
        self.metadata_manager.save_metadata()