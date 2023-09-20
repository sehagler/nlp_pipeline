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
import multiprocessing
import numpy as np
import os
import re
import traceback
import xml.etree.ElementTree as ET

#
from base_lib.manager_base_class import Manager_base
from nlp_pipeline_lib.manager_lib.dynamic_data_lib.dynamic_data_manager_class \
    import Dynamic_data_manager
from nlp_pipeline_lib.manager_lib.evaluation_lib.evaluation_manager_class \
    import Evaluation_manager
from nlp_pipeline_lib.manager_lib.file_lib.json_lib.json_manager_class \
    import Json_manager
from nlp_pipeline_lib.manager_lib.file_lib.xls_lib.xls_manager_class \
    import Xls_manager
from nlp_pipeline_lib.manager_lib.file_lib.xml_lib.xml_manager_class \
    import Xml_manager
from nlp_pipeline_lib.manager_lib.output_lib.output_manager_class \
    import Output_manager
from nlp_pipeline_lib.manager_lib.performance_data_lib.performance_data_manager_class \
    import Performance_data_manager
from nlp_pipeline_lib.manager_lib.raw_data_lib.raw_data_manager_class \
    import Raw_data_manager
from nlp_pipeline_lib.registry_lib.evaluator_registry_class \
    import Evaluator_registry
from nlp_pipeline_lib.registry_lib.nlp_tool_registry_class \
    import Nlp_tool_registry
from nlp_pipeline_lib.registry_lib.preprocessor_registry_class \
    import Preprocessor_registry
from nlp_text_normalization_lib.object_lib.text_normalization_object_class \
    import Text_normalization_object
from nlp_pipeline_lib.worker_lib.postprocessing_worker_class \
    import Postprocessing_worker
from nlp_pipeline_lib.worker_lib.preprocessing_worker_class \
    import Preprocessing_worker
from nlp_pipeline_lib.worker_lib.simple_template_worker_class \
    import Simple_template_worker
from specimens_lib.manager_lib.specimens_manager_class \
    import Specimens_manager
from tools_lib.processing_tools_lib.file_processing_tools \
    import read_txt_file, write_file
    
#
def _build_data_dictionary(data_dict):
    data_dict_list = []
    if bool(data_dict):
        for key in data_dict.keys():
            document_dict = {}
            document_dict['DOCUMENT_ID'] = key
            document_frame = []
            document_frame = _build_document_frame(data_dict[key])
            document_dict['DOCUMENT_FRAME'] = document_frame
            data_dict_list.append(document_dict)
    return data_dict_list
    
#
def _build_document_frame(data_list):
    document_frame = []
    for item in data_list:
        entry = []
        entry.append(tuple([item[1], item[2]]))
        entry.append(item[0])
        entry.append(item[3])
        document_frame.append(entry)
        num_elements = len(item) - 4
        for i in range(num_elements):
            entry.append(item[4+i])
    return document_frame
    
#
def _create_keywords_regexp(keywords):
    keywords_list = keywords.split('\n')
    keywords_list.remove('')
    keywords_regexp_str = '('
    for i in range(len(keywords_list)-1):
        keywords_regexp_str += keywords_list[i] + '|'
    keywords_regexp_str += keywords_list[-1] + ')'
    keywords_regexp = re.compile(keywords_regexp_str)
    return keywords_regexp

#
def _create_text_dict_preprocessing_data_out(data_dir, keywords_regexp):
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
            _parse_document(keywords_regexp, text)
    return text_dict

#
def _get_document_metadata(raw_data_manager, raw_data_files, i2e_version,
                           process_idx, start_idx, password):
    metadata = {}
    for data_file in raw_data_files:
        document_numbers = \
            raw_data_manager.get_document_numbers(data_file)
        for document_number in document_numbers:
            data_tmp, document_idx, source_metadata_list, \
            nlp_metadata_list, text_list, xml_metadata_list, \
            source_system = \
                raw_data_manager.get_data_by_document_number(data_file,
                                                             document_number,
                                                             i2e_version,
                                                             process_idx,
                                                             password)
            metadata[document_number] = {}
            metadata[document_number]['source_metadata'] = \
                source_metadata_list[0]
            metadata[document_number]['nlp_metadata'] = \
                nlp_metadata_list[0]
    return metadata

#
def _parse_document(keywords_regexp, text):
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
def _trim_data_by_document_list(data, document_identifiers, document_list):
    data_csn_list = []
    for document_identifier in document_identifiers:
        if document_identifier in data.keys():
            data_csn_list.extend(data[document_identifier])
    csn_list = []
    delete_idx_list = []
    for i in range(len(data_csn_list)):
        if (data_csn_list[i] in document_list and
            data_csn_list[i] not in csn_list):
            csn_list.append(data_csn_list[i])
        else:
            delete_idx_list.append(i)
    for key in data.keys():
        for i in sorted(delete_idx_list, reverse=True):
            del data[key][i]
    return data
    
#
def _trim_data_by_patient_list(data, patient_identifiers, patient_list):
    delete_idxs = []
    for key in patient_identifiers:
        if key in data.keys():
            patient_identifiers = data[key]
            for i in range(len(patient_identifiers)):
                if patient_identifiers[i] not in patient_list:
                    delete_idxs.append(i)
    delete_idxs.sort(reverse=True)
    for i in range(len(delete_idxs)):
        idx = delete_idxs[i]
        for key in data.keys():
            del data[key][idx]
    return data

#
def _trim_data_dict(data_dict_in, doc_list):
    doc_list = list(set(doc_list).intersection(set(list(data_dict_in.keys()))))
    data_dict_out = {}
    for doc in doc_list:
        data_dict_out[doc] = data_dict_in[doc]
    return data_dict_out

