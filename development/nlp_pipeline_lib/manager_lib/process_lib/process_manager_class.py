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
import plotext as plt
import multiprocessing
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
from nlp_pipeline_lib.manager_lib.metadata_lib.metadata_manager_class \
    import Metadata_manager
from nlp_pipeline_lib.manager_lib.output_lib.output_manager_class \
    import Output_manager
from nlp_pipeline_lib.manager_lib.raw_data_lib.raw_data_manager_class \
    import Raw_data_manager
from nlp_pipeline_lib.registry_lib.nlp_tool_lib.nlp_tool_registry_class \
    import Nlp_tool_registry
from nlp_text_normalization_lib.object_lib.text_normalization_object_class \
    import Text_normalization_object
from processor_lib.registry_lib.preprocessor_registry_class \
    import Preprocessor_registry
from nlp_pipeline_lib.worker_lib.preprocessing_lib.preprocessing_worker_class \
    import Preprocessing_worker
from tools_lib.processing_tools_lib.file_processing_tools \
    import read_json_file, read_txt_file, write_file
    
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
def _create_text_dict_postprocessing_data_in(sections):
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
class Process_manager(Manager_base):
    
    #
    def __init__(self, static_data_object, remote_registry, password):
        Manager_base.__init__(self, static_data_object)
        self.password = password
        self._project_imports()
        self._create_managers(remote_registry, password)
        
        # Kludge to get around memory issue in processor
        linguamatics_i2e_object = \
            self.nlp_tool_registry.get_manager('linguamatics_i2e_object')
        self.i2e_version = \
            linguamatics_i2e_object.get_i2e_version(password)
        # Kludge to get around memory issue in processor    
    
    #
    def _create_managers(self, remote_registry, password):
        static_data = self.static_data_object.get_static_data()
        directory_manager = static_data['directory_manager']
        project_name = static_data['project_name']
        project_AB_fields_dir = \
            directory_manager.pull_directory('ohsu_nlp_project_AB_fields_dir')
        processing_base_dir = \
            directory_manager.pull_directory('processing_base_dir')
        raw_data_dir = \
            directory_manager.pull_directory('raw_data_dir')
        json_manager_registry = {}
        for key in [ 'performance_data_files', 'project_data_files' ]:
            for filename in static_data[key]:
                file = os.path.join(processing_base_dir, filename)
                json_manager_registry[filename] = \
                    Json_manager(self.static_data_object, file)
        self.xls_manager_registry = {}
        self.xml_manager_registry = {}
        for key in static_data['raw_data_files'].keys():
            filename, extension = os.path.splitext(key)
            if extension.lower() in [ '.xls', '.xlsx' ]:
                file = os.path.join(raw_data_dir, key)
                self.xls_manager_registry[file] = \
                    Xls_manager(self.static_data_object, file, password)
            elif extension.lower() in [ '.xml' ]:
                file = os.path.join(raw_data_dir, key)
                self.xml_manager_registry[file] = \
                    Xml_manager(self.static_data_object, file, password)
        for file in os.listdir(project_AB_fields_dir):
            class_filename, extension = os.path.splitext(file)
            class_filename = re.sub('/', '.', class_filename)
            class_name, extension = os.path.splitext(os.path.basename(file))
            class_name = class_name[0].upper() + class_name[1:-6]
            import_cmd = 'from projects_lib.' + project_name + \
                         '.nlp_templates.AB_fields.' + class_filename + \
                         ' import ' + class_name + ' as Template_manager'
            exec(import_cmd, globals())
            print('OHSU NLP Template Manager: ' + class_name)
            template_manager = Template_manager(self.static_data_object)
            training_data_file = template_manager.pull_training_data_file()
            file = os.path.join(raw_data_dir, training_data_file)
            self.xls_manager_registry[file] = \
                Xls_manager(self.static_data_object, file, password) 
        if static_data['project_subdir'] == 'test' and \
           'validation_file' in static_data.keys():
            validation_filename = static_data['validation_file']
            file = os.path.join(raw_data_dir, validation_filename)
            self.xls_manager_registry[file] = \
                Xls_manager(self.static_data_object, file, password)
        self.dynamic_data_manager = \
            Dynamic_data_manager(self.static_data_object)
        evaluation_manager = \
            Evaluation_manager(self.static_data_object)
        self.metadata_manager = Metadata_manager(self.static_data_object)
        self.nlp_tool_registry = \
            Nlp_tool_registry(self.static_data_object, remote_registry,
                              password)
        try:
            self.performance_data_manager = \
                Performance_data_manager(self.static_data_object,
                                         evaluation_manager,
                                         json_manager_registry,
                                         self.metadata_manager,
                                         self.xls_manager_registry)
            print('Performance_data_manager: ' + project_name + '_performance_data_manager')
        except Exception:
            traceback.print_exc()
            self.performance_data_manager = None
        self.postprocessor_registry = \
            Postprocessor_registry(self.static_data_object,
                                   self.metadata_manager)
        text_normalization_object = \
            Text_normalization_object(static_data['section_header_structure_tools'],
                                      static_data['remove_date'])
        self.preprocessor_registry = Preprocessor_registry(static_data)
        self.preprocessor_registry.push_text_normalization_object(text_normalization_object)
        self.preprocessor_registry.create_preprocessors()
        self.output_manager = Output_manager(self.static_data_object, 
                                             self.metadata_manager)
        
        multiprocessing_flg = static_data['multiprocessing']
        if multiprocessing_flg:
            keys = list(static_data['raw_data_files'].keys())
            for key in keys:
                filename, extension = os.path.splitext(key)
        self.raw_data_manager = Raw_data_manager(self.static_data_object, 
                                                 multiprocessing_flg,
                                                 password)
        
        # kludge to get postperformance() working
        self.json_manager_registry = json_manager_registry
        # kludge to get postperformance() working
        
    #
    def _collect_performance_statistics_dict(self):
        static_data = self.static_data_object.get_static_data()
        #directory_manager = static_data['directory_manager']
        performance_data_files = static_data['performance_data_files']
        #processing_base_dir = \
        #    directory_manager.pull_directory('processing_base_dir')
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
    def _documents_by_year(self):
        static_data = self.static_data_object.get_static_data()
        #datetime_keys = {}
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
    def _get_document_metadata(self, raw_data_manager, i2e_version, 
                               process_idx, start_idx, password):
        metadata = {}
        static_data = self.static_data_object.get_static_data()
        raw_data_files_dict = static_data['raw_data_files']
        raw_data_files = list(raw_data_files_dict.keys())
        document_dict = {}
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
    def _ohsu_nlp_templates_generate_AB_fields(self):
        static_data = self.static_data_object.get_static_data()
        project_name = static_data['project_name']
        directory_manager = static_data['directory_manager']
        ohsu_nlp_template_manager = \
            self.nlp_tool_registry.get_manager('ohsu_nlp_template_manager')
        project_AB_fields_dir = \
            directory_manager.pull_directory('ohsu_nlp_project_AB_fields_dir')
        for file in os.listdir(project_AB_fields_dir):
            class_filename, extension = os.path.splitext(file)
            class_filename = re.sub('/', '.', class_filename)
            class_name, extension = os.path.splitext(os.path.basename(file))
            class_name = class_name[0].upper() + class_name[1:-6]
            import_cmd = 'from projects_lib.' + project_name + \
                         '.nlp_templates.AB_fields.' + class_filename + \
                         ' import ' + class_name + ' as Template_manager'
            exec(import_cmd, globals())
            print('OHSU NLP Template Manager: ' + class_name)
            template_manager = Template_manager(self.static_data_object)
            training_data_file = template_manager.pull_training_data_file()
            training_data_file = \
                os.path.join(static_data['directory_manager'].pull_directory('raw_data_dir'),
                             training_data_file)
            xls_manager = self.xls_manager_registry[training_data_file]
            xls_manager.read_training_data()
            template_manager.push_xls_manager(xls_manager)
            ohsu_nlp_template_manager.train_ab_fields(template_manager,
                                                      self.metadata_manager,
                                                      self.template_data_dir,
                                                      self.template_text_dict)
            data_AB_fields_dir = \
                directory_manager.pull_directory('AB_fields_dir')
            filename, extension = os.path.splitext(file)
            filename = re.sub('_AB_fields_template_manager_class', '', filename)
            ohsu_nlp_template_manager.write_ab_fields(data_AB_fields_dir,
                                                      filename)
            
    #
    def _ohsu_nlp_templates_push_AB_fields(self):
        static_data = self.static_data_object.get_static_data()
        project_name = static_data['project_name']
        directory_manager = static_data['directory_manager']
        user = static_data['user']
        AB_fields_dir = \
            directory_manager.pull_directory('AB_fields_dir')
        linguamatics_i2e_object = \
            self.nlp_tool_registry.get_manager('linguamatics_i2e_object')
        project_AB_fields_dir = \
            directory_manager.pull_directory('ohsu_nlp_project_AB_fields_dir')
        linguamatics_i2e_object.login()
        for file in os.listdir(project_AB_fields_dir):
            class_filename, extension = os.path.splitext(file)
            class_filename = re.sub('/', '.', class_filename)
            class_name, extension = os.path.splitext(os.path.basename(file))
            class_name = class_name[0].upper() + class_name[1:-6]
            import_cmd = 'from projects_lib.' + project_name + \
                         '.nlp_templates.AB_fields.' + class_filename + \
                         ' import ' + class_name + ' as Template_manager'
            exec(import_cmd, globals())
            print('OHSU NLP Template Manager: ' + class_name)
            template_manager = Template_manager(self.static_data_object)
            '''
            training_data_file = template_manager.pull_training_data_file()
            training_data_file = \
                os.path.join(static_data['directory_manager'].pull_directory('raw_data_dir'),
                             training_data_file)
            xls_manager = self.xls_manager_registry[training_data_file]
            xls_manager.read_training_data()
            '''
            linguamatics_i2e_AB_fields_path = \
                template_manager.pull_linguamatics_i2e_AB_fields_path()
            data_AB_fields_dir = \
                directory_manager.pull_directory('AB_fields_dir')
            filename, extension = os.path.splitext(file)
            filename = re.sub('_AB_fields_template_manager_class', '', filename)
            for field in [ '_AB_field', '_BA_field' ]:
                i2qy_file =  user + '/' + linguamatics_i2e_AB_fields_path + \
                             '/' + filename + field + '.i2qy'
                txt_file = AB_fields_dir + '/' + filename + field + '.txt'
                linguamatics_i2e_object.insert_field(i2qy_file, txt_file)
        linguamatics_i2e_object.logout()
        
    #
    def _ohsu_nlp_templates_setup(self):
        static_data = self.static_data_object.get_static_data()
        directory_manager = static_data['directory_manager']
        ohsu_nlp_preprocessing_data_out_dir = \
            directory_manager.pull_directory('ohsu_nlp_preprocessing_data_out')
        linguamatics_i2e_preprocessing_data_out_dir = \
            directory_manager.pull_directory('linguamatics_i2e_preprocessing_data_out')
        keywords_file = self.dynamic_data_manager.keywords_file()
        keywords = read_txt_file(keywords_file)
        keywords_regexp = _create_keywords_regexp(keywords)
        text_dict = \
            _create_text_dict_preprocessing_data_out(linguamatics_i2e_preprocessing_data_out_dir,
                                                     keywords_regexp)
        self.template_data_dir = ohsu_nlp_preprocessing_data_out_dir
        self.template_text_dict = text_dict
        
    #
    def _project_imports(self):
        static_data = self.static_data_object.get_static_data()
        project_name = static_data['project_name']
        import_cmd = 'from projects_lib.' + project_name + '.py.' + \
                     project_name.lower() + \
                     '_performance_data_manager_class import ' + project_name + \
                     '_performance_data_manager as Performance_data_manager'
        try:
            exec(import_cmd, globals())
        except Exception:
            traceback.print_exc()
        try:
            import_cmd = 'from projects_lib.' + project_name + '.py.' + \
                         project_name.lower() + \
                         '_postprocessor_registry_class import ' + project_name + \
                         '_postprocessor_registry as Postprocessor_registry'
            exec(import_cmd, globals())
            print('Postprocessor_registry: ' + project_name + '_postprocessor_registry')
        except Exception:
            traceback.print_exc()
            import_cmd = 'from processor_lib.registry_lib.postprocessor_registry_class import Postprocessor_registry'
            exec(import_cmd, globals())
            print('Postprocessor_registry: Postprocessor_registry')
            
    #
    def _total_documents(self):
        #static_data = self.static_data_object.get_static_data()
        #datetime_keys = {}
        metadata_json_file = self.metadata_manager.get_metadata_json_file()
        metadata = read_json_file(metadata_json_file)
        num_documents = str(len(metadata.keys()))
        print('number of documents: ' + num_documents)
        
    #
    def _total_patients(self):
        static_data = self.static_data_object.get_static_data()
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
        display_flg = True
        if self.performance_data_manager is not None:
            self.performance_data_manager.get_performance_data(display_flg)
            self.performance_data_manager.display_performance_statistics()
            self.performance_data_manager.write_performance_data()
            self.performance_data_manager.generate_csv_file()
            
    #
    def data_set_summary_info(self):
        self._documents_by_year()
        self._total_documents()
        self._total_patients()
        
    #
    def get_metadata_values(self):
        document_values = []
        patient_values = []
        date_values = []
        metadata_dict_dict = \
            self.metadata_manager.get_metadata_dict_dict()
        for key in metadata_dict_dict.keys():
            document_values.append(metadata_dict_dict[key]['METADATA']['SOURCE_SYSTEM_DOCUMENT_ID'])
            patient_values.append(metadata_dict_dict[key]['METADATA']['MRN_CD'])
            date_values.append(metadata_dict_dict[key]['METADATA']['SPECIMEN_COLLECTED_DATE'])
        document_values = list(set(document_values))
        patient_values = list(set(patient_values))
        date_values = list(set(patient_values))
        return document_values, patient_values, date_values
        
    #
    def linguamatics_i2e_generate_csv_files(self):
        static_data = self.static_data_object.get_static_data()
        directory_manager = static_data['directory_manager']
        data_dir = directory_manager.pull_directory('postprocessing_data_in')
        linguamatics_i2e_object = \
            self.nlp_tool_registry.get_manager('linguamatics_i2e_object')
        linguamatics_i2e_object.generate_csv_files(data_dir)
    
    #
    def linguamatics_i2e_indexer(self):
        static_data = self.static_data_object.get_static_data()
        project_name = static_data['project_name']
        now = datetime.datetime.now()
        index_start_datetime = now.strftime("%d-%b-%y %H:%M:%S.%f")[:-3]
        self.metadata_manager.load_metadata()
        self.metadata_manager.append_nlp_metadata_value('DOCUMENT_SET_INDEXING_START_DATETIME',
                                                        index_start_datetime)
        self.metadata_manager.save_metadata()
        linguamatics_i2e_object = \
            self.nlp_tool_registry.get_manager('linguamatics_i2e_object')
        linguamatics_i2e_object.login()
        linguamatics_i2e_object.make_index_runner(project_name)
        linguamatics_i2e_object.logout()
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
    def linguamatics_i2e_push_resources(self):
        static_data = self.static_data_object.get_static_data()
        directory_manager = static_data['directory_manager']
        static_data['directory_manager'].cleanup_directory('source_data')
        keywords_file = self.dynamic_data_manager.keywords_file()
        preprocessing_data_out_dir = directory_manager.pull_directory('linguamatics_i2e_preprocessing_data_out')
        processing_data_dir = directory_manager.pull_directory('processing_data_dir')
        project_name = static_data['project_name']
        source_data_dir = directory_manager.pull_directory('source_data')
        max_files_per_zip = static_data['max_files_per_zip']
        root_dir_flg = static_data['root_dir_flg']
        linguamatics_i2e_object = \
            self.nlp_tool_registry.get_manager('linguamatics_i2e_object')
        linguamatics_i2e_object.generate_regions_file(preprocessing_data_out_dir,
                                                       processing_data_dir)
        linguamatics_i2e_object.generate_xml_configuation_file(preprocessing_data_out_dir,
                                                                processing_data_dir)
        linguamatics_i2e_object.login()
        linguamatics_i2e_object.push_resources(project_name, keywords_file,
                                                preprocessing_data_out_dir,
                                                processing_data_dir, source_data_dir,
                                                max_files_per_zip, root_dir_flg)
        linguamatics_i2e_object.logout()
        
    #
    def linguamatics_i2e_push_queries(self):
        static_data = self.static_data_object.get_static_data()
        directory_manager = static_data['directory_manager']
        max_files_per_zip = static_data['max_files_per_zip']
        project_name = static_data['project_name']
        general_queries_dir = \
            directory_manager.pull_directory('linguamatics_i2e_general_queries_dir')
        processing_data_dir = \
            directory_manager.pull_directory('processing_data_dir')
        project_queries_dir = \
            directory_manager.pull_directory('linguamatics_i2e_project_queries_dir')
        linguamatics_i2e_object = \
            self.nlp_tool_registry.get_manager('linguamatics_i2e_object')
        linguamatics_i2e_object.generate_query_bundle_file(project_name, general_queries_dir,
                                                            processing_data_dir, 
                                                            project_queries_dir, 
                                                            max_files_per_zip)
        linguamatics_i2e_object.fix_queries(general_queries_dir)
        linguamatics_i2e_object.fix_queries(project_queries_dir)
        self._ohsu_nlp_templates_setup()
        self._ohsu_nlp_templates_generate_AB_fields()
        linguamatics_i2e_object.login()
        linguamatics_i2e_object.push_queries(processing_data_dir)
        self._ohsu_nlp_templates_push_AB_fields()
        linguamatics_i2e_object.logout()
        
    #
    def melax_clamp_run_pipeline(self):
        melax_clamp_manager = \
            self.nlp_tool_registry.get_manager('melax_clamp_manager')
        melax_clamp_manager.run_pipeline()
            
    #
    def ohsu_nlp_templates_post_i2e_linguamatics_setup(self):
        static_data = self.static_data_object.get_static_data()
        directory_manager = static_data['directory_manager']
        data_dir = directory_manager.pull_directory('postprocessing_data_in')
        if 'sections.csv' in os.listdir(data_dir):
            sections = []
            with open(os.path.join(data_dir, 'sections.csv')) as f:
                csv_reader = csv.reader(f)
                for row in csv_reader:
                    sections.append(row)
            text_dict = _create_text_dict_postprocessing_data_in(sections)
        else:
            text_dict = None
        self.template_data_dir = data_dir
        self.template_text_dict = text_dict
        
    #
    def ohsu_nlp_templates_run_simple_templates(self):
        static_data = self.static_data_object.get_static_data()
        project_name = static_data['project_name']
        directory_manager = static_data['directory_manager']
        data_dir = directory_manager.pull_directory('postprocessing_data_in')
        ohsu_nlp_template_manager = \
            self.nlp_tool_registry.get_manager('ohsu_nlp_template_manager')
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
            template_manager = Template_manager(self.static_data_object)
            ohsu_nlp_template_manager.clear_simple_template_output()
            ohsu_nlp_template_manager.run_simple_template(template_manager, 
                                                          self.template_text_dict)
            filename, extension = os.path.splitext(file)
            filename = re.sub('_simple_template_manager_class', '', filename)
            ohsu_nlp_template_manager.write_simple_template_output(template_manager,
                                                            data_dir,
                                                            filename + '.csv')
        
    #
    def postperformance(self):
        static_data = self.static_data_object.get_static_data()
        directory_manager = static_data['directory_manager']
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
            production_data_file = directory_manager.pull_directory('production_data_dir')  + '/' + \
                                   static_data['project_name'] + '.json'                     
            write_file(production_data_file, documents_wrapper, True, True)
            performance_data_file = directory_manager.pull_directory('production_data_dir')  + '/' + \
                                    static_data['project_name'] + '.performance.json'
            write_file(performance_data_file, performance_statistics_dict, False, False)

    #
    def postprocessor(self):
        static_data = self.static_data_object.get_static_data()
        directory_manager = static_data['directory_manager']
        data_dir = directory_manager.pull_directory('postprocessing_data_in')
        filelist = os.listdir(data_dir)
        linguamatics_i2e_object = \
            self.nlp_tool_registry.get_manager('linguamatics_i2e_object')
        sections_data_dict = \
            linguamatics_i2e_object.generate_data_dict(data_dir, 'sections.csv')
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
                data_dict = \
                    linguamatics_i2e_object.generate_data_dict(data_dir, filename)
                self.postprocessor_registry.push_data_dict(filename, data_dict,
                                                           sections_data_dict)
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
            directory_manager.pull_directory('processing_base_dir')
        data_out = directory_manager.pull_directory('postprocessing_data_out')
        for data_dict in merged_data_dict_list:
            if self.nlp_data_key in data_dict.keys():
                if bool(data_dict[self.nlp_data_key]):
                    outdir = data_out
                    filename = data_dict['DOCUMENT_ID'] + '.json'
                    data_dict.pop('DOCUMENT_ID', None)
                    file = os.path.join(outdir, filename)
                    filename = file.replace(processing_base_dir + '/', '')
                    self.json_manager_registry[filename] = \
                        Json_manager(self.static_data_object, file)
                    self.json_manager_registry[filename].write_file(data_dict)
        
    #
    def preperformance(self):
        static_data = self.static_data_object.get_static_data()
        directory_manager = static_data['directory_manager']
        load_dir = \
            directory_manager.pull_directory('postprocessing_data_out')
        data = {}
        for filename in os.listdir(load_dir):
            json_file = Json_manager(self.static_data_object,
                                     os.path.join(load_dir, filename))
            key = filename[0:-5]
            data[key] = json_file.read_json_file()
        filename = static_data['project_name'] + '/' + \
                   static_data['project_subdir'] + '/' + \
                   static_data['project_name'] + '.json'
        self.json_manager_registry[filename].write_performance_data_to_package_json_file(data)
    
    #
    def preprocessor_full(self, password, start_idx):
        static_data = self.static_data_object.get_static_data()
        num_processes = self.raw_data_manager.get_number_of_processes()
        
        # Kludge to get around memory issue in processor
        i2e_version = self.i2e_version
        # Kludge to get around memory issue in processor
        
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
        num_docs_preprocessed = 0
        processes = []
        argument_queues = []
        return_queues = []
        for process_idx in range(num_processes):
            aq = multiprocessing.Queue()
            rq = multiprocessing.Queue()
            w = Preprocessing_worker(self.static_data_object,
                                     self.preprocessor_registry,
                                     self.nlp_tool_registry)
            p = multiprocessing.Process(target=w.process_raw_data, args=(aq, rq,))
            processes.append(p)
            argument_queues.append(aq)
            return_queues.append(rq)
        for process_idx in range(num_processes):
            processes[process_idx].start()
        doc_idx_offset = 0
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
                print('invalid file extension: ' + extension)  
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
                dynamic_data_manager_copy = deepcopy(self.dynamic_data_manager)
                raw_data_manager_copy = deepcopy(self.raw_data_manager)
                raw_data_manager_copy.select_process(process_idx)
                metadata_manager_copy = deepcopy(self.metadata_manager)
                argument_dict = {}
                argument_dict['dynamic_data_manager'] = \
                    dynamic_data_manager_copy
                argument_dict['metadata_manager'] = metadata_manager_copy
                argument_dict['num_processes'] = num_processes
                argument_dict['process_idx'] = process_idx
                argument_dict['raw_data_manager'] = raw_data_manager_copy
                argument_dict['start_idx'] = start_idx
                argument_dict['i2e_version'] = i2e_version
                argument_dict['password'] = password
                argument_queues[process_idx].put(argument_dict)
            for process_idx in range(num_processes):
                ret = return_queues[process_idx].get()
                if ret[2] > 0:
                    self.dynamic_data_manager.merge_copy(ret[0])
                    self.metadata_manager.merge_copy(ret[1])
                    num_docs_preprocessed += ret[2]
            for process_idx in range(num_processes):
                argument_dict = {}
                argument_dict['command'] = 'stop'
                argument_queues[process_idx].put(argument_dict)
                processes[process_idx].join()
        print('Number of documents preprocessed: ' + str(num_docs_preprocessed))
        self.dynamic_data_manager.generate_keywords_file()
        self.metadata_manager.save_metadata()
        
    #
    def preprocessor_metadata(self, password, start_idx):
        static_data = self.static_data_object.get_static_data()
        num_processes = self.raw_data_manager.get_number_of_processes()
        
        # Kludge to get around memory issue in processor
        i2e_version = self.i2e_version
        # Kludge to get around memory issue in processor
        
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
        doc_idx_offset = 0
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
                print('invalid file extension: ' + extension)  
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
                metadata = \
                    self._get_document_metadata(raw_data_manager_copy,
                                                i2e_version, process_idx,
                                                start_idx, password)
                for document_idx in metadata.keys():
                    self.metadata_manager.append_metadata_dicts(str(document_idx),
                                                                metadata[document_idx]['source_metadata'],
                                                                metadata[document_idx]['nlp_metadata'])
                num_docs_preprocessed = 0
        print('Number of documents preprocessed: ' + str(num_docs_preprocessed))
        self.metadata_manager.save_metadata()