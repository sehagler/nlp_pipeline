# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 10:14:44 2019

@author: haglers
"""

#
from copy import deepcopy
import csv
import datetime
import multiprocessing
import os
import pickle
import re
import shutil
import time

#
from nlp_pipeline_lib.py.dynamic_data_lib.dynamic_data_manager_class \
    import Dynamic_data_manager
from nlp_pipeline_lib.py.evaluation_lib.evaluation_manager_class \
    import Evaluation_manager
from nlp_pipeline_lib.py.file_lib.json_lib.json_manager_class \
    import Json_manager
from nlp_pipeline_lib.py.file_lib.xls_lib.xls_manager_class \
    import Xls_manager
from nlp_pipeline_lib.py.file_lib.xml_lib.xml_manager_class \
    import Xml_manager
from nlp_pipeline_lib.py.metadata_lib.metadata_manager_class \
    import Metadata_manager
from nlp_pipeline_lib.py.output_lib.output_manager_class import Output_manager
from nlp_pipeline_lib.py.packaging_lib.packaging_manager_class \
    import Packaging_manager
from nlp_pipeline_lib.py.process_lib.worker_lib.preprocessing_worker_class \
    import Preprocessing_worker
from nlp_pipeline_lib.py.raw_data_lib.raw_data_manager_class \
    import Raw_data_manager
from nlp_text_normalization_lib.text_normalization_manager_class \
    import Text_normalization_manager
from nlp_tools_lib.nlp_tool_manager_registry_lib.nlp_tool_manager_registry_class \
    import Nlp_tool_manager_registry
from tool_lib.py.processing_tools_lib.file_processing_tools \
    import read_json_file, read_txt_file

#
class Process_manager(object):
    
    #
    def __init__(self, static_data_manager, server_manager, password):
        self.server_manager = server_manager
        self.static_data_manager = static_data_manager
        self.password = password
        self._project_imports()
        self._create_managers(server_manager, password)
        
        # Kludge to get around memory issue in processor
        linguamatics_i2e_manager = \
            self.nlp_tool_manager_registry.get_manager('linguamatics_i2e_manager')
        self.i2e_version = \
            linguamatics_i2e_manager.get_i2e_version(password)
        # Kludge to get around memory issue in processor
        
    #
    def _create_keywords_regexp(self, keywords):
        keywords_list = keywords.split('\n')
        keywords_list.remove('')
        keywords_regexp_str = '('
        for i in range(len(keywords_list)-1):
            keywords_regexp_str += keywords_list[i] + '|'
        keywords_regexp_str += keywords_list[-1] + ')'
        keywords_regexp = re.compile(keywords_regexp_str)
        return keywords_regexp
    
    #
    def _create_managers(self, server_manager, password):
        static_data = self.static_data_manager.get_static_data()
        directory_manager = static_data['directory_manager']
        project_name = static_data['project_name']
        processing_base_dir = \
            directory_manager.pull_directory('processing_base_dir')
        raw_data_dir = \
            directory_manager.pull_directory('raw_data_dir')
        json_manager_registry = {}
        for key in [ 'performance_data_files', 'project_data_files' ]:
            for filename in static_data[key]:
                file = os.path.join(processing_base_dir, filename)
                json_manager_registry[filename] = \
                    Json_manager(self.static_data_manager, file)
        self.xls_manager_registry = {}
        self.xml_manager_registry = {}
        for key in static_data['raw_data_files'].keys():
            filename, extension = os.path.splitext(key)
            if extension.lower() in [ '.xls', '.xlsx' ]:
                file = os.path.join(raw_data_dir, key)
                self.xls_manager_registry[file] = \
                    Xls_manager(static_data, server_manager, file, password)
            elif extension.lower() in [ '.xml' ]:
                file = os.path.join(raw_data_dir, key)
                self.xml_manager_registry[file] = \
                    Xml_manager(static_data, server_manager, file, password)
        if 'extracts_file' in static_data.keys():
            filename = static_data['extracts_file']
            file = os.path.join(raw_data_dir, filename)
            self.xls_manager_registry[file] = \
                Xls_manager(static_data, server_manager, file, password)
        if static_data['project_subdir'] == 'test':           
            validation_filename = static_data['validation_file']
            file = os.path.join(raw_data_dir, validation_filename)
            self.xls_manager_registry[file] = \
                Xls_manager(static_data, server_manager, file, password)
        self.dynamic_data_manager = \
            Dynamic_data_manager(self.static_data_manager)
        evaluation_manager = \
            Evaluation_manager(self.static_data_manager)
        self.metadata_manager = Metadata_manager(self.static_data_manager)
        self.nlp_tool_manager_registry = \
            Nlp_tool_manager_registry(self.static_data_manager, server_manager,
                                      self.xls_manager_registry, evaluation_manager,
                                      password)
        self.packaging_manager = \
            Packaging_manager(self.static_data_manager, json_manager_registry)
        try:
            self.performance_data_manager = \
                Performance_data_manager(self.static_data_manager,
                                         json_manager_registry,
                                         self.xls_manager_registry,
                                         evaluation_manager)
            print('Performance_data_manager: ' + project_name + '_performance_data_manager')
        except Exception as e:
            print(e)
            self.performance_data_manager = None
        self.postprocessor_registry = \
            Postprocessor_registry(self.static_data_manager,
                                   self.metadata_manager)
        self.text_normalization_manager = \
            Text_normalization_manager(self.static_data_manager)
        self.output_manager = Output_manager(self.static_data_manager, 
                                             self.metadata_manager,
                                             json_manager_registry)
        
        multiprocessing_flg = static_data['multiprocessing']
        if multiprocessing_flg:
            keys = list(static_data['raw_data_files'].keys())
            for key in keys:
                filename, extension = os.path.splitext(key)
                if extension in [ '.xls', '.xlsx' ]:
                    multiprocessing_flg = False
        self.raw_data_manager = Raw_data_manager(self.static_data_manager, 
                                                 self.server_manager,
                                                 multiprocessing_flg,
                                                 password)
        
    #
    def _create_text_dict_postprocessing_data_in(self, sections):
        document_ids = []
        for i in range(1, len(sections)):
            row = sections[i]
            document_ids.append(row[0])
        document_ids = list(set(document_ids))
        document_ids = sorted(document_ids)
        text_dict = {}
        for document_id in document_ids:
            text_dict[document_id] = {}
            for i in range(1, len(sections)):
                row = sections[i]
                if row[0] == document_id:
                    key = (row[2], row[3])
                    section = row[4]
                    offset_base = 0
                    if section != '.*':
                        text_dict[document_id][key] = {}
                        text_dict[document_id][key]['OFFSET_BASE'] = offset_base
                        text_dict[document_id][key]['TEXT'] = section
        return text_dict
        
    #
    def _create_text_dict_preprocessing_data_out(self, data_dir,
                                                 keywords_regexp):
        text_dict = {}
        filenames = os.listdir(data_dir)
        filenames = sorted(filenames)
        for filename in filenames:
            filename_base, extension = os.path.splitext(filename)
            if extension in [ '.xml' ]:
                parser = ET.iterparse(os.path.join(data_dir, filename))
                for event, elem in parser:
                    if elem.tag == 'DOCUMENT_ID':
                        document_id = elem.text
                    elif elem.tag == 'rpt_text':
                        text = elem.text
            elif extension in [ '.txt' ]:
                document_id = filename_base
                text = read_txt_file(os.path.join(data_dir, filename))
            text_dict[document_id] = \
                self._parse_document(keywords_regexp, text)
        return text_dict
    
    #
    def _parse_document(self, keywords_regexp, text):
        keyword = None
        offset_base = 0
        text_dict = {}
        for line in text.splitlines():
            if keywords_regexp.search(line):
                keyword = line
                offset_base += len(line)
                section = ''
            else:
                if keyword is not None:
                    key = (keyword, '')
                    text_dict[key] = {}
                    text_dict[key]['OFFSET_BASE'] = offset_base
                    text_dict[key]['TEXT'] = section
                offset_base += len(line)
                section += line + '\n'
        return text_dict
        
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
        linguamatics_i2e_manager = \
            self.nlp_tool_manager_registry.get_manager('linguamatics_i2e_manager')
        linguamatics_i2e_manager.login()
        linguamatics_i2e_manager.folder_downloader(query_folder,
                                                        destination_folder)
        linguamatics_i2e_manager.logout()
        
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
        linguamatics_i2e_manager = \
            self.nlp_tool_manager_registry.get_manager('linguamatics_i2e_manager')
        linguamatics_i2e_manager.fix_queries()
        
    #
    def linguamatics_i2e_generate_csv_files(self):
        static_data = self.static_data_manager.get_static_data()
        directory_manager = static_data['directory_manager']
        data_dir = directory_manager.pull_directory('postprocessing_data_in')
        linguamatics_i2e_manager = \
            self.nlp_tool_manager_registry.get_manager('linguamatics_i2e_manager')
        linguamatics_i2e_manager.generate_csv_files()
        
    #
    def linguamatics_i2e_generate_resource_files(self):
        static_data = self.static_data_manager.get_static_data()
        max_files_per_zip = static_data['max_files_per_zip']
        linguamatics_i2e_manager = \
            self.nlp_tool_manager_registry.get_manager('linguamatics_i2e_manager')
        linguamatics_i2e_manager.generate_i2e_resource_files(max_files_per_zip)
    
    #
    def linguamatics_i2e_indexer(self):
        now = datetime.datetime.now()
        index_start_datetime = now.strftime("%d-%b-%y %H:%M:%S.%f")[:-3]
        self.metadata_manager.load_metadata()
        self.metadata_manager.append_nlp_metadata_value('DOCUMENT_SET_INDEXING_START_DATETIME',
                                                        index_start_datetime)
        self.metadata_manager.save_metadata()
        linguamatics_i2e_manager = \
            self.nlp_tool_manager_registry.get_manager('linguamatics_i2e_manager')
        linguamatics_i2e_manager.login()
        linguamatics_i2e_manager.make_index_runner()
        linguamatics_i2e_manager.logout()
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
        linguamatics_i2e_manager = \
            self.nlp_tool_manager_registry.get_manager('linguamatics_i2e_manager')
        linguamatics_i2e_manager.login()
        linguamatics_i2e_manager.preindexer(keywords_file, processing_data_dir,
                                            source_data_dir, max_files_per_zip)
        linguamatics_i2e_manager.logout()
        
    #
    def ohsu_nlp_templates_run_templates(self):
        static_data = self.static_data_manager.get_static_data()
        project_name = static_data['project_name']
        directory_manager = static_data['directory_manager']
        data_dir = directory_manager.pull_directory('postprocessing_data_in')
        ohsu_nlp_template_manager = \
            self.nlp_tool_manager_registry.get_manager('ohsu_nlp_template_manager')
        template_dir = \
            directory_manager.pull_directory('ohsu_nlp_project_queries_dir')
        files = os.listdir(template_dir)
        for file in files:
            filename, extension = os.path.splitext(file)
            import_cmd = 'from projects_lib.' + project_name + \
                         '.nlp_templates.' + filename + ' import ' + \
                         filename[0].upper() + filename[1:-6] + \
                         ' as Template_manager'
            exec(import_cmd, globals())
            print('OHSU NLP Template: ' + filename)
            template_manager = Template_manager(self.static_data_manager)
            ohsu_nlp_template_manager.clear_template_output()
            ohsu_nlp_template_manager.run_template(template_manager, 
                                                   self.template_text_dict)
            filename = re.sub('_template_manager_class', '', filename)
            ohsu_nlp_template_manager.write_template_output(template_manager,
                                                            data_dir,
                                                            filename + '.csv')
            
    #
    def ohsu_nlp_templates_setup(self):
        static_data = self.static_data_manager.get_static_data()
        directory_manager = static_data['directory_manager']
        data_dir = \
            directory_manager.pull_directory('ohsu_nlp_preprocessing_data_out')
        keywords_file = self.dynamic_data_manager.keywords_file()
        keywords = read_txt_file(keywords_file)
        keywords_regexp = self._create_keywords_regexp(keywords)
        text_dict = \
            self._create_text_dict_preprocessing_data_out(data_dir,
                                                          keywords_regexp)
        self.template_data_dir = data_dir
        self.template_text_dict = text_dict
    
    #
    def ohsu_nlp_templates_post_i2e_linguamatics_setup(self):
        static_data = self.static_data_manager.get_static_data()
        directory_manager = static_data['directory_manager']
        data_dir = directory_manager.pull_directory('postprocessing_data_in')
        if 'sections.csv' in os.listdir(data_dir):
            sections = []
            with open(os.path.join(data_dir, 'sections.csv')) as f:
                csv_reader = csv.reader(f)
                for row in csv_reader:
                    sections.append(row)
            text_dict = self._create_text_dict_postprocessing_data_in(sections)
        else:
            text_dict = None
        self.template_data_dir = data_dir
        self.template_text_dict = text_dict
        
    #
    def ohsu_nlp_templates_train_templates(self):
        static_data = self.static_data_manager.get_static_data()
        project_name = static_data['project_name']
        directory_manager = static_data['directory_manager']
        ohsu_nlp_template_manager = \
            self.nlp_tool_manager_registry.get_manager('ohsu_nlp_template_manager')
        template_dir = \
            directory_manager.pull_directory('ohsu_nlp_project_queries_dir')
        files = os.listdir(template_dir)
        for file in files:
            filename, extension = os.path.splitext(file)
            import_cmd = 'from projects_lib.' + project_name + \
                         '.nlp_templates.' + \
                         filename + ' import ' + filename[0].upper() + \
                         filename[1:-6] + ' as Template_manager'
            exec(import_cmd, globals())
            print('OHSU NLP Template: ' + filename)
            template_manager = Template_manager(self.static_data_manager)
            extracts_file = static_data['extracts_file']
            extracts_file = os.path.join(static_data['directory_manager'].pull_directory('raw_data_dir'),
                                         extracts_file)
            xls_manager = \
                self.xls_manager_registry[extracts_file]
            xls_manager.read_training_data()
            ohsu_nlp_template_manager.clear_template_output()
            ohsu_nlp_template_manager.train_template(template_manager,
                                                     self.metadata_manager,
                                                     xls_manager,
                                                     self.template_data_dir,
                                                     self.template_text_dict)
            template_outlines_dir = \
                directory_manager.pull_directory('template_outlines_dir')
            filename = filename[:-13] + 'outline'
            ohsu_nlp_template_manager.write_template_outline(template_outlines_dir,
                                                             filename + '.txt')
        
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
        filelist = os.listdir(data_dir)
        if static_data['project_subdir'] == 'test' and \
           'test_postprocessing_data_in_files' in static_data.keys():
            filelist = \
                list(set(filelist).intersection(static_data['test_postprocessing_data_in_files']))
        for filename in filelist:
            filename_base, extension = os.path.splitext(filename)
            if extension in [ '.csv' ]:
                self.postprocessor_registry.create_postprocessor(filename)
        for filename in filelist:
            filename_base, extension = os.path.splitext(filename)
            if extension in [ '.csv' ]:
                linguamatics_i2e_manager = \
                    self.nlp_tool_manager_registry.get_manager('linguamatics_i2e_manager')
                data_dict = \
                    linguamatics_i2e_manager.generate_data_dict(filename)
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
        num_processes = self.raw_data_manager.get_number_of_processes()
        
        # Kludge to get around memory issue in processor
        i2e_version = self.i2e_version
        # Kludge to get around memory issue in processor
  
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
                                     self.text_normalization_manager,
                                     self.nlp_tool_manager_registry,
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
        
    #
    def read_data(self):
        static_data = self.static_data_manager.get_static_data()
        raw_data_files_dict = static_data['raw_data_files']
        if 'raw_data_files_sequence' in static_data.keys():
            raw_data_files_seq = static_data['raw_data_files_sequence']
        else:
            raw_data_files_seq = None
        if raw_data_files_seq is None:
            raw_data_files_seq = list(raw_data_files_dict.keys())
        raw_data_files = []
        for i in range(len(raw_data_files_seq)):
            raw_data_files.append(os.path.join(static_data['directory_manager'].pull_directory('raw_data_dir'),
                                               raw_data_files_seq[i]))
        for i in range(len(raw_data_files)):
            filename, extension = os.path.splitext(raw_data_files[i])
            if extension.lower() in [ '.xls', '.xlsx' ]:
                xls_manager = \
                    self.xls_manager_registry[raw_data_files[i]]
                raw_data = xls_manager.read_file()
                self.raw_data_manager.append_raw_data(raw_data)
            elif extension.lower() in [ '.xml' ]:
                xml_manager = \
                    self.xml_manager_registry[raw_data_files[i]]
                raw_data = xml_manager.read_file()
                self.raw_data_manager.append_raw_data(raw_data)
            else:
                print('invalid file extension: ' + extension)
        self.raw_data_manager.partition_data()