#
def _trim_sections(sections_in, doc_list):
    sections_out = []
    for i in range(len(sections_in)):
        if sections_in[i][0] in doc_list:
            sections_out.append(sections_in[i])
    return sections_out

#
class Process_manager(Manager_base):
    
    #
    def __init__(self, static_data_object, directory_object, logger_object,
                 metadata_manager, remote_registry, password):
        Manager_base.__init__(self, static_data_object, logger_object)
        self.directory_object = directory_object
        self.metadata_manager = metadata_manager
        self.password = password
        self._project_imports()
        self._create_registries(remote_registry, password)
        self._create_managers(password)
        self._push_directories()
        self._register_objects(password)
        self._create_workers()
        
        # Kludge to get around memory issue in processor
        linguamatics_i2e_object = \
            self.nlp_tool_registry.pull_object('linguamatics_i2e_object')
        self.i2e_version = \
            linguamatics_i2e_object.get_i2e_version(password)
        # Kludge to get around memory issue in processor
        
    #
    def _collect_performance_statistics_dict(self):
        static_data = self.static_data_object.get_static_data()
        performance_data_files = static_data['performance_data_files']
        #processing_base_dir = \
        #    directory_object.pull_directory('processing_base_dir')
        performance_statistics_dict = {}
        for filename in performance_data_files:
            #file = os.path.join(processing_base_dir, filename)
            performance_statistics_dict_tmp = \
                self.json_manager_registry[filename].read_performance_data()
            for key in performance_statistics_dict_tmp.keys():
                performance_statistics_dict[key] = \
                    performance_statistics_dict_tmp[key]
        return performance_statistics_dict
    
    #
    def _create_file_registries(self, password):
        static_data = self.static_data_object.get_static_data()
        self.xls_manager_registry = {}
        self.xml_manager_registry = {}
        for key in static_data['raw_data_files'].keys():
            filename, extension = os.path.splitext(key)
            if extension.lower() in [ '.xls', '.xlsx' ]:
                file = os.path.join(self.directory_object.pull_directory('raw_data_dir'), key)
                self.xls_manager_registry[file] = \
                    Xls_manager(self.static_data_object, self.logger_object,
                                file, password)
            elif extension.lower() in [ '.xml' ]:
                file = os.path.join(self.directory_object.pull_directory('raw_data_dir'), key)
                self.xml_manager_registry[file] = \
                    Xml_manager(self.static_data_object, self.logger_object,
                                file, password)
        files = glob.glob(self.directory_object.pull_directory('ab_fields_training_dir') + '/*.xlsx')
        for file in files:
            self.xls_manager_registry[file] = \
                Xls_manager(self.static_data_object, self.logger_object, file,
                            password)
        if static_data['project_subdir'] == 'test' and \
           'validation_file' in static_data.keys():
            validation_filename = static_data['validation_file']
            file = os.path.join(self.directory_object.pull_directory('raw_data_dir'), validation_filename)
            self.xls_manager_registry[file] = \
                Xls_manager(self.static_data_object, self.logger_object, file,
                            password)
    
    #
    def _create_managers(self, password):
        static_data = self.static_data_object.get_static_data()
        project_name = static_data['project_name']
        processing_base_dir = \
            self.directory_object.pull_directory('processing_base_dir')
        json_manager_registry = {}
        for key in [ 'performance_data_files', 'project_data_files' ]:
            for filename in static_data[key]:
                file = os.path.join(processing_base_dir, filename)
                json_manager_registry[filename] = \
                    Json_manager(self.static_data_object, self.logger_object,
                                 file)
        self.dynamic_data_manager = \
            Dynamic_data_manager(self.static_data_object, self.logger_object)
        self.evaluation_manager = \
            Evaluation_manager(self.static_data_object, self.logger_object,
                               self.evaluator_registry)
        self.output_manager = Output_manager(self.static_data_object,
                                             self.logger_object,
                                             self.metadata_manager)
        try:
            self.specimens_manager = \
                Specimens_manager(self.static_data_object, self.logger_object)
            log_text = 'Specimens_manager: ' + project_name + \
                       '_specimens_manager'
            self.logger_object.print_log(log_text)
        except Exception:
            traceback_text = traceback.format_exc()
            self.logger_object.print_exc(traceback_text)
        multiprocessing_flg = static_data['multiprocessing']
        if multiprocessing_flg:
            keys = list(static_data['raw_data_files'].keys())
            for key in keys:
                filename, extension = os.path.splitext(key)
        self.raw_data_manager = Raw_data_manager(self.static_data_object,
                                                 self.logger_object,
                                                 multiprocessing_flg,
                                                 password)
        
        # kludge to get postperformance() working
        self.json_manager_registry = json_manager_registry
        # kludge to get postperformance() working
        
        try:
            self.performance_data_manager = \
                Performance_data_manager(self.static_data_object,
                                         self.logger_object,
                                         self.evaluation_manager,
                                         self.json_manager_registry,
                                         self.metadata_manager,
                                         self.xls_manager_registry,
                                         self.specimens_manager)
            log_text = 'Performance_data_manager: ' + project_name + \
                       '_performance_data_manager'
            self.logger_object.print_log(log_text)
        except Exception:
            traceback_text = traceback.format_exc()
            self.logger_object.print_exc(traceback_text)
            
    #
    def _create_registries(self, remote_registry, password):
        static_data = self.static_data_object.get_static_data()
        self.evaluator_registry = Evaluator_registry(self.static_data_object,
                                                     self.logger_object)
        self.nlp_tool_registry = \
            Nlp_tool_registry(self.static_data_object, self.logger_object,
                              remote_registry)
        self.postprocessor_registry = \
            Postprocessor_registry(self.static_data_object, self.logger_object,
                                   self.metadata_manager)
        text_normalization_object = \
            Text_normalization_object(static_data['section_header_structure_tools'],
                                      static_data['remove_date'])
        self.preprocessor_registry = Preprocessor_registry(self.static_data_object,
                                                           self.logger_object)
        self.preprocessor_registry.push_text_normalization_object(text_normalization_object)
        self._create_file_registries(password)
                
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
    def _create_workers(self):
        num_processes = self.raw_data_manager.get_number_of_processes()
        self.preprocessing_dict = {}
        self.preprocessing_dict['processes'] = []
        self.preprocessing_dict['argument_queues'] = []
        self.preprocessing_dict['return_queues'] = []
        for process_idx in range(num_processes):
            aq = multiprocessing.Queue()
            rq = multiprocessing.Queue()
            w = Preprocessing_worker(self.static_data_object,
                                     self.logger_object,
                                     self.preprocessor_registry,
                                     self.nlp_tool_registry)
            p = multiprocessing.Process(target=w.process_data, args=(aq, rq,))
            self.preprocessing_dict['processes'].append(p)
            self.preprocessing_dict['argument_queues'].append(aq)
            self.preprocessing_dict['return_queues'].append(rq)
        self.postprocessing_dict = {}
        self.postprocessing_dict['processes'] = []
        self.postprocessing_dict['argument_queues'] = []
        self.postprocessing_dict['return_queues'] = []
        for process_idx in range(num_processes):
            aq = multiprocessing.Queue()
            rq = multiprocessing.Queue()
            w = Postprocessing_worker(self.static_data_object,
                                      self.logger_object,
                                      self.output_manager)
            p = multiprocessing.Process(target=w.process_data, args=(aq, rq,))
            self.postprocessing_dict['processes'].append(p)
            self.postprocessing_dict['argument_queues'].append(aq)
            self.postprocessing_dict['return_queues'].append(rq)
        self.simple_template_dict = {}
        self.simple_template_dict['processes'] = []
        self.simple_template_dict['argument_queues'] = []
        self.simple_template_dict['return_queues'] = []
        for process_idx in range(num_processes):
            ohsu_nlp_template_object = \
                self.nlp_tool_registry.pull_object('ohsu_nlp_template_object')
            aq = multiprocessing.Queue()
            rq = multiprocessing.Queue()
            w = Simple_template_worker(self.static_data_object,
                                       self.logger_object,
                                       ohsu_nlp_template_object)
            p = multiprocessing.Process(target=w.process_data, args=(aq, rq,))
            self.simple_template_dict['processes'].append(p)
            self.simple_template_dict['argument_queues'].append(aq)
            self.simple_template_dict['return_queues'].append(rq)
    
    #
    def _get_partitioned_document_list(self):
        static_data = self.static_data_object.get_static_data()
        docs_per_processor = static_data['docs_per_processor']
        num_processes = static_data['num_processes']
        data_dir = self.directory_object.pull_directory('postprocessing_data_in')
        linguamatics_i2e_object = \
            self.nlp_tool_registry.pull_object('linguamatics_i2e_object')
        sections_data_dict = \
            linguamatics_i2e_object.generate_data_dict(data_dir, 'sections.csv')
        doc_list = sections_data_dict.keys()
        doc_list = sorted(list(set(doc_list)))
        num_docs = len(doc_list)
        avg_docs_per_partition = num_docs / num_processes
        if avg_docs_per_partition <= docs_per_processor:
            rho = 1
        else:
            rho = avg_docs_per_partition // docs_per_processor
        partitioned_doc_array_list = np.array_split(doc_list, rho*num_processes)
        partitioned_doc_list = []
        for i in range(len(partitioned_doc_array_list)):
            partitioned_doc_list.append(partitioned_doc_array_list[i].tolist())
        return partitioned_doc_list
        
    #
    def _project_imports(self):
        static_data = self.static_data_object.get_static_data()
        project_name = static_data['project_name']
        import_cmd = 'from projects_lib.' + project_name + '.py.' + \
                     project_name.lower() + \
                     '_evaluation_manager_class import ' + project_name + \
                     '_evaluation_manager as Evaluation_manager'
        try:
            exec(import_cmd, globals())
        except Exception:
            traceback_text = traceback.format_exc()
            self.logger_object.print_exc(traceback_text)
        import_cmd = 'from projects_lib.' + project_name + '.py.' + \
                     project_name.lower() + \
                     '_performance_data_manager_class import ' + project_name + \
                     '_performance_data_manager as Performance_data_manager'
        try:
            exec(import_cmd, globals())
        except Exception:
            traceback_text = traceback.format_exc()
            self.logger_object.print_exc(traceback_text)
        try:
            import_cmd = 'from projects_lib.' + project_name + '.py.' + \
                         project_name.lower() + \
                         '_postprocessor_registry_class import ' + project_name + \
                         '_postprocessor_registry as Postprocessor_registry'
            exec(import_cmd, globals())
            log_text = 'Postprocessor_registry: ' + project_name + \
                       '_postprocessor_registry'
            self.logger_object.print_log(log_text)
        except Exception:
            traceback_text = traceback.format_exc()
            self.logger_object.print_exc(traceback_text)
            import_cmd = 'from nlp_pipeline_lib.registry_lib.postprocessor_registry_class import Postprocessor_registry'
            exec(import_cmd, globals())
            log_text = 'Postprocessor_registry: Postprocessor_registry'
            self.logger_object.print_log(log_text)
        try:
            import_cmd = 'from projects_lib.' + project_name + '.py.' + \
                         project_name.lower() + \
                         '_specimens_manager_class import ' + project_name + \
                         '_specimens_manager as Specimens_manager'
            exec(import_cmd, globals())
            log_text = 'Specimens_manager: ' + project_name + \
                       '_specimens_manager'
            self.logger_object.print_log(log_text)
        except Exception:
            traceback_text = traceback.format_exc()
            self.logger_object.print_exc(traceback_text)
            
    #
    def _push_directories(self):
        self.dynamic_data_manager.push_processing_data_dir(self.directory_object.pull_directory('processing_data_dir'))
        self.nlp_tool_registry.push_linguamatics_i2e_common_queries_directory(self.directory_object.pull_directory('linguamatics_i2e_common_queries_dir'))
        self.nlp_tool_registry.push_linguamatics_i2e_general_queries_directory(self.directory_object.pull_directory('linguamatics_i2e_general_queries_dir')) 
        self.nlp_tool_registry.push_linguamatics_i2e_project_queries_directory(self.directory_object.pull_directory('linguamatics_i2e_project_queries_dir'))
        self.nlp_tool_registry.push_linguamatics_i2e_preprocessing_data_out_directory(self.directory_object.pull_directory('linguamatics_i2e_preprocessing_data_out'))
        self.nlp_tool_registry.push_source_data_directory(self.directory_object.pull_directory('source_data'))
        self.nlp_tool_registry.push_processing_data_directory(self.directory_object.pull_directory('processing_data_dir'))
        self.output_manager.push_linguamatics_i2e_preprocessing_data_out_dir(self.directory_object.pull_directory('linguamatics_i2e_preprocessing_data_out'))
        self.output_manager.push_postprocessing_data_out_dir(self.directory_object.pull_directory('postprocessing_data_out'))
        self.postprocessor_registry.push_raw_data_directory(self.directory_object.pull_directory('raw_data_dir'))
        self.performance_data_manager.push_log_directory(self.directory_object.pull_directory('log_dir'))
        self.performance_data_manager.push_processing_data_directory(self.directory_object.pull_directory('processing_data_dir'))
        self.performance_data_manager.push_raw_data_directory(self.directory_object.pull_directory('raw_data_dir'))
        self.specimens_manager.push_log_directory(self.directory_object.pull_directory('log_dir'))
        self.specimens_manager.push_raw_data_directory(self.directory_object.pull_directory('raw_data_dir'))
        
    #
    def _register_objects(self, password):
        static_data = self.static_data_object.get_static_data()
        operation_mode = static_data['operation_mode']
        software_dir = \
            self.directory_object.pull_directory('software_dir')
        root_dir = \
            os.path.join(software_dir,
                         os.path.join(operation_mode,
                                      'query_lib/processor_lib'))
        log_text = root_dir
        self.logger_object.print_log(log_text)
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                file = os.path.basename(file)
                self.evaluator_registry.register_object(file)
                self.preprocessor_registry.register_object(file)
        self.nlp_tool_registry.register_linguamatics_i2e_object(password)
        self.nlp_tool_registry.register_nlp_template_object()
    
    #
    def _start_preprocessing_workers(self):
        for process_idx in range(len(self.preprocessing_dict['processes'])):
            log_text = 'Starting Preprocessing Worker ' + str(process_idx)
            self.logger_object.print_log(log_text)
            self.preprocessing_dict['processes'][process_idx].start()
                    
    #
    def _start_postprocessing_workers(self):
        for process_idx in range(len(self.postprocessing_dict['processes'])):
            log_text = 'Starting Postprocessing Worker ' + str(process_idx)
            self.logger_object.print_log(log_text)
            self.postprocessing_dict['processes'][process_idx].start()
            
    #
    def _start_simple_template_workers(self):
        for process_idx in range(len(self.simple_template_dict['processes'])):
            log_text = 'Starting Simple Template Worker ' + str(process_idx)
            self.logger_object.print_log(log_text)
            self.simple_template_dict['processes'][process_idx].start()
            
    #
    def _stop_preprocessing_workers(self):
        for process_idx in range(len(self.preprocessing_dict['processes'])):
            log_text = 'Stopping Preprocessing Worker ' + str(process_idx)
            self.logger_object.print_log(log_text)
            argument_dict = {}
            argument_dict['command'] = 'stop'
            self.preprocessing_dict['argument_queues'][process_idx].put(argument_dict)
            self.preprocessing_dict['processes'][process_idx].join()
            
    #
    def _stop_postprocessing_workers(self):
        for process_idx in range(len(self.postprocessing_dict['processes'])):
            log_text = 'Stopping Postprocessing Worker ' + str(process_idx)
            self.logger_object.print_log(log_text)
            argument_dict = {}
            argument_dict['command'] = 'stop'
            self.postprocessing_dict['argument_queues'][process_idx].put(argument_dict)
            self.postprocessing_dict['processes'][process_idx].join()
            
    #
    def _stop_simple_template_workers(self):
        for process_idx in range(len(self.postprocessing_dict['processes'])):
            log_text = 'Stopping Simple Template Worker ' + str(process_idx)
            self.logger_object.print_log(log_text)
            argument_dict = {}
            argument_dict['command'] = 'stop'
            self.simple_template_dict['argument_queues'][process_idx].put(argument_dict)
            self.simple_template_dict['processes'][process_idx].join()
            
    #
    def calculate_performance(self):
        display_flg = True
        self.performance_data_manager.get_performance_data(display_flg)
        self.performance_data_manager.display_performance_statistics()
        self.performance_data_manager.write_performance_data()
        self.performance_data_manager.generate_csv_file()
            
    #
    def cleanup_directory(self, directory_label):
        self.directory_object.cleanup_directory(directory_label)
        
    #
    def linguamatics_i2e_generate_csv_files(self):
        linguamatics_i2e_object = \
            self.nlp_tool_registry.pull_object('linguamatics_i2e_object')
        linguamatics_i2e_object.generate_csv_files(self.directory_object.pull_directory('postprocessing_data_in'))
    
    #
    def linguamatics_i2e_indexer(self):
        static_data = self.static_data_object.get_static_data()
        project_name = static_data['project_name']
        now = datetime.datetime.now()
        self.index_start_datetime = now.strftime("%d-%b-%y %H:%M:%S.%f")[:-3]
        linguamatics_i2e_object = \
            self.nlp_tool_registry.pull_object('linguamatics_i2e_object')
        linguamatics_i2e_object.login()
        linguamatics_i2e_object.make_index_runner(project_name)
        linguamatics_i2e_object.logout()
        now = datetime.datetime.now()
        self.index_end_datetime = now.strftime("%d-%b-%y %H:%M:%S.%f")[:-3]
        
    #
    def linguamatics_i2e_postindexer(self):
        self.metadata_manager.load_metadata()
        self.metadata_manager.append_nlp_metadata_value('DOCUMENT_SET_INDEXING_START_DATETIME',
                                                        self.index_start_datetime)
        self.metadata_manager.append_nlp_metadata_value('DOCUMENT_SET_INDEXING_END_DATETIME',
                                                        self.index_end_datetime)
        self.metadata_manager.save_metadata()
        
    #
    def linguamatics_i2e_push_resources(self):
        static_data = self.static_data_object.get_static_data()
        project_name = static_data['project_name']
        keywords_file = self.dynamic_data_manager.keywords_file()
        max_files_per_zip = static_data['max_files_per_zip']
        root_dir_flg = static_data['root_dir_flg']
        linguamatics_i2e_object = \
            self.nlp_tool_registry.pull_object('linguamatics_i2e_object')
        linguamatics_i2e_object.generate_regions_file()
        linguamatics_i2e_object.generate_xml_configuation_file()
        linguamatics_i2e_object.login()
        linguamatics_i2e_object.push_resources(project_name, keywords_file,
                                               max_files_per_zip, root_dir_flg)
        linguamatics_i2e_object.logout()
        
    #
    def linguamatics_i2e_push_queries(self):
        static_data = self.static_data_object.get_static_data()
        max_files_per_zip = static_data['max_files_per_zip']
        project_name = static_data['project_name']
        linguamatics_i2e_object = \
            self.nlp_tool_registry.pull_manager('linguamatics_i2e_object')
        linguamatics_i2e_object.generate_query_bundle_file(project_name,
                                                           max_files_per_zip)
        linguamatics_i2e_object.fix_queries()
        linguamatics_i2e_object.login()
        linguamatics_i2e_object.push_queries()
        linguamatics_i2e_object.logout()
        
    #
    def ohsu_nlp_templates_generate_AB_fields(self):
        static_data = self.static_data_object.get_static_data()
        project_name = static_data['project_name']
        ohsu_nlp_template_object = \
            self.nlp_tool_registry.pull_manager('ohsu_nlp_template_object')
        if 'sections.csv' in os.listdir(self.directory_object.pull_directory('postprocessing_data_in')):
            sections = []
            with open(os.path.join(self.directory_object.pull_directory('postprocessing_data_in'), 'sections.csv')) as f:
                csv_reader = csv.reader(f)
                for row in csv_reader:
                    sections.append(row)
            text_dict = _create_text_dict_postprocessing_data_in(sections)
        else:
            text_dict = None
        self.template_data_dir = self.directory_object.pull_directory('postprocessing_data_in')
        self.template_text_dict = text_dict
        files = \
            glob.glob(self.directory_object.pull_directory('ohsu_nlp_project_AB_fields_dir') + '/**/*.py', recursive=True)
        for i in range(len(files)):
            files[i] = re.sub(self.directory_object.pull_directory('ohsu_nlp_project_AB_fields_dir') + '/', '', files[i])
        for file in files:
            class_filename, extension = os.path.splitext(file)
            filename = class_filename[:-32]
            class_filename = re.sub('/', '.', class_filename)
            class_name, extension = os.path.splitext(os.path.basename(file))
            class_name = class_name[0].upper() + class_name[1:-6]
            import_cmd = 'from projects_lib.' + project_name + \
                         '.nlp_templates.AB_fields.' + class_filename + \
                         ' import ' + class_name + ' as Template_object'
            exec(import_cmd, globals())
            print('OHSU NLP Template Object: ' + class_name)
            template_object = Template_object()
            template_object.push_template_outlines_directory(self.directory_object.pull_directory('template_outlines_dir'))
            AB_fields_training_file = \
                static_data['AB_fields_training_files'][filename]
            AB_fields_training_file = \
                os.path.join(self.directory_object.pull_directory('ab_fields_training_dir'), 
                             AB_fields_training_file)
            xls_manager = \
                self.xls_manager_registry[AB_fields_training_file]
            xls_manager.read_training_data()
            template_object.push_xls_manager(xls_manager)
            ohsu_nlp_template_object.clear_template_output()
            ohsu_nlp_template_object.train_ab_fields(template_object,
                                                      self.metadata_manager,
                                                      self.template_data_dir,
                                                      self.template_text_dict)
            filedir = self.directory_object.pull_directory('ab_fields_text_dir')
            filedir += '/' + filename + '_AB_fields'
            if not os.path.exists(filedir):
                os.mkdir(filedir)
            ohsu_nlp_template_object.write_ab_fields(filedir, filename)
            
    #
    def ohsu_nlp_templates_push_AB_fields(self):
        static_data = self.static_data_object.get_static_data()
        user = static_data['user']
        linguamatics_i2e_object = \
            self.nlp_tool_registry.pull_object('linguamatics_i2e_object')
        linguamatics_i2e_object.login()
        for ab_fields_dir in os.listdir(self.directory_object.pull_directory('ab_fields_text_dir')):
            filename = ab_fields_dir[:-10]
            for field in [ '_AB_field', '_BA_field' ]:
                i2qy_file =  user + '/AB_fields/' + filename + \
                             '_AB_fields/' + filename + field + '.i2qy'
                txt_file = self.directory_object.pull_directory('ab_fields_text_dir') + \
                           '/' + ab_fields_dir + '/' + filename + field + '.txt'
                linguamatics_i2e_object.insert_field(i2qy_file, txt_file) 
        linguamatics_i2e_object.logout()
        
    #
    def ohsu_nlp_templates_run_simple_templates(self):
        static_data = self.static_data_object.get_static_data()
        num_processes = static_data['num_processes']
        project_name = static_data['project_name']
        #ohsu_nlp_template_object = \
        #    self.nlp_tool_registry.pull_object('ohsu_nlp_template_object')
        files = glob.glob(self.directory_object.pull_directory('ohsu_nlp_project_simple_templates_dir') + '/*.py')
        for i in range(len(files)):
            files[i] = \
                re.sub(self.directory_object.pull_directory('ohsu_nlp_project_simple_templates_dir') + '/', '', files[i])
        if len(files) > 0:
            self._start_simple_template_workers()
            sections = []
            if 'sections.csv' in os.listdir(self.directory_object.pull_directory('postprocessing_data_in')):
                with open(os.path.join(self.directory_object.pull_directory('postprocessing_data_in'), 'sections.csv')) as f:
                    csv_reader = csv.reader(f)
                    for row in csv_reader:
                        sections.append(row)
            for file in files:
                class_filename, extension = os.path.splitext(file)
                class_filename = re.sub('/', '.', class_filename)
                class_name, extension = os.path.splitext(os.path.basename(file))
                class_name = class_name[0].upper() + class_name[1:-6]
                import_cmd = 'from projects_lib.' + project_name + \
                             '.nlp_templates.simple_templates.' + class_filename + \
                             ' import ' + class_name + ' as Template_object'
                exec(import_cmd, globals())
                log_text = 'OHSU NLP Template Object: ' + class_name
                self.logger_object.print_log(log_text)
                template_object = Template_object()
                partitioned_doc_list = self._get_partitioned_document_list()
                num_worker_runs = len(partitioned_doc_list) // num_processes
                template_output = []
                for n in range(num_worker_runs):
                    for process_idx in range(len(self.simple_template_dict['processes'])):
                        doc_list = partitioned_doc_list[process_idx + n*num_processes]
                        sections_copy = deepcopy(sections)
                        sections_copy = _trim_sections(sections_copy, doc_list)
                        argument_dict = {}
                        argument_dict['doc_list'] = partitioned_doc_list[process_idx]
                        argument_dict['process_idx'] = process_idx
                        argument_dict['sections'] = sections_copy
                        argument_dict['template_object'] = template_object
                        self.simple_template_dict['argument_queues'][process_idx].put(argument_dict)
                    for process_idx in range(len(self.simple_template_dict['processes'])):
                        return_dict = \
                            self.simple_template_dict['return_queues'][process_idx].get()
                        template_output.extend(return_dict['template_output'])
                filename, extension = os.path.splitext(file)
                filename = re.sub('_simple_template_object_class', '', filename)
                csv_filename = filename + '.csv'
                template_dict = template_object.simple_template()
                template_headers = template_dict['template_headers']
                header = [ 'DOCUMENT_ID', 'DATETIME', 'Section Title', 'Specimen Id' ]
                for i in range(len(template_headers)):
                    header.append(template_headers[i])
                #header.append('Snippet')
                header.append('Coords')
                with open(os.path.join(self.directory_object.pull_directory('postprocessing_data_in'), csv_filename), 'w', encoding='UTF8', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(header)
                    writer.writerows(template_output)
            self._stop_simple_template_workers()
        
    #
    def postperformance(self):
        static_data = self.static_data_object.get_static_data()
        if static_data['project_subdir'] == 'production':
            performance_statistics_dict = \
                self._collect_performance_statistics_dict()
            filename = static_data['project_name'] + '/' + \
                       static_data['project_subdir'] + '/' + \
                       static_data['project_name'] + '.json'
            documents_wrapper = \
                self.json_manager_registry[filename].read_json_file()
            for i in range(len(documents_wrapper[self.documents_wrapper_key])):
                nlp_data = \
                    documents_wrapper[self.documents_wrapper_key][i][self.document_wrapper_key][self.nlp_data_key]
                query_list = []
                for nlp_datum in nlp_data:
                    if self.nlp_query_key in nlp_datum[self.nlp_datum_key].keys():
                        query_list.append(nlp_datum[self.nlp_datum_key][self.nlp_query_key])
                query_list = list(set(query_list))
                #performance_statistics_dict_tmp = []
                tmp_dict = {}
                for key in performance_statistics_dict.keys():
                    if key in query_list:
                        tmp_dict = performance_statistics_dict[key]
                        tmp_dict['QUERY'] = key
                if tmp_dict:    
                    documents_wrapper[self.documents_wrapper_key][i][self.document_wrapper_key][self.nlp_performance_key] = \
                        static_data['project_name'] + '.performance.json'
            production_data_file = self.directory_object.pull_directory('production_data_dir')  + '/' + \
                                   static_data['project_name'] + '.json'                     
            write_file(production_data_file, documents_wrapper, True, True)
            performance_data_file = self.directory_object.pull_directory('production_data_dir')  + '/' + \
                                    static_data['project_name'] + '.performance.json'
            write_file(performance_data_file, performance_statistics_dict, False, False)

    #
    def postprocessor(self):
        static_data = self.static_data_object.get_static_data()
        num_processes = static_data['num_processes']
        file_list = os.listdir(self.directory_object.pull_directory('postprocessing_data_in'))
        linguamatics_i2e_object = \
            self.nlp_tool_registry.pull_object('linguamatics_i2e_object')
        if static_data['project_subdir'] == 'test' and \
           'test_postprocessing_data_in_files' in static_data.keys():
            file_list = \
                list(set(file_list).intersection(static_data['test_postprocessing_data_in_files']))
        for filename in file_list:
            filename_base, extension = os.path.splitext(filename)
            if extension in [ '.csv' ]:
                self.postprocessor_registry.register_object(filename)
        partitioned_doc_list = self._get_partitioned_document_list()
        num_worker_runs = len(partitioned_doc_list) // num_processes
        self._start_postprocessing_workers()
        data_dict_dict = {}
        for filename in file_list:
            filename_base, extension = os.path.splitext(filename)
            if extension in [ '.csv' ]:
                data_dict = \
                    linguamatics_i2e_object.generate_data_dict(self.directory_object.pull_directory('postprocessing_data_in'),
                                                               filename)
                data_dict_dict[filename_base] = data_dict
        for n in range(num_worker_runs):
            for process_idx in range(len(self.postprocessing_dict['processes'])):
                doc_list = partitioned_doc_list[process_idx + n*num_processes]
                data_dict_dict_copy = deepcopy(data_dict_dict)
                for key in data_dict_dict_copy.keys():
                    data_dict_dict_copy[key] = \
                        _trim_data_dict(data_dict_dict_copy[key], doc_list)
                json_manager_registry_copy = deepcopy(self.json_manager_registry)
                postprocessor_registry_copy = deepcopy(self.postprocessor_registry)
                argument_dict = {}
                argument_dict['data_dict_dict'] = data_dict_dict_copy
                argument_dict['doc_list'] = doc_list
                argument_dict['filename'] = filename
                argument_dict['file_list'] = file_list
                argument_dict['json_manager_registry'] = \
                    json_manager_registry_copy
                argument_dict['nlp_data_key'] = self.nlp_data_key
                argument_dict['postprocessor_registry'] = \
                    postprocessor_registry_copy
                argument_dict['postprocessing_data_out'] = \
                    self.directory_object.pull_directory('postprocessing_data_out')
                argument_dict['process_idx'] = process_idx
                argument_dict['processing_base_dir'] = \
                    self.directory_object.pull_directory('processing_base_dir')
                self.postprocessing_dict['argument_queues'][process_idx].put(argument_dict)
            for process_idx in range(len(self.postprocessing_dict['processes'])):
                self.postprocessing_dict['return_queues'][process_idx].get()
        self._stop_postprocessing_workers()
        
    #
    def preperformance(self):
        static_data = self.static_data_object.get_static_data()
        data = {}
        for filename in os.listdir(self.directory_object.pull_directory('postprocessing_data_out')):
            json_file = Json_manager(self.static_data_object, 
                                     self.logger_object,
                                     os.path.join(self.directory_object.pull_directory('postprocessing_data_out'),
                                                  filename))
            key = filename[0:-5]
            data[key] = json_file.read_json_file()
        filename = static_data['project_name'] + '/' + \
                   static_data['project_subdir'] + '/' + \
                   static_data['project_name'] + '.json'
        self.json_manager_registry[filename].write_performance_data_to_package_json_file(data)
    
    #
    def preprocessor_full(self, password):
        static_data = self.static_data_object.get_static_data()
        raw_data_files_dict = static_data['raw_data_files']
        if 'raw_data_files_sequence' in static_data.keys():
            raw_data_files_seq = static_data['raw_data_files_sequence']
        else:
            raw_data_files_seq = None
        if raw_data_files_seq is None:
            raw_data_files_seq = list(raw_data_files_dict.keys())
        raw_data_files = []
        for i in range(len(raw_data_files_seq)):
            raw_data_files.append(os.path.join(self.directory_object.pull_directory('raw_data_dir'),
                                  raw_data_files_seq[i]))            
        num_docs_preprocessed = 0
        self.metadata_manager.load_metadata()
        doc_idx_offset = self.metadata_manager.get_doc_idx_offset()
        self.metadata_manager.clear_metadata()
        self._start_preprocessing_workers()
        for i in range(len(raw_data_files)):
            filename, extension = os.path.splitext(raw_data_files[i])
            if extension.lower() in [ '.xls', '.xlsx' ]:
                xls_manager = self.xls_manager_registry[raw_data_files[i]]
                raw_data = xls_manager.read_file()
            elif extension.lower() in [ '.xml' ]:
                xml_manager =  self.xml_manager_registry[raw_data_files[i]]
                raw_data = xml_manager.read_file()
            else:
                log_text = 'invalid file extension: ' + extension  
                self.logger_object.print_log(log_text)
            if 'document_list' in static_data:
                document_list = static_data['document_list']
                document_identifiers = static_data['document_identifiers']
                raw_data = _trim_data_by_document_list(raw_data,
                                                       document_identifiers,
                                                       document_list)
            if 'patient_list' in static_data:
                patient_list = static_data['patient_list']
                patient_identifiers = static_data['patient_identifiers']
                raw_data = _trim_data_by_patient_list(raw_data, 
                                                      patient_identifiers,
                                                      patient_list)
            self.raw_data_manager.clear_raw_data()
            self.raw_data_manager.append_raw_data(raw_data) 
            doc_idx_offset = \
                self.raw_data_manager.partition_data(doc_idx_offset)
            self.raw_data_manager.print_num_of_docs_in_preprocessing_set()
            for process_idx in range(len(self.preprocessing_dict['processes'])):
                dynamic_data_manager_copy = deepcopy(self.dynamic_data_manager)
                raw_data_manager_copy = deepcopy(self.raw_data_manager)
                raw_data_manager_copy.select_process(process_idx)
                metadata_manager_copy = deepcopy(self.metadata_manager)
                argument_dict = {}
                argument_dict['dynamic_data_manager'] = \
                    dynamic_data_manager_copy
                argument_dict['linguamatics_i2e_preprocessing_data_out_dir'] = \
                    self.directory_object.pull_directory('linguamatics_i2e_preprocessing_data_out')
                argument_dict['metadata_manager'] = metadata_manager_copy
                argument_dict['num_processes'] = \
                    len(self.preprocessing_dict['processes'])
                argument_dict['process_idx'] = process_idx
                argument_dict['raw_data_manager'] = raw_data_manager_copy
                argument_dict['start_idx'] = 0
                argument_dict['i2e_version'] = self.i2e_version
                argument_dict['password'] = password
                self.preprocessing_dict['argument_queues'][process_idx].put(argument_dict)
            for process_idx in range(len(self.preprocessing_dict['processes'])):
                return_dict = \
                    self.preprocessing_dict['return_queues'][process_idx].get()
                dynamic_data_manager = return_dict['dynamic_data_manager']
                document_dict = return_dict['document_dict']
                metadata_manager = return_dict['metadata_manager']
                if len(document_dict.keys()) > 0:
                    self.dynamic_data_manager.merge_copy(dynamic_data_manager)
                    self.metadata_manager.load_metadata()
                    self.metadata_manager.merge_copy(metadata_manager)
                    self.metadata_manager.save_metadata()
                    self.metadata_manager.clear_metadata()
                    num_docs_preprocessed += len(document_dict.keys())
        self._stop_preprocessing_workers()
        log_text = 'Number of documents preprocessed: ' + \
                   str(num_docs_preprocessed)
        self.logger_object.print_log(log_text)
        self.dynamic_data_manager.generate_keywords_file()
        
    #
    def preprocessor_metadata(self, password, start_idx):
        static_data = self.static_data_object.get_static_data()
        num_processes = self.raw_data_manager.get_number_of_processes()
        raw_data_files_dict = static_data['raw_data_files']
        if 'raw_data_files_sequence' in static_data.keys():
            raw_data_files_seq = static_data['raw_data_files_sequence']
        else:
            raw_data_files_seq = None
        if raw_data_files_seq is None:
            raw_data_files_seq = list(raw_data_files_dict.keys())
        raw_data_files = []
        for i in range(len(raw_data_files_seq)):
            raw_data_files.append(os.path.join(self.directory_object.pull_directory('raw_data_dir'),
                                               raw_data_files_seq[i]))
        self.metadata_manager.load_metadata()
        doc_idx_offset = self.metadata_manager.get_doc_idx_offset()
        self.metadata_manager.clear_metadata()
        for i in range(len(raw_data_files)):
            filename, extension = os.path.splitext(raw_data_files[i])
            if extension.lower() in [ '.xls', '.xlsx' ]:
                xls_manager = \
                    self.xls_manager_registry[raw_data_files[i]]
                raw_data = xls_manager.read_file()
            elif extension.lower() in [ '.xml' ]:
                xml_manager = \
                    self.xml_manager_registry[raw_data_files[i]]
                raw_data = xml_manager.read_file()
            else:
                log_text = 'invalid file extension: ' + extension
                self.logger_object.print_log(log_text)
            if 'document_list' in static_data:
                document_list = static_data['document_list']
                document_identifiers = static_data['document_identifiers']
                raw_data = _trim_data_by_document_list(raw_data,
                                                       document_identifiers,
                                                       document_list)
            if 'patient_list' in static_data:
                patient_list = static_data['patient_list']
                patient_identifiers = static_data['patient_identifiers']
                raw_data = _trim_data_by_patient_list(raw_data, 
                                                      patient_identifiers,
                                                      patient_list)
            self.raw_data_manager.clear_raw_data()
            self.raw_data_manager.append_raw_data(raw_data) 
            doc_idx_offset = \
                self.raw_data_manager.partition_data(doc_idx_offset)
            self.raw_data_manager.print_num_of_docs_in_preprocessing_set()
            for process_idx in range(num_processes):
                raw_data_manager_copy = deepcopy(self.raw_data_manager)
                raw_data_manager_copy.select_process(process_idx)
                raw_data_files = list(raw_data_files_dict.keys())
                metadata = \
                    _get_document_metadata(raw_data_manager_copy, 
                                           raw_data_files, self.i2e_version,
                                           process_idx, start_idx, password)
                for document_idx in metadata.keys():
                    self.metadata_manager.load_metadata()
                    self.metadata_manager.append_metadata_dicts(str(document_idx),
                                                                metadata[document_idx]['source_metadata'],
                                                                metadata[document_idx]['nlp_metadata'])
                    self.metadata_manager.save_metadata()
                    self.metadata_manager.clear_metadata()
                num_docs_preprocessed = 0
        log_text = 'Number of documents preprocessed: ' + \
                   str(num_docs_preprocessed)
        self.logger_object.print_log(log_text)