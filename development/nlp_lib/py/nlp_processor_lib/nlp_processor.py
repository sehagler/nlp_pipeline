# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 09:52:09 2020

@author: haglers
"""

#
from datetime import datetime
import math
from matplotlib import pyplot as plt
import os
import pickle
import random
import re

#
from nlp_lib.py.process_lib.process_manager_class import Process_manager
from nlp_lib.py.software_lib.software_manager_class import Software_manager
from nlp_lib.py.static_data_lib.static_data_manager_class \
    import Static_data_manager
from tool_lib.py.query_tools_lib.date_tools import datetime2matlabdn
from tool_lib.py.server_lib.server_manager_class import Server_manager

#
class Nlp_processor(object):
    
    #
    def __init__(self):
        pass
    
    #
    def _create_managers(self, server, root_dir, project_subdir, user, password):
        self.static_data_manager = \
            Static_data_manager(server, project_subdir, user, root_dir)
        server_manager = Server_manager(self.static_data_manager, password)
        self.process_manager = Process_manager(self.static_data_manager,
                                               server_manager,
                                               password)
        
    #
    def _project_imports(self, server, root_dir, project_name):
        import_cmd = 'from projects_lib.' + project_name + '.py.' + \
                     project_name.lower() + \
                     '_static_data_manager_class import ' + project_name + \
                     '_static_data_manager as Static_data_manager'
        exec(import_cmd, globals())
        
    #
    def _quality_control(self):
        document_values, patient_values, date_values = \
            self.process_manager.get_metadata_values()
        num_documents = len(list(set(document_values)))
        num_days = round(date_values[-1] - date_values[0])
        num_patients = len(patient_values)
        plt.hist(date_values, bins=num_days)
        print('number of documents: %d' % num_documents)
        print('number of patients: %d' % num_patients)
    
    #
    def download_queries(self):
        self.process_manager.download_queries()
    
    #
    def generate_training_data_sets(self, password):
        static_data = self.static_data_manager.get_static_data()
        doc_fraction_list = []
        for key in static_data['raw_data_files'].keys():
            doc_fraction_list.append(static_data['raw_data_files'][key]['DOCUMENT_FRACTION'])
        doc_fraction_list = list(set(doc_fraction_list))
        if len(doc_fraction_list) == 1:
            doc_fraction = doc_fraction_list[0]
        else:
            print('Multiple document fractions detected!')
        num_groups = 4
        self.process_manager.preprocessor(password, 0, False)
        document_values, patient_values, date_values = \
            self.process_manager.get_metadata_values()
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
    def linguamatics_i2e_postqueries(self, project_subdir):
        static_data = self.static_data_manager.get_static_data()
        static_data['directory_manager'].cleanup_directory('postprocessing_data_out')
        self.process_manager.linguamatics_i2e_generate_csv_files()
        self.process_manager.postprocessor()
        self.process_manager.preperformance()
        if project_subdir == 'test':
            self.process_manager.calculate_performance()
        self.process_manager.postperformance()
        
    #
    def linguamatics_i2e_prequeries(self, password, start_idx=0, cleanup_flg=True):
        if start_idx >= 0:
            if start_idx > 0:
                cleanup_flg = False
            static_data = self.static_data_manager.get_static_data()
            if start_idx > 0:
                cleanup_flg = False
            if cleanup_flg:
                static_data['directory_manager'].cleanup_directory('preprocessing_data_out')
            self.process_manager.preprocessor(password, start_idx, True)
            self.process_manager.linguamatics_i2e_generate_resource_files()
            self.process_manager.linguamatics_i2e_fix_queries()
            self.process_manager.linguamatics_i2e_preindexer()
            self.process_manager.linguamatics_i2e_indexer()
            self.process_manager.linguamatics_i2e_postindexer()
    
    #
    def move_software(self):
        if self.root_dir_flg == 'X':
            dest_drive = 'Z'
        elif self.root_dir_flg == 'Z':
            dest_drive = 'X'
        else:
            print('bad root directory')
        self.nlp_software.copy_x_nlp_software_to_nlp_sandbox(dest_drive)
        
    #
    def ohsu_nlp_templates(self, password, project_subdir, start_idx=0,
                           cleanup_flg=True):
        if start_idx >= 0:
            if start_idx > 0:
                cleanup_flg = False
            static_data = self.static_data_manager.get_static_data()
            if start_idx > 0:
                cleanup_flg = False
            if cleanup_flg:
                pass
                static_data['directory_manager'].cleanup_directory('preprocessing_data_out')
            self.process_manager.preprocessor(password, start_idx, True)
            self.process_manager.ohsu_nlp_templates_run()
        
    #
    def process_manager(self, server, root_dir, project_subdir, project_name,
                        user, password):
        if root_dir == 'server':
            if server == 'development':
                root_dir = 'dev_server'
            elif server == 'production':
                root_dir = 'prod_server'
        self._project_imports(server, root_dir, project_name)
        self._create_managers(server, root_dir, project_subdir, user, password)
        
    #
    def software_manager(self, user, password, root_dir_flg):
        self.root_dir_flg = root_dir_flg
        static_data_manager = \
            Static_data_manager('development', None, None, user, root_dir_flg)
        server_manager = Server_manager(static_data_manager, password)
        self.nlp_software = Software_manager(static_data_manager, server_manager)