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
import re
import shutil
import time

#
from linguamatics_i2e_lib.py.linguamatics_i2e_manager_class \
    import Linguamatics_i2e_manager
from nlp_lib.py.dynamic_data_lib.dynamic_data_manager_class \
    import Dynamic_data_manager
from nlp_lib.py.file_lib.json_manager_class import Json_manager
from nlp_lib.py.metadata_lib.metadata_manager_class import Metadata_manager
from nlp_lib.py.output_lib.output_manager_class import Output_manager
from nlp_lib.py.packaging_lib.packaging_manager_class import Packaging_manager
from nlp_lib.py.process_lib.worker_lib.preprocessing_worker_class \
    import Preprocessing_worker
from nlp_lib.py.raw_data_lib.raw_data_manager_class import Raw_data_manager
from ohsu_nlp_template_lib.py.ohsu_nlp_template_manager_class \
    import Ohsu_nlp_template_manager
from tool_lib.py.processing_tools_lib.file_processing_tools \
    import read_json_file
from tool_lib.py.registry_lib.template_registry_class import Template_registry

#
class Process_manager(object):
    
    #
    def __init__(self, static_data_manager, server_manager, password):
        self.server_manager = server_manager
        self.static_data_manager = static_data_manager
        self.password = password
        self._project_imports()
        self._create_managers(server_manager, password)
        self._create_registries()
        
    #
    def _create_managers(self, server_manager, password):
        static_data = self.static_data_manager.get_static_data()
        directory_manager = static_data['directory_manager']
        project_name = static_data['project_name']
        save_dir = \
            directory_manager.pull_directory('processing_data_dir')
        save_dir_tmp = re.sub('/production$', '/test', save_dir)
        filename = \
            os.path.join(save_dir_tmp, project_name + '.performance.json')
        performance_json_manager = \
            Json_manager(self.static_data_manager, filename)
        data_dir = directory_manager.pull_directory('processing_data_dir')
        filename = os.path.join(data_dir, project_name + '.json')
        project_json_manager = \
            Json_manager(self.static_data_manager, filename)
        self.dynamic_data_manager = \
            Dynamic_data_manager(self.static_data_manager)
        self.linguamatics_i2e_manager = \
            Linguamatics_i2e_manager(self.static_data_manager, server_manager,
                                     password)
        self.metadata_manager = Metadata_manager(self.static_data_manager)
        self.ohsu_nlp_template_manager = Ohsu_nlp_template_manager()
        self.packaging_manager = \
            Packaging_manager(self.static_data_manager,
                              performance_json_manager, project_json_manager)
        try:
            self.performance_data_manager = \
                Performance_data_manager(self.static_data_manager,
                                         performance_json_manager,
                                         project_json_manager)
            print('Performance_data_manager: ' + project_name + '_performance_data_manager')
        except Exception as e:
            print(e)
            self.performance_data_manager = None
        self.postprocessor_registry = \
            Postprocessor_registry(self.static_data_manager,
                                   self.metadata_manager)
        self.output_manager = Output_manager(self.static_data_manager, 
                                             self.metadata_manager)
        
    #
    def _create_registries(self):
        self.template_registry = Template_registry(self.static_data_manager)
        
    #
    def _project_imports(self):
        static_data = self.static_data_manager.get_static_data()
        project_name = static_data['project_name']
        import_cmd = 'from projects_lib.' + project_name + '.py.' + \
                     project_name.lower() + \
                     '_performance_data_manager_class import ' + project_name + \
                     '_performance_data_manager as Performance_data_manager'
        try:
            exec(import_cmd, globals())
        except Exception as e:
            print(e)
        try:
            import_cmd = 'from projects_lib.' + project_name + '.py.' + \
                         project_name.lower() + \
                         '_postprocessor_registry_class import ' + project_name + \
                         '_postprocessor_registry as Postprocessor_registry'
            exec(import_cmd, globals())
            print('Postprocessor_registry: ' + project_name + '_postprocessor_registry')
        except Exception as e:
            import_cmd = 'from tool_lib.py.registry_lib.postprocessor_registry_class import Postprocessor_registry'
            exec(import_cmd, globals())
            print(e)
            print('Postprocessor_registry: Postprocessor_registry')
            
    #
    def calculate_performance(self):
        if self.performance_data_manager is not None:
            self.performance_data_manager.get_performance_data()
            self.performance_data_manager.display_performance_data()
            self.performance_data_manager.write_performance_data()
        
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
    def get_metadata_values(self):
        static_data = self.static_data_manager.get_static_data()
        metadata_json_file = self.metadata_manager.get_metadata_json_file()
        metadata = read_json_file(metadata_json_file)
        num_documents = len(metadata.keys())
        document_values = []
        patient_values = []
        date_values = []
        for key0 in metadata.keys():
            for key1 in metadata[key0]['METADATA'].keys():
                '''
                if key1 in static_data['datetime_identifiers'].keys():
                    date_str = metadata[key0]['METADATA'][key1]
                    date_num = \
                        datetime2matlabdn(datetime.strptime(date_str,
                                                            static_data['datetime_identifiers'][key1]))
                    date_values.append(date_num)
                '''
                if key1 in static_data['document_identifiers']:
                    document_values.append(metadata[key0]['METADATA'][key1])
                if key1 in static_data['patient_identifiers']:
                    patient_values.append(metadata[key0]['METADATA'][key1])
        document_values = list(set(document_values))
        patient_values = list(set(patient_values))
        #date_values.sort()
        patient_values.sort()
        return document_values, patient_values, date_values
        
    #
    def linguamatics_i2e_fix_queries(self):
        self.linguamatics_i2e_manager.fix_queries()
        
    #
    def linguamatics_i2e_generate_csv_files(self):
        static_data = self.static_data_manager.get_static_data()
        directory_manager = static_data['directory_manager']
        data_dir = directory_manager.pull_directory('postprocessing_data_in')
        self.linguamatics_i2e_manager.generate_csv_files()
        
    #
    def linguamatics_i2e_generate_resource_files(self):
        static_data = self.static_data_manager.get_static_data()
        max_files_per_zip = static_data['max_files_per_zip']
        self.linguamatics_i2e_manager.generate_i2e_resource_files(max_files_per_zip)
    
    #
    def linguamatics_i2e_indexer(self):
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
    def linguamatics_i2e_postindexer(self):
        self.metadata_manager.save_metadata()
        
    #
    def linguamatics_i2e_preindexer(self):
        static_data = self.static_data_manager.get_static_data()
        directory_manager = static_data['directory_manager']
        static_data['directory_manager'].cleanup_directory('source_data')
        keywords_file = self.dynamic_data_manager.keywords_file()
        processing_data_dir = directory_manager.pull_directory('processing_data_dir')
        source_data_dir = directory_manager.pull_directory('source_data')
        max_files_per_zip = static_data['max_files_per_zip']
        self.linguamatics_i2e_manager.login()
        self.linguamatics_i2e_manager.preindexer(keywords_file,
                                                 processing_data_dir,
                                                 source_data_dir,
                                                 max_files_per_zip)
        self.linguamatics_i2e_manager.logout()
        
    #
    def ohsu_nlp_templates_run(self):
        static_data = self.static_data_manager.get_static_data()
        directory_manager = static_data['directory_manager']
        data_dir = directory_manager.pull_directory('preprocessing_data_out')
        keywords_file = self.dynamic_data_manager.keywords_file()
        template = self.template_registry.tnm_template()
        self.ohsu_nlp_template_manager.clear_template_output()
        self.ohsu_nlp_template_manager.run_template(data_dir, keywords_file,
                                                    template)
        data_dir = directory_manager.pull_directory('postprocessing_data_in')
        filename = 'breast_cancer_tnm_stage.csv'
        header = [ 'DOCUMENT_ID', 'DATETIME', 'Section Title', 'Specimen Id',
                   'TNM Stage', 'Snippet', 'Coords' ]
        self.ohsu_nlp_template_manager.write_template_output(data_dir, 
                                                             filename, header)
        
    #
    def postperformance(self):
        static_data = self.static_data_manager.get_static_data()
        if static_data['project_subdir'] == 'test':
            self.packaging_manager.create_postperformance_test_data_json()
        elif static_data['project_subdir'] == 'production':
            self.packaging_manager.create_postperformance_production_data_json()

    #
    def postprocessor(self):
        static_data = self.static_data_manager.get_static_data()
        directory_manager = static_data['directory_manager']
        data_dir = directory_manager.pull_directory('postprocessing_data_in')
        for filename in os.listdir(data_dir):
            filename_base, extension = os.path.splitext(filename)
            if extension in [ '.csv' ]:
                self.postprocessor_registry.create_postprocessor(filename)
        for filename in os.listdir(data_dir):
            filename_base, extension = os.path.splitext(filename)
            if extension in [ '.csv' ]:
                data_dict = \
                    self.linguamatics_i2e_manager.generate_data_dict(filename)
                self.postprocessor_registry.push_data_dict(filename, data_dict)
        self.postprocessor_registry.run_registry()
        postprocessor_registry = \
            self.postprocessor_registry.pull_postprocessor_registry()
        for key in postprocessor_registry.keys():
            self.output_manager.append(postprocessor_registry[key])
        self.output_manager.merge_data_dict_lists()
        self.output_manager.include_metadata()
        self.output_manager.include_text()
        self.output_manager.create_json_files()
        
    #
    def preperformance(self):
        self.packaging_manager.create_preperformance_test_data_json()
    
    #
    def preprocessor(self, password, start_idx, preprocess_files_flg):
        static_data = self.static_data_manager.get_static_data()
        i2e_version = \
            self.linguamatics_i2e_manager.get_i2e_version(password)
        multiprocessing_flg = static_data['multiprocessing']
        if multiprocessing_flg:
            keys = list(static_data['raw_data_files'].keys())
            for key in keys:
                filename, extension = os.path.splitext(key)
                if extension in [ '.xls', '.xlsx' ]:
                    multiprocessing_flg = False
        if multiprocessing_flg:
            num_processes = static_data['num_processes']
        else:
            num_processes = 1
        self.raw_data_manager = Raw_data_manager(static_data, 
                                                 self.server_manager, 
                                                 multiprocessing_flg,
                                                 password)
            
        # Read data kludge to be done properly later
        operation_mode = static_data['operation_mode']
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
                                     preprocess_files_flg)
            dynamic_data_manager_copy = deepcopy(self.dynamic_data_manager)
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
        os.remove(pkl_file)
        # Read data kludge to be done properly later
        
        print('Number of documents preprocessed: ' + str(num_docs_preprocessed))
        if preprocess_files_flg:
            self.dynamic_data_manager.generate_keywords_file()
        self.metadata_manager.save_metadata()