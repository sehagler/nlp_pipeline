# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 09:52:09 2020

@author: haglers
"""

#
import datetime
import math
import pickle
import plotext as plt
import random

#
from nlp_pipeline_lib.manager_lib.metadata_lib.metadata_manager_class \
    import Metadata_manager
from nlp_pipeline_lib.manager_lib.process_lib.process_manager_class \
    import Process_manager
from nlp_pipeline_lib.manager_lib.software_lib.software_manager_class \
    import Software_manager
from nlp_pipeline_lib.object_lib.directory_lib.directory_object_class \
    import Directory_object
from nlp_pipeline_lib.object_lib.logger_lib.logger_object_class \
    import Logger_object
from nlp_pipeline_lib.registry_lib.remote_lib.remote_registry_class \
    import Remote_registry
from static_data_lib.object_lib.static_data_object_class \
    import Static_data_object
from tools_lib.processing_tools_lib.file_processing_tools \
    import read_json_file
    
#
def _total_documents(metadata_json_file):
    #static_data = self.static_data_object.get_static_data()
    #datetime_keys = {}
    metadata = read_json_file(metadata_json_file)
    num_documents = str(len(metadata.keys()))
    return num_documents
    
#
def _total_patients(patient_identifiers, metadata_json_file):
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
    return num_patients

#
class Pipeline_object(object):
    
    #
    def __init__(self):
        pass
    
    #
    def _create_objects(self, server, root_dir, project_subdir, user,
                         password):
        self.static_data_object = \
            Static_data_object(server, user, root_dir,
                                project_subdir=project_subdir)
        static_data = self.static_data_object.get_static_data()
        self.directory_object = Directory_object(static_data, root_dir)
        self.software_dir = self.directory_object.pull_directory('software_dir')
        log_dir = self.directory_object.pull_directory('log_dir')
        self.logger_object = Logger_object(log_dir)
        self.update_static_data_object = \
            Static_data_object('development', user, root_dir)
            
    #
    def _create_managers(self):
        self.metadata_manager = Metadata_manager(self.static_data_object,
                                                 self.directory_object,
                                                 self.logger_object)
        
    #
    def _create_registries(self, root_dir, password):
        self.remote_registry = \
            Remote_registry(self.static_data_object, 
                            self.update_static_data_object,
                            self.directory_object, self.logger_object,
                            root_dir, password)
            
    #
    def _data_set_summary_info(self):
        static_data = self.static_data_object.get_static_data()
        patient_identifiers = set(static_data['patient_identifiers'])
        metadata_json_file = self.metadata_manager.get_metadata_json_file()
        self._documents_by_year(metadata_json_file)
        num_documents = _total_documents(metadata_json_file)
        log_text = 'number of documents: ' + num_documents
        self.logger_object.print_log(log_text)
        num_patients = _total_patients(patient_identifiers, metadata_json_file)
        log_text = 'number of patients: ' + num_patients
        self.logger_object.print_log(log_text)
        
    #
    def _documents_by_year(self, metadata_json_file):
        static_data = self.static_data_object.get_static_data()
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
    def _get_metadata_values(self):
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
    def _project_imports(self, server, root_dir, project_name):
        import_cmd = 'from projects_lib.' + project_name + '.py.' + \
                     project_name.lower() + \
                     '_static_data_object_class import ' + project_name + \
                     '_static_data_object as Static_data_object'
        exec(import_cmd, globals())
        
    #
    def cleanup_directory(self, directory_label):
        self.process_manager.cleanup_directory(directory_label)
    
    #
    def download_queries(self):
        self.process_manager.download_queries()
    
    #
    def generate_training_data_sets(self, password):
        static_data = self.static_data_object.get_static_data()
        doc_fraction_list = []
        for key in static_data['raw_data_files'].keys():
            doc_fraction_list.append(static_data['raw_data_files'][key]['DOCUMENT_FRACTION'])
        doc_fraction_list = list(set(doc_fraction_list))
        if len(doc_fraction_list) == 1:
            doc_fraction = doc_fraction_list[0]
        else:
            log_text = 'Multiple document fractions detected!'
            self.logger_object.print_log(log_text)
        num_groups = 4
        self.process_manager.preprocessor_metadata(password, 0)
        document_values, patient_values, date_values = \
            self._get_metadata_values()
        num_documents = len(document_values)
        random.shuffle(document_values)
        number_training_docs = math.floor(doc_fraction * len(document_values))
        training_docs = document_values[:number_training_docs]
        with open('training_docs.pkl', 'wb') as f:
            pickle.dump([document_values, training_docs], f)
        random.shuffle(patient_values)
        patients_per_group = math.floor(len(patient_values)/num_groups)
        training_groups = []
        for i in range(num_groups-1):
            training_groups.append(patient_values[0:patients_per_group])
            patient_values = patient_values[patients_per_group:]
        training_groups.append(patient_values)
        with open('training_groups.pkl', 'wb') as f:
            pickle.dump(training_groups, f)
            
    #
    def initialize_metadata(self):
        self.metadata_manager.save_metadata()
            
    #
    def linguamatics_i2e_indexer(self):
        self.process_manager.linguamatics_i2e_push_resources()
        self.process_manager.linguamatics_i2e_indexer()
        self.process_manager.linguamatics_i2e_postindexer()
        #self.process_manager.linguamatics_i2e_push_queries()
        
    #
    def linguamatics_i2e_postqueries(self, project_subdir):
        self.process_manager.linguamatics_i2e_generate_csv_files()
        self.process_manager.ohsu_nlp_templates_run_simple_templates()
        self.process_manager.postprocessor()
        self.process_manager.preperformance()
        if project_subdir == 'test':
            self.process_manager.calculate_performance()
        self.process_manager.postperformance()
        
    #
    def linguamatics_i2e_prequeries(self, password):
        self.process_manager.preprocessor_full(password)
        self._data_set_summary_info()
        
    #
    def linguamatics_i2e_push_queries(self):
        self.process_manager.linguamatics_i2e_push_queries()
            
    #
    def melax_clamp_run_pipeline(self):
        self.process_manager.melax_clamp_run_pipeline()
    
    #
    def move_software(self):
        if self.root_dir == 'X':
            dest_drive = 'Z'
        elif self.root_dir == 'Z':
            dest_drive = 'X'
        else:
            log_text = 'bad root directory'
            self.logger.print_log(log_texft)
        self.nlp_software.copy_x_nlp_software_to_nlp_sandbox(dest_drive,
                                                             software_dir)
        
    #
    def ohsu_nlp_templates_generate_AB_fields(self):
        self.process_manager.ohsu_nlp_templates_setup()
        self.process_manager.ohsu_nlp_templates_generate_AB_fields()
        
    #
    def ohsu_nlp_templates_run_templates(self, password, project_subdir):
        self.process_manager.set_metadata()
        self.process_manager.preprocessor_full(password)
        self.process_manager.ohsu_nlp_templates_setup()
        self.process_manager.ohsu_nlp_templates_run_simple_templates()
        self.process_manager.postprocessor()
        self.process_manager.preperformance()
        if project_subdir == 'test':
            self.process_manager.calculate_performance()
        self.process_manager.postperformance()
        
    #
    def process_manager(self, server, root_dir, project_subdir, project_name,
                        user, password):
        if root_dir == 'server':
            if server == 'development':
                root_dir = 'dev_server'
            elif server == 'production':
                root_dir = 'prod_server'
        self._project_imports(server, root_dir, project_name)
        self._create_objects(server, root_dir, project_subdir, user, password)
        self._create_managers()
        self._create_registries(root_dir, password)
        self.process_manager = Process_manager(self.static_data_object,
                                               self.directory_object,
                                               self.logger_object,
                                               self.metadata_manager,
                                               self.remote_registry,
                                               password)
        
    #
    def software_manager(self, root_dir, user, password):
        self.root_dir = root_dir
        self._create_objects(None, root_dir, None, user, password)
        self._create_registries(root_dir, password)
        server_manager = self.remote_registry.get_manager('update_manager')
        self.nlp_software = Software_manager(self.update_static_data_object,
                                             self.logger_object,
                                             server_manager)