# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 10:14:44 2019

@author: haglers
"""

#
from copy import deepcopy
import csv
import datetime
import glob
import json
import plotext as plt
import multiprocessing
import numpy as np
import os
import pickle
import re
import shutil
import time

#
from nlp_pipeline_lib.dynamic_data_lib.dynamic_data_manager_class \
    import Dynamic_data_manager
from nlp_pipeline_lib.evaluation_lib.evaluation_manager_class \
    import Evaluation_manager
from nlp_pipeline_lib.file_lib.json_lib.json_manager_class \
    import Json_manager
from nlp_pipeline_lib.file_lib.xls_lib.xls_manager_class \
    import Xls_manager
from nlp_pipeline_lib.file_lib.xml_lib.xml_manager_class \
    import Xml_manager
from nlp_pipeline_lib.metadata_lib.metadata_manager_class \
    import Metadata_manager
from nlp_pipeline_lib.output_lib.output_manager_class import Output_manager
from nlp_pipeline_lib.packaging_lib.packaging_manager_class \
    import Packaging_manager
from nlp_pipeline_lib.process_lib.worker_lib.preprocessing_worker_class \
    import Preprocessing_worker
from tool_lib.py.registry_lib.preprocessor_registry_class \
    import Preprocessor_registry
from nlp_pipeline_lib.raw_data_lib.raw_data_manager_class \
    import Raw_data_manager
from nlp_text_normalization_lib.text_normalization_manager_class \
    import Text_normalization_manager
from nlp_pipeline_lib.registry_lib.nlp_tool_manager_registry_class \
    import Nlp_tool_manager_registry
from tool_lib.py.processing_tools_lib.file_processing_tools \
    import read_json_file, read_txt_file

#
class Process_manager(object):
    
    #
    def __init__(self, static_data_manager, remote_manager_registry, 
                 password):
        self.static_data_manager = static_data_manager
        self.password = password
        self._project_imports()
        self._create_managers(remote_manager_registry, password)
        
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
    def _create_managers(self, remote_manager_registry, password):
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
                    Xls_manager(static_data, file, password)
            elif extension.lower() in [ '.xml' ]:
                file = os.path.join(raw_data_dir, key)
                self.xml_manager_registry[file] = \
                    Xml_manager(static_data, file, password)
        if 'extracts_file' in static_data.keys():
            filename = static_data['extracts_file']
            file = os.path.join(raw_data_dir, filename)
            self.xls_manager_registry[file] = \
                Xls_manager(static_data, file, password)
        if static_data['project_subdir'] == 'test' and \
           'validation_file' in static_data.keys():
            validation_filename = static_data['validation_file']
            file = os.path.join(raw_data_dir, validation_filename)
            self.xls_manager_registry[file] = \
                Xls_manager(static_data, file, password)
        self.dynamic_data_manager = \
            Dynamic_data_manager(self.static_data_manager)
        evaluation_manager = \
            Evaluation_manager(self.static_data_manager)
        self.metadata_manager = Metadata_manager(self.static_data_manager)
        self.nlp_tool_manager_registry = \
            Nlp_tool_manager_registry(self.static_data_manager, 
                                      remote_manager_registry,
                                      password)
        self.packaging_manager = \
            Packaging_manager(self.static_data_manager, json_manager_registry)
        try:
            self.performance_data_manager = \
                Performance_data_manager(self.static_data_manager,
                                         evaluation_manager,
                                         json_manager_registry,
                                         self.metadata_manager,
                                         self.xls_manager_registry)
            print('Performance_data_manager: ' + project_name + '_performance_data_manager')
        except Exception as e:
            print(e)
            self.performance_data_manager = None
        self.postprocessor_registry = \
            Postprocessor_registry(self.static_data_manager,
                                   self.metadata_manager)
        preprocessor_registry = Preprocessor_registry(static_data)
        preprocessor_registry.create_preprocessors()
        self.text_normalization_manager = \
            Text_normalization_manager(self.static_data_manager,
                                       preprocessor_registry)
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
    def _documents_by_year(self):
        static_data = self.static_data_manager.get_static_data()
        datetime_keys = {}
        metadata_json_file = self.metadata_manager.get_metadata_json_file()
        metadata = read_json_file(metadata_json_file)
        year_list = []
        for doc_id in metadata.keys():
            doc_id = str(int(doc_id))
            key = metadata[doc_id]['NLP_METADATA']['FILENAME']
            datetime_key = static_data['raw_data_files'][key]['DATETIME_KEY']
            datetime_format = \
                static_data['raw_data_files'][key]['DATETIME_FORMAT']
            date_str = \
                metadata[doc_id]['METADATA'][datetime_key]
            if date_str is not None and len(date_str) > 0:
                dt = datetime.datetime.strptime(date_str, datetime_format)
                year_list.append(dt.year)
        years = list(set(year_list))
        years = sorted(list(range(min(years), max(years)+1)))
        year_cts = []
        year_lbls = []
        for i in range(len(years)):
            year_cts.append(year_list.count(years[i]))
            year_lbls.append('*' + str(years[i]))
        plt.bar(year_lbls, year_cts, orientation = 'h')
        plt.show()
    
    #
    def _parse_document(self, keywords_regexp, text):
        key = None
        offset_base = 0
        text_dict = {}
        for line in text.splitlines():
            if keywords_regexp.search(line) and key is None:
                key = (line, '')
                offset_base += len(line)
                section = ''
            elif keywords_regexp.search(line) and key is not None:
                text_dict[key] = {}
                text_dict[key]['OFFSET_BASE'] = offset_base
                text_dict[key]['TEXT'] = section
                key = (line, '')
                offset_base += len(line)
                section = ''
            else:
                offset_base += len(line)
                section += line + '\n'
        text_dict[key] = {}
        text_dict[key]['OFFSET_BASE'] = offset_base
        text_dict[key]['TEXT'] = section
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
    def _total_documents(self):
        static_data = self.static_data_manager.get_static_data()
        datetime_keys = {}
        metadata_json_file = self.metadata_manager.get_metadata_json_file()
        metadata = read_json_file(metadata_json_file)
        num_documents = str(len(metadata.keys()))
        print('number of documents: ' + num_documents)
        
    #
    def _total_patients(self):
        static_data = self.static_data_manager.get_static_data()
        patient_identifiers = set(static_data['patient_identifiers'])
        metadata_json_file = self.metadata_manager.get_metadata_json_file()
        metadata = read_json_file(metadata_json_file)
        patient_list = []
        for doc_id in metadata.keys():
            metadata_keys = set(metadata[doc_id]['METADATA'].keys())
            keys = list(metadata_keys & patient_identifiers)
            if len(keys) != 1:
                keys = None
            if keys is not None:
                patient_list.append(metadata[doc_id]['METADATA'][keys[0]])
        patient_list = list(set(patient_list))
        num_patients = str(len(patient_list))
        print('number of patients: ' + num_patients)
            
    #
    def calculate_performance(self):
        if self.performance_data_manager is not None:
            self.performance_data_manager.get_performance_data()
            self.performance_data_manager.display_performance_data()
            self.performance_data_manager.write_performance_data()
            
    #
    def data_set_summary_info(self):
        self._documents_by_year()
        self._total_documents()
        self._total_patients()
        
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
    def linguamatics_i2e_fix_queries(self):
        static_data = self.static_data_manager.get_static_data()
        directory_manager = static_data['directory_manager']
        general_queries_dir = \
            directory_manager.pull_directory('linguamatics_i2e_general_queries_dir')
        project_queries_dir = \
            directory_manager.pull_directory('linguamatics_i2e_project_queries_dir')
        linguamatics_i2e_manager = \
            self.nlp_tool_manager_registry.get_manager('linguamatics_i2e_manager')
        linguamatics_i2e_manager.fix_queries(general_queries_dir)
        linguamatics_i2e_manager.fix_queries(project_queries_dir)
        
    #
    def linguamatics_i2e_generate_csv_files(self):
        static_data = self.static_data_manager.get_static_data()
        directory_manager = static_data['directory_manager']
        data_dir = directory_manager.pull_directory('postprocessing_data_in')
        linguamatics_i2e_manager = \
            self.nlp_tool_manager_registry.get_manager('linguamatics_i2e_manager')
        linguamatics_i2e_manager.generate_csv_files(data_dir)
        
    #
    def linguamatics_i2e_generate_resource_files(self):
        static_data = self.static_data_manager.get_static_data()
        directory_manager = static_data['directory_manager']
        max_files_per_zip = static_data['max_files_per_zip']
        project_name = static_data['project_name']
        general_queries_source_dir = \
            directory_manager.pull_directory('linguamatics_i2e_general_queries_dir')
        preprocessing_data_out_dir = \
            directory_manager.pull_directory('linguamatics_i2e_preprocessing_data_out')
        processing_data_dir = \
            directory_manager.pull_directory('processing_data_dir')
        project_queries_source_dir = \
            directory_manager.pull_directory('linguamatics_i2e_project_queries_dir')
        linguamatics_i2e_manager = \
            self.nlp_tool_manager_registry.get_manager('linguamatics_i2e_manager')
        linguamatics_i2e_manager.generate_query_bundle_file(project_name, general_queries_source_dir,
                                                            processing_data_dir, 
                                                            project_queries_source_dir, 
                                                            max_files_per_zip)
        linguamatics_i2e_manager.generate_regions_file(preprocessing_data_out_dir,
                                                       processing_data_dir)
        linguamatics_i2e_manager.generate_xml_configuation_file(preprocessing_data_out_dir,
                                                                processing_data_dir)
    
    #
    def linguamatics_i2e_indexer(self):
        static_data = self.static_data_manager.get_static_data()
        project_name = static_data['project_name']
        now = datetime.datetime.now()
        index_start_datetime = now.strftime("%d-%b-%y %H:%M:%S.%f")[:-3]
        self.metadata_manager.load_metadata()
        self.metadata_manager.append_nlp_metadata_value('DOCUMENT_SET_INDEXING_START_DATETIME',
                                                        index_start_datetime)
        self.metadata_manager.save_metadata()
        linguamatics_i2e_manager = \
            self.nlp_tool_manager_registry.get_manager('linguamatics_i2e_manager')
        linguamatics_i2e_manager.login()
        linguamatics_i2e_manager.make_index_runner(project_name)
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
        preprocessing_data_out_dir = directory_manager.pull_directory('linguamatics_i2e_preprocessing_data_out')
        processing_data_dir = directory_manager.pull_directory('processing_data_dir')
        project_name = static_data['project_name']
        source_data_dir = directory_manager.pull_directory('source_data')
        max_files_per_zip = static_data['max_files_per_zip']
        root_dir_flg = static_data['root_dir_flg']
        linguamatics_i2e_manager = \
            self.nlp_tool_manager_registry.get_manager('linguamatics_i2e_manager')
        linguamatics_i2e_manager.login()
        linguamatics_i2e_manager.preindexer(project_name, keywords_file,
                                            preprocessing_data_out_dir,
                                            processing_data_dir, source_data_dir,
                                            max_files_per_zip, root_dir_flg)
        linguamatics_i2e_manager.logout()
        
    #
    def melax_clamp_run_pipeline(self):
        melax_clamp_manager = \
            self.nlp_tool_manager_registry.get_manager('melax_clamp_manager')
        melax_clamp_manager.run_pipeline()
        
    #
    def ohsu_nlp_templates_generate_AB_fields(self):
        static_data = self.static_data_manager.get_static_data()
        project_name = static_data['project_name']
        directory_manager = static_data['directory_manager']
        ohsu_nlp_template_manager = \
            self.nlp_tool_manager_registry.get_manager('ohsu_nlp_template_manager')
        project_AB_fields_dir = \
            directory_manager.pull_directory('ohsu_nlp_project_AB_fields_dir')
        files = glob.glob(project_AB_fields_dir + '/**/*.py', recursive=True)
        for i in range(len(files)):
            files[i] = re.sub(project_AB_fields_dir + '/', '', files[i])
        for file in files:
            class_filename, extension = os.path.splitext(file)
            class_filename = re.sub('/', '.', class_filename)
            class_name, extension = os.path.splitext(os.path.basename(file))
            class_name = class_name[0].upper() + class_name[1:-6]
            import_cmd = 'from projects_lib.' + project_name + \
                         '.nlp_templates.AB_fields.' + class_filename + \
                         ' import ' + class_name + ' as Template_manager'
            exec(import_cmd, globals())
            print('OHSU NLP Template Manager: ' + class_name)
            extracts_file = static_data['extracts_file']
            extracts_file = os.path.join(static_data['directory_manager'].pull_directory('raw_data_dir'),
                                         extracts_file)
            xls_manager = \
                self.xls_manager_registry[extracts_file]
            xls_manager.read_training_data()
            template_manager = Template_manager(self.static_data_manager,
                                                xls_manager)
            ohsu_nlp_template_manager.clear_template_output()
            ohsu_nlp_template_manager.train_template(template_manager,
                                                     self.metadata_manager,
                                                     self.template_data_dir,
                                                     self.template_text_dict)
            data_AB_fields_dir = \
                directory_manager.pull_directory('AB_fields_dir')
            filename, extension = os.path.splitext(file)
            filename = filename[:-23]
            ohsu_nlp_template_manager.write_ab_fields(data_AB_fields_dir,
                                                      filename + '.txt')
            
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
    def ohsu_nlp_templates_push_AB_fields(self):
        static_data = self.static_data_manager.get_static_data()
        directory_manager = static_data['directory_manager']
        user = static_data['user']
        AB_fields_dir = \
            directory_manager.pull_directory('AB_fields_dir')
        linguamatics_i2e_manager = \
            self.nlp_tool_manager_registry.get_manager('linguamatics_i2e_manager')
        files = glob.glob(AB_fields_dir + '/**/*.txt', recursive=True)
        for i in range(len(files)):
            files[i] = re.sub(AB_fields_dir + '/', '', files[i])
        linguamatics_i2e_manager.login()
        for file in files:
            i2qy_file =  user + '/' + file[:-4] + '.i2qy'
            txt_file = AB_fields_dir + '/' + file
            linguamatics_i2e_manager.insert_field(i2qy_file, txt_file)
        linguamatics_i2e_manager.logout()
        
    #
    def ohsu_nlp_templates_run_simple_templates(self):
        static_data = self.static_data_manager.get_static_data()
        project_name = static_data['project_name']
        directory_manager = static_data['directory_manager']
        data_dir = directory_manager.pull_directory('postprocessing_data_in')
        ohsu_nlp_template_manager = \
            self.nlp_tool_manager_registry.get_manager('ohsu_nlp_template_manager')
        simple_templates_dir = \
            directory_manager.pull_directory('ohsu_nlp_project_simple_templates_dir')
        files = glob.glob(simple_templates_dir + '/*.py')
        for i in range(len(files)):
            files[i] = re.sub(simple_templates_dir + '/', '', files[i])
        for file in files:
            class_filename, extension = os.path.splitext(file)
            class_filename = re.sub('/', '.', class_filename)
            class_name, extension = os.path.splitext(os.path.basename(file))
            class_name = class_name[0].upper() + class_name[1:-6]
            import_cmd = 'from projects_lib.' + project_name + \
                         '.nlp_templates.simple_templates.' + class_filename + \
                         ' import ' + class_name + ' as Template_manager'
            exec(import_cmd, globals())
            print('OHSU NLP Template Manager: ' + class_name)
            template_manager = Template_manager(self.static_data_manager)
            ohsu_nlp_template_manager.clear_template_output()
            ohsu_nlp_template_manager.run_template(template_manager, 
                                                   self.template_text_dict)
            filename, extension = os.path.splitext(file)
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
    def postperformance(self):
        static_data = self.static_data_manager.get_static_data()
        if static_data['project_subdir'] == 'test':
            self.packaging_manager.create_postperformance_test_data_json()
        elif static_data['project_subdir'] == 'production':
            performance_data_files = static_data['performance_data_files']
            self.packaging_manager.create_postperformance_production_data_json(performance_data_files)

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
                    linguamatics_i2e_manager.generate_data_dict(data_dir, filename)
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
        document_identifier_list = []
        for i in range(len(raw_data_files)):
            filename, extension = os.path.splitext(raw_data_files[i])
            if extension.lower() in [ '.xls', '.xlsx' ]:
                xls_manager = \
                    self.xls_manager_registry[raw_data_files[i]]
                raw_data_in = xls_manager.read_file()
            elif extension.lower() in [ '.xml' ]:
                xml_manager = \
                    self.xml_manager_registry[raw_data_files[i]]
                raw_data_in = xml_manager.read_file()
            else:
                print('invalid file extension: ' + extension)
            raw_data = {}
            for document_identifier_key in static_data['document_identifiers']:
                if document_identifier_key in raw_data_in.keys():
                    for key in raw_data_in.keys():
                        raw_data[key] = []
                    for i in range(len(raw_data_in[document_identifier_key])):
                        if raw_data_in[document_identifier_key][i] not in document_identifier_list:
                            document_identifier_list.append(raw_data_in[document_identifier_key][i])
                            for key in raw_data_in.keys():
                                raw_data[key].append(raw_data_in[key][i])
            self.raw_data_manager.append_raw_data(raw_data)       
        self.raw_data_manager.partition_data()